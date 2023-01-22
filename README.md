# About kaniwani.py
This program reads a csv file with two words per line. These words should be separated by a comma. Then it will ask you the first word and you need to type in the second word. If you typed correctly, you move to the next word, until you are done with all. 

There's several options to configure its usage, but in its default way, it will tell you at the end which ones  you got wrong, so you can practice again. 

## Quick test

Open your terminal and assuming you have python3 installed, type: 

``python3 kaniwany.py --file words.csv``

(in the directory where you have ``kaniwany.py`` and our example file with words ``words.csv``)

## Making a file of words 
The file is quite simple, it is a comma-separated value (csv). It is a simple file with two words per line, each separated by a comma. For example, here's a valid file which we have included and called ``test.csv``:

``
木、もく
外人,がいじん
``
Note the file can use the separator , or 、(japanese).

Each line represents a word that will be asked to the user. For example `木` in the first line of the example above is the word that the user is trying to guess its meaning. The words in the same line, which are separated by commas and come right after `木` are its meanings. In this case `もく`. The user is not shown `もく` and tries to guess it by writing it when the program prompts the meaning of 木`. 

### japanese or english meanings

This program accepts "meaning" words in both japanese or english. 

``
木、もく
木、tree
``
Is a valid program. In fact, ``kaniwani`` will check the writing language used in the meaning word and will prompt the user accordingly:

1. ``木 in japanese: <prompts user for input here>`` (for the first line)
2. ``木 in english: <prompts user for input here>`` (for the second line)   

### multiple meanings

Furthermore, you can add multiple meanings too, as long as they follow on the same line of the word and just are added each in their own entry (i.e., comma separated). For example, the ``words.csv`` file that we include as a demo for this program has multiple meanings on all lines:

```
前、in front, before 
前、まえ、ぜん
```

## Options to invoke this program
On command line:

``python3 kaniwany.py``

This will start and ask you to input the filename of your words.csv file.

``python3 kaniwany.py help``

Will start the program with this text.

``python3 kaniwany.py --file words.csv``

This will start and load ``words.csv`` file. Replace ``words.csv`` with whatever file you want to load, keeping in mind the correct instructions on how to format your file.

## Producing output files 
If you want to productively study a particular set of words, you should keep track of the mistakes you made in a session. To assist you with that, this program produces a file called ``<date>typos.csv`` with the mistakes you made in your session. You can simply load this file when you invoke the program and keep iterating until you have no mistakes left. 

This option, like many other options, can be disabled directly in the source code by changing
``produce_output_file_of_mistakes = True`` to ``=False``. Refer to the section below for more details. 

## Special options
You can simply configure the options by changing the values in the ``kaniwani.py`` file directly. In the first lines of code, there's a series of ``Booleans`` that allow you to set options like disable random order, etc. Refer to actual source code for all the options.

## If you are using VI to edit your files

This section is maybe only for me, but perhaps you are also studying using this program and using ``vi``? If so, here's a few useful tips:

1. to duplicate every line of text (useful when editing the .csv files to create the translations/meanings) you can use ``:g/^/norm yyp``
2. to center your text in a big screen/etc (useful whe looking at or editing the csv in vi) you can, from a visual selection (``V``and select), run ``:center``

## Installing using requirements.txt

Yes, you can install via requirements.txt using the traditional ``pip install -r requirements.txt`` in your virtual environment. Note that if you find that libraries were still missing after this step, please let us know by filing a Github request/issue. 
