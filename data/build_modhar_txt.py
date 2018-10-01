#! /home/wilcoxen/bin/python
#  Aug 18 (PJW)
#
#  Build a text input file for MODHAR from a portion of OpenIGEM's
#  data and parameters. Accepts a filename stem on the command line
#  and then reads two input files and writes three output files,
#  all with names based on the stem. If no stem is provided, it will
#  default to 'par', which corresponds to the parameter file.
#
#  Usage:
#     build_modhar_txt.py [<stem>]
#
#  Inputs:
#     <stem>_data.csv - IGEM NAICS data or parameter file
#     <stem>.json     - Variable and set definitions for the data file
#
#  Outputs:
#     <stem>_modhar.txt - Data formatted for input to MODHAR
#     <stem>_modhar.inp - Stored input file for running MODHAR
#     <stem>_dec.sym    - Sym declaration file with header names
#
#  Required modules:
#     openigem - local module supporting OpenIGEM
#     pandas
#     sys
#

import pandas as pd
import openigem as oi
import sys

#
#  Set up optional debug flag
#

debug = False

#
#  Check command line; default to par if no stem was given
#

if len(sys.argv) < 2:
   stem = 'par'
else:
   stem = sys.argv[1]

#
#  Set up input file names
#

json_file = stem+'.json'
data_file = stem+'_data.csv'

#
#  Set up output file names
#

modhar_txt = stem+'_modhar.txt'
modhar_inp = stem+'_modhar.inp'
decfile    = stem+'_dec.sym'

#
#  Read the JSON and CSV data files. The JSON file is read by
#  a function in the OpenIGEM module, which returns an object
#  that is stored in 'model'.
#

model = oi.read_json(json_file)
data  = pd.read_csv(data_file)
data.set_index('name',inplace=True)

#
#  Open the output files
#

dfh = open(decfile,'w')
mfh = open(modhar_txt,'w')
ifh = open(modhar_inp,'w')

#
#  Set up a dictionary of data objects for this file.
#

names = model.dat_names
objs  = model.dats

#
#  Process the data objects one by one, writing declarations
#  and MODHAR data for each.
#

kind = 'parameter' if stem == 'par' else 'variable'

for name in names:
   obj = objs[name]
   coeff_decl = obj.decl()

#  Build sym declarations for the data objects

   text = coeff_decl+' '+obj.get('header')+';'
   if obj.get('longname'):
      text += ' // name too long'
   dfh.write(kind+' '+text+'\n')

#  Write the start of the MODHAR block, which declares the variable
#  and its dimensions

   set_list = list(obj.sets)

   set_sizes = ['1']
   if len(set_list)>0:
      set_sizes = [str(len(model.getset(s).elements)) for s in set_list]

   mfh.write(' '.join(set_sizes)+' header "'+obj.header+'"\n')
   mfh.write('   longname "'+obj.name+'"\n')
   mfh.write('   coefficient '+coeff_decl+'\n')
   mfh.write('   ;\n')

#  Now write the data. Order elements from arrays with two or more
#  dimensions into a series of two-dimensional tables with elements
#  in the order expected by MODHAR.
#
#  Start by popping the last two sets, if they exist, into row_set
#  (elements over which the row index ranges) and col_set (elements
#  over which the column index ranges).

   row_set = set_list.pop(0) if len(set_list)> 0 else None
   col_set = set_list.pop(0) if len(set_list)> 0 else None

#  Remaining sets will vary most rapidly at the right so pop
#  them off in reverse order.

   har_order = []
   while len(set_list)>0:
      har_order.append( model.getset(set_list.pop()) )

#  Add on the row and column sets

   if row_set is not None:
      har_order.append( model.getset(row_set) )
   if col_set is not None:
      har_order.append( model.getset(col_set) )

#  Build a cartesian product of all the sets, with the rows in the correct
#  order for MODHAR. In effect, it is a ravel of subscripts in the order
#  in which they should be written out. Each item in the list will be a
#  dictionary with a set names as keys and element names as values.

   seq = oi.cartprod(har_order)

#  Now go through the list and write out the elements

   if len(seq)> 0:
      for subs in seq:
         sublist = [subs[s] for s in obj.sets]
         fullname = name + '(' + ','.join(sublist) + ')'
         if debug:
            mfh.write(fullname+str(data.loc[fullname][0])+'\n')
         else:
            mfh.write(str(data.loc[fullname][0])+'\n')
   else:
      if debug:
         mfh.write(name+'\n')
      else:
         mfh.write(str(data.loc[name][0])+'\n')

#
#  Finished with the declaration and MODHAR data files; close them.
#

mfh.close()
dfh.close()

#
#  Now write the stored input file for MODHAR
#

ifh.writelines([
   'bat\n',
   '\n',
   'n\n',
   stem+'.har\n',
   'at\n',
   modhar_txt+'\n',
   'a\n',
   'ex\n',
   '0\n'
   ])

ifh.close()
