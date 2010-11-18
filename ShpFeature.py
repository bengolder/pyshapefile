


class ShpFeature(object):
    '''
    classdocs
    '''

    def __init__(self, shpFile, recordNumber):
        self.shpFile = shpFile
        self.recordNumber = recordNumber
        self.shapeType = shpFile.shapeType
        self.dbfData = self.readDbfData()
        
    def readDbfData(self):
        db = self.shpFile.dbfTable
        dbfData = {}
        for i in range(len(db[0])):
                dbfData[db[0][i]] = db[self.recordNumber + 2][i]
        return dbfData
    
    def make3D(self,zVals):
        # if there's not enough z values for the number of points
        # or not enough points for the number of z values
        if len(zVals) != len(self.points):
            print "That won't work. Please give me one Z value for each point, no more, no less."
            return
        # clear points3D
        self.points3D = []
        for i in range(len(zVals)):
            z = zVals[i]
            x = self.points[i][0]
            y = self.points[i][1]
            point3d = (x,y,z)
            self.points3D.append(point3d)
            
    def chopParts(self, partlist, pointlist):
        if type(partlist) == tuple:
            indexSpread = list(partlist)
        elif type(partlist) == list:
            indexSpread = partlist
        else:
            indexSpread = [partlist]
        indexSpread.append(len(pointlist))
        chunks = []
        for i in range(len(indexSpread) - 1):
            chunks.append(pointlist[indexSpread[i]:indexSpread[i+1]])
        return chunks
        
    def shapelyFormat(self):
        if self.parts > 1:
            return self.chopParts(self.parts, self.points)[0]
        elif self.numPoints == 1:
            return self.points[0]
        else:
            return self.points
        
    def geoJSON(self):
            '''
            
            '''
            pass
        
    def KML(self):
            '''
            
            '''
            pass

class ShpPoint(ShpFeature):
    
    def __init__(self, ShpFile, recordNumber):
        
        ShpFeature.__init__(self, ShpFile, recordNumber)
        self.parts = [0]
        self.numParts = 1
        self.numPoints = 1
        self.points = [self.shpFile.readPoint()]
        self.x = self.points[0][0]
        self.y = self.points[0][1]
        self.points3D = [(self.x,self.y,0.0)]
       
class ShpPointM(ShpPoint):
    def __init__(self,ShpFile, recordNumber):
        
        ShpPoint.__init__(self, ShpFile, recordNumber)
        
        self.m = self.shpFile.readZ()

class ShpPointZ(ShpPoint):
    def __init__(self,ShpFile, recordNumber):
        
        ShpPoint.__init__(self, ShpFile, recordNumber)
        
        self.z = self.shpFile.readZ()
        self.m = self.shpFile.readZ()
        self.make3D([self.z])

class ShpMultiPoint(ShpFeature):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpFeature.__init__(self, ShpFile, recordNumber)
        self.parts[0]
        self.numParts = 1
        self.boundingBox = self.shpFile.readBoundingBox()
        self.numPoints = self.shpFile.readNumPoints()
        self.points = self.shpFile.readPoints(self.numPoints)
    
class ShpMultiPointM(ShpMultiPoint):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpMultiPoint.__init__(self, ShpFile, recordNumber)
        self.mBounds = self.shpFile.readZBounds()
        self.mArray = self.shpFile.readZArray(self.numPoints)

class ShpMultiPointZ(ShpMultiPoint):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpMultiPoint.__init__(self, ShpFile, recordNumber)
        self.zBounds = self.shpFile.readZBounds()
        self.zArray = self.shpFile.readZArray(self.numPoints)
        self.mBounds = self.shpFile.readZBounds()
        self.mArray = self.shpFile.readZArray(self.numPoints)
        self.make3D(self.zArray)

class ShpPolyLine(ShpFeature):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpFeature.__init__(self, ShpFile, recordNumber)
        
        self.boundingBox = self.shpFile.readBoundingBox()
        self.numParts = self.shpFile.readNumParts()
        self.numPoints = self.shpFile.readNumPoints()
        self.parts = self.shpFile.readParts(self.numParts)
        self.points = self.shpFile.readPoints(self.numPoints)
    
class ShpPolyLineM(ShpPolyLine):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpPolyLine.__init__(self, ShpFile, recordNumber)
        
        self.mBounds = self.shpFile.readZBounds()
        self.mArray = self.shpFile.readZArray(self.numPoints)
        
class ShpPolyLineZ(ShpPolyLine):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpPolyLine.__init__(self, ShpFile, recordNumber)
        
        self.zBounds = self.shpFile.readZBounds()
        self.zArray = self.shpFile.readZArray(self.numPoints)
        self.mBounds = self.shpFile.readZBounds()
        self.mArray = self.shpFile.readZArray(self.numPoints)
        self.make3D(self.zArray)
        
class ShpPolygon(ShpFeature):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpFeature.__init__(self, ShpFile, recordNumber)
        
        self.boundingBox = self.shpFile.readBoundingBox()
        self.numParts = self.shpFile.readNumParts()
        self.numPoints = self.shpFile.readNumPoints()
        self.parts = self.shpFile.readParts(self.numParts)
        self.points = self.shpFile.readPoints(self.numPoints)

class ShpPolygonM(ShpPolygon):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpPolygon.__init__(self, ShpFile, recordNumber)
        
        self.mBounds = self.shpFile.readZBounds()
        self.mArray = self.shpFile.readZArray(self.numPoints)
        
class ShpPolygonZ(ShpPolygon):
    
    def __init__(self,ShpFile, recordNumber):
        
        ShpPolygon.__init__(self, ShpFile, recordNumber)
        
        self.zBounds = self.shpFile.readZBounds()
        self.zArray = self.shpFile.readZArray(self.numPoints)
        self.mBounds = self.shpFile.readZBounds()
        self.mArray = self.shpFile.readZArray(self.numPoints)
        self.make3D(self.zArray)
  
            