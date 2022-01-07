# Reads in the radar images taken from WU radar loop and converts into list of imgs

import os
import imageio
import urllib.request

# Prototype for scraping image files
def read_image():
    # Default: Saint Paul, MN Intellicast Radar ("stc")
    locations = {
        "California": "bfl",
        "New York": "bgm",
        "New Hampshire": "bml",
        "Texas": "bro",
        "Kentucky": "bwg",
        "Michigan": "cad",
        "North Carolina": "clt",
        "Georgia": "csg",
        "Ohio": "day",
        "Colorado": "den",
        "Iowa": "dsm",
        "Florida": "pie",
        "Virginia": "fcx",
        "Connecticut": "hfd",
        "Missouri": "jef",
        "Oklahoma": "law",
        "Nebraska": "lbf",
        "Arkansas": "lit",
        "Louisiana": "msy",
        "Idaho": "myl",
        "South Dakota": "pir",
        "Arizona": "prc",
        "Utah": "pvu",
        "Oregon": "rdm",
        "Wyoming": "riw",
        "Nevada": "rno",
        "New Mexico": "row",
        "Kansas": "sln",
        "Illinois": "spi",
        "Minnesota": "stc",
        "Washington": "tiw",
        "Mississippi": "tvr"
    }
    state = "Minnesota"
    url = "https://s.w-x.co/staticmaps/wu/wxtype/county_loc/{}/animate.png".format(locations[state])
    fname = "radarloop.gif"

    # Read the gif from the web, save to the disk
    imdata = urllib.request.urlopen(url).read()
    open(fname, "wb+").write(imdata)

    # Read the gif from disk to `RGB`s using `imageio.miread`
    imgs = imageio.mimread(fname)

    # Remove written file - May not remove depending on working directory of program
    os.remove(fname)
    nums = len(imgs)
    print("Total {} frames in the gif!".format(nums), "\nCurrent Location:", state)

    # Crop top part out of images
    for i in range(len(imgs)):
        imgs[i] = imgs[i][22:, :]

    return imgs

