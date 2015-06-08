#prepareTraindata.py
#reads all annotated data en creates traindata for Stanford NER tagger
import os
import nltk
from collections import defaultdict

class Trainer():

	def __init__(self):
		lastid = ''
		for line in open('data/testdata.txt'):
			elements = line.strip().split()
			if lastid != elements[0]:
				print()

			if not len(elements) < 4:
			
				if len(elements) > 6:
					if elements[6] == '-':
						print("{} \t {}".format(elements[4], "O" ))
					else:
						print("{} \t {}".format(elements[4], elements[6] ))
				else:
					print("{} \t {}".format(elements[4], "O" ))
				lastid = elements[0]
			

				

trainer = Trainer()