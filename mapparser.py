 #MAP IMPORTER: 
class MapError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


def MapImport(fname):
	#Read the file to a string
	try:
		f = os.path.join(os.path.dirname(__file__), fname)
		string = f.read()
	except:
		raise MapError('No such file name')
	#Separate the header and body of the map
	array = string.split('#\n')
	#handle null string case
	if array == None:
		raise MapError('No map')
	header = array[0:1]
	if header == None:
		raise MapError('Invalid map')
	body = array[1:len(array)]
	#parse the header
	header = header[0]
	references = header.split(',')
	ref2 = []  
	for reference in references:
		ref2.append(reference.split('-'))
	key = {}
	#create a dictionary of symbols, image names
	for ref in ref2:
		key[ref[0]] = ref[1]
	lines = body
	columns = []
	for line in lines:
		row = []
		characters = list(Line)
		for character in characters:
			row.append(key[character])
		columns.append(row)
		
	return columns[0:len(columns)-1]
	#reparse the lists into image names 

if __name__ == '__main__':
        print MapImport("maps/test.mp")
