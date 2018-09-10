import sys
import pandas as pd
import json

class Obj(object):
   '''OpenIGEM object'''

   #
   #  Constructor
   #

   def __init__(self,kind,name):
      self.kind  = kind
      self.name  = name
      self.desc  = self.kind+' '+self.name
      if len(name)>12:
         self.set('longname',True)

   #
   #  Set an attribute
   #

   def set(self,attrib,value,update=False):
      if attrib in self.__dict__ and self.__dict__[attrib] is not None:
         if update==False:
            print self.desc,"already has",attrib
            sys.exit(1)
      if type(value) == float and pd.isna(value):
         value = None
      self.__dict__[attrib] = value

   #
   #  Get an attribute
   #

   def get(self,attrib,must_exist=False):
      if attrib in self.__dict__:
         return self.__dict__[attrib]
      if must_exist == False:
         return None
      print self.desc,"has no attribute",attrib
      sys.exit(1)

   #
   #  Stripped down version for saving
   #

   def save(self):
      dct = {}
      for k,v in self.__dict__.iteritems():
         if k in ['kind','desc']:
            continue
         if v is None:
            v = ''
         dct[k] = v
      return dct

