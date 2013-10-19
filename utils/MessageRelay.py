from types import IntType, StringType

class MessageRelay(object):
    
    def __init__(self, relay_name, subnet_prefix, throughput):
        """
            @type relay_name: StringType
            @type subnet_prefix: StringType
            @type throughput: IntType
        """
        assert isinstance(relay_name, StringType)
        assert isinstance(subnet_prefix, StringType)
        assert isinstance(throughput, IntType)
        
        self.relay_name = relay_name
        self.subnet_prefix = subnet_prefix
        self.throughput = throughput