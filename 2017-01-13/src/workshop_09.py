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
			new_point.append(i[0][0]+math.cos(PI/4))
			new_point.append(i[0][1]+math.sin(PI/4))
			
		if(i[1]==2): 
			new_point.append(i[0][0]-math.cos(PI/4))
			new_point.append(i[0][1]+math.sin(PI/4))
			
		if(i[1]==3): 
			new_point.append(i[0][0]-math.cos(PI/4))
			new_point.append(i[0][1]-math.sin(PI/4))
			
		if(i[1]==4): 
			new_point.append(i[0][0]+math.cos(PI/4))
			new_point.append(i[0][1]-math.sin(PI/4))
			
		new_point.append(i[0][2]+math.sin(alfa))
		plane_points.append(new_point)

	points = []
	for i in plane_points:
		points.append(i)
	points.append(plane_points[0])
	return points

def create_flaps(verts,directions):
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
	#landing = TEXTURE("images/texture02.jpg")(landing)
	flaps = create_flaps(verts, directions)
	#flaps = TEXTURE("images/texture01.jpg")(flaps)

	#VIEW(STRUCT([landing, flaps]))


#TEST-----------------------------------------------------------------

verts = [[0,0,0],[6,0,0],[6,6,0],[3,6,0],[3,3,0],[0,3,0],[0,0,0]]
cells = [[1,2,5,6],[2,3,4,5]]

directions = [[[0,0,0],1],[[6,0,0],2],[[6,6,0],3],[[3,6,0],4],[[3,3,0],4],[[0,3,0],4]]

alfa = PI/4

create_roof(verts, cells, alfa, directions)
