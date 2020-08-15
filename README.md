# About kaniwani.py
This program reads a csv file with two words per line. These words should be separated by a comma. Then it will ask you the first word and you need to type in the second word. If you typed correctly, you move to the next word, until you are done with all. 

There's several options to configure its usage, but in its default way, it will tell you at the end which ones  you got wrong, so you can practice again. 

## Making a file of words 
The file is quite simple, it is a comma-separated value (csv). It is a simple file with two words per line, each separated by a comma. For example, here's a valid file which we have included and called ``test.csv``:

``
木、もく
外人,がいじん
``
Note the file can use the separator , or 、(japanese).

## Invoking this program
On command line:

``python3 kaniwany.py``

This will start and ask you to input the filename of your words.csv file.

``python3 kaniwany.py help``

Will start the program with this text.

``python3 kaniwany.py --file filename.csv``

This will start and load filename.csv

## Special options
You can simply configure the options by changing the values
in the ``kaniwani.py`` file. 

## Producing output files 
If you want to productively study, you can set the option that ``produce_output_file_of_mistakes = True`` With this option set, at the end of each session the program will produce a file called typos.csv, which all the ones you got wrong. This way you can simply run the program again and choosing ``typos.csv`` as the input set of words. Keep working on it until
you have no typos left.

