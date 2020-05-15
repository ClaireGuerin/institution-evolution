#What are the phenotype positions for the full model?
import sys


first = "contribution of resources to public good (x). Expressed only in CIVILIANS class"
second = "contribution of time to political debate (y). Expressed only in LEADERS class"
third = "opinion on policing vs advances (z). Expressed by ALL"
fourth = "opinion on leadership strength (lambda). Expressed by ALL"

phenlist = [first, second, third, fourth]

scriptdesc = "This script gives informaiton on the order in which phenotypes are given in the full model. There are 4 different phenotypes."
globalphen = "To get the whole list of phenotypes in order, type: python whatphenotypes.py 0"
specificphen = "To get the description of the phenotype at a specific position x in [1:4], type: python whatphenotypes.py x"

def get_response(arguments):
	if len(arguments) == 1:
		response = [scriptdesc,globalphen,specificphen]
	elif len(arguments) == 2:
		arg = int(arguments[1])
		if arg <= 0:
			response = [str(i+1)+": "+phenlist[i] for i in range(len(phenlist))]
		elif arg <= 4:
			response = [phenlist[arg - 1]]
		else:
			response = ["phenotype rank out of range > 4"]
	else:
		response = ["too many arguments given, only give one"]
	return(response)

result = get_response(sys.argv)
for element in result:
	print(element)


