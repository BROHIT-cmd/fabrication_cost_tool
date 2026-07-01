import FreeCAD
import Part

shape = Part.Shape()
shape.read("input.step")

# Geometry
volume = shape.Volume          # mm³
bbox = shape.BoundBox

length = bbox.XLength
width = bbox.YLength
height = bbox.ZLength

# Save output
with open("output.txt", "w") as f:
    f.write(f"{volume},{length},{width},{height}")
