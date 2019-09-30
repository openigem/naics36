#
# Builds the GEMPACK executable for the NAICS36 version
# of OpenIGEM
#

all : naics36.exe naics36.inf 

naics36.exe : naics36.inf
	ltg.bat naics36 

naics36.inf : naics36.tab naics36_build.sti
	-tablo < naics36_build.sti 

clean :
	@rm -f *.fig *~ *.for *.har parcomp.log
	@rm -f naics36.{inf,tb5,tbr,axs,axt,ext,exe,for,min,mnc}
