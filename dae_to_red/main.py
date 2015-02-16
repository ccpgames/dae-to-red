

import textwrap
import argparse
import math
import sys
import os

from . import axis
from . import colladamunge
from . import red
from . import util


DESCRIPTION = """Extracts curve data from a .dae file exported from
 for example Blender or Maya and converts it to one .red file.

 Notes:
 - Currently only tested on collada files exported from BLENDER or MAYA.
 - Only extracts location and rotation from objects.
 - Only supports rotation mode XYZ Euler.
"""


def axis_to_index(c):
    return ord(c) - ord('X')


def get_parameter_offset(parameter_name, parameter_list):
    for i, p in enumerate(parameter_list):
        if p["name"] == parameter_name:
            return i
    raise RuntimeError("Parameter not in list")


def read_source_dict_from_animation(animation):
    source_dict = {}
    for s in animation.samplers:
        for i in s.inputs:
            source = animation.sources[i.source_id]
            source_dict[i.semantic] = {
                "stride": source.stride,
                "parameters": source.parameters,
                "values":  source.values,
                "count": source.count,
                }
    return source_dict


def read_curve_data_from_animation(animation, curves):
    if not animation.samplers:
        return

    source_dict = read_source_dict_from_animation(animation)
    input_dict = source_dict["INPUT"]
    output_dict = source_dict["OUTPUT"]
    for i in xrange(source_dict["INPUT"]["count"] - 1):
        curve_type = source_dict["INTERPOLATION"]["values"][i]

        for c in animation.channels.keys():
            for out_param in output_dict["parameters"]:
                out_stride = output_dict["stride"]
                target_param = out_param["name"]
                param_index = get_parameter_offset(target_param, output_dict["parameters"])
                start_time = input_dict["values"][i]
                end_time = input_dict["values"][i+1]
                start_point = (input_dict["values"][i], output_dict["values"][i * out_stride + param_index])
                end_point = (input_dict["values"][i+1], output_dict["values"][i * (out_stride) + out_stride + param_index])

                control_point_1 = (source_dict["OUT_TANGENT"]["values"][param_index * i * 2], source_dict["OUT_TANGENT"]["values"][param_index * i *2 + 1])
                control_point_2 = (source_dict["IN_TANGENT"]["values"][param_index * i * 2 + 2],source_dict["IN_TANGENT"]["values"][param_index * i * 2 + 3])

                target_object = animation.channels[c].target.split("/")[0]
                target_translation = animation.channels[c].target.split("/")[1].split(".")[0]

                if target_object not in curves:
                    curves[target_object] = {}
                if target_translation not in curves[target_object]:
                    curves[target_object][target_translation] = {}
                if target_param not in curves[target_object][target_translation]:
                    curves[target_object][target_translation][target_param] = []

                if curve_type == "BEZIER":
                    curve = util.QuadraticBezierCurve(
                        start_point,
                        end_point,
                        control_point_1,
                        control_point_2,
                        start_time,
                        end_time
                    ).to_hermite()
                elif curve_type == "HERMITE":
                    curve = util.QuadraticHermiteCurve(
                        start_point,
                        end_point,
                        control_point_1,
                        control_point_2,
                        start_time,
                        end_time
                    )
                else:
                    raise RuntimeError("Unsupported curve type %s" % curve_type)

                curves[target_object][target_translation][target_param].append(curve)


def evaluate_curve_values(curves):
    d = {}
    for object_name in curves:
        d[object_name] = {}
        for transformation_type in curves[object_name]:
            d[object_name][transformation_type] = {}
            for target_parameter in curves[object_name][transformation_type]:
                d[object_name][transformation_type][target_parameter] = {}

                subtype_dict = d[object_name][transformation_type][target_parameter]
                for c in curves[object_name][transformation_type][target_parameter]:
                    sub_id = len(subtype_dict.keys())
                    curve_dict = subtype_dict[sub_id] = {}
                    curve_dict["start_value"] = c.start_value[1]
                    curve_dict["end_value"] = c.end_value[1]
                    curve_dict["start_time"] = c.start_time
                    curve_dict["end_time"] = c.end_time
                    curve_dict["control_1"] = c.control_1
                    curve_dict["control_2"] = c.control_2
    return d


