# Import user affinity data which contains preferred brands and categories by user ID
from context import UserContext
from db.user_affinities import user_affinities_db
from db.user import user_db


# ProductModel handles logic for ranking and recommending products
class ProductModel:
    def __init__(self, product_catalog):
        # Store the in-memory product catalog
        self.product_catalog = product_catalog

    def rank_by_price(self, top_n):
        """
        Rank products by price in ascending order and return top N cheapest products.
        Used as a default recommendation for guest users.
        """
        return sorted(self.product_catalog, key=lambda x: x['price'])[:top_n]

    def recommend_products(self, user_context: UserContext, top_n):
        affinity = user_affinities_db.get(user_context.user_id, {})
        preferred_brands = set(affinity.get('brands', []))
        preferred_categories = set(affinity.get('categories', []))

        # Get user info (assumes global or passed-in user_info dict)
        user = user_db.get(user_context.user_id, {})
        home_location = user.get("home_state", "")
        user_curr_location = user_context.location
        user_income = user.get("household_income", 50000)  # default to median if missing

        scored_products = []

        for product in self.product_catalog:
            score = 0

            # Affinity-based scoring
            if product['brand'] in preferred_brands:
                score += 2
            if product['category'] in preferred_categories:
                score += 1

            # Location-based scoring (if product has region/locality info)
            if 'location' in product and (product['location'] == user_curr_location or product['location'] == home_location):
                score += 1  # small bonus if product matches user's location

            # Price-based personalization based on income
            price = product['price']
            if user_income >= 100000 and price > 500:
                score += 1  # high-income users prefer premium
            elif user_income < 30000 and price < 100:
                score += 1  # low-income users prefer affordable

            if score > 0:
                scored_products.append((score, product))

        # Sort by score (high to low), then price (low to high)
        scored_products.sort(key=lambda x: (-x[0], x[1]['price']))

        # Return top N products
        return [product for _, product in scored_products[:top_n]]
