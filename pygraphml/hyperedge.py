# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from . import Item

class Hyperedge(Item):
    """
    """

    def __init__(self):
        """
        """

        super(Hyperedge, self).__init__()

        self.in_nodes = set()
        self.out_nodes = set()
        self.undir_nodes = set()

    def add_endpoint(self, node, direction=None):
        if direction == "in":
            self.in_nodes.add(node)
        elif direction == "out":
            self.out_nodes.add(node)
        else:
            self.undir_nodes.add(node)

    def sources(self):
        return self.in_nodes

    def targets(self):
        return self.out_nodes

    def endpoints(self):
        nodes = set()
        nodes.update(self.in_nodes)
        nodes.update(self.out_nodes)
        nodes.update(self.undir_nodes)
        return nodes
