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

scale = .05 
hwall= 6
hdoor = hwall-(hwall/4.)
hwindow = hwall-(hwall/4.)
dimborder = .2
alfa = PI/4.




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


#----windows/doors--------

def hpc_door(dx,dy,dz):

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([dx-(dx/4.),dy/4.,dz-(dz/4.)])
	c1 = STRUCT([T([1,3])([(dx/4.)/2.,(dz/4.)/2.]),c1])
	c2 = STRUCT([T([2])([dy-(dy/4.)]),c1])

	

	door = DIFFERENCE([c,STRUCT([c1,c2])])

	door = TEXTURE("texture/texturefloor.jpg")(door)
	return door


def create_doors(filename):

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	doors = []

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


def hpc_window(dx,dy,dz):
	dimborder = 1

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([(dx-(3*dimborder))/2.,dy,(dz-(3*dimborder))/2.])
	c2 = STRUCT([T([1,3])([dimborder,dimborder]),c1,T([1])([((dx-(3*dimborder))/2.)+dimborder]),c1])
	c3 = STRUCT([c2, T(3)([((dz-(3*dimborder))/2.)+dimborder]),c2])


	borders = STRUCT([DIFFERENCE([c,c3])])
	glasses = STRUCT([T(2)(3*(dy/8.)),CUBOID([dx,dy/4.,dz])])

	borders = TEXTURE("texture/texturefloor.jpg")(borders)
	glasses = TEXTURE("texture/textureglass.jpg")(glasses)


	window = STRUCT([borders,glasses])
	return window




def create_windows(filename):

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	windows = []


	for i in reader:
		if(i[1]==i[3]):
			if(i[2]>i[0]):
				window = hpc_window(i[2]-i[0],5,hwindow/scale)
				window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
			else:
				window = hpc_window(i[0]-i[2],5,hwindow/scale)
				window = STRUCT([T([1,2,3])([i[2],i[1],((hwall/8.)/scale)]),window]) 		
			
		if(i[0]==i[2]):
			if(i[3]>i[1]):
				window = hpc_window(i[3]-i[1],5,hwindow/scale)
				window = R([1,2])(PI/2.)(window)
				window = STRUCT([T([1,2,3])([i[0]+5,i[1],((hwall/8.)/scale)]),window])
				
			else:
				window = hpc_window(i[1]-i[3],5,hwindow/scale)
				window = R([1,2])(PI/2.)(window)
				window = STRUCT([T([1,2,3])([i[0]+5,i[1],((hwall/8.)/scale)]),window])
				

				 
			#window = hpc_window(5,i[3]-i[1],hwindow/scale)
			#window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
		windows.append(window)

	windows = STRUCT(windows)
	windows = S([1,2,3])([scale,scale,scale])(windows)

	return windows


def create_ground_floor(path_ext_walls,path_int_walls, path_windows, path_doors):
	ext = h.create_external_enclosure(path_ext_walls)
	intP = h.create_internal_partitions(path_int_walls)
	parquet = h.create_floor(path_ext_walls)

	dimDoor = [2.,dimborder,(hwall)-(hwall/8.)]
	door = hpc_door(dimDoor[0],dimDoor[1],dimDoor[2])
	c = CUBOID([dimDoor[0],dimDoor[1],dimDoor[2]])

	reader = readFile(path_ext_walls)
	reader = [[float(float(j)) for j in i] for i in reader]

	door = STRUCT([T([1,2])([reader[0][1]*scale,reader[0][1]*scale]),door])
	c = STRUCT([T([1,2])([reader[0][1]*scale,reader[0][1]*scale]),c])
	
	#floor = DIFFERENCE([ext,c])
	floor = TEXTURE("texture/texturewall.jpg")(ext)

	doors = create_doors(path_doors)
	windows = create_windows(path_windows)

	return STRUCT([floor,intP, parquet, doors, windows])



def create_roof_first_model(filename):
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

def create_roof_second_model(filename):
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

	print points
	roof = r.create_roof(points,cells,alfa,directions)
	roof = S([1,2,3])([scale+.001,scale+.001,scale])(roof)

	return roof


def create_stairs(filename):
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

	stairs = TEXTURE("texture/texturestairs.jpg")(stairs)

	return stairs

def create_int_floor(path_ext_walls,path_int_walls,path_stairs,path_windows,path_doors):
	ext = h.create_external_enclosure(path_ext_walls)
	intP = h.create_internal_partitions(path_int_walls)
	walls = STRUCT([ext, intP])
	parquet = OFFSET([.1,.1,.1])(h.create_floor(path_ext_walls))

	reader = readFile(path_stairs)
	reader = [[float(float(j)) for j in i] for i in reader]

	hole = []
	for i in reader:
		hole.append(POLYLINE([[i[0],i[1]],[i[2],i[3]]]))
	hole = SOLIDIFY(STRUCT(hole))

	hole = S([1,2,3])([scale,scale,scale])(hole)
	hole = OFFSET([.01,.01,.1])(hole)
	floor = DIFFERENCE([parquet,hole])
	
	floor = TEXTURE("texture/texturefloor.jpg")(floor)
	doors = create_doors(path_doors)
	windows = create_windows(path_windows)

	intfloor = STRUCT([floor, doors, windows, walls])

	return STRUCT([T(3)(hwall), intfloor])


def main():

	#------------First Model --------------------------------------------------
	#uncomment for execute
	"""
	stairs1 = create_stairs("first_house/lines/stairs.lines")
	stairs2 = STRUCT([T(3)(hwall),stairs1])
	ground = create_ground_floor("first_house/lines/ext_walls.lines","first_house/lines/int_walls.lines","first_house/lines/windows.lines","first_house/lines/doors.lines")
	floor1 = create_int_floor("first_house/lines/ext_walls.lines","first_house/lines/int_walls.lines","first_house/lines/stairs.lines","first_house/lines/windows.lines","first_house/lines/doors.lines")
	floor2 = STRUCT([T(3)(hwall), floor1])
	roof1 = STRUCT([T(3)(hwall*3),create_roof_first_model("first_house/lines/ext_walls.lines")])
	VIEW(STRUCT([floor1, stairs1, ground, stairs2, floor2,roof1]))
	

	"""
	#------------Second Model --------------------------------------------------

	
	ground = create_ground_floor("second_house/lines/ext_walls.lines","second_house/lines/int_walls.lines","second_house/lines/windows.lines","second_house/lines/doors.lines")
	floor1 = create_int_floor("second_house/lines/ext_walls.lines","second_house/lines/int_walls.lines","second_house/lines/stairs.lines","second_house/lines/windows.lines","second_house/lines/doors.lines")
	stairs1 = create_stairs("second_house/lines/stairs.lines")
	roof = STRUCT([T(3)(hwall*2),create_roof_second_model("second_house/lines/ext_walls.lines")])
	VIEW(STRUCT([ground, stairs1, floor1, roof]))
	

if __name__ == '__main__':
    main()