import unittest
import piqueserver.scripts.blockinfo as blockinfo
from unittest.mock import Mock


class TestBlockinfo(unittest.TestCase):
    def test_grief_check1(self):
        connection = Mock()
        connection.colors = True
        connection.protocol = Mock()
        connection.protocol.players = {123:"Jerry"}

        self.assertRaises(ValueError,blockinfo.grief_check,connection,"#123",minutes=-10)
