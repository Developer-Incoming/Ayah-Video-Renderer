import os

## External Libraries
from moviepy import editor # Used for video rendering, what did you expect?

# The amount of of number signs indicates comment's *unimportance*, just like markdown

# Settings
recitersFolder = "Reciters"
verseImagesFolder = "Verse Images"
outputPath = "Output"
disableTerminalColors = False
enumeratingOutputs = False ## enumerating the videos or just replacing the existing file with a new one.


## colors for aesthetics
class colors:
    end = "\033[0m" if not disableTerminalColors else ""
    black = "\033[90m" if not disableTerminalColors else ""
    red = "\033[91m" if not disableTerminalColors else ""
    green = "\033[92m" if not disableTerminalColors else ""
    yellow = "\033[93m" if not disableTerminalColors else ""
    blue = "\033[94m" if not disableTerminalColors else ""
    magenta = "\033[95m" if not disableTerminalColors else ""
    cyan = "\033[96m" if not disableTerminalColors else ""
    white = "\033[97m" if not disableTerminalColors else ""


## Setup chapters data
basePath = os.path.dirname(os.path.abspath(__file__))
chaptersData = []
with open(f"{basePath}\\Chapter Names.dat", mode="r") as chapterNamesFile:
    chaptersData = chapterNamesFile.read().splitlines()


#-- Functions

## A simple function to validate user input by using a validator such as str.isdigit for instance, and use default input (0) when needed
def validateInput(inp: str, validator: str.isdigit = str.isdigit, default: str = "1") -> str:
    return inp if validator(inp) else default

## Starting, ending, or even containing X: str
def filesXingWith(xingWith: str, conditionFunc = str.startswith, dirPath = outputPath) -> int:
    amount = 0
    print("hyseyse@")
    for file in os.listdir(dirPath):
        print(file)
        if conditionFunc(file, xingWith):
            amount += 1
    
    return amount

## Prompts the user to select the reciter
def selectReciter() -> str:
    dirs = []

    i = 0
    output = ""
    magicPath = f"{basePath}\\{recitersFolder}"

    for filename in os.listdir(magicPath):
        if os.path.isdir(f"{magicPath}\\{filename}"):
            dirs.append(f"{magicPath}\\{filename}")
            i += 1
            output += f"[ {colors.green}{i}{colors.end} ] - {colors.blue}{filename}{colors.end}\n"
    
    print(f"{colors.black}Index {colors.end}_{colors.black} Reciter{colors.end}")
    print(output)

    return dirs[ int( validateInput(input(f"Select a reciter:{colors.yellow} "), str.isdigit) ) - 1 ]

## Prompts the user to select the chapter
def selectChapter() -> list:
    i = 0
    output = ""
    
    longestChapterLength = 0

    for chapterData in chaptersData:
        chapter, length = chaptersData[i].split(",")
        i += 1
        output += f"[ {colors.green}{i}{colors.end} ] - {colors.blue}{chapter}{colors.end}\n"
        if longestChapterLength > len(chapter):
            longestChapterLength = len(chapter)
    
    print(f"{colors.black}Index {colors.end}_{colors.black} Chapter{colors.end}")
    print(output)
    
    chapterIndex = int( validateInput(input(f"Select chapter:{colors.yellow} "), str.isdigit) ) - 1
    return [chaptersData[chapterIndex], chapterIndex]

## Prompts the user to select the verses
def selectVerses(chapterIndex: int) -> range:
    chapter, length = chaptersData[chapterIndex].split(",")

    print(f"{colors.black}Length {colors.end}_{colors.black} Chapter{colors.end}")
    print(f"( {colors.green}{length}{colors.end} )  - {colors.blue}{chapter}{colors.end}\n")

    rawSelection = str( validateInput(input(f"Select verses {colors.black}(start end){colors.end}:{colors.yellow} "), str.isdigit) ).split(" ")[0:]
    if len(rawSelection) > 1:
        startVerse, endVerse = rawSelection
        if startVerse > endVerse:
            temp = startVerse
            startVerse = endVerse
            endVerse = temp
        return range(int(startVerse), int(endVerse) + 1)
    else:
        endVerse = rawSelection[0]
        return range(1, int(endVerse) + 1)
    

## Fetches necessary files with parameters and then returns lists of data
def fetchFiles(reciterFolder: str, chapterIndex: int, selectedVerses: range, getVerses: bool, getImages: bool) -> list[list[str], list[str]]:
    verses = []
    verseImages = []

    for verseIndex in selectedVerses:
        if getVerses:
            verses.append(f"{reciterFolder}\\{(chapterIndex + 1):03}{(verseIndex):03}.mp3")
        if getImages:
            verseImages.append(f"{basePath}\\{verseImagesFolder}\\{chapterIndex + 1}_{verseIndex}.png")
    
    return [verses, verseImages]


#-- Functionality, a/k/a function calling

reciterFolder = selectReciter()
selectedChapter, chapterIndex = selectChapter()
selectedVerses = selectVerses(chapterIndex)

print(f'''
{type(reciterFolder)} - {reciterFolder}
{type(selectedChapter)} - {selectedChapter}
{type(chapterIndex)} - {chapterIndex}
{type(selectedVerses)} - {selectedVerses}
''')

## Fetched files
verseFiles = fetchFiles(reciterFolder, chapterIndex, selectedVerses, True, True)
verseAudioFiles, verseImgFiles = verseFiles
print(verseFiles)

# Video creation
### VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip
verse_clips = []
clipEnd = 0 # for appending clips' ending times
i = 0
for verseRecitationPath in verseAudioFiles:
    verseImagePath = verseImgFiles[i]
    print(f"\n{verseRecitationPath}\n{verseImagePath}\n")

    audio_clip = editor.AudioFileClip(verseRecitationPath)
    image_clip = editor.ImageClip(verseImagePath)

    clipDuration = audio_clip.duration

    audio_clip.set_start(clipEnd)
    image_clip = image_clip.set_start(clipEnd).set_audio(audioclip=audio_clip)
    image_clip = image_clip.set_duration(clipDuration)
    verse_clips.insert(i, image_clip)

    clipEnd += clipDuration

    i += 1

print(len(verse_clips))
print(verse_clips)

fileTag = "" if not enumeratingOutputs else f"{filesXingWith('output'):03}"

finalClip = editor.CompositeVideoClip(verse_clips)
finalClip.write_videofile(f"{outputPath}\\output{fileTag}.mp4", fps=24)
