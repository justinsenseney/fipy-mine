#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input1Ddimensional.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 6/2/04 {6:15:06 PM} 
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

from fipy.tools.profiler.profiler import Profiler
from fipy.tools.profiler.profiler import calibrate_profiler

from fipy.meshes.grid2D import Grid2D
from fipy.viewers.grid2DGistViewer import Grid2DGistViewer
from fipy.iterators.iterator import Iterator

from fipy.tools.dimensions.physicalField import PhysicalField

import fipy.models.elphf.elphf as elphf


## from elphfIterator import ElPhFIterator

nx = 40
dx = PhysicalField(1.,"m")
L = nx * dx

mesh = Grid2D(
    dx = dx,
    dy = 1.,
    nx = nx,
    ny = 1)
    
parameters = {
    'time step duration': 10000,
##     'substitutional molar volume': 1,
    'phase': {
	'name': "xi",
	'mobility': 1.,
	'gradient energy': PhysicalField(1.,"J/m"),
	'value': 1.,
	'final': (1.,)
    },
    'solvent': {
	'standard potential': 0.,
	'barrier height': 0.
    }
}

parameters['substitutionals'] = (
    {
	'name': "c1",
	'diffusivity': 1.,
	'standard potential': 1.,
	'barrier height': 1.
    },
    {
	'name': "c2",
	'diffusivity': 1.,
	'standard potential': 1.,
	'barrier height': 1.
    }
)

fields = elphf.makeFields(mesh = mesh, parameters = parameters)

setCells = mesh.getCells(filter = lambda cell: cell.getCenter()[0] > mesh.getPhysicalShape()[0]/2)
fields['substitutionals'][0].setValue(PhysicalField(0.3,"mol/m**3"))
fields['substitutionals'][0].setValue(PhysicalField(0.6,"mol/m**3"),setCells)
fields['substitutionals'][1].setValue(PhysicalField(0.6,"mol/m**3"))
fields['substitutionals'][1].setValue(PhysicalField(0.3,"mol/m**3"),setCells)

equations, timeStepDuration = elphf.makeEquations(
    mesh = mesh, 
    fields = fields, 
    parameters = parameters
)

it = Iterator(equations = equations, timeStepDuration = timeStepDuration)

if __name__ == '__main__':
    viewers = [Grid2DGistViewer(var = field) for field in fields['all']]

    for viewer in viewers:
	viewer.plot()
	
    raw_input()

    # fudge = calibrate_profiler(10000)
    # profile = Profiler('profile', fudge=fudge)

    # it.timestep(50)
    # 
    # for timestep in range(5):
    #     it.sweep(50)
    #     it.advanceTimeStep


    for i in range(1):
	it.timestep(1)
    #     raw_input()
	
	for viewer in viewers:
	    viewer.plot()
	
    # profile.stop()
	    
    raw_input()
