#Identical to Solution.py with one exception:
#tempScore[1].remove(max(tempScore[1]))
#is deleted from sumScore.
#Therefore, all calculations are done without discarding the worst performance,
#working in the same way.

import random

def sumScore(score):
	from copy import deepcopy
	tempScore = deepcopy(score)
	return sum(tempScore[1])

def sortScores(scores):
	return sorted(scores, key=lambda x: (sumScore(x), x[1][0]))

def readPerformances(csvfile):
	import csv
	with open(csvfile) as performances:
		rdr = csv.reader(performances)
		output = {}
		next(rdr)
		for row in rdr:
			output[row[0]] = (float(row[1]), float(row[2]))
		return output

def generatePerformanceValue(performances):
	perfValues = {}
	for entry in performances.items():
		processed = random.normalvariate(entry[1][0], entry[1][1])
		perfValues.update({entry[0] : processed})
	return perfValues

def generatePositions(performancevalues):
	positiontuples = sorted(list(performancevalues.items()), key = lambda x: -x[1])
	positions = [name[0] for name in positiontuples]
	return positions

def calculateResults(csvfile):
	sailordata = readPerformances(csvfile)
	results = {}
	for key in sailordata.keys():
		results[key] = []
	for i in range(len(results)):
		genVal = generatePerformanceValue(sailordata)
		genPos = generatePositions(genVal)
		for position in genPos:
			results[position].append((genPos.index(position) + 1))
	resultsList = sortScores(results.items())
	resultsFinal = []
	for sailor in resultsList:
		resultsFinal.append(sailor[0])
	return resultsFinal

def resultsPositionGraph(csvfile, sailor, sample=1000):
	positionCount = [0] * len(readPerformances(csvfile))
	x = [(n+1) for n in range(len(positionCount))]
	xax = [0] + x + [len(x)+1]
	for i in range(sample):
		sailors = calculateResults(csvfile)
		position = sailors.index(sailor)
		positionCount[position] += 1
	import matplotlib.pyplot as plt
	plt.bar(x, positionCount, align='center')
	plt.ylim([0, sample])
	plt.xlim([1, len(x)])
	plt.title('Performance for %s over %s tournaments' % (sailor, str(sample)))
	plt.xlabel("Position")
	plt.ylabel("Frequency")
	plt.xticks(xax)
	plt.show()

def resultsDeviationGraph(csvfile, sample=1000): #this csvfile must contain 3 sailors
	if len(readPerformances(csvfile)) != 3:
		return 'Please use a file with 3 sailors, ideally with separate std devs'
	competitors = []
	for key, value in readPerformances(csvfile).items():
		competitors.append(key)
	competitors.sort()

	posCount1 = [0] * len(readPerformances(csvfile))
	posCount2 = [0] * len(readPerformances(csvfile))
	posCount3 = [0] * len(readPerformances(csvfile))
	x = [(n+1) for n in range(len(posCount1))]
	xax = [0] + x + [len(x)+1]
	for i in range(sample):
		sailors = calculateResults(csvfile)
		position1 = sailors.index(competitors[0])
		position2 = sailors.index(competitors[1])
		position3 = sailors.index(competitors[2])
		posCount1[position1] += 1
		posCount2[position2] += 1
		posCount3[position3] += 1
	import matplotlib.pyplot as plt
	import numpy as np
	ind = np.arange(len(x))
	width = 0.2

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, posCount1, width, color='r', align='center')
	rects2 = ax.bar(ind+width, posCount2, width, color='y', align='center')
	rects3 = ax.bar(ind+(width*2), posCount3, width, color='b', align='center')
	ax.set_ylabel('Frequency')
	ax.set_title('Performance to compare standard deviation')
	ax.set_xticks(xax)
	ax.set_xticklabels((1, 2, 3))
	ax.set_xlabel('Position')
	plt.ylim([0,sample])

	ax.legend((rects1[0], rects2[0], rects3[0]), (competitors[0] , competitors[1], competitors[2]))

	def autolabel(rects):
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x()+rect.get_width()/2, 1.05*height, '%d'%int(height), ha='center', va='bottom')
	autolabel(rects1)
	autolabel(rects2)
	autolabel(rects3)

	plt.show()