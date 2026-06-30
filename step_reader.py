import FreeCAD
import Part

shape = Part.Shape()
shape.read("input.step")

volume = shape.Volume
bbox = shape.BoundBox

length = bbox.XLength
width = bbox.YLength
height = bbox.ZLength

with open("output.txt", "w") as f:
    f.write(f"{volume},{length},{width},{height}")
