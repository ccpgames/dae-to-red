[![Build Status](https://travis-ci.org/ccpgames/dae-to-red.svg)](https://travis-ci.org/ccpgames/dae-to-red)

# dae-to-red
Extract and convert animation data from Collada files exported from Blender or Maya.
This could enable determined probe users to create their own animated scenes.


# How to use it

1. Create a keyframe animation in Blender or Maya.
2. Export the scene as a Collada file.
3. Run the Python program on the input (.dae) file in order to create an output (.red) file.
4. Place the generated .red file somewhere under **%SHARED_CACHE%\probe\res\** so the Eve Probe can reference it
5. Use the sequencer command **bind_matching_dynamics** to bind the actors to their matching animations. Make sure that the names of the actors in the scene file matches those used in the animation program.

Here is an example scene file where actors are bound to their animation data:
```
name: Example
description: |
  Example scene. Three identical drones are bound to matching curves.
  Note that the names of the objects that are used for the actors in the animation software
  need to match the ones that are used in the scene file.
  The path to the generated file is %SHARED_CACHE%\curves\example_animation.red
commands:
  - [scene, m10]
  - [set_camera_position, [0.0, 1.0, 40.0]]
  - [set_camera_focus, [0.0, 0.0, 0.0]]
  - [actor, left, 'res:/dx9/model/drone/ore/medium/oredm1/oredm1_t1.red']
  - [actor, center, 'res:/dx9/model/drone/ore/medium/oredm1/oredm1_t1.red']
  - [actor, right, 'res:/dx9/model/drone/ore/medium/oredm1/oredm1_t1.red']
  - [set_position, left, [-10, 0, 0]]
  - [set_position, center, [0, 0, 0]]
  - [set_position, right, [10, 0, 0]]
  - [add_actor, left]
  - [add_actor, center]
  - [add_actor, right]
  - [preload_lods]
  - [wait_for_loads]
  - [bind_matching_dynamics, 'res:/curves/example_animation.red']
  - [start_measurement, drone]
  - [sleep, 30]
  - [stop_measurement, drone]
```

Notes:
 - Currently only tested on collada files exported from BLENDER or MAYA.
 - Only extracts location and rotation from objects.
 - Only supports rotation mode XYZ Euler.