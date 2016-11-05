from pyplasm import*
import numpy


#start function ------------------------------------------------------------
def ggpl_roof_builder(pol):
	"""
	Main function. Taking in input an hpc model of the solid model of roof, then creating
	the convex cell and in output there is a new hpc model with cells and beam's structure of roof
	@param pol: initial roof solid making by MKPOL function
	"""
	
	listCell = UKPOL(SKEL_2(pol))

	verts = listCell[0]
	verts = roundValues(verts)
	cells = listCell[1]
	param = listCell[2]

	#if cell are not complanarity, return none object
	if(not complanarity(verts, cells)):
		return 0
	
	#list of hpc object cell
	cells3d = []

	#list of cells made by list of verts. Example: [[v1,..,vn],[v1,..,vn],...]
	vertsAndCellsList = []

	#building lists
	for i in cells:
		vertsTemp = []	#temp list of vertex group by cell
		numVerts = len(i)	#number of verts inside a cell
		temp =[]	#temp list of index of the vertex that belongs to cell.
		
		for count in range(0,numVerts):
			vertsTemp.append(verts[count])
			temp.append(count+1)

		#if cell is no the plane cell ad the base of the roof, create it with mkpol.
		if(not baseCell(vertsTemp)):
			cells3d.append(OFFSET([.1,.1,.1])(MKPOL([vertsTemp,[temp],param])))


		vertsAndCellsList.append(vertsTemp)

		#update verts list, inside iteration
		verts = verts[numVerts:]

	#create dictionary
	dictionary = create_dict(vertsAndCellsList)

	#make hpc object with all cell 
	cells3d = T(3)(.1)(COLOR(Color4f([0/255., 204/255., 0/255.,1]))((STRUCT(cells3d))))

	#create beam structure of roof
	roofStructure = COLOR(Color4f([132/255., 54/255., 9/255.,1]))(OFFSET([.1,.1,.1])(SKEL_1(pol)))

	return STRUCT([cells3d, roofStructure])
#end function ------------------------------------------------------------



#start function ------------------------------------------------------------
def create_dict(values):
	"""
	Function that creates a dictionary using all rounded skel's vertex
	@param values: input list of vertex
	"""

	dictionary = {}
	for i in range(len(values)-1):
		for j in values[i]:
			key=",".join(str(x) for x in j)
			if(not dictionary.has_key(key)):
				dictionary[key] = [i]
			else:
				dictionary[key].append(i)
	return dictionary
#end function ------------------------------------------------------------




#start function ------------------------------------------------------------
def complanarity(verts, cells):
	"""
	For this method, values need to be rounded.
	@param verts: list of verts
	@param cells: list of cells
	"""
	for c in cells:
		
		if(len(c) > 3): 
			matrix = []			#Building matrix with verts for every cell
			lastValue = c[-1]
			for label in c:
				value = verts[int(label)-1]
				row = []
				for i in range(len(value)):
					row.append(value[i]-verts[lastValue-1][i])
				matrix.append(row)
			
			A = numpy.matrix(matrix)
			dim = numpy.linalg.matrix_rank(A)		#rank of matrix
			
			if(dim > 2):		#complanarity is satisfied if the matrix has rank 2 or less
				return False
	return True
#end function ------------------------------------------------------------


#start function ------------------------------------------------------------
def roundValues(values):
	"""
	Rounding values function
	@param values: list of values
	"""

	values = [[numpy.round(float(i), 2) for i in nested] for nested in values]
	values = [[abs(i) for i in nested] for nested in values]

	return values
#end function ------------------------------------------------------------


#start function ------------------------------------------------------------	
def baseCell(verts):
	"""
	Cheching if all verts of a cell take parts of the base cell.
	@param verts: list of verts
	"""
	for i in verts:
		if(i[2]!=0):
			return False
	return True
#end function ------------------------------------------------------------



#Nedeed values for executing function

#Hip roof------------------------------
verts = [[0,0,0],[5,0,0],[5,3,0],[4,1.5,2],[1,1.5,2],[0,3,0]]
cells = [[1,2,4,5],[2,4,3],[1,5,6],[3,4,5,6],[1,2,3,6]]

#Hip and valley roof------------------------
#verts = [[0,0,0],[6,0,0],[6,12,0],[3,12,0],[3,3,0],[0,3,0],[1.5,1.5,3],[4.5,1.5,3],[4.5,10.5,3]]
#cells = [[1,7,6],[2,8,7,1],[2,3,9,8],[4,3,9],[4,9,8,5],[5,8,7,6],[6,5,2,1],[5,4,3,2]]

#Gable roof---------------------------
#verts=[[0,0,0],[0,5,0],[8,5,0],[8,0,0],[4,0,3],[4,5,3]]
#cells=[[3,4,5,6],[1,2,6,5],[1,4,3,2]]


pol = MKPOL([verts,cells,1])

#run main function
VIEW(ggpl_roof_builder(pol))





