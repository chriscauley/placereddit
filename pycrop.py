import math
from PIL import Image

def prepare_image(image, thumbnail_size):
  x,y = image.size
  ratio_in = x / float(y)
  th_x, th_y = thumbnail_size
  ratio_out = th_x / float(th_y)
  
  #the image is smaller than the minimum thumbnail dimensions
  if x < th_x and y < th_y:
    return image 
  
  if ratio_out > ratio_in: #wide image
    im = crop_tall_image(image,ratio_out)
  elif ratio_out < ratio_in: #tall image
    im = crop_wide_image(image,ratio_out)
  else: #it's already crop
    im = image  
  
  if im.mode != "RGB":
    im = im.convert('RGB')

  im.thumbnail(thumbnail_size, Image.ANTIALIAS)
  return im

def image_entropy(img):
  """calculate the entropy of an image"""
  hist = img.histogram()
  hist_size = sum(hist)
  hist = [float(h) / hist_size for h in hist]
  return -sum([p * math.log(p, 2) for p in hist if p != 0])

def crop_wide_image(img,ratio):
  x,y = img.size
  while ratio < float(x) / y:
    #slice 10px at a time until crop
    slice_width = min(int(x-y*ratio), 10)
    right = img.crop((x-slice_width, 0, x, y))
    left = img.crop((0, 0, slice_width, y))

    #remove the slice with the least entropy
    if image_entropy(left) < image_entropy(right):
      img = img.crop((slice_width, 0, x, y)) #crop the left side
    else:
      img = img.crop((0,0,x-slice_width, y)) #crop the right side

    x,y = img.size

  return img
  
def crop_tall_image(img,ratio):
  """if the image is taller than it is wide, crop it off. determine
  which pieces to cut off based on the entropy pieces."""
  x,y = img.size
  while ratio > float(x) / y:
    #slice 10px at a time until crop
    slice_height = min(int(y*ratio-x), 10)

    bottom = img.crop((0, y - slice_height, x, y))
    top = img.crop((0, 0, x, slice_height))

    #remove the slice with the least entropy
    if image_entropy(bottom) < image_entropy(top):
      img = img.crop((0, 0, x, y - slice_height))
    else:
      img = img.crop((0, slice_height, x, y))

    x,y = img.size

  return img
