import math
from PIL import Image

# FUNCTIONS TO SEPERATE COLOR
def spec_color_only(color_img, index):
    """
    Parameters:
        color_image, dict
            height: int, height of the color image
            width: int, width of the color image
            pixels: (tuple), (red, green, blue) values of color image
    Task:
        Isolates the a specific color, to create a new greyscaled image for specific color
    Return:
        a new greyscaled image for a specific color
    """
    
    # returns a greyscale image for red color
    return {"height": color_img["height"],
            "width": color_img["width"],
            "pixels": [color[index] for color in color_img["pixels"]]}

# FUNCTION RECOMBINE SEPERATE COLORS
def recombine_colors(red_img, green_img, blue_img):
    """
    Parameters:
        red_img, dict
            image object with only red pixel values
        green_img, dict
            image object with only green pixel values
        blue_img, dict
            image object with only blue pixel values
    
    Task:
        combine the red, green, and blue image objects
    into one new image
    
    Return:
        a new image with the combined red, green, and blue values    
    """
    # returns a new image with the combined red, green, and blue pixel values
    return {"height": red_img["height"],
            "width": red_img["width"],
            "pixels": [(red, blue, green) for red, blue, green in 
                       zip(red_img["pixels"], green_img["pixels"], blue_img["pixels"])]
        }

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
    
# FUNCTIONS TO APPLY A FUNCTION TO EVERY PIXEL
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
    
    # checks if pixel is from cumulative energy
    elif bound_behavior == "energy":
        # checks if x is out of matrix boundary
        if x < 0: 
            # returns big value, so energy value will not be selected
            x = 0
        
        # checks if x is out of matrix boundary
        elif x >= image["width"]:
            x = image["width"] - 1
        
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

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    
    def color_filter(color_image):
        """
        Parameter:
            color_image, dict
                height: int, height of the image
                width: int, width of the image
                pixels: tuple, (red, green, blue) color pixel values
        Task:
            seperated the colored image into red, green, and blue images
            invert all the red, green, and blue images to greyscale
            recombine all the inverted red, green, and blue images into one colored image
        Return:
            a new recombined colored image with the color filtered applied to it
        """
        
        # need to apply the color filter on the color image
        color_img_copy = color_image.copy()
        
        # seperating the red, green, and blue colors
        red_color_img = spec_color_only(color_img_copy, 0)
        green_color_img = spec_color_only(color_img_copy, 1)
        blue_color_img = spec_color_only(color_img_copy, 2)
        
        # applies a filter to all the seperate color images
        red_filt = filt(red_color_img)
        green_filt = filt(green_color_img)
        blue_filt = filt(blue_color_img)
        
        # returns a new recombined colored images with filter applied to it
        return recombine_colors(red_filt, green_filt, blue_filt)
    
    # returns a function that applies a color filter
    return color_filter

def make_blur_filter(n):
    """
    Parameters:
        n, int
            the shape of the nxn kernel
    Task:
        Make a blur filter
    Return:
        returns a function that will apply a blur filter to a colored image
    """ 
    
    def blur_filter(color_image):
        """
        Parameters:
            color_image, dict
                height: int, height of the image
                width: int, width of the image
                pixels: list of tuples, (r,g,b) pixel values
        Task:
            apply a blurred filter to the colored image
        Return:
            returns a new colored image with the blur filter applied
        """
        
        # returns a new colored image with blur filter applied
        return blurred(color_image, n) # applies a blur filter
        
    # returns a blur color filter and applies the blur filter to colored image
    return blur_filter

def make_sharpen_filter(n):
    """
    Parameters:
        n, int 
            the size of the nxn kernel
    Task: 
        Make a sharpen filter for colored image
    Return:
        returns a function that will apply a sharpen filter to a colored image
    """
    
    def sharp_filter(color_img):
        """
        Parameters:
            color_img, dict
                height: int, height of the image
                width: int, width of the image
                pixels: list of tuples, (r,g,b) pixel values
        Task:
            applies a sharpened filter to a colored image
        Return:    
            returns a new colored image with the sharpened filter applied to it
        """
        
        # returns a new colored image with sharpen filter applied to it
        return sharpened(color_img, n)
    
    # returns a filter that can sharpen a colored image    
    return sharp_filter

