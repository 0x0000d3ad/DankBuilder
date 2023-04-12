#!/usr/bin/python

###########################################################################
#
# name          : main.py
#
# purpose       : generate images
#
# usage         : python main.py
#
# description   :
#
#       rules :
#
#       1. DONE eye lashes must match eye type 01-06, with 00 or NA matching no eye lash 
#       2. DONE if blocking glasses, then remove eye and eyelash properties
#       3. DONE only one red glasses pfp in the entire set
#       4. DONE no top features if no top 
#       5. bottoms [M/F] need pants/skirt component
#          - DONE Append M/F name in the JSON
#          - DONE add M/F component in the image
#       6. DONE Laser beam eyes must match laser beam glasses (beam layer in glasses)
#       7. DONE Gold BG with Gold body
#          - DONE Gold accessories, no clothes
#          - DONE only 5 in the set
#
#       Sprinkle in 1/1's into the mix
#
#       rules round 2
#
#       1. WAIT The pigtails (in the hair layer) has headphones built into this.  Deferring to your judgement, but seems to me that perhaps the headphones should be in the “headwater/hats” layer, separate from pigtails.
#       2. WAIT No glasses or hat or earring with headphones
#       3. DONE All DB should have mouth so they don’t get bullied like rankbot
#       4. WAIT The hooped earring has a small gap in it for the illusion of it piercing through the ear layer (see attached).  Should we keep this or make it a perfect circle?
#       5. DONE Eyewear should go over hats (as per your example in the previous email)
#       6. DONE Confirming there’s a green and red laser beam for the laser beam eyes, laser beam paired with laser beam eyes only
#       7. DONE The alien eyes to match alien body
#       8. WAIT body accessories covered by clothing?
#       9. DONE Gold body type only with gold background
#       10. DONE Mohawk, halo mutually exclusive
#
#   usage :
#       redo statistics on a specific metadata directory
#       > python3 main.py -S -o 2022-04-06/metadata
#       generate all DANKBOTS
#       > python3 main.py -a 
#       update ipfs has urls in metadata
#       > python3 main.py -i <directory> -H -1 <old hash> -2 <new hash>
#       > python3 main.py -i 2022-04-06/metadata -H -1 QmW1JzhfSFrJZkHhSuHbktc9TcnDub3jyKz6Baq4n1zPXg -2 QmaMZZCiBDhGk4yZdKYgHkvrdu4YHwYCkwiZNJmS31sQxZ
#       main.py -i "2022-04-11 163333" -H -1 "QmW1JzhfSFrJZkHhSuHbktc9TcnDub3jyKz6Baq4n1zPXg" -2 "QmUagRN5bixenK7zkVSbyfF6EeGXXuvTvV9C5H9868MhVw"
#
###########################################################################

import base64
import copy
import datetime
import json
import os
import random
import re
import shutil
import string
import sys

from PIL import Image, ImageColor
Image.MAX_IMAGE_PIXELS = 434055556 


RESERVED = 0
MAX_MINT = 7777

MAX_GOLD = 50
# NOTE: uncomment to make max qty a multiple of the total mint
#MAX_ALIEN = int( 0.005 * float( MAX_MINT ) ) 
#MAX_APE = int( 0.01 * float( MAX_MINT ) )
#MAX_ZOMBIE = int( 0.03 * float( MAX_MINT ) )
#MAX_TATTOO = int( 0.20 * float( MAX_MINT ) )
#MAX_RAINBOW = int( 0.05 * float( MAX_MINT ) )
MAX_ALIEN = 60 
MAX_APE = 80 
MAX_ZOMBIE = 150
MAX_TATTOO = 80 
MAX_RAINBOW = 120


DNA_SET = string.ascii_lowercase + string.ascii_uppercase
ONEOFF_DIR = "oneoffs" 
ONEOFF_IMAGES_DIR = os.path.join( ONEOFF_DIR, "images" )
ONEOFF = len( os.listdir( ONEOFF_IMAGES_DIR ) )
ONEOFF_METADATA_DIR = os.path.join( ONEOFF_DIR, "metadata" )
MAX_RETRY = 100000
NA_DICT = { "image" : "NA", "name" : "NA", "probability" : "NA", "gender" : "NA" }
LASER_EYE_DICT = { "image" : "Square [SQ]/06 SQ Laser Beam [See Glasses for Laser Component]-01.png", "name" : "Square Laser Beam Eyes", "probability" : 1, "gender" : "*" }
LASER_BEAM_DICT_1 = { "image" : "[EYES ON] Laser Beams Green-01.png", "name" : "Laser Beams Green", "probability" : 3, "gender" : "*" }
LASER_BEAM_DICT_2 = { "image" : "[EYES ON] Laser Beams Red-01.png", "name" : "Laser Beams Red", "probability" : 3, "gender" : "*" }
ALIEN_EYE_1 = { "image" : "Circle [CI]/00 CI [Alien]-01.png", "name" : "Circle Alien", "probability" : 1, "gender" : "*" },
ALIEN_EYE_2 = { "image" : "Square [SQ]/00 SQ [Alien]-01.png", "name" : "Square Alien", "probability" : 1, "gender" : "*" },
GOLD_BODY = { "image" : "Gold 001-01.png", "name" : "Gold", "probability" : 1, "gender" : "*" }
GOLD_BG = { "image" : "Gold-01.png", "name" : "Gold", "probability" : 1, "gender" : "*" }
data_file = os.path.join( "data", "config.json" )
image_dir = "images"
output_dir = "output"
output_image_dir = os.path.join( output_dir, "images" )
output_metadata_dir = os.path.join( output_dir, "metadata" )

