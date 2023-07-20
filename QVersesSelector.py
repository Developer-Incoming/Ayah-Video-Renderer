### Organizes and fetches the necessary files to your liking.


import os
# import argparse TODO use this instead of manually complicating everything.


# TODO recode verses selector


# Default settings in case the setup function isn't called.
settings = {
    "recitersFolder": "Reciters",
    "verseImagesFolder": "Verse Images",
    "disableTerminalColors": False
}

## Colors for aesthetics
class colors:            ## sorry
    end = "\033[0m"      if not settings["disableTerminalColors"] else ""
    black = "\033[90m"   if not settings["disableTerminalColors"] else ""
    red = "\033[91m"     if not settings["disableTerminalColors"] else ""
    green = "\033[92m"   if not settings["disableTerminalColors"] else ""
    yellow = "\033[93m"  if not settings["disableTerminalColors"] else ""
    blue = "\033[94m"    if not settings["disableTerminalColors"] else ""
    magenta = "\033[95m" if not settings["disableTerminalColors"] else ""
    cyan = "\033[96m"    if not settings["disableTerminalColors"] else ""
    white = "\033[97m"   if not settings["disableTerminalColors"] else ""


## Setup chapters data
basePath = os.path.dirname(os.path.abspath(__file__))
chaptersData = []
with open(f"{basePath}\\Chapter Names.dat", mode="r") as chapterNamesFile:
    chaptersData = chapterNamesFile.read().splitlines()


# Functions

## Sets new settings, overwriting defaults
def setup(reciterFolder: str = "Reciters", verseImagesFolder: str = "Verse Images", disableTerminalColors: bool = False):
    settings["reciterFolder"] = reciterFolder
    settings["verseImagesFolder"] = verseImagesFolder
    settings["disableTerminalColors"] = disableTerminalColors

    ### updates colors' class
    global colors
    class colors:
        end = "\033[0m"      if not settings["disableTerminalColors"] else ""
        black = "\033[90m"   if not settings["disableTerminalColors"] else ""
        red = "\033[91m"     if not settings["disableTerminalColors"] else ""
        green = "\033[92m"   if not settings["disableTerminalColors"] else ""
        yellow = "\033[93m"  if not settings["disableTerminalColors"] else ""
        blue = "\033[94m"    if not settings["disableTerminalColors"] else ""
        magenta = "\033[95m" if not settings["disableTerminalColors"] else ""
        cyan = "\033[96m"    if not settings["disableTerminalColors"] else ""
        white = "\033[97m"   if not settings["disableTerminalColors"] else ""

## A simple function to validate user input by using a validator such as str.isdigit for instance, and use default input (0) when needed
def validateInput(inp: str, validator: str.isdigit = str.isdigit, default: str = "1") -> str:
    return inp if validator(inp) else default

## Prompts the user to select the reciter
def selectReciter() -> str:
    dirs = []

    i = 0
    output = ""
    magicPath = f"{basePath}\\{settings['recitersFolder']}"

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
    output = []
    
    longestChapterLength = 0

    for chapterData in chaptersData:
        chapter, length = chaptersData[i].split(",")
        i += 1
        output.append(f"[ {colors.green}{i}{colors.end} ] - {colors.blue}{chapter}{colors.end}")
        if longestChapterLength > len(chapter):
            longestChapterLength = len(chapter)
    
    print(f"{colors.black}Index {colors.end}_{colors.black} Chapter{colors.end}")

    ## Better chapters print, ty spickeycactus [198167646510776320]
    used = []
    for string in output:
        if string in used:
            continue
        elif len(string) > 10:
            print(string)
            used.append(string)
            continue
        
        for short_string in output:
            if short_string in used:
                continue

            if len(short_string) < 5:
                print(string, short_string)

                used.append(string)
                used.append(short_string)

                break
        else:
            print(string)

    # for chapterData in output:
    #     print(chapterData)
    
    chapterIndex = int( validateInput(input(f"Select chapter:{colors.yellow} "), str.isdigit) ) - 1
    return [chaptersData[chapterIndex], chapterIndex]

## Prompts the user to select the verses
def selectVerses(chapterIndex: int) -> range:
    chapter, length = chaptersData[chapterIndex].split(",")

    print(f"{colors.black}Length {colors.end}_{colors.black} Chapter{colors.end}")
    print(f"( {colors.green}{length}{colors.end} )  - {colors.blue}{chapter}{colors.end}\n")

    rawSelection = str( input(f"Select verses {colors.black}(start end){colors.end}:{colors.yellow} ") ).split(" ")[0:]
    if len(rawSelection) < 1:
        rawSelection = ["1"]
    elif len(rawSelection) > 1:
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
            verseImages.append(f"{basePath}\\{settings['verseImagesFolder']}\\{chapterIndex + 1}_{verseIndex}.png")
    
    return [verses, verseImages]
