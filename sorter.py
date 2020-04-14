######Labhoratories######

#Import libraries
import os, os.path
import shutil
import pyfiglet
import keyboard
from difflib import SequenceMatcher

#Ascii banners for being cool
ascii_banner = pyfiglet.figlet_format("Hos File Sorter")
ascii_banner_fail = pyfiglet.figlet_format("Oh, c#ck!")
ascii_banner_success = pyfiglet.figlet_format("Finished")

#Print banner
print(ascii_banner)

#Set some variables up
dir_path = os.path.dirname(os.path.realpath(__file__))
path_script = os.path.realpath(__file__)
name_script = os.path.basename(__file__)

#Just to make sure if you want to continue
print("You are currently in {}".format(dir_path))

print("\nIf you do not wish to continue now. Close this window, otherwise press the enter key to start.")
keyboard.wait('enter')

#Start discoveirng files
print("\nDiscovering files in the directory...")

discoveredResults = [name for name in os.listdir('.') if os.path.isfile(name)]
discoveredResults.remove(name_script)
amountofResults = len(discoveredResults) - 1

#List the files
print("There are {} files in the chosen directory:".format(len(discoveredResults)))
for x in discoveredResults:
  print(x)

#Check for similarity between 2 variables funciton
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#Time for the main part of the script
print("\nMoving files and creating folders...")

while (amountofResults >= 0):
    #Set up soem variables for current file that's being worked on
    print("\nWorking with file {}...".format(discoveredResults[amountofResults]))
    filename, file_extension = os.path.splitext(discoveredResults[amountofResults])

    print("Discovering current folders.")
    folderList = [f.path for f in os.scandir(dir_path) if f.is_dir()]
    folderListCount = len(folderList) - 1
    # for x in folderList:
    #     print(x)

    #The brains
    try:
        while folderListCount >= 0:
            folderpath, foldername = os.path.split(folderList[folderListCount])
            similarity = similar(foldername, filename)
            #Check for similarity in filename and foldername, put them together
            if (similarity >= 0.6):
                print("Similarity >= 60%, moving file {} to folder {}. ".format(filename, foldername))
                folderLocationExisting = dir_path + "/" + foldername
                shutil.move(discoveredResults[amountofResults], folderLocationExisting)
                amountofResults -= 1
                FolderListCount = -1
                break
            else:
                folderListCount -= 1
                continue
         #If there is no folder do this
        if (folderListCount < 0):
            os.mkdir(filename)
            print("Folder created and now moving {}. ".format(filename))
            folderLocation = dir_path + "/" + filename
            shutil.move(discoveredResults[amountofResults], folderLocation)
            amountofResults -= 1
            continue

    except shutil.Error as e:
        print("Failed to move current file to folder.")
        print("File might already exist in folder, skipping...")
        amountofResults -= 1
    except:
        #fail message feat. James May
        print("\n", ascii_banner_fail)
        print("Something went wrong with moving the files and creating folders.")
        print("Press the enter key to quit")
        keyboard.wait('enter')
        exit()

print("\n", ascii_banner_success)
print("Finished with sorting. Scroll up for log.")
print("Press the enter key to quit")
keyboard.wait('enter')