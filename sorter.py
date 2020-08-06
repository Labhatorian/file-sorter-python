######Labhoratories######
# !----- Libraries -----!
# Included with Python
import os, os.path
import shutil
import re
from difflib import SequenceMatcher

#For getch, both Win32 and Unix.
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
            

# !----- Banners -----!
# Created with Pyfiglet
ascii_banner = " _   _             _____ _ _        ____             _            \n| | | | ___  ___  |  ___(_) | ___  / ___|  ___  _ __| |_ ___ _ __ \n| |_| |/ _ \\/ __| | |_  | | |/ _ \\ \\___ \\ / _ \\| '__| __/ _ \\ '__|\n|  _  | (_) \\__ \\ |  _| | | |  __/  ___) | (_) | |  | ||  __/ |   \n|_| |_|\\___/|___/ |_|   |_|_|\\___| |____/ \\___/|_|   \\__\\___|_|   \n                                                                  \n"
ascii_banner_fail = "  ___  _                _  _        _    _ \n / _ \\| |__       ___ _| || |_  ___| | _| |\n| | | | '_ \\     / __|_  ..  _|/ __| |/ / |\n| |_| | | | |_  | (__|_      _| (__|   <|_|\n \\___/|_| |_( )  \\___| |_||_|  \\___|_|\\_(_)\n            |/                             \n"
ascii_banner_success = " _____ _       _     _              _ \n|  ___(_)_ __ (_)___| |__   ___  __| |\n| |_  | | '_ \\| / __| '_ \\ / _ \\/ _` |\n|  _| | | | | | \\__ \\ | | |  __/ (_| |\n|_|   |_|_| |_|_|___/_| |_|\\___|\\__,_|\n                                      \n"

#Print banner
print(ascii_banner)

# !----- Config -----!
#Don't change these
dir_path = os.path.dirname(os.path.realpath(__file__))
path_script = os.path.realpath(__file__)
name_script = os.path.basename(__file__)
IgnoredFileFound = 0

#You can change these, make sure you rename your ignored file too.
debug = 0
ask_log = 1
ask_percentage = 0
percentageConfig = 60
name_ignored = "ignored.txt"
log_name = "moved.txt"
# !----- Ignored words -----!
try:
    with open(name_ignored,'r') as f:
        ignored_list = [str(x) for x in f]
    f.close
    IgnoredFileFound = 1
except FileNotFoundError:
    print("Ignored list not found.")

# !----- Log -----!
try:
    log = open("log.txt", "r")
    if ask_log == 1:
        print("There is already a log file in the files.")
        while True:
            key = input("\nAre you sure you want to continue? The log file will then get overwritten. Enter y to continue, n to quit.")
            if key in ('y', 'n', 'Y', 'N'):
                break
        
        if key == "n":
            exit()
    log.close
    log = open("log.txt", "w")
except FileNotFoundError:
    print("Log File not found.")
    log = open("log.txt", "w")
# !----- Percentages -----!
# Set percentage to check for
print("You are currently in {}".format(dir_path))

if ask_percentage == 1:
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
else:
    percentageDec = percentageConfig
    percentage = percentageDec / 100
    print("Config ask_percentage set to 0 => Percentage set as {}%".format(percentageConfig))

# !----- Discover files -----!
print("\nDiscovering files in the directory...")

discoveredResults = [name for name in os.listdir('.') if os.path.isfile(name) and name != name_script and name != log_name]

if (IgnoredFileFound == 1):   
    discoveredResults.remove(name_ignored)
amountofResults = len(discoveredResults) - 1

# !----- List files -----!
print("There are {} files in the chosen directory:".format(len(discoveredResults)))
for x in discoveredResults:
  print(x)

# !----- Function for getting percentage of similarity in names -----!
def similar(a, b):
    if IgnoredFileFound ==1:
        for x in ignored_list:
            x = x.rstrip('\n')
            b = re.sub(r"\b{}\b".format(x), " ", b)
            a = re.sub(r"\b{}\b".format(x), " ", a)
    global EmptyFile
    if b == " ":
        EmptyFile = 1

    return SequenceMatcher(None, a, b).ratio()

# !----- Find folders -----!
print("Discovering current folders.")
folderList = [f.path for f in os.scandir(dir_path) if f.is_dir()]
folderList = [x.lower() for x in folderList]

# !----- Get to work -----!
print("\nMoving files and creating folders...")

while (amountofResults >= 0):
    #Set up some variables for the current file that's being worked on
    print("\nWorking with file {}...".format(discoveredResults[amountofResults]))
    filename, file_extension = os.path.splitext(discoveredResults[amountofResults])
    filename = filename.lower()
    folderListCount = len(folderList) - 1
    EmptyFile = 0

    #The main function of the program
    try:
        while folderListCount >= 0:
            folderpath, foldername = os.path.split(folderList[folderListCount])
            foldername = foldername.lower()
            similarity = similar(foldername, filename)
            if debug == 1:
                print(similarity)
            #Check for similarity in filename and foldername, put them together if okay
            if (similarity >= percentage):
                print("Similarity >= {}%, moving file {} to folder {}. ".format(percentageDec, filename, foldername))
                folderLocationExisting = dir_path + "\\" + foldername
                shutil.move(discoveredResults[amountofResults], folderLocationExisting)

                newFileLocation = folderLocationExisting + "\\" + filename + file_extension
                log.write("{}\n".format(newFileLocation))

                amountofResults -= 1
                FolderListCount = -1
                break
            else:
                folderListCount -= 1
                continue

        if EmptyFile == 1:
                break

         #If there is no folder, create one.
        if (folderListCount < 0):
            os.mkdir(filename)
            print("Folder created and now moving {}. ".format(filename))
            folderLocation = dir_path + "\\" + filename
            shutil.move(discoveredResults[amountofResults], folderLocation)
            
            newFileLocation = folderLocationExisting + "\\" + filename + file_extension
            log.write("{}\n".format(newFileLocation))

            #Add the new folder to the current pool of folders
            folderList.append(folderLocation)
            amountofResults -= 1
            continue

    except shutil.Error as e:
        print("Failed to move current file to folder.")
        print("File might already exist in folder, skipping...")
        amountofResults -= 1

log.close
print("\n", ascii_banner_success)
print("Finished with sorting. Scroll up for detailed log.")
print("Press any key to quit")
getch()