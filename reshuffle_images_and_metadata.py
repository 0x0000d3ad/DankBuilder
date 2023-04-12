#!/usr/bin/python

###########################################################################
#
# name          : main.py
#
# purpose       : generate images
#
# usage         : python main.py
#
# description   : shuffle all metadata 
# 
###########################################################################

import base64
import copy
import datetime
import hashlib
import json
import os
import pandas
import random
import re
import shutil
import string
import sys

from PIL import Image, ImageColor
Image.MAX_IMAGE_PIXELS = 434055556 


RESERVED = 0
MAX_MINT = 7777


def get_hash( index ) :
    hash_key = "DankBotsMintOut7777"
    string = str( index ) + hash_key
    return hashlib.sha256( string.encode() ).hexdigest()


def shuffle_and_reindex( input_dir, reshuffle_index ) :
    output_dir = datetime.datetime.now().strftime( "%Y-%m-%d %H%M%S" )
    os.mkdir( output_dir )

    input_image_dir = os.path.join( input_dir, "images" )
    input_metadata_dir = os.path.join( input_dir, "metadata" )

    output_image_dir = os.path.join( output_dir, "images" )
    os.mkdir( output_image_dir )
    output_metadata_dir = os.path.join( output_dir, "metadata" )
    os.mkdir( output_metadata_dir )


    # copy over images that have already been minted
    for i in range( reshuffle_index ) :

        # get metadata source, destination
        filename = "%u.json" % i
        metadata_index = i 
        print( "--> Metadata index: %u" % metadata_index )
        metadata_src_path = os.path.join( input_metadata_dir, filename )
        metadata_dst_path = os.path.join( output_metadata_dir, "%u.json" % metadata_index )
        print( "--> Metadata src, dst: '%s', '%s'" % ( metadata_src_path, metadata_dst_path ) )

        # read metadata
        metadata_json = None
        with open( metadata_src_path, 'r' ) as f :
            metadata_json = json.load( f )

        # get image source, destination
        image_src = metadata_json[ "image" ][ metadata_json[ "image" ].find( "/%u" % int( filename.replace( ".json", "" ) ) ) + 1 : ]
        image_src_components = os.path.splitext( image_src )
        image_dst = "%s%s" % ( get_hash( metadata_index ), image_src_components[ 1 ] )
        image_src_path = os.path.join( input_image_dir, image_src )
        image_dst_path = os.path.join( output_image_dir, image_dst )
        print( "--> Image src, dst: '%s', '%s'" % ( image_src_path, image_dst_path ) )
        shutil.copyfile( image_src_path, image_dst_path )

        # adjust metadata
        metadata_json[ "tokenId" ] = metadata_index
        metadata_json[ "name" ] = "DANKBOTS #%u" % ( metadata_index + 1 )
        replacement_index = metadata_json[ "image" ].find( "/%s" % filename.replace( ".json", "" ) )
        metadata_json[ "image" ] = metadata_json[ "image" ][ 0 : replacement_index ] + "/%s%s" % ( get_hash( metadata_index ), image_src_components[ 1 ] )
        replacement_index = metadata_json[ "external_url" ].find( "/%s" % filename.replace( ".json", "" ) )
        metadata_json[ "external_url" ] = metadata_json[ "external_url" ][ 0 : replacement_index ] + "/%s%s" % ( get_hash( metadata_index ), image_src_components[ 1 ] )

        # write metadata to file
        with open( metadata_dst_path, 'w' ) as f :
            f.write( json.dumps( metadata_json, indent=2 ) )


    # reshuffle images that have not been minted yet
    metadata_files = [ "%s.json" % str( i ) for i in range( reshuffle_index, MAX_MINT ) ]
    random.shuffle( metadata_files )
    rare_data = []
    for filename in metadata_files :

        # get metadata source, destination
        metadata_index = metadata_files.index( filename ) + reshuffle_index
        print( "--> Metadata index: %u" % metadata_index )
        metadata_src_path = os.path.join( input_metadata_dir, filename )
        metadata_dst_path = os.path.join( output_metadata_dir, "%u.json" % metadata_index )
        print( "--> Metadata src, dst: '%s', '%s'" % ( metadata_src_path, metadata_dst_path ) )

        # read metadata
        metadata_json = None
        with open( metadata_src_path, 'r' ) as f :
            metadata_json = json.load( f )

        # get image source, destination
        image_src = metadata_json[ "image" ][ metadata_json[ "image" ].find( "/%u" % int( filename.replace( ".json", "" ) ) ) + 1 : ]
        image_src_components = os.path.splitext( image_src )
        image_dst = "%s%s" % ( get_hash( metadata_index ), image_src_components[ 1 ] )
        image_src_path = os.path.join( input_image_dir, image_src )
        image_dst_path = os.path.join( output_image_dir, image_dst )
        print( "--> Image src, dst: '%s', '%s'" % ( image_src_path, image_dst_path ) )
        shutil.copyfile( image_src_path, image_dst_path )

        # adjust metadata
        metadata_json[ "tokenId" ] = metadata_index
        if "DANKBOTS" in metadata_json[ "name" ] :
            metadata_json[ "name" ] = "DANKBOTS #%u" % ( metadata_index + 1 )
        replacement_index = metadata_json[ "image" ].find( "/%s" % filename.replace( ".json", "" ) )
        metadata_json[ "image" ] = metadata_json[ "image" ][ 0 : replacement_index ] + "/%s%s" % ( get_hash( metadata_index ), image_src_components[ 1 ] )
        replacement_index = metadata_json[ "external_url" ].find( "/%s" % filename.replace( ".json", "" ) )
        metadata_json[ "external_url" ] = metadata_json[ "external_url" ][ 0 : replacement_index ] + "/%s%s" % ( get_hash( metadata_index ), image_src_components[ 1 ] )
        head_and_body = list( filter( lambda x : "head and body" in x[ "trait_type" ], metadata_json[ "attributes" ] ) )
        if re.match( r'Zombie|Alien|Ape|One', head_and_body[ 0 ][ "value" ] ) :
            rare_data.append( { "attribute" : head_and_body[ 0 ][ "value" ], "name" : metadata_json[ "name" ], "index" : metadata_index, "image" : image_dst } )

        # write metadata to file
        with open( metadata_dst_path, 'w' ) as f :
            f.write( json.dumps( metadata_json, indent=2 ) )

    df1 = pandas.DataFrame( list( filter( lambda x : "One" in x[ "attribute" ], rare_data ) ) )
    dfz = pandas.DataFrame( list( filter( lambda x : x[ "attribute" ] == "Zombie", rare_data ) ) )
    dfa = pandas.DataFrame( list( filter( lambda x : x[ "attribute" ] == "Alien", rare_data ) ) )
    dfA = pandas.DataFrame( list( filter( lambda x : x[ "attribute" ] == "Ape", rare_data ) ) )

    writer = pandas.ExcelWriter( os.path.join( output_dir, 'rarities.xlsx' ), engine='xlsxwriter' )

    df1.to_excel( writer, sheet_name="One of One", index=False )
    dfz.to_excel( writer, sheet_name="Zombie", index=False )
    dfa.to_excel( writer, sheet_name="Alien", index=False )
    dfA.to_excel( writer, sheet_name="Ape", index=False )

    writer.save()

