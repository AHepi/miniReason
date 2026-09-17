import bpy
import math
from mathutils import Vector

SHOT_SPEC = {'schema_version': 'uc1.blender-blocking.v1', 'api_target': 'Blender 5.2 Python API', 'fps': 24, 'resolution': {'width': 1920, 'height': 1080, 'percentage': 100}, 'scene': 'Warehouse discovery: courier approaches a glowing crate as a drone descends, then retreats.', 'subjects': [{'id': 'courier', 'primitive': 'cube', 'dimensions': [0.8, 0.6, 1.8], 'initial_location': [-5.0, -4.0, 0.9], 'role': 'human placeholder'}, {'id': 'crate', 'primitive': 'cube', 'dimensions': [1.5, 1.5, 1.5], 'initial_location': [2.0, 1.0, 0.75], 'role': 'glowing-crate placeholder'}, {'id': 'drone', 'primitive': 'cube', 'dimensions': [1.2, 1.2, 0.4], 'initial_location': [0.0, 2.0, 7.0], 'role': 'drone placeholder'}], 'shots': [{'id': 'S01_APPROACH', 'frame_start': 1, 'frame_end': 96, 'duration_seconds': 4.0, 'subjects': ['courier', 'crate'], 'camera': {'location': [10.0, -14.0, 8.0], 'target': [0.0, 0.0, 1.0], 'lens_mm': 28.0, 'framing': 'wide establishing two-shot; courier enters left, crate holds right third'}, 'motion': [{'subject': 'courier', 'data_path': 'location', 'frame_start': 1, 'value_start': [-5.0, -4.0, 0.9], 'frame_end': 96, 'value_end': [-1.0, -1.0, 0.9], 'description': 'courier walks diagonally toward the crate'}], 'constraints': ['crate remains fixed at [2,1,0.75]', "drone remains out of this shot's subject list"]}, {'id': 'S02_REVEAL', 'frame_start': 97, 'frame_end': 168, 'duration_seconds': 3.0, 'subjects': ['courier', 'crate', 'drone'], 'camera': {'location': [-4.0, -6.0, 2.8], 'target': [1.2, 0.5, 1.2], 'lens_mm': 50.0, 'framing': 'medium over-courier shoulder; crate is the focal subject and descending drone stays visible above it'}, 'motion': [{'subject': 'courier', 'data_path': 'rotation_euler', 'frame_start': 97, 'value_start': [0.0, 0.0, 0.0], 'frame_end': 120, 'value_end': [0.0, 0.0, 0.7853981633974483], 'description': 'courier turns toward the revealed crate'}, {'subject': 'drone', 'data_path': 'location', 'frame_start': 121, 'value_start': [0.0, 2.0, 7.0], 'frame_end': 168, 'value_end': [0.0, 2.0, 4.0], 'description': 'drone descends into the reveal without reaching the floor'}], 'constraints': ['crate stays fixed and visible', 'drone moves only after frame 120']}, {'id': 'S03_RETREAT', 'frame_start': 169, 'frame_end': 240, 'duration_seconds': 3.0, 'subjects': ['courier', 'crate', 'drone'], 'camera': {'location': [7.0, -10.0, 2.0], 'target': [0.0, 0.0, 1.5], 'lens_mm': 35.0, 'framing': 'low wide three-subject composition; courier has open retreat space to frame left'}, 'motion': [{'subject': 'courier', 'data_path': 'location', 'frame_start': 169, 'value_start': [-1.0, -1.0, 0.9], 'frame_end': 240, 'value_end': [-4.0, -3.0, 0.9], 'description': 'courier backs away while facing the threat'}, {'subject': 'drone', 'data_path': 'location', 'frame_start': 169, 'value_start': [0.0, 2.0, 4.0], 'frame_end': 240, 'value_end': [0.0, 2.0, 2.5], 'description': 'drone continues its controlled descent'}], 'constraints': ['crate remains fixed', 'courier and drone motions continue from S02 without a position jump']}]}


def look_at(obj, target):
    direction = Vector(target) - obj.location
    rotation = direction.to_track_quat("-Z", "Y")
    obj.rotation_euler = rotation.to_euler()


def key_transform(obj, data_path, frame, value):
    if data_path == "location":
        obj.location = tuple(value)
    elif data_path == "rotation_euler":
        obj.rotation_euler = tuple(value)
    obj.keyframe_insert(data_path=data_path, frame=frame)


def build_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 240
    scene.render.resolution_x = SHOT_SPEC["resolution"]["width"]
    scene.render.resolution_y = SHOT_SPEC["resolution"]["height"]
    scene.render.resolution_percentage = SHOT_SPEC["resolution"]["percentage"]
    scene.render.fps = SHOT_SPEC["fps"]

    objects = {}
    for subject in SHOT_SPEC["subjects"]:
        bpy.ops.mesh.primitive_cube_add(location=tuple(subject["initial_location"]))
        obj = bpy.context.object
        obj.name = "BLOCK_" + subject["id"]
        obj.scale = tuple(value / 2.0 for value in subject["dimensions"])
        objects[subject["id"]] = obj

    bpy.ops.object.camera_add(location=tuple(SHOT_SPEC["shots"][0]["camera"]["location"]))
    camera = bpy.context.object
    camera.name = "BLOCK_Camera"
    scene.camera = camera

    for shot in SHOT_SPEC["shots"]:
        start = shot["frame_start"]
        end = shot["frame_end"]
        camera.location = tuple(shot["camera"]["location"])
        camera.data.lens = shot["camera"]["lens_mm"]
        look_at(camera, shot["camera"]["target"])
        camera.keyframe_insert(data_path="location", frame=start)
        camera.keyframe_insert(data_path="rotation_euler", frame=start)
        camera.keyframe_insert(data_path="location", frame=end)
        camera.keyframe_insert(data_path="rotation_euler", frame=end)
        camera.data.keyframe_insert(data_path="lens", frame=start)
        camera.data.keyframe_insert(data_path="lens", frame=end)
        for motion in shot["motion"]:
            obj = objects[motion["subject"]]
            key_transform(obj, motion["data_path"], motion["frame_start"], motion["value_start"])
            key_transform(obj, motion["data_path"], motion["frame_end"], motion["value_end"])

    courier = objects["courier"]
    courier.rotation_euler = (0.0, 0.0, math.radians(45.0))
    courier.keyframe_insert(data_path="rotation_euler", frame=240)


build_scene()
