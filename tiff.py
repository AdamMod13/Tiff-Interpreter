from PIL import Image
import cv2
import numpy as np
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
    tiffinfo[int(newTagIndex)] = value
    img.save("file2.tiff", tiffinfo=tiffinfo)
    print(img.tag_v2[newTagIndex])


def clearTag(img, tagIndex):
    tiffinfo = img.tag_v2
    tiffinfo[int(tagIndex)] = ""
    img.save("file2.tiff", tiffinfo=tiffinfo)
    print(img.tag_v2[tagIndex])


def getHistogramTo16Bits(img):
    plt.hist(img.getdata(), bins=256, color='blue')
    plt.show()


def getColoursPaletteTo8Bits(img):
    palette = img.getpalette()
    print(palette)


def doFourierTransformation(img):
    f = np.fft.fft2(img)
    f_shift = np.fft.fftshift(f)

    magnitude_spec = 20*np.log(np.absolute(f_shift))

    magnitude_spec = cv2.normalize(
        magnitude_spec, None, 0, 255, cv2.NORM_MINMAX)

    cv2.imshow('Obraz oryginalny', img)
    cv2.imshow("Image after TF", magnitude_spec.astype('uint8'))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def maskTiffPersonalInfo(img):
    tags_to_anonymize = [270, 271, 272, 305, 306, 315, 316]
    tags = img.tag_v2

    for tag in tags.keys():
        if tag in tags_to_anonymize:
            tags[tag] = ""

    with Image.fromarray(np.array(img)) as im_output:
        im_output.save('anonimizowany_plik.tiff')


print("Program służy do analizy pliku w formacie tiff")
print("1 - Wyświetl podstawowe Tagi")
print("2 - Dodaj nowy Tag (dedykowany numer tagu -> 6300)")
print("3 - Wyczyść Tag")
print("4 - Wygeneruj histogram")
print("5 - Wygeneruj paletę kolorów")
print("6 - Wykonaj transformatę Fouriera")
print("7 - Wykonaj anonimizację")
choice = input("Podaj numer operacji: ")
tiff_file = input("Podaj nazwę pliku: ")

if (choice == "1"):
    with tiff.TiffFile(tiff_file) as img:  
        printDefaultTags(img)

elif (choice == "2"):
    text = input("Podaj zawartość tagu: ")
    with Image.open(tiff_file) as img:  
        addNewTag(img, 270, text)

elif (choice == "3"):
    tag = int(input("Podaj tag do usunięcia: "))
    with Image.open(tiff_file) as img:  
        clearTag(img, tag)

elif (choice == "4"):
    with Image.open(tiff_file) as img: 
        getHistogramTo16Bits(img)

elif (choice == "5"):
    with Image.open(tiff_file) as img: 
        getColoursPaletteTo8Bits(img)

elif (choice == "6"):
    with Image.open(tiff_file) as img:
        img = cv2.imread(tiff_file, 0)
        doFourierTransformation(img)
        
elif (choice == "7"):
    with Image.open(tiff_file) as img: 
        maskTiffPersonalInfo(img)


