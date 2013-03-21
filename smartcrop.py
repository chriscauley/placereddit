from PIL import Image
import math,datetime

def cache_entropies(image):
  return entropy_x(image), entropy_y(image)

def image_entropy(img):
  """calculate the entropy of an image"""
  hist = img.histogram()
  hist_size = sum(hist)
  hist = [float(h) / hist_size for h in hist]
  return -sum([p * math.log(p, 2) for p in hist if p != 0])

def entropy_x(img):
  x,y = img.size
  dx = 10
  out = ""
  while True:
    right = img.crop((x-dx,0,x,y))
    left = img.crop((0,0,dx,y))
    if image_entropy(left) < image_entropy(right):
      img = img.crop((dx, 0, x, y))
      out += "0"
    else:
      img = img.crop((0, 0, x-dx, y))
      out += "1"

    x,y = img.size

    if x <= dx:
      return out

def entropy_y(img):
  x,y = img.size
  dy = 10
  out = ""
  while True:
    bot = img.crop((0,y-dy,x,y))
    top = img.crop((0,0,x,dy))
    if image_entropy(top) < image_entropy(bot):
      img = img.crop((0, dy, x, y))
      out += "0"
    else:
      img = img.crop((0, 0, x, y-dy))
      out += "1"

    x,y = img.size

    if y < dy:
      return out

def scale_image(image,size):
  if image.mode != "RGB":
    image = image.convert('RGB')
 
  image.thumbnail(size, Image.ANTIALIAS)
  return image


def crop_image(image,thumbnail_size,x_crop_order,y_crop_order,multiplier):
  """
  returns a cropped image.
  image = PIL.Image object
  thumbnail_size = (width,height) to be returned
  x/y_crop_order = a "binary string" telling which side to crop from for each dimension
    0 means left/top chunck is less entropic, 1 means right/bottom chunk is more entropic
  multiplier = (1..10)
    the crop orders are defaulted to 10px, but we're using pre-resized images.
    pre-resized images are (1..10)/10 times the size of the original
    so the multiplier tells the size of the slices
  """
  x,y = image.size
  th_x, th_y = thumbnail_size

  #the image is smaller than the minimum thumbnail dimensions
  if x < th_x and y < th_y:
    return image

  dx = abs(x-th_x)
  from_left = x_crop_order[:dx/int(multiplier)].count('0')*multiplier
  from_right = dx-from_left

  dy = abs(y-th_y)
  from_top = y_crop_order[:dy/int(multiplier)].count('0')*multiplier
  from_bot = dy-from_top
  return image.crop((from_left,from_top,x-from_right,y-from_bot))
