import services.common.tools as tools

def search(args):
    """
    Return the sequence of a gene
    """

    # Get the gene coordinates
    coordinate = tools.get_gene_data(args['identifier'])
    if not coordinate:
        raise Exception("Identifier '%s' could not be found!" % args['identifier'])

    # Validate the coordinates
    tools.validate_coordinates(coordinate['start'], coordinate['end'])

    # Build the XML path query
    query_xml = tools.create_xml(coordinate['chromosome'])

    # Request the sequence data
    tools.get_sequence_data(coordinate['start'], coordinate['end'], coordinate['chromosome'], query_xml, args['flank'])

def list(args):
    raise Exception('Does not provide any kind of list.')
