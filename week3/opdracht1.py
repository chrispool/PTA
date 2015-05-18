# Opdracht 1
# Leonardo Losno Velozo & Chris Pool


from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from collections import defaultdict, Counter
import re

class OpdrachtEen:

	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		self.text = open('ada_lovelace.txt').read()
		self.tokens = word_tokenize(self.text)
		posTag = pos_tag(self.tokens)
		self.nouns = [word for word, tag in posTag if tag == 'NN']
		self.lemmatize()
		print("Opdracht 1.1 & 1.2 & 1.3")
		self.words() #opdracht 1.1
		print("Opdracht 2.1")
		self.isHyponymOf() #opdracht 1.2
		wordPairs = [['car', 'automobile'],['coast','shore'],['food','fruit'],['journey','car'],['monk','slave'],['moon','string']]
		result = Counter()
		for word1, word2 in wordPairs:
			result[word1 + "<> "+word2] = self.wordsSim(word1, word2)
		print("Opdracht 3")
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

	def wordsSim(self, word1, word2):
		word1SS = wordnet.synsets(word1, pos="n")
		word2SS = wordnet.synsets(word2, pos="n")
		return self.getMaxSim(word1SS,word2SS)

	def words(self):
		words = ['relative', 'illness', 'science']
		for w in words:
			wordSynsets = wordnet.synsets(w, wordnet.NOUN)
			score = 0
			lemmaWords = []
			for wordSynset in wordSynsets:
				
				for lemma in self.lemma:
					for synset in self.lemma[lemma]:
						if self.isHypernymOf(synset, wordSynset) == True:
							score += 1
							lemmaWords.append(lemma)

			print("Score for {} = {} ({})".format(w, score, " ,".join(lemmaWords)))

	def lemmatize(self):
		self.lemma = defaultdict(list)
		for noun in self.nouns:		
			self.lemma[self.lemmatizer.lemmatize(noun, wordnet.NOUN)] = wordnet.synsets(self.lemmatizer.lemmatize(noun, wordnet.NOUN), pos="n")	
	
	def isHyponymOf(self):
		'''
		categories = '{act,action,activity}{animal,fauna}{artifact}{attribute,property}{body,corpus} \
			{cognition,knowledge}{communication}{event,happening} \
			{feeling,emotion}{food}{group,collection}{location,place} \
			{motive}{natural object}{natural phenomenon}{person,human being} \
			{plant,flora}{possession}{process}{quantity,amount}{relation}{shape}{state,condition}\
			{substance}{time}'

		categories = re.findall(r"\{([A-Za-z0-9_,]+)\}", categories)
		'''
		categories = ['act,action,activity', 'animal,fauna', 'artifact', 'attribute,property', 'body,corpus', 'cognition,knowledge', 'communication', 'event,happening', 'feeling,emotion', 'food', 'group,collection', 'location,place', 'motive', 'plant,flora', 'possession', 'process', 'quantity,amount', 'relation', 'shape', 'state,condition', 'substance', 'time']
		self.top25 = defaultdict(list)
		for category in categories:
			key = category.split(',')
			self.top25[tuple(key)] = []

		for lemma in self.lemma:
			for synset in self.lemma[lemma]:
				#print()
				words = self.getTree(synset,lemma)
		
		w = []		
		for key in self.top25:
			print("category: {} - {} ".format(key, ' ,'.join(set(self.top25[key]))))
			w.extend(list(set(self.top25[key])))
		

		counterN = Counter(list(w))
		print("Opdracht 2.1 & 2.2")
		print(counterN) # opdracht 2.1 % 2.2
		print("Opdracht 2.3")
		print(len(self.lemma) / len(self.top25.values())) # 2.3

	def getTree(self, synset,noun):
		for hypernym in synset.hypernyms():
			for key in self.top25:
				if hypernym.name().split('.')[0] in key:
					self.top25[key].append(noun)
					break
			if hypernym.name() == 'entities':
				return words
			else:
				self.getTree(hypernym, noun)


	def isHypernymOf(self, synset1, synset2):
		if synset1 == synset2:
			return True
		for hypernym in synset1.hypernyms():

			if synset2 == hypernym:
				return True
			if self.isHypernymOf(hypernym, synset2):
				return True
		return False
		
opdracht = OpdrachtEen()