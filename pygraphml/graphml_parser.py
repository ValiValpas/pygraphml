# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from xml.dom import minidom

from . import Graph
from . import Node
from . import Edge

class GraphMLParser:
    """
    """

    def __init__(self):
        """
        """

    def write(self, graph, fname):
        """
        """

        doc = minidom.Document()

        root = doc.createElement('graphml')
        doc.appendChild(root)

        # Add attributs
        for a in graph.get_attributs():
            attr_node = doc.createElement('key')
            attr_node.setAttribute('id', a.name)
            attr_node.setAttribute('attr.name', a.name)
            attr_node.setAttribute('attr.type', a.type)
            root.appendChild(attr_node)

        graph_node = doc.createElement('graph')
        graph_node.setAttribute('id', graph.name)
        if graph.directed:
            graph_node.setAttribute('edgedefault', 'directed')
        else:
            graph_node.setAttribute('edgedefault', 'undirected')
        root.appendChild(graph_node)

        # Add nodes
        for n in graph.nodes():

            node = doc.createElement('node')
            node.setAttribute('id', n['label'])
            for a in n.attributes():
                if a != 'label':
                    data = doc.createElement('data')
                    data.setAttribute('key', a)
                    data.appendChild(doc.createTextNode(str(n[a])))
                    node.appendChild(data)
            graph_node.appendChild(node)

        # Add edges
        for e in graph.edges():

            edge = doc.createElement('edge')
            edge.setAttribute('source', e.node1['label'])
            edge.setAttribute('target', e.node2['label'])
            if e.directed() != graph.directed:
                edge.setAttribute('directed', 'true' if e.directed() else 'false')
            for a in e.attributes():
                if e != 'label':
                    data = doc.createElement('data')
                    data.setAttribute('key', a)
                    data.appendChild(doc.createTextNode(e[a]))
                    edge.appendChild(data)
            graph_node.appendChild(edge)

        f = open(fname, 'w')
        f.write(doc.toprettyxml(indent = '    '))
        
    def set_default_keys(self, obj, keytype, keys):
        for key in keys.values():
            if key.getAttribute("for") == keytype:
                default = key.getElementsByTagName("default")[0]
                if default.firstChild:
                    obj[key.getAttribute("id")] = default.firstChild.data
                else:
                    obj[key.getAttribute("id")] = ""
                
    def parse_attributes(self, obj, element):
        for attr in element.childNodes:
            if isinstance(attr, minidom.Element):
                if attr.tagName == "data":
                    if attr.firstChild:
                        obj[attr.getAttribute("key")] = attr.firstChild.data
                    else:
                        obj[attr.getAttribute("key")] = ""
        
    def parse_graph(self, source, target, keys):
        """
        """
        
        graph = source
        g = target

        # Get nodes
        for node in graph.childNodes:
            if isinstance(node, minidom.Element):
                if node.tagName == "node":
                    n = g.add_node(node.getAttribute('id'))
                    self.set_default_keys(n, "node", keys)
                    self.parse_attributes(n, node)
                    
                    # parse subgraph if present
                    elements = node.getElementsByTagName("graph")
                    if elements:
                        name = elements[0].getAttribute('id')
                        n.set_child_graph(Graph(name, n))
                        self.parse_graph(elements[0], n.child_graph(), keys)

        # Get edges
        for edge in graph.childNodes:
            if isinstance(edge, minidom.Element):
                if edge.tagName == "edge":
                    source = edge.getAttribute('source')
                    dest = edge.getAttribute('target')
                    e = g.add_edge_by_label(source, dest)
                    self.set_default_keys(e, "edge", keys)
                    self.parse_attributes(e, edge)


    def parse(self, fname):
        """
        """

        dom = minidom.parse(open(fname, 'r'))
        root = dom.getElementsByTagName("graphml")[0]
        graph = root.getElementsByTagName("graph")[0]
        name = graph.getAttribute('id')

        # Get keys
        keys = dict()
        for key in root.getElementsByTagName("key"):
            keys[key.getAttribute("id")] = key

        g = Graph(name)

        self.parse_graph(graph, g, keys)

        return g


if __name__ == '__main__':

    parser = GraphMLParser()
    g = parser.parse('test.graphml')

    g.show(True)