hair_data = [ 
    { "image" : "Black 001_Long-01.png", "name" : "Black Long",                "probability" : 15, "gender" : "F" },
    { "image" : "Black 001_Pigtails-01.png", "name" : "Black Pigtails",   "probability" : 15, "gender" : "F" },
    { "image" : "Black 001_Short-01.png", "name" : "Black Short",                "probability" : 15, "gender" : "F" },
    { "image" : "Pink 001_Long-01.png", "name" : "Pink Long",             "probability" : 15, "gender" : "F" },
    { "image" : "Pink 001_Pigtails-01.png", "name" : "Pink Pigtails",     "probability" : 15, "gender" : "F" },
    { "image" : "Pink 001_Short-01.png", "name" : "Pink Short",             "probability" : 15, "gender" : "F" },
    { "image" : "Yellow 001_Long-01.png", "name" : "Yellow Long",         "probability" : 15, "gender" : "F" },
    { "image" : "Yellow 001_Pigtails-01.png", "name" : "Yellow Pigtails", "probability" : 15, "gender" : "F" },
    { "image" : "Yellow 001_Short-01.png", "name" : "Yellow Short",         "probability" : 15, "gender" : "F" },
    { "image" : "NA", "name" : "NA", "probability" : 100, "gender" : "M" }
]

