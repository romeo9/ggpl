from pyplasm import*
import math


#---------start function--------------------------------------------------
def create_straight_stairs(dx, dy, dz, nStep):
	"""
	function that creates a stairs according to given parameters.
	@param dx: horizontal length of single step
	@param dy: distance between single step
	@param dz: distance of height of single step
	"""
	
	xStep = MKPOL([[[0,0],[dy,dz/2],[dy,dz],[0,dz],[0,0]],[[1,2,3,4,5]], 1]) #create single step
	step = PROD([QUOTE([dx]), xStep])

	xFirstStep = MKPOL([[[0,0],[dy,0],[dy,dz/2],[0,dz/2],[0,0]],[[1,2,3,4,5]], 1]) #create first step
	firstStep = PROD([QUOTE([dx]),xFirstStep])


	stairsList=[]
	stairsList.append(firstStep)

	tempy = 0
	tempz = 0
	for i in range(nStep):
		trasl = STRUCT([T(2)(tempy),T(3)(tempz/2), step]) #every step there is a traslation
		stairsList.append(trasl)
		tempy = dy+tempy
		tempz = dz+tempz

	return STRUCT(stairsList)
#---------end function--------------------------------------------------


#---------start function--------------------------------------------------
def ggpl_straight_stairs(dx, dy, dz):
	"""
	function that take in input three dimensions of an example box. According to these params
	this function build a structure with a skeleton of the box and inside
	"""
	dy=dy*2
	dz=dz/2

	yStep = 1	#dimension of single step
	xStep = 5 	#dimension of single step, if you want to make this param editable, you can make xStep=dx
	
	box = SKEL_1(CUBOID([dx,dy,dz]))

	nStep = int(dy/yStep)
	zStep = (float(dz)/float(nStep+1)*2)


	stairs = create_straight_stairs(xStep, yStep, zStep, nStep)

	VIEW(STRUCT([stairs, box]))

#---------end function--------------------------------------------------


ggpl_straight_stairs(5,8,20)

