# Import product catalog, context resolver, and model logic
from db.product_catalog import product_catalog_db
from context import ContextResolver, UserContext
from model import ProductModel


# Main serving agent that handles product personalization
class ProductServingAgent:
    def __init__(self):
        # Initialize context resolver and product model with the in-memory product catalog
        self.context_resolver = ContextResolver()
        self.model = ProductModel(product_catalog_db)

    def handle_request(self, request, top_n=3):
        # Resolve user context from the request (e.g., user_id, preferences, login state)
        user_context = self.context_resolver.resolve(request)
        # Select ranking strategy based on context (logged-in vs guest)
        return self.select_strategy(user_context, top_n)

    def select_strategy(self, user_context: UserContext, top_n):
        # For logged-in users, generate personalized recommendations
        if user_context.logged_in:
            recommended_products = self.model.recommend_products(user_context, top_n)

            # If less than 3 personalized products are found, fill with price-ranked items
            if len(recommended_products) < top_n:
                # Collect product IDs already in recommendations
                unique_ids = {product["id"] for product in recommended_products}

                # Get fallback products ranked by price (lowest first)
                filler_recommendations = self.model.rank_by_price(top_n)
                unique_filler_ids = {product["id"] for product in filler_recommendations}

                # Identify filler products not already in personalized recommendations
                diff_ids = unique_filler_ids - unique_ids

                # Add filler products until we have at least 3 total
                for item in filler_recommendations:
                    if len(recommended_products) >= top_n:
                        break
                    if item["id"] in diff_ids:
                        recommended_products.append(item)

            # Return final curated list of products
            return recommended_products

        else:
            # For guest users, return top products ranked by price
            return self.model.rank_by_price(top_n)
