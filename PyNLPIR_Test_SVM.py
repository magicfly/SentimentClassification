#!/usr/bin/env python
import pynlpir
import string
##Importing PyNLPIR
import svmutil
import codecs
import XMLprase
import urllib  
import sys,os
import math
import sys
#计算tf-idf值
def tfidf(list, word):
	countdoc=0#出现word的文档数目
	countword=0
	for each in list:
		if each[0]==word[1]:#找到匹配的文档id号
			for eachword in each[1]:
				if eachword[0]==word[0]:
					countword+=1
			tf=countword/len(each[1])#该id文档中word词频
		if word[0] in each[1]:
				countdoc+=1#所有文档中出现word的文档数
	idf=math.log(len(list)/(1+countdoc),2)#防止出现word的文档数目为0使用1+countdoc
	return (tf*idf)
#判断字符串中是否有英文字符
def checkletters(a):
	letters = string.ascii_letters
	if (type(a) is not str):
		return False
	else:
		for i in a:
			if i in letters:
				return True
		return False
#判断字符串中是否有数字
def check(a):
	nums = string.digits
	if (type(a) is not str):
		return False
	else:
		for i in a:
			if i in nums:
				return True
		return False
#打印输出文档头部
def printTitle():
    ##Print Title for Result
    print('Id\tStudent-Num\tWord-String\tWord-Polarity\tDoc-Id\tContext-String\tConfidence-Score')
    return None
#返回文档头部
def strTitle():
	return ('Id\tStudent-Num\tWord-String\tWord-Polarity\tDoc-Id\tContext-String\tConfidence-Score\r\n')
#输出列表时首先添加tab
def addTabForList(list1):
    ##Format every element in the List to string and add Tab after.
    temp=''
    for each in list1:
        temp+=str(each)+'\t'
    return temp
#打印结果
def printResult(idnum,word_string,word_polarity,doc_id,context_string,confidence_score,student_num='1150332032'):
    listT=[]
    listT.append(idNum)
    listT.append(student_num)
    listT.append(word_string)
    listT.append(word_polarity)
    listT.append(doc_id)
    listT.append(context_string)
    listT.append(confidence_score)
    print(addTabForList(listT))
    return None
def strResult(idnum,word_string,word_polarity,doc_id,context_string,confidence_score,student_num='1150332032'):
    listT=[]
    listT.append(idnum)
    listT.append(student_num)
    listT.append(word_string)
    listT.append(word_polarity)
    listT.append(doc_id)
    listT.append(context_string)
    listT.append(confidence_score)
    return(addTabForList(listT)+'\r\n')
#载入停用词文档
def loadStopwords(path_stopwords='./stopwords.txt'):
	fstopwords=codecs.open(path_stopwords,'r','utf-8')
	ltemp=fstopwords.readlines()
	# print(len(ltemp))
	return ltemp
#删除停用词，分词有词性标记时使用
def removeStopwords(segment_list,stopwords_list):
	count=0
	listremove=[]
	for each in segment_list:
		if (each[1]==u'punctuation mark' or each[1]==u'numeral'):
			listremove.append(each)
		else:
			ueach=each[0]+u'\r\n'
			if ueach in stopwords_list:
				listremove.append(each)
			elif check(each[0]) or checkletters(each[0]):
				listremove.append(each)
	for eachw in listremove:
		segment_list.remove(eachw)
	return segment_list
#删除停用词，分词无词性标记时使用
def removeStopwordsNoTag(segment_list,stopwords_list):
	count=0
	listremove=[]
	for each in segment_list:
		ueach=each+u'\r\n'
		if ueach in stopwords_list:
			listremove.append(each)
		elif check(each) or checkletters(each):
			listremove.append(each)
	for eachnum in listremove:
		segment_list.remove(eachnum)
	return segment_list
#获得列表数组中全部单词个数
def getTotalWordsNum(list_list):
	listnum=0
	for each in list_list:
		listnum+=len(each[1])
	return listnum
#载入NTUSD情感词典中褒义词词表
def loadPosDic():
	path=sys.path[0]
	if os.path.isdir(path):
		filename=path
	elif os.path.isfile(path):
		filename=os.path.dirname(path)
	filename=filename + '/NTUSD_positive_simplified.txt'
	# print(filename)
	# fpos=open(filename,'r+')
	fpos=codecs.open(filename,'r','utf-8')
	ltemppos=fpos.readlines()
	for i in range(len(ltemppos)):
		ltemppos[i]=ltemppos[i].strip()
	# print(len(ltemppos))
	fpos.close()
	return ltemppos
#载入NTUSD情感词典中贬义词词表
def loadNegDic():
	path=sys.path[0]
	if os.path.isdir(path):
		filename=path
	elif os.path.isfile(path):
		filename=os.path.dirname(path)
	filename=filename + '/NTUSD_negative_simplified.txt'
	# print(filename)
	# fneg=open(filename,'r+')
	fneg=codecs.open(filename,'r','utf-8')
	ltempneg=fneg.readlines()
	for i in range(len(ltempneg)):
		ltempneg[i]=ltempneg[i].strip()
	# print(len(ltempneg))
	fneg.close()
	return ltempneg
