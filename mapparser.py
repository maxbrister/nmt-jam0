#MAP IMPORTER: 
def MAPIMPORT(fname):
	#Read the file to a string
	try:
		with open(fname) as f:
			string = f.read()
	except:
		print "FILE NAME DOES NOT EXIST"
		return none
	#Separate the header and body of the map
	Array = string.split('#\n')
	#handle null string case
	if Array == None:
		print "INVALID MAP"
		return 0
	Header = Array[0:1]
	if Header == None:
		print "INVALID MAP"
		return 0
	Body = Array[1:len(Array)]
	#parse the header
	Header = Header[0]
	References = Header.split(',')
	Ref2 = []  
	for Reference in References:
		Ref2.append(Reference.split('-'))
	Key = {}
	#create a dictionary of symbols, image names
	for Ref in Ref2:
		Key[Ref[0]] = Ref[1]
	Lines = Body
	Columns = []
	for Line in Lines:
		Row = []
		Characters = list(Line)
		for Character in Characters:
			Row.append(Key[Character])
		Columns.append(Row)
	return Columns
	#reparse the lists into image names 


print MAPIMPORT("test.mp")