def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    
    def all_filters(color_image):
        """
        Parameters:
            color_image, dict
                height: int, height of the image
                width: int, width of the image
                pixels: list of tuples, (r,g,b) pixel values
        Task:
            applies a list of filters to a colored image
        Return:
            returns a new colored image with all the filters applied to it
        """
        filtered_img = {"height": color_image["height"],
                        "width": color_image["width"],
                        "pixels": color_image["pixels"].copy()}
        
        # iterates through all the filters
        for f in filters:
            filtered_img = f(filtered_img)
            
        # returns a new colored image with all the filters applied to it
        return filtered_img
            
    # returns a function that can apply multiple filters to a colored image
    return all_filters

# SEAM CARVING
# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    height = image["height"]
    width = image["width"]
    new_width = width
    color_image = {"height": height,
                   "width": width,
                   "pixels": image["pixels"].copy()
                    }
   
    # keeps on removing seams until the width has been reduced by ncols
    while (width-ncols)!= new_width:
        grey_image = greyscale_image_from_color_image(color_image)
        energy_image = compute_energy(grey_image)
        cem_image = cumulative_energy_map(energy_image)
        remove_seam = minimum_energy_seam(cem_image)
        color_image = image_without_seam(color_image, remove_seam)
        new_width = color_image["width"]
        
    return color_image
    
# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    # color represents the tuple for the r,g,b values
    # color[0] -> red, color[1] -> green, color[2] -> blue
    
    # list of the corresponding greyscale values
    pixels = [round(0.299*color[0] + 0.587*color[1] + 0.114*color[2])
              for color in image["pixels"]]
    
    # returns a new greyscale image from the corresponding color image
    return {"height": image["height"],
            "width": image["width"],
            "pixels": pixels}

def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    
    # returns a greyscale images with edges detected
    return edges(grey)
        
def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    # energy is an image representation, i.e. a dictionary
    height = energy["height"]   # number of rows
    width = energy["width"]     # number of columns
    pixels = []                 # empty array of cumulative energy
    
    cumulative_pixels_image = {"height": height,
                               "width": width,
                               "pixels": pixels
                               }
    # adds the first row energy values
    pixels.extend(energy["pixels"][:width])

    # iterates through each row
    for y in range(1, height):
            
        # iterates through each pixel in a row
        for x in range(width):
            current_pixel = get_pixel(energy, x, y)
            
            # get adjacent pixel cumulative energy values
            adj_pix1 = get_pixel(cumulative_pixels_image, x-1, y-1, "energy")
            adj_pix2 = get_pixel(cumulative_pixels_image, x, y-1, "energy")
            adj_pix3 = get_pixel(cumulative_pixels_image, x+1, y-1, "energy")
            
            # finding the minimum cumulative energy from adjacent pixels
            min_cumulative_energy = min(adj_pix1, adj_pix2, adj_pix3)
            
            current_min_cummulative = min_cumulative_energy+current_pixel
            
            pixels.append(current_min_cummulative)
    
    # returns a new image with that total energy is the lowest-energy path
    return cumulative_pixels_image

def find_min_index(image, min_value, start_x, end_x, row):
     """
     Parameters:
         min_value, int
             the minimum value in the row
         start_x, int
             the column you are starting at to find index of min value
         end_x, int
             one more than the column you want to stop at
         row, int
             row in which you want to look at
     Task:
         find the index of the minimum element in specific range of columns
     Return:
         the index of the minimum value in the range of the specific columns
     """
     # iterates through each pixel in specific row
     for col in range(start_x, end_x): 
         value = get_pixel(image, col, row)
         
         # checks if the current value is minimum value
         if value == min_value:
             # returns the index of the value
             return row*image["width"]+col
         
def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    indices_pixels = [0]*cem["height"]
    height = cem["height"]
    width = cem["width"]
    pixels = cem["pixels"]
    
    # finds min energy value of last row
    min_value = min(pixels[(height-1)*width:])
    
    # finds index of min value in that row
    min_index = find_min_index(cem, min_value, 0, width, height-1)
    
    indices_pixels[0] = min_index
     
    # iterates through each row, except last row, starts at 2nd to last row
    for y in range(1, height):
        row = height-y-1 # goes backwards through the rows
        
        min_index -= width     # moves index to the above row
        
        x = min_index%width     # finds the specific col
        
        # iterates through corresponding adjacent pixels from the row below
        adj_pix1 = get_pixel(cem, x-1, row, "energy")
        adj_pix2 = get_pixel(cem, x, row, "energy")
        adj_pix3 = get_pixel(cem, x+1, row, "energy")

        min_value = min(adj_pix1, adj_pix2, adj_pix3)
        
        # checks if adjacent pixels in bounds
        if x-1 >=0 and x+2<=width:
            min_index = find_min_index(cem, min_value, x-1, x+2, row)
        
        # checks if pixel is at left most column
        elif x-1<0:
            min_index = find_min_index(cem, min_value, x, x+2, row)
        
        # if pixel is at right most column
        else:
            min_index = find_min_index(cem, min_value, x-1, x+1, row)
        
        indices_pixels[y] = min_index
    
    # returns a list of indices
    return indices_pixels

