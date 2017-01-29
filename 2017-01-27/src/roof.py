from pyplasm import*

def segment_list(verts):
	#each element of segmentList is a list with two points.
	#output example [[p1,p2],[p2,p3],...]

	lines = []
	for i in range(len(verts)-1):
		lines.append([verts[i],verts[i+1]])
	lines.append([verts[len(verts)-1],verts[0]])
	return lines

def create_landing(directions,alfa):
	#directions are explained as quadrants. For each point of roof's base, we give a number like 1,2,3 or 4
	#number represent in whitch quadrant we want to rotate flaps.
	#	2 | 1
	#	-----
	#	3 | 4
	#output: list of points of landing
	plane_points = []

	for i in directions:
		new_point = []
		if(i[1]==1): 
			new_point.append(i[0][0]+30*math.cos(PI/4))
			new_point.append(i[0][1]+30*math.sin(PI/4))
			
		if(i[1]==2): 
			new_point.append(i[0][0]-30*math.cos(PI/4))
			new_point.append(i[0][1]+30*math.sin(PI/4))
			
		if(i[1]==3): 
			new_point.append(i[0][0]-30*math.cos(PI/4))
			new_point.append(i[0][1]-30*math.sin(PI/4))
			
		if(i[1]==4): 
			new_point.append(i[0][0]+30*math.cos(PI/4))
			new_point.append(i[0][1]-30*math.sin(PI/4))
			
		new_point.append(i[0][2]+30*math.sin(alfa))
		plane_points.append(new_point)

	points = []
	for i in plane_points:
		points.append(i)
	points.append(plane_points[0])
	return points

def create_flaps(verts,directions,alfa):
	#output: hpc with flaps

	points = create_landing(directions,alfa)

	segmUp = segment_list(points)
	segmDown = segment_list(verts)

	if (len(segmDown) == len(segmUp)):
		listFalde = []
		for i in range(len(segmUp)-1):
			
			verts_temp = []
			hpc = 0
			verts_temp.append(segmUp[i][0])
			verts_temp.append(segmUp[i][1])
			verts_temp.append(segmDown[i][0])
			verts_temp.append(segmDown[i][1])
			hpc = MKPOL([verts_temp,[[1,2,3,4]],1])
			listFalde.append(hpc)

	return STRUCT(listFalde)

def create_roof(verts, cells, alfa, directions):

	points_landing = create_landing(directions,alfa) 
	landing = MKPOL([points_landing,cells,1])
	flaps = create_flaps(verts, directions,alfa)
	
	roof = STRUCT([landing, flaps])
	roof = OFFSET([.4,.4])(roof)
	roof = TEXTURE("src/texture/textureroof.jpg")(roof)

	return roof

#TEST-----------------------------------------------------------------
"""
verts = [[0,0,0],[6,0,0],[6,6,0],[3,6,0],[3,3,0],[0,3,0],[0,0,0]]
cells = [[1,2,5,6],[2,3,4,5]]

directions = [[[0,0,0],1],[[6,0,0],2],[[6,6,0],3],[[3,6,0],4],[[3,3,0],4],[[0,3,0],4]]

alfa = PI/4


#----------------------------------

cells = [[1,2,3],[3,4,5,6,3],[6,7,8,9,3],[9,10,11,3],[3,11,12,1]]
verts = [[4.1426775, 115.85808,0], [163.28571, 115.85808,0], [163.28571, 150.72321,0], [220.17113, 150.72321,0], [220.17113, 262.22619,0], [163.28571, 262.22619,0], [163.28571, 293.22024,0], [96.383926, 293.22024,0], [96.383926, 252.20982,0], [37.797618, 252.20982,0], [37.797618, 178.69345,0], [4.1577381, 178.69345,0], [4.1426775, 115.85808,0]]

directions = [[[4.1426775, 115.85808,0], 1], [[163.28571, 115.85808,0], 2], [[163.28571, 150.72321,0], 2], [[220.17113, 150.72321,0], 2], [[220.17113, 262.22619,0], 3], [[163.28571, 262.22619,0], 3], [[163.28571, 293.22024,0], 3], [[96.383926, 293.22024,0], 4], [[96.383926, 252.20982,0], 4], [[37.797618, 252.20982,0], 4], [[37.797618, 178.69345,0], 4], [[4.1577381, 178.69345,0], 4]]

"""

#create_roof(verts, cells, alfa, directions)