def fix_token_name( original_dir, output_dir, reshuffle_index ) :
    m1 = os.path.join( original_dir, "metadata" )
    m2 = os.path.join( output_dir, "metadata" )

    for i in range( MAX_MINT ) :
        filename = "%u.json" % i
        original_file = os.path.join( m1, filename )
        output_file = os.path.join( m2, filename )

        if i < reshuffle_index :
            file_contents = None
            with open( original_file, 'r' ) as f :
                file_contents = json.load( f )

            if "One of One" not in [ j[ "value" ] for j in file_contents[ "attributes" ] ] :
                file_contents[ "name" ] = "DANKBOTS #%u" % i
            else : 
                print( i, file_contents[ "name" ] )
    
            with open( output_file, 'w' ) as f :
                f.write( json.dumps( file_contents, indent=2 ) )
        else :
            file_contents = None
            with open( output_file, 'r' ) as f :
                file_contents = json.load( f )

            if "DANKBOTS" in file_contents[ "name" ] :
                file_contents[ "name" ] = "DANKBOTS #%u" % i
                with open( output_file, 'w' ) as f :
                    f.write( json.dumps( file_contents, indent=2 ) )
            else :
                print( i, file_contents[ "name" ] )


def fix_image_name( output_dir, reshuffle_index ) :
    m = os.path.join( output_dir, "metadata" )
    image_pre = "ipfs://QmUagRN5bixenK7zkVSbyfF6EeGXXuvTvV9C5H9868MhVw/"
    ext_pre = "https://gateway.pinata.cloud/ipfs/QmUagRN5bixenK7zkVSbyfF6EeGXXuvTvV9C5H9868MhVw/"
    site_url = "https://www.dankbotsnft.fun/images/"

    for i in range( MAX_MINT ) :
        filename = os.path.join( m, "%u.json" % i )
        data = None
        with open( filename, 'r' ) as f :
            data = json.load( f )

        full_path = ""
        if i < reshuffle_index :
            full_path = site_url 
            full_path += get_hash( i ) + os.path.splitext( os.path.basename( data[ "image" ] ) )[ 1 ]

            data[ "image" ] = full_path 
            data[ "external_url" ] = full_path 
        else :
            full_path = data[ "image" ].replace( image_pre, site_url )

            data[ "image" ] = full_path 
            data[ "external_url" ] = full_path 

        with open( filename, 'w' ) as f :
            f.write( json.dumps( data, indent=2 ) )


if __name__ == "__main__" :
    
    input_dir = "2022-04-11 163333"
    reshuffle_index = 1214
    shuffle_and_reindex( input_dir, reshuffle_index )