def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    height = image["height"]
    width = image["width"]
    edited_pixels = []
    # removes one pixel from each row of the colored image
    
    edited_pixels = [value for index, value in enumerate(image["pixels"]) if index not in seam]
    
    # returns new color image that has the seams removed
    return {"height": height,
            "width": width-1,
            "pixels": edited_pixels
            }

def emboss_filter(image, kernel):
    """
    Parameters:
        image, dict
            height, int
                height of the image
            width, int 
                width of the image
            pixels, list of tuples
                (r,g,b) values
                
       kernel, dictionary
            height, int
                height of the kernel
            width, int
                width of the kernel
            pixels, int
                list of kernel values
    Task:
        applies one of the directional emboss kernels to a colored image
    Return:
        new colored image
    """
    corr_image = correlate(image, kernel, "extend") 
    
    return round_and_clip_image(corr_image)

def custom_feature(image):
    """
    Parameters:
        image, dict
            height, int
                height of the image
            width, int 
                width of the image
            pixels, list of tuples
                (r,g,b) values
                
    Task:
        apply the emboss directional filter to a colored image
    Return:
        a new colored image with the emboss filter applied
    """
    
    kernel1 = {"height": 3,
               "width": 3,
               "pixels": [0, 1, 0,
                          0, 0, 0,
                          0, -1, 0]
               }
    
    color_image = {"height": image["height"],
                   "width": image["width"],
                   "pixels": image["pixels"].copy()
                   }
    """kernel2 = {"height": 3,
               "width": 3,
               "pixels":[1, 0, 0,
                         0, 0, 0,
                         0, 0, -1]
               }
    kernel3 = {"height": 3,
               "width": 3,
               "pixels":[0, 0, 0,
                         1, 0, -1,
                         0, 0, 0]
               }
    kernel4 = {"height": 3,
               "width": 3,
               "pixels":[0, 0, 1,
                         0, 0, 0,
                         -1, 0, 0]
               }
    emboss_kernel = [kernel1, kernel2, kernel3, kernel4]
   
    color_image = {"height": image["height"],
                   "width": image["width"],
                   "pixels": image["pixels"].copy()
                   }"""
                   
   """ # iterates through all the kernels and applies each of them to colored image
   for kern in emboss_kernel:
        color_filter = color_filter_from_greyscale_filter(emboss_filter)
        color_image = color_filter(color_image, kern)"""
        
    color_image = correlate(image, kernel1, "extend")
    
    # returns a new colored image with emboss filter applied
    return round_and_clip_image(color_image)
    
# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {"height": h, "width": w, "pixels": pixels}

def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError("Unsupported image mode: %r" % img.mode)
        w, h = img.size
        return {"height": h, "width": w, "pixels": pixels}

def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    """# colored inverted filter
    cat = load_color_image("test_images/cat.png")
    color_filter = color_filter_from_greyscale_filter(inverted)
    color_cat = color_filter(cat)
    save_color_image(color_cat, "color_cat.png")
    
    # blurring a colored image
    python = load_color_image("test_images/python.png")
    blurred_filter = color_filter_from_greyscale_filter(make_blur_filter(9))
    python_blurry = blurred_filter(python)
    save_color_image(python_blurry, "python_blurry.png")
    
    # sharpening a colored image
    sparrow = load_color_image("test_images/sparrowchick.png")
    sharpen_filter = color_filter_from_greyscale_filter(make_sharpen_filter(7))
    sparrow_sharp = sharpen_filter(sparrow)
    save_color_image(sparrow_sharp, "sparrow_sharp.png")
    
    # cascading filters applied to colored image
    frog = load_color_image("test_images/frog.png")
    filter1 = color_filter_from_greyscale_filter(edges)
    filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    filt = filter_cascade([filter1, filter1, filter2, filter1])
    frog_cascade = filt(frog)
    save_color_image(frog_cascade, "frog_cascade.png")"""
    
    """
    # seam carving
    twocats = load_color_image("test_images/twocats.png")
    seam_removed_two_cats = seam_carving(twocats, 100)
    save_color_image(seam_removed_two_cats, "seam_removed_two_cats.png")
    """
    # custom feature
    frog = load_color_image("test_images/frog.png")
    frog_emboss = custom_feature(frog)
    save_color_image(frog_emboss, "frog_emboss.png")
