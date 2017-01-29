from pyplasm import*
import roof as r
import house as h
import csv,numpy
import stairs as s

"""
- scale interne/esterne
- struttura spaziale
- tetto
- porte/finestre
"""

#----Variables-----------------------------------------------------
#scale = .05					#Scale factor
#------------------------------------------------------------------



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
def hpc_door(dx,dy,dz):
	"""
	Function that create a door's hpc according to x,y,z dimensions.
	"""

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([dx-(dx/4.),dy/4.,dz-(dz/4.)])
	c1 = STRUCT([T([1,3])([(dx/4.)/2.,(dz/4.)/2.]),c1])
	c2 = STRUCT([T([2])([dy-(dy/4.)]),c1])

	

	door = DIFFERENCE([c,STRUCT([c1,c2])])

	door = TEXTURE("src/texture/texturefloor.jpg")(door)
	return door
#end function -----------------------------------------------------------



#start function ---------------------------------------------------------
def create_doors(filename, hwall,scale):
	"""
	Function that create all doors that are in file doors.lines
	@param filename: name of file, in this example is ../doors.lines
	"""

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	doors = []
	hdoor = hwall-(hwall/4.)

	for i in reader:
		if(i[1]==i[3]):
			door = hpc_door(i[2]-i[0],4,hdoor/scale)
			door = STRUCT([T([1,2])([i[0],i[1]]),door])	
			doors.append(door)
		else:
			door = hpc_door(4,i[3]-i[1],hdoor/scale)
			door = STRUCT([T([1,2])([i[0],i[1]]),door])	
			doors.append(door)

	doors = STRUCT(doors)
	doors = S([1,2,3])([scale,scale,scale])(doors)

	return doors
#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def hpc_window(dx,dy,dz,hwall):
	"""
	Function that create a window's hpc according to x,y,z dimensions.
	"""
	hwindow = hwall-(hwall/4.) 
	dimborder = hwindow/2.

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([(dx-(3*dimborder))/2.,dy,(dz-(3*dimborder))/2.])
	c2 = STRUCT([T([1,3])([dimborder,dimborder]),c1,T([1])([((dx-(3*dimborder))/2.)+dimborder]),c1])
	c3 = STRUCT([c2, T(3)([((dz-(3*dimborder))/2.)+dimborder]),c2])


	borders = STRUCT([DIFFERENCE([c,c3])])
	glasses = STRUCT([T(2)(3*(dy/8.)),CUBOID([dx,dy/4.,dz])])

	borders = TEXTURE("src/texture/texturefloor.jpg")(borders)
	glasses = TEXTURE("src/texture/textureglass.jpg")(glasses)


	window = STRUCT([borders,glasses])
	return window
#end function -----------------------------------------------------------




#start function ---------------------------------------------------------
def create_windows(filename,hwall,scale):
	"""
	Function that create all windows that are in file windows.lines
	@param filename: name of file, in this example is ../windows.lines
	"""

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	windows = []
	hwindow = hwall-(hwall/4.)

	for i in reader:
		if(i[1]==i[3]):
			if(i[2]>i[0]):
				window = hpc_window(i[2]-i[0],5,hwindow/scale,hwall)
				window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
			else:
				window = hpc_window(i[0]-i[2],5,hwindow/scale,hwall)
				window = STRUCT([T([1,2,3])([i[2],i[1],((hwall/8.)/scale)]),window]) 		
			
		if(i[0]==i[2]):
			if(i[3]>i[1]):
				window = hpc_window(i[3]-i[1],5,hwindow/scale,hwall)
				window = R([1,2])(PI/2.)(window)
				window = STRUCT([T([1,2,3])([i[0]+5,i[1],((hwall/8.)/scale)]),window])
				
			else:
				window = hpc_window(i[1]-i[3],5,hwindow/scale,hwall)
				window = R([1,2])(PI/2.)(window)
				window = STRUCT([T([1,2,3])([i[0]+5,i[1],((hwall/8.)/scale)]),window])
					
		windows.append(window)

	windows = STRUCT(windows)
	windows = S([1,2,3])([scale,scale,scale])(windows)

	return windows
#end function -----------------------------------------------------------



#start function ---------------------------------------------------------
def create_roof_first_model(filename,scale):
	"""
	Function that create the roof according to first model given.
	"""
	alfa = PI/4.
	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]
	
	points = []
	for i in reader:
		points.append([i[0],i[1],0])
	points.append([reader[0][0],reader[0][1]])
	
	directions = []
	directions.append([points[0],1])
	directions.append([points[1],2])
	directions.append([points[2],2])
	directions.append([points[3],2])
	directions.append([points[4],3])
	directions.append([points[5],3])
	directions.append([points[6],3])
	directions.append([points[7],4])
	directions.append([points[8],4])
	directions.append([points[9],4])
	directions.append([points[10],4])
	directions.append([points[11],4])

	cells = [[1,2,3],[3,4,5,6,3],[6,7,8,9,3],[9,10,11,3],[3,11,12,1]]
	
	roof = r.create_roof(points,cells,alfa,directions)
	roof = S([1,2,3])([scale+.001,scale+.001,scale])(roof)
	return roof
#end function -----------------------------------------------------------



