import services.common.tools as tools
import sys
import json
import dicttoxml
from intermine.webservice import Service

def search(args):
    """
    Return the sequence of a gene
    """

    # Get the gene coordinates
    coordinate = tools.get_gene_data(args['identifier'])
    
    # Build the XML path query
    query_xml = tools.create_xml(coordinate['chromosome'])
    
    # Request the sequence data
    tools.get_sequence_data(coordinate['start'],coordinate['end'],query_xml)

    
    
def list():
    raise Exception('Does not provide any kind of list.')

    

    
    

        
    

    
    
