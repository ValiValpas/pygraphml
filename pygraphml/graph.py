# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from . import Node
from . import Edge
from . import Hyperedge

from collections import deque

class Graph:
    """
    Main class which represent a Graph

    :param name: name of the graph
    """

    def __init__(self, name="", parent=None):
        """
        """

        self.name = name

        self._nodes = []
        self._edges = []
        self._hyperedges = []
        self._root = None
        self._parent_node = parent
        self.directed = True

        self.i = 0
        
    def parent_graph(self, ):
        if self._parent_node is None:
            return None
        else:
            return self._parent_node.graph()
    
    def parent_node(self, ):
        return self._parent_node

    def sort(self, edges=None):
        """
        Implement Kahn's algorithm, which returns a topological sort.

        :param edges: edges that are used for traversal
        :return: list of nodes or None if graph is not a DAG
        """

        result = list()
        start_nodes = list()
        if edges is None:
            edges = list(self._edges)

        # initialise start nodes
        for n in self.nodes():
            if len(n.inedges()) == 0:
                start_nodes.append(n)

        while len(start_nodes) > 0:
            n = start_nodes.pop()
            result.append(n)

            # iterate target nodes
            for e in n.outedges():
                # remove edge (virtually)
                if e in edges:
                    edges.remove(e)

                indegree = 0
                for f in e.target().inedges():
                    if f in edges:
                        indegree += 1

                # if the target node has no other incoming edge
                if indegree == 0:
                    start_nodes.append(e.target())

        if len(edges) > 0:
            # graph has at least one cycle
            return None

        return result

    def DFS_prefix(self, root=None):
        """
        Depth-first search.

        .. seealso::
           `Wikipedia DFS descritpion <http://en.wikipedia.org/wiki/Depth-first_search>`_

        :param root: first to start the search
        :return: list of nodes
        """

        if not root:
            root = self._root

        return self._DFS_prefix(root)

    def _DFS_prefix(self, n):
        """
        """

        nodes = [n]
        n['depth'] = self.i

        for c in n.targets():
            nodes += self._DFS_prefix(c, n)
            self.i += 1

        return nodes

    def BFS(self, root=None):
        """
        Breadth-first search.

        .. seealso::
           `Wikipedia BFS descritpion <http://en.wikipedia.org/wiki/Breadth-first_search>`_

        :param root: first to start the search
        :return: list of nodes


        """

        if not root:
            root = self.root()

        queue = deque()
        queue.append(root)

        nodes = []

        while len(queue) > 0:
            x = queue.popleft()
            nodes.append(x)

            for out in x.targets():
                queue.append(out)

        return nodes

    def get_depth(self, node):
        """
        """

        depth = 0
        while node.sources() and node != self.root():
            node = node.sources()[0]
            depth += 1

        return depth

    def nodes(self, ):
        """
        """

        return self._nodes

    def edges(self, ):
        """
        """

        return self._edges

    def outedges(self, node):
        """
        """

        return node.outedges()

    def hyperedges(self, ):
        return self._hyperedges

    def targets(self, node):
        """
        """

        return node.targets()

    def add_node(self, nid=""):
        """
        """

        n = Node(self)
        n['id'] = nid
        self._nodes.append(n)
        
        if self.parent_graph() is not None:
            self.parent_graph().nodes().append(n)

        return n

    def add_edge(self, n1, n2, directed=False):
        """
        """

        if n1 not in self._nodes:
            raise Test("fff")
        if n2 not in self._nodes:
            raise Test("fff")

        e = Edge(n1, n2, directed)
        self._edges.append(e)

        return e

    def add_edge_by_id(self, id1, id2):
        """
        """

        n1 = None
        n2 = None

        for n in self._nodes:
            if n['id'] == id1:
                n1 = n
            if n['id'] == id2:
                n2 = n

        if n1 and n2:
            return self.add_edge(n1, n2)
        else:
            return

    def add_hyperedge(self):
        h = Hyperedge()
        self._hyperedges.append(h)
        return h

    def add_endpoint_by_id(self, hyperedge, id1, direction=None):
        for n in self._nodes:
            if n['id'] == id1:
                hyperedge.add_endpoint(n, direction)
                return n

    def set_root(self, node):
        """
        """

        self._root = node

    def root(self):
        """
        """

        return self._root

    def set_root_by_attribute(self, value, attribute='id'):
        """
        """

        for n in self.nodes():
            if n[attribute] in value:
                self.set_root(n)
                return n

    def get_node_attributes(self):
        """
        """

        attr = []
        attr_obj = []
        for n in self.nodes():
            for a in n.attr:
                if a not in attr:
                    attr.append(a)
                    attr_obj.append(n.attr[a])

        return attr_obj

    def get_edge_attributes(self):
        """
        """

        attr = []
        attr_obj = []
        for e in self.edges():
            for a in e.attr:
                if a not in attr:
                    attr.append(a)
                    attr_obj.append(e.attr[a])

        return attr_obj

    def show(self, show_label=False):
        """
        """

        import matplotlib

        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.Graph()

        for n in self._nodes:
            if show_label:
                n_id = n['id']
            else:
                n_id = n.id
            G.add_node(n_id)

        for e in self._edges:
            if show_label:
                n1_id = e.node1['id']
                n2_id = e.node2['id']
            else:
                n1_id = e.node1.id
                n2_id = e.node2.id
            G.add_edge(n1_id, n2_id)

        nx.draw(G)

        if show_label:
            nx.draw_networkx_labels(G, pos=nx.spring_layout(G))

        plt.show()

class NoDupesGraph(Graph):
    '''Add nodes without worrying if it is a duplicate.
       Add edges without worrying if nodes exist   '''

    def __init__(self,*args,**kwargs):
        Graph.__init__(self,*args,**kwargs)
        self._nodes = {}

    def nodes(self):
        return self._nodes.values()

    def add_node(self,nid):
      '''Return a node with id. Create node if id is new'''
      try:
          n = self._nodes[nid]
      except KeyError:
          n = Node()
          n['id'] = nid
          self._nodes[nid]=n
      return n

    def add_edge(self, n1_id, n2_id,directed=False):
      """
      Get or create edges using get_or_create_node
      """
      n1 = self.add_node(n1_id)
      n2 = self.add_node(n2_id)
      e = Edge(n1, n2, directed)
      self._edges.append(e)
      return e

    def flush_empty_nodes(self):
        '''not implemented'''
        pass

    def condense_edges(self):
        '''if a node connects to only two edges, combine those
        edges and delete the node.

        not implemented
        '''
        pass

if __name__ == '__main__':

    import GraphMLParser
    parser = GraphMLParser.GraphMLParser()
    import random
    import timeit

    def no_dupes_test():
     graph = NoDupesGraph()
     n0 = graph.add_node(nid='first')
     for x in range (20000):
        x = str(random.random())
        n1 = graph.add_node(nid=x)
        graph.add_edge(n0['id'],n1['id'])
        n0=n1
     #parser.write(graph,'/dev/null')

    def vanilla_graph_test():
     graph = Graph()
     n0 = graph.add_node(nid='first')
     for x in range (20000):
        x = str(random.random())
        n1 = graph.add_node(nid=x)
        graph.add_edge(n0,n1)
        n0=n1
     #parser.write(graph,'/dev/null')

    number = 5
    print("No Dupes Test: ")
    print('  %s'.format(timeit.timeit('no_dupes_test()',setup='from __main__ import no_dupes_test',number=number)))

    print("Vanilla Graph Test: ")
    print('  %s'.format(timeit.timeit('vanilla_graph_test()',setup='from __main__ import vanilla_graph_test', number=number)))
