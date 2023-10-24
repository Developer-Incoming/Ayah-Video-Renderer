import argparse
import QVersesSelector as qvsel

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

parser = argparse.ArgumentParser(
    prog=f"{Fore.GREEN}Ayah Video Renderer{Fore.RESET}",
    description=f"{Fore.CYAN}Renders Qur'anic verses into videos.{Fore.RESET}",
    epilog=f"{Fore.CYAN}Make sure to include the chapter and the needed start and end verse to produce it into a video.{Fore.RESET}"
)
subParser = parser.add_subparsers()

renderParser = subParser.add_parser("render")
renderParser.add_argument("filename")
renderParser.add_argument("-c", "--chapter",        type=int,   required=True, help="The index of the chapter")
renderParser.add_argument("-s", "--start-verse",    type=int,   default=0)
renderParser.add_argument("-e", "--end-verse",      type=int,   default=-1)
renderParser.add_argument("-r", "--reciter",        type=int,   default=1)
renderParser.add_argument("--reciters-folder",      type=str,   default="Reciters")
renderParser.add_argument("--verses-images-folder", type=str,   default="Verses Images")
renderParser.add_argument("--getVerseAudio",        type=bool,  default=True)
renderParser.add_argument("--getVerseImages",       type=bool,  default=True)
renderParser.add_argument("--colors",               type=bool,  default=True)

renderParser = subParser.add_parser("list")
renderParser.add_argument("-c", "--chapter", type=int)
# subParser.add_argument("-c", "--chapters")
# subParser.add_argument("-v", "--verses")

if __name__ == "__main__":
    args = parser.parse_args()
    print(vars(args))

    if not "filename" in vars(args):
        if args.chapter == None:
            qvsel.printChapters()
        else:
            qvsel.printVersesOf(chapterIndex=int(args.chapter) - 1)
    else:
        print("setup")
        input()
        qvsel.setup(
            reciterFolder=args.reciters_folder,
            verseImagesFolder=args.verses_images_folder,
            terminalColors=args.colors
        )
        
        reciterFolder = qvsel.selectReciter(preselect=int(args.reciter))
        selectedChapter, chapterIndex = qvsel.selectChapter(preselect=int(args.chapter))
        selectedVerses = qvsel.selectVerses(chapterIndex, preselectStart=int(args.start_verse), preselectEnd=int(args.end_verse))

        print(f'''{qvsel.colors.end}
        {type(reciterFolder)} - {reciterFolder}
        {type(selectedChapter)} - {selectedChapter}
        {type(chapterIndex)} - {chapterIndex}
        {type(selectedVerses)} - {selectedVerses}
        ''')

        input("\n\nsatisfied?")

        ## Fetched files
        verseFiles = qvsel.fetchFiles(
            reciterFolder=reciterFolder,
            chapterIndex=chapterIndex,
            selectedVerses=selectedVerses,
            getVerseAudio=True,
            getVerseImage=True
        )
        verseAudioFiles, verseImgFiles = verseFiles
        print(verseFiles)
