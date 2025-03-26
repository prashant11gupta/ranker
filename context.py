# UserContext holds extracted user-related information for personalization
from db.user import user_db


class UserContext:
    def __init__(self, user_id=None, location="US", logged_in=False):
        self.user_id = user_id if user_db.get(user_id) else None  # Unique identifier for the user
        self.location = location  # User's location (default is "US")
        self.logged_in = True if self.user_id else False  # Flag to check if the user is logged in


# ContextResolver is responsible for extracting context from the incoming request
class ContextResolver:
    def resolve(self, request):
        # Extract user information dictionary from the request
        user = request.user_info

        # Create and return a UserContext object using provided or default values
        return UserContext(
            user_id=user.get("user_id"),  # Extract user_id if available
            location=user.get("location", "US"),  # Use provided location or default to "US"
            logged_in=user.get("logged_in", False)  # Use provided login status or
        )