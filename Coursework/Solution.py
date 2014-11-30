"""
Does it correctly sum scores after discarding the lowest?

>>> sumScore(("bob", [2, 4, 1, 1, 2, 5]))
10

Does it sort the scores in ascending order?

>>> sortScores([("Alice", [1, 2, 1, 1, 1, 1]), ("Bob", [3, 1, 5, 3, 2, 5]), ("Clare", [2, 3, 2, 2, 4, 2]), ("Dennis", [5, 4, 4, 4, 3, 4]), ("Eva", [4, 5, 3, 5, 5, 3])])
[('Alice', [1, 2, 1, 1, 1, 1]), ('Clare', [2, 3, 2, 2, 4, 2]), ('Bob', [3, 1, 5, 3, 2, 5]), ('Dennis', [5, 4, 4, 4, 3, 4]), ('Eva', [4, 5, 3, 5, 5, 3])]

Does it sort the scores in ascending order while accounting for identical totals ie. sorting by first race?

>>> sortScores([('Alice', [1, 2, 1, 1, 1, 1]), ('Bob', [1, 3, 2, 2, 4, 3]), ('Clare', [2, 3, 2, 2, 4, 2]), ('Dennis', [5, 4, 4, 4, 3, 4]), ('Eva', [4, 5, 3, 5, 5, 3])])
[('Alice', [1, 2, 1, 1, 1, 1]), ('Bob', [1, 3, 2, 2, 4, 3]), ('Clare', [2, 3, 2, 2, 4, 2]), ('Dennis', [5, 4, 4, 4, 3, 4]), ('Eva', [4, 5, 3, 5, 5, 3])]

Does it read the csv and correctly return a dictionary with the value pairs?

>>> readPerformances("sailors.csv") == {'Dennis': (90.0, 0.0), 'Clare': (100.0, 10.0), 'Eva': (90.0, 5.0), 'Bob': (100.0, 5.0), 'Alice': (100.0, 0.0)}
True

Does it properly create performance values with the normal distribution? 
YOU MUST SET THE SEED TO 57 BEFORE YOU RUN THESE TESTS

>>> generatePerformanceValue({'Dennis': (90.0, 0.0)})
{'Dennis': 90.0}

>>> generatePerformanceValue({'Clare': (100.0, 10.0)})
{'Clare': 111.52090179040226}

>>> generatePerformanceValue({'Eva': (90.0, 5.0)})
{'Eva': 94.18226076274071}

>>> generatePerformanceValue({'Bob': (100.0, 5.0)})
{'Bob': 101.4389222493041}

>>> generatePerformanceValue({'Alice': (100.0, 0.0)})
{'Alice': 100.0}

>>> generatePerformanceValue({'Bob': (100.0, 5.0)})
{'Bob': 102.13138621730953}

>>> generatePerformanceValue({'Bob': (100.0, 5.0)})
{'Bob': 102.29409458787741}

>>> generatePerformanceValue({'Bob': (100.0, 5.0)})
{'Bob': 93.0291295329582}

Does it properly list the sailor positions?

>>> generatePositions( {'Dennis': 90.0, 'Alice': 100.0, 'Bob': 101.4389222493041, 'Eva': 94.18226076274071, 'Clare': 111.52090179040226})
['Clare', 'Bob', 'Alice', 'Eva', 'Dennis']

Does it properly trial races and give winners?

>>> calculateResults("sailors.csv")
['Alice', 'Clare', 'Bob', 'Dennis', 'Eva']

"""
import random

def sumScore(score):
	from copy import deepcopy
	tempScore = deepcopy(score)
	tempScore[1].remove(max(tempScore[1]))
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