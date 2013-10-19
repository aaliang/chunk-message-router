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
