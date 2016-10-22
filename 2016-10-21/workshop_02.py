from pyplasm import*
import csv
from ast import literal_eval as make_number

def ggpl_bone_structure(file_name):

	file = open(file_name, 'rb')
	reader = csv.reader(file, delimiter = ';')



	inputList = list(reader)

	distanceRow = []
	frameRow = []
	
	distanceRow.append(inputList[::2])
	frameRow.append(inputList[1::2])

	
	frameList = frameRow

	frameSolid = []


	for item in frameList:
		temp=[]
		for j in item:
			distanceList = [float(i) for i in j[0].split(',')]
			interstoryHeight = [float(i) for i in j[1].split(',')]
			widthPill = float(j[2])
			widthBeam = float(j[3])
			#print(distanceList)
		#print(isinstance(widthBeam, basestring))
			newFrame = plane_frame(distanceList, interstoryHeight, widthPill, widthBeam)
			frameSolid.append(newFrame)
	
	
	l=[]
	xdist = 0
	ydist = 0 
	zdist = 0
	data=[]

	for i in frameSolid:
		for d in distanceRow:
			xdist = xdist + float(d[0][0])
			ydist = ydist + float(d[0][1])
			zdist = zdist + float(d[0][2])
			frameElement = STRUCT([T(1)(xdist), T(2)(ydist), T(3)(zdist), i])
			l.append(frameElement)
				

	print(l)

	beams=(generate_beams(distanceRow, widthBeam, interstoryHeight))

	l.extend(beams)
	
	
	VIEW(STRUCT(l))	
	
def generate_beams(distanceRow, widthBeam, interstoryHeight):
	
	distance=[]
	distanceRow=distanceRow[0]
	for item in distanceRow:
		temp=[]
		for j in item:
			temp.append(float(j))
		distance.append(temp)
	

	lengthBeam=0
	for i in distance:
		for j in i:
			lengthBeam += j

	lengthBeam = lengthBeam - distance[len(distance)-1][0]

	xBeam = [-(distance[len(distance)-1][0]), lengthBeam]

	xBeam = QUOTE(xBeam)

	yBeam = QUOTE([widthBeam])
	xyBeam = INSR(PROD)([xBeam, yBeam])


	hBeam = []
	for i in interstoryHeight:
		hBeam.append(i)
		hBeam.append(widthBeam)

	#print(hBeam)

	beamList=[]
	temp = INSR(PROD)([xyBeam, QUOTE(hBeam)])
	beamList.append(temp)

	#VIEW(STRUCT(beamList))
	return beamList
	


	

#start function ------------------------------------------------------------
def plane_frame(distanceList, interstoryHeight, widthPill, widthBeam):
	"""
	@param distanceList: list of distance between the pillars. 
	@param interstoryHeight: list of distance between the floor.
	@param widthPill: is the width of a pillar. All pillars have same width.
	@param widthBeam: width of the beam.
	In this function we consider that widthPill = widthBeam, because of the stability of the frame.
	
	"""
	
	numBeam = len(interstoryHeight) #number of beam
	pillarsList = [widthPill] #create a new list of pillars and distance between them. First element is the first pillar.

	#creation of pillars' list
	for item in distanceList:
		pillarsList.append(item)
		pillarsList.append(widthPill)


	beamList = [] #create an empty beams' list

	#inserting element inside beams' list
	for item in interstoryHeight:
		beamList.append(item)
		beamList.append(widthBeam)

	#number of pillars it's like number of distance - 1
	numPill = len(distanceList)+1
	
	#create a list with the pillars' heights that are negative instead of interstory height
	hPillList = [(-i) for i in beamList]

	#x axis of pillars
	xPillar = QUOTE(pillarsList)
	#y axis of pillars
	yPillar = QUOTE([widthPill, -4])
	#2D pillars
	xyPillar = PROD([yPillar, xPillar])
	#3D pillars
	pillar = PROD([xyPillar, QUOTE(hPillList)])

	#need sum of distance between pillars to calculate lenght of beam
	sumdistancepill = sum([abs(i) for i in distanceList])

	#x axis of beam
	xBeam = QUOTE([(widthPill*numPill)+sumdistancepill])
	#y axis of beam
	yBeam = QUOTE([widthBeam])
	#2D beam
	xyBeam = PROD([yBeam, xBeam])
	#3D beam
	beam = PROD([xyBeam, QUOTE(beamList)]) 

	s = STRUCT([pillar, beam])

	return s

#end function---------------------------------------------------------------------

ggpl_bone_structure("frame_data_461963.csv")
