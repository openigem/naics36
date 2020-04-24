# Sym Code for OpenIGEM

## Subdirectories and master model definition files

Each of the subdirectories contains a master file suitable for building
a version of the model for a particular time grid. The master files are 
all named `openigem.sym` and pull in other sym files as needed from the 
current directory via include statements.

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
    inter.sym
    investment.sym
    markets.sym
    nipa.sym
    openigem.sym
    parameters.sym
    producer.sym
    sets.sym
    steady.sym
    time01.sym
    time10.sym
    time31.sym
    trade.sym
    unused.sym
    variables.sym

## Makefile-sub

This file contains the general procedure for building a version of 
the model for a specified time grid. It is included by makefiles in 
the subdirectories. 
