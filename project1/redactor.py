import argparse
import nltk
import re
import pyap
from nltk.stem.porter import PorterStemmer
from thesaurus import Word
import inflect
import os
from pathlib import Path
import glob
import ntpath
import sys

# reads input file
def readFile(file):
    with open(file, 'r') as myFile:
        data = myFile.read()
    return data

# writes new redacted file
def outFlag(directory, file, myText):
    p = Path(os.getcwd()+'/'+directory)
    if p.is_dir() == False:
        os.mkdir(directory)
    path = directory + ntpath.basename(file)
    with open(path, 'w') as myFile:
        myFile.write(myText)

# finds the names in the input file and returns a list of names
def listNames(myText):
    myWordTok = nltk.word_tokenize(myText)
    myPOS = nltk.pos_tag(myWordTok)
    myList = []
    for chunk in nltk.ne_chunk(myPOS):
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                for c in chunk:
                    myList.append(c[0])
    return myList

# finds the dates in the input file and returns a list of dates
def listDates(myText):
    regEx = (r"\d{1,2}[-/]{1}\d{1,2}[-/]{1}\d{2,4}|"
             r"\d{2,4}[-/]{1}\d{1,2}[-/]{1}\d{1,2}|"
             r"\d{1,2}[-/]{1}\d{2,4}|"
             r"\d{1,2}[-/]{1}\d{1,2}|"
             r"\d{2,4}[-/]{1}\d{1,2}|"
             r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
             r"July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)"
             r"\s+\d{1,2},?\s+\d{4}|"
             r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
             r"July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)"
             r"\s+\d{1,2],?\s+\d{2}|"
             r"\d{1,2}\s+"
             r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
             r"July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)"
             r"\s+\d{4}|"
             r"\d{1,2}\s+"
             r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
             r"July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)"
             r"\s+\d{2}|"
             r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
             r"July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)"
             r"\s+\d{4}|"
             r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
             r"July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)"
             r"\s+\d{2}")
    myRe = re.compile(regEx)
    myList = myRe.findall(myText)
    return myList

# finds the addresses in the input file and returns a list of addresses
def listAddresses(myText):
    addresses = pyap.parse(myText, country='US')
    myList = []
    for address in addresses:
        tok = nltk.word_tokenize(str(address))
        for t in tok:
            myList.append(t)
    return myList

# finds the phone numbers in the input file and returns a list of phone numbers
def listPhones(myText):
    regEx = (r"(\(\d{3}\)\s*\d{3}[-\s\.]??\d{4}|"
             r"\d{3}[-\s\.]??\d{3}[-\s\.]??\d{4}|"
             r" \d{3}[-\s\.]??\d{4})")
    myRe = re.compile(regEx)
    phoneNums = myRe.findall(myText)
    myList = []
    for num in phoneNums:
        tok = nltk.word_tokenize(str(num))
        for t in tok:
            myList.append(t)
    return myList

# creates a list of gender words to find in the input file
def listGenders(myText):
    myList = ['he', 'she', 'his', 'hers', 'him', 'her', 'himself', 'herself', 'sister', 'brother', 'father', 'mother', 'aunt', 'uncle']
    return myList

# takes the concept word provided and finds its plural/singular, stem, and synonyms then returns a list of concept words
def listConcept(word):
    w = Word(word)
    iE = inflect.engine()
    pS = PorterStemmer()
    wordSyns = w.synonyms()
    myList1 = []
    myList1.append(word)
    for w in wordSyns:
        myList1.append(w)
    myList2 = myList1.copy()
    for w in myList2:
        pW = iE.plural(w)
        myList1.append(pW)
    myList3 = myList1.copy()
    for w in myList3:
        myList1.append(pS.stem(w))
    myList1 = list(dict.fromkeys(myList1))
    return myList1

# searches for a word or sentence in the input file, with this return I can find the span
def regExSearch(myString, myText):
    myRegEx = r'\b' + myString + r'\b'
    myRe = re.search(myRegEx, myText, re.IGNORECASE)
    return myRe

# replaces text at a given location with the block character
def strReplace(myStart, myEnd, myText):
    myLen = myEnd - myStart
    if myStart == 0:
        myText = '\u2588'*myLen + myText[myEnd:]
    else:
        myText = myText[0:myStart] + '\u2588'*myLen + myText[myEnd:]
    return myText

# replaces text at a given location with the light arc up and right character
def strReplace2(myStart, myEnd, myText):
    myLen = myEnd - myStart
    if myStart == 0:
        myText = '\u2570'*myLen + myText[myEnd:]
    else:
        myText = myText[0:myStart] + '\u2588'*myLen + myText[myEnd:]
    return myText

