# example usage: python parse_dell_log.py san-05/store_2022_10_26__10_18_44.logs
import re
from optparse import OptionParser

def get_options():
    parser = OptionParser()
    return parser.parse_args()
(opt,args) = get_options()

f = open(args[0], encoding="utf8", errors='ignore')

slots = []
types = []
for x in f:
    line = x.rstrip()
    pdiskn = re.compile("\s+\<PROPERTY\s\S+durable-id\S+\stype\S+disk_(\S+)\<\S+")
    mdiskn = pdiskn.match(line)

    pdiskt = re.compile("\s+\<PROPERTY\sname=\"model\"\stype\S+\>(\S+)\<\S+")
    mdiskt = pdiskt.match(line)

    pstop = re.compile("\s+\<PROPERTY\sname=\"board\-model.*")
    mstop = pstop.match(line)

    if mstop:
        break
    
    if mdiskn:
        if len(types)!=len(slots):
            print ("WARNING: slot ",slots[-1]," has not a regular disk type")
        slots.append(mdiskn.group(1))
        
    if mdiskt:
        mname = mdiskt.group(1)
        if mname.startswith("HUH") or mname.startswith("ST") or  mname.startswith("MG"):
            types.append(mdiskt.group(1))

        
if (len(slots)!=len(types)):
    print ("ERROR: not the same number of matches of slots and disk types")
    print (len(slots), "   ",len(types))
    print (slots)
    print ("\n")
    print (types)
else:
    for i in range(len(slots)):
        print ("slot %s has disk type %s" % (slots[i],types[i]))
