#prepareTraindata.py

import os
import nltk
from nltk.metrics import ConfusionMatrix, precision, recall, f_measure
from collections import defaultdict

class Trainer():

	def __init__(self):
		rootdir = 'data'
		for subdir, dirs, files in os.walk(rootdir):
			for filename in files:
				
				if filename[-3:] == "ent":
					with open(os.path.join(subdir, filename)) as f:
						lines = f.read().splitlines()
						for line in lines:
							elements = line.split()
							if len(elements) > 5:
								print("{} \t {}".format(elements[3], elements[5] ))
							else:
								print("{} \t {}".format(elements[3], "O" ))
					print()


				

trainer = Trainer()