#start function ---------------------------------------------------------
def create_roof_second_model(filename,scale):
	"""
	Function that create the roof according to second model given.
	"""
	alfa = PI/4.	
	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	points = []
	for i in reader:
		points.append([i[0],i[1],0])
	points.append([reader[0][0],reader[0][1]])

	cells = [[1,2,3,4]]
	directions = []
	directions.append([points[0],1])
	directions.append([points[1],2])
	directions.append([points[2],3])
	directions.append([points[3],4])

	roof = r.create_roof(points,cells,alfa,directions)
	roof = S([1,2,3])([scale+.001,scale+.001,scale])(roof)

	return roof
#end function -----------------------------------------------------------


#start function ---------------------------------------------------------
def create_stairs(filename, hwall,scale):
	"""
	Function that create stairs according to .lines given by param.
	Between stairs.lines this function can takes x,y,z dimensions of the stairs and
	it makes a translation to create a stairs that fit in the house.
	"""
	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]
	dx=0
	dy=0
	tx = reader[0][0]*scale
	ty = reader[0][1]*scale
	for i in reader:
		if i[1]==i[3]: #parallelo asse x
			dx = (i[2]-i[0])*scale
		if i[0]==i[2]: #parallelo asse y
			dy = (i[3]-i[1])*scale
	if dx < 0:
		dx = -dx
	if dy < 0:
		dy = -dy

	stairs = s.ggpl_straight_stairs(dx,dy,hwall)
	stairs = R([1,2])(PI)(stairs)
	stairs = STRUCT([T([1,2])([tx+dx,ty+dy]),stairs])

	stairs = TEXTURE("src/texture/texturestairs.jpg")(stairs)

	return stairs
#end function -----------------------------------------------------------



#start function ---------------------------------------------------------
def create_int_floor(walls,parquet,path_stairs,scale):
	"""
	Function that create intermediate floor. This kind of floor has a hole in the flooring
	because of the stairs.
	@param path_stairs: path to stairs.lines
	"""

	reader = readFile(path_stairs)
	reader = [[float(float(j)) for j in i] for i in reader]

	hole = []
	for i in reader:
		hole.append(POLYLINE([[i[0],i[1]],[i[2],i[3]]]))
	hole = SOLIDIFY(STRUCT(hole))

	hole = S([1,2,3])([scale,scale,scale])(hole)
	hole = OFFSET([.01,.01,.1])(hole)
	floor = DIFFERENCE([parquet,hole])
	
	floor = TEXTURE("src/texture/texturefloor.jpg")(floor)
	intfloor = STRUCT([floor, walls])

	return intfloor
#end function -----------------------------------------------------------


#start function -----------------------------------------------------------
def create_floor(path_ext_walls,path_int_walls,path_stairs,path_windows,path_doors,flag,flagmodel,hwall,scale):
	"""
	Function that create a basic floor.
	@param flag: char that says if the floor we want to create is ground floor or intermediate.
	"""

	ext_walls = h.create_external_enclosure(path_ext_walls,flagmodel,hwall,scale)
	int_walls = h.create_internal_partitions(path_int_walls,flagmodel,hwall,scale)
	walls = STRUCT([ext_walls, int_walls])
	parquet = OFFSET([.1,.1,.1])(h.create_floor(path_ext_walls,scale))
	doors = create_doors(path_doors,hwall,scale)
	windows = create_windows(path_windows,hwall,scale)

	walls = TEXTURE("src/texture/muri.jpg")(walls)

	if flag=='i':
		floor = create_int_floor(walls,parquet,path_stairs,scale) 
		floor = STRUCT([floor, windows, doors])
		return STRUCT([T(3)(hwall),floor])
	if flag=='g':
		parquet = TEXTURE("src/texture/texturefloor.jpg")(parquet)
		
		return STRUCT([walls,parquet, windows, doors])



#end function -----------------------------------------------------------


def create_first_model():
	hwall = 3.
	scale = .05
	path_to_first_model = "src/first_house/lines/"
	file_ext_walls = path_to_first_model + "ext_walls.lines"
	file_int_walls = path_to_first_model + "int_walls.lines"
	file_stairs = path_to_first_model + "stairs.lines"
	file_doors = path_to_first_model + "doors.lines"
	file_windows = path_to_first_model + "windows.lines"


	stairs1 = create_stairs(file_stairs, hwall,scale)
	stairs2 = STRUCT([T(3)(hwall),stairs1])
	ground = create_floor(file_ext_walls,file_int_walls,file_stairs,file_windows,file_doors,'g','first_model',hwall,scale)
	floor1 = create_floor(file_ext_walls,file_int_walls,file_stairs,file_windows,file_doors,'i','first_model',hwall,scale)
	
	roof1 = STRUCT([T(3)(hwall*2),create_roof_first_model(file_ext_walls,scale)])
	return STRUCT([floor1, stairs1, ground, stairs2,roof1])

def create_second_model():
	hwall = 6.
	scale = .05
	path_to_second_model = "src/second_house/lines/"
	file_ext_walls = path_to_second_model + "ext_walls.lines"
	file_int_walls = path_to_second_model + "int_walls.lines"
	file_stairs = path_to_second_model + "stairs.lines"
	file_doors = path_to_second_model + "doors.lines"
	file_windows = path_to_second_model + "windows.lines"

	ground = create_floor(file_ext_walls,file_int_walls,file_stairs,file_windows,file_doors,'g','second_model',hwall,scale)
	floor1 = create_floor(file_ext_walls,file_int_walls,file_stairs,file_windows,file_doors,'i','second_model',hwall,scale)
	stairs1 = create_stairs(file_stairs, hwall,scale)
	roof = STRUCT([T(3)(hwall*2),create_roof_second_model(file_ext_walls,scale)])
	return STRUCT([ground, stairs1, roof,floor1])
