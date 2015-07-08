import json
import os.path as op
import services.common.tools as tools

# Thalemine Query Service
from intermine.webservice import Service
service = Service("https://apps.araport.org:443/thalemine/service")
query = service.new_query("Chromosome")
query.add_view("sequence.residues")
query.add_constraint("Chromosome", "LOOKUP", "Chr1", "A. thaliana", code = "A")


#operation
def search(args):
    """

    """

    # Assign input parameters
    chrId = args['Chr']
    start = args['Start']
    end = args['End']
    revComp = args['ReverseComplement']
    flanking = args['Flanking']

    # Validate input parameters
    tools.is_valid_chr(chrId)
    tools.is_valid_coordinate(start,end)
    tools.is_valid_flanking(flanking)

    sequence = run_query(chrId)
    print_json(chrId,start,end,sequence)
    
def list(args):
    """
    List all of the available sequence ids for Arabidopsis thaliana Col-0 genome
    """


def run_query(chrId):

    for row in query.rows():
        return row["sequence.residues"]


def print_json(chrId,start,end,sequence):
    json.dumps(sequence)
    
