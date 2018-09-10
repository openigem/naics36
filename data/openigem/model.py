import sys
import json

from obj import Obj
from set import Set
from var import Var
from var import Par

#
#  Read a model from a JSON file and return a model object
#

def read_json(filename):
   fh = open(filename,'r')
   obj = json.load(fh)
   mod = Model(obj['name'])
   for v in obj['sets']:
      mod.newset(v['name'],v['elements'])
   for v in obj['pars']:
      mod.newpar(v['name'],v['sets'],v['header'])
   for v in obj['vars']:
      mod.newvar(v['name'],v['sets'],v['header'])
   return mod

#
#  Define the model class
#

class Model(Obj):
   '''OpenIGEM model representation'''

   #
   #  Constructor
   #

   def __init__(self,name):
      Obj.__init__(self,'model',name)
      self.set('sets', {'type':'set',       'obj':[], 'names':[]})
      self.set('pars', {'type':'parameter', 'obj':[], 'names':[]})
      self.set('vars', {'type':'variable',  'obj':[], 'names':[]})

   #
   #  String representation
   #

   def __repr__(self):
      dct = {}
      dct['name'] = self.name
      dct['sets'] = self.sets['obj']
      dct['pars'] = self.pars['obj']
      dct['vars'] = self.vars['obj']
      return str(dct)

   #
   #  Add a new set
   #

   def newset(self,name,elements=None):
      '''Create a new set and add it to the model'''
      item = Set(name,elements)
      self._addobj('sets',name,item)
      return item

   #
   #  Add a new parameter
   #

   def newpar(self,name,setnames=None,header=None):
      '''Create a new parameter and add it to the model'''
      item = Par(name,setnames,header)
      self._addobj('pars',name,item)
      return item

   #
   #  Add a new variables
   #

   def newvar(self,name,setnames=None,header=None):
      '''Create a new variable and add it to the model'''
      item = Var(name,setnames,header)
      self._addobj('vars',name,item)
      return item

   #
   #  Look up and return a set, parameter or variable
   #

   def getsets(self):
      '''Get a sorted list of all Set objects in the model.
         Aliases are listed after normal sets.'''
      names = self.set_names()
      setlist = []
      aliases = []
      for n in sorted(names):
         this_set = self.getset(n)
         if this_set.get('alias_of') is not None:
            aliases.append(n)
         else:
            setlist.append(self.getset(n))
      for n in sorted(aliases):
         this_set = self.getset(n)
         setlist.append(self.getset(n))
      return setlist

   def getset(self,name):
      '''Get a set from the model'''
      return self._getobj('sets',name)

   def elements_of(self,name):
      this_set = self._getobj('sets',name)
      alias_of = this_set.get('alias_of')
      if alias_of is None:
         return list(this_set.elements)
      return self.elements_of(alias_of)

   def getpar(self,name):
      '''Get a parameter from the model'''
      return self._getobj('pars',name)

   def getvar(self,name):
      '''Get a variable from the model'''
      return self._getobj('vars',name)

   def sets_of(self,name):
      for t in ['vars','pars']:
         obj = self._getobj(t,name)
         if obj is not None:
            return list(obj.sets)
      print 'variable or parameter not found:',name
      sys.exit(1)

   #
   #  Return lists of sets, parameters or variables
   #

   def set_names(self):
      return self.get('sets')['names']

   def par_names(self):
      return self.get('pars')['names']

   def var_names(self):
      return self.get('vars')['names']

   #
   #  Validate a model
   #

   def validate(self):
      '''Validate the model. Checks for empty sets or parameters and variables
      that are defined over sets that don't exist.
      '''
      errors = 0

      for o in self.get('sets')['obj']:
         if len(o.elements)<1:
            print 'set has no elements:',o.name
            errors += 1

      setnames = self.get('sets')['names']
      for type in ['pars','vars']:
         info = self.get(type)
         for o in info['obj']:
            if len(o.sets)>0:
               for s in o.sets:
                  if s not in setnames:
                     print info['type'],o.name,'uses an undefined set:',s
                     errors += 1

      return errors == 0

   #
   #  Write a model in JSON format
   #

   def to_json(self,filename,validate=True):
      '''Write a model to a file in JSON format. By default, the model will be
      validated first.'''

      if validate and not self.validate():
         print 'file not written'
         sys.exit(1)

      dct = {}
      dct['name'] = self.name
      dct['sets'] = [s.save() for s in self.sets_used()]
      dct['pars'] = [s.save() for s in self.pars['obj']]
      dct['vars'] = [s.save() for s in self.vars['obj']]

      text = json.dumps(dct,indent=4,sort_keys=True)

      fh = open(filename,'w')
      fh.write(text)
      fh.close()

   #
   #  Set headers
   #

   def set_headers(self,key):
      num = 1
      for t in ['pars','vars']:
         for o in self.get(t,must_exist=True)['obj']:
            o.set('header','{}{:03d}'.format(key,num))
            num += 1

   #
   #  Find sets actually used
   #

   def sets_used(self):

      used_sets  = []
      used_names = []

      for t in ['pars','vars']:
         for obj in self.get(t)['obj']:
            if obj.sets is None:
               continue
            for name in obj.sets:
               if name not in used_names:
                  used_sets.append(self.getset(name))
                  used_names.append(name)

      return used_sets

   #
   #  Private methods
   #

   #
   #  Add an object
   #

   def _addobj(self,kind,name,obj):
      info = self.get(kind)
      if name in info['names']:
         print info['type'],'already in model:',name
         sys.exit(1)
      info['obj'].append(obj)
      info['names'].append(name)

   #
   #  Look up and return an object
   #

   def _getobj(self,kind,name):
      info = self.get(kind)
      if name not in info['names']:
         return None
      for i in info['obj']:
         if i.name == name:
            return i
      assert False

