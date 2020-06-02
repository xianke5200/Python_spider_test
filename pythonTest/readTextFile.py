'readTextFile.py -- read and display text file'

#get filename
fname = input('Enter filename: ')
print

#atempt to open file for reading
try:
    fobj = open(fname, 'r')
except IOError:
    print("file open error")
else:
    #display contents to the screen
    for eachLine in fobj:
        print(eachLine)
    fobj.close()