#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 4/2/04 {4:01:07 PM} { 1:23:41 PM}
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
 #  2003-11-17 JEG 1.0 original
 # ###################################################################
 ##

"""
This example first solves the distance function Equation in one dimension:

.. raw:: latex

    $$ |\\nabla \\phi| = 1 $$

with

.. raw:: latex

    $$ \\phi = 0 \;\; \\text{at} \;\; x = L / 5 $$

then the variable is advected with,

.. raw:: latex

    $$ \\frac{ \\partial \\phi } { \\partial t} + \\vec{u} \\cdot \\nabla \\phi = 0 $$

The scheme used in the `AdvectionTerm` preserves the `distanceVariable` as a distance function.

The result can be tested with the following code:

   >>> distanceEquation.solve()
   >>> for step in range(steps):
   ...     it.timestep(dt = timeStepDuration)

   >>> x = Numeric.array(mesh.getCellCenters()[:,0])
   >>> distanceTravelled = timeStepDuration * steps * velocity
   >>> answer = x - interfacePosition - timeStepDuration * steps * velocity
   >>> answer = Numeric.where(x < distanceTravelled, x[0] - interfacePosition, answer)
   >>> Numeric.allclose(answer, Numeric.array(distanceVariable), atol = 1e-10)
   1
   
"""

import Numeric
   
from fipy.meshes.grid2D import Grid2D
from fipy.viewers.grid2DGistViewer import Grid2DGistViewer
from fipy.variables.cellVariable import CellVariable
from fipy.models.levelSet.distanceFunction.distanceFunctionEquation import DistanceFunctionEquation
from fipy.models.levelSet.advection.advectionEquation import AdvectionEquation
from fipy.iterators.iterator import Iterator
from fipy.solvers.linearPCGSolver import LinearPCGSolver

velocity = 1.
dx = 1.
dy = 1.
nx = 10
ny = 1
timeStepDuration = 1.
steps = 2

L = nx * dx

interfacePosition = L / 5.

mesh = Grid2D(dx = dx, dy = dy, nx = nx, ny = ny)

distanceVariable = CellVariable(
    name = 'level set variable',
    mesh = mesh,
    value = -1.
    )

distanceVariable.setValue(1.,  mesh.getCells(filter = lambda cell: cell.getCenter()[0] > interfacePosition))

distanceEquation = DistanceFunctionEquation(distanceVariable)

advectionEquation = AdvectionEquation(
    distanceVariable,
    advectionCoeff = velocity,
    solver = LinearPCGSolver(
        tolerance = 1.e-15, 
        steps = 1000))

it = Iterator((advectionEquation,))

if __name__ == '__main__':
    distanceViewer = Grid2DGistViewer(var = distanceVariable, palette = 'rainbow.gp', minVal = -10., maxVal = 10.)
    distanceViewer.plot()

    distanceEquation.solve()

    for step in range(steps):
        it.timestep(dt = timeStepDuration)

        distanceViewer.plot()

    raw_input('finished')