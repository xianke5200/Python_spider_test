'makeTextFile.py -- create text file'

import os
#import linecache
ls = os.linesep

def readWrite():
    while True:
        rw = input('read or write or quit(r or  w or q)>>: ')
        if rw == 'w':
            fname = input('file name > ')

            #get filename
            #while True:
            if os.path.exists(fname):
                #fname = input('reinput file name > ')
                print("FILE: ", fname, "already exist")
                rewrite = input('modify file %s or not(y or n)>>: ' %(fname))
                if rewrite == 'y':
                    reobj = open(fname, 'r+')
                    linecontent = reobj.readlines()
                    count = len(linecontent)
                    #count = 0
                    #for index, line in enumerate(reobj):
                    #    print("%d, %s" %(index, line))
                    #    count += 1
                    print("FILE:",fname, count,"lines total")
                    while input('quit(q)? > ') != 'q':
                        linesel = int(input('which line you want to modify(0-%d): ' %(count-1)))
                        if(linesel >= count):
                            print("linesel out range, please input right linesel")
                            continue
                        #linecontent = linecache.getline(fname, linesel)
                        print(linecontent[linesel])
                        newlinecontent = input('new line content:').strip('\n')
                        linecontent[linesel] = newlinecontent
                        reobj.seek(0)
                        for i in linecontent:
                            reobj.write(str(i.strip('\n'))+'\n')

                    reobj.close()
                elif rewrite == 'n':
                    break

            else:
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
            break
        elif rw == 'r':
            # get filename
            fname = input('Enter filename: ')
            print

            # atempt to open file for reading
            try:
                fobj = open(fname, 'r')
            except IOError:
                print("file open error")
            else:
                # display contents to the screen
                for eachLine in fobj:
                    print(eachLine)
                fobj.close()

            break
        elif rw == 'q':
            print("quit")
            break
        else:
            print("input error, please reinput")

if __name__  == '__main__':
    readWrite()
