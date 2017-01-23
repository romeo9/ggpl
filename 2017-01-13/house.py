from pyplasm import*
import csv
import workshop_10 as w



hwall = w.hwall
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
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	extWall = STRUCT(points)	
	extWall = S([1,2,3])([scale,scale,scale])(extWall)
	extWall = OFFSET([.2,.2,hwall])(extWall)

	#doors = create_doors("first_house/lines/doors.lines")
	doors = create_doors("second_house/lines/doors.lines")
	walls = DIFFERENCE([extWall, doors])

	#windows = create_windows("first_house/lines/windows.lines")
	windows = create_windows("second_house/lines/windows.lines")
	walls = DIFFERENCE([walls, windows])

	walls = TEXTURE("texture/texturewall.jpg")(walls)

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

	#doors = create_doors("first_house/lines/doors.lines")
	doors = create_doors("second_house/lines/doors.lines")

	walls = DIFFERENCE([intWall, doors])

	walls = TEXTURE("texture/texturewall.jpg")(walls)


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
	floor = TEXTURE("texture/texturefloor.jpg")(floor)
	

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
	xaxis = []
	yaxis = []

	temp = 0

	for i in pointsRead:
		if float(i[1])==float(i[3]): #parallelo asse x
			xaxis.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
		if float(i[0])==float(i[2]): #parallelo asse y
			yaxis.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
		
	
	if(len(yaxis)!=0 and len(xaxis)!=0):
		yaxis = STRUCT(yaxis)
		xaxis = STRUCT(xaxis)
		yaxis = PROD([yaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
		yaxis = OFFSET([5,.001,.001])(yaxis)
		xaxis = PROD([xaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
		xaxis = OFFSET([.001,5,.001])(xaxis)

		windows = STRUCT([xaxis,yaxis])
		windows = S([1,2,3])([scale,scale,scale])(windows)
		windows = STRUCT([T(2)(-.01),windows])
	else:
		if(len(xaxis)!=0):
			xaxis = STRUCT(xaxis)
			xaxis = PROD([xaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
			xaxis = OFFSET([.001,5,.001])(xaxis)
			windows = xaxis
			windows = S([1,2,3])([scale,scale,scale])(windows)
			windows = STRUCT([T(2)(-.01),windows])
		if(len(yaxis)!=0):
			yaxis = STRUCT(yaxis)
			yaxis = PROD([yaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
			yaxis = OFFSET([.001,5,.001])(yaxis)
			windows = yaxis
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
