#  var.py
#  Aug 18 (PJW)

import sys
import pandas as pd


class Var():
    """OpenIGEM variable or parameter object.

    Args:
        name (str): Name of the variable
        setnames (list): Names of sets over which the variable is defined
        header (str): GEMPACK header
        par (bool): If True, this is a parameter
    """

    def __init__(self, name, setnames=None, header=None, par=False):
        self.kind = 'var'
        self.name = name
        self.desc = self.kind + ' ' + self.name
        self.set_sets(setnames)
        self.header = header if header is not None else ''
        self.longname = len(name) > 12
        self.stack_set = None
        if par:
            self.kind = 'par'
            self.desc = self.kind + ' ' + self.name

    # 
    #  String representation
    #

    def __repr__(self):
        """Make a string representation of the Var."""
        text = self.desc
        if len(self.sets) > 0:
            text += '(' + ','.join(self.sets) + ')'
        if not self.header == '':
            text += ', header "' + self.header + '"'
        return text

    # 
    #  Return the core of a declaration: the name and then the 
    #  list of sets in parentheses
    #

    def decl(self):
        """Returns the core of a declaration for the Var.
        
        The declaration will be the name followed by the list of sets in
        parentheses: name(set1,set1...).
        """
        text = self.name
        if self.sets is not None and len(self.sets) > 0:
            text += '(' + ','.join(self.sets) + ')'
        return text

    #
    #  Add a list of sets
    #

    def set_sets(self, setnames):
        """Add a list of sets over which this Var is defined. Can be a single
        string or a list of strings."""

        if isinstance(setnames, str):
            setnames = [setnames]

        if isinstance(setnames, float) and pd.isna(setnames):
            self.sets = None
        else:
            self.sets = setnames

    #
    #  Add a header
    #

    def set_header(self, header):
        """Add a GEMPACK header to the Var.
        
        In the process, check that the header is between 1 and 4 characters.
        """
        if header is not None:
            if len(header) < 1 or len(header) > 4:
                print self.desc, "invalid header: ", header
                sys.exit(1)
            self.header = header

    #
    #  Make an exportable version
    #

    def export(self):
        dct = {
            'header': self.header,
            'name': self.name
        }

        if self.sets is not None:
            dct['sets'] = self.sets
        else:
            dct['sets'] = ''

        if self.longname:
            dct['longname'] = self.longname
        
        if self.stack_set is not None:
            dct['stack_set'] = self.stack_set

        return dct
