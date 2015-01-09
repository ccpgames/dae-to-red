

import collada


class Animation(object):
    def __init__(self, sources, channels, samplers, animations):
        self.sources = sources # array and accessor. Input.
        self.channels = channels # Output
        self.samplers = samplers # Connects a semantic to a source, (tells us how to interpret them).
        self.animations = animations # Child animations if we have any.

    def __eq__(self, other):
        return (    self.sources == other.sources  and
                    self.channels == other.channels and
                    self.samplers == other.samplers and
                    self.animations == other.animations  )


class Channel(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __eq__(self, other):
        return (    self.source == other.source  and
                    self.target == other.target  )


class Source(object):
    def __init__(self, id, type, count, stride, parameters, values):
        self.id = id
        self.type = type
        self.count = count
        self.stride = stride
        self.parameters = parameters
        self.values = values

    def __repr__(self):
        return """
        Source:
        {
            id: {id}
            type: {type}
            count: {count}
            stride: {stride}
            parameters: {parameters}
            values: {values}
        }
        """.format(
            id=self.id,
            type=self.type,
            count=self.count,
            stride=self.stride,
            parameters=self.parameters,
            values=self.values,
            )

    def __eq__(self, other):
        return (  self.id == other.id and
                  self.type == other.type and
                  self.count == other.count and
                  self.stride == other.stride and
                  self.parameters == other.parameters and
                  self.values == other.values  )


class Sampler(object):
    def __init__(self, inputs):
        self.inputs = inputs

    def __eq__(self, other):
        return self.inputs == other.inputs


class Input(object):
    def __init__(self, semantic, source_id):
        self.semantic = semantic
        self.source_id = source_id

    def __eq__(self, other):
        return (    self.semantic == other.semantic and
                    self.source_id == other.source_id   )


def _get_tag(element):
    return element.tag.split('}')[1]


def _parse_channel(channel_node):
    return Channel(channel_node.get("source"), channel_node.get("target"))


def _parse_source(source_node):
    source_id = source_node.get("id")
    parameters = []
    for source_child in source_node.getchildren():
        child_tag = _get_tag(source_child)
        if child_tag.endswith('Name_array'):
            values = source_child.text.rstrip().split(' ')
        elif child_tag.endswith('float_array'):
            line_split_array = [i for i in source_child.text.rstrip().splitlines()]
            line_and_space_split_array = []
            for i in line_split_array:
                if not i:
                    continue
                floats = i.split(' ')
                for j in floats:
                    line_and_space_split_array.append(float(j.strip()))

            values = line_and_space_split_array
        elif child_tag.endswith('technique_common'):
            accessor = source_child.getchildren()[0]
            accessor_tag = _get_tag(accessor)
            if accessor_tag != 'accessor':
                raise RuntimeError("Expected accessor element, got %s" % accessor_tag)
            count = int(accessor.get("count"))
            stride = accessor.get("stride")

            params = accessor.getchildren()
            for p in params:
                param = {
                    "name": p.get("name"),
                    "type": p.get("type"),
                }
                parameters.append(param)

            if stride is None:
                stride = 1
            else:
                stride = int(stride)
    return Source(source_id, child_tag, count, stride, parameters, values)


def _parse_sampler(sampler_node):
    inputs = []
    for input_element in sampler_node.getchildren():
        input_tag = _get_tag(input_element)
        if input_tag != "input":
            raise RuntimeError("Expected input element, got %s" % input_tag)
        inputs.append(Input(input_element.get("semantic"), input_element.get("source")[1:]))
    return Sampler(inputs)


def _parse_animation(animation_node):
    sources = {}
    channels = {}
    samplers = []
    animations = []
    for animation_child in animation_node.getchildren():
        animation_child_tag = _get_tag(animation_child)
        if animation_child_tag == 'channel':
            channel = _parse_channel(animation_child)
            channels[channel.source] = channel
        elif animation_child_tag == "source":
            source = _parse_source(animation_child)
            sources[source.id] = source
        elif animation_child_tag == "sampler":
            samplers.append(_parse_sampler(animation_child))
        elif animation_child_tag == "animation":
            animations.append(_parse_animation(animation_child))
        else:
            raise RuntimeError("Unexpected child element of animation: '%s'" % animation_child)
    return Animation(sources, channels, samplers, animations)


def get_collada_instance_for_file(f):
    return collada.Collada(f)


def rip_animations_from_collada_instance(collada_instance):
    animations = []
    for animation_node in collada_instance.animations:
        animations.append(_parse_animation(animation_node.xmlnode))
    return animations


class Node(object):
    def __init__(self):
        self.axis_rotations = [None, None, None]
        self.axis_translations = []

    def __repr__(self):
        return "Node: " + str(self.axis_rotations) + " " + str(self.axis_translations)

    def get_translation_keys(self):
        return [i[0] for i in self.axis_translations]

    def get_rotation_keys(self):
        return [i[0] for i in self.axis_rotations]


def get_axis_index(axis_list):
    for i, n in enumerate(axis_list):
        if n == 1.0:
            return i
        elif n == 0.0:
            pass
        else:
            raise RuntimeError("Not a coordinate system axis \"%s\"" % axis_list)


def get_object_id_to_node_dict(collada_instance):
    nodes = {}
    for scene in collada_instance.scenes:
        scene_children = scene.xmlnode.getchildren()
        for scene_child in scene_children:
            scene_child_tag = _get_tag(scene_child)
            if scene_child_tag == 'node':
                node = scene_child
                node_id = node.get("id")
                current_node =  nodes.setdefault(node_id, Node())
                for node_child in node.getchildren():
                    node_child_sid = node_child.get("sid")
                    node_child_tag = _get_tag(node_child)
                    node_child_elements = [ float(i) for i in node_child.text.rstrip().split(" ") if i != "" ]
                    if node_child_tag == "rotate":
                        rotation_axis_index = get_axis_index(node_child_elements)
                        rot_x, rot_y, rot_z, rot_angle = node_child_elements
                        current_node.axis_rotations[rotation_axis_index] = (node_child_sid, rot_angle)
                    elif node_child_tag == "translate":
                        current_node.axis_translations.append((node_child_sid, node_child_elements))
    return nodes


def get_up_axis(collada_instance):
    return collada_instance.assetInfo.upaxis