import math

def getPolygonCenter(points):
	x = [p['x'] for p in points]
	y = [p['y'] for p in points]

	return {
		'x' : sum(x) / float(len(points)),
		'y' : sum(y) / float(len(points))
		}

def enlargePolygonAbs(points, delta):
	center = getPolygonCenter(points)
	signs = {'x':1,'y':1};
	print center
	for point in points:
		x = point['x'] - center['x']
		y = point['y'] - center['y']
		z = math.sqrt(math.pow(x,2)+math.pow(y,2))
		
		if z > 0: 
			fi = math.acos(abs(x)/abs(z))

			point['x'] = math.copysign(1, x)*round((z + delta)*math.cos(fi),2) + center['x']
			point['y'] = math.copysign(1, y)*round((z + delta)*math.sin(fi),2) + center['y']

	return points

polygon = [{'x':0,'y':0},{'x':0,'y':100},{'x':100,'y':100},{'x':100,'y':0}]

print polygon
print enlargePolygonAbs(polygon,10)