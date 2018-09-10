import sys

from obj import Obj

class Var(Obj):
   '''OpenIGEM variable'''

   #
   #  Constructor
   #

   def __init__(self,name,setnames=None,header=None):
      Obj.__init__(self,'var',name)
      self.set_sets(setnames)
      self.set('header',header)

   def __repr__(self):
      text = self.desc
      if len(self.sets) > 0:
         text += '(' + ','.join(self.sets) +')'
      if self.header is not None:
         text += ', header "'+self.header+'"'
      return text

   # 
   #  Return a declaration
   #

   def decl(self):
      text = self.name
      if self.sets is not None and len(self.sets)>0:
         text += '(' + ','.join(self.sets) + ')'
      return text

   #
   #  Add a list of sets
   #

   def set_sets(self,setnames):
      if isinstance(setnames,str):
         setnames = [setnames]
      self.set('sets',setnames)

   #
   #  Add a header
   #

   def set_header(self,header):
      if header is not None:
         if len(header) <1 or len(header) > 4:
            print self.desc,"invalid header: ",header
            sys.exit(1)
      self.set('header',header)


class Par(Var):
   '''OpenIGEM parameter'''

   def __init__(self,name,setnames=None,header=None):
      Var.__init__(self,name,setnames,header)
      self.kind = 'par'
      self.desc = self.kind+' '+self.name


