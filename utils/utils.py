import geopy.distance as distance

from models.Branch import Branch


def distance(from_branch, destination_branch):
    # verify whether we have got Branch instances as args
    if not (isinstance(from_branch, Branch) and isinstance(destination_branch, Branch)):
        raise Exception('Argument(s) not of type Branch')
    from_branch_position = from_branch.getPosition()
    destination_branch_position = destination_branch.getPosition()
    # verify whether we do have not none 2 coordinates for each branch
    if not ((
                        (len(destination_branch_position) + len(from_branch_position) == 4 and (
                        destination_branch_position[0])) and (
                            destination_branch_position[1])) and (from_branch_position[0])) or not (from_branch_position[1]):
        raise Exception('Missing postion on destination')

    # distance calculated using vincenty in Km see : https://en.wikipedia.org/wiki/Vincenty%27s_formulae
    return distance.vincenty(
        from_branch.getPosition(),
        destination_branch.getPosition()
    ).km