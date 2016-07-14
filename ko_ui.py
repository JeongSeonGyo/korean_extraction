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
import ko_extraction

reload(sys)
sys.setdefaultencoding('utf-8')

class MyListView(QListView):
	def ItemClicked(self,index):
		QMessageBox.information(None,"dk","ds")

class filedialogdemo(QWidget):
 	def __init__(self,parent = None):
		super(filedialogdemo, self).__init__(parent)


		layout = QVBoxLayout()
		layout.addStretch()
	
		self.le = QLabel("Select file and push Conversion button")

		layout.addWidget(self.le)
		self.btn1 = QPushButton("File open")
		self.btn1.clicked.connect(self.getfiles)
		layout.addWidget(self.btn1)

		
		self.setLayout(layout)
		self.setWindowTitle("Extract Word")

		self.btn2 = QPushButton("Conversion to text")
		self.btn2.clicked.connect(self.convert_pdf_to_txt)
		layout.addWidget(self.btn2)

		self.ql = QLineEdit()
		self.ql.setObjectName("Keyword")
		self.ql.setText("Input Keyword what you search")
		self.btn3 = QPushButton("Search")
		self.btn3.clicked.connect(self.search)
		layout.addWidget(self.ql)
		layout.addWidget(self.btn3)

		self.fl = MyListView(None)
		self.model = QStringListModel()

	def getfiles(self):
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.AnyFile)
		dlg.setFilter("Pdf files (*.pdf)")
		filename = QStringList()

		if dlg.exec_():
			filenames = dlg.selectedFiles()
			global f
			f = filenames[0]
		

	def convert_pdf_to_txt(self):
		token = f.split('/')

		global input_file 
		input_file = token[-1]
		
		filename_extension = input_file[-3:]

		global filename_txt
		filename_txt = 'txt_'+input_file[:-3]+'txt'

		path = os.path.dirname(os.path.abspath(__file__))
		outtxt = path + '/'+filename_txt
		
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
		fp = file(f, 'rb')
		
		output = open(outtxt,'w')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos = set()

		for page in PDFPage.get_pages(fp, pagenos, maxpages = maxpages, password = password, caching = caching, check_extractable = True):
			interpreter.process_page(page)
		
		fp.close()
		device.close()
		strg= retstr.getvalue()
		output.write(strg)
		retstr.close()
		output.close()
		
		#os_input = 'ko_modified_topic_modeling_and_frequency.py '+outtxt
		print "Convertion pdf to txt is Successfully finished"

		ext = ko_extraction.extract_korean()
		ext.extraction(filename_txt)

		return strg	


	def search(self):
		search_keyword = str(self.ql.text()).lower()
		
		result = []
	 	file_string = ''
	 	search_list = []
	 	start_time = time.time()
	 	
	 	with open('word.csv','rb') as archive:
    			archive.readline()
    			for line in archive:
    				if (search_keyword in line.lower()):
    					result.append(line)
    					
    			if (len(result)  == 0):
    				print "\nNo such File!"
    				file_string = "No Such File\n"
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

    				print file_string    			
    				print search_list
    				print len(search_list)
   		
    		self.model.setStringList(QString(file_string).split(";"))
    		self.fl.setModel(self.model)
    		self.fl.setWindowTitle("File list")
    		self.fl.show()

    		end_time = time.time()
    		print end_time - start_time
    		print "Search is successfuly finish!"
       


def main():
	app = QApplication(sys.argv)
	ex = filedialogdemo()
	ex.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
	