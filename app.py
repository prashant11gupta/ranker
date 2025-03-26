from flasgger import Swagger
from flask import Flask, request, jsonify

from agent import ProductServingAgent
from protocol import ProductRequest, ProductResponse
from validation.schema import RecommendationRequest

# Initialize Flask app and Swagger docs
app = Flask(__name__)
swagger = Swagger(app)
agent = ProductServingAgent()


# Endpoint for product recommendation
@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Get personalized product recommendations
    ---
    tags:
      - Recommendation
    parameters:
      - in: body
        name: request
        required: true
        schema:
          type: object
          properties:
            top_n:
              type: integer
              default: 4
            user:
              type: object
              properties:
                user_id:
                  type: integer
                location:
                  type: string
    responses:
      200:
        description: List of recommended products
        schema:
          type: object
          properties:
            recommended_products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  brand:
                    type: string
                  category:
                    type: string
                  price:
                    type: number
    """
    try:
        json_data = request.get_json()
        validated_request = RecommendationRequest(**json_data)

        # Build protocol-level request
        product_request = ProductRequest(user_info=validated_request.user.model_dump())
        recommended_products = agent.handle_request(product_request, top_n=validated_request.top_n)

        response = ProductResponse(recommended_products)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Failed to recommend products: {str(e)}",
            "data": None
        }
        return jsonify(error_response), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
