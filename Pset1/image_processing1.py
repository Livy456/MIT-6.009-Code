#!/usr/bin/env python3

import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!

def legal_color(c):
    """
    Parameters:
        c, numerical value -> either float or int
            corresponds to illegal brightness color
    Task:
        changes to an appropriate color
    Return:
        int, proper color
    """
    # checks for negative numbers
    if c < 0: 
        return 0
    
    # checks for numbers that exceed brightest color
    elif c > 255: 
        return 255
    
    # checks for floats, truncates them
    else: 
        return round(c)

def get_pixel(image, x, y, bound_behavior=None):
    """
    Parameters:
        image, dict
            height, int -> height of image 
            width, int  -> width of image
            pixel, list of ints -> brightness of pixel
        index, int
            specific pixel you want to index
        bound_behavior, string or None by default---> "zero", "wrap", "extend"
            type of out of bounds behavior
    Task:   
        Get the color at a specify pixel
    Return:
        the color of specific pixel
    """
    # checks if you don't have to account for bound_behavior
    
    # checks if pixel out of bound and needs value 0
    if bound_behavior == "zero":
        # checks if x is out of bounds
        if x < 0 or x >= image["width"]:
            return 0
        # checks if y is out of bounds
        if y < 0 or y >= image["height"]:
            return 0
     
    # checks if pixel needs to be wrapped        
    elif bound_behavior == "wrap":
        # accounts for x being out of bounds
        x = x % image["width"]
        # accounts for y being out of bounds
        y = y % image["height"]
        
    # checks if pixel is from extended image
    elif bound_behavior == "extend":
        if x < 0:
            x = 0
        if x>=image["width"]:
            x = image["width"]-1
        if y < 0:
            y = 0
        if y >= image["height"]:
            y = image["height"]-1
    
    # calculates the index
    index = y*image["width"] + x
    
    # returns the pixel at a given image
    return image['pixels'][index]

def set_pixel(image, x, y, c):
    """
    Sets the color at a specify pixel
    """
    index = y*image["width"]+x
    image['pixels'][index] = c

def apply_per_pixel(image, func):
    """
    Parameters:
        image- dict,
            height, int --> number of rows
            width, int ---> number of columns
            pixels, list -> brightness for each pixel (a single long list of ints)
        func- function
    Task:
        Applies a function to every pixel on an image
    Returns:
        modified image with different pixel brightness
    
    """
    # finds total number of pixel
    area = image["height"] * image["width"] # all total pixels

    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0]*area,
    }
    
    # iterates through each pixel in image
    for y in range(image['height']):
        for x in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
   
    # returns new image with modified pixels
    return result

def inverted(image):
    # pixels range from 0 to 255
    return apply_per_pixel(image, lambda c: 255-c)

# HELPER FUNCTIONS      
    
