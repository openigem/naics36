# OpenIGEM Data

## Data Blocks

The model's data and parameters are divided into five blocks: parameters,
exogenous data, Kalman terms, make table variables, and endogenous 
variables. This directory contains a number of files associated with 
each block. The start of each filename indicates the block as follows:
```
   end = endogenous variables
   exo = main block of exogenous variables
   ext = additional endogenous variables: pb
   imp = implicit variables not saved by the previous model
   int = intermediate inputs: int_val and int_qty
   iot = Full IO table: io
   kal = exogenous Kalman terms
   mak = make table variables
   par = parameters
```

## JSON Files

These describe the logical structure of each data block. They include the
names of the variables, the sets over which the variables are defined, and
the elements of the sets.

## CSV Files

These contain the data and parameters in a compact readable format that 
is convenient to use with spreadsheets or other tools. The variable name, 
including any applicable subscripts, appears in the first column and 
subsequent columns give values of the parameter or variable in the year 
shown in the first row. The data must be reformatted before it can be used 
with GEMPACK: see the section on build_modhar_txt below for details. 

## Script build_modhar_txt.py

This script reads IGEM-NAICS variable or parameter declarations in JSON 
format and data files in CSV format, and then writes the data in a form
suitable for conversion to GEMPACK's header array format using GEMPACK's 
MODHAR program. It also writes a Sym declaration file that links GEMPACK 
header array names to Sym variable or parameter declarations. The files
used are:
```
   <prefix>.json       - input, variable or parameter definitions
   <prefix>_data.csv   - input, the block's data
   <prefix>_modhar.txt - output, data in MODHAR input format
   <prefix>_modhar.inp - output, Stored input for MODHAR
   <prefix>_dec.sym    - output, Sym declaration file with headers
```

## Subdirectory: openigem

Python code for the openigem module used by build_modhar_txt.py.

## Subdirectories p01s, p10a and p31e

Working directories for building sets of GEMPACK header array files
for various intertemporal grids.:

+ `p01s` supports the 1-period steady state version of the model. The 
    date of the steady state is defined in the file `p01s.json`.
    
+ `p10a` supports the 10-period model with varying grid spacing. The 
   dates of the periods are defined in the file `p10a.json`.
   
+ `p31e` supports the 31-period model with even grid spacing. The 
  periods are defined in `p31e.json`.

### Txt and Inp files

These are output by build_modhar_txt.py. The TXT files contain data 
in a format suitable for MODHAR. The INP files are directives passed
to MODHAR (GEMPACK STI files) to describe the processing that is 
required.

### Sym Files

These are declarations for the corresponding variables or parameters.
The GEMPACK header codes are included.
