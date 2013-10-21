from utils.MessageRelays import MessageRelays
from utils.SubnetUtil import SubnetUtil
from types import ListType, StringType
# import json

class NetworkRequestController(object):
    """
        Static class containing methods to handle network_request API requests
    """

    MAX_RECIPIENTS = 5000
    """The maximum amount of recipients the router can handle"""


    @staticmethod
    def handle_routing(message, recipients):
        """
            TODO: This contract needs work
            Handles routing decisions for mappings of ips to recipients based on the request
            
            @type message: UnicodeType
            @type recipients: ListType
            @rtype: DictType
            @return: the representation of the response object
        """
        #all chunks is a dictionary keyed by throughput types. 
        #the values are Lists of Lists of recipients.

        all_chunks = NetworkRequestController.__get_request_chunks_dp(recipients)
        routes = []
        for tp_class, chunks in all_chunks.items():
#             if len(chunks) > 255:
#                 raise Exception("this is broken")
            ip_generator = SubnetUtil.gen_ip(tp_class.subnet_prefix)

            for chunk in chunks:
                routes.append({
                 "ip": ip_generator.next(),
                 "recipients": chunk
                 })
        
        return {'message': message,
                'routes': routes
                }
        
    @staticmethod
    def __get_request_chunks_dp(recipients):
        """
            Uses a dynamic-programming approach to chunk up recipients into message
            relay groups.
        """
        assert isinstance(recipients, ListType)
        
        sum_tableau = [None for _ in xrange(len(recipients) + 1)]

        throughput_sizes = set(x.throughput for x in MessageRelays.ALL_DESCENDING)
        
        def min_subset(throughput_set):
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

        for i, state in enumerate(sum_tableau[1:]):
            
            index = i+1
            if index in throughput_sizes:
                sum_tableau[index] = {MessageRelays.get_relay_type_by_throughput(index): 1}
            else:
                #for each throughput size, we want to know the "cost" of state[sum] - throughput size
                candidate_cell = [sum_tableau[i-x.throughput+1] for x in MessageRelays.ALL_DESCENDING if i-x.throughput+1 >= 0]
                minimal_sum = min(candidate_cell, key=min_subset)
                #since by definition, the incremental step we take is equal to one unit, we just need get the
                #minimum cell

                sum_tableau[index] = minimal_sum.copy()
                throughput_val =  index - sum(k.throughput * v for (k,v) in minimal_sum.items())
                relay_type = MessageRelays.get_relay_type_by_throughput(throughput_val)
                assert relay_type
                if relay_type in sum_tableau[index]:
                    sum_tableau[index][relay_type] += 1
                else:
                    sum_tableau[index][relay_type] = 1

        #the last cell in sum_tableau contains the abstraction for doing the chunking
        chunk_count = sum_tableau[len(sum_tableau)-1]
        all_chunks = {}
        start_index = 0
        
        #start dividing up the recipients into chunks
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
            solution in O(1) time. Note: this is not used
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
