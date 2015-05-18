from nltk.tag.stanford import NERTagger #Note that this does not import the implementation, just the wrapper!
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import os
import nltk
from nltk import word_tokenize
from collections import defaultdict, Counter
 
class Ner:

	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		
		'''
		#Create the argument paths accordingly. Note that you can also pass the entire string to NERTagger().
		classifiers = []
		classifiers.append("ner/classifiers/" + "english.all.3class.distsim.crf.ser.gz")
		classifiers.append("ner/classifiers/" + "english.conll.4class.distsim.crf.ser.gz")
		classifiers.append("ner/classifiers/" + "english.muc.7class.distsim.crf.ser.gz")
		classifiers.append("ner/classifiers/" + "english.nowiki.3class.distsim.crf.ser.gz")

		for classifier in classifiers:
			print(classifier)
			jar = "ner/stanford-ner-3.4.jar"
			self.tagger = NERTagger(classifier, jar)
			self.text = open('ada_lovelace.txt').read()
			self.tokens = self.text.split()
			self.tag()
			self.printOutput()
	
		'''
		classifier = "ner/classifiers/" + "english.all.3class.distsim.crf.ser.gz"
		jar = "ner/stanford-ner-3.4.jar"
		self.tagger = NERTagger(classifier, jar)
		self.text = open('ada_lovelace.txt').read()
		self.tokens = self.text.split()
		posTag = nltk.pos_tag(self.tokens)
		self.nouns = [word for word, tag in posTag if tag == 'NN']
		self.lemmatize()
		self.tag()
		self.isHyponymOf()
		self.printOutput()
		

	def printOutput(self):
		del self.words['O']
		for tag in self.words:
			
			if len(self.words[tag]) > 0:
				print("{}({}): {}".format(tag, len(self.words[tag]),' ,'.join(self.words[tag])))

	def lemmatize(self):
		self.lemma = defaultdict(list)
		for noun in self.nouns:		
			self.lemma[self.lemmatizer.lemmatize(noun, wordnet.NOUN)] = wordnet.synsets(self.lemmatizer.lemmatize(noun, wordnet.NOUN), pos="n")	
	

	def tag(self):
		self.words = defaultdict(list)
		for line in self.tagger.tag(self.tokens):
			for word, tag in line:
				self.words[tag].append(word)

		

	def isHyponymOf(self):
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
			#print("category: {} - {} ".format(key, ' ,'.join(set(self.top25[key]))))
			#w.extend(list(set(self.top25[key])))
			
			self.words[' ,'.join(key).upper()].extend((list(set(self.top25[key]))))

		

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

o = Ner()