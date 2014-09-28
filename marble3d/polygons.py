import math

# -------------------------------------
# Polygons Geometry
# -------------------------------------

def getPolygonArea(points):
    total = 0.0
    N = len(points)
    
    for i in range(N):
        v1 = points[i]
        v2 = points[(i+1) % N]
        total += v1['x']*v2['y'] - v1['y']*v2['x']
    
    return abs(total/2)

def getPolygonPerimetr(points):
	p = 0.0
	for i in range(1, len(points)):
		p += getDistance(points[i-1],points[i])
	return p

def getPolygonCenter(points):
	x = [p['x'] for p in points]
	y = [p['y'] for p in points]

	return {
		'x' : sum(x) / float(len(points)),
		'y' : sum(y) / float(len(points))
		}
def getDistance(point1,point2):
	return math.hypot(point2['x'] - point1['x'], point2['y'] - point1['y'])

def getPolygonAreaDiagonalLength(points):
	# if we imagine a rectangle around polygon, here we calculate diagonal length of such a rectangle
	xs = [point['x'] for point in points]
	ys = [point['y'] for point in points]
	
	left_top = {
		'x':min(xs),
		'y':min(ys)
	}
	right_bottom = {
		'x':max(xs),
		'y':max(ys)
	}
	return getDistance(left_top,right_bottom)

def enlargePolygon(points, multiplier):
	center = getPolygonCenter(points)
	return [{'x':multiplier*(point['x']-center['x'])+center['x'],'y':multiplier*(point['y']-center['y'])+center['y']} for point in points]

def enlargePolygonAbs(points, delta):
	for point in points:
		x = point['x']
		y = point['y']
		z = math.sqrt(math.pow(x,2)+math.pow(y,2))
		
		if z > 0: 
			fi = math.acos(x/z)
			print fi

			point['x'] = round((z + delta)*math.cos(fi),2)
			point['y'] = round((z + delta)*math.sin(fi),2)

	return points
# -----------------------------------------------
# Get Canonical Coordinates from CrowdCafe data
# -----------------------------------------------
def getRectangleCoordinates(shape):
	# convert rectangle into polygon to have the same logic for both shape types
	return [
		{'x': shape['left'],'y':shape['top']}, # left - top
		{'x': shape['left']+shape['width']*shape['scaleX'],'y':shape['top']}, # right - top
		{'x': shape['left']+shape['width']*shape['scaleX'],'y':shape['top']+shape['height']*shape['scaleY']}, # right - bottom
		{'x': shape['left'],'y':shape['top']+shape['height']*shape['scaleY']} # left - bottom
		
	]
def getPolygonPoints(shape):
	# apply starting point shift to all points of the polygon
	return [ {'x':point['x']+shape['left'],'y':point['y']+shape['top']} for point in shape['points'] ]

def getCanvasSize(shape):
	canvas = {}
	for key in ['width','height']:
		canvas[key]=shape[key]
	return canvas