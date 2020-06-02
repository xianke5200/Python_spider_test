import urllib

def firstNonblank(lines):
    for eachLine in lines:
        if not eachLine.strip():
            continue
        else:
            return eachLine

def firstLast(webpage):
    f = open(webpage)
    lines = f.readlines()
    f.close()
    print(firstNonblank(lines))
    lines.reverse()
    print(firstNonblank(lines))

def download(url = 'http://www', process = firstLast):
    try:
        retval = urllib.urlretrieve(url)[0]
    except IOError:
        retval = None
    if retval:
        process(retval)

if __name__ == '__main__':
    download()
