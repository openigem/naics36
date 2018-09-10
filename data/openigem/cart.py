import sys

#
#  cartprod
#
#  Build a Cartesian product of a list of sets.
#

def cartprod(setlist):

   if len(setlist)==0 :
      return []

   names = []
   for s in setlist:
      names.append( s.name )

   prod  = []

   # make a copy of the set list since we're going to pop elements off it

   setlist = list(setlist)

   while( len(setlist)>0 ):
      tail = setlist.pop()
      eles = tail.elements

      newprod = []

      if len(prod)==0:
         for ele in eles:
            newprod.append([ele])
      else:
         for ele in eles:
            for old in prod:
               newprod.append([ele]+old)

      prod = newprod

   sublist = []
   for l in prod:
      newsub = dict(zip(names,l))
      sublist.append(newsub)

   return sublist


