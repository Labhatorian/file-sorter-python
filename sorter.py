######Labhoratories######
# !----- Libraries -----!
#TODO: Bundle libraries with python.
import os, os.path
import shutil
import pyfiglet
import re
from difflib import SequenceMatcher

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
            

# !----- Banners -----!
ascii_banner = pyfiglet.figlet_format("Hos File Sorter")
ascii_banner_fail = pyfiglet.figlet_format("Oh, c#ck!")
ascii_banner_success = pyfiglet.figlet_format("Finished")

#Print banner
print(ascii_banner)

# !----- Variable setup -----!
dir_path = os.path.dirname(os.path.realpath(__file__))
path_script = os.path.realpath(__file__)
name_script = os.path.basename(__file__)
name_ignored = "ignored.txt"
IgnoredFileFound = 0

log_name = "moved.txt"

# !----- Ignored words -----!
try:
    with open(name_ignored,'r') as f:
        ignored_list = [str(x) for x in f]
    f.close
    IgnoredFileFound = 1
except FileNotFoundError:
    print("Ignored words list not found.")

# !----- Percentages -----!
print("You are currently in {}".format(dir_path))

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


# !----- Discover files -----!
#f = open("moved.txt","w+")
print("\nDiscovering files in the directory...")

discoveredResults = [name for name in os.listdir('.') if os.path.isfile(name) and name != name_script]
#discoveredResults.remove(name_script)

if (IgnoredFileFound == 1):   
    discoveredResults.remove(name_ignored)
amountofResults = len(discoveredResults) - 1

# !----- List files -----!
print("There are {} files in the chosen directory:".format(len(discoveredResults)))
for x in discoveredResults:
  print(x)

# !----- Function for getting percentage of similarity in names -----!
def similar(a, b):
    for x in ignored_list:
        x = x.rstrip('\n')
       # b = b.str.replace(x, " ") # !---- IS A FILE
        b = re.sub(r"\b{}\b".format(x), " ", b)

    global EmptyFile
    if b == " ":
        EmptyFile = 1

    return SequenceMatcher(None, a, b).ratio()

# !----- Get to work-----!
print("\nMoving files and creating folders...")

while (amountofResults >= 0):
    #Set up some variables for current file that's being worked on
    print("\nWorking with file {}...".format(discoveredResults[amountofResults]))
    filename, file_extension = os.path.splitext(discoveredResults[amountofResults])
    filename = filename.lower()
    EmptyFile = 0

    print("Discovering current folders.")
    folderList = [f.path for f in os.scandir(dir_path) if f.is_dir()]
    folderList = [x.lower() for x in folderList]
    folderListCount = len(folderList) - 1

    #The main function of the program
    try:
        while folderListCount >= 0:
            folderpath, foldername = os.path.split(folderList[folderListCount])
            foldername = foldername.lower()
            similarity = similar(foldername, filename)

            #Check for similarity in filename and foldername, put them together
            if (similarity >= percentage):
                print("Similarity >= {}%, moving file {} to folder {}. ".format(percentageDec, filename, foldername))
                folderLocationExisting = dir_path + "/" + foldername
                shutil.move(discoveredResults[amountofResults], folderLocationExisting)
                amountofResults -= 1
                FolderListCount = -1
                break
            else:
                folderListCount -= 1
                continue

        if EmptyFile == 1:
                break

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



# !----- WIP-----!
  # except:
        #fail message feat. James May
      #  print("\n", ascii_banner_fail)
       # print("Something went wrong with moving the files and creating folders.")
       # print("Press any key to quit")
       # getch()
       # exit()

# f.close

# if os.path.exists("movedlists"):
#     try:
#         folderLocation = "movedlists" + "/" + "moved.txt"
#         shutil.move("moved.txt", "movedlists")
#     except shutil.Error as e:
#         try: 
#             for i in log_name:
#                 try:
#                     os.rename(r"log_name",r'moved.txt%s.xml' % i)
#                     shutil.move("moved.txt", "movedlists")
# else:
#     try:
#         os.mkdir("movedlists")
#         shutil.move("moved.txt", "movedlists")
#     except shutil.Error as e:
#         try: 
#             os.rename(r'file path\OLD file name.file type',r'file path\NEW file name.file type')
#             shutil.move("moved.txt", "movedlists")
#         except shutil.Error as e:
#         #fail message feat. James May
#             print("\n", ascii_banner_fail)
#             print("Something went wrong with moving the log.")
#             print("Press any key to quit")
#             getch()
#             exit()
    

print("\n", ascii_banner_success)
print("Finished with sorting. Scroll up for log.")
print("Press any key to quit")
getch()