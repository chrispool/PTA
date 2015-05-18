# Opdracht 1
# Leonardo Losno Velozo & Chris Pool


import nltk
from nltk.corpus import wordnet
from collections import Counter

class OpdrachtTwee:

	def __init__(self):
		wordPairs = [['car', 'automobile'],['coast','shore'],['food','fruit'],['journey','car'],['monk','slave'],['moon','string']]
		result = Counter()
		for word1, word2 in wordPairs:
			result[word1 + "<> "+word2] = self.words(word1, word2)

		for word,score in result.most_common():
			print("{} : {}".format(word, score))

	def getMaxSim(self,synsets1, synsets2):
		maxSim = None
		for s1 in synsets1:
			for s2 in synsets2:
				sim = s1.lch_similarity(s2)
				if maxSim == None or maxSim < sim:
					maxSim = sim
		return maxSim

	def words(self, word1, word2):
		word1SS = wordnet.synsets(word1, pos="n")
		word2SS = wordnet.synsets(word2, pos="n")
		return self.getMaxSim(word1SS,word2SS)
		

	
		
opdracht = OpdrachtTwee()