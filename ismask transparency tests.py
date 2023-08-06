import os, random, imageio

# TODO get all required images, resize them to the largest image in the requests then save them in a temp
# finally pipe them directly to the processing moviepy afterward you'll be able to use ImageSequenceClip, thus masking?
# import argparse TODO use this instead of manually complicating everything.

## External Libraries
from moviepy import editor # Used for video rendering, what did you expect?

# The amount of of number signs indicates comment's *unimportance*, just like markdown,
# but also means something has been commented to prevent its execution, most likely dev prints.

basePath = os.path.dirname(__file__)

def getImages(amount: int = 5) -> list[str]:
    result = []

    for i in range(1, amount):
        result.append(f"{basePath}\\Verse Images\\2_{i}.png")
    
    return result

print(basePath)
requestedImgs = getImages(50)

input(requestedImgs)

imgSequence = editor.ImageSequenceClip(requestedImgs, durations=10, fps=24)

# videoComposition = editor.CompositeVideoClip(imgSequence, size=(1500, 500), bg_color=(235, 235, 235))
imgSequence.write_videofile(f"{basePath}\\putput\\sussy wussy.mp4", audio=False)
# for imagePath in getImages():
