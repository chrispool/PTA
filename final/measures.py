from collections import Counter, defaultdict
import nltk
import unicodedata
class Measures:

	def _init_(self):
		pass


	def normalizeString(self,s):
		return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

	def calculate(self, testdata):
		#calculate precision and recall for each category
		ref = defaultdict(set) 
		test = defaultdict(set)
		
		#calculate precision and recall for entity detection
		refSimple = defaultdict(set)
		testSimple = defaultdict(set)
		
		#confusion matrix
		cmRef = []
		cmTest = []

		#links
		correctLinks = 0
		nLinks = 0

		#all categories
		categories = ('COU', 'CIT', 'NAT', 'PER', 'ORG', 'ANI', 'SPO', 'ENT')

		#classify text
		for doc in testdata:
			for i,line in enumerate(testdata[doc]):
				
				#add category to confusion matrix list
				cmRef.append(testdata[doc][i][6]) #what it is
				cmTest.append(testdata[doc][i][8]) #what our classifier thinks

				#add unique token id to category p and recall
				tokenId = doc + str(i)
				ref[testdata[doc][i][6]].add(tokenId) 
				test[testdata[doc][i][8]].add(tokenId)

				#add unique token id to simple p and r by converting category to yes/no
				tokenId = doc + str(i)
				if testdata[doc][i][6] == '':
					testCategory = 'NO'
				else:
					testCategory = 'YES'

				if testdata[doc][i][8] == 'O':
					refCategory = 'NO'
				else:
					refCategory = 'YES'

				refSimple[refCategory].add(tokenId) 
				testSimple[testCategory].add(tokenId)
				#print(len())
				
				if testdata[doc][i][8] != 'O':
					nLinks += 1
					prediction = testdata[doc][i][9].lower().split(',')
					prediction[0] = self.normalizeString(prediction[0])
					print(testdata[doc][i][0])
					print("{} - {} - {}".format(testdata[doc][i][4],testdata[doc][i][7].lower(),prediction[0] ))
					print()
					if testdata[doc][i][7].lower() == prediction[0]:
						correctLinks += int(prediction[1])



		print("Accuracy WIKI = {:.2f}".format(correctLinks/nLinks))
		print(nltk.ConfusionMatrix(cmRef, cmTest))
		
		#print stats
		for category in categories:
			print(category)
			if category in test:
				self.printRecallPrecision(test[category], ref[category])
			else:
				print("0")

		print("Total")
		self.printRecallPrecision(testSimple['YES'], refSimple['YES'])

	def printRecallPrecision(self, obs, ref):
		p = nltk.metrics.precision(ref, obs)
		r = nltk.metrics.recall(ref, obs)
		f = nltk.metrics.f_measure(ref, obs)
		print("{:.2f} {:.2f} {:.2f} ".format(p,r,f))


if __name__ == "__main__":
    pass
    #todo, make this work to calculate given two files
