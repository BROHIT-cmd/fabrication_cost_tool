import FreeCAD
import Part

# Read STEP file
shape = Part.Shape()
shape.read("input.step")

# Volume in mm³
volume = shape.Volume

# Bounding box
bbox = shape.BoundBox
length = bbox.XLength
width = bbox.YLength
height = bbox.ZLength

# Save output
with open("output.txt", "w") as f:
    f.write(f"{volume},{length},{width},{height}")
