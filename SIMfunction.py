import math
import sys,os
#计算基于同义词词林的词语相似度
class SIMClass():
#初始化类
	def __init__(self):
		dirNow=self.cur_file_dir()
		dirCode=dirNow+'/tongyiciCode.txt'
		dirWordDic=dirNow+'/tongyiciCiLin.txt'
		self.code=self.loadWordCode(dirCode)
		self.worddic=self.loadWordDic(dirWordDic)
#获得当前目录	
	def cur_file_dir(self):
		path = sys.path[0]
		if os.path.isdir(path):
			return path
		elif os.path.isfile(path):
			return os.path.dirname(path)
#载入所有编码
	def loadWordCode(self, dir):
		fcode=open(dir,'r')
		listR=[]
		listRead=fcode.readlines()
		for strT in listRead:
			strT=strT.strip()
			listR.append(strT)
		fcode.close()
		return listR
#载入所有词及其编码
	def loadWordDic(self, dir):
		dicR={}
		fworddic=open(dir,'r')
		listRead=fworddic.readlines()
		# print(listRead)
		for strT in listRead:
			strT=strT.strip()
			listT=strT.split(' ')
			# print(listT)
			word=listT[0]
			count=int(listT[1])
			listcode=[]
			for i in range(count):
				listcode.append(listT[i+2])
			dicR[word]=listcode
			# print(word)
			# print(listcode)
		fworddic.close()
		return dicR
#计算词语word1和word2的相似度
	def CalcSimilarSenses(self, word1, word2):
		similar = 0.0
		max_temp = 0.0
		temp = 0.0
		if (word1 not in self.worddic) or (word2 not in self.worddic):
			return similar
		for i in range(len(self.worddic[word1])):
			for j in range(len(self.worddic[word2])):
				# print(self.worddic[word1][i])
				# print(self.worddic[word2][j])
				temp=self.CalcSimilar(self.worddic[word1][i],self.worddic[word2][j])
				if temp>max_temp:
					max_temp=temp
		similar=max_temp
		return max_temp
#判断词的结尾字符
	def endsWith(self, word, charw):
		# print(word[len(word)-1:len(word)])
		# print(charw)
		if (word[len(word)-1:len(word)]==charw):
			return True
		else:
			return False
#获得两个编码的相同的前导部分
	def getCommonStr(self, code1, code2):
		strT=''
		for i in range(len(code1)):
			if (code1[i:i+1]==code2[i:i+1]):
				strT+=code1[i:i+1]
			else:
				break
		strTlen=len(strT)
		if (strTlen==3) or (strTlen==6):
			strT=strT[0:strTlen-1]
		return strT
#获得编码分支距离
	def getK(self, code1, code2):
		str1=code1[0:1]
		str2=code2[0:1]
		if (str1==str2):
			str1=code1[1:2]
			str2=code2[1:2]
		else:
			return math.fabs(ord(str1)-ord(str2))
		if (str1==str2):
			str1=code1[2:4]
			str2=code2[2:4]
		else:
			return math.fabs(ord(str1)-ord(str2))
		if (str1==str2):
			str1=code1[4:5]
			str2=code2[4:5]
		else:
			return math.fabs(int(str1)-int(str2))
		if (str1==str2):
			str1=code1[5:7]
			str2=code2[5:7]
		else:
			return math.fabs(ord(str1)-ord(str2))
		# print(int(str1))
		# print(int(str2))
		return math.fabs(int(str1)-int(str2))
#获得相同前导部分的编码所在分支层的分支个数
	def getN(self,comstr):
		lenstr=len(comstr)
		if (lenstr==1):
			return self.getCount(comstr,2)
		elif (lenstr==2):
			return self.getCount(comstr,4)
		elif (lenstr==4):
			return self.getCount(comstr,5)
		elif (lenstr==5):
			return self.getCount(comstr,7)
		else:
			return 0
	
	def getCount(self, comstr, end):
		listCode=[]
		for each in self.code:
			if (each[0:len(comstr)]==comstr):
				strTemp=each[0:end]
				if (strTemp in listCode):
					continue
				else:
					listCode.append(strTemp)
		return len(listCode)
