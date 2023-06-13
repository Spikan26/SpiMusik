from update_check import checkForUpdates

ListOfFiles = ["SpiMusic.py", "README.md",
               ".gitignore", ".gitattributes", "SpiUpdate.py"]

for file in ListOfFiles:
    try:
        print("Checking for updates : " + file)
        checkForUpdates(
            file, "https://raw.githubusercontent.com/Spikan26/SpiMusik/main/"+file)
    except:
        print("Couldn't find or couldn't update the file "+file)

print("All files updated")
