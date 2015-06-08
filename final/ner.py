#reads all raw texts and 

from nltk.tag.stanford import NERTagger 
from collections import defaultdict
import os
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import os
from nltk.wsd import lesk
import re
from collections import Counter

class Ner():
	def __init__(self):
		classifier = "ner/classifiers/" + "wikification.ser.gz"
		jar = "ner/stanford-ner-3.4.jar"
		self.tagger = NERTagger(classifier, jar)
		self.lemmatizer = WordNetLemmatizer()

		
		rootdir = 'data'
		for subdir, dirs, files in os.walk(rootdir):
			for filename in files:
				
				if filename[-3:] == "raw":

					with open(os.path.join(subdir, filename)) as f:
						lines = f.read().strip()
						tokens = nltk.word_tokenize(lines)
						
						htmlFilename = subdir.split("/")[-1] + '.html'
						self.tag(tokens, htmlFilename)
						'''
						for l in self.tagger.tag(tokens):
							for word, tag in l:
								if tag == "O":
									print("{} ".format(word), end="")
								else:
									print("{} ({}) ".format(word, tag), end="")
						'''
	def tag(self,tokens,filename):
		result = []
		test = []
		for line in self.tagger.tag(tokens):
			skip = 0
			for i, pair in enumerate(line):
				if skip == 0:
					if pair[1] == 'O':
						word = pair[0]
					else:
						word = ''
						n = i
						while pair[1] == line[n][1]:
							word += "{} ".format(line[n][0])
							n += 1
							skip = n

					#print(word)
			
					test.append((word, pair[1]))
				else:
					skip -= 1
				

		
		
		
				
		rLine = []	
		
		words = [word for word, tag in test]
		# make list with word, ne, pos
		nerInLine = [tag for word, tag in test]
		posInLine = [tag for word, tag in nltk.pos_tag(words)]
		

			
		for i, word in enumerate(words):
			if nerInLine[i] == "O":
				if posInLine[i] == 'NN' or posInLine[i] == 'NNP':
					lemma = self.lemmatizer.lemmatize(word, wordnet.NOUN)
					synsets = wordnet.synsets(self.lemmatizer.lemmatize(lemma), pos="n")
					if len(synsets) == 1:
						ss = synsets[0]
						iswn = [lemma, ss, ss.definition() ]
						#iswn = 'SYN'
					elif len(synsets) > 1:
						
						pos = 'n'
						ss = lesk(words, lemma, pos)
						iswn = [lemma, ss, ss.definition() ]
						#iswn = 'SYN'
						
				else:
					iswn = 'O'
				rLine.append((word, iswn))

			else:
				rLine.append((word, nerInLine[i]))
		result.append(rLine)
		self.createHTMLpage(result,filename)
		self.printText(result)
	
	
	def createHTMLpage(self, text,filename):
		f = open('html/'+filename,'w')
		html = """
		<!DOCTYPE html>
		<html lang="en">
		  <head>
		    <meta charset="utf-8">
		    <meta http-equiv="X-UA-Compatible" content="IE=edge">
		    <meta name="viewport" content="width=device-width, initial-scale=1">
		    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
		    <title>Bootstrap 101 Template</title>

		    <!-- Bootstrap -->
		    <link href="css/bootstrap.min.css" rel="stylesheet">
		    <link href="css/pta.css" rel="stylesheet">
		    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
		    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
		    <!--[if lt IE 9]>
		      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		    <![endif]-->
		  </head>
		  <body>
		  <nav class="navbar navbar-inverse navbar-fixed-top">
	      <div class="container">
	        <div class="navbar-header">
	          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
	            <span class="sr-only">Toggle navigation</span>
	            <span class="icon-bar"></span>
	            <span class="icon-bar"></span>
	            <span class="icon-bar"></span>
	          </button>
	          <a class="navbar-brand" href="#">Project name</a>
	        </div>
	        <div id="navbar" class="collapse navbar-collapse">
	          <ul class="nav navbar-nav">
	            <li class="active"><a href="#">Home</a></li>
	            <li><a href="#about">About</a></li>
	            <li><a href="#contact">Contact</a></li>
	          </ul>
	        </div><!--/.nav-collapse -->
	      </div>
	    </nav>


		  <div id="text" class="container">
		    

		"""

		for l in text:
			
			for word, tag in l:
				if tag == "O":
					html += "{} ".format(word)
				else:
					if type(tag) is str:
						title = tag
						cssClass = tag
					else:
						title = tag[2]
						cssClass = 'SYN' 
					html += '<a title="{}" target="blank" class="{}" href="{}"">{}</a> '.format(title, cssClass, word, word)	
		
			html += '<br/>'


		html += """
		</div>

		    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
		    <!-- Include all compiled plugins (below), or include individual files as needed -->
		    <script src="js/bootstrap.min.js"></script>
		  </body>
		</html>

		"""

		f.write(html)
		f.close()


	def printText(self, text):
		print()
		print("New document")
		print("------------")
		prevTag = ''
		for l in text:
			print() #line in the text
			for word, tag in l:
				if tag == "O":
					print("{} ".format(word), end="")
				else:
					

					print("[{} ({})]".format(word, tag), end="")	
				
						
				prevTag = tag

		

n = Ner()