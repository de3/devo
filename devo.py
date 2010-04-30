#!/usr/bin/env python

__author__="de_3"
__date__="1 May 2010 00:40"
__version__="0.1"
__URL__=""
__ThanksTo__="Andrew Pennebaker, ini orang asli yang nulis script python downloader sederhananya, bisa diliat di http://snippets.dzone.com/posts/show/2887"

import urllib2
import os
import sys
import getopt

def getURLName(url):
    mydir=os.curdir
    name = "%s%s%s" % (mydir, os.sep, url.split('/')[-1])
    return name

def getBytesRange(url, start=0, end=None):
    request = urllib2.Request(url)
    if end is not None:
        request.add_header("Range", "bytes=%d-%d" % (start,end))
    else:
        request.add_header("Range", "bytes=%d-" % start)
    response = urllib2.urlopen(request)
    return response

def beginDownload(url, out):
    outstream = open(out, 'wb')
    instream = urllib2.urlopen(url)
    filesize = instream.info().getheader('Content-Length')
    if not filesize:
        print 'Filesize None'
        sys.exit()
    else:
        filesize = float(filesize)
    printResult(instream, outstream, filesize)
        
def resumeDownload(url, out):
    outsize = os.path.getsize(out)
    newstartsize = outsize
    instream = getBytesRange(url, newstartsize)
    outstream = open(out, 'ab')
    filesize = urllib2.urlopen(url).info().getheader('Content-Length')
    if not filesize:
        print 'Filesize None'
        sys.exit()
    else:
        filesize = float(filesize)
    printResult(instream, outstream, filesize, newstartsize)
    
def printResult(instream, outstream, filesize, byteDownloaded = 0.0):
    percentDownloaded = 0
    temp = 0
    print 'Downloading .. ',
    for line in instream:
        byteDownloaded += len(line)
        percentDownloaded = 100*byteDownloaded/filesize
        temp2 = percentDownloaded - temp
        if temp2 >= 1:
            print '%d%%' % percentDownloaded ,
            temp = percentDownloaded
        outstream.write(line)
    instream.close()
    outstream.close()
    print ''
    print 'Downloaded'

def usage():
    print "Usage: %s url" % (sys.argv[0])
    sys.exit()

def main():
    systemArgs = sys.argv[1:]

    try:
        optlist, url = getopt.getopt(systemArgs, None, ['help'])
    except:
        usage()
    if len(url) < 1:
        usage()
    for option, value in optlist:
        if option == 'help':
            usage()
        else:
            print 'Use --help option to view help :p'
    
    outfile = getURLName(url[0])

    if os.path.isfile(outfile):
        resumeDownload(url[0], outfile)
    else:
        beginDownload(url[0], outfile)

if __name__ == "__main__":
    main()
