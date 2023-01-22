import sys 
import re
import random
from datetime import datetime
import urllib.parse
import urllib.request
import webbrowser

# using jisho (.org) as a dictionary for lookups
from jisho_api.word import Word
from jisho_api.kanji import Kanji
from jisho_api.sentence import Sentence
from jisho_api.tokenize import Tokens

# options
silence_correct_answers = True
silence_wrong_answers = False
allow_for_cheating = True
skip_enabled = False
produce_output_file_of_mistakes = True
random_order = True
search_engine = "https://jisho.org/search/"
debug = False

# messages for each event
message_correct = "Correct!"

message_wrong = "Wrong."

message_options_on_wrong = """ Options are:
[enter]\tretry
+\tmark as correct
-\tmark as wrong 
0\treveal answer
j\tsearch in jisho.org (display here)
b\tsearch in jisho.org (display browser)
x\texit"""

if_word_is_roman_character_based = "in english"
if_word_is_not_roman_character_based = "in ひらがな"
if_word_is_empty_draw_its_kanji = "in 漢字 (write down, then press any key to self-assess answer or type correct using keyboard after you wrote it down)"

message_help = """
Welcome to kaniwani!

== About == 
This program reads a csv file with two words per line. 
These words should be separated by a comma.
Then it will ask you the first word and you need to
type in the second word. If you typed correctly, you
move to the next word, until you are done with all. 

There's several options to configure its usage, but
in its default way, it will tell you at the end which ones 
you got wrong, so you can practice again. 

== Making a file of words ==
The file is quite simple, it is a comma-separated value (csv)
file with two words per line, each separated by a comma. 
For example, here's a valid file
------------- file contents -------------
木、もく
外人,がいじん
------------- end of file ---------------
Note the file can use the separator , or 、(japanese).
You can add comments by starting a line with # or ＃.

== Invoking this program ==
On command line:
    >python3 kaniwany.py
    This will start and ask you to input the filename
    of your words.csv file.

    >python3 kaniwany.py help
    Will start the program with this text.

    >python3 kaniwany.py --file filename.csv
    This will start and load filename.csv

== Special options == 
You can simply configure the options by changing the values
in the kaniwani.py file

== Producing output files == 
If you want to productively study, you can set the option
that produce_output_file_of_mistakes = True
With this option set, at the end of each session the program will
produce a file called typos.csv, which all the ones you got wrong.
This way you can simply run the program again and choosing
typos.csv as the input set of words. Keep working on it until
you have no typos left."""


#---------------------------------------------------------------

def test_internet(host='http://jisho.org/'):
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False

def print_if_debug(*args,**kwargs):
        if debug:
            return print("DEBUG:\t",*args,**kwargs)
        else:
            pass

# check if user has supplied filename as argument
# otherwise, ask for it
if len(sys.argv) == 1:
    filename = input("Type the name of the file to open:")
else:
    if sys.argv[1] == "--help":
        print(message_help)
        sys.exit()
    elif sys.argv[1] == "--file" and len(sys.argv) >= 2:
        filename = sys.argv[2]
    else:
        filename = sys.argv[1]

print("Note: ", end='')
print( "jisho.org is available for online dictionary lookups"  if test_internet() else " jisho.org is not available for online dictionary lookups (cause: likely your internet connection is not available or jisho itself is not available)" )

# load words from file
words = []
with open(filename) as csv_file:
    for row in csv_file:
        if row[0] == '#' or row[0] == '＃':
            continue #jumps over comments
        row = re.split(',|、', row)
        meanings = []
        for w in row[1:]:
            meanings.append(w.strip())
        words.append([row[0],meanings,0]) #0 1 -1 
    print("{0} words loaded from {1}".format(len(words),filename))
print("==== Start ====")

if random_order:
    random.shuffle(words)

print_if_debug("shuffle done")

exit = False
# ask each word once
for i in range(0,len(words)):
    print_if_debug("{0} out of {1}".format(i+1, len(words)))
    if exit:
        print("==== Stop ====")
        break
    advance = False
    while not advance:

        if words[i][1][0] == '': 
            print_if_debug("empty for kanji!")
            user_answer = input(words[i][0]+" {0}: ".format(if_word_is_empty_draw_its_kanji))
        
        else:

            if re.match("^[a-zA-Z\s./-/']+$",words[i][1][0]): #check first meaning only
                # in english 
                user_answer = input(words[i][0]+" {0}: ".format(if_word_is_roman_character_based))
            else: 
                # in japanese
                user_answer = input(words[i][0]+" {0}: ".format(if_word_is_not_roman_character_based))
        
        if user_answer == "": #skip a word by just not typing it
            if skip_enabled:
                advance = True
            else:
                advance = False
        else:
            for meaning in words[i][1]:
                if user_answer == meaning:
                    if not silence_correct_answers:
                        print(message_correct)
                    words[i][2]=1 #set as correct
                    advance = True
                    break
            else:
                if not silence_wrong_answers:
                    print(message_wrong, end = '')
                if allow_for_cheating:
                    print(message_options_on_wrong, end = '')
                    if produce_output_file_of_mistakes:
                        print(" (will save progress in {0}_typos.csv file".format(datetime.today().strftime('%Y-%m-%d')))
                    else:
                        print()
                    option = input("option: ")
                    if option == "+" or option == "＋":
                        words[i][2]=1 #set as correct
                        advance = True
                    elif option == "-" or option == "ー":
                        words[i][2]=-1 #set as wrong
                        advance = True
                    elif option == "0" or option == "０":
                        print(words[i][1])
                        advance = False
                    elif option == "j" or option == "J" or option == "じ":
                        if words[i][1][0] == '': 
                            #webbrowser.open(search_engine+urllib.parse.quote((words[i][1])[1])+"%23kanji")
                            r = Kanji.request((words[i][1])[1])
                        else: 
                            #webbrowser.open(search_engine+urllib.parse.quote(words[i][0])+"%23kanji")
                            r = Kanji.request(words[i][0])
                        r.rich_print()
                        advance = False
                    elif option == "b" or option == "B" or option == "ぶ":
                        if words[i][1][0] == '': 
                            webbrowser.open(search_engine+urllib.parse.quote((words[i][1])[1])+"%23kanji")
                        else: 
                            webbrowser.open(search_engine+urllib.parse.quote(words[i][0])+"%23kanji")
                        advance = False

                    elif option =="x":
                        advance = True
                        exit = True
                        break
                    else:
                        #retry without increments
                        advance = False
                else:
                    print()
                    words[i][2]=-1 #set as wrong

# print stats at the end
typos = 0
if produce_output_file_of_mistakes:
    typos_filename = "{0}_typos.csv".format(datetime.today().strftime('%Y-%m-%d'))
    typosfile = open(typos_filename, "w")

for i, word in enumerate(words):
    if word[2] == -1:
        typos+=1
if typos >= 1:
    print("==== {0} Mistake(s) ====".format(typos))
    typos_idx = 1
    for i, word in enumerate(words):
        if word[2] == -1:
            print(typos_idx, end = ': ')
            typos_idx+=1
            print("{0} is ".format(word[0]), end = '')
            for idx, meaning in enumerate(word[1]):
                print("{1}".format(word[0], meaning), end = '')
                if idx != len(word[1])-1:
                    print(", ", end = '')
            print()
            if produce_output_file_of_mistakes:
                print("{0},{1}".format(word[0], word[1]),file=typosfile)
    typosfile.close()
    print("{0} Mistake(s) saved to {1} \n(hint: you can load the program with that file to iteratively finish your study of this set)".format(typos, typos_filename))
else:
    print("==== Perfect! ====")
