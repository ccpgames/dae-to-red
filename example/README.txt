This folder contains example Blender and Maya files to show a simple scene containing three drones.
They are intended to demonstrate the workflow,

How to run the example scene:
1. Install the dae-to-red package.
2. Export a .collada file from Blender or Maya (or use one of the pre-exported ones)
3. Run the conversion command "dae_to_red" on one of the exported .dae files like so:

$>dae_to_red Blender\example.dae example.red

4. Copy the resulting .red file into %SHAREDCACHE%\probe\res\curves
5. Copy example_scene.yaml into %SHAREDCACHE%\probe\res\sequences
6. Navigate to %SHAREDCACHE%\probe and start the probe from the command line like so:

$>bin\exefile.exe /lib=code.ccp /scenes=example_scene.yaml

You should see three drones, each moving along and spinning clockwise around an axis, and then stopping.