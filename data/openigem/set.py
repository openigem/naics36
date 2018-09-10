import sys

from obj import Obj

class Set(Obj):
   '''OpenIGEM set object'''

   def __init__(self,name,elements=None):
      Obj.__init__(self,'set',name)
      self.set('elements',elements)

   def __repr__(self):
      text = self.name
      if self.elements is not None:
         text += '(' + ','.join(self.elements) + ')'
      return text

   def add_element(self,element):
      if 'elements' not in self.__dict__ or self.elements is None:
         self.__dict__['elements'] = []
      self.elements.append(element)

   def set_alias_of(self,name):
      self.set('alias_of',name)

   def write_sym(self,fh):

      alias_of = self.get('alias_of')
      if alias_of is not None:
         fh.write('set '+self.name+' = '+alias_of+';\n')
         return
      
      if self.elements is None:
         print 'set has no elements:',self.name
         sys.exit(1)

      items = sorted(self.elements)
      
      blocks = {}
      for i in range(len(items)):
         blk = i/10
         if blk not in blocks:
            blocks[blk] = []
         blocks[blk].append(items[i])

      elems = [','.join(blocks[i]) for i in range(len(blocks))]

      text = 'set '+self.name+' ('+',\n      '.join(elems)+');'
      if self.get('longname'):
         text += ' // name too long'

      fh.write(text+'\n\n')
      return

         
