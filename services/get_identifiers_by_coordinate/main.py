import services.common.tools as tools
import json

def search(args):
    """
    Return the sequence provided a coordinate
    """
    # Validate the coordinates
    tools.validate_coordinates(args['start'], args['end'])

    # Build the JSON query
    query_json = tools.create_json(args['chromosome'], args['start'], args['end'])

    # Request the identifier data
    payload = {'query': query_json}
    response = tools.do_request_generic('regions/gff3', **payload)

    for line in response.iter_lines():
        if line.startswith('##') or line.startswith('Nothing to export'):
            continue
        record = tools.parse_gff_record(line)
        print json.dumps(record, indent=2)
        print '---'

def list(args):
    """
    List all of the available sequence ids for Arabidopsis thaliana Col-0 genome
    """

    # call to print the available chromosome identifiers for A. thaliana
    tools.print_list_of_chromosome_ids()
