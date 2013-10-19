import cherrypy #@UnresolvedImport

class AbstractController(object):
    """
        Abstract base class for HTTP controllers
    """
    
    @staticmethod
    def expose_as_http(func=None, alias=None):
        def http_deco(f):
            expose_func = cherrypy.expose(func, alias)
            f = expose_func(f)
            return f

        return http_deco