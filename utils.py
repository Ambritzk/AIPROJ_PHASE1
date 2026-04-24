def lerp(A,B,t):
    return A + (B - A) * t

def getIntersection(A,B,C,D):
    tTop = (D['x'] - C['x']) * (A['y'] - C['y']) - (D['y'] - C['y']) * (A['x'] - C['x'])
    uTop = (C['y'] - A['y']) * (A['x'] - B['x']) - (C['x'] - A['x']) * (A['y'] - B['y'])
    bottom = (D['y'] - C['y']) * (B['x'] - A['x']) - (D['x'] - C['x']) * (B['y'] - A['y'])

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