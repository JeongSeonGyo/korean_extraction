from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path,outtxt):
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
	fp = file(path, 'rb')
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
	str = retstr.getvalue()
	output.write(str)
	retstr.close()
	output.close()
	return str

_
if __name__ == '__main__':
	path = '/home/user/python/2008_ipsn_koala.pdf'
	outtxt = '/home/user/python/outtxt.txt'
	words = convert_pdf_to_txt(path,outtxt)
	print words