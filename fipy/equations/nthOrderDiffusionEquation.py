#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "nthOrderDiffusionEquation.py"
 #                                    created: 6/10/04 {4:38:06 PM} 
 #                                last update: 6/10/04 {4:39:13 PM} 
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
 #  2004-06-10 JEG 1.0 original
 # ###################################################################
 ##

from fipy.equations.matrixEquation import MatrixEquation
from fipy.terms.transientTerm import TransientTerm
from fipy.terms.nthOrderDiffusionTerm import NthOrderDiffusionTerm

class NthOrderDiffusionEquation(MatrixEquation):
    """
    Diffusion equation is implicit.
    """    
    def __init__(self,
                 var,
                 transientCoeff = 1.,
                 diffusionCoeff = (1.,),
                 solver='default_solver',
                 boundaryConditions=()):
        mesh = var.getMesh()
	terms = (
	    TransientTerm(transientCoeff,mesh),
	    NthOrderDiffusionTerm(diffusionCoeff,mesh,boundaryConditions)
            )
	MatrixEquation.__init__(
            self,
            var,
            terms,
            solver)
