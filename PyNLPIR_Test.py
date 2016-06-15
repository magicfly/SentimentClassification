#!/usr/bin/env python
import pynlpir
import math
import string
##Importing PyNLPIR
import codecs
import urllib  
import sys,os
import XMLprase
import PMIfunction
import SIMfunction
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
			listremove.append(each[0])
		else:
			ueach=each[0]+u'\r\n'
			if ueach in stopwords_list:
				listremove.append(each[0])
			elif check(each[0]) or checkletters(each[0]):
				listremove.append(each[0])
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
	posDic=loadPosDic()
	negDic=loadNegDic()
	liststopword=loadStopwords(XMLprase.cur_file_dirTwo() + '/stopwords.txt')#载入停用词词表
	basePosDic=[]
	basePosDicTemp=[]
	basePosDicTempOne=[]
	basePosDicTempTwo=[]
	baseNegDic=[]
	baseNegDicTemp=[]
	baseNegDicTempOne=[]
	baseNegDicTempTwo=[]
	docID=0
	wordID=0
	totalResult=[]
	resultFile=''
	pynlpir.open()
	
	for i in range(numfile):
		path=sys.path[0]
		if os.path.isdir(path):
			filename=path
		elif os.path.isfile(path):
			filename=os.path.dirname(path)
		resultFile=filename + '/result.txt'
		filename=filename + '/' + str(i+1) + '.xml'
		if os.path.exists(filename):
			txtT=XMLprase.getText(filename)#从xml文件中获取评论文本
			txtf.append([i+1,txtT])#以文档编号保存评论文本
			result=pynlpir.segment(txtT,pos_tagging=False)#使用ICTCLAS分词系统分词
			result=removeStopwordsNoTag(result,liststopword)#移除停用词
			# print(result)
			#.....................................................................
			#文本词与NTUSD情感词典取交集添加到临时基础情感词典1中
			for eachword in result:
				if (eachword in posDic) and (eachword not in basePosDicTempOne):
					basePosDicTempOne.append(eachword)
				elif (eachword in negDic) and (eachword not in baseNegDicTempOne):
					baseNegDicTempOne.append(eachword)
				else:
					pass
			#.................................................................
			#从文本中提取人工标记的情感词添加到基础情感词典2中
			for eachp in XMLprase.getPositiveWords(filename):
				if (eachp not in basePosDicTempTwo):
					basePosDicTempTwo.append(eachp)
			for eachn in XMLprase.getNegativeWords(filename):
				if (eachn not in baseNegDicTempTwo):
					baseNegDicTempTwo.append(eachn)
			#..................................................................
			totalList.append([i+1,result])#以文档编号保存分词结果
	pynlpir.close()
	#..............................................................................
	#添加网络收集的基础情感词到基础情感词典2中
	listPosDicFromWeb=['好','安全','不错','喜欢','加速','舒适','豪华','满意','爱','解决','风格','优势','保证','全新','实在','舒服','稳定','方便','品质','提升','乐趣','省油','先进','成功','漂亮','最好','保护','好车','值得','良好','满足','享受','出色','提高','适合','平稳','轻松','优点','完美','实用']
	listNegDicFromWeb=['碰撞','噪音','事故','毛病','不好','严重','下降','缺点','不够','死','不足','故障','缺陷','郁闷','撞击','断裂','失望','担心','倒','车祸','遗憾','怀疑','不行','变形','断','危险','震动','损失','噪声','麻烦','冲击','隐患','后悔','恐怕','粗糙','颠簸','造成','难看','不爽','伤害']
	for eachpfw in listPosDicFromWeb:
		if eachpfw not in basePosDicTempTwo:
			basePosDicTempTwo.append(eachpfw)
	for eachnfw in listNegDicFromWeb:
		if eachnfw not in baseNegDicTempTwo:
			baseNegDicTempTwo.append(eachnfw)
	#...............................................................................
	#情感词典1和情感词典2中情感词取交集为新的基础情感词典
	for eachpone in basePosDicTempOne:
		if eachpone in basePosDicTempTwo:
			basePosDicTemp.append(eachpone)
	for eachnone in baseNegDicTempOne:
		if eachnone in baseNegDicTempTwo:
			baseNegDicTemp.append(eachnone)
	#...............................................................................
	dicP={}
	dicN={}
	cPMI=PMIfunction.PMIClass(totalList)#初始化PMI模块类
	cSIM=SIMfunction.SIMClass()#初始化SIM模块类
	#..................................................................................
	#计算基础情感词典中词在文本中出现的频率
	for eachpt in basePosDicTemp:
		dicP[eachpt]=cPMI.getNumberHits(totalList,eachpt)/cPMI.totalnumber
	for eachpn in baseNegDicTemp:
		dicN[eachpn]=cPMI.getNumberHits(totalList,eachpn)/cPMI.totalnumber
	#............................................................................
	#根据基础情感词典的词频率降序排序
	basePosDicTemp=sorted(dicP.items(), key=lambda asd:asd[1], reverse=True)
	baseNegDicTemp=sorted(dicN.items(), key=lambda asd:asd[1], reverse=True)
	#............................................................................
	#提取出现频率不为0且排序在前100%的词构成基础情感词典
	for i in range(int(1.0*len(basePosDicTemp))):
		if basePosDicTemp[i][1]>0:
			basePosDic.append(basePosDicTemp[i][0])
	for i in range(int(1.0*len(baseNegDicTemp))):
		if baseNegDicTemp[i][1]>0:
			baseNegDic.append(baseNegDicTemp[i][0])
	#............................................................................
	print('基础情感词典')
	print(basePosDic)
	print(baseNegDic)
	#计算各个单词的so-pmi和so-sim
	print('######################################################')
	print('计算开始，请耐心等待...............')
	print('######################################################')
	for i in range(len(totalList)):	
		docID=totalList[i][0]
		for j in range(len(totalList[i][1])):#迭代获取分词后的每个词
			listT=[]
			listT.append(docID)#记录文档编号 index =0 
			wordID=j+1
			listT.append(wordID)#记录单词编号 index = 1
			listT.append(totalList[i][1][j])#记录单词 index = 2 
			listT.append(cPMI.sopmi(totalList[i][1][j],basePosDic,baseNegDic,1))#计算词与基础情感词典的SO-PMI值 index = 3 
			listT.append(cPMI.confidence(totalList,totalList[i][1][j],basePosDic,baseNegDic,1))#计算so-pmi置信度 index = 4 
			temp=cSIM.sosim(totalList[i][1][j],basePosDic,baseNegDic)#计算词与基础情感词典的SO-SIM值和置信度
			listT.append(temp[0])#SO-SIM值 index = 5  
			listT.append(temp[1])#so-sim置信度 index = 6 
			writePMISIMtoLogTxt(listT)#计算结果写入临时文本文档中
			totalResult.append(listT)
	#.................................................................................
	#根据各个单词构建结果字典，便于查询和排序
	dicResult={}
	for eachlist in totalResult:
		tempList=[]
		if eachlist[2] not in dicResult.keys():
			if (eachlist[3]>0.0 and eachlist[5]>0.0) or (eachlist[3]<0.0 and eachlist[5]<0.0):#两种方式都为pos 置信度相加
				confidenceT=math.fabs(eachlist[4])*0.2+math.fabs(eachlist[6])*0.8 #SO-SIM置信度权重为0.8 so-pmi置信度权重为0.2
			else:#两种方式结果不同置信度相减
				confidenceT=math.fabs(math.fabs(eachlist[4])*0.2-math.fabs(eachlist[6])*0.8)
			tempList.append(confidenceT)
			tempList.append(eachlist)
			dicResult[eachlist[2]]=tempList
		else:
			tempList=dicResult[eachlist[2]]
			tempList.append(eachlist)
			dicResult[eachlist[2]]=tempList
	#..................................................................................
	#对结果字典根据置信度降序排序
	dicFinal=sorted(dicResult.items(), key=lambda asd:asd[1], reverse=True)
	#..................................................................................
	#输出结果
	fresult=open(resultFile, 'a')
	fresult.write(strTitle())
	for i in range(numfile):
		resutlID=i#序号
		resutlWordString=dicFinal[i][0]#单词
		if dicFinal[i][1][1][5]>0:#优先判断so-sim so-sim>0为pos
			resultWordPolarity='pos'
		elif dicFinal[i][1][1][5]<0:#优先判断so-sim so-sim<0为pos
			resultWordPolarity='neg'
		else:
			if dicFinal[i][1][1][4]>0:#后判断so-pmi so-pmi>0为pos
				resultWordPolarity='pos'
			elif dicFinal[i][1][1][4]<0:#后判断so-pmi so-pmi<0为pos
				resultWordPolarity='neg'
			else:
				resultWordPolarity='na'#两个都为0为中性
		resultDocID=dicFinal[i][1][1][0]#获取单词出现的首个文档编号
		for each in txtf:#在结果list中找到文档编号为当前编号的文档并取出该次的左右各5个词范围内的句子
			if each[0]==resultDocID:
				indexNum=each[1].find(resutlWordString)
				if indexNum<10:
					resultContext=each[1][0:indexNum+11]
				elif indexNum>(len(each[1])-10) or (indexNum+len(resutlWordString)-1+11)>(len(each[1])):
					resultContext=each[1][indexNum-10:len(each[1])]
				else:
					resultContext=each[1][indexNum-10:indexNum+len(resutlWordString)-1+11]
		resultConfidenceScore=dicFinal[i][1][0]#获得置信度值
		fresult.write(strResult(resutlID,resutlWordString,resultWordPolarity,resultDocID,resultContext,resultConfidenceScore,student_num='1150332032'))#输出结果到结果文档中
	fresult.close()
	# print(totalResult)