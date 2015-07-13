import urllib
import json
import re
import requests
import os
from intermine.webservice import Service

# Thalemine root API
BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(BASE_URL)

def validate_args(start,end,chr):

    # Validate coordinate range
    if start >= end:
        raise Exception('The end coordinate must be greater than the start!')

    if start <= 0 or end <= 0:
        raise Exception('The coordinates must be greater than 0!')

    # Validate chromosome identifier
    case = chr[:1]
    chromosome_num = chr[3:]

    if case == 'c':
        # Invalid
        raise Exception('Invalid chromosome input. Please specify chromosome between Chr1-Chr8 or ChrC or ChrM.')
    elif chromosome_num == 'C' or chromosome_num == 'M':
        # Valid chromosome identifier
        return True
    elif int(chromosome_num) < 1 or int(chromosome_num) > 9:
        # Invalid
        raise Exception('Invalid chromosome input. Please specify chromosome between Chr1-Chr8 or ChrC or ChrM.')
    else:
        # Invalid
        return True
    
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
        
    parameters={}
    parameters['start'] = start
    parameters['end'] = end
    parameters['query'] = query_xml

    
    # Build the full url
    url = os.path.join(BASE_URL, 'sequence')

    # Run the query
    response = requests.get(url, params=parameters)

    # Validate the results
    if response.status_code != 200:
        raise Exception('There is a problem. Status code: ' + str(response.status_code))

    # Print the results
    sequence_json = json.loads(response.text)
    start = sequence_json['features'][0]['start']
    end = sequence_json['features'][0]['end']
    seq = sequence_json['features'][0]['seq']
    new_json = {
        'start': start,
        'end': end,
        'sequence': seq
    }
    print json.dumps(new_json, indent=2)
    print '---'

def print_list_of_chromosome_ids():
    """
    Query the Thalemine chromosome table
    """


    # Lookup in this table
    query = service.new_query("Chromosome")

    # Return these two rows
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

    # Lookup in this table
    query = service.new_query("Gene")
    
    query.add_constraint("chromosomeLocation.feature.primaryIdentifier", "=", gene, code = "A")
    
    # Return this two rows
    query.add_view("chromosomeLocation.start","chromosomeLocation.end", "chromosome.primaryIdentifier")

    # Iterate through results
    coordinate = {}
    for row in query.rows():

        # load into a dict
        coordinate = {
            'start': row["chromosomeLocation.start"],
            'end': row["chromosomeLocation.end"],
            'chromosome': row["chromosome.primaryIdentifier"]
        }

    return coordinate
