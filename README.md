# Introduction 
 This repo contains the code used to construct DANKBOTS and their metadata.  It is still a bit haphazard, due to the fast-paced nature of how the layers evolved, even though some efforts went into refactoring.

# Contents
 The following contents are contained in this repo:

 - `data/` - Data directory.
 - `data/config.json` - Contains all the probabilities for trait creation.
 - `images/` - Image directory for the layers.  The layers are also in [this ARDrive folder](https://app.ardrive.io/#/drives/18bd83b1-5346-4ed1-b71f-3dd5122b6087/folders/6cddf731-c684-4152-8d3d-13ab3db82fc5).
 - `LICENSE` - MIT license file.
 - `main.py` - Main entry point for the image and metadata generation.
 - `README.md` - This file.
 - `regenerate_images.py` - Stand-alone script to regenerate images from DNA.
 - `requirements.txt` - Python requirements to install.
 - `reshuffle_images_and_metadata.py` - Reshuffles images and metadata.

# Installation
 All necessary python modules are contained in `requirements.txt`.  You may install them with the following command:

 `pip install -r requirements.txt`
 
# Running Scripts

 The core fuctionality is in `main.py`.  After installation of the dependencies, you can invoke this by running the following:

 `python main.py <args>`

 Other scripts may be run in a similar manner:

 `python <script>.py`

# Highlights
 The following notes are worthy of mention:

 - There are three DANKBOT genders: Male, Female, and DANKBOT.
 - Traits are defined with respect to gender.  For example, female haircuts are assigned to Female and DANKBOT genders only.
 - The logic in main.py is fairly complex because certain traits block each other.  For example, in the event of a facial accessory that covers the eyes (like VR glasses), we do not assign an eye trait.  Also, some facial accessories and headware interfere, so for each instance there must be rule defined.
 - We reshuffled the metadata because we did a reveal fairly early in the mint to stoke some interest.  We honestly thought we would mint out shortly after, but that did not happen.  Metadata reveals make all metadata public, including for tokens that were not minted yet.  This included our 1/1's.  To make things fair for everyone, we decided to reshuffle the metadata and enforce security via a [private server](https://github.com/0x0000d3ad/Webserver).  The script `reshuffle_images_and_metadata.py` contains the reshuffling code.
