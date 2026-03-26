from .current_user import set_current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else None
        set_current_user(user)
        response = self.get_response(request)
        set_current_user(None)
        return response


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        is_auth_page = request.path.startswith("/accounts/")
        if request.user.is_authenticated or is_auth_page:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

        return response
