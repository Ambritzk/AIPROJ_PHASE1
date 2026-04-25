#This function is used to return a point between A and B
def lerp(A,B,t):
    return A + (B - A) * t

#This is used to check if there's an intersection between two line segments
def getIntersection(A,B,C,D):
    tTop = (D['x'] - C['x']) * (A['y'] - C['y']) - (D['y'] - C['y']) * (A['x'] - C['x'])
    uTop = (C['y'] - A['y']) * (A['x'] - B['x']) - (C['x'] - A['x']) * (A['y'] - B['y'])
    bottom = (D['y'] - C['y']) * (B['x'] - A['x']) - (D['x'] - C['x']) * (B['y'] - A['y'])

    #If not parallel
    if bottom != 0:
        t = tTop / bottom
        u = uTop / bottom
        if t >= 0 and t <= 1 and u >=0 and u <= 1:
            return {
                'x':lerp(A['x'],B['x'],t),
                'y':lerp(A['y'],B['y'],t),   
                'offset':t
                }    
        
    return None

#This is 
def polysIntersect(poly1,poly2):
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            touch = getIntersection(poly1[i],poly1[(i + 1) % len(poly1)],poly2[j],poly2[(j + 1) % len(poly2)])
            if touch:
                return True
    return False