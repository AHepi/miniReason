import ast
import json
import math
import sys


REQUIRED_API_CALLS = {
    "bpy.ops.object.select_all", "bpy.ops.object.delete", "bpy.ops.mesh.primitive_cube_add",
    "bpy.ops.object.camera_add", "keyframe_insert", "to_track_quat", "to_euler", "math.radians"
}
PINNED_BPY_CHAINS = {
    "bpy.ops", "bpy.ops.object", "bpy.ops.object.select_all", "bpy.ops.object.delete",
    "bpy.ops.object.camera_add", "bpy.ops.mesh", "bpy.ops.mesh.primitive_cube_add",
    "bpy.context", "bpy.context.object", "bpy.context.scene"
}
PINNED_BPY_CALLS = {
    "bpy.ops.object.select_all", "bpy.ops.object.delete",
    "bpy.ops.object.camera_add", "bpy.ops.mesh.primitive_cube_add"
}
TYPE_ATTRIBUTES = {
    "Object": {"location", "rotation_euler", "name", "scale", "keyframe_insert"},
    "CameraObject": {"location", "rotation_euler", "name", "scale", "keyframe_insert", "data"},
    "Scene": {"frame_start", "frame_end", "render", "camera"},
    "RenderSettings": {"resolution_x", "resolution_y", "resolution_percentage", "fps"},
    "CameraData": {"lens", "keyframe_insert"},
    "Vector": {"to_track_quat"},
    "Quaternion": {"to_euler"},
}
TYPE_CALLS = {
    "Object": {"keyframe_insert"}, "CameraObject": {"keyframe_insert"},
    "CameraData": {"keyframe_insert"}, "Vector": {"to_track_quat"},
    "Quaternion": {"to_euler"}
}
BANNED_NAMES = {
    "open", "exec", "eval", "compile", "__import__", "getattr", "setattr", "delattr",
    "globals", "locals", "vars", "input", "breakpoint"
}
BANNED_IMPORTS = {
    "os", "pathlib", "io", "socket", "urllib", "http", "requests", "subprocess", "shutil",
    "tempfile", "ctypes", "pickle", "importlib", "builtins", "sys"
}


