from services.AbstractController import AbstractController
from utils.MessageRelays import MessageRelays
from types import ListType, StringType
import json

class NetworkRequestController(AbstractController):

    @staticmethod
    def gen_ip(subnet):
        """
            @type subnet: StringType
        """
        assert isinstance(subnet, StringType)
        subnet_split = subnet.split("/")
        sig_bits = subnet_split[1]
        prefixes = subnet_split[0].split(".")
        
        
        
        

    @staticmethod
    def handle_routing(message, recipients):
        """
            TODO: This contract needs work
            Handles routing decisions for mappings of ips to recipients based on the request
            
            @type message: UnicodeType
            @type recipients: ListType
        """

        all_chunks = NetworkRequestController.__get_request_chunks(recipients)
        #all chunks is a dictionary keyed by throughput types. The values are Lists of Lists of recipients.
        routes = []
        
        for tp_class, chunk in all_chunks.items():
            if len(chunk) > 254:
                raise Exception("this is broken")
            NetworkRequestController.gen_ip(tp_class.subnet_prefix)
            routes.append()
            f = 3
            
            
            
    
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
