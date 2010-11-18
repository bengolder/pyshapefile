'''
Created on Oct 22, 2010

@author: Benjamin Golder

This module was inspired by shpUtils by 
Zachary Forest Johnson
which was later edited by
Michael Geary
'''
import dbfUtils
from struct import unpack
from ShpFeature import *

def readAndUnpack(type, data):
    if data=='': return data
    return unpack(type, data)[0]

shapeTypeDict = {
                 0:'Null Shape',
                 1:'Point',
                 3:'PolyLine',
                 5:'Polygon',
                 8:'MultiPoint',
                 11:'PointZ',
                 13:'PolyLineZ',
                 15:'PolygonZ',
                 18:'MultiPointZ',
                 21:'PointM',
                 23:'PolyLineM',
                 25:'PolygonM',
                 28:'MultiPointM',
                 31:'MultiPatch'
                 }

classTypeDict = {
                'Point':ShpPoint,
                'PointM':ShpPointM,
                'PointZ':ShpPointZ,
                'MultiPoint':ShpMultiPoint,
                'MultiPointM':ShpMultiPointM,
                'MultiPointZ':ShpMultiPointZ,
                'PolyLine':ShpPolyLine,
                'PolyLineM':ShpPolyLineM,
                'PolyLineZ':ShpPolyLineZ,
                'Polygon':ShpPolygon,
                'PolygonM':ShpPolygonM,
                'PolygonZ':ShpPolygonZ,
                }


class ShpFile(object):
    '''
    This class is intended to serve as a translating device between
    ESRI Shapefiles and other types of spatial data
    I don't intend to use it to write Shapefiles, but I 
    have built it with the notion that it might do so
    in the future.
    '''

    def __init__(self,filePath):
        self.filePath = filePath
        self.proj = filePath[0:-4] + '.prj'
        self.dbfTable = self.readDbfTable()
        self.f = open(self.filePath, 'rb')
        header = self.readFileHeader()
        self.shapeType = header[0]
        self.boundingBox = header[1]
        self.records = self.readRecords()
        self.f.close()
 
    def readBoundingBox(self):
            xMin = readAndUnpack('d', self.f.read(8))
            yMin = readAndUnpack('d', self.f.read(8))
            xMax = readAndUnpack('d', self.f.read(8))
            yMax = readAndUnpack('d', self.f.read(8))
            bbox = (xMin, yMin, xMax, yMax)
            return bbox
    
    def readFileHeader(self):
        self.f.seek(32)
        shapeKey =  readAndUnpack('i', self.f.read(4))
        shapeType = shapeTypeDict[shapeKey]
        boundingBox = self.readBoundingBox()
        return (shapeType, boundingBox)
        
    def readPoint(self):
        x = readAndUnpack('d', self.f.read(8))
        y = readAndUnpack('d', self.f.read(8))
        return (x,y)
    
    def readNumParts(self):
        return readAndUnpack('i', self.f.read(4))
    
    def readNumPoints(self):
        return readAndUnpack('i', self.f.read(4))
    
    def readParts(self, numParts):
        partIndices = []
        for i in range(numParts):
            partIndex = readAndUnpack('i', self.f.read(4))
            partIndices.append(partIndex)
        return partIndices
              
    def readPoints(self, numPoints):
        points = []
        pointcheck = (0.0,0.0)
        for i in range(numPoints):
            point = self.readPoint()
            # ignore identical consecutive points
            if point != pointcheck:
                points.append(point)
            pointcheck = point
        return points
    
    def readZ(self):
        z = readAndUnpack('d', self.f.read(8))
        return z

    def readZBounds(self):
        zMin = self.readZ()
        zMax = self.readZ()
        return (zMin,zMax)
    
    def readZArray(self, numPoints):
        zArray = []
        for i in range(numPoints):
            z = self.readZ()
            zArray.append(z)
        return zArray
    
    def setZfield(self, fieldKey=None, zValue=0.0):
        # this method will erase any existing
        # z data of the geometry
        # and will replace it with values
        # from the field designated
        # by the fieldKey
        for record in self.records:
            if fieldKey != None:
                try:
                    zValue = float(record.dbfData[fieldKey])
                except:
                    print 'There is no field by that name in the table'
                    return 
            zArray = []
            for each in range(record.numPoints):
                zArray.append(zValue)
            record.make3D(zArray)
           
    def readDbfTable(self):
        dbfFile = self.filePath[0:-4] + '.dbf'
        dbf = open(dbfFile, 'rb')
        db = list(dbfUtils.dbfreader(dbf))
        dbf.close()
        return db
        
    def readRecords(self):
        records = []
        self.f.seek(100)
        iterator = 0
        while True:
            record = self.readFeature(iterator)
            if record == False:
                    break
            records.append(record)
            iterator += 1
        return records
    
    def readFeature(self, iterator):
        # the next 12 bytes are simply passed over, though they contain:
        # a record number: which doesn't seem to correspond to the dbf
        # a content length integer
        # a shapeType integer, which is never different form the shapeType of the file 
        read = self.f.read(12)
        if read == '':
                # signifies end of shapefile
                print 'Reached end of records.'
                return False
        else:
            # get shapeType and creates appropriate feature
            feature = classTypeDict[self.shapeType](self,iterator)
            return feature
        
    def getGeoJSON(self):
        '''
        
        '''
        pass
    
    def getKML(self):
        '''
        
        '''
        pass
    
    def getShapely(self):
        '''
        
        '''
        pass
        
    def getWKT(self):
        '''
        
        '''
        pass