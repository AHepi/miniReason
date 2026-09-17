import bpy
import math
from mathutils import Vector

SHOT_SPEC = {"schema_version": "uc1.blender-blocking.v1", "api_target": "Blender 5.2 Python API", "fps": 24, "resolution": {"width": 1920, "height": 1080, "percentage": 100}, "scene": "warehouse_blocking", "subjects": [{"id": "courier", "primitive": "cube", "dimensions": [0.8, 0.6, 1.8], "initial_location": [-5.0, -4.0, 0.9], "role": "mobile courier figure"}, {"id": "crate", "primitive": "cube", "dimensions": [1.5, 1.5, 1.5], "initial_location": [2.0, 1.0, 0.75], "role": "static crate prop"}, {"id": "drone", "primitive": "cube", "dimensions": [1.2, 1.2, 0.4], "initial_location": [0.0, 2.0, 7.0], "role": "aerial drone figure"}], "shots": [{"id": "S01_APPROACH", "frame_start": 1, "frame_end": 96, "duration_seconds": 4.0, "subjects": ["courier", "crate"], "camera": {"location": [10.0, -14.0, 8.0], "target": [0.0, 0.0, 1.0], "lens_mm": 28, "framing": "28 mm wide establishing two-shot"}, "motion": [{"subject": "courier", "data_path": "location", "frame_start": 1, "value_start": [-5.0, -4.0, 0.9], "frame_end": 96, "value_end": [-1.0, -1.0, 0.9], "description": "courier moves across warehouse floor to approach mark"}], "constraints": ["crate remains fixed at [2,1,0.75]", "drone excluded from visible subjects in S01"]}, {"id": "S02_REVEAL", "frame_start": 97, "frame_end": 168, "duration_seconds": 3.0, "subjects": ["courier", "crate", "drone"], "camera": {"location": [-4.0, -6.0, 2.8], "target": [1.2, 0.5, 1.2], "lens_mm": 50, "framing": "50 mm medium over-courier reveal"}, "motion": [{"subject": "courier", "data_path": "rotation_euler", "frame_start": 97, "value_start": [0.0, 0.0, 0.0], "frame_end": 120, "value_end": [0.0, 0.0, 0.7853981633974483], "description": "courier turns 45 degrees during 97-120"}, {"subject": "drone", "data_path": "location", "frame_start": 121, "value_start": [0.0, 2.0, 7.0], "frame_end": 168, "value_end": [0.0, 2.0, 4.0], "description": "drone descends from [0,2,7] to [0,2,4] during 121-168"}], "constraints": ["crate remains fixed at [2,1,0.75] and visible"]}, {"id": "S03_RETREAT", "frame_start": 169, "frame_end": 240, "duration_seconds": 3.0, "subjects": ["courier", "crate", "drone"], "camera": {"location": [7.0, -10.0, 2.0], "target": [0.0, 0.0, 1.5], "lens_mm": 35, "framing": "35 mm low wide three-subject shot"}, "motion": [{"subject": "courier", "data_path": "location", "frame_start": 169, "value_start": [-1.0, -1.0, 0.9], "frame_end": 240, "value_end": [-4.0, -3.0, 0.9], "description": "courier retreats continuously to [-4,-3,0.9]"}, {"subject": "drone", "data_path": "location", "frame_start": 169, "value_start": [0.0, 2.0, 4.0], "frame_end": 240, "value_end": [0.0, 2.0, 2.5], "description": "drone continuously descends to [0,2,2.5]"}], "constraints": ["crate remains fixed at [2,1,0.75]"]}]}


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def key_transform(obj, data_path, frame, value):
    setattr(obj, data_path, value)
    obj.keyframe_insert(data_path=data_path, frame=frame)


def build_scene():
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 240
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    objects = {}
    for subject in SHOT_SPEC["subjects"]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=tuple(subject["initial_location"]))
        obj = bpy.context.object
        obj.name = subject["id"]
        obj.scale = tuple(subject["dimensions"])
        objects[subject["id"]] = obj
    bpy.ops.object.camera_add(location=(10.0, -14.0, 8.0))
    camera = bpy.context.object
    scene.camera = camera
    camera.data.lens = 28
    look_at(camera, [0.0, 0.0, 1.0])
    key_transform(camera, "location", 1, (10.0, -14.0, 8.0))
    key_transform(camera.data, "lens", 1, 28)
    look_at(camera, [-4.0, -6.0, 2.8])
    key_transform(camera, "location", 97, (-4.0, -6.0, 2.8))
    key_transform(camera.data, "lens", 97, 50)
    look_at(camera, [7.0, -10.0, 2.0])
    key_transform(camera, "location", 169, (7.0, -10.0, 2.0))
    key_transform(camera.data, "lens", 169, 35)
    for shot in SHOT_SPEC["shots"]:
        for motion in shot["motion"]:
            obj = objects[motion["subject"]]
            start_value = motion["value_start"]
            end_value = motion["value_end"]
            if motion["data_path"] == "location":
                key_transform(obj, "location", motion["frame_start"], tuple(start_value))
                key_transform(obj, "location", motion["frame_end"], tuple(end_value))
            else:
                key_transform(obj, "rotation_euler", motion["frame_start"], math.radians(0.0))
                key_transform(obj, "rotation_euler", motion["frame_end"], math.radians(45.0))


build_scene()