# p2_excercise1.py
# Leonardo Losno Velozo & Chris Pool
import nltk
from nltk.corpus import brown
from nltk.tag import UnigramTagger
import numpy

class OpdrachtTwee:
	
	def __init__(self):
		self.br_tw = brown.tagged_words(categories='mystery')
		self.br_ts = brown.tagged_sents(categories='mystery')
		
	def outputPrinten(self):
		print("1a Tagged version (Penn Treebank POS tagset): {}".format(self.manualTagPenn()))
		print("1b Tagged version (Brown): {}".format(self.manualTagPenn()))
		print("1c Tagged version (NLTK): {}".format(self.manualTagNltk()))
		print("2a - There are {} words and {} sentences".format(len(self.br_tw), len(self.br_ts)) )
		print("2b - Word 100 is: {} and word 101: {}".format(self.br_tw[100], self.br_tw[101]) )
		print("2c - There are {} different tags".format(self.nTags()))
		print("2d - 10 most frequent words are {}".format(self.freqWords()))
		print("2e - 10 most frequent tags are {}".format(self.freqTags()))
		print("2f - the most frequent adverb is: {}".format(self.freqTag('RB')))
		print("2g - the most frequent adjective is: {}".format(self.freqTag('JJ')))
		print("2h, i - find tags and counts for 'so' {}".format(self.wordTags('so')))
		print("2j - 3 example sentences for 'so': \n - {}".format("\n - ".join(self.sentenceTags('so'))))
		print("2k - POS preceeding 'so' {}, and following {} ".format(self.preceedingTag('so'),self.followingTag('so')))
	
	def manualTagPenn(self):
		sentence = 'Marley was dead : to begin with . There is no doubt whatever about that .'
		tokens = nltk.word_tokenize(sentence)	
		taggedText = nltk.pos_tag(tokens)
		return list(taggedText)

	def manualTagBrown(self):
		sentence = 'Marley was dead : to begin with . There is no doubt whatever about that .'
		tokens = nltk.word_tokenize(sentence)
		tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents(categories='news')[:500])
		return tagger.tag(tokens)
		
	def manualTagNltk(self):
		sentence = 'Marley was dead : to begin with . There is no doubt whatever about that .'
		tokens = nltk.word_tokenize(sentence)
		taggedText = [(word, nltk.map_tag('brown', 'universal', tag) ) for word, tag in self.manualTagBrown()]
		return list(taggedText)

	def nTags(self):
		tags = set([tag for word, tag in self.br_tw])
		return len(tags)

	def freqWords(self):
		words = [word for word,tag in self.br_tw]
		fdist = nltk.FreqDist(words)
		return fdist.most_common(10)

	def freqTags(self):
		tags = [tag for word,tag in self.br_tw]
		fdist = nltk.FreqDist(tags)
		return fdist.most_common(10)

	def freqTag(self, t):
		#get frequency of specific tag
		words = [word for word,tag in self.br_tw if tag == t]
		fdist = nltk.FreqDist(words)
		return fdist.most_common(1)

	def wordTags(self, w):
		tags = [tag for word,tag in self.br_tw if word == w]
		fdist = nltk.FreqDist(tags)
		return fdist.most_common()

	def sentenceTags(self, w):
		usedTags = []
		result = []		
		for sentence in self.br_ts:
			for word, tag in sentence:
				if word == w and tag not in usedTags:
					sentenceStr = " ".join([w for w, t in sentence]) + "(" + tag + ")"
					result.append(sentenceStr)
					usedTags.append(tag)
		return result

	def preceedingTag(self, w):
		tags = []
		for i,wordTag in enumerate(self.br_tw):
			if wordTag[0] == w:
				tags.append( self.br_tw[(i-1)][1] )
		fdist = nltk.FreqDist(tags)
		return fdist.most_common(5)		

	def followingTag(self, w):
		tags = []
		for i,wordTag in enumerate(self.br_tw):
			if wordTag[0] == w:
				tags.append( self.br_tw[(i+1)][1] )
		fdist = nltk.FreqDist(tags)
		return fdist.most_common(5)	
	
	def posTags(self,txtFile):
		text = open(txtFile).read()[:1000] #otherwise it takes to long
		tokens = nltk.word_tokenize(text)
		taggedText = nltk.pos_tag(tokens)
		print("3 - Tagged version of Holmes.txt \n {}".format(taggedText))

opdracht = OpdrachtTwee()
opdracht.outputPrinten()
opdracht.posTags('holmes.txt')
