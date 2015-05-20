import os
import nltk
from nltk.metrics import ConfusionMatrix, precision, recall, f_measure
from collections import defaultdict
class Compare():

	def __init__(self):
		JUDGE1NAME = 'leonardo'
		JUDGE2NAME = 'chris'
		rootdir = 'data'
		self.judge1 = []
		self.judge2 = []
		for subdir, dirs, files in os.walk(rootdir):
			for filename in files:
				#Leonardo
				if filename.endswith(JUDGE1NAME):
					with open(os.path.join(subdir, filename)) as f:
						
						lines = f.read().splitlines()
						for line in lines:
								self.judge1.append(line.split())
				#chris
				if filename.endswith(JUDGE2NAME):
					with open(os.path.join(subdir, filename)) as f:
						
						lines = f.read().splitlines()
						for line in lines:
								self.judge2.append(line.split())
		
	

	def compareJudges(self):
		judge1 = []
		judge2 = []
		
		judge1Set = defaultdict(set)
		judge2Set = defaultdict(set)

		judge1SetD = defaultdict(set)
		judge2SetD = defaultdict(set)	

		for i, row in enumerate(self.judge1):
			if len(self.judge1[i]) > 5:
				judge1.append(self.judge1[i][5])
				judge1Set['yes'].add(i)
				judge1SetD[self.judge1[i][5]].add(i)
			else:
				judge1.append('NOT')
				judge1Set['no'].add(i)
				judge1SetD['NOT'].add(i)
			
			if len(self.judge2[i]) > 5:
				judge2.append(self.judge2[i][5])
				judge2Set['yes'].add(i)
				judge2SetD[self.judge2[i][5]].add(i)
			else:
				judge2.append('NOT')
				judge2Set['no'].add(i)
				judge2SetD['NOT'].add(i)


		print("Precision and recall for interesting entities")
		for key in judge1Set:
			print("For {: <10} P: {:.2f} R:{:.2f} F:{:.2f}".format(key, precision(judge1Set[key], judge2Set[key]),recall(judge1Set[key],judge2Set[key]),f_measure(judge1Set[key], judge2Set[key])))
		print()
		
		print("Precision and recall for categories")
		for key in judge1SetD:
			print("For {: <10} P: {:.2f} R:{:.2f} F:{:.2f}".format(key, precision(judge1SetD[key], judge2SetD[key]),recall(judge1SetD[key],judge2SetD[key]),f_measure(judge1SetD[key], judge2SetD[key])))
		print()
		
		print("ConfusionMatrix")
		print(ConfusionMatrix(judge1, judge2))

	
	def adjudication(self):
		JUDGE1NAME = 'leonardo'
		JUDGE2NAME = 'chris'
		rootdir = 'data'
		for subdir, dirs, files in os.walk(rootdir):
			newFile = []
			judge1 = []
			judge2 = []
			for filename in files:
			
				#Leonardo
				if filename.endswith(JUDGE1NAME):
					with open(os.path.join(subdir, filename)) as f:	
						lines = f.read().splitlines()
						for line in lines:
								judge1.append(line.split())
				#chris
				if filename.endswith(JUDGE2NAME):
					with open(os.path.join(subdir, filename)) as f:
						
						lines = f.read().splitlines()
						for line in lines:
								judge2.append(line.split())


			#bekijken of lijsten hetzelfde zijn
			for i, row in enumerate(judge1):
				#als beide judges het niks vinden
				if len(judge1[i]) == 5 and len(judge2[i]) == 5:
					newFile.append(judge1[i])
				
				elif len(judge1[i]) > 6 and len(judge2[i]) > 6:
					if judge1[i][5] == judge2[i][5] and judge1[i][6] == judge2[i][6]:
						newFile.append(judge1[i])

				else:
					print("Judge1 zegt: {} |||||| Judge2 zegt: {}".format(" ".join(judge1[i][3:])," ".join(judge2[i][3:])))
					inp = input("Judge 1 or 2? ")
					if inp == '1':
						newFile.append(judge1[i])
					else:
						newFile.append(judge2[i])
					
			#write new file
			if os.path.isfile(os.path.join(subdir, 'en.tok.off.pos.ent')) :
				os.remove(os.path.join(subdir, 'en.tok.off.pos.ent'))

			f = open(os.path.join(subdir, 'en.tok.off.pos.ent'), 'a')
			for row in newFile:
				newRow = "{} \n".format(" ".join(row))
				f.write(newRow)
			f.close()
			print()
			print("saved file {}".format(subdir +'/en.tok.off.pos.ent'))
			print()
		print("Generated Gold standard")

#C = Compare()
#C.compareJudges()
C.adjudication()