eyes_data = [ 
    { "image" : "Circle [CI]/00 CI Side Eye-01.png", "name" : "Circle Side Eye", "probability" : 10, "gender" : "*" },
    { "image" : "Circle [CI]/04 CI Closed-01.png", "name" : "Circle Closed", "probability" : 10, "gender" : "*" },
    { "image" : "Circle [CI]/04 CI Dank-01.png", "name" : "Circle Dank", "probability" : 10, "gender" : "*" },
    { "image" : "Circle [CI]/00 CI [Alien]-01.png", "name" : "Circle Alien", "probability" : 1, "gender" : "*" },
    { "image" : "Square [SQ]/00 SQ [Alien]-01.png", "name" : "Square Alien", "probability" : 1, "gender" : "*" },
    { "image" : "Square [SQ]/00 SQ Pain-01.png", "name" : "Square Pain", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/00 SQ Side Eye-01.png", "name" : "Square Side Eye", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/00 SQ Trippin-01.png", "name" : "Square Trippin", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/01 SQ Unwell-01.png", "name" : "Square Unwell", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/02 SQ Closed-01.png", "name" : "Square Closed", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/03 SQ Dank Love-01.png", "name" : "Square Dank Love", "probability" : 10, "gender" : "*" },
    { "image" : "Square [SQ]/03 SQ Suspicious-01.png", "name" : "Square Suspicious", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/04 SQ Cry-01.png", "name" : "Square Cry", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/04 SQ Dank Side Eye-01.png", "name" : "Square Dank Side Eye 1", "probability" : 10, "gender" : "*" },
    { "image" : "Square [SQ]/04 SQ Very Dank-01.png", "name" : "Square Very Dank", "probability" : 2, "gender" : "*" },
    { "image" : "Square [SQ]/05 SQ Dank Side Eye-01.png", "name" : "Square Dank Side Eye 2", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/05 SQ Mad-01.png", "name" : "Square Mad", "probability" : 5, "gender" : "*" },
    { "image" : "Square [SQ]/06 SQ Laser Beam [See Glasses for Laser Component]-01.png", "name" : "Square Laser Beam Eyes", "probability" : 1, "gender" : "*" }
]

if not os.path.exists( output_dir ) :
    os.mkdir( output_dir )
if not os.path.exists( output_image_dir ) :
    os.mkdir( output_image_dir )
if not os.path.exists( output_metadata_dir ) :
    os.mkdir( output_metadata_dir )


def get_attributes_from_dna( data_config, dna_string ) :
    return_value = {}
    for layer in sorted( [ int( key ) for key in data_config[ "layers" ] ] ) :
        print( "--> layer: %u" % layer )
        if layer == 0 :
            choices = [ key for key in data_config[ "root" ] ]
            ascii_index = DNA_SET.index( dna_string[ 0 ] )
            return_value[ "0" ] = { "property" : "gender", "item" : { "image" : choices[ ascii_index ] } }
        else :
            choices = [ item[ "image" ] for item in data_config[ "layers" ][ str( layer ) ][ "items" ] ]
            print( choices )
            choices.append( "NA" )
            ascii_index = DNA_SET.index( dna_string[ layer ] )
            print( ascii_index )
            choice = choices[ ascii_index ]
            property_key = data_config[ "layers" ][ str( layer ) ][ "description" ]
            location_key = data_config[ "layers" ][ str( layer ) ][ "location" ]
            return_value[ str( layer ) ] = { "property" : property_key, "location" : location_key, "item" : choice }

    return return_value  

def verify_files_exist( data_config ) :
    return_value = True
    for layer in sorted( [ int( key ) for key in data_config[ "layers" ] ] ) :
        images = [ i[ "image" ] for i in remove_na( data_config[ "layers" ][ str( layer ) ][ "items" ] ) ]
        temp_image_dir = data_config[ "layers" ][ str( layer ) ][ "location" ]
        for filename in images :
            full_filename = os.path.join( image_dir, temp_image_dir, filename )
            if not os.path.exists( full_filename ) :
                print( "--> Error: Layer '%u' - '%s' does not exist!!" % ( layer, full_filename ) )
                return_value = False
    return return_value


def remove_na( elements ) :
    return [ i for i in elements if i[ "name" ] != "NA" ]


def get_attributes( data_config ) :

    return_value = {}
    element = random.choices( [ key for key in data_config[ "root" ] ], weights=[ data_config[ "root" ][ key ] for key in data_config[ "root" ] ] )
    return_value[ "0" ] = { "property" : "gender", "item" : { "image" : element[ 0 ], "name" : element[ 0 ] } }
    gender_choice = element[ 0 ]

    rule_eyes = ""
    rule_has_ear = ""

    mouth_elements = []
    for layer in sorted( [ int( key ) for key in data_config[ "layers" ] ] ) :

        property_key = data_config[ "layers" ][ str( layer ) ][ "description" ]
        location_key = data_config[ "layers" ][ str( layer ) ][ "location" ]
        required_key = data_config[ "layers" ][ str( layer ) ][ "required" ]

        # select elements by gender
        elements = []
        if gender_choice == "male" :
            elements = copy.deepcopy( [ choice for choice in data_config[ "layers" ][ str( layer ) ][ "items" ] if choice[ "gender" ] in [ "M", "*" ] ] )
        elif gender_choice == "female" :
            elements = copy.deepcopy( [ choice for choice in data_config[ "layers" ][ str( layer ) ][ "items" ] if choice[ "gender" ] in [ "F", "*" ] ] )
        else :
            elements = copy.deepcopy( [ choice for choice in data_config[ "layers" ][ str( layer ) ][ "items" ] if choice[ "gender" ] in [ "M", "F", "*" ] ] )

        weights = [ i[ "probability" ] for i in elements ]
        element = random.choices( elements, weights=weights )

        # save mouth selection for verification
        if property_key == "mouth" :
            mouth_elements = copy.deepcopy( elements )

        # filter elements by gold body type if applicable
        if layer > 1 :
            try :
                if return_value[ "1" ][ "item" ][ "name" ] == "Gold" and property_key not in [ "eyes", "eye lashes", "mouth" ] :
                    elements = list( filter( lambda x : "Gold" in x[ "name" ] or "NA" in x[ "name" ], elements ) )
                    if elements == [] :
                        elements = [ NA_DICT ]
            except Exception as e :
                print( "--> Error [ get_attributes 1 ]: '%s'" % str( e ) )
                print( json.dumps( return_value, indent=2 ) )
                sys.exit()


        # apply contingencies
        # [ 1 ] background
        if property_key == "background" :
            # all must have a background
            if element[ 0 ][ "image" ] == "NA" :
                element = random.choices( remove_na( elements ) )

        # [ 2 ] head and body 
        elif property_key == "head and body" :
            # gold body must have gold background
            if element[ 0 ][ "name" ] == "Gold" : 
                return_value[ "1" ] = { "property" : "background", "location" : "12 Background", "item" : GOLD_BG }

            # gold background must have gold body
            if return_value[ "1" ][ "item" ][ "name" ] == "Gold" :
                element[ 0 ] = GOLD_BODY

            # gold body must have gold background.  If no gold background choose a different body
#            if return_value[ "1" ][ "item" ][ "name" ] != "Gold" and element[ 0 ][ "name" ] == "Gold" :
#                element = random.choices( remove_na( elements ) )

        # [ 3 ] tattoos
        elif property_key == "tattoos" :
            # no tattoos for ape body type
            if return_value[ "2" ][ "item" ][ "name" ] == "Ape" :
                element[ 0 ] = NA_DICT

        # [ 5 ] hair
        elif property_key == "hair" :
            # all females must have hair (aside from layers that block this)
            if gender_choice == "female" and element[ 0 ][ "name" ] == "NA" :
                element = random.choices( remove_na( hair_data ) )

            # all males have no hair 
            if gender_choice == "male" and element[ 0 ][ "name" ] != "NA" :
                element[ 0 ] = NA_DICT

        # [ 6 ] clothing - bottom 
        elif property_key == "clothing - bottom" :
            # add bottom by gender, correct naming
            if element[ 0 ][ "image" ] != "NA" :
                element[ 0 ][ "name" ] = "%s %s" % ( gender_choice, re.sub( r'male|female|dankbot', '', element[ 0 ][ "name" ] ).strip() )
            # if BDSM BBL need bottoms
            if return_value[ "4" ][ "item" ][ "name" ] == "BDSM BBL" and element[ 0 ] == "NA" :
                element = random.choices( remove_na( elements ) )

        # [ 7 ] clothing - top
        elif property_key == "clothing - top" :
            # no nipple rings if top 
            if element[ 0 ][ "name" ] != "NA" and return_value[ "4" ][ "item" ][ "name" ] == "Nipple Rings" :
                return_value[ "4" ][ "item" ] = NA_DICT

        # [ 8 ] clothing - top features
        elif property_key == "clothing - top features" :
            # no top features if no top 
            if return_value[ "7" ][ "item" ][ "image" ] == "NA" :
                element[ 0 ] = NA_DICT

        # [ 9 ] mouth 
        elif property_key == "mouth" :
            # no mouth if BDSM hogtie
            if return_value[ "4" ][ "item" ][ "name" ] == "BDSM Hogtie" :
                element[ 0 ] = NA_DICT

        # [ 10 ] eyes
        elif property_key == "eyes" :
            # alien eye rule - alien body requires alien eyes 
            if return_value[ "2" ][ "item" ][ "name" ] == "Alien" :
                element = random.choices( [ ALIEN_EYE_1, ALIEN_EYE_2 ] )[ 0 ]

            # determine which eye type we have 00-06 for use in female eyelashes
            rule_eyes = "NA"
            try :
                rule_eyes = re.search( r'([0-6]{2})', element[ 0 ][ "image" ] ).group( 1 )
            except Exception as e :
                print( "--> [ 1 ] Error: Unable to get 'rule_eyes', details '%s'" % str( e ) )
                print( element[ 0 ] )
                sys.exit()

        # [ 11 ] eye lashes
        elif property_key == "eye lashes" :
            # eye lashes must match eye type 01-06, with 00 or NA matching no eye lash 
            if element[ 0 ][ "image" ] != "NA" :
                if rule_eyes in [ "00", "NA" ] :
                    element[ 0 ] = NA_DICT
                else :
                    element[ 0 ][ "image" ] = "%s-01.png" % rule_eyes
                    element[ 0 ][ "name" ] = "%u" % int( rule_eyes )

        # [ 13 ] eyewear
        elif property_key == "eyewear" :
            # if blocking glasses, then remove eye and eyelash properties
            if "EYES OFF" in element[ 0 ][ "image" ] :
                return_value[ "10" ][ "item" ] = NA_DICT
                return_value[ "11" ][ "item" ] = NA_DICT

            # no earring for ski goggles
            if element[ 0 ][ "name" ] == "Ski Goggles" :
                return_value[ "12" ][ "item" ] = NA_DICT

            # if laser eyes, then no eye lashes
            # lasers must be paired with laser eyes
            if "Laser" in element[ 0 ][ "name" ] :
                return_value[ "10" ][ "item" ] = LASER_EYE_DICT
                return_value[ "11" ][ "item" ] = NA_DICT
            if "Laser" in return_value[ "10" ][ "item" ][ "name" ] :
                element = random.choices( [ LASER_BEAM_DICT_1, LASER_BEAM_DICT_2 ] )
                return_value[ "11" ][ "item" ] = NA_DICT

            # if pigtails then no eyewear
            if "Pigtails" in return_value[ "5" ][ "item" ][ "name" ] :
                element[ 0 ] = NA_DICT

        # [ 14 ] headware
        elif property_key == "headware" :
            # no hair if certain headware 
            forbidden_hats = []
            long_hair_only = []
            long_hair_only.append( "Beanie Cap" )
#            forbidden_hats.append( "Beige Headphones" )
            long_hair_only.append( "Beige Backwards Cap" )
            long_hair_only.append( "Black Backwards Cap" )
            long_hair_only.append( "Black Beanie" )
            forbidden_hats.append( "Black Durag" )
#            forbidden_hats.append( "Black Headphones" )
#            forbidden_hats.append( "Black Sweatband" )
            forbidden_hats.append( "Blue Cap" )
#            forbidden_hats.append( "Blue Sweatband" )
            forbidden_hats.append( "Blue Durag" )
            long_hair_only.append( "Brown Beanie" )
            forbidden_hats.append( "Cowboy Hat" )
            long_hair_only.append( "Gold Crown" )
#            forbidden_hats.append( "Halo" )
            long_hair_only.append( "Pink Cap" )
#            forbidden_hats.append( "Pink Sweatband" )
            long_hair_only.append( "Top Hat" )
            long_hair_only.append( "Yellow Cap" )

            # if head ware in forbidden_hats, set hair to NA
            if return_value[ "5" ][ "item" ][ "name" ] != "NA" and element[ 0 ][ "name" ] in forbidden_hats :
                return_value[ "5" ][ "item" ] = NA_DICT
            # if head ware in long_hair_only, set hair to long_hair
            elif element[ 0 ][ "name" ] in long_hair_only :
                return_value[ "5" ] = { "property" : "hair", "location" : "10 Hair", "item" : random.choice( [ i for i in hair_data if "Long" in i[ "name" ] ] ) }
            # Headphones rules
            if "Headphones" in element[ 0 ][ "name" ] :
                # if headphones then no eyewear
                return_value[ "13" ][ "item" ] = NA_DICT

                # if headphones then no earring
                return_value[ "12" ][ "item" ] = NA_DICT

                # make sure headphones have eyes
                if return_value[ "10" ][ "item" ][ "name" ] == "NA" :
                    return_value[ "10" ] = { "property" : "eyes", "location" : "09 Eyes", "item" : random.choice( eyes_data ) }
                    return_value[ "11" ][ "item" ] = NA_DICT

            # no headware if joint or cigarette
            if return_value[ "9" ][ "item" ][ "name" ] in [ "Joint", "Cigarette" ] :
                element[ 0 ] = NA_DICT

            # if sweatband no glasses, choose eyes again in case sunglasses were blocking
            if "Sweatband" in element[ 0 ][ "name" ] :
                return_value[ "13" ][ "item" ] = NA_DICT
                return_value[ "10" ] = { "property" : "eyes", "location" : "09 Eyes", "item" : random.choice( eyes_data ) }
                return_value[ "11" ][ "item" ] = NA_DICT

        # assign element to return_value after application of rules
        return_value[ str( layer ) ] = { "property" : property_key, "location" : location_key, "item" : element[ 0 ] }

    # all must have eyes unless blocking glasses
    if return_value[ "10" ][ "item" ][ "name" ] == "NA" and "EYES OFF" not in return_value[ "13" ][ "item" ][ "image" ] :
        return_value[ "10" ] = { "property" : "eyes", "location" : "09 Eyes", "item" : random.choice( eyes_data ) }
        return_value[ "11" ][ "item" ] = NA_DICT

    # all must have mouth, unless hogtie
    if return_value[ "9" ][ "item" ][ "name" ] == "NA" :
        if return_value[ "4" ][ "item" ][ "name" ] == "BDSM Hogtie" :
            return_value[ "9" ][ "item" ] = NA_DICT
        else :
            return_value[ "9" ] = { "property" : property_key, "location" : location_key, "item" : random.choice( mouth_elements ) }

    # all must have background
    if return_value[ "1" ][ "item" ][ "name" ] in [ "NA", "" ] :
        print( "--> Error: No Background!" )
        print( json.dumps( return_value ) )
        sys.exit()

    return return_value 


def create_metadata( data_config, attributes, token_id ) :
    return_value = {}
    return_value[ "tokenId" ] = token_id
    return_value[ "name" ] = "%s #%u" % ( data_config[ "project_name" ], token_id )
    return_value[ "image" ] = "%s/%u.%s" % ( data_config[ "image_url_base" ], token_id, data_config[ "file_type" ] )
    return_value[ "external_url" ] = "%s/%u.%s" % ( data_config[ "external_image_url_base" ], token_id, data_config[ "file_type" ] )
    return_value[ "attributes" ] = []
    for layer in sorted( [ int( key ) for key in attributes ] ) :
        property_key = attributes[ str( layer ) ][ "property" ]

        value = "NA"
        try :
            value = attributes[ str( layer ) ][ "item" ][ "name" ]
        except Exception as e :
            print( "--> [ create_metadata ] - Unable to get value from attributes! Details: '%s'" % str( e ) )
            print( "--> layer: %u" % layer )
            print( json.dumps( attributes, indent=2 ) )
            sys.exit()

        return_value[ "attributes" ].append( { "trait_type" : property_key, "value" : value } )

    dna = ""
    for layer in sorted( [ int( key ) for key in data_config[ "layers" ] ] ) :
        choices = [ item[ "name" ] for item in data_config[ "layers" ][ str( layer ) ][ "items" ] ]
        if "NA" not in choices :
            choices.append( "NA" )
        choice = attributes[ str( layer ) ][ "item" ][ "name" ]
        if layer == 6 : 
            choice = re.sub( r'male|female|dankbot', '', choice ).strip()
        ascii_index = choices.index( choice )
        try :
            dna += DNA_SET[ ascii_index ]
        except Exception as e :
            print( "--> Error in the forming DNA details:" )
            print( "--> Choices:     " + str( choices ) )
            print( "--> Choice:      " + choice )
            print( "--> ascii_index: " + str( ascii_index ) )

    return_value[ "dna" ] = dna

    return return_value


def create_image( data_config, attributes, token_id ) :
    return_value = None

    # eyewear in front of headware 
    temp14 = copy.deepcopy( attributes[ "14" ] )
    temp13 = copy.deepcopy( attributes[ "13" ] )
    attributes[ "13" ] = temp14
    attributes[ "14" ] = temp13

    # earring to go in front
    if attributes[ "12" ][ "item" ][ "name" ] != "NA" :
        attributes[ "15" ] = copy.deepcopy( attributes[ "12" ] )

    # body accessories over clothing - top
    temp4 = copy.deepcopy( attributes[ "4" ] )
    temp7 = copy.deepcopy( attributes[ "7" ] )
    attributes[ "7" ] = temp4
    attributes[ "4" ] = temp7

    for layer in sorted( [ int( key ) for key in attributes ] ) :
        if str( layer ) != "0" :
            # add choker at the end
            if attributes[ str( layer ) ][ "item" ][ "name" ] == "BDSM Hogtie" :
                continue
            property_key = attributes[ str( layer ) ][ "property" ]
            value = attributes[ str( layer ) ][ "item" ][ "image" ]
            location = attributes[ str( layer ) ][ "location" ]
            if value != "NA" :
                layer_path = os.path.join( image_dir, location, value )
                if return_value is not None :
                    img = Image.open( layer_path )
                    return_value.paste( img, ( 0, 0 ), img )
                else :
                    return_value = Image.open( layer_path )

    # add BDSM Hogtie over all else
    if attributes[ "7" ][ "item" ][ "name" ] == "BDSM Hogtie" : 
        location = "02 Body Accessories"
        img_element = "BDSM_Hogtie-01.png"
        layer_path = os.path.join( image_dir, location, img_element )
        img = Image.open( layer_path )
        return_value.paste( img, ( 0, 0 ), img )


    return return_value


def create_oneoff( oneoff_id, token_id ) :
    images = os.listdir( ONEOFF_IMAGES_DIR )
    metadata = os.listdir( ONEOFF_METADATA_DIR )
#    re_oneoff = "%02u" % oneoff_id 
#    oneoff_images = list( filter( lambda x : re.search( re_oneoff, x ), images ) ) 
    oneoff_image = os.path.join( ONEOFF_IMAGES_DIR, images[ oneoff_id ] )
    oneoff_metadata = os.path.join( ONEOFF_METADATA_DIR, metadata[ oneoff_id ])
    oneoff_image_dest = os.path.join( output_image_dir, "%u%s" % ( token_id, os.path.splitext( oneoff_image )[ 1 ] ) )
    oneoff_metadata_dest = os.path.join( output_metadata_dir, "%u.json" % token_id )
    shutil.copyfile( oneoff_image, oneoff_image_dest )
    shutil.copyfile( oneoff_metadata, oneoff_metadata_dest )
    with open( oneoff_metadata_dest, 'r' ) as f :
        metadata_json = json.load( f )

    metadata_json[ "attributes" ] = [ i for i in metadata_json[ "attributes" ] if i[ "trait_type" ] != "ear" ]
    metadata_json[ "tokenId" ] = token_id
    metadata_json[ "name" ] = re.sub( r'\s+', " ", os.path.splitext( os.path.basename( oneoff_image_dest ) )[ 0 ].replace( "_", "" ) )
    metadata_json[ "image" ] = "<default>/%s" % os.path.basename( oneoff_image_dest )
    metadata_json[ "external_url" ] = "<default2>/%s" % os.path.basename( oneoff_image_dest )
    for datum in metadata_json[ "attributes" ] :
        datum[ "value" ] = "One of One"
    with open( oneoff_metadata_dest, 'w' ) as f :
        f.write( json.dumps( metadata_json, indent=2 ) )

    print( "--> ONEOFF!! %u %u" % ( oneoff_id, token_id ) )
    print( "    %s %s" % ( oneoff_image, oneoff_image_dest ) )
    print( "    %s %s" % ( oneoff_metadata, oneoff_metadata_dest ) )


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


# make sure output attributes are formatted correctly
def verify_attribute_text( metadata ) :
    return_value = copy.deepcopy( metadata )
    for datum in return_value[ "attributes" ] :
        datum[ "value" ] = " ".join( [ i[ 0 ].upper() + i[ 1 : ] for i in datum[ "value" ].split( " " ) ] )
    return return_value
        

def generate_images( GENERATE_IMAGES ) :
    data_config = []
    with open( data_file, 'r' ) as f :
        data_config = json.load( f )


    if not verify_files_exist( data_config ) :
        sys.exit()

    token_id = RESERVED + 1
    retry_id = 1
    list_dna = []
    print( "--> Begin" )

    gold_body_count = 0
    alien_body_count = 0
    ape_body_count = 0
    zombie_body_count = 0
    rainbow_body_count = 0
    tattoo_body_count = 0

    oneoffs = []
    if ONEOFF != 0 :
        oneoffs = random.choices( range( token_id, MAX_MINT ), k=ONEOFF )
    oneoff_id = 0

    while token_id <= MAX_MINT :
        restart_line()
        sys.stdout.write( str( token_id ) )
        sys.stdout.flush()

        if token_id in oneoffs :
            if oneoff_id < ONEOFF :
                create_oneoff( oneoff_id, token_id )
                oneoff_id += 1
                token_id += 1
                continue

        attributes = get_attributes( data_config )
        metadata = create_metadata( data_config, attributes, token_id )

        if metadata[ "dna" ] in list_dna :
            print( "--> DNA '%s' already exists!  Generating another, attempt: %u" % ( metadata[ "dna" ], retry_id ) )
            if retry_id == MAX_RETRY :
                print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                sys.exit()
            retry_id += 1
            continue
        elif metadata[ "attributes" ][ 1 ][ "value" ] == "Gold" :
            if gold_body_count < MAX_GOLD :
                gold_body_count += 1
            else :
                print( "--> Max number gold bodies reached, trying again!  Generating another, attempt: %u" % retry_id)
                if retry_id == MAX_RETRY :
                    print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                    sys.exit()
                retry_id += 1
                continue
        elif metadata[ "attributes" ][ 2 ][ "value" ] == "Alien" :
            if alien_body_count < MAX_ALIEN :
                alien_body_count += 1
            else :
                print( "--> Max number alien bodies reached, trying again!  Generating another, attempt: %u" % retry_id)
                if retry_id == MAX_RETRY :
                    print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                    sys.exit()
                retry_id += 1
                continue
        elif metadata[ "attributes" ][ 2 ][ "value" ] == "Ape" :
            if ape_body_count < MAX_APE:
                ape_body_count += 1
            else :
                print( "--> Max number ape bodies reached, trying again!  Generating another, attempt: %u" % retry_id)
                if retry_id == MAX_RETRY :
                    print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                    sys.exit()
                retry_id += 1
                continue
        elif metadata[ "attributes" ][ 2 ][ "value" ] == "Zombie" :
            if zombie_body_count < MAX_ZOMBIE:
                zombie_body_count += 1
            else :
                print( "--> Max number zombie bodies reached, trying again!  Generating another, attempt: %u" % retry_id)
                if retry_id == MAX_RETRY :
                    print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                    sys.exit()
                retry_id += 1
                continue
        elif metadata[ "attributes" ][ 2 ][ "value" ] == "Rainbow" :
            if rainbow_body_count < MAX_RAINBOW:
                rainbow_body_count += 1
            else :
                print( "--> Max number rainbow bodies reached, trying again!  Generating another, attempt: %u" % retry_id)
                if retry_id == MAX_RETRY :
                    print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                    sys.exit()
                retry_id += 1
                continue
        elif metadata[ "attributes" ][ 3 ][ "value" ] == "Tattoos" :
            if tattoo_body_count < MAX_TATTOO :
                tattoo_body_count += 1
            else :
                print( "--> Max number tatooed bodies reached, trying again!  Generating another, attempt: %u" % retry_id)
                if retry_id == MAX_RETRY :
                    print( "--> Max retries reached!  %u retries!  %u generated" % ( MAX_RETRY, token_id ) )
                    sys.exit()
                retry_id += 1
                continue
        else :
            pass
        

        if GENERATE_IMAGES : 
            image = create_image( data_config, attributes, token_id )

            with open( os.path.join( output_metadata_dir, "%u.json" % token_id ), 'w' ) as f :
                f.write( json.dumps( verify_attribute_text( metadata ), indent=2 ) )

            image.save( os.path.join( output_image_dir, "%u.%s" % ( token_id, data_config[ "file_type" ] ) ), data_config[ "file_type" ] )

        list_dna.append( metadata[ "dna" ] )
        token_id += 1

# shuffle all values and reindex from zero instead of 1
def shuffle_and_reindex() :
    shuffled_images = os.path.join( output_image_dir, "shuffled" )
    shuffled_metadata = os.path.join( output_metadata_dir, "shuffled" )

    if os.path.exists( shuffled_images ) :
        os.remove( shuffled_images )
    if os.path.exists( shuffled_metadata ) :
        os.remove( shuffled_metadata )

    if not os.path.exists( shuffled_images ) :
        os.mkdir( shuffled_images )
    if not os.path.exists( shuffled_metadata ) :
        os.mkdir( shuffled_metadata )

    metadata_files = [ "%s.json" % str( i ) for i in range( 1, MAX_MINT + 1 ) ]
    random.shuffle( metadata_files )
    for filename in metadata_files :
        # get metadata source, destination
        metadata_index = metadata_files.index( filename )
        print( "--> Metadata index: %u" % metadata_index )
        metadata_src_path = os.path.join( output_metadata_dir, filename )
        metadata_dst_path = os.path.join( shuffled_metadata, "%u.json" % metadata_index )
        print( "--> Metadata src, dst: '%s', '%s'" % ( metadata_src_path, metadata_dst_path ) )

        # read metadata
        metadata_json = None
        with open( metadata_src_path, 'r' ) as f :
            metadata_json = json.load( f )

        # get image source, destination
        image_src = metadata_json[ "image" ][ metadata_json[ "image" ].find( "/%u" % int( filename.replace( ".json", "" ) ) ) + 1 : ]
        image_src_components = os.path.splitext( image_src )
        image_dst = "%u%s" % ( metadata_index, image_src_components[ 1 ] )
        image_src_path = os.path.join( output_image_dir, image_src )
        image_dst_path = os.path.join( shuffled_images, image_dst )
        print( "--> Image src, dst: '%s', '%s'" % ( image_src_path, image_dst_path ) )
        #shutil.copyfile( image_src_path, image_dst_path )
        shutil.move( image_src_path, image_dst_path )

        # adjust metadata
        metadata_json[ "tokenId" ] = metadata_index
        metadata_json[ "name" ] = "DANKBOTS #%u" % ( metadata_index + 1 )
        replacement_index = metadata_json[ "image" ].find( "/%s" % filename.replace( ".json", "" ) )
        metadata_json[ "image" ] = metadata_json[ "image" ][ 0 : replacement_index ] + "/%u%s" % ( metadata_index, image_src_components[ 1 ] )
        replacement_index = metadata_json[ "external_url" ].find( "/%s" % filename.replace( ".json", "" ) )
        metadata_json[ "external_url" ] = metadata_json[ "external_url" ][ 0 : replacement_index ] + "/%u%s" % ( metadata_index, image_src_components[ 1 ] )

        # write metadata to file
        with open( metadata_dst_path, 'w' ) as f :
            f.write( json.dumps( metadata_json, indent=2 ) )

        # remove original metadata file
        os.remove( metadata_src_path )


def resize_images() :
    return_value = True

    with open( data_file, 'r' ) as f :
        data_config = json.load( f )

    parent_dir_high_res = "high_res/images"
    image_dir = "images"

    for layer in sorted( [ int( key ) for key in data_config[ "layers" ] ] ) :
        temp_image_dir = data_config[ "layers" ][ str( layer ) ][ "location" ]
        images = [ i[ "image" ] for i in data_config[ "layers" ][ str( layer ) ][ "items" ] ]
        for filename in images :
            src = os.path.join( parent_dir_high_res, temp_image_dir, filename )
            dst = os.path.join( image_dir, temp_image_dir, filename )
            print( "--> %s" % src )
            if not os.path.exists( src ) :
                print( "--> Error: Layer '%u' - '%s' does not exist!!" % ( layer, src ) )
                return_value = False
            else :
                img = Image.open( src )
                img = img.resize( ( 1000, 1000 ) )
                img.save( dst )

    return return_value


def get_stats( target_dir = None ) :
    import pandas as pd
    shuffled_metadata = target_dir
    if not target_dir :
        shuffled_metadata = os.path.join( output_metadata_dir, "shuffled" )
    metadata_files = list( filter( lambda x : re.search( r'.json$', x ), os.listdir( shuffled_metadata ) ) )
    metadata_aggregate = {}
    export_xlsx = {}

    indexes = [] 
    for i in range( MAX_MINT ) :
        with open( os.path.join( shuffled_metadata, "%u.json" % i ), 'r' ) as f :
            data = json.load( f )
            for trait in data[ "attributes" ] :
                if trait[ "trait_type" ] == "head and body" :
                    #if trait[ "value" ] in [ "Ape", "Zombie", "Alien", "One of One" ] :
                    if trait[ "value" ] in [ "Gold", "One of One" ] :
                        indexes.append( { "Type" : trait[ "value" ], "Index" : data[ "tokenId" ] } )
    export_xlsx[ "indexes" ] = pd.DataFrame( indexes )
#    print( json.dumps( indexes, ident=2 ) )

    for metadata_file in metadata_files :
        metadata = None
        with open( os.path.join( shuffled_metadata, metadata_file ), 'r' ) as f :
            metadata = json.load( f )
        for datum in metadata[ "attributes" ] :
            key = datum[ "trait_type" ]
            value = datum[ "value" ]
            if value == "" :
                print( metadata_file )
            if key in metadata_aggregate :
                if value in metadata_aggregate[ key ] :
                    metadata_aggregate[ key ][ value ] += 1
                else :
                    metadata_aggregate[ key ][ value ] = 1
            else :
                metadata_aggregate[ key ] = { value : 1 }

    for key in metadata_aggregate :
        total = sum( metadata_aggregate[ key ].values() )
        for key2 in metadata_aggregate[ key ] :
            metadata_aggregate[ key ][ key2 ] = "%.02f%%" % float( ( float( metadata_aggregate[ key ][ key2 ] ) / float( total ) ) * 100.0 )
        metadata_aggregate[ key ] = sorted( [ { key2 : metadata_aggregate[ key ][ key2 ] } for key2 in metadata_aggregate[ key ].keys() ], key = lambda x : float( list( x.values() )[ 0 ].replace( "%", "" ) ), reverse=True )

        pandas_temp = [] 
        for datum in metadata_aggregate[ key ] :
            pandas_temp.append( { "Trait" : list( datum.keys() )[ 0 ], "Value" : list( datum.values() )[ 0 ] } )
        export_xlsx[ key ] = pd.DataFrame( pandas_temp )

#    print( json.dumps( metadata_aggregate, indent=2 ) )

    writer = pd.ExcelWriter( "output_analytics.xls" )
    for key in export_xlsx :
        export_xlsx[ key ].to_excel( writer, key, index=False )
    writer.save()


def configure_output() :
    date_string = datetime.datetime.now().strftime( "%Y-%m-%d %H%M%S" )
    os.mkdir( date_string )
    shutil.move( os.path.join( "output", "metadata", "shuffled" ), os.path.join( date_string, "metadata" ) )
    shutil.move( os.path.join( "output", "images", "shuffled" ), os.path.join( date_string, "images" ) )
    shutil.move( "output_analytics.xls", os.path.join( date_string, "output_analytics.xls" ) )
    shutil.make_archive( "%s.zip" % date_string, 'zip', date_string )

def adjust_metadata( output_metadata_dir ) :
    with open( data_file, 'r' ) as f :
        data_config = json.load( f )

    for filename in list( filter( lambda x : re.search( r'.json$', x ), os.listdir( output_metadata_dir ) ) ) :
        json_filename = os.path.join( output_metadata_dir, filename )
        print( json_filename )
        metadata = None
        with open( json_filename, 'r' ) as f :
            metadata = json.load( f )

        metadata[ "image" ] = metadata[ "image" ].replace( "<default>", data_config[ "image_url_base" ] )
        metadata[ "external_url" ] = metadata[ "external_url" ].replace( "<default2>", data_config[ "external_image_url_base" ] ) 
        with open( json_filename, 'w' ) as f :
            f.write( json.dumps( metadata, indent=2 ) )

def adjust_metadata_by_ipfs_hash( output_metadata_dir, old_hash, new_hash ) :
    with open( data_file, 'r' ) as f :
        data_config = json.load( f )

    for filename in list( filter( lambda x : re.search( r'.json$', x ), os.listdir( output_metadata_dir ) ) ) :
        json_filename = os.path.join( output_metadata_dir, filename )
        print( json_filename )
        metadata = None
        with open( json_filename, 'r' ) as f :
            metadata = json.load( f )

        metadata[ "image" ] = metadata[ "image" ].replace( old_hash, new_hash )
        metadata[ "external_url" ] = metadata[ "external_url" ].replace( old_hash, new_hash ) 
        with open( json_filename, 'w' ) as f :
            f.write( json.dumps( metadata, indent=2 ) )


if __name__ == "__main__" :
    import optparse
    parser = optparse.OptionParser()
    parser.add_option( '-a', '--all',      dest='all',      action='store_true', help='Generate Image, Shuffle/Reindex, Get Statistics' )
    parser.add_option( '-g', '--generate', dest='generate', action='store_true', help='Generate images' )
    parser.add_option( '-m', '--metadata', dest='metadata', action='store_true', help='Generate metadata without images' )
    parser.add_option( '-r', '--resize',   dest='resize',   action='store_true', help='Resize images' )
    parser.add_option( '-s', '--shuffle',  dest='shuffle',  action='store_true', help='Shuffle and reindex' )
    parser.add_option( '-S', '--stats',    dest='stats',    action='store_true', help='Statistics on traits' )
    parser.add_option( '-H', '--hash',     dest='hash',     action='store_true', help='Adjust metadata by IPFS hash' )
    parser.add_option( '-i', '--ipfs',     dest='ipfs',     action='store', default="", help='Adjust IPFS URLS in metadata dir', metavar="DIR" )
    parser.add_option( '-o', '--output',   dest='output',   action='store', default="", help='Output dir', metavar="DIR" )
    parser.add_option( '-1', '--hash1',    dest='hash1',    action='store', default="", help='Old IPFS hash', metavar="STRING" )
    parser.add_option( '-2', '--hash2',    dest='hash2',    action='store', default="", help='New IPFS hash', metavar="STRING" )
    ( options, args ) = parser.parse_args()

    if options.generate :
        generate_images( True )

    if options.metadata :
        generate_images( False )

    if options.resize :
        resize_images()

    if options.shuffle :
        shuffle_and_reindex()

    if options.stats :
        if options.output :
            get_stats( options.output )
        else :
            get_stats()

    if options.all :
        generate_images( True )
        shuffle_and_reindex()
        get_stats()
        configure_output()

    if options.hash :
        adjust_metadata_by_ipfs_hash( options.ipfs, options.hash1, options.hash2 )
        sys.exit()

    if options.ipfs :
        adjust_metadata( options.ipfs )

