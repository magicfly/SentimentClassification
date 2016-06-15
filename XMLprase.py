#coding=utf-8
import  xml.dom.minidom
import os,sys
#提取XML文档中评论文字
def cur_file_dirTwo():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
		 
def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename='user.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')
#以tag1和tag2为匹配标签提取文字	
def getTextFromXML(path,tag1,tag2):
	domp = xml.dom.minidom.parse(path)
	root = domp.documentElement
	tagwr = root.getElementsByTagName(tag1)
	value=''
	for each in tagwr:
		try:
			node=get_xmlnode(each,tag2)
			value=value + get_nodevalue(node[0])
		except Exception as e:
			pass
	return value	
#提取XML文档中评论文字
def getText(path):
	return getTextFromXML(path,'w:r','w:t')
#提取XML文档中标为红色 color='FF0000' 的褒义词
def getPositiveWords(path):
	domp = xml.dom.minidom.parse(path)
	root = domp.documentElement
	tagwr = root.getElementsByTagName('w:r')
	value=[]
	for each in tagwr:
		node=get_xmlnode(each,'w:rPr')
		for eachTwo in node:
			try:
				if(eachTwo.childNodes[2].attributes['w:val'].value=='FF0000'):
					textnode=get_xmlnode(each,'w:t')
					value.append(get_nodevalue(textnode[0]))
			except Exception as e:
				# print(Exception,":",e)
				pass
	return value	
#提取XML文档中标为绿色 color='00B050' 的贬义词
def getNegativeWords(path):
	domp = xml.dom.minidom.parse(path)
	root = domp.documentElement
	tagwr = root.getElementsByTagName('w:r')
	value=[]
	for each in tagwr:
		node=get_xmlnode(each,'w:rPr')
		for eachTwo in node:
			try:
				if(eachTwo.childNodes[2].attributes['w:val'].value=='00B050'):
					textnode=get_xmlnode(each,'w:t')
					value.append(get_nodevalue(textnode[0]))
			except Exception as e:
				# print(Exception,":",e)
				pass
	return value
#保存list列表为txt文档
def writeWordsToTXT(listw,filename):
	outputf=open(filename,'w+')
	for each in listw:
		outputf.write(str(each)+'\r\n')
	outputf.close()

if __name__=='__main__':
	# for i in range(100):
		# print(i+1)
		# filename=cur_file_dirTwo() + '/' + str(i+1) + '.xml'
		# if os.path.exists(filename):
			# print(getText(filename))
	pass