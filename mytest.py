#!/usr/bin/python
# -*- coding: utf-8 -*-

from konlpy.corpus import kobill
from konlpy.tag import Twitter
import nltk
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

# read document
files_ko = kobill.fileids()
doc_ko = kobill.open('txt_Final_Report.txt').read()

#tokenize - use konlpy.tag.Twitter.morph
#t = Twitter()
tokens_ko = Twitter.__morph__(doc_ko)

#load tokens with nltk.Text() - provide easy fuctions to search each document
ko = nltk.Text(tokens_ko, name = 'Final Report')

print(len(ko.tokens)) # returns number of tokens
print(len(set(ko.tokens))) # returns number of unique tokens
ko.vocab() # returns frequency distribution