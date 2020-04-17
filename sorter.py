######Labhoratories######

#Import libraries
import os, os.path
import shutil
import pyfiglet
from difflib import SequenceMatcher
import logging

#For getch both Win32 and Unix.
try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

#log
log_name = "log.log"
logging.basicConfig(filename=log_name, filemode='w', format='%(asctime)s - %(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
logging.info('Logging started')

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

#Set percentages and making sure if you want to continue
print("You are currently in {}".format(dir_path))
logging.debug("You are currently in {}".format(dir_path))

percentageDec = input("\nPlease enter the similarity percentage. (Default is 60%)")
try:
    percentageDec = int(percentageDec)
except:
        print("Input invalid value, defaulting to 60%")
        percentageDec = 60

if (percentageDec < 0):
    print("Percentage is lower than 0%, defaulting to 60%.")
    percentage = 0.6
else:
    if percentageDec > 100:
        print("Percentage is higher than 100%, defaulting to 60%.")
        percentage = 0.6
    else:
        print("\nPercentage set as {} %.".format(percentageDec))
        percentage = percentageDec / 100

while True:
    key = input("\nAre you sure you want to continue? Enter y to continue, n to quit.")
    if key in ('y', 'n', 'Y', 'N'):
        break
        
if key == "n":
    exit()

logging.info("Percentage set as {} %.".format(percentageDec))

#Start discovering files
print("\nDiscovering files in the directory...")
logging.info("Discovering files in the directory...")

discoveredResults = [name for name in os.listdir('.') if os.path.isfile(name)]
discoveredResults.remove(name_script)
discoveredResults.remove(log_name)
amountofResults = len(discoveredResults) - 1

#List the files
print("There are {} files in the chosen directory:".format(len(discoveredResults)))
for x in discoveredResults:
  print(x)
logging.info("There are {} files in the chosen directory:".format(len(discoveredResults)))

#Check for similarity between 2 variables funciton
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#Time for the main part of the script
print("\nMoving files and creating folders...")
logging.info("Moving files and creating folders...")

while (amountofResults >= 0):
    #Set up some variables for current file that's being worked on
    print("\nWorking with file {}...".format(discoveredResults[amountofResults]))
    filename, file_extension = os.path.splitext(discoveredResults[amountofResults])
    logging.info("Working with file {}...".format(discoveredResults[amountofResults]))

    print("Discovering current folders...")
    folderList = [f.path for f in os.scandir(dir_path) if f.is_dir()]
    folderListCount = len(folderList) - 1
    logging.info("Discovering current folders...")

    # for x in folderList:
    #     print(x)

    #The brains
    try:
        while folderListCount >= 0:
            folderpath, foldername = os.path.split(folderList[folderListCount])
            similarity = similar(foldername, filename)
            #Check for similarity in filename and foldername, put them together
            if (similarity >= percentage):
                print("Similarity >= {}%, moving file {} to folder {}. ".format(percentageDec, filename, foldername))
                logging.info("Similarity >= {}%, moving file {} to folder {}. ".format(percentageDec, filename, foldername))
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
            logging.info("Folder created and now moving {}. ".format(filename))
            folderLocation = dir_path + "/" + filename
            shutil.move(discoveredResults[amountofResults], folderLocation)
            amountofResults -= 1
            continue

    except shutil.Error as e:
        print("Failed to move current file to folder. Maybe the file already exists in the folder? Skipping...")
        logging.error("Failed to move current file to folder. Maybe the file already exists in the folder? Skipping...")
        amountofResults -= 1
    except:
        #fail message feat. James May
        logging.critical("Failed moving files and creating folders. Script stopped.")
        print("\n", ascii_banner_fail)
        print("Something went wrong with moving the files and creating folders.")
        print("Press any key to quit")
        getch()
        exit()

logging.info("Sorting finished")
print("\n", ascii_banner_success)
print("Finished with sorting. Check the log for the... log. Save the log if needed because the script will overwrite it next time.")
print("Press any key to quit")
getch()