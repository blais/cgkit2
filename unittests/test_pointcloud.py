# Test the pointcloud module

import unittest
import os, os.path
from cgkit import pointcloud
from cgkit.cgtypes import *
import ctypes
try:
    import numpy
    numpy_available = True
except ImportError:
    print("Warning: numpy not available. pointcloud test incomplete.")
    numpy_available = False

class TestPointCloud(unittest.TestCase):
    """Test the pointcloud module.
    """
    
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.libName = os.getenv("CGKIT_POINTCLOUD_LIB")
        if self.libName is None:
            print ("pointcloud test is disabled. Set CGKIT_POINTCLOUD_LIB to the renderer lib to enable the test.")
#        self.libName = "aqsis_tex"
#        self.libName = "3delight"
#        self.libName = "prman"
        self.accuracy = 3
        
    def setUp(self):
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
    
    def testSinglePoints(self):
        """Test writing/reading individual points.
        """
        if self.libName is None:
            return
        
        world2eye = mat4(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
        world2ndc = mat4(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.10,0.11,0.12,0.13,0.14,0.15,0.16)
        ptc = pointcloud.open("tmp/pointcloud.ptc", "w", self.libName, vars=[], world2eye=world2eye, world2ndc=world2ndc, format=(640,480,1))
        ptc.writeDataPoint((0.1,0.2,0.3), (0,1,0), 0.5, {})
        ptc.writeDataPoint((1,2,3), (1,0,0), 1.0, {})
        ptc.writeDataPoint((-1,0.17,42), (0,0,1), 1.5, {})
        ptc.close()
        
        ptc = pointcloud.open("tmp/pointcloud.ptc", "r", self.libName)
        self.assertEqual(3, ptc.npoints)
        self.assertEqual([], ptc.variables)
        self.assertEqual(0, ptc.datasize)
#        print ptc.bbox
        self.assertAlmostEqual(-1.0, ptc.bbox[0], places=1)
        self.assertAlmostEqual(0.17, ptc.bbox[1], places=1)
        self.assertAlmostEqual( 0.3, ptc.bbox[2], places=1)
        self.assertAlmostEqual( 1.0, ptc.bbox[3], places=1)
        self.assertAlmostEqual( 2.0, ptc.bbox[4], places=1)
        self.assertAlmostEqual(42.0, ptc.bbox[5], places=1)
        self.assertEqual(16, len(ptc.world2eye))
        self.assertAlmostEqual(1, ptc.world2eye[0], places=self.accuracy)
        self.assertAlmostEqual(2, ptc.world2eye[1], places=self.accuracy)
        self.assertAlmostEqual(3, ptc.world2eye[2], places=self.accuracy)
        self.assertAlmostEqual(4, ptc.world2eye[3], places=self.accuracy)
        self.assertAlmostEqual(5, ptc.world2eye[4], places=self.accuracy)
        self.assertAlmostEqual(6, ptc.world2eye[5], places=self.accuracy)
        self.assertAlmostEqual(7, ptc.world2eye[6], places=self.accuracy)
        self.assertAlmostEqual(8, ptc.world2eye[7], places=self.accuracy)
        self.assertAlmostEqual(9, ptc.world2eye[8], places=self.accuracy)
        self.assertAlmostEqual(10, ptc.world2eye[9], places=self.accuracy)
        self.assertAlmostEqual(11, ptc.world2eye[10], places=self.accuracy)
        self.assertAlmostEqual(12, ptc.world2eye[11], places=self.accuracy)
        self.assertAlmostEqual(13, ptc.world2eye[12], places=self.accuracy)
        self.assertAlmostEqual(14, ptc.world2eye[13], places=self.accuracy)
        self.assertAlmostEqual(15, ptc.world2eye[14], places=self.accuracy)
        self.assertAlmostEqual(16, ptc.world2eye[15], places=self.accuracy)
        self.assertEqual(16, len(ptc.world2ndc))
        self.assertAlmostEqual(0.1, ptc.world2ndc[0], places=self.accuracy)
        self.assertAlmostEqual(0.2, ptc.world2ndc[1], places=self.accuracy)
        self.assertAlmostEqual(0.3, ptc.world2ndc[2], places=self.accuracy)
        self.assertAlmostEqual(0.4, ptc.world2ndc[3], places=self.accuracy)
        self.assertAlmostEqual(0.5, ptc.world2ndc[4], places=self.accuracy)
        self.assertAlmostEqual(0.6, ptc.world2ndc[5], places=self.accuracy)
        self.assertAlmostEqual(0.7, ptc.world2ndc[6], places=self.accuracy)
        self.assertAlmostEqual(0.8, ptc.world2ndc[7], places=self.accuracy)
        self.assertAlmostEqual(0.9, ptc.world2ndc[8], places=self.accuracy)
        self.assertAlmostEqual(0.10, ptc.world2ndc[9], places=self.accuracy)
        self.assertAlmostEqual(0.11, ptc.world2ndc[10], places=self.accuracy)
        self.assertAlmostEqual(0.12, ptc.world2ndc[11], places=self.accuracy)
        self.assertAlmostEqual(0.13, ptc.world2ndc[12], places=self.accuracy)
        self.assertAlmostEqual(0.14, ptc.world2ndc[13], places=self.accuracy)
        self.assertAlmostEqual(0.15, ptc.world2ndc[14], places=self.accuracy)
        self.assertAlmostEqual(0.16, ptc.world2ndc[15], places=self.accuracy)
        self.assertEqual((640.0, 480.0, 1.0), ptc.format)

        pos,norm,rad,data = ptc.readDataPoint()
        self.assertAlmostEqual(0.1, pos[0], places=self.accuracy)
        self.assertAlmostEqual(0.2, pos[1], places=self.accuracy)
        self.assertAlmostEqual(0.3, pos[2], places=self.accuracy)
        self.assertAlmostEqual(0, norm[0], places=self.accuracy)
        self.assertAlmostEqual(1, norm[1], places=self.accuracy)
        self.assertAlmostEqual(0, norm[2], places=self.accuracy)
        self.assertAlmostEqual(0.5, rad, places=self.accuracy)
        self.assertEqual({}, data)

        pos,norm,rad,data = ptc.readDataPoint()
        self.assertAlmostEqual(1.0, pos[0], places=self.accuracy)
        self.assertAlmostEqual(2.0, pos[1], places=self.accuracy)
        self.assertAlmostEqual(3.0, pos[2], places=self.accuracy)
        self.assertAlmostEqual(1, norm[0], places=self.accuracy)
        self.assertAlmostEqual(0, norm[1], places=self.accuracy)
        self.assertAlmostEqual(0, norm[2], places=self.accuracy)
        self.assertAlmostEqual(1.0, rad, places=self.accuracy)
        self.assertEqual({}, data)

        pos,norm,rad,data = ptc.readDataPoint()
        self.assertAlmostEqual(-1.0, pos[0], places=self.accuracy)
        self.assertAlmostEqual(0.17, pos[1], places=self.accuracy)
        self.assertAlmostEqual(42.0, pos[2], places=self.accuracy)
        self.assertAlmostEqual(0, norm[0], places=self.accuracy)
        self.assertAlmostEqual(0, norm[1], places=self.accuracy)
        self.assertAlmostEqual(1, norm[2], places=self.accuracy)
        self.assertAlmostEqual(1.5, rad, places=self.accuracy)
        self.assertEqual({}, data)

        self.assertRaises(EOFError, lambda: ptc.readDataPoint())
        
        ptc.close()
    
    def testMultiPoints(self):
        """Test writing/reading several points at once.
        """
        if self.libName is None:
            return
        
        pnts = (6*ctypes.c_float)(0.4, 0.8, 1.0,  0.9, 0.7, 0.6)
        norms = (6*ctypes.c_float)(1,0,0,  0,0,1)
        rads = (2*ctypes.c_float)(0.4, 0.5)
        data = (8*ctypes.c_float)(12.0, 1,2,3,   42.0, -1,-2,-3)
        ptc = pointcloud.open("tmp/pointcloud2.ptc", "w", self.libName, vars=[("float", "fspam"), ("vector", "vspam")], world2eye=mat4(1), world2ndc=mat4(1), format=(640,480,1))
        ptc.writeDataPoints(2, (pnts,norms,rads,data))
        ptc.close()
        
        ptc = pointcloud.open("tmp/pointcloud2.ptc", "r", self.libName)
        self.assertEqual(2, ptc.npoints)
        self.assertEqual([("float","fspam"), ("vector","vspam")], ptc.variables)
        self.assertEqual(4, ptc.datasize)
        ps = (6*ctypes.c_float)()
        ns = (6*ctypes.c_float)()
        rs = (2*ctypes.c_float)()
        ds = (8*ctypes.c_float)()
        ptc.readDataPoints(2, (ps,ns,rs,ds))
        self.assertAlmostEqual(0.4, ps[0], places=self.accuracy)
        self.assertAlmostEqual(0.8, ps[1], places=self.accuracy)
        self.assertAlmostEqual(1.0, ps[2], places=self.accuracy)
        self.assertAlmostEqual(0.9, ps[3], places=self.accuracy)
        self.assertAlmostEqual(0.7, ps[4], places=self.accuracy)
        self.assertAlmostEqual(0.6, ps[5], places=self.accuracy)
        self.assertAlmostEqual(1, ns[0], places=self.accuracy)
        self.assertAlmostEqual(0, ns[1], places=self.accuracy)
        self.assertAlmostEqual(0, ns[2], places=self.accuracy)
        self.assertAlmostEqual(0, ns[3], places=self.accuracy)
        self.assertAlmostEqual(0, ns[4], places=self.accuracy)
        self.assertAlmostEqual(1, ns[5], places=self.accuracy)
        self.assertAlmostEqual(0.4, rs[0], places=self.accuracy)
        self.assertAlmostEqual(0.5, rs[1], places=self.accuracy)
        self.assertAlmostEqual(12.0, ds[0], places=self.accuracy)
        self.assertAlmostEqual(1, ds[1], places=self.accuracy)
        self.assertAlmostEqual(2, ds[2], places=self.accuracy)
        self.assertAlmostEqual(3, ds[3], places=self.accuracy)
        self.assertAlmostEqual(42.0, ds[4], places=self.accuracy)
        self.assertAlmostEqual(-1, ds[5], places=self.accuracy)
        self.assertAlmostEqual(-2, ds[6], places=self.accuracy)
        self.assertAlmostEqual(-3, ds[7], places=self.accuracy)
        ptc.close()

        ptc = pointcloud.open("tmp/pointcloud2.ptc", "r", self.libName)
        pos,norm,rad,data = ptc.readDataPoint()
        self.assertAlmostEqual(0.4, pos[0], places=self.accuracy)
        self.assertAlmostEqual(0.8, pos[1], places=self.accuracy)
        self.assertAlmostEqual(1.0, pos[2], places=self.accuracy)
        self.assertAlmostEqual(1, norm[0], places=self.accuracy)
        self.assertAlmostEqual(0, norm[1], places=self.accuracy)
        self.assertAlmostEqual(0, norm[2], places=self.accuracy)
        self.assertAlmostEqual(0.4, rad, places=self.accuracy)
        self.assertAlmostEqual(12, data["fspam"], places=self.accuracy)
        self.assertAlmostEqual(1, data["vspam"][0], places=self.accuracy)
        self.assertAlmostEqual(2, data["vspam"][1], places=self.accuracy)
        self.assertAlmostEqual(3, data["vspam"][2], places=self.accuracy)
        ptc.close()
        
        ptc = pointcloud.open("tmp/pointcloud2.ptc", "r", self.libName)
        for buf in ptc.iterBatches(10, numpyArray=False, combinedBuffer=True):
            self.assertEqual(22, len(buf))
            self.assertAlmostEqual(0.4, buf[0], places=self.accuracy)
            self.assertAlmostEqual(0.8, buf[1], places=self.accuracy)
            self.assertAlmostEqual(1.0, buf[2], places=self.accuracy)
            self.assertAlmostEqual(1, buf[3], places=self.accuracy)
            self.assertAlmostEqual(0, buf[4], places=self.accuracy)
            self.assertAlmostEqual(0, buf[5], places=self.accuracy)
            self.assertAlmostEqual(0.4, buf[6], places=self.accuracy)
            self.assertAlmostEqual(12, buf[7], places=self.accuracy)
            self.assertAlmostEqual(1, buf[8], places=self.accuracy)
            self.assertAlmostEqual(2, buf[9], places=self.accuracy)
            self.assertAlmostEqual(3, buf[10], places=self.accuracy)
        ptc.close()

    def testMultiPointsOneBuffer(self):
        """Test writing/reading several points at once.
        """
        if self.libName is None:
            return
        if not numpy_available:
            return
        
        buffer = numpy.zeros(shape=(2,8), dtype=numpy.float32)
        buffer[0] = (1,2,3,1,0,0,7,8)
        buffer[1] = (-1,-2,-3,0,0,1,2,-8)
        ptc = pointcloud.open("tmp/pointcloud3.ptc", "w", self.libName, vars=[("float", "spam")], world2eye=mat4(1), world2ndc=mat4(1), format=(640,480,1))
        ptc.writeDataPoints(2, buffer)
        ptc.close()

        buf = numpy.zeros(shape=(3,8), dtype=numpy.float32)
        ptc = pointcloud.open("tmp/pointcloud3.ptc", "r", self.libName)
        n = ptc.readDataPoints(3, buf)
        self.assertEqual(2, n)
        # Round the normals
        buf[0][3] = round(buf[0][3],self.accuracy)
        buf[0][4] = round(buf[0][4],self.accuracy)
        buf[0][5] = round(buf[0][5],self.accuracy)
        buf[1][3] = round(buf[1][3],self.accuracy)
        buf[1][4] = round(buf[1][4],self.accuracy)
        buf[1][5] = round(buf[1][5],self.accuracy)
        self.assertEqual([1,2,3,1,0,0,7,8], list(list(buf)[0]))
        self.assertEqual([-1,-2,-3,0,0,1,2,-8], list(list(buf)[1]))
        n = ptc.readDataPoints(3, buf)
        self.assertEqual(0, n)
        ptc.close()

######################################################################

if __name__=="__main__":
    unittest.main()
