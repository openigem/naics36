#
# makefile 
#
# Builds the TABLO version of OpenIGEM. Also builds the 
# debugging version for convenience.
#

PARTS = openigem.sym   \
        sets.sym       \
        variables.sym  \
        parameters.sym \
        producer.sym   \
        household.sym  \
        investment.sym \
        government.sym \
        trade.sym      \
        factors.sym    

all : ../tablo/naics36.tab ../docs/naics36.html

../tablo/naics36.tab : $(PARTS)
	sym -tablo openigem.sym $@

../docs/naics36.html : $(PARTS)
	sym -html openigem.sym $@

clean :
	@rm -f ../tablo/naics36.{tab,lis} ../docs/naics36.html
