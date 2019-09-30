#! /home/wilcoxen/bin/python
#  Aug 18 (PJW)
#
#  Build a text input file for MODHAR from a portion of OpenIGEM's
#  data and parameters.
#
#  Accepts the name of a selection file and a datatype stem on the
#  command line and then reads two input files and writes three output
#  files, all with names based on the selection file and the stem.
#
#  Usage:
#     build_modhar_txt.py <select>.json <stem>
#
#  Inputs:
#     <select>.json   - Text file with details about selecting the data
#     <stem>_data.csv - IGEM NAICS data or parameter file
#     <stem>.json     - Variable and set definitions for the data file
#
#  Outputs:
#     <select>_<stem>_modhar.txt - Data formatted for input to MODHAR
#     <select>_<stem>_modhar.inp - Stored input file for running MODHAR
#     <select>_<stem>_dec.sym    - Sym declaration file with header names
#
#  Required modules:
#     openigem - local module supporting OpenIGEM
#     pandas
#     sys
#     json
#

import pandas as pd
import openigem as oi
import sys
import json

#
#  Usage message
#

usage = "Usage: build_modhar_txt.py <select>.json <stem>\n"

#
#  Set up optional debug flag
#

debug = False

#
#  Parse the command line
#

if len(sys.argv) != 3:
    print "Unexpected number of arguments"
    print usage
    sys.exit()

(myname,select,stem) = sys.argv

#
#  Read the data info file
#

with open(select,'r') as dfh:
    info = json.load(dfh)

#
#  Figure out which years to select
#

if "years" not in info:
    print "No years attribute in",select
    sys.exit()

years = [str(y) for y in info["years"]]

#
#  Set up input file names
#

json_file = '../' + stem + '.json'
data_file = '../' + stem + '_data.csv'

#
#  Set up output file names
#

modhar_txt = stem + '_modhar.txt'
modhar_inp = stem + '_modhar.inp'
decfile = stem + '_dec.sym'

#
#  Read the JSON and CSV data files. The JSON file is read by
#  a function in the OpenIGEM module, which returns an object
#  that is stored in 'model'.
#

model = oi.read_json(json_file)
data = pd.read_csv(data_file)
data.set_index('name', inplace=True)

#
#  If this isn't a parameter file, take a subset of the years
#

nyrs = 1
if stem != "par":
    data = data[years]
    print "Selected years:",",".join(years)
    nyrs = len(years)

#
#  Open the output files
#

dfh = open(decfile, 'w')
mfh = open(modhar_txt, 'w')
ifh = open(modhar_inp, 'w')

#
#  Set up a dictionary of data objects for this file.
#

names = model.dat_names
objs = model.dats

#
#  Process the data objects one by one, writing declarations
#  and MODHAR data for each.
#

kind = 'parameter' if stem == 'par' else 'variable'

mfh.write("! File: {}\n".format(modhar_txt))
mfh.write("! Filter: {}\n".format(select))

if kind == 'variable':
    mfh.write("! Periods: {}\n".format(nyrs))
    mfh.write("! Years: "+",".join(years)+"\n!\n")

for name in names:
    obj = objs[name]
    coeff_decl = obj.decl()
    set_list = list(obj.sets)

    #  Build sym declarations for the data objects

    text = coeff_decl + ' ' + obj.header + ';'
    if obj.longname:
        text += ' // name too long'
    dfh.write(kind + ' ' + text + '\n')

    #  Now add an explicit time dimension to variables

    if kind == "variable":
        if len(set_list) == 0:
            coeff_decl += "(time)"
        else:
            coeff_decl = coeff_decl.replace(')', ',time)')

    #  Write the start of the MODHAR block, which declares the variable
    #  and its dimensions

    set_sizes = ['1']
    if len(set_list) > 0:
        set_sizes = [str(len(model.getset(s).elements)) for s in set_list]

    if kind == 'variable':
        if len(set_list) == 0:
            set_sizes = [str(nyrs)]
        else:
            set_sizes.append(str(nyrs))

    mfh.write(' '.join(set_sizes) + ' header "' + obj.header + '"\n')
    mfh.write('   longname "' + obj.name + '"\n')
    mfh.write('   coefficient ' + coeff_decl + '\n')
    mfh.write('   ;\n')

    #  Now write the data. Order elements from arrays with two or more
    #  dimensions into a series of two-dimensional tables with elements
    #  in the order expected by MODHAR.
    #
    #  Start by popping the left two sets, if they exist, into row_set
    #  (elements over which the row index ranges) and col_set (elements
    #  over which the column index ranges).

    row_set = set_list.pop(0) if len(set_list) > 0 else None
    col_set = set_list.pop(0) if len(set_list) > 0 else None

    #  Remaining sets will vary most rapidly at the right so pop
    #  them off in reverse order.

    har_order = []
    while len(set_list) > 0:
        har_order.append(model.getset(set_list.pop()))

    #  Add on the row and column sets

    if row_set is not None:
        har_order.append(model.getset(row_set))
    if col_set is not None:
        har_order.append(model.getset(col_set))

    #  Build a cartesian product of all the sets, with the rows in the correct
    #  order for MODHAR. In effect, it is a ravel of subscripts in the order
    #  in which they should be written out. Each item in the list will be a
    #  dictionary with a set names as keys and element names as values.

    seq = oi.cartprod(har_order)

    #  Now go through the list and write out the elements. Do it once
    #  for each selected year. Note that period is NOT added to the
    #  fullname variable because that's not how the data is stored.
    #  That is, the years in the columns and the rows don't have a
    #  time subscript.

    for yr in range(nyrs):
        if kind == "variable":
            mfh.write("! time={} data, year is {}\n".format(yr,years[yr]))
        if len(seq) > 0:
            for subs in seq:
                sublist = [subs[s] for s in obj.sets]
                fullname = name + '(' + ','.join(sublist) + ')'
                if debug:
                    mfh.write(fullname + str(data.loc[fullname][yr]) + '\n')
                else:
                    mfh.write(str(data.loc[fullname][yr]) + '\n')
        else:
            if debug:
                mfh.write(name + '\n')
            else:
                mfh.write(str(data.loc[name][yr]) + '\n')

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
    stem + '.har\n',
    'at\n',
    modhar_txt + '\n',
    'a\n',
    'ex\n',
    '0\n'
])

ifh.close()