def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings 'zero', 'extend', or 'wrap',
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of 'zero', 'extend', or 'wrap', return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with 'height', 'width', and 'pixels' keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    
    My kernel representation will be a dict,
    
    height (key)  int, height of kernel
    width (key)   int, width of kernel
    pixels (key)  list of ints, value to scale one of image's pixel
    
    """
    # checks if boundary behavior is none of the out of bound behaviors
    if not((boundary_behavior == "zero") or (boundary_behavior == "extend") or (boundary_behavior == "wrap")):
        return None
    
    pixels = []
        
    # iterating through the image
    for y in range(image["height"]):
        for x in range(image["width"]):            
            # resets color, accounts for kernel center position being 0
            new_color = 0 
            
            # center of kernel is 0, 0
            # iterates through half the kernel
            for ky in range(-(kernel["height"]//2), kernel["height"]//2 + 1):
                # iterates through half the kernel
                for kx in range(-(kernel["width"]//2), kernel["width"]//2 + 1):
                    # gets the color of the image
                    color = get_pixel(image, x+kx, y+ky, boundary_behavior)
                    value = get_pixel(kernel, kx + kernel["width"]//2, ky + kernel["height"]//2)
                    new_color+= color*value
            pixels.append(new_color)
       
    # returns copy of image with correlated pixels
    return {"height": image["height"],
            "width": image["width"],
            "pixels": pixels
            }

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    # ensures every pixel has valid value
    return apply_per_pixel(image, legal_color)
     
# FILTERS
def build_kernel(n):
    """
    Parameters:
        n, int --> width and height of the new square kernel
        
    Task:
        Create a dictionary representation of the square kernel.
    Each position in the kernel has identical values that sum 
    to 1.
    dict representation
    height : int
    width: int
    pixels: same value that sums to 1
    
    Returns:
        A dictionary representation of the kernel, with all the values summing to 1
    """
    
    value = 1/n**2  # value for each position of the kernel
    
    # returns a dictionary representation of kernel
    return {"height":n,
            "width": n,
            "pixels": [value]*n**2}

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    kernel = build_kernel(n) # builds dictionary representation of kernel with nxn

    blurred_image = correlate(image, kernel, "extend")
    
    # returns a round/clipped blurred image
    return round_and_clip_image(blurred_image)
    
def sharpened(image, n):
    """
    Parameters:
        image, dict
            height: int, height of the image
            width: int, width of the image
            pixels: list of ints, color of pixel
        n, int
            size of kernel --> nxn
            
    Task:
        calculates the a new sharpened image
    """
    blur_image = blurred(image, n) # makes a blurred image
    pixels = [2*img - blur for img, blur in zip(image["pixels"], blur_image["pixels"])]
    
    sharp_img = {"height": image["height"],
                "width": image["width"],
                "pixels": pixels
                }
    
    # returns a sharpened image 
    return round_and_clip_image(sharp_img)
    
def edges(image):
    """
    Parameter:
        image- dict,
            height, int --> number of rows
            width, int ---> number of columns
            pixels, list -> brightness for each pixel (a single long list of ints)
    Task:
        Emphasizes the edges of an image by using correlate twice
    then performing a calculation to combine the two blurred images
    
    Return:
        new image that emphasizes the edges
    """
    # initializes the kernels that create emphasized edges
    kernel1 = {"height": 3,
               "width": 3,
               "pixels": [-1, 0, 1,
                          -2, 0, 2,
                          -1, 0, 1]
               }
    kernel2 = {"height": 3,
               "width":3, 
               "pixels": [-1, -2, -1,
                          0,  0,  0,
                          1,  2,  1]
               }
    corr_image1 = correlate(image, kernel1, "extend") 
    corr_image2 = correlate(image, kernel2, "extend")
    
    # makes a new list of pixels that emphasizes edges of new image
    # iterates through the pixel values of both first and second correlated image
    pixels = [round(math.sqrt(pix1**2 + pix2**2))
              for pix1, pix2 in zip(corr_image1["pixels"], corr_image2["pixels"])]
    
    # new image with edges emphasized
    edges_img = {"height": image["height"],
                 "width": image["width"],
                 "pixels": pixels}
    
    # returns rounded/clipped image with edges emphasized
    return round_and_clip_image(edges_img)
    
# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    # inverting image
    blue_gill = load_greyscale_image("test_images/bluegill.png")
    gill_inverted = inverted(blue_gill)
    save_greyscale_image(gill_inverted, "inverted_gill.png")
    
    # using kernel on image
    kernel = {"height": 13,
              "width":13,
              "pixels": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
              
    kern = load_greyscale_image("test_images/pigbird.png")
    
    # making images after calling correlate function
    pigbird_zero = correlate(kern, kernel, "zero")
    pigbird_extend = correlate(kern, kernel, "extend")
    pigbird_wrap = correlate(kern, kernel, "wrap")
    
    # saving modified images
    save_greyscale_image(pigbird_zero, "pigbird_kern_zero.png")
    save_greyscale_image(pigbird_extend, "pigbird_kern_extend.png")
    save_greyscale_image(pigbird_wrap, "pigbird_kern_wrap.png")
    
    # blurring image
    cat = load_greyscale_image("test_images/cat.png")
    cat_blur = blurred(cat, 13)
    save_greyscale_image(cat_blur, "cat_blur.png")
    
    # sharpening image
    python = load_greyscale_image("test_images/python.png")
    python_sharp = sharpened(python, 11)
    save_greyscale_image(python_sharp, "python_sharpen.png")
    
    # image wuth edges emphasized
    construct = load_greyscale_image("test_images/construct.png")
    edge_img = edges(construct)
    save_greyscale_image(edge_img, "construct_edge.png")    
