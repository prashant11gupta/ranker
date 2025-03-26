class ProductRequest:
    def __init__(self, user_info=None):
        self.user_info = user_info or {}


class ProductResponse:
    def __init__(self, recommended_products, message="Products recommended successfully"):
        self.status = "success"
        self.message = message
        self.data = {
            "recommended_products": recommended_products
        }

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }
