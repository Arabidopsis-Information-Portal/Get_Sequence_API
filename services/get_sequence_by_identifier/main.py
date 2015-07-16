import services.common.tools as tools

def search(args):
    """
    Return the sequence of a gene
    """

    # Get the gene coordinates
    coordinate = tools.get_gene_data(args['identifier'])

    # Validate the input parameters
    tools.validate_args(coordinate['start'],coordinate['end'],coordinate['chromosome'],args['flank'])
    
    # Build the XML path query
    query_xml = tools.create_xml(coordinate['chromosome'])
    
    # Request the sequence data
    tools.get_sequence_data(coordinate['start'],coordinate['end'],coordinate['chromosome'],query_xml,args['flank'])

    
    
def list(args):
    raise Exception('Does not provide any kind of list.')

    

    
    

        
    

    
    
