import cadquery as cq

def calculate_volume(step_file_path):
    try:
        shape = cq.importers.importStep(step_file_path)

        # cadquery objects may contain multiple solids
        volumes = []

        for solid in shape.solids().vals():
            volumes.append(solid.Volume())

        total_volume = sum(volumes)

        return total_volume

    except Exception as e:
        raise Exception(f"STEP processing failed: {str(e)}")
``
