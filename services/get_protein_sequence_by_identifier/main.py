import services.common.tools as tools

def search(args):
    """
    Return the sequence of a protein given an id and data source
    """
    ident = args["identifier"]
    source = args["source"]

    tools.get_protein_sequence(ident, source)

def list(args):
    """
    args contains a dict with one or key:values
    source is a ThaleMine data source and is mandatory
    """
    source = args["source"]

    tools.get_protein_identifiers(source)
