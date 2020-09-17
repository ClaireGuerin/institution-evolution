def specialmean(lst):
	length, total = 0, 0
	for value in lst:
		total += value
		length += 1
	if length == 0:
		tmpmean = None
	else:
		tmpmean = total / length
	return tmpmean

def specialdivision(x, y):
	if y == 0:
		tmp = None
	else:
		tmp = x / y
	return tmp

def specialvariance(samplesum, samplesumofsq, samplelength):
	if samplelength == 0:
		tmpvar = 0.0
	else:
		mean = samplesum / samplelength
		tmpvar = (samplesumofsq / samplelength) - mean * mean
	return tmpvar

def extractMeanAndVariance(lst, n):
	if n == 0:
		mean = None
		var = None
	else:
		mean = sum(lst) / n
		samplesumofsq = sum([x * x for x in lst])
		var = (samplesumofsq / n) - mean * mean
	return (mean,var)