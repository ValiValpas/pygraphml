# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from . import Item

class Node(Item):
    """
    """

    def __init__(self, graph):
        """
        """

        super(Node, self).__init__()

        self._edges = []
        self._graph = graph
        self._child_graph = None
        
    def graph(self):
        return self._graph
        
    def child_graph(self):
        return self._child_graph
    
    def set_child_graph(self, graph):
        self._child_graph = graph

    def edges(self, ):
        """
        """

        return self._edges


    def children(self):
        """
        """

        children = []
        for e in self._edges:
            if e.parent() == self:
                children.append(e.child())

        return children

    def parent(self):
        """
        """

        parent = []
        for e in self._edges:
            if e.child() == self:
                parent.append(e.parent())

        return parent

