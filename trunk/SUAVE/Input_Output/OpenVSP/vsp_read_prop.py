## @ingroup Input_Output-OpenVSP
# vsp_read_prop.py

# Created:  Sep 2021, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units 
import vsp as vsp
import numpy as np
import string

# This enforces lowercase names
chars = string.punctuation + string.whitespace
t_table = str.maketrans( chars          + string.ascii_uppercase , 
                         '_'*len(chars) + string.ascii_lowercase )

# ----------------------------------------------------------------------
#  vsp read prop
# ----------------------------------------------------------------------

## @ingroup Input_Output-OpenVSP
def vsp_read_prop(prop_id, units_type='SI',write_airfoil_file=True): 	
    """This reads an OpenVSP propeller geometry and writes it into a SUAVE prop format. 
    """  

    # Check if this is vertical tail, this seems like a weird first step but it's necessary
    # Get the initial rotation to get the dihedral angles
    x_rot = vsp.GetParmVal( prop_id,'X_Rotation','XForm')		
    if  x_rot >=70:
        prop = SUAVE.Components.Energy.Converters.Lift_Rotor()	
    else:
        # Instantiate a prop
        prop = SUAVE.Components.Energy.Converters.Propeller()		

    # Set the units
    if units_type == 'SI':
        units_factor = Units.meter * 1.
    elif units_type == 'imperial':
        units_factor = Units.foot * 1.
    elif units_type == 'inches':
        units_factor = Units.inch * 1.		

    # Apply a tag to the prop
    if vsp.GetGeomName(prop_id):
        tag = vsp.GetGeomName(prop_id)
        tag = tag.translate(t_table)
        prop.tag = tag
    else: 
        prop.tag = 'propgeom'

    # Top level prop parameters
    # Wing origin
    prop.origin[0][0] = vsp.GetParmVal(prop_id, 'X_Location', 'XForm') * units_factor 
    prop.origin[0][1] = vsp.GetParmVal(prop_id, 'Y_Location', 'XForm') * units_factor 
    prop.origin[0][2] = vsp.GetParmVal(prop_id, 'Z_Location', 'XForm') * units_factor 
 
     

    # TO BE COMPLETED MY MICHAEL
    return prop