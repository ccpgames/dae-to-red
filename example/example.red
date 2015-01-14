type: EveSpaceScene
curveSets:
-   type: TriCurveSet
    name: "Right_curve_set"
    curves:
    - &location_curve_Right
        type: Tr2Vector3Curve
        name: "Right_location_curve"
        length: 9.95833338
        startValue: [5.0, 0.0, 0.0]
        endValue: [5.0, 10.0, 0.0]
        startTangent: [0.0, 0.0, 0.0]
        endTangent: [0.0, 0.0, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
    - &euler_rotation_Right
        type: Tr2EulerRotation
        yawCurve:
            type: Tr2ScalarCurve
            length: 9.95833338
            cycle: 0
            timeScale: 1.0
            startValue: 0.0
            endValue: 6.28318530718
            startTangent: 0.0
            endTangent: 0.0
            interpolation: 2
            timeOffset: 0.04166662
-   type: TriCurveSet
    name: "Center_curve_set"
    curves:
    - &location_curve_Center
        type: Tr2Vector3Curve
        name: "Center_location_curve"
        length: 9.95833338
        startValue: [0.0, 0.0, 0.0]
        endValue: [10.0, 0.0, 0.0]
        startTangent: [0.0, 0.0, 0.0]
        endTangent: [0.0, 0.0, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
    - &euler_rotation_Center
        type: Tr2EulerRotation
        pitchCurve:
            type: Tr2ScalarCurve
            length: 9.95833338
            cycle: 0
            timeScale: 1.0
            startValue: 0.0
            endValue: 6.28318530718
            startTangent: 0.0
            endTangent: 0.0
            interpolation: 2
            timeOffset: 0.04166662
-   type: TriCurveSet
    name: "nurbsSphere3_curve_set"
    curves:
    - &location_curve_nurbsSphere3
        type: Tr2Vector3Curve
        name: "nurbsSphere3_location_curve"
        length: 9.95833338
        startValue: [-5.0, 0.0, 0.0]
        endValue: [-5.0, 0.0, 10.0]
        startTangent: [0.0, 0.0, 0.0]
        endTangent: [0.0, 0.0, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
    - &euler_rotation_nurbsSphere3
        type: Tr2EulerRotation
        rollCurve:
            type: Tr2ScalarCurve
            length: 9.95833338
            cycle: 0
            timeScale: 1.0
            startValue: 0.0
            endValue: 6.28318530718
            startTangent: 0.0
            endTangent: 0.0
            interpolation: 2
            timeOffset: 0.04166662
-   type: TriCurveSet
    name: "nurbsSphere2_curve_set"
    curves:
    - &location_curve_nurbsSphere2
        type: Tr2Vector3Curve
        name: "nurbsSphere2_location_curve"
        length: 9.95833338
        startValue: [0.0, 0.0, 0.0]
        endValue: [10.0, 0.0, 0.0]
        startTangent: [0.0, 0.0, 0.0]
        endTangent: [0.0, 0.0, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
    - &euler_rotation_nurbsSphere2
        type: Tr2EulerRotation
        pitchCurve:
            type: Tr2ScalarCurve
            length: 9.95833338
            cycle: 0
            timeScale: 1.0
            startValue: 0.0
            endValue: 6.28318530718
            startTangent: 0.0
            endTangent: 0.0
            interpolation: 2
            timeOffset: 0.04166662
-   type: TriCurveSet
    name: "nurbsSphere1_curve_set"
    curves:
    - &location_curve_nurbsSphere1
        type: Tr2Vector3Curve
        name: "nurbsSphere1_location_curve"
        length: 9.95833338
        startValue: [-0.401735, 0.0, 0.0]
        endValue: [10.0, 5.0, 0.0]
        startTangent: [0.0, -0.12102477222407926, -0.12102477222407926]
        endTangent: [0.9716599158812634, 0.4858299579406317, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
-   type: TriCurveSet
    name: "nurbsSphere4_curve_set"
    curves:
    - &location_curve_nurbsSphere4
        type: Tr2Vector3Curve
        name: "nurbsSphere4_location_curve"
        length: 9.95833338
        startValue: [5.0, 0.0, 0.0]
        endValue: [5.0, 10.0, 0.0]
        startTangent: [0.0, 0.0, 0.0]
        endTangent: [0.0, 0.0, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
    - &euler_rotation_nurbsSphere4
        type: Tr2EulerRotation
        yawCurve:
            type: Tr2ScalarCurve
            length: 9.95833338
            cycle: 0
            timeScale: 1.0
            startValue: 0.0
            endValue: 6.28318530718
            startTangent: 0.0
            endTangent: 0.0
            interpolation: 2
            timeOffset: 0.04166662
-   type: TriCurveSet
    name: "Left_curve_set"
    curves:
    - &location_curve_Left
        type: Tr2Vector3Curve
        name: "Left_location_curve"
        length: 9.95833338
        startValue: [-5.0, 0.0, 0.0]
        endValue: [-5.0, 0.0, 10.0]
        startTangent: [0.0, 0.0, 0.0]
        endTangent: [0.0, 0.0, 0.0]
        interpolation: 2
        timeOffset: 0.04166662
    - &euler_rotation_Left
        type: Tr2EulerRotation
        rollCurve:
            type: Tr2ScalarCurve
            length: 9.95833338
            cycle: 0
            timeScale: 1.0
            startValue: 0.0
            endValue: 6.28318530718
            startTangent: 0.0
            endTangent: 0.0
            interpolation: 2
            timeOffset: 0.04166662