# OpenIGEM TABLO Code

## naics36.tab

Input to Tablo. This was produced from the sym version of the
model via the makefile in the [sym](../sym) directory.

## naics36_build.sti

Input to Tablo. A GEMPACK stored-input file that is used to
provide instructions to Tablo when it builds the Fortran version
of the model. 

## naics36.lis, naics36.inf

Informational output. naics36.lis is produced by sym when 
the model is converted to Tablo. naics36.inf is produced
by Tablo when it converts the model to Fortran. Both 
are included here for reference.

## Makefile

Provides the commands used to build the Fortran and executable
versions of the model.

## Fortran files and executable

The Fortran files produced by Tablo are deleted after they are
linked into the final executable. The executable itself is large
and stored elsewhere as a binary download.

