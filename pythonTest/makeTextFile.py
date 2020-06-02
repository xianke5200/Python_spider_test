'makeTextFile.py -- create text file'

import os
ls = os.linesep
fname = input('file name > ')

#get filename
while True:
    if os.path.exists(fname):
        fname = input('reinput file name > ')
        print("ERROR: %s already exist", fname)
    else:
        break

#get file content (text) lines
all = []
print("\nEnter lines ('.' by itself to quit).\n")

#loop until user termenates input
while True:
    entry = input('input content> ')
    if entry == '.':
        break
    else:
        entry.strip('\n')
        all.append(entry)

#write lines to file with proper line-ending
fobj = open(fname, 'w')
fobj.writelines(['%s%s' % (x, ls) for x in all])
fobj.close()
print("DONE")