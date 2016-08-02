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

class extract_korean:

	def __init__(self):
		self.file = ''

	def extraction(self,f,p,original_file):
		global file
		file = f


		


		doc = kolaw.open(os.getcwd(),file).read().lower()

		doc = kolaw.open(file).read().lower()
		print ("Start keyword extraction.")

		k = Komoran()
		pos = k.nouns(doc)
	 
		cnt = Counter(pos)
		# format : nonus, frequency, path
		count = len(cnt)
		

		global data 
		data = cnt.most_common(count)
		self.to_csv(p,original_file)
		


	def to_csv(self,path,origin_f):
		matrix = []
		#path =os.path.dirname(os.path.abspath(__file__)) 
		path_plus_filename = path + '/' + origin_f
		
		with open('temp.csv', 'w') as f:
			writer = csv.writer(f,delimiter = ',')
			writer.writerows(data)
		print "First conversion to csv is successfully finished"

		csv_file = open('temp.csv','rb')
		reader = csv.reader(csv_file)
		for row in reader:
			row.append(path_plus_filename)
			matrix.append(row)
		print "Second conversion to csv is successfully finished"

		with open('word.csv','a') as final:
			final.write('NP, frequency, FileName\n')
			writer = csv.writer(final,delimiter = ',')
			writer.writerows(matrix)
		print "Finally Conversion text to csv is successfully finished"
 

		os.system("rm temp.csv")
		os.system("rm txt_*.txt")

 
