#disambiguation.py
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import os
from nltk.wsd import lesk
import re
from collections import Counter
class Disambiguation():

	def __init__(self):
		'''self.getData() #Maar 1x nodig'''
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
		counterWords = Counter()
		cTotal = []
		docs = 0
		cSynsets = 0
		nSynsets = 0
		for fn in os.listdir('data/wiki'):	
			c = 0
			docs += 1
			f = open("data/wiki/" + fn, 'rb')
			content = f.read()
			
			#clean up page (remove strange chars)
			content = str(content).replace("\\n", "")
			content = re.sub('[\[0-9*\]]', '', content)
			content = content.replace("\\'s", "'s");
			fromC = content[5:].find("'")
			content = content[fromC:]
			
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
						counterWords[len(synsets)] += 1
						nSynsets += 1
						cSynsets += len(synsets)
						c += 1
						sent = rawText[i-100:i+100]
						
						pos = "n"
						print()
						print("Results for {}".format(lemma))
						print(" ".join(rawText[i-20:i+20]))
						print(lesk(sent, lemma, pos))
						print("All possible senses:")
						for ss in wordnet.synsets(lemma, pos):
							print(ss, ss.definition())
						print()
						
			cTotal.append(c)
			print("file done")
		print("Total number of p words {}, portion per document {}, n of docs without p {} avg. synsets per synset {} ".format(sum(cTotal), sum(cTotal) / docs, cTotal.count(0), cSynsets/nSynsets  ))
		for w, n in counterWords.most_common():
			print(w, n)
	



D = Disambiguation()