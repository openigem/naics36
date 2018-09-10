#! /home/wilcoxen/bin/python
#  Aug 18 (PJW)
#
#  Build a text input file for MODHAR from a portion of OpenIGEM's 
#  data and parameters.
#

import pandas as pd
import openigem as oi
import sys

debug = False

usage = 'build_modhar_input.py stem'

if len(sys.argv) < 2:
   stem = 'par'
else:
   stem = sys.argv[1]

json_file = stem+'.json'
data_file = stem+'_data.csv'
modhar_txt = stem+'_modhar.txt'
modhar_inp = stem+'_modhar.inp'
decfile = stem+'_dec.sym'

model = oi.read_json(json_file)
data  = pd.read_csv(data_file)
data.set_index('name',inplace=True)

dfh = open(decfile,'w')
mfh = open(modhar_txt,'w')
ifh = open(modhar_inp,'w')

#%%

if stem == 'par':
   kind = 'parameter'
   names = model.par_names()
   objs = { n: model.getpar(n) for n in names}
else:
   kind = 'variable'
   names = model.var_names()
   objs = { n: model.getvar(n) for n in names}

for name in names:
   obj = objs[name]
   coeff_decl = obj.decl()

   text = coeff_decl+' '+obj.get('header')+';'
   if obj.get('longname'):
      text += ' // name too long'
   dfh.write(kind+' '+text+'\n')

   set_list = list(obj.sets)

   set_sizes = ['1']
   if len(set_list)>0:
      set_sizes = [str(len(model.getset(s).elements)) for s in set_list]

   row_set = set_list.pop(0) if len(set_list)> 0 else None
   col_set = set_list.pop(0) if len(set_list)> 0 else None

   har_order = []
   while len(set_list)>0:
      har_order.append( model.getset(set_list.pop()) )
   if row_set is not None:
      har_order.append( model.getset(row_set) )
   if col_set is not None:
      har_order.append( model.getset(col_set) )

   mfh.write(' '.join(set_sizes)+' header "'+obj.header+'"\n')
   mfh.write('   longname "'+obj.name+'"\n')
   mfh.write('   coefficient '+coeff_decl+'\n')
   mfh.write('   ;\n')

   seq = oi.cartprod(har_order)
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

mfh.close()
dfh.close()

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