def strict_load(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate key: " + key)
            out[key] = value
        return out
    def reject(value):
        raise ValueError("nonfinite JSON: " + value)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return json.load(handle, object_pairs_hook=pairs, parse_constant=reject)


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted(node.value)
        return (prefix + "." if prefix else "") + node.attr
    return ""


def motion_exists(shot, subject, data_path, start, before, end, after):
    for motion in shot["motion"]:
        if (motion["subject"], motion["data_path"], motion["frame_start"], motion["value_start"],
                motion["frame_end"], motion["value_end"]) == (subject, data_path, start, before, end, after):
            return True
    return False


def is_number(value):
    return type(value) in {int, float} and math.isfinite(value)


def valid_vec3(value):
    return isinstance(value, list) and len(value) == 3 and all(is_number(item) for item in value)


def finite_tree(value):
    if isinstance(value, float): return math.isfinite(value)
    if isinstance(value, list): return all(finite_tree(item) for item in value)
    if isinstance(value, dict): return all(isinstance(key, str) and finite_tree(item) for key, item in value.items())
    return value is None or type(value) in {str, int, bool}


def validate_spec(spec):
    errors = []
    if not isinstance(spec, dict): return ["spec object"]
    if not finite_tree(spec): errors.append("finite JSON values")
    if set(spec) != {"schema_version", "api_target", "fps", "resolution", "scene", "subjects", "shots"}: errors.append("top-level fields")
    if spec.get("schema_version") != "uc1.blender-blocking.v1": errors.append("schema_version")
    if spec.get("api_target") != "Blender 5.2 Python API": errors.append("api_target")
    if spec.get("fps") != 24: errors.append("fps")
    if spec.get("resolution") != {"width": 1920, "height": 1080, "percentage": 100}: errors.append("resolution")
    if not isinstance(spec.get("scene"), str) or not spec.get("scene"): errors.append("scene string")
    subject_records = spec.get("subjects", [])
    if not isinstance(subject_records, list) or len(subject_records) != 3:
        errors.append("exactly three subject records")
        subject_records = subject_records if isinstance(subject_records, list) else []
    subjects = {item.get("id"): item for item in subject_records if isinstance(item, dict)}
    expected_subjects = {
        "courier": ("cube", [0.8, 0.6, 1.8], [-5.0, -4.0, 0.9]),
        "crate": ("cube", [1.5, 1.5, 1.5], [2.0, 1.0, 0.75]),
        "drone": ("cube", [1.2, 1.2, 0.4], [0.0, 2.0, 7.0])
    }
    if set(subjects) != set(expected_subjects): errors.append("subject ids")
    if len(subjects) != len(subject_records): errors.append("duplicate or non-object subject record")
    for subject_id, expected in expected_subjects.items():
        item = subjects.get(subject_id, {})
        if set(item) != {"id", "primitive", "dimensions", "initial_location", "role"}: errors.append("subject fields " + subject_id)
        if not valid_vec3(item.get("dimensions")) or not valid_vec3(item.get("initial_location")): errors.append("subject vectors " + subject_id)
        if not isinstance(item.get("role"), str) or not item.get("role"): errors.append("subject role " + subject_id)
        if (item.get("primitive"), item.get("dimensions"), item.get("initial_location")) != expected:
            errors.append("subject " + subject_id)
    shots = spec.get("shots", [])
    exact = [
        ("S01_APPROACH", 1, 96, 4.0, ["courier", "crate"], [10.0, -14.0, 8.0], [0.0, 0.0, 1.0], 28.0, "wide"),
        ("S02_REVEAL", 97, 168, 3.0, ["courier", "crate", "drone"], [-4.0, -6.0, 2.8], [1.2, 0.5, 1.2], 50.0, "over-courier"),
        ("S03_RETREAT", 169, 240, 3.0, ["courier", "crate", "drone"], [7.0, -10.0, 2.0], [0.0, 0.0, 1.5], 35.0, "low wide")
    ]
    if len(shots) != 3:
        errors.append("exactly three shots")
        return errors
    for index, expected in enumerate(exact):
        shot = shots[index]
        if not isinstance(shot, dict):
            errors.append("shot object " + str(index + 1))
            continue
        camera = shot.get("camera", {})
        if set(shot) != {"id", "frame_start", "frame_end", "duration_seconds", "subjects", "camera", "motion", "constraints"}: errors.append("shot " + str(index + 1) + " fields")
        if set(camera) != {"location", "target", "lens_mm", "framing"}: errors.append("shot " + str(index + 1) + " camera fields")
        for motion in shot.get("motion", []):
            if set(motion) != {"subject", "data_path", "frame_start", "value_start", "frame_end", "value_end", "description"}: errors.append("shot " + str(index + 1) + " motion fields")
            if motion.get("subject") not in expected_subjects or motion.get("data_path") not in {"location", "rotation_euler"}: errors.append("shot " + str(index + 1) + " motion enum")
            if type(motion.get("frame_start")) is not int or type(motion.get("frame_end")) is not int: errors.append("shot " + str(index + 1) + " motion frames")
            if not valid_vec3(motion.get("value_start")) or not valid_vec3(motion.get("value_end")): errors.append("shot " + str(index + 1) + " motion vectors")
            if not isinstance(motion.get("description"), str) or not motion.get("description"): errors.append("shot " + str(index + 1) + " motion description")
        if len(shot.get("motion", [])) != [1, 2, 2][index]: errors.append("shot " + str(index + 1) + " exact motion count")
        if type(shot.get("frame_start")) is not int or type(shot.get("frame_end")) is not int or not is_number(shot.get("duration_seconds")): errors.append("shot " + str(index + 1) + " timing types")
        if not isinstance(shot.get("subjects"), list) or len(shot.get("subjects")) != len(set(shot.get("subjects", []))): errors.append("shot " + str(index + 1) + " subject list")
        if not valid_vec3(camera.get("location")) or not valid_vec3(camera.get("target")) or not is_number(camera.get("lens_mm")): errors.append("shot " + str(index + 1) + " camera values")
        if not isinstance(camera.get("framing"), str) or not camera.get("framing"): errors.append("shot " + str(index + 1) + " framing type")
        if not isinstance(shot.get("constraints"), list) or not shot.get("constraints") or any(not isinstance(item, str) or not item for item in shot.get("constraints", [])): errors.append("shot " + str(index + 1) + " constraints")
        actual = (shot.get("id"), shot.get("frame_start"), shot.get("frame_end"), shot.get("duration_seconds"),
                  shot.get("subjects"), camera.get("location"), camera.get("target"), camera.get("lens_mm"))
        if actual != expected[:8]: errors.append("shot " + str(index + 1) + " exact fields")
        if expected[8] not in camera.get("framing", "").lower(): errors.append("shot " + str(index + 1) + " framing")
        if shot.get("duration_seconds") != (shot.get("frame_end") - shot.get("frame_start") + 1) / 24:
            errors.append("shot " + str(index + 1) + " duration")
    if not motion_exists(shots[0], "courier", "location", 1, [-5.0, -4.0, 0.9], 96, [-1.0, -1.0, 0.9]): errors.append("S01 courier approach")
    if not motion_exists(shots[1], "courier", "rotation_euler", 97, [0.0, 0.0, 0.0], 120, [0.0, 0.0, 0.7853981633974483]): errors.append("S02 courier turn")
    if not motion_exists(shots[1], "drone", "location", 121, [0.0, 2.0, 7.0], 168, [0.0, 2.0, 4.0]): errors.append("S02 drone descent")
    if not motion_exists(shots[2], "courier", "location", 169, [-1.0, -1.0, 0.9], 240, [-4.0, -3.0, 0.9]): errors.append("S03 courier retreat")
    if not motion_exists(shots[2], "drone", "location", 169, [0.0, 2.0, 4.0], 240, [0.0, 2.0, 2.5]): errors.append("S03 drone descent")
    if any(motion.get("subject") == "crate" for shot in shots for motion in shot.get("motion", [])): errors.append("crate must remain static")
    return errors


def expr_type(node, env):
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.Dict):
        return "ObjectMap"
    if isinstance(node, ast.Subscript) and expr_type(node.value, env) == "ObjectMap":
        return "Object"
    if isinstance(node, ast.BinOp) and (expr_type(node.left, env) == "Vector" or expr_type(node.right, env) == "Vector"):
        return "Vector"
    if isinstance(node, ast.Attribute):
        chain = dotted(node)
        if chain == "bpy.context.scene": return "Scene"
        if chain == "bpy.context.object": return "Object"
        owner = expr_type(node.value, env)
        if owner == "Scene" and node.attr == "render": return "RenderSettings"
        if owner == "CameraObject" and node.attr == "data": return "CameraData"
    if isinstance(node, ast.Call):
        chain = dotted(node.func)
        if chain == "Vector": return "Vector"
        owner = expr_type(node.func.value, env) if isinstance(node.func, ast.Attribute) else None
        if owner == "Vector" and node.func.attr == "to_track_quat": return "Quaternion"
    return None


