import services.common.tools as tools

def search(args):
    """
    Return the sequence provided a coordinate
    """
    # Validate the coordinates
    tools.validate_coordinates(args['start'], args['end'])

    # Build the XML path query
    query_xml = tools.create_xml(args['chromosome'])

    # Request the sequence data
    tools.get_sequence_data(args['start'], args['end'], args['chromosome'], query_xml, args['flank'])

def list(args):
    """
    List all of the available sequence ids for Arabidopsis thaliana Col-0 genome
    """

    # call to print the available chromosome identifiers for A. thaliana
    tools.print_list_of_chromosome_ids()
