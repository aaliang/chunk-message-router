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
        if carry_over > 0:
            unmasked_bits = 8-carry_over
            partial_max = ((1 << (unmasked_bits+1)) - 1) + prefixes[cursor_position]
        else:
            partial_max = 255#default max TODO: use constants
        
        maxes = []
        for x in xrange(cursor_position):
            maxes.append(prefixes[x])
        
        maxes.append(partial_max)
        
        for x in xrange(cursor_position+1, len_prefixes):
            maxes.append(255)

        temp_ip = prefixes[:]

        def rebuild_ip(index, ip_parts, prefixes, maxes):
            """
                recursively builds ips according to their prefix and maxes
            """
            for i in xrange(prefixes[index], maxes[index]+1):
                if i == 0:
                    continue
                ip_parts[index] = i
                if index < len_prefixes-1:
                    for i in rebuild_ip(index+1, ip_parts, prefixes,maxes):
                        yield i
                else:
                    yield ".".join(str(x) for x in temp_ip)


        for x in reversed(xrange(cursor_position, len_prefixes)):
            for ip in rebuild_ip(x, temp_ip, prefixes, maxes):
                yield ip
