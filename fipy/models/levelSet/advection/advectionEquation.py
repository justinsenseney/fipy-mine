#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "advectionEquation.py"
 #                                    created: 11/12/03 {10:39:23 AM} 
 #                                last update: 6/3/04 {2:53:54 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

"""

The `AdvectionEquation` object constructs the b vector and L matrix
necessary for the solution of the advection equation. The advection
equation is given by:

.. raw:: latex

    $$ \\frac{\\partial \\phi}{\\partial t} + u | \\nabla \\phi | $$

This solution method for the `AdvectionTerm` is set up specifically to
evolve `var` while preserving `var` as a distance function. This
equation is used in conjunction with the `DistanceFunction`
object. Further details of the numerical method can be found in "Level
Set Methods and Fast Marching Methods" by J.A. Sethian, Cambridge
University Press, 1999. Testing for the advection equation is in
`examples.levelSet.advection`

"""

from fipy.equations.matrixEquation import MatrixEquation
from fipy.terms.transientTerm import TransientTerm
from advectionTerm import AdvectionTerm


class AdvectionEquation(MatrixEquation):

    def __init__(self, var = None, advectionCoeff = None, solver = None):
        
        mesh = var.getMesh()

        terms = (
            TransientTerm(1., mesh),
            AdvectionTerm(advectionCoeff, mesh))
	
	MatrixEquation.__init__(
            self,
            var,
            terms,
            solver)
        

        
        
        
        