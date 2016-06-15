import win32com
from win32com.client import Dispatch, constants
import sys,os
#讲word文档保存为XML格式
def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
		 
def wordSaveAsXml(path,filename,fileoutname):
	w=win32com.client.Dispatch('Word.Application')
	w.Visible=0
	w.DisplayAlerts=0
	doc=w.Documents.Open(path + '/' +filename)
	wc = win32com.client.constants
	doc.SaveAs(filenameout,11)
	doc.Close()
	w.Quit()
	
def wordToXMLTest(path):
	numfile=101
	w=win32com.client.Dispatch('Word.Application')
	w.Visible=0
	w.DisplayAlerts=0
	wc = win32com.client.constants
	for i in range(1,numfile):
		filename=path + '/T' + str(i) +'.docx'
		if os.path.exists(filename):
			doc=w.Documents.Open(filename)
			doc.SaveAs(path + '/T' + str(i),11)
			doc.Close()
	w.Quit()

def wordToXMLTrain(path):
	numfile=101
	w=win32com.client.Dispatch('Word.Application')
	w.Visible=0
	w.DisplayAlerts=0
	wc = win32com.client.constants
	for i in range(1,numfile):
		filename=path + '/' + str(i) +'.docx'
		if os.path.exists(filename):
			doc=w.Documents.Open(filename)
			doc.SaveAs(path + '/' + str(i),11)
			doc.Close()
	w.Quit()
if __name__=='__main__':
	# pass
	wordToXMLTest(cur_file_dir())