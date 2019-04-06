from threading import local

_user = local()


class CurrentUserMiddleware(object):
    def __init__(self, get_response):
        """Init CurrentUserMiddleware with given response."""
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        return self.get_response(request)

    def get_current_user():
        try:
            return _user.value if _user.value.is_authenticated else None
        except AttributeError:
            return None