def compute_tangent_from_vector(p, dt):
    return (p[1] / p[0]) * dt


def compute_tangents_for_translation_vector(xyz_tangent_vector_vector, dt):
    r = []
    for i in xyz_tangent_vector_vector:
        r.append(compute_tangent_from_vector(i, dt))
    return r


class ObjectConverter(object):
    def __init__(self, object_node, object_data, object_name, axis_converter):
        self.axis_converter = axis_converter
        self.object_data = object_data
        self.object_name = object_name
        self.object_node = object_node

    def _extract_translation_key(self, before_key_point_dicts, after_key_point_dicts):
        x, y, z = self.axis_converter.convert(before_key_point_dicts)
        next_x, next_y, next_z = self.axis_converter.convert(after_key_point_dicts)

        value = util.get_all("end_value", x, y, z)
        left_tangent = util.get_all("control_2", x, y, z)
        right_tangent = util.get_all("control_1", next_x, next_y, next_z)

        dt = x["end_time"] - x["start_time"]

        right_tangent = compute_tangents_for_translation_vector(right_tangent, dt)
        left_tangent = compute_tangents_for_translation_vector(left_tangent, dt)

        time = x["end_time"]
        return red.Tr2VectorKey(
            self.object_name,
            value,
            right_tangent,
            left_tangent,
            time,
        )

    def _convert_translation(self, curve_set):
        translation_keys = self.object_node.get_translation_keys()
        if not translation_keys:
            return

        default_axis_dict = {
            "end_value": 0.0,
            "end_time": 0.0,
            "control_1": (1.0, 0.0),
            "control_2": (1.0, 0.0),
            }
        start_values = self.object_node.axis_translations[0][1]
        end_values = start_values[:]
        start_tangents = [0.0, 0.0, 0.0]
        end_tangents = [0.0, 0.0, 0.0]
        length = 0

        vector_keys = []
        for translation_key in translation_keys:
            if translation_key not in self.object_data:
                continue
            object_location_dict = self.object_data[translation_key]

            keys = []
            for ok in object_location_dict.keys():
                ov = object_location_dict[ok]
                first = ov[ov.keys()[0]]
                last = ov[ov.keys()[-1]]
                length = last["end_time"] - first["start_time"]
                start_value = first["start_value"]
                end_value = last["end_value"]
                start_tangent = compute_tangent_from_vector(first["control_1"], first["end_time"])
                end_tangent = compute_tangent_from_vector(last["control_2"], first["start_time"])
                start_time = first["start_time"]
                keys = ov.keys()

                start_values[axis_to_index(ok)] = start_value
                end_values[axis_to_index(ok)] = end_value
                start_tangents[axis_to_index(ok)] = start_tangent
                end_tangents[axis_to_index(ok)] = end_tangent

            for i, key in enumerate(keys[:-1]):
                next_key = keys[i+1]
                x = y = z = next_x = next_y = next_z = default_axis_dict.copy()
                before_key_point = [x,y,z]
                after_key_point = [next_x, next_y, next_z]

                for ok in object_location_dict.keys():
                    current = self.object_data[translation_key][ok][key]
                    if next_key not in self.object_data[translation_key][ok]:
                        continue
                    next = self.object_data[translation_key][ok][next_key]
                    index = axis_to_index(ok)
                    before_key_point[index] = current
                    after_key_point[index] = next

                vector_key = self._extract_translation_key(before_key_point, after_key_point)
                vector_keys.append(vector_key)

        start_values = self.axis_converter.convert(start_values)
        end_values = self.axis_converter.convert(end_values)
        start_tangents = self.axis_converter.convert(start_tangents)
        end_tangents = self.axis_converter.convert(end_tangents)

        vector_curve = red.Tr2VectorCurve(self.object_name, start_time, length, start_values, end_values, start_tangents, end_tangents)
        vector_curve.keys = vector_keys
        curve_set.curves.append(vector_curve)

    def _convert_axis_rotation(self, axis_key, curve_name):
        if axis_key not in self.object_data:
            return None

        if 'ANGLE' not in self.object_data[axis_key]:
            raise RuntimeError('Could not find angle data for axis key "%s"' % format(axis_key))

        curve_data = self.object_data[axis_key]['ANGLE']

        if not curve_data:
            return None

        curve_values = curve_data.values()
        start_value = math.radians(curve_values[0]["start_value"])

        start_time = curve_values[0]["start_time"]
        end_time = curve_values[-1]["end_time"]
        length = end_time - start_time

        first = curve_values[0]
        last = curve_values[-1]

        curve = red.Tr2ScalarCurve(
            curve_name,
            start_time,
            length,
            start_value,
            math.radians(curve_values[-1]["end_value"]),
            compute_tangent_from_vector(first["control_1"], first["end_time"]),
            compute_tangent_from_vector(last["control_2"], last["end_time"]),
        )
        for i, current in enumerate(curve_values[:-1]):
            next = curve_values[i + 1]
            key = red.Tr2ScalarKey(
                current["end_time"],
                math.radians(current["end_value"]),
                compute_tangent_from_vector((current["control_2"][0], math.radians(current["control_2"][1])), current["end_time"] - current["start_time"]),
                compute_tangent_from_vector((next["control_1"][0], math.radians(next["control_1"][1])), next["end_time"] - next["start_time"]),
            )
            curve.scalar_keys.append(key)
        return curve

    def _convert_rotation(self, curve_set):
        yaw = self._convert_axis_rotation(self.axis_converter.yaw_key, "yawCurve")
        pitch = self._convert_axis_rotation(self.axis_converter.pitch_key, "pitchCurve")
        roll = self._convert_axis_rotation(self.axis_converter.roll_key, "rollCurve")

        if yaw or pitch or roll:
            euler_rotation = red.Tr2EulerRotation(self.object_name, yaw, pitch, roll)
            curve_set.curves.append(euler_rotation)

    def convert_object(self):
        curve_set = red.TriCurveSet(self.object_name)
        self._convert_translation(curve_set)
        self._convert_rotation(curve_set)
        return curve_set


