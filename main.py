from PIL import Image
from PIL.TiffTags import TAGS
import tifffile as tiff
import matplotlib.pyplot as plt

def printDefaultTags(img):
   for tag in img.pages[0].tags.values():
      name, value = tag.name, tag.value
      if name in ('ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression',
                  'PhotometricInterpretation', 'SamplesPerPixel', 'PlanarConfiguration',
                  'ResolutionUnit', "XPTitle", "ImageDescription", 'RowsPerStrip',
                  'XResolution', 'YResolution',
                  'Artist'):
        print(f"{name}: {value}")

# Aby dodać kompletnie nowy tag dostajemy specjalny indeks dedykowany pod testy 65000
# który tworzy tag i przypisuje mu wartość
def addNewTag(img, newTagIndex, value):
  tiffinfo = img.tag_v2
  tiffinfo[newTagIndex] = value
  img.save("file2.tiff", tiffinfo=tiffinfo)
  print(img.tag_v2[newTagIndex])

def clearTag(img, tagIndex):
  tiffinfo = img.tag_v2
  tiffinfo[tagIndex] = ""
  img.save("file2.tiff", tiffinfo=tiffinfo)
  print(img.tag_v2[tagIndex])

def getHistogramTo16Bits(img):
  plt.hist(img.getdata(), bins=256, color='blue')
  plt.show()

def getColoursPaletteTo8Bits(img):
  palette = img.getpalette()
  print(palette)

with tiff.TiffFile('file.tiff') as img:
  printDefaultTags(img)


# with Image.open('file.tiff') as img:
  #  addNewTag(img, 270, "Example image")
  #  clearTag(img, 270)
  #  getColoursPaletteTo8Bits(img)
  #  getHistogramTo16Bits(img)