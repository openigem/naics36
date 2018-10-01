#  cartprod.py
#  Aug 18 (PJW)


def cartprod(list_of_sets):
    """Build a Cartesian product of the elements in a list of Sets.

    Args:
        list_of_sets: List of Set objects
        
    Returns:
        A list consisting of one entry for each combination of subscripts.
        The entries are dictionaries with set names as keys and elements
        as values.
    """

    if len(list_of_sets) == 0:
        return []

    #  Get the set names

    names = [s.name for s in list_of_sets]

    #  Make a copy of the set list since we're going to pop elements off it

    setlist = list(list_of_sets)

    #  Now build the cartesian product, pulling off sets from right to
    #  left. for each new set, go through the elements and add the existing
    #  list of subscripts to each one.

    prod = []
    while len(setlist) > 0:

        #  Get the elements of the right-most remaining set

        tail = setlist.pop()
        eles = tail.elements

        #  Start a new list of subscripts

        newprod = []

        #  If this is this first time through, build a starter product that
        # is a list of lists, where each inner list is a singleton with just
        # the current element.

        if len(prod) == 0:
            for ele in eles:
                newprod.append([ele])

        #  If this is NOT the first time through, build a new product by
        #  going through each element and prepending it to every row of
        #  the existing product.

        else:
            for ele in eles:
                for old in prod:
                    newprod.append([ele] + old)

        #  Update the result

        prod = newprod

    #  Done building the list of subscripts; now turn each line into a
    #  dictionary with set names as keys and subscript values as elements.
    #  do it this way to be paranoid about potential misalignments of
    #  subscripts if they were passed by order alone.

    subinfo = []
    for l in prod:
        newsub = dict(zip(names, l))
        subinfo.append(newsub)

    return subinfo
