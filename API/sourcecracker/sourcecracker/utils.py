from sourcecracker.middlewares.current_user import CurrentUserMiddleware


def current_user():
    return CurrentUserMiddleware.get_current_user()
