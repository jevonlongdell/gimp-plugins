#!/usr/bin/env python
#import math
from gimpfu import *

def python_makemono(img, layer) :
    #the first step is a high pass filter
    #this we do in 3 parts
    # part 1 -- make new layer
    newlayer = pdb.gimp_layer_copy(layer,False)
    pdb.gimp_image_add_layer(img,newlayer,0)
    #part 2 -- invert it and blur it
    pdb.gimp_invert(newlayer)
    blursize = max(layer.height,layer.width)/5.0;
    pdb.plug_in_gauss(img,newlayer,blursize,blursize,1)
    #part 3 -- merge back with starting layer
    pdb.gimp_layer_set_opacity(newlayer,50.0)
    newlayer = pdb.gimp_image_merge_visible_layers(img,0)
    
    #make a histogram of pixel values
    histogram = [];
    for k in range(256):
        (mean, std_dev, median, pixels, count, percentile) = pdb.gimp_histogram (newlayer, 0,k,k);
        histogram.append(count)
    
    
    #calculate threshold using Otsu method
    #following notes I found on web by Bryan S. Morse

    #calculate mean of image
    mean = 0;     
    for k in range(256):
        mean = mean+k*histogram[k];
    mean=float(mean)/pixels
    
    #work out grey level of the darkest pixel
    for k in range(256):
        if histogram[k]!=0:
            minpixel = k
            break
   
    #values for threshold=minpixel
    nwhite=pixels-histogram[minpixel]
    nblack=histogram[minpixel];
    meanwhite =(mean*pixels-histogram[minpixel]*minpixel)/nwhite;
    meanblack= minpixel;
    bestT =minpixel;
    best_var = nwhite*nblack*(meanwhite-meanblack)**2
    
    

    for T in range(minpixel+1,256):
        newnwhite = nwhite-histogram[T]
        newnblack = nblack+histogram[T]
        if newnwhite==0:
            break
        meanwhite = (meanwhite*nwhite-histogram[T]*T)/newnwhite;
        meanblack = (meanblack*nblack+histogram[T]*T)/newnblack;
        nwhite=newnwhite
        nblack=newnblack
        var = nwhite*nblack*(meanwhite-meanblack)**2
#        print T, math.log10(var), var
        if var>best_var:
            best_var=var
            bestT=T

    #threshold and convert to 1bit pallete        
    pdb.gimp_threshold(newlayer,bestT,255)
    pdb.gimp_image_convert_indexed(img,0,3,2,False,True,"")
    return

register(
       	"python_fu_makemono",
	"makes image monocrhome",
	"Converts RGB into monochrome, indended for text and line art",
	"Jevon Longdell",
	"Jevon Longdell",
	"2013",
	"<Image>/Image/Make monochrome ...",
	"*",
	[],
	[],
	python_makemono,
       )

main()
