### Organizes and fetches the necessary files to your liking.

import os
try:
    from colorama import init, Fore
    init()
except ImportError as exec:
    global Fore
    class Fore:
        LIGHTBLACK_EX = ""
        RED           = ""
        GREEN         = ""
        YELLOW        = ""
        CYAN          = ""
        RESET         = ""
    
    print(exec)

# Default settings in case the setup function isn't called.
settings = {
    "recitersFolder": "Reciters",
    "verseImagesFolder": "Verse Images",
    "terminalColors": "Fore" in dir() # imported Colorama?
}


## Setup chapters data
basePath = os.path.dirname(os.path.abspath(__file__))
chaptersData = []
with open(f"{basePath}\\Chapter Names.dat", mode="r") as chapterNamesFile:
    chaptersData = chapterNamesFile.read().splitlines()


# Functions

## Sets new settings, overwriting defaults
def setup(reciterFolder: str = "Reciters", verseImagesFolder: str = "Verses Images", terminalColors: bool = "Fore" in dir()):
    settings["reciterFolder"] = reciterFolder
    settings["verseImagesFolder"] = verseImagesFolder
    settings["terminalColors"] = terminalColors

## A simple function to validate user input by using a validator such as str.isdigit for instance, and use default input (0) when needed
def validateInput(inp: str, validator: str.isdigit = str.isdigit, default: str = "1") -> str:
    return inp if validator(inp) else default

## Prompts the user to select the reciter
def selectReciter(preselect: int = -1) -> str:
    dirs = []

    i = 0
    output = ""
    magicPath = f"{basePath}\\{settings['recitersFolder']}"

    for filename in os.listdir(magicPath):
        if os.path.isdir(f"{magicPath}\\{filename}"):
            dirs.append(f"{magicPath}\\{filename}")
            i += 1
            output += f"[ {Fore.GREEN}{i}{Fore.RESET} ] - {Fore.CYAN}{filename}{Fore.RESET}\n"
    
    if preselect != -1:
        print(f"{Fore.LIGHTBLACK_EX}Index {Fore.RESET}_{Fore.LIGHTBLACK_EX} Reciter{Fore.RESET}")
        print(output)

    return dirs[ preselect if preselect != -1 else int( validateInput(input(f"Select a reciter:{Fore.YELLOW} "), str.isdigit) ) - 1 ]

### Prints the chapters
def printChapters() -> None:
    i = 0
    output = []
    
    longestChapterLength = 0

    for chapterData in chaptersData:
        chapter, length = chaptersData[i].split(",")
        i += 1
        output.append(f"[ {Fore.GREEN}{' ' if i < 100 else ''}{i}{' ' if i < 10 else ''}{Fore.RESET} ] - {Fore.CYAN}{chapter}{Fore.RESET}")
        if longestChapterLength > len(chapter):
            longestChapterLength = len(chapter)
    
    print(f"{Fore.LIGHTBLACK_EX} Index {Fore.RESET} _{Fore.LIGHTBLACK_EX}  Chapter{Fore.RESET}")

    ## Better chapters print, ty spickeycactus [198167646510776320]
    used = []
    for string in output:
        if string in used:
            continue
        elif len(string) > 25:
            print(string)
            used.append(string)
            continue
        
        for short_string in output:
            if short_string in used:
                continue

            if len(short_string) < 35:
                print(string, short_string)

                used.append(string)
                used.append(short_string)

                break
        else:
            print(string)

## Prompts the user to select the chapter
def selectChapter(preselect: int = -1) -> list:
    if preselect != -1:
        printChapters()
    
    # for chapterData in output:
    #     print(chapterData)
    
    chapterIndex = preselect if preselect != -1 else int( validateInput(input(f"Select chapter:{Fore.YELLOW} "), str.isdigit) ) - 1
    return [chaptersData[chapterIndex], chapterIndex]

## Prompts the user to select the verses
def selectVerses(chapterIndex: int, preselectStart: int = -1, preselectEnd: int = -1) -> range:
    chapter, length = chaptersData[chapterIndex].split(",")

    if preselect != -1:
        print(f"{Fore.LIGHTBLACK_EX}Length {Fore.RESET}_{Fore.LIGHTBLACK_EX} Chapter{Fore.RESET}")
        print(f"( {Fore.GREEN}{length}{Fore.RESET} )  - {Fore.CYAN}{chapter}{Fore.RESET}\n")
    
    rawSelection = [preselectStart, preselectEnd] if preselectStart != -1 else (str( input(f"Select verses {Fore.LIGHTBLACK_EX}(start end){Fore.RESET}:{Fore.YELLOW} ") ).split(" ")[0:])
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
def fetchFiles(reciterFolder: str, chapterIndex: int, selectedVerses: range, getVerseAudio: bool, getVerseImage: bool) -> list[list[str], list[str]]:
    verses = []
    verseImages = []

    for verseIndex in selectedVerses:
        if getVerseAudio:
            verses.append(f"{reciterFolder}\\{(chapterIndex + 1):03}{(verseIndex):03}.mp3")
        if getVerseImage:
            verseImages.append(f"{basePath}\\{settings['verseImagesFolder']}\\{chapterIndex + 1}_{verseIndex}.png")
    
    return [verses, verseImages]

