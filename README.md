NAME:

    Lawrence Ensminger

REFERENCES:

    1) https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
        Used to understand ntpath for redacted output file
    2) https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
        Used to understand how to print to stderr
    3) https://stackoverflow.com/questions/32404666/python-generating-the-plural-noun-of-a-singular-noun/32404813
        Used to understand inflect to find singular and plural forms
    4) https://www.youtube.com/watch?v=FLZvOKSCkxY&list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL
        Used to help me understand a lot about NLP
    5) https://stackoverflow.com/questions/25778813/how-to-read-multiple-command-line-parameters-with-same-flag-in-python
        Used to help me understand how to read multiple command line parameters
    6) https://github.com/acrosson/nlp/blob/master/information-extraction.py
        Used to help me understand how to extract names (using chunking and named entity recognition)  and phone numbers
        (using regular expressions)
    7) https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk
        Used to help me understand named entity recognition

KNOWN BUGS:

    1) I don't know of any yet.  But, it seemed like every time I fixed something another issue
       would come up.  So, I assume there will be something that I missed.

ASSUMPTIONS:

    1) "Phrases" as concept were things like "little one" meaning child, not interpreting a
       sentence or longer phrase.
    2) For dates I redacted the entire date including whitespaces.  I did this so the month
       could not easily be guessed.  And looking for a day may also find a number that is not
       a date.

MODULES:

    1) import argparse:  to pass argurments
    2) import nltk:  to parse sentences
    3) import re:  to use regex
    4) import pyap:  for detecting and parsing addresses
    5) from nltk.stem.porter import PorterStemmer:  to stem words
    6) from thesaurus import Word:  synonyms
    7) import inflect:  plural/singular
    8) import os:  file read/write
    9) from pathlib import Path:  for file paths
    10) import glob:  for multiple files with paths
    11) import ntpath:  for file paths
    12) import sys:  stderr writing

HOW TO USE:

    From the Linux command line enter:
        pipenv run python project1/redactor.py --input '*.txt' --input 'otherfiles/*.txt'
        --phones --addresses --names --dates --genders --concept 'kids' --output 'files/'
        --stats stderr

    This reads in the .txt files flagged as inputs and redacts the flagged redaction elements
    and saves a new file to the specified location.

    This first makes a list of words to be redacted based on the flags.  Then for concepts,
    finds the words associated with the concept in the sentences and replaces sentence with the
    black box character.  For the other flags, it finds the words associated with the flags and
    replaces the characters of the words with the black box character.

    In addition, if stats is flagged a file (I used this flag as a file extension and saved the
    stats flags to a directory 'statistics'.  This way, if multiple files are redacted, each file
    will have its own stats file with the same name + the extention provided in the flag) is
    printed to the parameter passed through the flag, this can be a file name and path or stderr.
    The stats include how many redactions of each flag were made and the total of all redactions.
    Concept redactions were made by sentence and counted only once per sentence.  The format of
    the stats file provides the name of the file for the stats, and then a sentence for each flag
    saying "For concepts, there were X redactions.", and at the bottom there are notes explaining
    in more detail some of the output.

    Exclude any tags not desired.  With the exception that at least one input flag is required.

REDACTION FLAGS:

    Names:
        Anything with a PERSON tag in the nltk named entity recognition
        Examples:
            1) Bob Smith
            2) Mr. Bob Smith
            3) Bob

    Dates:
        Used regurlar expressions to find dates in the forms:
            1) 00/00/0000
            2) 00-00-0000
            3) Jan 00, 0000
            4) January 00, 0000
            5) 00 Jan 0000
            6) 00 January 0000
            7) and 2 digit year forms of above
            8) with and without the day
            9) or with the year coming first

    Addresses:
        Used pyap to identify and parse addresses.
        This identifies things like:
            1) street number
            2) street
            3) city
            4) state
            5) zip code.

    Phones:
        Used regurlar expressions to find phone numbers in the forms:
            1) 000-000-0000
            2) 000 000 0000
            3) (000)000-0000
            4) 000-0000

    Gender:
        I created this list to specify gender:
            ['he', 'she', 'his', 'hers', 'him', 'her', 'himself', 'herself', 'sister', 'brother',
             'father', 'mother', 'aunt', 'uncle']

    Concept:
        Any word related to the flagged concept by plural/singular form, stem, or synonym.

HOW TO TEST:

    From the command line:
        pipenv run python -m pytest

    I tested the file myText.txt saved in the cs5293sp19-project1 directory using the concept
    'kid'.

    The test file test_mine.py has 8 test methods:

        1) test_readFile()
            This tests to see if an input file was read
        2) test_concepts_count()
            This tests if the correct count of concept redactions were made.
        3) test_names_count()
            This tests if the correct count of name redactions were made.
        4) test_dates_count()
            This tests if the correct count of date redactions were made.
        5) test_addresses_count()
            This tests if the correct count of address redactions were made.
        6) test_phones_count()
            This tests if the correct count of phone number redactions were made.
        7) test_genders_count()
            This tests if the correct count of gender redactions were made.
        8) test_total_count()
            This tests if the correct count of total redactions were made.
