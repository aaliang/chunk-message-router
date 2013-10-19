from services.NetworkRequestController import NetworkRequestController

#TODO: remove me

class Root(object):
    """
        Concrete implementation of the application root structure
    """

    def __init__(self):
        self.setup_routes()
        
    def setup_routes(self):
        """sets up routes on this instance"""
        self.network_request = NetworkRequestController()
