## -*-Pyth-*-
 # ###################################################################
 #  FiPy - a finite volume PDE solver in Python
 # 
 #  FILE: "vanLeerConvectionTerm.py"
 #                                    created: 7/14/04 {4:42:01 PM} 
 #                                last update: 7/16/04 {10:15:47 AM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This document was prepared at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this document is not subject to copyright
 # protection and is in the public domain.  vanLeerConvectionTerm.py
 # is an experimental work.  NIST assumes no responsibility whatsoever
 # for its use by other parties, and makes no guarantees, expressed
 # or implied, about its quality, reliability, or any other characteristic.
 # We would appreciate acknowledgement if the document is used.
 # 
 # This document can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2004-07-14 JEG 1.0 original
 # ###################################################################
 ##

"""
"""

__docformat__ = 'restructuredtext'

import Numeric

from fipy.terms.explicitUpwindConvectionTerm import ExplicitUpwindConvectionTerm
import fipy.tools.array as array

class VanLeerConvectionTerm(ExplicitUpwindConvectionTerm):
    def getGradient(self, normalGradient, gradUpwind):
	gradUpUpwind = -gradUpwind + 2 * normalGradient
	
	grad = Numeric.where(gradUpwind * gradUpUpwind < 0., 
				0., 
				Numeric.where(gradUpUpwind > 0., 
						Numeric.minimum(gradUpwind, gradUpUpwind), 
						-Numeric.minimum(abs(gradUpwind), abs(gradUpUpwind))))
			
	return grad
	
    def getOldAdjacentValues(self, oldArray, id1, id2):
	oldArray1, oldArray2 = ExplicitUpwindConvectionTerm.getOldAdjacentValues(self, oldArray, id1, id2)

	interiorIDs = self.mesh.getInteriorFaceIDs()
	interiorFaceAreas = array.take(self.mesh.getFaceAreas(), interiorIDs)
	interiorFaceNormals = array.take(self.mesh.getOrientedFaceNormals(), interiorIDs)
	
	# Courant-Friedrichs-Levy number
	interiorCFL = abs(array.take(self.coeff, interiorIDs)) * self.dt
	
	gradUpwind = (oldArray2 - oldArray1) / array.take(self.mesh.getCellDistances(), interiorIDs)
	
	vol1 = array.take(self.mesh.getCellVolumes(), id1)
## 	if Numeric.logical_or.reduce(interiorCFL > vol1):
	self.CFL = interiorCFL / vol1
## 	print "CFL1:", Numeric.maximum.reduce(interiorCFL / vol1)
	
	oldArray1 += 0.5 * self.getGradient(array.dot(array.take(oldArray.getGrad(), id1), interiorFaceNormals), gradUpwind) \
	    * (vol1 - interiorCFL) / interiorFaceAreas
	    
	vol2 = array.take(self.mesh.getCellVolumes(), id2)
## 	if Numeric.logical_or.reduce(interiorCFL > vol2):
	
	self.CFL = Numeric.maximum(interiorCFL / vol2, self.CFL)

## 	print "CFL2:", Numeric.maximum.reduce(interiorCFL / vol2)

	oldArray2 += 0.5 * self.getGradient(array.dot(array.take(oldArray.getGrad(), id2), -interiorFaceNormals), -gradUpwind) \
	    * (vol2 - interiorCFL) / interiorFaceAreas
	
## 	print "volume:", array.take(self.mesh.getCellVolumes(), id1)
## 	print "sweep:", interiorCFL
## 	print "area:", interiorFaceAreas
## 	print "oldArray:", oldArray
## 	print "oldArray1:", oldArray1
## 	print "oldArray2:", oldArray2
	
	return oldArray1, oldArray2

    def getFigureOfMerit(self):
	return min(0.2 / self.CFL)