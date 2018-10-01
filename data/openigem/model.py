#  model.py
#  Aug 18 (PJW)

import sys
import json

from set import Set
from var import Var


def _add_name(name, namelist):
    """Add a name to a list, aborting if it is already present.

    Args:
        name (str): Name to add
        namelist (list): Current list

    Returns:
        None
    """
    if name in namelist:
        print 'Error:', name, 'previously added to model'
        sys.exit(1)
    namelist.append(name)


class Model():
    """OpenIGEM representation of a model.

    A model can contain a collection of Set and Var objects.
    Var objects can be designated as parameters or variables
    and retrieved accordingly.

    Args:
        name: A string giving the name of the model.

    Attributes:
        sets (dict) : Dictionary of Sets
        dats (dict): Dictionary of Vars
        set_names (list): Names of Sets
        dat_names (list): Names of all Vars
        par_names (list): Names of Vars marked as parameters
        var_names (list): Names of Vars not marked as parameters
    """

    def __init__(self, name):
        self.kind = 'model'
        self.name = name
        self.desc = self.kind + ' ' + self.name

        #  keep the actual objects in dictionaries

        self.sets = {}
        self.dats = {}

        #  keep a separate list of names, partly to allow the
        #  sequence of additions to be retained, but also to
        #  allow parameters and variables to be pulled out of
        #  the data dictionary separately when needed.

        self.set_names = []
        self.par_names = []
        self.var_names = []
        self.dat_names = []

    #
    #  String representation
    #

    def __repr__(self):
        dct = {
            'name': self.name,
            'sets': self.list_set_obj(),
            'pars': self.list_par_obj(),
            'vars': self.list_var_obj()
        }
        return str(dct)

    #
    #  Add a new set
    #

    def newset(self, name, elements=None):
        """Create a new set and add it to the model.
        
        Args:
            name (str): Name of set
            elements (list): Elements
        
        Returns:
            Set: new object
        """
        _add_name(name, self.set_names)
        item = Set(name, elements)
        self.sets[name] = item
        return item

    #
    #  Add a new parameter or variable
    #

    def newvar(self, name, setnames=None, header=None, par=False):
        """Create a new variable and add it to the model.

        Args:
            name (str): Name of variable or parameter
            setnames (list): List of set names
            header (str): GEMPACK header
            par (bool): True if a parameter

        Returns:
             Var: new object.
        """
        _add_name(name, self.dat_names)
        item = Var(name, setnames, header, par=par)
        self.dats[name] = item
        if par:
            self.par_names.append(name)
        else:
            self.var_names.append(name)
        return item

    #
    #  Return a list of sets
    #

    def getsets(self):
        """Return a sorted list of Sets; aliases are listed last."""
        names = self.set_names
        setlist = []
        aliases = []
        for n in sorted(names):
            this_set = self.sets[n]
            if this_set.alias_of is not None:
                aliases.append(n)
            else:
                setlist.append(self.sets[n])
        for n in sorted(aliases):
            setlist.append(self.sets[n])
        return setlist

    #
    #  Return a single set
    #

    def getset(self, name):
        """Return a Set if it exists, otherwise return None."""
        if name in self.sets:
            return self.sets[name]
        return None

    #
    #  Validate
    #

    def validate(self):
        """Validate the model.

        Check for empty sets or data objects that are defined over
        sets that don't exist. Prints error messages if any issues
        are found.

        Returns:
            bool: True if no errors, otherwise False
        """

        errors = 0

        # sets with no elements?

        for so in self.list_set_obj():
            if len(so.elements) < 1:
                print 'set has no elements:', so.name
                errors += 1

        # data objects defined over undeclared sets?

        for do in self.list_dat_obj():
            if len(do.sets) > 0:
                for s in do.sets:
                    if s not in self.set_names:
                        print do.name, 'uses an undefined set:', s
                        errors += 1

        return errors == 0

    #
    #  Write a model in JSON format
    #

    def to_json(self, filename, validate=True):
        """Write the Model to a file in JSON.

        By default, the model will be validated first.

        Args:
            filename (str): Name of file to write.
            validate (bool): Validate the model first.
        """

        if validate and not self.validate():
            print 'file not written'
            sys.exit(1)

        dct = {
            'name': self.name,
            'sets': [s.export() for s in self.sets_used()],
            'pars': [s.export() for s in self.list_par_obj()],
            'vars': [s.export() for s in self.list_var_obj()]
        }

        text = json.dumps(dct, indent=4, sort_keys=True)

        fh = open(filename, 'w')
        fh.write(text)
        fh.close()

    #
    #  Set headers
    #

    def set_headers(self, key):
        """
        Add a GEMPACK header name to every data object.

        Each variable or parameter will have a header that will begin
        with `key` and end with three digits.

        Args:
            key (str): A one-character prefix.
        """

        num = 1
        for do in self.list_dat_obj():
            do.header = '{}{:03d}'.format(key, num)
            num += 1

    #
    #  Find sets actually used
    #

    def sets_used(self):
        """Return a list of Sets actually used in the Model."""
        used_sets = []
        used_names = []

        for dn in self.dat_names:
            do = self.dats[dn]
            if do.sets is None:
                continue
            for name in do.sets:
                if name not in used_names:
                    used_sets.append(self.getset(name))
                    used_names.append(name)

        return used_sets

    #
    #  Return lists of component objects
    #

    def list_set_obj(self):
        """Return the list of Set objects."""
        return [self.sets[n] for n in self.set_names]

    def list_par_obj(self):
        """Return the list of Var objects flagged as parameters."""
        return [self.dats[n] for n in self.par_names]

    def list_var_obj(self):
        """Return the list of Var objects not flagged as parameters."""
        return [self.dats[n] for n in self.var_names]

    def list_dat_obj(self):
        """Return the list of all Var objects."""
        return [self.dats[n] for n in self.dat_names]
