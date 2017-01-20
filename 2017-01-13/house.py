from pyplasm import*
import csv

hwall = 3.
scale = .05
hwindow = hwall-(hwall/4.)
dimborder = .4

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
	extWall = S([1,2,3])([scale,scale,scale])(extWall)
	extWall = OFFSET([.2,.2,hwall])(extWall)

	doors = create_doors("lines/doors.lines")
	#doors = STRUCT([T([1,2])([.42,1.85]),doors])
	walls = DIFFERENCE([extWall, doors])

	windows = create_windows("lines/windows.lines")
	#windows = STRUCT([T([1,2])([.5,1.7]),windows])
	walls = DIFFERENCE([walls, windows])

	walls = TEXTURE("images/interior.jpg")(walls)

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
	intWall = S([1,2,3])([scale,scale,scale])(intWall)
	intWall = OFFSET([.2,.2,hwall])(intWall)

	doors = create_doors("lines/doors.lines")
	#doors = STRUCT([doors])
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
	floor = S([1,2,3])([scale,scale,scale])(floor)
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
	doors = S([1,2,3])([scale,scale,scale])(points)
	doors = OFFSET([.01,.4,hwall-(hwall/4.)])(doors)
	doors = STRUCT([T(2)(-.1),doors])
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
	
	windows = PROD([points, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
	windows = OFFSET([0.001,5,0.001])(windows)
	windows = S([1,2,3])([scale,scale,scale])(windows)
	windows = STRUCT([T(2)(-.01),windows])

	return STRUCT([windows])

#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def ggpl_create_house(path_ext_walls,path_int_walls):

	"""
	Main function
	path_ext_walls is the file .lines of external walls
	path_int_walls is the file .lines of internal walls
	"""

	ext = create_external_enclosure(path_ext_walls)
	intP = create_internal_partitions(path_int_walls)
	floor = create_floor(path_ext_walls)

	
	walls = STRUCT([ext,intP])		
	house = STRUCT([floor, walls])

	return house

	
#end function -----------------------------------------------------------




#calling main function:
#ggpl_create_house()
