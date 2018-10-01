#  obj.sys
#  Aug 18 (PJW)

import sys
import pandas as pd


class Obj(object):
    """OpenIGEM base object.
    
    Parent class of Model, Set and Var objects. Provides some unified functionality
    for all three.
    """

    #
    #  Constructor
    #

    def __init__(self, kind, name):
        self.kind = kind
        self.name = name
        self.desc = self.kind + ' ' + self.name
        if len(name) > 12:
            self.longname = True

    #
    #  Set an attribute
    #

    def set(self, attrib, value, update=False):
        """Set a specified attribute of the Obj to a given value.
       
        Set an attribute. Setting an attribute that already exists is
        a fatal error unless the update flag is used.
 
        Args:
            attrib (str): Attribute to set
            value (object): Value of attribute
            update (bool): If True, ok to replace an existing attribute.
        """

        if attrib in self.__dict__ and self.__dict__[attrib] is not None:
            if not update:
                print self.desc, "already has", attrib
            sys.exit(1)

        if type(value) == float and pd.isna(value):
            value = None

        self.__dict__[attrib] = value

    #
    #  Get an attribute
    #

    def get(self, attrib, must_exist=False):
        """Get a specified attribute of the Obj.
       
        Args:
            attrib (str): Attribute to return
            must_exist (bool): If True, abort if the attribute doesn't exist
 
        Returns:
            Value of the attribute, or None if it doesn't exist.
        """

        if attrib in self.__dict__:
            return self.__dict__[attrib]
        if not must_exist:
            return None

        print self.desc, "has no attribute", attrib
        sys.exit(1)

    #
    #  Stripped down version for saving
    #

    def save(self, opt=[], omit=[]):
        """Build a trimmed-down version of the Obj for saving.
       
        Omits some internal details that are not part of the economic
        structure of the object.

        Args:
            opt (list): Only include these if they are not None
            omit (list): Don't ever save these

        Returns:
            Dictionary of the Obj's attributes.
        """

        opts = ['longname'] + opt
        omits = ['kind', 'desc'] + omit

        dct = {}
        for k, v in self.__dict__.iteritems():
            if k in omits:
                continue
            if k in opts and (v is None or v == ''):
                continue
            if v is None:
                v = ''
            dct[k] = v

        return dct
