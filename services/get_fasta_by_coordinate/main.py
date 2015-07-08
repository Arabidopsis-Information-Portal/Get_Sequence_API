import json
from intermine.webservice import Service

# Thalemine Query Service
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
    is_valid_chr(chrId)
    is_valid_coordinate(start,end)
    is_valid_flanking(flanking)

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
    
def is_valid_chr(chr):
    """

    """
    
    if chr == 'C' or chr == 'M':
        # chromosome or mitochondria
        return true
    else:
        # should be between 1 - 8
        id = int(chr)
        if id > 0 and id < 9:
            return true
        else:
            return false
        
    
def is_valid_coordinate(start,end):
    """
    Validate the user provided start and end coordinates.
    """

    # Check for appropriate coordinate values
    if start < 0 or end < 0:
        # no negative values
        return false
    elif start > end:
        # end coordinate must be greater
        return false
    else:
        return true
    
    
    
def is_valid_flanking(flanking):
    """

    """
    # Check for minimum and maximum cutoff
    if flanking > 0 and flanking <= 10000:
        return true
    else:
        return false
