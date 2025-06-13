from enum import Enum

class _AuthRoutes(Enum):
    LOGIN = ('login', 'auth/login.html')
    REGISTER = ('register', 'auth/register.html')
    LOGOUT = ('logout', None)

    def __init__(self, url_name, template_path):
        self.url_name = url_name
        self.template_path = template_path

class _TasksRoute(Enum):
    LIST = ('task_list', 'protected/tasks.html')

    def __init__(self, url_name, template_path):
        self.url_name = url_name
        self.template_path = template_path

class _HomeRoute(Enum):
    HOME = ('home', 'protected/home.html')

    def __init__(self, url_name, template_path):
        self.url_name = url_name
        self.template_path = template_path

class _PublicRoutes:
    LOGIN = _AuthRoutes.LOGIN
    REGISTER = _AuthRoutes.REGISTER
    LOGOUT = _AuthRoutes.LOGOUT

class _ProtectedRoutes:
    HOME = _HomeRoute.HOME

    # Tasks paths
    TASKS = _TasksRoute.LIST

class RouteGroup:
    AUTH = _PublicRoutes()
    PROTECTED = _ProtectedRoutes()