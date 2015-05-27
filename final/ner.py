from nltk.tag.stanford import NERTagger 
from collections import defaultdict
import os
import nltk


class Ner():
	def __init__(self):
		classifier = "ner/classifiers/" + "wikification.ser.gz"
		jar = "ner/stanford-ner-3.4.jar"
		self.tagger = NERTagger(classifier, jar)

		
		rootdir = 'data'
		for subdir, dirs, files in os.walk(rootdir):
			for filename in files:
				
				if filename[-3:] == "raw":
					print()
					print()	

					with open(os.path.join(subdir, filename)) as f:
						lines = f.read().strip()
						tokens = nltk.word_tokenize(lines)
						for l in self.tagger.tag(tokens):
							for word, tag in l:
								if tag == "O":
									print("{} ".format(word), end="")
								else:
									print("{} ({}) ".format(word, tag), end="")

n = Ner()