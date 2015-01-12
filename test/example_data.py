

from dae_to_red import colladamunge

test_file = """<?xml version="1.0" encoding="utf-8"?>
<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
  <library_images/>
  <library_geometries>
    <geometry id="Cube_001-mesh" name="Cube.001">
      <mesh>
        <source id="Cube_001-mesh-positions">
          <float_array id="Cube_001-mesh-positions-array" count="24">-1 -1 -1 -1 1 -1 1 1 -1 1 -1 -1 -1 -1 1 -1 1 1 1 1 1 1 -1 1</float_array>
          <technique_common>
            <accessor source="#Cube_001-mesh-positions-array" count="8" stride="3">
              <param name="X" type="float"/>
              <param name="Y" type="float"/>
              <param name="Z" type="float"/>
            </accessor>
          </technique_common>
        </source>
        <source id="Cube_001-mesh-normals">
          <float_array id="Cube_001-mesh-normals-array" count="36">-1 0 0 0 1 0 1 0 0 0 -1 0 0 0 -1 0 0 1 -1 0 0 0 1 0 1 0 0 0 -1 0 0 0 -1 0 0 1</float_array>
          <technique_common>
            <accessor source="#Cube_001-mesh-normals-array" count="12" stride="3">
              <param name="X" type="float"/>
              <param name="Y" type="float"/>
              <param name="Z" type="float"/>
            </accessor>
          </technique_common>
        </source>
        <vertices id="Cube_001-mesh-vertices">
          <input semantic="POSITION" source="#Cube_001-mesh-positions"/>
        </vertices>
        <polylist count="12">
          <input semantic="VERTEX" source="#Cube_001-mesh-vertices" offset="0"/>
          <input semantic="NORMAL" source="#Cube_001-mesh-normals" offset="1"/>
          <vcount>3 3 3 3 3 3 3 3 3 3 3 3 </vcount>
          <p>4 0 5 0 1 0 5 1 6 1 2 1 6 2 7 2 3 2 7 3 4 3 0 3 0 4 1 4 2 4 7 5 6 5 5 5 0 6 4 6 1 6 1 7 5 7 2 7 2 8 6 8 3 8 3 9 7 9 0 9 3 10 0 10 2 10 4 11 7 11 5 11</p>
        </polylist>
      </mesh>
    </geometry>
  </library_geometries>
  <library_animations>
    <animation id="Cube_location_X">
      <source id="Cube_location_X-input">
        <float_array id="Cube_location_X-input-array" count="4">0.04166662 0.8333333 5.458333 9.875</float_array>
        <technique_common>
          <accessor source="#Cube_location_X-input-array" count="4" stride="1">
            <param name="TIME" type="float"/>
          </accessor>
        </technique_common>
      </source>
      <source id="Cube_location_X-output">
        <float_array id="Cube_location_X-output-array" count="4">0.03813225 0.03813225 0.03813225 0.03813225</float_array>
        <technique_common>
          <accessor source="#Cube_location_X-output-array" count="4" stride="1">
            <param name="X" type="float"/>
          </accessor>
        </technique_common>
      </source>
      <source id="Cube_location_X-interpolation">
        <Name_array id="Cube_location_X-interpolation-array" count="4">BEZIER BEZIER BEZIER BEZIER</Name_array>
        <technique_common>
          <accessor source="#Cube_location_X-interpolation-array" count="4" stride="1">
            <param name="INTERPOLATION" type="name"/>
          </accessor>
        </technique_common>
      </source>
      <source id="Cube_location_X-intangent">
        <float_array id="Cube_location_X-intangent-array" count="8">-0.2674091 0.03813225 0.5242576 0.03813225 3.65268 0.03813225 8.150683 0.03813225</float_array>
        <technique_common>
          <accessor source="#Cube_location_X-intangent-array" count="4" stride="2">
            <param name="X" type="float"/>
            <param name="Y" type="float"/>
          </accessor>
        </technique_common>
      </source>
      <source id="Cube_location_X-outtangent">
        <float_array id="Cube_location_X-outtangent-array" count="8">0.3507424 0.03813225 2.378712 0.03813225 7.182651 0.03813225 11.59932 0.03813225</float_array>
        <technique_common>
          <accessor source="#Cube_location_X-outtangent-array" count="4" stride="2">
            <param name="X" type="float"/>
            <param name="Y" type="float"/>
          </accessor>
        </technique_common>
      </source>
      <sampler id="Cube_location_X-sampler">
        <input semantic="INPUT" source="#Cube_location_X-input"/>
        <input semantic="OUTPUT" source="#Cube_location_X-output"/>
        <input semantic="INTERPOLATION" source="#Cube_location_X-interpolation"/>
        <input semantic="IN_TANGENT" source="#Cube_location_X-intangent"/>
        <input semantic="OUT_TANGENT" source="#Cube_location_X-outtangent"/>
      </sampler>
      <channel source="#Cube_location_X-sampler" target="Cube/location.X"/>
    </animation>
  </library_animations>
  <library_controllers/>
  <library_visual_scenes>
    <visual_scene id="Scene" name="Scene">
      <node id="Cube" name="Cube" type="NODE">
        <translate sid="location">0.03813227 -0.00892112 0.429184</translate>
        <rotate sid="rotationZ">0 0 1 0</rotate>
        <rotate sid="rotationY">0 1 0 0</rotate>
        <rotate sid="rotationX">1 0 0 0</rotate>
        <scale sid="scale">1 1 1</scale>
        <instance_geometry url="#Cube_001-mesh"/>
      </node>
    </visual_scene>
  </library_visual_scenes>
  <scene>
    <instance_visual_scene url="#Scene"/>
  </scene>
</COLLADA>
"""

