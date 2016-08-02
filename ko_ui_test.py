#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import docx #for docx file

from django.utils.encoding import smart_str, smart_unicode

#for korean
from konlpy.corpus import kolaw
from konlpy.utils import concordance, pprint
from matplotlib import pyplot
from konlpy.tag import Komoran

import sys 

#for ui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#for pdf file 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import os
import time

import ko_extraction #for korean keyword extraction


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
		self.setWindowTitle("Word Extraction")

		self.btn2 = QPushButton("Converse file format")
		self.btn2.clicked.connect(self.convert)
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
		dlg.setNameFilters(["pdf files (*.pdf)" , "docx files (*.docx)", "odt files (*.odt)", "text files (*.txt)", "hwp files (*.hwp)", "All files (*.*)"])
		filename = QStringList()

		print os.getcwd()

		if dlg.exec_():
			filenames = dlg.selectedFiles()
			global f
			f = filenames[0]
			global filepath
			filepath = os.path.dirname(str(f))
			
	def convert(self):

		# check whether variable 'f' exist or not
		if 'f' not in globals().keys():
			print "ERROR! You OPEN file first"
			return

		token = f.split('/')

		global input_file 
		input_file = token[-1] # ex : what.pdf
		
		filename_extension = input_file[-4:] #ex: pdf docx ...

		if filename_extension == 'docx':
			filename_extension = filename_extension
			extension_num = -4
		else:
			filename_extension = input_file[-3:]
			extension_num = -3


		filename_txt = 'txt_'+input_file[:extension_num]+'txt' #ex: txt_filename.txt
		
		#path = os.path.dirname(os.path.abspath(__file__))	#/home/user/pyhon/code

		global outtxt
		outtxt = os.getcwd() + '/'+filename_txt	#os.getcwd() ; current path
		path_plus_file = filepath + '/' + input_file
		
		#for different file type
		if filename_extension == "pdf":
			print "Start convert pdf to txt"
			self.convert_pdf_to_txt()

		elif filename_extension == "docx":
			print "Start convert docx to txt"
			self.convert_docx_to_txt(input_file)

		elif filename_extension == "txt":
			print "Text file don't need to convert. Do next step"

		elif filename_extension == "hwp":
			print "Start convert hwp to txt"
			self.convert_hwp_to_txt(input_file)			

		elif filename_extension == "odt":
			print "Start convert odt to txt"
			self.convert_odt_to_txt(input_file)
		
		else:
			print ("Sorry, We Don't support %s file." %filename_extension)
			return
			'''
			elif filename_extension == "doc":
				print "Start convert doc to txt"
				self.convert_doc_to_txt(input_file)
			'''
		#for extraction korean keyword
		ext = ko_extraction.extract_korean()
		ext.extraction(filename_txt,filepath,input_file)
		

	def convert_pdf_to_txt(self):
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
		#return strg	

	def convert_doc_to_txt(self,f):    
		output = open(outtxt,'w')
		
		output.write(strg)
		output.close()

		print "Conversion doc to txt is successufully finished"
		#return strg
	    
	def convert_docx_to_txt(self,f):
		output = open(outtxt,'w')
		document = docx.opendocx(str(f))

		paratextlist = docx.getdocumenttext(document)
		newparatextlist = []
		for paratext in paratextlist:
			newparatextlist.append(paratext.encode('utf-8'))
		print "Convertion docx to txt is Successfully finished"
		strg = '\n\n'.join(newparatextlist)
		output.write(strg)
		output.close()

		#return strg

	def convert_odt_to_txt(self,f):
		output = open(outtxt,'w')		
		os.system("odt2txt " + str(f) + " > " + str(outtxt))
	   	output.close()

	   	print "Convertion odt to txt is Successfully finished"

	def convert_hwp_to_txt(self,f):
		output = open(outtxt,'w')		
		os.system("hwp5txt " + str(f) + " > " + str(outtxt))
	   	output.close()

	   	print "Convertion hwp to txt is Successfully finished"

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

    				file_string = unicode(str(file_string).decode('utf-8'))
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
