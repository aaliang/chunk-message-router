from utils.MessageRelay import MessageRelay

class MessageRelays(object):
    """
        Static enumeration of the categories of MessageRelays
    """
    
    SMALL = MessageRelay("small", "10.0.1.0/24", 1)
    """Representation of a small relay"""
    
    MEDIUM = MessageRelay("medium", "10.0.2.0/24", 5)
    """Representation of a medium relay"""

    LARGE = MessageRelay("large", "10.0.3.0/24", 10)
    """Representation of a large relay"""

    SUPER = MessageRelay("super", "10.0.4.0/24", 25)
    """Representation of a super relay"""
    
    ALL_DESCENDING = (SUPER, LARGE, MEDIUM, SMALL,)
    """Tuple of all the known message relay types. Sorted, in ascending order, by throughput size"""
    
    __throughput_lookup = dict((k.throughput, k) for k in ALL_DESCENDING)
    
    @staticmethod
    def get_relay_type_by_throughput(throughput):
        """
            Returns the MessageRelay corresponding to the throughput if it exists.
            If it does not exist, return None

            @type size: IntType
            @rtype: MessageRelay
        """
        if throughput in MessageRelays.__throughput_lookup:
            return MessageRelays.__throughput_lookup[throughput]
        else:
            return None
