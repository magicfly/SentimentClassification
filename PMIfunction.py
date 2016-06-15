import math
import sys
#计算PMI值的类
class PMIClass():
	def __init__(self, list):
		self.totalnumber=self.getTotalNumber(list)
		self.allwords=list
	#计算PMI值
	def pmi(self, word1, word2, nearness):
		hitsNearword = self.getNumberAround(self.allwords, word1, word2, nearness)
		if hitsNearword==0:
			return 0
		word1Hits = self.getNumberHits(self.allwords, word1)
		if word1Hits==0:
			return 0
		word2Hits = self.getNumberHits(self.allwords, word2)
		if word2Hits==0:
			return 0
		result = math.log((hitsNearword*self.totalnumber)/(word1Hits*word2Hits), 2)
		return result
	#计算so-pmi值
	def sopmi(self, word, plist, nlist, nearness):
		sop = 0
		son = 0
		for pword in plist:
			sop += self.pmi(pword, word, nearness)
		for nword in nlist:
			son += self.pmi(nword, word, nearness)
		return (sop/len(plist)-son/len(nlist))
	#获取单词出现数目
	def getNumberHits(self, wordslist, word):
		countn=0
		for eachword in wordslist:
			if len(eachword)>1:
				for eacheachword in eachword[1]:
					if eacheachword==word:
						countn+=1
			else:
				if eachword==word:
					countn+=1
		return countn
	#获取单词在总数目
	def getTotalNumber(self, wordslist):
		countn=0
		for eachword in wordslist:
			if len(eachword)>1:
				for eacheachword in eachword[1]:
					countn+=1
			else:
				countn+=1
		return countn
	#计算置信度，定义：词与基础情感词中褒义词共现的次数减去与贬义词共现的次数的绝对值除以该词出现次数
	def confidence(self, wordlist, word, plist, nlist, nearness):
		pcount=0
		ncount=0
		for i in range(len(wordlist)):
			if len(wordlist[i])>1:
				for j in range(len(wordlist[i][1])):
					if wordlist[i][1][j]==word:
						for k in range(1,nearness+1):
							if (j-k)>=0:
								if wordlist[i][1][j-k] in plist:
									pcount+=1
								if wordlist[i][1][j-k] in nlist:
									ncount+=1
							if (j+k)<len(wordlist[i][1]):
								if wordlist[i][1][j+k] in plist:
									pcount+=1
								if wordlist[i][1][j+k] in nlist:
									ncount+=1
			else:
				if wordlist[i]==word:
					for j in range(1,nearness+1):
						if (i-j)>=0:
							if wordlist[i-j] in plist:
								pcount+=1
							if wordlist[i-j] in nlist:
								ncount+=1
						if (i+j)<len(wordlist):
							if wordlist[i+j] in plist:
								pcount+=1
							if wordlist[i+j] in nlist:
								ncount+=1
		return ((math.fabs(pcount-ncount)/(2*nearness))/self.getNumberHits(self.allwords, word))
	#获取单词2出现在单词1附近的数目	
	def getNumberAround(self, wordlist, word1, word2, nearness):
		countn=0
		for i in range(len(wordlist)):
			if len(wordlist[i])>1:
				for j in range(len(wordlist[i][1])):
					if wordlist[i][1][j]==word1:
						for k in range(1,nearness+1):
							if (j-k)>=0:
								if wordlist[i][1][j-k]==word2:
									countn+=1
									break
							if (j+k)<len(wordlist[i][1]):
								if wordlist[i][1][j+k]==word2:
									countn+=1
									break
			else:
				if wordlist[i]==word1:
					for j in range(1,nearness+1):
						if (i-j)>=0:
							if wordlist[i-j]==word2:
								countn+=1
								break
						if (i+j)<len(wordlist):
							if wordlist[i+j]==word2:
								countn+=1
								break
		return countn