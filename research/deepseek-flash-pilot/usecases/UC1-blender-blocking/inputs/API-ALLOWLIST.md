# Blender 5.2 Python API pin for UC1

Read 2026-09-17 from the official current reference. The index identified itself as **Blender 5.2 Python API**. UC1 is a static compatibility target; Blender was not installed or executed.

Official pages:

- https://docs.blender.org/api/current/
- https://docs.blender.org/api/current/bpy.ops.mesh.html#bpy.ops.mesh.primitive_cube_add
- https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.select_all
- https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.delete
- https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.camera_add
- https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.keyframe_insert
- https://docs.blender.org/api/current/bpy.types.Object.html
- https://docs.blender.org/api/current/bpy.types.Scene.html
- https://docs.blender.org/api/current/bpy.types.RenderSettings.html
- https://docs.blender.org/api/current/bpy.types.Camera.html
- https://docs.blender.org/api/current/mathutils.html#mathutils.Vector.to_track_quat

Pinned callable names are `bpy.ops.mesh.primitive_cube_add`, `bpy.ops.object.select_all`, `bpy.ops.object.delete`, `bpy.ops.object.camera_add`, `bpy_struct.keyframe_insert`, `mathutils.Vector`, `Vector.to_track_quat`, `Quaternion.to_euler`, and `math.radians`.

Pinned Blender attributes used by the fixture are `bpy.context.object`, `bpy.context.scene`, `Scene.frame_start`, `Scene.frame_end`, `Scene.render`, `RenderSettings.resolution_x`, `resolution_y`, `resolution_percentage`, `fps`, `Scene.camera`, `Object.data`, `Camera.lens`, `Object.location`, `Object.rotation_euler`, `Object.scale`, and `Object.name`. Any other imported module, callable, or attribute is refused by this task's narrow grammar.

The checker uses a narrow typed AST grammar: exact unaliased imports, exact full `bpy.*` operator chains, fixed helper signatures, and receiver-specific attribute/call sets for scene, render settings, object, camera-data, vector, and quaternion aliases. It rejects dynamic call targets, submodule aliases, unknown qualified chains, fake receiver methods, dunder access, render-write calls, and listed file/network/process surfaces. This deliberately rejects some potentially safe alternative Blender programs. It does not execute the submitted script or prove runtime behavior, camera-space visibility, or visual quality.

If the owner names a specific Blender plugin at launch time, that plugin's documented interface and version replace this plain-`bpy` pin; the task must be resealed with a new checker allowlist before dispatch.
