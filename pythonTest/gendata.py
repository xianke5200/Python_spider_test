from random import  randint, choice
from string import ascii_lowercase
from sys import maxsize
from time import ctime
import re

doms = ('com', 'edu', 'net', 'org', 'gov')

def gendata():
    for i in range(randint(5, 10)):
        dtint = randint(0, maxsize-1)/1000000000       #pick data
        dtstr = ctime(dtint)                #date string
        shorter = randint(4, 7)             #login shorter
        em = ''
        for j in range(shorter):
            em += choice(ascii_lowercase)

        longer = randint(shorter, 12)
        dn = ''
        for j in range(longer):
            dn += choice(ascii_lowercase)

        print("%s::%s@%s.%s::%d-%d-%d" % (dtstr, em, dn, choice(doms), dtint, shorter, longer))

"""
data0 = 'Fri May  9 01:36:14 2228::pgejwt@ajrhnzcp.com::8152767374-6-8'
data1 = 'Fri Sep 17 04:18:44 2241::otfhis@wcfvihvoxwd.org::8574322724-6-11'
data2 = 'Wed Dec 31 15:31:04 2149::zijb@fxhwpbmrgfdu.edu::5680222264-4-12'
data3 = 'Fri Jul 21 15:50:45 2209::pvcecjh@aowbntbyps.com::7559509845-7-10'
data4 = 'Sat Jul 24 01:06:11 2004::sswiz@nfdczgzkzwjk.edu::1090602371-5-12'
data5 = 'Tue Oct 15 21:40:47 2216::tgfuqb@ulmhkci.org::7787886047-6-7'
data6 = 'Mon Aug 23 17:15:44 2021::fgwo@ttydpjw.edu::1629710144-4-7'
data7 = 'Wed Dec 24 16:21:22 2160::yvzgsh@vwcljnxdhnd.com::6026775682-6-11'
"""

def redata():
    reobj = open("redata.txt", 'r')
    data = reobj.readlines()
    #print(data)
    for i in range(0, len(data)):
        patt = '^(\w{3})'#'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
        m = re.match(patt, data[i])
        print(m.group())

        patt = '\d+-\d+-\d+'
        m = re.search(patt, data[i])
        print(m.group())
        patt = '.+(\d+-\d+-\d+)'
        m = re.match(patt, data[i])
        print(m.group(1))
        patt = '.+?(\d+-\d+-\d+)'
        m = re.match(patt, data[i])
        print(m.group(1))

if __name__ == "__main__":
    redata()