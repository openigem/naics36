# OpenIGEM TABLO Code

## openigem.tab, openigem.lis

These files were produced by running the following command in the 
[sym](../sym) directory to convert the model into GEMPACK's TABLO 
language:

    sym -tablo openigem.sym ../tablo/openigem.tab

## openigem.dbg

This file is not used by GEMPACK but can be helpful for debugging. It was
produced using the following command:

    sym -debug openigem.sym ../tablo/openigem.dbg

## openigem.html

This file is not used by GEMPACK but can be useful for documentation. It was
produced using the following command:

    sym -html openigem.sym ../tablo/openigem.html
