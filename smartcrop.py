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

def prepare_image(image,thumbnail_size,x_crop_order,y_crop_order):
  x,y = image.size
  ratio_in = x / float(y)
  th_x, th_y = thumbnail_size
  ratio_out = th_x / float(th_y)

  #the image is smaller than the minimum thumbnail dimensions
  if x < th_x and y < th_y:
    return image

  if ratio_out < ratio_in: #image too wide
    x_out = int(ratio_out*y)
    dx = abs(x-x_out)
    from_left = x_crop_order[:dx/10].count('0')*10
    from_right = dx-from_left
    im = image.crop((from_left,0,x-from_right,y))
  elif ratio_out > ratio_in: #image too tall
    y_out = int(x/ratio_out)
    dy = abs(y-y_out)
    from_top = y_crop_order[:dy/10].count('0')*10
    from_bot = dy-from_top
    im = image.crop((0,from_top,x,y-from_bot))
  else: #it's already crop
    im = image

  if im.mode != "RGB":
    im = im.convert('RGB')

  im.thumbnail(thumbnail_size, Image.ANTIALIAS)
  return im
