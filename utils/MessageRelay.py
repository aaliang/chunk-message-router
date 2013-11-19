from types import IntType, StringType

class MessageRelay(object):
    """
        Represents a type of message relay router. Each message relay type has a name, a subnet mask, and a throughput
    """
    
    
    def __init__(self, relay_name, subnet_prefix, throughput):
        """
            @type relay_name: StringType
            @type subnet_prefix: StringType
            @type throughput: IntType
            
            @param subnet_prefix: CIDR notation of a subnet mask
            @param throughput: The number of chunks the relay is capabale of passing through
        """
        assert isinstance(relay_name, StringType)
        assert isinstance(subnet_prefix, StringType)
        assert isinstance(throughput, IntType)
        
        self.relay_name = relay_name
        self.subnet_prefix = subnet_prefix
        self.throughput = throughput
