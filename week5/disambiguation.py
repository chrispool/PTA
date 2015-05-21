#disambiguation.py
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import os
from nltk.wsd import lesk


class Disambiguation():

	def __init__(self):
		#self.getData() Maar 1x nodig
		self.lemmatizer = WordNetLemmatizer()
		self.findNouns()

	def getData(self):
		
		links = []
		rootdir = 'data/annotation'
		for subdir, dirs, files in os.walk(rootdir):
			for filename in files:
				if filename == "en.tok.off.pos.ent":
					with open(os.path.join(subdir, filename)) as f:		
						lines = f.read().splitlines()
						for line in lines:
								elements = line.split()
								if len(elements) > 6:
									links.append(elements[6])
									print(elements[6], os.path.join(subdir, filename))
						
		for url in set(links):
			title = url.split("/")[-1]
			getPage = 'curl ' + url + '| grep "<p>" | sed \'s/<[^<]*>//g\' > data/wiki/' + title + '.txt' 
			os.system(getPage)
		print("Wiki files generated")

	def findNouns(self):
		for fn in os.listdir('data/wiki'):	
			f = open("data/wiki/" + fn, 'rb')
			content = f.read()
			content = str(content).replace("\\n", "")
			tokens = word_tokenize(content)
			
			posTag = pos_tag(tokens)
			#for word, tag in posTag:
				#print("{:>10} - {}".format(word,tag))
			text = []
			rawText = []
			for word,tag in posTag:
				if tag == 'NN' or tag == 'NNP':
					text.append((word, 'yes'))
				else:
					text.append((word, 'no'))
				rawText.append(word)
			
			
			for i, tag in enumerate(text):
				
				if tag[1] == 'yes':
					lemma = self.lemmatizer.lemmatize(tag[0], wordnet.NOUN)
					synsets = wordnet.synsets(self.lemmatizer.lemmatize(tag[0], wordnet.NOUN), pos="n")
					if len(synsets) > 1:
						sent = rawText[i-10:i+10]
							
						pos = "n"
						print()
						print("Results for {}".format(lemma))
						print(lemma, " ".join(rawText[i-20:i+100]))
						print(lesk(sent, lemma, pos))
						print("All possible senses:")
						for ss in wordnet.synsets(lemma, pos):
							print(ss, ss.definition())
						print()
						'''
						print()
						print(lemma)
						for synset in synsets:
							print(synset, synset.definition())
						print()
						'''


	def getSynset(self,word):		
		for ss in wordnet.synsets(word, "n"):
			print(ss, ss.definition())



D = Disambiguation()