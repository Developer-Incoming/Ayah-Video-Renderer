from os import listdir
import QVersesSelector as qvsel

## External Libraries
from moviepy import editor # Used for video rendering, what did you expect?

# The amount of of number signs indicates comment's *unimportance*, just like markdown,
# but also means something has been commented to prevent its execution, most likely dev prints.

# Settings
settings = {
    "recitersFolder": "Reciters",
    "verseImagesFolder": "Verse Images",
    "outputPath": "Output",
    "disableTerminalColors": False,
    "minimumResolution": (1500, 500), # minimum, will be overwritten if any image is wider or longer.
    "backgroundColor": (235, 235, 235),
    "maskImages": True,
    "enumeratingOutputs": True, ## enumerating the videos or just replacing the existing file with a new one.
    "writeOutput": True
}

# Functions

## Starting, ending, or even containing X: str
def filesXingWith(xingWith: str, conditionFunc = str.startswith, dirPath = settings["outputPath"]) -> int:
    amount = 0
    
    for file in listdir(dirPath):
        if conditionFunc(file, xingWith):
            amount += 1
    
    return amount



#-- Functionality, a/k/a function calling

## Sets up QVersesSelector's settings
qvsel.setup(
    reciterFolder=settings["recitersFolder"],
    verseImagesFolder=settings["verseImagesFolder"],
    disableTerminalColors=settings["disableTerminalColors"]
)


reciterFolder = qvsel.selectReciter()
selectedChapter, chapterIndex = qvsel.selectChapter()
selectedVerses = qvsel.selectVerses(chapterIndex)

print(f'''{qvsel.colors.end}
{type(reciterFolder)} - {reciterFolder}
{type(selectedChapter)} - {selectedChapter}
{type(chapterIndex)} - {chapterIndex}
{type(selectedVerses)} - {selectedVerses}
''')

input("\n\nsatisfied?")

## Fetched files
verseFiles = qvsel.fetchFiles(reciterFolder, chapterIndex, selectedVerses, True, True)
verseAudioFiles, verseImgFiles = verseFiles
print(verseFiles)
input("\n\n oki doki?")

# Video creation
### VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip
clips_group0 = []
clips_group1 = []

nextClipEndTime = 0 # for appending clips' ending times
largestImageDimensions = settings["minimumResolution"] #(0, 0) # x, y -- for the output's resolution to fit the request
i = 0

## empty clip for later use
image_clip = None
clips_group0.append(image_clip)

image_clips = []
audio_clips = []

for verseRecitationPath in verseAudioFiles:
    verseImagePath = verseImgFiles[i]
    # print(f"{verseRecitationPath}{verseImagePath}")
    
    try:
        ## Clips creation process
        audio_clip = editor.AudioFileClip(verseRecitationPath)
        image_clip = editor.ImageClip(verseImagePath, ismask=settings["maskImages"])

        clipDuration = audio_clip.duration

        audio_clip = audio_clip.set_start(nextClipEndTime)
        print(audio_clip.buffersize)

        image_clip = image_clip.set_start(nextClipEndTime
        ).set_duration(clipDuration
        ).set_position(("center", "top"))

        largestImageDimensions = (
            image_clip.size[0] if image_clip.size[0] > largestImageDimensions[0] else largestImageDimensions[0],
            image_clip.size[1] if image_clip.size[1] > largestImageDimensions[1] else largestImageDimensions[1]
        )


        image_clips.append(image_clip)
        audio_clips.append(audio_clip)

        nextClipEndTime += clipDuration

        # print(nextClipEndTime)
    except OSError as err: ## handling file not found and such issues properly
        print(f"{qvsel.colors.red}Skipped verse {i + 1} because:{qvsel.colors.end}\n{err}")

    i += 1



# clips_group0[0] = editor.ColorClip(size=largestImageDimensions, color=settings["backgroundColor"], duration=nextClipEndTime).to_ImageClip()

# print(len(clips_group0)) 
# print(clips_group0)

fileTag = "" if not settings["enumeratingOutputs"] else f"{filesXingWith('output'):03}" ## output file naming

print(largestImageDimensions)

# videoClip0 = editor.ImageSequenceClip(clips_group0, fps=24)#, ismask=False)
# videoClip1 = editor.ImageSequenceClip(clips_group1, fps=24, ismask=True)

video_clip = editor.CompositeVideoClip(image_clips, size=largestImageDimensions).set_audio(editor.CompositeAudioClip(audio_clips))

# finalClip = editor.CompositeVideoClip(clips=image_clips, ismask=False, bg_color=settings["backgroundColor"])

if settings["writeOutput"]:
    video_clip.write_videofile(f"{settings['outputPath']}\\output{fileTag}.mp4", fps=24)
else:
    # finalClip.
    pass # TODO play video without writing to disk.