#计算词语word1和word2的相似度
	def CalcSimilar(self,code1,code2):
		a = 0.65
		b = 0.8
		c = 0.9
		d = 0.96
		e = 0.5
		f = 0.1
		degrees = 180
		similar = 0.0
		n = 1
		k = 0
		strCommom=self.getCommonStr(code1,code2)
		# print(strCommom)
		length=len(strCommom)
		# print(length)
		k=self.getK(code1,code2)
		# print(k)
		n=self.getN(strCommom)
		# print(n)
		if (self.endsWith(code1,'@') or self.endsWith(code2,'@') or (length==0)):
			similar=f
			return similar
		if (length==1):
			similar=a*math.cos(n*math.pi/degrees)*((n-k+1)/n)
		elif (length==2):
			similar=b*math.cos(n*math.pi/degrees)*((n-k+1)/n)
		elif (length==4):
			similar=c*math.cos(n*math.pi/degrees)*((n-k+1)/n)
		elif (length==5):
			similar=d*math.cos(n*math.pi/degrees)*((n-k+1)/n)
		else:
			if (self.endsWith(code1,'=') and self.endsWith(code2,'=')):
				similar=1.0
			elif (self.endsWith(code1,'#') and self.endsWith(code2,'#')):
				similar=e
		return similar
#计算so-sim和置信度，定义：(褒义情感词相似度最大值-贬义情感词相似度的最大值).绝对值
	def sosim(self, word, plist, nlist):
		rlist=[]
		pcount=0
		maxp=0
		minp=1.0
		maxn=0
		minn=1.0
		ncount=0
		sop = 0
		son = 0
		for pword in plist:
			temp=self.CalcSimilarSenses(word, pword)
			if temp>maxp:
				maxp=temp
			if temp<minp:
				minp=temp
			if temp>0.5:
				pcount+=1
			sop += temp
		for nword in nlist:
			temp=self.CalcSimilarSenses(word, nword)
			if temp>maxn:
				maxn=temp
			if temp<minn:
				minn=temp
			if temp>0.5:
				ncount+=1
			son += temp
		rlist.append(sop/len(plist)-son/len(nlist))
		rlist.append(math.fabs(maxp-maxn))#估算置信度
		return rlist
		
if __name__=='__main__':
	# Csim=SIMClass()
	# print(Csim.code)
	# print(Csim.CalcSimilarSenses('人民', '国民'))
	# print(Csim.CalcSimilarSenses('人民', '群众'))
	# print(Csim.CalcSimilarSenses('人民', '党群'))
	# print(Csim.CalcSimilarSenses('人民', '良民'))
	# print(Csim.CalcSimilarSenses('人民', '同志'))
	# print(Csim.CalcSimilarSenses('人民', '成年人'))
	# print(Csim.CalcSimilarSenses('人民', '市民'))
	# print(Csim.CalcSimilarSenses('人民', '亲属'))
	# print(Csim.CalcSimilarSenses('人民', '志愿者'))
	# print(Csim.CalcSimilarSenses('人民', '先锋'))
	pass

# 人民--国民:1.0
# 人民--群众:0.9576614882494312
# 人民--党群:0.8978076452338418
# 人民--良民:0.7182461161870735
# 人民--同志:0.6630145969121822
# 人民--成年人:0.6306922220793977
# 人民--市民:0.5405933332109123
# 人民--亲属:0.36039555547394153
# 人民--志愿者:0.22524722217121346
# 人民--先锋:0.18019777773697077

# 1.0
# 0.9576614882494312
# 0.8978076452338418
# 0.7182461161870735
# 0.6630145969121822
# 0.6306922220793977
# 0.5405933332109123
# 0.36039555547394153
# 0.22524722217121346
# 0.18019777773697077
# Press any key to continue . . .