def function_env(function):
    known = {
        "look_at": {"obj": "Object"},
        "key_transform": {"obj": "Object"},
        "build_scene": {},
    }.get(function.name, {})
    env = dict(known)
    for _ in range(4):
        for node in ast.walk(function):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                inferred = expr_type(node.value, env)
                if dotted(node.value) == "bpy.context.object":
                    inferred = "CameraObject" if name == "camera" else "Object"
                if inferred is not None:
                    env[name] = inferred
    return env


def validate_script(spec, source):
    errors = []
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as error:
        return ["syntax: " + str(error)]
    imports = []
    assigned_spec = None
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    required_signatures = {"look_at": ["obj", "target"], "key_transform": ["obj", "data_path", "frame", "value"], "build_scene": []}
    if set(functions) != set(required_signatures): errors.append("functions must be exactly look_at, key_transform, build_scene")
    for name, args in required_signatures.items():
        function = functions.get(name)
        if function is not None and ([arg.arg for arg in function.args.args] != args or function.args.vararg or function.args.kwarg or function.args.defaults):
            errors.append("function signature: " + name)
    allowed_top = (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.Expr)
    for node in tree.body:
        if not isinstance(node, allowed_top): errors.append("unsupported top-level statement: " + node.__class__.__name__)
        if isinstance(node, ast.Expr) and not (isinstance(node.value, ast.Call) and dotted(node.value.func) == "build_scene"):
            errors.append("only build_scene() may be a top-level expression")
    env_by_node = {}
    for function in functions.values():
        env = function_env(function)
        for node in ast.walk(function): env_by_node[id(node)] = env
    observed = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(("import", alias.name, alias.asname))
        elif isinstance(node, ast.ImportFrom):
            imports.append(("from", node.module, tuple((alias.name, alias.asname) for alias in node.names), node.level))
        elif isinstance(node, ast.Name) and (node.id in BANNED_NAMES or node.id.startswith("__")):
            errors.append("banned name: " + node.id)
        elif isinstance(node, ast.Attribute):
            chain = dotted(node)
            if node.attr.startswith("_"): errors.append("private attribute: " + node.attr)
            elif chain.startswith("bpy"):
                if chain not in PINNED_BPY_CHAINS: errors.append("unpinned bpy chain: " + chain)
            elif chain.startswith("math"):
                if chain != "math.radians": errors.append("unpinned math chain: " + chain)
            else:
                env = env_by_node.get(id(node), {})
                owner = expr_type(node.value, env)
                if owner not in TYPE_ATTRIBUTES or node.attr not in TYPE_ATTRIBUTES[owner]:
                    errors.append("untyped or unpinned receiver attribute: " + (chain or node.attr))
        elif isinstance(node, ast.Call):
            name = dotted(node.func)
            if isinstance(node.func, ast.Name):
                if name not in {"Vector", "tuple", "look_at", "key_transform", "build_scene"}:
                    errors.append("unapproved direct call: " + (name or "<dynamic>"))
            elif isinstance(node.func, ast.Attribute):
                if name.startswith("bpy"):
                    if name not in PINNED_BPY_CALLS: errors.append("unapproved bpy call: " + name)
                elif name.startswith("math"):
                    if name != "math.radians": errors.append("unapproved math call: " + name)
                else:
                    env = env_by_node.get(id(node), {})
                    owner = expr_type(node.func.value, env)
                    if owner not in TYPE_CALLS or node.func.attr not in TYPE_CALLS[owner]:
                        errors.append("untyped or unapproved receiver call: " + (name or "<dynamic>"))
            else:
                errors.append("dynamic call target")
            if name in REQUIRED_API_CALLS: observed.add(name)
            if name.endswith(".keyframe_insert"): observed.add("keyframe_insert")
            if name.endswith(".to_track_quat"): observed.add("to_track_quat")
            if name.endswith(".to_euler"): observed.add("to_euler")
        elif isinstance(node, (ast.Global, ast.Nonlocal, ast.With, ast.AsyncWith, ast.AsyncFunctionDef,
                               ast.ClassDef, ast.Lambda, ast.Await, ast.Yield, ast.YieldFrom, ast.Try)):
            errors.append("unsupported statement: " + node.__class__.__name__)
        elif isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "SHOT_SPEC" for target in node.targets):
                try: assigned_spec = ast.literal_eval(node.value)
                except (ValueError, TypeError): errors.append("SHOT_SPEC must be a literal")
    expected_imports = [("import", "bpy", None), ("import", "math", None), ("from", "mathutils", (("Vector", None),), 0)]
    if imports != expected_imports: errors.append("imports must be exactly unaliased import bpy; import math; from mathutils import Vector")
    imported_roots = {item[1].split(".", 1)[0] for item in imports if isinstance(item[1], str)}
    if imported_roots & BANNED_IMPORTS: errors.append("banned import")
    if assigned_spec != spec: errors.append("embedded SHOT_SPEC differs from supplied spec")
    missing = sorted(REQUIRED_API_CALLS - observed)
    if missing: errors.append("missing required API calls: " + ", ".join(missing))
    return sorted(set(errors))


def main():
    if len(sys.argv) != 3:
        print(json.dumps({"ok": False, "errors": ["usage: verify_uc1.py SPEC_JSON BLENDER_SCRIPT"]}))
        return 2
    try:
        spec = strict_load(sys.argv[1])
        with open(sys.argv[2], "r", encoding="utf-8", newline="") as handle:
            source = handle.read()
        errors = validate_spec(spec) + validate_script(spec, source)
    except (OSError, ValueError, TypeError, KeyError) as error:
        errors = [error.__class__.__name__ + ": " + str(error)]
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
