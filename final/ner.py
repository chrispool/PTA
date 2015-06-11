
from nltk.tag.stanford import NERTagger 
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import os
from nltk.wsd import lesk
import re
from collections import Counter, defaultdict
import sys
import glob
from measures import Measures
import urllib.request
import json

class Ner():
	
	def __init__(self, argv):
		classifier = "ner/classifiers/" + "wikification.ser.gz"
		jar = "ner/stanford-ner-3.4.jar"
		self.tagger = NERTagger(classifier, jar)
		self.testfile = open(sys.argv[1])
		with open('html/htmlheader.txt', 'r') as h:
			self.htmlHeader = h.read()
		with open('html/htmlfooter.txt', 'r') as f:
			self.htmlFooter = f.read()
		
		self.measures = Measures()
		self.classify()
	
	def cleanData(self, line):
		#function to clean wrong annotated data
		if len(line) > 6:	
			if line[6] == '-':
				line[6] = ''
		if len(line) > 7:
			if line[7] == '-':
				line[7] = ''
		return line

	def classify(self):
		#create test data with as key document and tuple of word and label
		testdata = defaultdict(list)
		tokens = defaultdict(list)
		for line in self.testfile:
			e = self.cleanData(line.strip().split())
			if len(e) == 6:
				testdata[e[0]].append([e[0],e[1],e[2],e[3], e[4], e[5], 'O', ''])
			elif len(e) == 7:
				testdata[e[0]].append([e[0],e[1],e[2],e[3],e[4], e[5], e[6], ''])
			elif len(e) == 8:
				testdata[e[0]].append([e[0],e[1],e[2],e[3],e[4], e[5], e[6],e[7]])
			
			if len(e) < 4:
				#print(e)
				pass		
			else:
				tokens[e[0]].append(e[4]) #store tokens of this document
		#add classification
		for n,doc in enumerate(testdata):
			
			taggedDoc = self.tagger.tag(tokens[doc])
			taggedTokens = []
			for sentence in taggedDoc:
				taggedTokens.extend(sentence)

			for i,line in enumerate(testdata[doc]):
				expectedCategory = taggedTokens[i][1]
				testdata[doc][i].append(expectedCategory)

			#use entire doc for getting wiki links
			
			wikiLinks = self.getWikiLinks(testdata[doc])
			for i,line in enumerate(testdata[doc]):
				expectedLink = wikiLinks[i]
				testdata[doc][i].append(expectedLink)

		self.saveFile(testdata)
		self.measures.calculate(testdata) #use the measures script
		self.saveHTML(testdata)

	def saveFile(self, testdata):
		os.remove("data/output.txt")
		with open("data/output.txt", "a") as outputFile:
			for doc in testdata:
				for e in testdata[doc]:
					lineString = "{} {} {}".format(" ".join(e[0:6]), e[8], e[9])
					outputFile.write(lineString.strip() + '\n')


	def saveHTML(self, testdata):
		for html in glob.glob("html/*.html"):
 			os.remove(html)
		docs = []
		for doc in testdata:
			filename = doc + ".html"
			with open("html/" + filename, "a") as htmlfile:
				docs.append((filename, doc))
				htmlfile.write(self.htmlHeader)
				htmlfile.write('<h1>Document '+ doc +'</h1>\n')
				for line in testdata[doc]:
					if line[9] != '':
						url = line[9].split(",")
						htmlfile.write('<a data-toggle="tooltip" data-placement="top" title="Category: ' + line[8] + '" href="' + url[0] + '" target="_blank" class="' + line[8] + '">' + line[4] + ' </a>')
					else:
						htmlfile.write(line[4] + " ")
				
				htmlfile.write('<br /><br /><a href="index.html" class="btn btn-default">Back</a>\n')
				htmlfile.write(self.htmlFooter)

				htmlfile.close()
		
		with open("html/index.html", "a") as htmlfile:
			htmlfile.write(self.htmlHeader)
			htmlfile.write('<h1>List of documents</h1>\n')
			for link in docs:
				htmlfile.write('<li><a href="'+link[0]+'">'+link[1]+'</a></li>\n')
			htmlfile.write(self.htmlFooter)
		

		with open("html/classify.html", "a") as htmlfile:
			htmlfile.write(self.htmlHeader)
			htmlfile.write('<h1>Classify</h1>\n')
			htmlfile.write('''<form action="../htmlClassifier.py" method="post">
							First Name: <input type="text" name="first_name"><br />
							Last Name: <input type="text" name="last_name" />

							<input type="submit" value="Submit" />
							</form>''')
			htmlfile.write(self.htmlFooter)
		

	def getWikiLinks(self, doc):
		#make word pairs, for example new york as one query
		test = []
		skip = 0
		currentToken = []
		lastToken = 'O'
		keywords = []
		result = [''] * len(doc) #make list with default NONE tag
		for i, token in enumerate(doc):				
			if token[8] == lastToken:
				currentToken.append(i)		
			else:
				if lastToken is not 'O':
					keywords.append(currentToken)
				currentToken = [i]
			lastToken = token[8]

		for keyword in keywords:
			query = ''
			for token in keyword:
				query += doc[token][4] + "%20"
			

			url = 'http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch='+query[:-3]+'&format=json'
			
			with urllib.request.urlopen(url) as response:
				str_response = response.readall().decode('utf-8')
				data = json.loads(str_response)
			
			links = []
			for d in data:
				for r in data[d]:
					if r == 'search':
						for s in data[d][r]:
							
							if 'snippet' in s:
								
								links.append('http://en.wikipedia.org/wiki/' + s['title'].replace(" ", "_"))

			if len(links) > 0:

				link = links[0] #todo, check if other links are better
			else:
				link = 'NONE'
			for token in keyword:
				result[token] = link+",1"
		
		return result
		
		
	






		
n = Ner(sys.argv)