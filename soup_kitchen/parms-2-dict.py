
import re

parms = 'naziv_novi=&inn=svi&proizvodjac=svi&nosilac=svi&rezim=svi&atc=svi&jkl=svi&broj_resenja=svi&datum_resenja=svi&tip=svi&button=Search&MM_insert=form1'

string = "{\n"
for pair in parms.split("&"):
    key_val = pair.split("=")
    print(pair)
    entry = "\"{}\": \"{}\"".format(key_val[0], key_val[1])
    string = string + entry + ",\n"

string = string + "}"

print (string)