# first redacts the concepts, then redacts the list of words from the other flags
def redactList(myText, redactionTupleList, redactionConceptList):
    countConcepts = 0
    countNames = 0
    countDates = 0
    countAddresses = 0
    countPhones = 0
    countGenders = 0
    countTotal = 0
    redactionConceptList = sorted(redactionConceptList, key=len, reverse=True)
    redactionTupleList = sorted(redactionTupleList, key=lambda tup: tup[2], reverse=True)
    if len(redactionConceptList) > 0:
        mySentTok = nltk.sent_tokenize(myText)
        mySentList = []
        for m in mySentTok:
            for s in m.split('\n'):
                mySentList.append(s)
        while '' in mySentList:
            mySentList.remove('')
        for m in mySentList:
            for r in redactionConceptList:
                if r.endswith("'"):
                    r = r[:-1]
                elif r.endswith("'s"):
                    r = r[:-2]
                if m.endswith(".") or m.endswith("?") or m.endswith("!") or m.endswith(";"):
                    m = m[:-1]
                if regExSearch(r, m):
                    while myText.find(m) != -1:
                        countConcepts += 1
                        countTotal += 1
                        myStart = myText.find(m)
                        myEnd = myStart + len(m)
                        myText = strReplace(myStart, myEnd, myText)
    if len(redactionTupleList) > 0:
        for redact in redactionTupleList:
            if redact[1] != ',' and redact[1] != '(' and redact[1] != ')':
                if redact[1].endswith('.'):
                    r = redact[1][:-1]
                else:
                    r = redact[1]
                while regExSearch(r, myText):
                    if redact[0] == 'Names':
                        countNames += 1
                        countTotal += 1
                    elif redact[0] == 'Dates':
                        countDates += 1
                        countTotal += 1
                    elif redact[0] == 'Addresses':
                        countAddresses += 1
                        countTotal += 1
                    elif redact[0] == 'Phones':
                        countPhones += 1
                        countTotal += 1
                    elif redact[0] == 'Genders':
                        countGenders += 1
                        countTotal += 1
                    mySpan = regExSearch(r, myText).span()
                    myStart = mySpan[0]
                    myEnd = mySpan[1]
                    myText = strReplace(myStart, myEnd, myText)
    myDict = {'Concepts':countConcepts, 'Names':countNames, 'Dates':countDates, 'Addresses':countAddresses, 'Phones':countPhones, 'Genders':countGenders, 'Total':countTotal}
    return myText, myDict

# writes the stats file to its flagged location
def statsFlag(file, fileName, stats):
    kVal = ''
    for k in stats:
        a = stats[k]
        b = "For "+str(k)+", there were "+str(a)+" redactions.\n"
        kVal = kVal + b
    stats = ("These are the redaction statistics for "+fileName+".\n\n"+kVal+"\n"
             "Notes:\n"
             "    1) For Concepts, 1 redaction is a full sentence.\n"
             "    2) For Dates, 1 redaction is a full date sentence.\n"
             "    3) For Phones, 1 redaction is a full phone sentence.\n"
             "    4) For all others 1 redaction is a word.\n\n\n")
    if file == 'stderr':
        sys.stderr.write(stats)
    else:
        myDir = "statistics/"
        p = Path(os.getcwd()+'/'+myDir)
        if p.is_dir() == False:
            os.mkdir(myDir)
        path = myDir + ntpath.basename(fileName) + "." + file
        with open(path, 'w') as myFile:
            myFile.write(stats)

# main method
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="The text files to input", action="append")
    parser.add_argument("--names", help="option declaring if names are to be redacted", action="store_true")
    parser.add_argument("--dates", help="option declaring if dates are to be redacted", action="store_true")
    parser.add_argument("--addresses", help="option declaring if addresses are to be redacted", action="store_true")
    parser.add_argument("--phones", help="option declaring if phone numbers are to be redacted", action="store_true")
    parser.add_argument("--genders", help="option declaring if gender information is to be redacted", action="store_true")
    parser.add_argument("--concept", type=str, help="concept that is to be redacted", action="append")
    parser.add_argument("--output", type=str, help="location to save redacted files")
    parser.add_argument("--stats", type=str, help="where to write the statistics of the redactions")
    args = parser.parse_args()

    myFileList = []

    for a in args.input:
        myFileList.append(a)

    myFileGlobList = []

    for m in myFileList:
        myFileGlobList.extend(glob.glob(m))

    redactionConceptList = []
    if args.concept:
        for a in args.concept:
            conceptList = listConcept(a)
            for l in conceptList:
                redactionConceptList.append(l)

    for fileName in myFileGlobList:

        try:
            myText = readFile(fileName)
        except:
            sys.stderr.write("The file " + fileName + " was not read\n\n")
            continue
        redactedFile = myText

        redactionList = []
        redactionTupleList = []

        if args.dates:
            datesList = listDates(myText)
            for l in datesList:
                redactionList.append(l)
                redactionTupleList.append(('Dates',l, len(l)))

        if args.names:
            namesList = listNames(myText)
            for l in namesList:
                redactionList.append(l)
                redactionTupleList.append(('Names',l, len(l)))

        if args.addresses:
            addressesList = listAddresses(myText)
            for l in addressesList:
                redactionList.append(l)
                redactionTupleList.append(('Addresses',l, len(l)))

        if args.phones:
            phonesList = listPhones(myText)
            for l in phonesList:
                redactionList.append(l)
                redactionTupleList.append(('Phones',l, len(l)))

        if args.genders:
            gendersList = listGenders(myText)
            for l in gendersList:
                redactionList.append(l)
                redactionTupleList.append(('Genders',l, len(l)))

        redactedFile = redactList(myText, redactionTupleList, redactionConceptList)

        if args.output:
            newFileName = fileName+".redacted"
            outFlag(args.output, newFileName, redactedFile[0])

        if args.stats:
            statsFlag(args.stats, fileName, redactedFile[1])

if __name__ == '__main__':
    main()
