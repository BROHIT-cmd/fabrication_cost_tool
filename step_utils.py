from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps

def calculate_volume(step_file_path):
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file_path)

    if status != 1:
        raise Exception("Error reading STEP file")

    reader.TransferRoots()
    shape = reader.OneShape()

    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)

    volume = props.Mass()  # cubic units

    return volume
