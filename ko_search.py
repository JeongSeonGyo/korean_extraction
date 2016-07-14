#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from django.utils.encoding import smart_str, smart_unicode
from collections import Counter

from konlpy.corpus import kolaw
from konlpy.utils import concordance, pprint
from matplotlib import pyplot
from konlpy.tag import Komoran

import sys 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import os
import time
import extraction


search_keyword = str('그림자')

result = []
file_string = ''
search_list = []
start_time = time.time()

#keyword_cnt = doc.count(search_keyword)

#print ("\nkeyword count =")

with open('word.csv','rb') as archive:
        archive.readline()
        for line in archive:
            if (search_keyword in line.lower()):
                result.append(line)
                
        if (len(result)  == 0):
            print "\nNo such File!"
            del search_list[0:len(search_list)]
        else:
            for a in result:
                token2 = a.split(',')
                search_file =  token2[-1]
                
                search_list.append(search_file[:-1])
              
            search_list = list(set(search_list))
            
            file_string = ''
            for b in range(len(search_list)):
                file_string = file_string + search_list[b] + ';'

            print "\nfile_string"
            print file_string               
            print search_list
            print len(search_list)

            # QObject.connect(self.fl, SIGNAL("clicked(QModelIndex)"),
            #   self.fl,SLOT("ItemClicked(QModelIndex)"))
end_time = time.time()
print end_time - start_time
print "Search is successfully finished!"