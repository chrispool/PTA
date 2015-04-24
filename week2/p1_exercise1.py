# p1_excercise1.py
# Leonardo Losno Velozo

import nltk
from nltk.collocations import *

class OpdEen:
	
	def __init__(self, txtFile):
		self.text = open(txtFile).read()

	# Vraag 1:	
	def characterTypes(self):
		 fdist = nltk.FreqDist(self.text)
		 
		 forbiddenCh = ['\n', '\r', '\xa0', '\xa2', '\xa8', '\xa9', '\xc3']
		 characters = [c for c in sorted(fdist.keys()) if c not in forbiddenCh]
		 
		 print('Antwoord 1A:')
		 print(fdist)
		 for c in characters:
			 print(c,fdist[c])
			 
	def wordTypes(self):
		tokens = nltk.wordpunct_tokenize(self.text)
		fdist = nltk.FreqDist(tokens)
		
		forbiddenWord = ['\xa2','\xa8','\xa9','\xa9,','\xa9--']
		wordList = [w for w in sorted(fdist.keys()) if w not in forbiddenWord]
		 
		print('Antwoord 1B:')
		print(fdist)
		for w in wordList[:100]:
			print(w,fdist[w])
	
	def uniGramCh(self):
		fdist = nltk.FreqDist(self.text)
		
		print(fdist.most_common(20))
		
	def bigramCh(self):
		bigrams = nltk.bigrams(self.text)
		fdist = nltk.FreqDist(bigrams)
		
		print(fdist.most_common(20))
		
	def trigramCh(self):
		
		trigrams = nltk.trigrams(self.text)
		fdist = nltk.FreqDist(trigrams)
		
		print(fdist.most_common(20))
	
	def uniGram(self):
		tokens = nltk.wordpunct_tokenize(self.text)
		fdist = nltk.FreqDist(tokens)
		
		print(fdist.most_common(20))
		
	def bigram(self):
		tokens = nltk.wordpunct_tokenize(self.text)
		bigrams = nltk.bigrams(tokens)
		fdist = nltk.FreqDist(bigrams)
		
		print(fdist.most_common(20))
		
	def trigram(self):
		tokens = nltk.wordpunct_tokenize(self.text)
		trigrams = nltk.trigrams(tokens)
		fdist = nltk.FreqDist(trigrams)
		
		print(fdist.most_common(20))
		
	# Vraag 2:	
	def collocationsPMI(self):
		tokens = nltk.wordpunct_tokenize(self.text)
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		finder = BigramCollocationFinder.from_words(tokens)
		finder.apply_freq_filter(3)
		result = finder.nbest(bigram_measures.pmi, 20)
		print(result)
		
	def collocationsChi(self):
		tokens = nltk.wordpunct_tokenize(self.text)
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		finder = BigramCollocationFinder.from_words(tokens)
		finder.apply_freq_filter(3)
		result = finder.nbest(bigram_measures.chi_sq, 20)
		print(result)
		
	
		 
		 

e = OpdEen('holmes.txt')
# e.characterTypes()
e.collocationsChi()
