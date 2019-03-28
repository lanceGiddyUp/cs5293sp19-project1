import pytest
from project1 import redactor

fileName = 'myText.txt'
concept = 'kid'

myText = redactor.readFile(fileName)
redactedFile = myText

redactionList = []
redactionTupleList = []
redactionConceptList = []

conceptList = redactor.listConcept(concept)
for l in conceptList:
    redactionConceptList.append(l)

datesList = redactor.listDates(myText)
for l in datesList:
    redactionList.append(l)
    redactionTupleList.append(('Dates', l, len(l)))

namesList = redactor.listNames(myText)
for l in namesList:
    redactionList.append(l)
    redactionTupleList.append(('Names', l, len(l)))

addressesList = redactor.listAddresses(myText)
for l in addressesList:
    redactionList.append(l)
    redactionTupleList.append(('Addresses',l, len(l)))

phonesList = redactor.listPhones(myText)
for l in phonesList:
    redactionList.append(l)
    redactionTupleList.append(('Phones',l, len(l)))

gendersList = redactor.listGenders(myText)
for l in gendersList:
    redactionList.append(l)
    redactionTupleList.append(('Genders',l, len(l)))

redactedFile = redactor.redactList(myText, redactionTupleList, redactionConceptList)

def test_readFile():
    assert len(myText) > 0

def test_concepts_count():
    assert redactedFile[1]['Concepts'] == 2

def test_names_count():
    assert redactedFile[1]['Names'] == 15

def test_dates_count():
    assert redactedFile[1]['Dates'] == 2

def test_addresses_count():
    assert redactedFile[1]['Addresses'] == 8

def test_phones_count():
    assert redactedFile[1]['Phones'] == 7

def test_genders_count():
    assert redactedFile[1]['Genders'] == 5

def test_total_count():
    assert redactedFile[1]['Total'] == 39
