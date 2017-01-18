from pyplasm import*
from larlib import*


#start function ------------------------------------------------------
def ggpl_window(x,y,z,occurrency):

	#start subfunction ------------------------------------------------------
	def create_window(dx,dy,dz):
		"""
		Function that creates a window according to given params
		@param dx: width on the x-axis
		@param dx: width on the y-axis
		@param dx: width on the z-axis

		"""

		X = QUOTE(x)
		Y = QUOTE(y)

		window = PROD([X,Y])
		window = SKEL_2(window)

		pol = UKPOL(window)

		verts = pol[0]
		cells = pol[1]

		glass = []

		for i in range(0,len(cells)):
			if(occurrency[i]==False):
				glass.append(cells[i])
				cells.remove(cells[i])

		glass2d = MKPOL([verts,glass,1])
		glass3d = COLOR(Color4f([153/255., 255/255., 255/255.,1]))(PROD([glass2d,Q(dz/2)]))


		win2d = MKPOL([verts,cells,1])
		win3d = COLOR(Color4f([102/255., 51/255., 0/255.,1]))(PROD([win2d, Q(dz)]))

		window = STRUCT([glass3d, win3d])
		#VIEW(window)
		return window
	#end subfunction ------------------------------------------------------


	return create_window
#end function ------------------------------------------------------


#start function ------------------------------------------------------	
def ggpl_door(x,y,z,occurrency):

	#start subfunction ------------------------------------------------------
	def create_door(dx,dy,dz):
		"""
		Function that creates a door according to given params
		@param dx: width on the x-axis
		@param dx: width on the y-axis
		@param dx: width on the z-axis

		"""
		X = QUOTE(x)
		Y = QUOTE(y)

		d = PROD([X,Y])
		d = SKEL_2(d)

		pol = UKPOL(d)

		verts = pol[0]
		cells = pol[1]

		slots = []

		for i in range(0,len(cells)):
			if(occurrency[i]==False):
				slots.append(cells[i])
				cells.remove(cells[i])

		handle = STRUCT([T([1,2,3])([dz,dy/2.,dz*1.2]),SPHERE(.2)([20,20])])
		handle = COLOR(Color4f([50/255., 21/255., 0/255.,1]))(JOIN(SKEL_1(handle)))


		win2d = MKPOL([verts,cells,1])
		win3d = COLOR(Color4f([102/255., 51/255., 0/255.,1]))(PROD([win2d, Q(dz)]))

		slot2d = MKPOL([verts,slots,1])
		slot3d = COLOR(Color4f([90/255., 41/255., 0/255.,1]))(PROD([slot2d,Q(dz/2)]))

		door = STRUCT([handle,win3d,slot3d])
		#VIEW(door)

		return door
	#end subfunction ------------------------------------------------------

	return create_door
#end function ------------------------------------------------------



	

#Input values window--------------------------------------------

dx = 5
dy = 10
dz = .5	

x = [dz,(dx-3*dz)/2,dz,(dx-3*dz)/2,dz]
y = [dz,(dy-2*dz),dz]
z = dz

occurrency = [True,True,True,True,False,True,True,True,True,False,True,True,True,True,True]

#ggpl_window(x,y,z,occurrency)(dx,dy,dz)


#Input values door--------------------------------------------

x = [dz,(dx-2*dz),dz]
y = [dz,(dy-3*dz)/5.,dz,((dy-3*dz)*4)/5.,dz]

occurrency = [True,True,True,True,True,True,False,False,True,True,True,True,True,True,True]


#ggpl_door(x,y,z,occurrency)(dx,dy,dz)
	 

