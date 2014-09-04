from types import StringType

class SubnetUtil(object):
    """
        Utility class intended to hold helper methods with dealing with subnets
    """
    
    @staticmethod
    def gen_ip(subnet):
        """
            Generator yielding all possible ip values on a given subnet mask
        
            @type subnet: StringType
            @param subnet: Subnet address is represented by the <ip>/<bits>
        """

        assert isinstance(subnet, StringType)
        subnet_split = subnet.split("/")
        sig_bits = int(subnet_split[1])
        prefixes = [int(x) for x in subnet_split[0].split(".")]
        
        len_prefixes = len(prefixes)
        assert len_prefixes == 4
        
        cursor_position = sig_bits/8
        carry_over = sig_bits % 8
        #if the subnet mask ends in the middle of a byte, we'll need to calculate the maximum
        #value of that 'partial' byte
        if carry_over > 0:
            unmasked_bits = 8-carry_over
            partial_max = ((1 << (unmasked_bits+1)) - 1) + prefixes[cursor_position]
        else:
            partial_max = SubnetUtil.MAXIMUM_IP_BYTE_VALUE
        
        #maxes is an array that will contain the maximum possible value of each byte in the IP
        maxes = [prefixes[x] for x in xrange(cursor_position)]
        #the numbers contained in the mask (and not part of the partial) are the absolute maxes
        
        maxes.append(partial_max)
        
        #everything to the right of the partial will have a max value of 255
        
        maxes.extend([SubnetUtil.MAXIMUM_IP_BYTE_VALUE for _ in xrange(cursor_position+1, len_prefixes)])

        def rebuild_ip(index, ip_parts, prefixes, maxes):
            """
                recursively builds ips according to their prefix and maxes
            """
            for i in xrange(prefixes[index], maxes[index]+1):
                if i == 0 and index == SubnetUtil.LEAST_SIGNIFICANT_IP_BYTE_INDEX:
                    continue #IP addresses cannot end in 0
                ip_parts[index] = i
                if index < len_prefixes-1:
                    for i in rebuild_ip(index+1, ip_parts, prefixes,maxes):
                        yield i
                else:
                    yield ".".join(str(x) for x in ip_parts)

        temp_ip = prefixes[:]
        for x in reversed(xrange(cursor_position, len_prefixes)):
            for ip in rebuild_ip(x, temp_ip, prefixes, maxes):
                yield ip

    LEAST_SIGNIFICANT_IP_BYTE_INDEX = 3
    """
        The index of the least significant byte of an ip address is split by the period delimiters
        eg:
         10.000.000.001
        [0].[1].[2].[3]
    """
    
    MAXIMUM_IP_BYTE_VALUE = 255
    """
        The maximum value that each byte in an IP address can have
    """