#txt文本中记录临时SO-PMI和SO-SIM结果
def writePMISIMtoLogTxt(listlog):
	path=sys.path[0]
	if os.path.isdir(path):
		filename=path
	elif os.path.isfile(path):
		filename=os.path.dirname(path)
	filename=filename + '/PMISIMlog.txt'
	flog=open(filename,'a')
	flog.write(addTabForList(listlog)+'\r\n')
	flog.close()

if __name__=='__main__':
	numfile=100#文本个数
	totalList=[]
	txtf=[]
	liststopword=loadStopwords(XMLprase.cur_file_dirTwo() + '/stopwords.txt')#载入停用词词表
	docID=0
	wordID=0
	totalResult=[]
	dicWordClass={}
	
	vecWords=[]
	vecInput=[]
	vecOut=[]
	
	resultFile=''
	pynlpir.open()
	path=sys.path[0]
	if os.path.isdir(path):
		filename=path
	elif os.path.isfile(path):
		filename=os.path.dirname(path)
	resultFile=filename + '/result.txt'
	svmtrainfile=filename + '/SVMTrainData.txt'
	svmResultFile=filename + '/SVMResult.txt'
	print('#####################################')
	print('读取训练集...............')
	print('#####################################')
	for i in range(numfile):
		path=sys.path[0]
		if os.path.isdir(path):
			filename=path
		elif os.path.isfile(path):
			filename=os.path.dirname(path)
		filename=filename + '/' + str(i+1) + '.xml'
		if os.path.exists(filename):
			txtT=XMLprase.getText(filename)#从xml文件中获取评论文本
			txtf.append([i+1,txtT])#以文档编号保存评论文本
			result=pynlpir.segment(txtT)#使用ICTCLAS分词系统分词
			result=removeStopwords(result,liststopword)#移除停用词
			basePosDic=[]
			baseNegDic=[]
			#.................................................................
			#从文本中提取人工标记的情感词添加到情感词典中
			for eachp in XMLprase.getPositiveWords(filename):
				if (eachp not in basePosDic):
					basePosDic.append(eachp)
			for eachn in XMLprase.getNegativeWords(filename):
				if (eachn not in baseNegDic):
					baseNegDic.append(eachn)
			#..................................................................
			#构建词的特征向量和结果向量，词特征向量为[词左边词性，词性，词右边词性，词的tf-idf]，结果向量为[pos=1/neg=-1/na=0]
			for id in range(len(result)):
				vecTemp=[]
				vecWords.append([result[id][0],i+1])
				if id==0:
					vecTemp.append(0)
					if result[id][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id][1]])
					if result[id+1][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id+1][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id+1][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id+1][1]])
				elif id==(len(result)-1):
					if result[id-1][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id-1][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id-1][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id-1][1]])
					if result[id][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id][1]])
					vecTemp.append(0)
				else:
					if result[id-1][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id-1][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id-1][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id-1][1]])
					if result[id][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id][1]])
					if result[id+1][1] in dicWordClass.keys():
						vecTemp.append(dicWordClass[result[id+1][1]])
					else:
						lendicT=len(dicWordClass)
						dicWordClass[result[id+1][1]]=lendicT + 1
						vecTemp.append(dicWordClass[result[id+1][1]])
				vecInput.append(vecTemp)
				if result[id][0] in basePosDic:
					vecOut.append(1)
				elif result[id][0] in baseNegDic:
					vecOut.append(-1)
				else:
					vecOut.append(0)
			totalList.append([i+1,result])
	pynlpir.close()
	#..............................................................................
	# print(vecWords)
	# print(len(vecWords))
	#................................................................................
	#添加tf-idf特征值到input向量中
	for j in range(len(vecWords)):
		vecInput[j].append(tfidf(totalList,vecWords[j]))
	#..................................................................................
	#生成libsvm训练使用的文本文件
	print('#####################################')
	print('生成libsvm训练文档..................')
	print('#####################################')
	svmfile=open(svmtrainfile,'w')
	for k in range(len(vecOut)):
		svmfile.write(str(vecOut[k])+' 1:'+str(vecInput[k][0])+' 2:'+str(vecInput[k][1])+' 3:'+str(vecInput[k][2])+' 4:'+str(vecInput[k][3])+'\r')
	svmfile.close()
	#..................................................................................
	y,x=svmutil.svm_read_problem(svmtrainfile)
	print('#####################################')
	print('svm训练中..................')
	print('#####################################')
	# print(x)
	# print('#####################################')
	# print(y)
	m=svmutil.svm_train(y,x)
	print('#####################################')
	print('svm测试中..................')
	print('#####################################')
	fsvmR=open(svmResultFile,'w')
	for each in svmutil.svm_predict(y,x,m):
		fsvmR.writelines(str(each))
	fsvmR.close()
	# print(m)
	#输出结果
	# fresult=open(resultFile, 'a')
	# fresult.write(strTitle())
	# for i in range(numfile):
		# fresult.write(strResult(resutlID,resutlWordString,resultWordPolarity,resultDocID,resultContext,resultConfidenceScore,student_num='1150332032'))#输出结果到结果文档中
	# fresult.close()
	# print(totalResult)