def _read_axis_keys_from_nodes(axis_converter, nodes):
    for n in nodes:
        xyz = [None, None, None]
        for i in xrange(3):
            if nodes[n].axis_rotations[i] is not None:
                xyz[i] = nodes[n].axis_rotations[i][0]
        converted_xyz = axis_converter.convert(xyz)
        axis_converter.update_rotation_keys(converted_xyz)


def convert_object(curve_values, nodes, object_name, axis_converter):
    object_data = curve_values[object_name]
    object_node = nodes[object_name]
    converter = ObjectConverter(object_node, object_data, object_name, axis_converter)
    curve_set = converter.convert_object()
    return curve_set


def convert_file(source_file, target_file):
    collada_instance = colladamunge.get_collada_instance_for_file(source_file)
    animations = colladamunge.rip_animations_from_collada_instance(collada_instance)
    nodes = colladamunge.get_object_id_to_node_dict(collada_instance)

    source_axis_name = colladamunge.get_up_axis(collada_instance)
    source_axis = axis.get_axis_object_from_name(source_axis_name)
    target_axis = axis.Axes.Y_UP
    axis_converter = axis.AxisConverter(source_axis, target_axis)

    _read_axis_keys_from_nodes(axis_converter, nodes)

    curves = {}
    for a in animations:
        read_curve_data_from_animation(a, curves)

    curve_values = evaluate_curve_values(curves)

    space_scene = red.EveSpaceScene()
    for object_name in curve_values.keys():
        curve_set = convert_object(curve_values, nodes, object_name, axis_converter)
        space_scene.curve_sets.append(curve_set)

    with open(target_file, 'w') as f:
        f.write(str(space_scene))


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(DESCRIPTION),
        epilog="It's simple, really.",
    )
    parser.add_argument('sourcefile')
    parser.add_argument('targetfile')
    args = parser.parse_args()
    target_dir = os.path.dirname(args.targetfile)
    if not os.path.exists(os.path.abspath(target_dir)):
        sys.stderr.write("The target directory \"%s\" does not exist" % target_dir)
        sys.exit(1)
    convert_file(args.sourcefile, args.targetfile)

if __name__ == '__main__':
    main()
