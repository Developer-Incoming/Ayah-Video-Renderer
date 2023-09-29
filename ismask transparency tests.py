import os, random, math

# TODO get all required images, resize them to the largest image in the requests then save them in a temp
# finally pipe them directly to the processing moviepy afterward you'll be able to use ImageSequenceClip, thus masking?
# import argparse TODO use this instead of manually complicating everything.

## External Libraries
from moviepy import editor # Used for video rendering, what did you expect?
from PIL import Image

# The amount of of number signs indicates comment's *unimportance*, just like markdown,
# but also means something has been commented to prevent its execution, most likely dev prints.

basePath = os.path.dirname(os.path.abspath(__file__))

# https://stackoverflow.com/a/27784150/13879297
def resizeCanvas(oldImagePath: str, newImagePath: str = "save.jpg", canvasWidth: int = 500, canvasHeight: int = 500):
    """
    Resize the canvas of oldImagePath.

    Store the new image in newImagePath. Center the image on the new canvas.

    Parameters
    ----------
    oldImagePath : str
    newImagePath : str
    canvasWidth : int
    canvasHeight : int
    """
    im = Image.open(oldImagePath)
    old_width, old_height = im.size

    # Center the image
    x1 = int(math.floor((canvasWidth - old_width) / 2))
    y1 = int(math.floor((canvasHeight - old_height) / 2))

    mode = im.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    elif len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)
    else:# len(mode) == 3:  # RGB
        new_background = (255, 255, 255)

    newImage = Image.new("RGBA", (canvasWidth, canvasHeight), (225, 225, 255, 255))
    print(im)
    newImage.paste(im, (0, 0, 0 + old_width, 0 + old_height))
    newImage.save(newImagePath)


def getImages(amount: int = 5) -> list[str]:
    largestImageDimensions = (25, 25)
    result = []

    for i in range(1, amount):
        imgPath = f"{basePath}\\Verse Images\\2_{i}.png"
        result.append(imgPath)
        imgResolution = Image.open(imgPath).size
        largestImageDimensions = (
            largestImageDimensions[0] if imgResolution[0] < largestImageDimensions[0] else imgResolution[0],
            largestImageDimensions[1] if imgResolution[1] < largestImageDimensions[1] else imgResolution[1]
        )
    
    return (largestImageDimensions, result)

def resizeImages(images: list[str], size: tuple) -> list[str]:
    result = []

    for img in images:
        newName = img.removeprefix(f"{basePath}\\Verse Images\\")
        resizeCanvas(img, f"{basePath}\\putput\\temp{newName}", size[0], size[1])
        result.append(f"{basePath}\\putput\\temp{newName}")

    return result

print(basePath)
resolution, images = getImages(15)
print(images)
print(resolution)
Image.new("RGBA", resolution, (255, 255, 255, 255)).save(f"{basePath}\\putput\\temp_bg.png")
background = f"{basePath}\\putput\\temp_bg.png"
input()
requestedImgs = [background, *resizeImages(images, resolution)]

print(type(requestedImgs))
input(requestedImgs)

for reqImg in requestedImgs:
    print(Image.open(reqImg).size)

imgSequence = editor.ImageSequenceClip(requestedImgs, durations=[1 for _ in range(len(requestedImgs))], with_mask=True, ismask=True)

# videoComposition = editor.CompositeVideoClip(imgSequence, size=(1500, 500), bg_color=(235, 235, 235))
imgSequence.write_videofile(f"{basePath}\\putput\\sussy wussy.mp4", audio=False, fps=24)
# for imagePath in getImages():
