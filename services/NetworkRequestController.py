from services.AbstractController import AbstractController
from utils.MessageRelays import MessageRelays
from types import ListType, StringType
import json

class NetworkRequestController(AbstractController):

    @staticmethod
    def gen_ip(subnet):
        """
            Generator yielding all possible ip values on a given subnet mask
        
            @type subnet: StringType
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

    @staticmethod
    def handle_routing(message, recipients):
        """
            TODO: This contract needs work
            Handles routing decisions for mappings of ips to recipients based on the request
            
            @type message: UnicodeType
            @type recipients: ListType
            @rtype: UnicodeType
            @return: the JSON representation of the response object
        """

        all_chunks = NetworkRequestController.__get_request_chunks(recipients)
        #all chunks is a dictionary keyed by throughput types. The values are Lists of Lists of recipients.
        routes = []

        try:
            for tp_class, chunks in all_chunks.items():
                if len(chunks) > 254:
                    raise Exception("this is broken")
                ip_gen = NetworkRequestController.gen_ip(tp_class.subnet_prefix)

                
                for chunk in chunks:
                    routes.append({
                     "ip": ip_gen.next(),
                     "recipients": chunk
                     })
        except Exception, e:
            print e
        
        
        return json.dumps({'message': message,
                'routes': routes
                })
    
    @staticmethod
    def __get_request_chunks(recipients):
        """
            Uses a greedy approach to chunk up recipients into message relay groups
        """
        assert isinstance(recipients, ListType)
        
        #top-level
        chunks = {}
        
        remaining_length = len(recipients)
        start_index = 0
        
        for relay_type in MessageRelays.ALL_DESCENDING:
            if relay_type.throughput <= remaining_length:
                num_chunks = remaining_length/relay_type.throughput
                
                #TODO low priority: can use a list comprehension
                chunk_array = []
                #chunks of relays of type relay_type
                for _ in xrange(num_chunks):
                    end_index = relay_type.throughput + start_index
                    new_chunk = recipients[start_index:end_index]
                    chunk_array.append(new_chunk)
                    chunks[relay_type] = chunk_array
                    
                    #advance the index pointer to the end
                    start_index = end_index
            
                remaining_length = remaining_length % relay_type.throughput
                if remaining_length == 0:
                    break
        
        return chunks