def get_sources():
    return {
        "Cube_location_X-intangent": colladamunge.Source(
            "Cube_location_X-intangent",
            "technique_common",
            4,
            2,
            [{'type': 'float', 'name': 'X'}, {'type': 'float', 'name': 'Y'}],
            [-0.2674091, 0.03813225, 0.5242576, 0.03813225, 3.65268, 0.03813225, 8.150683, 0.03813225]
        ),
        "Cube_location_X-output": colladamunge.Source(
            "Cube_location_X-output",
            "technique_common",
            4,
            1,
            [{'type': 'float', 'name': 'X'}],
            [0.03813225, 0.03813225, 0.03813225, 0.03813225],
            ),
        "Cube_location_X-input": colladamunge.Source(
            "Cube_location_X-input",
            "technique_common",
            4,
            1,
            [{'type': 'float', 'name': 'TIME'}],
            [0.04166662, 0.8333333, 5.458333, 9.875]
        ),
        "Cube_location_X-interpolation": colladamunge.Source(
            "Cube_location_X-interpolation",
            "technique_common",
            4,
            1,
            [{'type': 'name', 'name': 'INTERPOLATION'}],
            ['BEZIER', 'BEZIER', 'BEZIER', 'BEZIER']
        ),
        "Cube_location_X-outtangent": colladamunge.Source(
            "Cube_location_X-outtangent",
            "technique_common",
            4,
            2,
            [{'type': 'float', 'name': 'X'}, {'type': 'float', 'name': 'Y'}],
            [0.3507424, 0.03813225, 2.378712, 0.03813225, 7.182651, 0.03813225, 11.59932, 0.03813225],
            ),
        }

def get_channels():
    return  {
        "#Cube_location_X-sampler": colladamunge.Channel("#Cube_location_X-sampler", "Cube/location.X")
    }

def get_samplers():
    sampler_inputs = [
        colladamunge.Input("INPUT", "Cube_location_X-input"),
        colladamunge.Input("OUTPUT", "Cube_location_X-output"),
        colladamunge.Input("INTERPOLATION", "Cube_location_X-interpolation"),
        colladamunge.Input("IN_TANGENT", "Cube_location_X-intangent"),
        colladamunge.Input("OUT_TANGENT", "Cube_location_X-outtangent"),
        ]
    return [colladamunge.Sampler(sampler_inputs)]

def get_animations():
    return []