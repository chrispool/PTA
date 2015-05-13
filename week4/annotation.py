import os
import nltk
class Annotation():

	def __init__(self):
		rootdir = 'data'

		for subdir, dirs, files in os.walk(rootdir):
			for filename in files:
				if filename[-3:] == "off":
					with open(os.path.join(subdir, filename)) as f:
						open(os.path.join(subdir, filename) + '.pos', 'w').close() #empty file

						lines = f.read().splitlines()
						result = []
						tokens = []
						for line in lines:
							charS, charE, tokenId, token = line.split()
							tokens.append(token)
							result.append((charS, charE, tokenId, token))
						posTokens = nltk.pos_tag(tokens)	
						
						f = open(os.path.join(subdir, filename) + '.pos', 'a')
						for i, row in enumerate(result):
							newRow = "{} {} {} {} {} \n".format(row[0], row[1], row[2], row[3], posTokens[i][1])
							f.write(newRow)
						f.close()

						f = open(os.path.join(subdir, filename) + '.pos_leonardo', 'a')
						for i, row in enumerate(result):
							newRow = "{} {} {} {} {} \n".format(row[0], row[1], row[2], row[3], posTokens[i][1])
							f.write(newRow)
						f.close()

						f = open(os.path.join(subdir, filename) + '.pos_chris', 'a')
						for i, row in enumerate(result):
							newRow = "{} {} {} {} {} \n".format(row[0], row[1], row[2], row[3], posTokens[i][1])
							f.write(newRow)
						f.close()
		print(".pos files generated")

a = Annotation()