#! /usr/bin/python
'''
NOTE: As of 10/12/2015, I could not get spatialite_tool to build. The Spatialite
Users Forum says that support for this package has been dropped. Will need to
determine alternative ways to accomplish what we need.

This program is used to load all of the shapefiles in
a given directory into a spatialite database. The 
.shp, .shx and .dbf files must all be present for each 
shapefile. It uses the spatialite_tool, which can be downloaded and
built from:
https://www.gaia-gis.it/fossil/spatialite-tools/home

The path to the spatialite tool is specified on the command line.

The database must already exist and have been initialized.
You can use spatial-gui to do this. Simple run it, create a new
database, and exit.

Note that table names cannot begin with digits.  It is reasonable
to use the shape file names as the table names. Since the Natural Earth
files begin with prefixes such as 10m_, 50m_ etc., this routine 
will create the table name from the file name by stripping off
the specified number of characters from the file name.
'''

import os
import os.path
import sys
import stat
import subprocess

def tableNames(dir):
    '''
    Search dir for all .shp files. Return a list of just the 
    base file name for each file.
    '''
    names = []
    for f in os.listdir(dir):
        head, tail = os.path.splitext(f)
        if tail == '.shp':
            names.append(head)
                
    return names
                    
if __name__ == '__main__':

    fileNamePrefixLen = 4
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print 'Usage: SpatialFill <path to spatialite_tool> <path to spatiaLit db> [<path to dir with_shp files>]'
        print 'The .shp, shx and dbf files must be present for each shapefile.'
        sys.exit(1)
        
    spatial_tool = os.path.abspath(sys.argv[1])
    
    dbPath   = sys.argv[2]
    dbPath = os.path.abspath(dbPath)
    
    if len(sys.argv) == 4:
        shpPath  = sys.argv[3]
    else:
        shpPath = '.'
    shpPath = os.path.abspath(shpPath)
        
    # get the names of all of the shape files    
    names    = tableNames(shpPath)
    print "***** Shape files *****"
    for n in names:
        print n
    print
    
    # save the current working directory
    currentDir = os.getcwd()
    
    # import all of the tables
    # the spatialite_tool has to run in the directory with the
    # shape files because it looks for multiple 
    # files with the base name, and it is not too smart about 
    # how it does this.
    # 
    # Strip the leading 10m_ from the name, to use as 
    # the table name. For some reason, spatialite_tool
    # chokes if the leading character of the table name
    # is a digit.
    os.chdir(shpPath)
    for n in names:
        table = n[fileNamePrefixLen:]
        print "* Process ", table
        args = []
        args.append(spatial_tool)
        args.append('-d')
        args.append(dbPath)
        args.append('-i')
        args.append('-shp')
        args.append(n)
        args.append('-t')
        args.append(table)
        args.append('-c')
        args.append('ISO-8859-1')
        args.append('-s')
        args.append('4326')
        # print args
        subprocess.call(args)
        
    os.chdir(currentDir)
    
