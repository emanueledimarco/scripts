#! /usr/bin/python
import sys,re

inputf = sys.argv[1]
nbreaks = int(sys.argv[2])

splitlines = []
with open(inputf) as bigfile:
    for lineno, line in enumerate(bigfile):
        if re.match("^ER",line): 
            splitlines.append(lineno+1)

breaks = [ s for i,s in enumerate(splitlines) if (i+1) % nbreaks == 0 ]
print "breaks = ", breaks

smallfile = None
ifile=0
with open(inputf) as bigfile:
    for lineno, line in enumerate(bigfile):
        if len(breaks)>0 and lineno % int(breaks[0]) == 0:
            print "Splitting at line ",lineno
            ifile += 1
            if smallfile:
                smallfile.write("EF\n")
                smallfile.close()
            small_filename = 'small_file_%d.txt' % ifile
            smallfile = open(small_filename, "w")
            if ifile>1: smallfile.write("FN Clarivate Analytics Web of Science")
            if lineno>0: del breaks[0]
        smallfile.write(line)
    if smallfile:
        smallfile.write("EF\n")
        smallfile.close()
