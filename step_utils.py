import cadquery as cq

def calculate_volume(step_file_path):
    shape = cq.importers.importStep(step_file_path)
    volume = shape.val().Volume()
    return volume
