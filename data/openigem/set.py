#  set.py
#  Aug 18 (PJW)

import sys


class Set:
    """OpenIGEM set object.

    Args:
        name (str): Name of the set
        elements (list): Elements of the set

    Attributes:
        kind (str): Kind of object
        desc (str): Debugging description of object
        alias_of (str): If not None, the name of the original set
        longname (bool): True if this name exceeds GEMPACK's limit
    """

    def __init__(self, name, elements=None):
        self.kind = 'set'
        self.name = name
        self.desc = self.kind + ' ' + self.name
        self.elements = elements
        self.alias_of = None
        self.longname = len(name) > 12

    #
    # String representation
    #

    def __repr__(self):
        text = self.name
        if self.elements is not None:
            text += '(' + ','.join(self.elements) + ')'
        return text

    #
    # Add an element
    #

    def add_element(self, element):
        """Add an element to the Set."""
        if self.elements is None:
            self.elements = []
        self.elements.append(element)

    #
    # Indicate that this Set is actually an alias of another Set.
    #

    def set_alias_of(self, name):
        """Make this Set an alias of the indicated Set."""
        self.alias_of = name

    #
    # Write out a Sym declaration of this Set.
    #

    def write_sym(self, fh):
        """Write a Sym declaration of this Set to the given file.

        Aliases are handled automatically.

        Args:
            fh (file): File handle to use
        """

        #  Handle aliases

        if self.alias_of is not None:
            fh.write('set ' + self.name + ' = ' + self.alias_of + ';\n')
            return

        #  Handle empty sets

        if self.elements is None or len(self.elements) == 0:
            print 'set has no elements:', self.name
            sys.exit(1)

        #  Get the elements

        items = sorted(self.elements)

        #  Make them into blocks so we can avoid having really long
        #  lines. Doesn't guarantee any particular line length; rather
        #  limit lines to 10 elements.

        blocks = {}
        for i in range(len(items)):
            blk = i / 10
            if blk not in blocks:
                blocks[blk] = []
            blocks[blk].append(items[i])

        elems = [','.join(blocks[i]) for i in range(len(blocks))]

        #  Write out the declaration. As a courtesy, add a comment
        #  flagging names that will be too long for GEMPACK.

        text = 'set ' + self.name + ' (' + ',\n      '.join(elems) + ');'
        if self.longname:
            text += ' // name too long'

        fh.write(text + '\n\n')
        return

    #
    #  Make an exportable version
    #

    def export(self):
        dct = {
            'name': self.name,
            'elements': self.elements
        }
        if self.elements is None:
            dct['elements'] = ''
        if self.alias_of is not None:
            dct['alias_of'] = self.alias_of
        if self.longname:
            dct['longname'] = self.longname

        return dct
