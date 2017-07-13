import os
from PIL import Image
from PIL.ImageOps import grayscale, posterize
def convertb(my_file):
    new_file = my_file + "_b"
    img=Image.open(my_file)
    img=grayscale(img)
    img.save(new_file, "PNG")
    os.remove(my_file)

def convertp(my_file):
    new_file = my_file + "_p"
    img=Image.open(my_file)
    img=posterize(img,2)
    img.save(new_file, "PNG")
    os.remove(my_file)
