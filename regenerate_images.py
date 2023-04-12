#!/usr/bin/python

###########################################################################
#
# name          : regenerate_images.py
#
# purpose       : generate images
#
# usage         : python regenerate_images.py
#
# description   :
#
###########################################################################

import json
import os
import random
import re
import shutil
import sys

import main

output_dir = "2022-04-07"
metadata_dir = os.path.join( output_dir, "metadata" )
images_dir = os.path.join( output_dir, "images" )

data_config = []
with open( main.data_file, 'r' ) as f :
    data_config = json.load( f )


def get_attributes_from_dna( index ) :
    return_value = {}

    if not main.verify_files_exist( data_config ) :
        sys.exit()

    
    metadata = []
    with open( os.path.join( metadata_dir, "%u.json" % index ), 'r' ) as f :
        metadata = json.load( f )
    dna = metadata[ "dna" ]
    if dna == "NA" :
        print( "--> One of One!! Skipping!!" )
        return

    indexes = [ main.DNA_SET.index( i ) for i in dna ]
    for i in range( len( indexes ) ) :
        choice = indexes[ i ]
        layer = str( i + 1 )
        try :
            item = data_config[ "layers" ][ layer ][ "items" ][ choice ]
        except Exception as e :
#            print( " " + layer, len( data_config[ "layers" ][ layer ][ "items" ] ), choice )
            item = main.NA_DICT
        return_value[ layer ] = { "property" : data_config[ "layers" ][ layer ][ "description" ], "location" : data_config[ "layers" ][ layer ][ "location" ], "item" : item }
    return return_value

def main() :
    for token_id in range( 7777 ) :
        main.restart_line()
        sys.stdout.write( str( token_id ) )
        sys.stdout.flush()

        attributes = get_attributes_from_dna( token_id )
        if attributes :
            image = main.create_image( data_config, attributes, token_id )
            image.save( os.path.join( images_dir, "%u.%s" % ( token_id, data_config[ "file_type" ] ) ), data_config[ "file_type" ] )

if __name__ == "__main__" :
    main()
