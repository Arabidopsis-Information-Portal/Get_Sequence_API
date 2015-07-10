import urllib
import json
import re
import requests
from intermine.webservice import Service


def create_xml(chr):
    """
    Build the path query xml for the specified chromosome
    """

    constraint = {
        'path' : 'Chromosome',
        'op' : 'LOOKUP',
        'value' : chr,
        'extraValue' : 'A. thaliana'
    }
    query = {
        'model' : 'genomic',
        'view' : 'Chromosome.sequence.residues',
    }

    xml = ' <query '
    for key, val in query.items():
        xml +=  str(key) + '=\"' + str(val) + '\" '

    xml += '>     <constraint '
    for key, val in constraint.items():
        xml +=  str(key) + '=\"' + str(val) + '\" '    

    xml += '/> </query>'

    return xml


def get_sequence_data(start,end,query_xml):
    """
    Runs a query using the Thalemine Sequence Endpoint
    """
    
    BASE_URL = 'https://apps.araport.org/thalemine/service/sequence?'
        
    parameters={}
    parameters['start'] = start
    parameters['end'] = end
    parameters['query'] = query_xml

    # Encode the parameters for URL processing
    url_encoded = urllib.urlencode(parameters)

    # Build the full url
    url = BASE_URL + url_encoded

    # Run the query
    response = requests.get(url)

    # Validate the results
    if response.status_code != 200:
        raise Exception('Can\'t connect to server. Status code: ' + str(response.status_code))

    # Print the results
    sequence_json = json.loads(response.text)
    print sequence_json
    print '---'

def print_list_of_chromosome_ids():
    """
    Query the Thalemine chromosome table
    """
    
    # Thalemine root API
    service = Service("https://apps.araport.org:443/thalemine/service")

    # Lookup in this table
    query = service.new_query("Chromosome")

    # Return this two rows
    query.add_view("primaryIdentifier", "sequence.length")

    # Iterate through results
    for row in query.rows():

        # load into a dict
        list = {
            'length': row["sequence.length"],
            'chromosome': row["primaryIdentifier"]
        }

        # Print the results
        print json.dumps(list, indent=2)
        print '---'
    
def get_gene_data(gene):
    """
    Query the Thalemine gene table
    """
    
    # Thalemine root API
    service = Service("https://apps.araport.org:443/thalemine/service")

    # Lookup in this table
    query = service.new_query("Gene")
    
    query.add_constraint("chromosomeLocation.feature.primaryIdentifier", "=", "AT1G01210", code = "A")
    
    # Return this two rows
    query.add_view("chromosomeLocation.start","chromosomeLocation.end", "chromosome.primaryIdentifier")

    # Iterate through results
    for row in query.rows():

        # load into a dict
        coordinate = {
            'start': row["chromosomeLocation.start"],
            'end': row["chromosomeLocation.end"],
            'chromosome': row["chromosome.primaryIdentifier"]
        }

        return coordinate
