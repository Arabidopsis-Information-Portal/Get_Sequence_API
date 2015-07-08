

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
    
