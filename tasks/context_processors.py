from .constants import RouteGroup

def routes_context(request):
    return {
        'routes': RouteGroup
    }