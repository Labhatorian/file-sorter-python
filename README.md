# file-sorter-python
Sort files in individual folders with multiple features for your comfort.

## Introduction
This is my second Python program so this is just my testing grounds for Python and Github itself. But I am also using this script for my own sorting of files.\
Open for contributions, as long as I can learn from them.

## How does it work
The script checks every file to see if a folder with a similiar enough name exists and then moves the file in there.\
Otherwise it will create a new folder and continue with the next file.

There are features that can influence the program that you can read below:

## How can you use it
Just put it in the folder with all the files you want to get it sorted.

## Important
This is in no way a perfect script. It makes mistakes for like 20% of the files, at least in my tests. You will probably need to still do some manual labour, but it will still be faster than doing every file invidually by hand. I do recommend playing around with the percentages, sometimes going higher will yield better results.

## Config
In the beginning of the script are a few variables you can change to your liking. However they don't do much. \
*Maybe there will be a variable for the percentage instead of it asking for one every time.*

### Setting a percentage
You will be prompted to set a percentage. This percentage will be used to check if the file and folder have similar enough names i.e. having it set to 50% means that the filename must match for 50% with the foldername. Otherwise make a new folder and move that file in the new folder.

### Ignored words list
Add an ignored.txt file with every ignored word on it's own line. (It is called ignored **words** list but you can put anything in there).\
It will remove the word from the filename before getting the similarity percentage. If the filename ends up empty, it will ignore the file alltogether.\
\
This does not remove parts of words in a file name i.e. ignored word is potato and the filename is potatocrop, potatocrop will not be changed.

### Logging
Disabled. Work in progress.

## Planned things
Logging and a reverse script. Be able to use them together
