import urllib
import urlparse
import json
import re
import requests
import os
from intermine.webservice import Service

# Thalemine root API
BASE_URL = 'https://apps.araport.org/thalemine/service'
service = Service(BASE_URL)

def validate_coordinates(start, end):
    # Validate coordinate range
    if start >= end:
        raise Exception('The end coordinate must be greater than the start!')

def create_json(chromosome, start, end):
    """
    Build the query json object for the specified chromosome and range
    """
    query = {
        'regions': ["%s:%s..%s" % (chromosome,start,end)],
        'featureTypes': ['Gene'],
        'organism': 'A. thaliana'
    }

    return json.dumps(query)

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

def extract_agi_identifier(line):
    id_line = line.split(';')[0]
    p = re.compile(r'ID=(.*)')
    ident = ""
    m = p.search(id_line)
    if m:
        ident = m.group(1)
    return ident

def parse_gff_record(line):
    """Parse a GFF3 record into individual fields"""
    fields = line.strip().split('\t')
    record = {
        'location': fields[0],
        'source': fields[1],
        'type': fields[2],
        'start': fields[3],
        'end': fields[4],
        'strand': fields[6],
        'locus': extract_agi_identifier(fields[8]),
        'class': 'locus_property',
        'source_text_description': 'ThaleMine locus feature'
    }
    return record

def do_request(endpoint, **kwargs):
    """Perform a request to SITE and return JSON."""

    url = urlparse.urljoin(BASE_URL, endpoint)
    response = requests.get(url, params=kwargs)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    try:
        # Try to convert result to JSON
        # abort if not possible
        return response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))

def do_request_generic(endpoint, **kwargs):
    """Perform a request to SITE and return response."""

    url = urlparse.urljoin(BASE_URL + '/', endpoint)
    response = requests.get(url, stream=True, params=kwargs)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    return response

def get_sequence_data(start,end,chromosome,query_xml,flank):
    """
    Runs a query using the Thalemine Sequence Endpoint
    """

    # Adjust the start coordinate since Thalemine Sequence Endpoint
    # index starts at 0
    start = int(start) - 1
    end = int(end)
    flank = int(flank)

    parameters={}
    parameters['query'] = query_xml

    adjust_start = start - flank
    if adjust_start <= 0:
        adjust_start = 0

    adjust_end = end + flank

    parameters['start'] = adjust_start
    parameters['end'] = adjust_end

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
        'chromosome' : chromosome,
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

def get_protein_sequence(identifier, source):
    """
    Query the ThaleMine protein table by identifier and data source
    """

    # get a new query on the class (table) from the model
    query = service.new_query("Protein")

    # views specify the output columns
    query.add_view(
        "primaryIdentifier", "length", "isFragment", "isUniprotCanonical", "name",
        "dataSets.dataSource.name", "sequence.residues"
    )

    # set the constraint value(s)
    query.add_constraint("primaryIdentifier", "=", identifier, code = "A")
    query.add_constraint("dataSets.dataSource.name", "=", source, code = "B")

    for row in query.rows():
        """
        row["name"], row["dataSets.dataSource.name"], row["sequence.residues"]
        """
        record = {
            'class': 'sequence_property',
            'source_text_description': 'ThaleMine Protein Sequence',
            'identifier': row["primaryIdentifier"],
            'length': row["length"],
            'is_fragment': row["isFragment"],
            'is_uniprot': row["isUniprotCanonical"],
            'name': row["name"],
            'source': row["dataSets.dataSource.name"],
            'sequence': row["sequence.residues"]
        }
        print json.dumps(record, indent=2)
        print '---'

def get_protein_identifiers(source):
    """
    Query the ThaleMine protein table by data source
    """

    # get a new query on the class (table) from the model
    query = service.new_query("Protein")

    # views specify the output columns
    query.add_view("primaryIdentifier", "dataSets.dataSource.name")

    # set the constraint value(s)
    query.add_constraint("dataSets.dataSource.name", "=", source, code = "A")

    for row in query.rows():
        ident = row["primaryIdentifier"]
        if ident:
            record = {
                'identifier': row["primaryIdentifier"],
                'source': row["dataSets.dataSource.name"]
            }
            print json.dumps(record, indent=2)
            print '---'
