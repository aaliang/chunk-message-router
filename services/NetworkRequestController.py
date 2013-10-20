from services.AbstractController import AbstractController
from utils.MessageRelays import MessageRelays
from utils.SubnetUtil import SubnetUtil
from types import ListType, StringType
import json

class NetworkRequestController(AbstractController):
    """
        NetworkRequestController
    """

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

        all_chunks = NetworkRequestController.__get_request_chunks_dp(recipients)
#         all_chunks = NetworkRequestController.__get_request_chunks_greedy(recipients)
        #all chunks is a dictionary keyed by throughput types. The values are Lists of Lists of recipients.
        routes = []

        try:
            for tp_class, chunks in all_chunks.items():
                if len(chunks) > 254:
                    raise Exception("this is broken")
                ip_generator = SubnetUtil.gen_ip(tp_class.subnet_prefix)

                for chunk in chunks:
                    routes.append({
                     "ip": ip_generator.next(),
                     "recipients": chunk
                     })
        except Exception, e:
            print e
        
        
        return json.dumps({'message': message,
                'routes': routes
                })
        
    @staticmethod
    def __get_request_chunks_dp(recipients):
        """
            Uses a dynamic-programming approach to chunk up recipients into message
            relay groups.
        """
        assert isinstance(recipients, ListType)
        
        states = [None for _ in xrange(len(recipients) + 1)]
        states[0] = 0
        throughput_sizes = set(x.throughput for x in MessageRelays.ALL_DESCENDING)
        
        def min_key(throughput_set):
            """
                Inner function to be used as the key function for min(). THe size of the object
                {throughput_set} is determined by summing the values
                
                @type throughput_set: DictType
                @precondition: all(isinstance(x, IntType) for x in throughput_set.values())
            """
            
            if throughput_set:
                return sum(throughput_set.values())
            else:
                return float('inf')

        for i, state in enumerate(states[1:]):
            
            index = i+1
            if index in throughput_sizes:
                states[index] = {MessageRelays.get_relay_type_by_throughput(index): 1}
            else:
                slice = [states[i-x.throughput+1] for x in MessageRelays.ALL_DESCENDING]
                minimal_sum = min(slice, key=min_key)

                states[index] = minimal_sum.copy()
#                 throughput_val = index - sum(x for x in minimal_sum.values())
                throughput_val =  index - sum(k.throughput * v for (k,v) in minimal_sum.items())
                relay_type = MessageRelays.get_relay_type_by_throughput(throughput_val)
                assert relay_type
                if relay_type in states[index]:
                    states[index][relay_type] += 1
                else:
                    states[index][relay_type] = 1
        
        chunk_count = states[len(states)-1]
        all_chunks = {}
        start_index = 0
        for rtype, num  in chunk_count.items():
            chunks_array = []
            for i in xrange(num):
                end_index = start_index + rtype.throughput
                chunks_array.append(recipients[start_index:end_index])
                start_index = end_index
            all_chunks[rtype] = chunks_array

        return all_chunks

    @staticmethod
    def __get_request_chunks_greedy(recipients):
        """
            Uses a greedy approach to chunk up recipients into message relay groups.
            In the general case, this is an approximation. However it also finds the
            solution in O(1).
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
