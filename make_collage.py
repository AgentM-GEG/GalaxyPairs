from PIL import *
import glob
import formic
import random
import os
import numpy as np
def make_contact_sheet(fnames,(ncols,nrows),(photow,photoh),
                       (marl,mart,marr,marb),
                       padding):
    """\
    Make a contact sheet from a group of filenames:

    fnames       A list of names of the image files
    
    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marl         The left margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """

    # Read in all images and resize appropriately
    imgs = [Image.open(fn).resize((photow,photoh)) for fn in fnames]

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                img = imgs.pop(0)
            except:
                break
            inew.paste(img,bbox)
    return inew


#files = glob.glob('*.TIFF')


fileset = formic.FileSet(include="**/*.png", directory="/Users/km4n6/Box Sync/bharath/Second Project/cutouts/Zach/",exclude=["**/collage*.png","**/lmc.png"])

file_set_array =[]
for each in fileset:
    file_set_array.append(str(each))

files = np.random.choice(file_set_array,20,replace=False)

ncols =5
nrows =4
# Don't bother reading in files we aren't going to use
if len(files) > ncols*nrows: files = files[:ncols*nrows]

# These are all in terms of pixels:
photow,photoh = 1000,800
photo = (photow,photoh)

margins = [2,2,2,2]

padding = 0

inew = make_contact_sheet(files,(ncols,nrows),photo,margins,padding)
inew.save('/Users/km4n6/Box Sync/bharath/Second Project/cutouts/Zach/collage3.png')
#os.system('display bs.png')
#os.system('/Users/km4n6/Box\ /Sync/bharath/Second Project/cutouts/Zach/collage.png')
