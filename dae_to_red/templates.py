eve_space_scene = """type: EveSpaceScene"""

curve_set_header = """
-   type: TriCurveSet
    name: "{object_name}_curve_set"
    curves:"""

rotation_curve_header = """
        {curve_type}:
            type: Tr2ScalarCurve
            length: {length}
            cycle: 0
            timeScale: 1.0
            startValue: {start_value}
            endValue: {end_value}
            startTangent: {start_tangent}
            endTangent: {end_tangent}
            interpolation: 2
            timeOffset: {time_offset}"""

scalar_key = """
            -   type: Tr2ScalarKey
                value: {value}
                time: {time}
                leftTangent: {left_tangent}
                rightTangent: {right_tangent}
                interpolation: 2"""

vector_key = """
        -   type: Tr2Vector3Key
            time: {time}
            value: {value}
            leftTangent: {left_tangent}
            rightTangent: {right_tangent}
            interpolation: 2"""

location_curve_header = """
    - &location_curve_{object_name}
        type: Tr2Vector3Curve
        name: "{object_name}_location_curve"
        length: {length}
        startValue: {start_value}
        endValue: {end_value}
        startTangent: {start_tangent}
        endTangent: {end_tangent}
        interpolation: 2
        timeOffset: {time_offset}"""

euler_rotation_header = """
    - &euler_rotation_{object_name}
        type: Tr2EulerRotation"""