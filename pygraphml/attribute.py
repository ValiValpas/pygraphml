# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


class Attribute:
    """
    """

    def __init__(self, name, value):
        """
        """

        self.name = name
        self.value = value

    def set_value(self, value):
        if isinstance(self.value, int):
            self.value = int(value)
        elif isinstance(self.value, str) or isinstance(self.value, unicode):
            self.value = str(value)
        elif isinstance(self.value, float):
            self.value = float(value)
        else:
            raise Exception("Unknown data type %s" % type(self.value))

    def __str__(self):
        """
        """

        s = ""
        s += "%s : %s" % (self.name, str(self.value))
        return s

