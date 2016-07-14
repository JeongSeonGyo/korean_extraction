#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from collections import Counter
from konlpy.corpus import kolaw
from konlpy.utils import concordance, pprint
from matplotlib import pyplot
from konlpy.tag import Komoran
import csv
import sys
import os 

reload(sys)
sys.setdefaultencoding('utf-8')

file = 'sing.txt'

doc = kolaw.open('sing.txt').read().lower()
print ("Start")

'''
pprint(pos)
#pos = k.sentences(doc)
#pprint(pos)
'''

path =os.path.dirname(os.path.abspath(__file__)) 
path_name = path +'/'+ file

pprint (path_name)

matrix = []

k = Komoran()
pos = k.nouns(doc)
cnt = Counter(pos)



#print('nchars  :', len(doc))
#print('ntokens :', len(doc.split()))
#print('nmorphs :', len(set(pos)))	#형태소
'''
print('\nTop 20 frequent morphemes:')
pprint(cnt.most_common(30))
print('\nLocations of "우주" in the document:')
concordance(u'우주', doc, show=False)
'''
# format : nonus, path
count = len(cnt)
data = cnt.most_common(count)

pprint (data)

#pprint (data)
'''
with open('word.csv', 'w') as f:
	f.write(',NP Chunk,FileName\n')
	writer = csv.writer(f,delimiter = ',')
	writer.writerows(data)
'''

with open('temp.csv', 'w') as f:
	f.write('NP,fre,FileName\n')
	writer = csv.writer(f,delimiter = ',')
	writer.writerows(data)


matrix = []

csv_file = open('temp.csv','rb')
reader = csv.reader(csv_file)
for row in reader:
	row.append(path_name)
	matrix.append(row)


with open('word.csv','a') as file:
	file.write('\nNP, fre, FileName\n')
	writer = csv.writer(file,delimiter = ',')
	writer.writerows(matrix)
	
