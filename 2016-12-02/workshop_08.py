from pyplasm import*
import csv

#start function ---------------------------------------------------------
def readFile(filename):
	"""
	Function that read a file between filename.
	@param filename: name of file
	"""

	file = open(filename, 'rb')
	reader = csv.reader(file, delimiter=",")
	return list(reader)
#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def create_external_enclosure(filename):
	"""
	Function that creates the external walls of an house, with doors and windows
	"""
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	extWall = STRUCT(points)	
	extWall = S([1,2,3])([.02,.02,.02])(extWall)
	extWall = OFFSET([.2,.2,3])(extWall)

	doors = create_doors("lines/doors.lines")
	doors = STRUCT([T([1,2])([.42,1.85]),doors])
	walls = DIFFERENCE([extWall, doors])

	windows = create_windows("lines/windows.lines")
	windows = STRUCT([T([1,2])([.5,1.7]),windows])
	walls = DIFFERENCE([walls, windows])

	walls = TEXTURE("images/exterior.jpg")(walls)

	return walls
#end function -----------------------------------------------------------

	

#start function ---------------------------------------------------------
def create_internal_partitions(filename):
	"""
	Function that creates internal walls, with doors.
	"""
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))

	intWall = STRUCT(points)
	intWall = S([1,2,3])([.02,.02,.02])(intWall)
	intWall = OFFSET([.2,.2,3])(intWall)

	doors = create_doors("lines/doors.lines")
	doors = STRUCT([T([1,2])([-.1,-.1]),doors])
	walls = DIFFERENCE([intWall, doors])

	walls = TEXTURE("images/interior.jpg")(walls)


	return walls

#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def create_floor(filename):
	"""
	Simple function that returns the hpc floor of the house.
	"""
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	floor = SOLIDIFY(STRUCT(points))	
	floor = S([1,2,3])([.02,.02,.02])(floor)
	floor = TEXTURE("images/parquet.jpg")(floor)

	return floor

#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def create_doors(filename):
	"""
	Function that creates doors, taking paramether filename.
	"""
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))

	points = STRUCT(points)
	doors = S([1,2,3])([.02,.02,.02])(points)
	doors = OFFSET([.4,.4,2.5])(doors)
	return doors

#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def create_windows(filename):
	"""
	Function that creates windows, taking paramether filename.
	"""
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))

	points = STRUCT(points)
	
	windows = PROD([points, QUOTE([-50,70])])
	windows = OFFSET([10,30,10])(windows)
	windows = S([1,2,3])([.02,.02,.02])(windows)

	return STRUCT([windows])

#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def ggpl_create_house():

	"""
	Main function
	"""

	ext = create_external_enclosure("lines/external_enclosure.lines")
	intP = create_internal_partitions("lines/internal_partitions.lines")
	floor = create_floor("lines/external_enclosure.lines")
	
	walls = STRUCT([ext, T([1,2])([.42,1.85]),intP])		
	house = STRUCT([floor, walls])

	VIEW(house)
#end function -----------------------------------------------------------



#calling main function:
ggpl_create_house()
