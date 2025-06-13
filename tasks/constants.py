# Template paths for the application
class _ProtectedTemplates:
    HOME = 'protected/home.html'
    TASKS = 'protected/tasks.html'
    
class _AuthTemplates:
    LOGIN = 'auth/login.html'
    REGISTER = 'auth/register.html'

class Templates:
    AUTH = _AuthTemplates()
    PROTECTED = _ProtectedTemplates()


# URL patterns for the application
class _ProtectedUrls:
    HOME = 'home'
    TASKS = 'tasks'

class _AuthUrls:
    LOGIN = 'login'
    REGISTER = 'register'
    LOGOUT = 'logout'

class Urls:
    AUTH = _AuthUrls()
    PROTECTED = _ProtectedUrls()