# Sym Code for OpenIGEM

## Master file

The file below defines the full model. It pulls in the other sym files via include statements.

    openigem.sym

## Declarations 
The following files contain declarations of sets, parameters,
and variables.

    sets.sym
    parameters.sym
    variables.sym

## Equations
The files below contain the model's equations divided up into 
functional blocks.

    factors.sym
    government.sym
    household.sym
    investment.sym
    producer.sym
    trade.sym

## Makefile

The makefile in the directory is used for building the Tablo
version of the model from the sym files. The Tablo version 
itself is stored in a parallel directory. The makefile 
also builds the HTML description of the model in the docs
directory.
