import argparse
import QVersesSelector as qvsel

parser = argparse.ArgumentParser(
    prog="Ayah Video Renderer",
    description="Renders Qur'anic verses into videos.",
    epilog="Make sure to include the chapter and the needed start and end verse to produce it into a video."
)

parser.add_argument("filename")
parser.add_argument("-c", "--chapter", type=int)
parser.add_argument("-s", "--start-verse", type=int)
parser.add_argument("-e", "--end-verse", type=int)
parser.add_argument("-r", "--reciter", type=int)
parser.add_argument("--reciters-folder", type=str, default="Reciters")
parser.add_argument("--verses-images-folder", type=str, default="Verses Images")
parser.add_argument("--getVerseAudio", type=bool, default=True)
parser.add_argument("--getVerseImages", type=bool, default=True)
parser.add_argument("--colors", type=bool, default=True)

if __name__ == "__main__":
    args = parser.parse_args()
    print(*{x for x in args._get_kwargs()})
    print(args.reciters_folder)
    input()
    qvsel.setup(
        reciterFolder=args.reciters_folder,
        verseImagesFolder=args.verses_images_folder,
        terminalColors=args.colors
    )
    input()
    
    reciterFolder = qvsel.selectReciter(preselect=args.reciter)
    selectedChapter, chapterIndex = qvsel.selectChapter(preselect=args.chapter)
    selectedVerses = qvsel.selectVerses(chapterIndex, preselectStart=args.start_verse, preselectEnd=args.end_verse)

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
    input("\n\n oki doki?")
    print("yes")
