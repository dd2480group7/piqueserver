import unittest
import piqueserver.scripts.blockinfo as blockinfo
from piqueserver.commands import CommandError
from unittest.mock import Mock


class TestBlockinfo(unittest.TestCase):
    def test_grief_check1(self):
        connection = Mock()
        connection.colors = True
        connection.protocol = Mock()
        connection.protocol.players = {123:"Jerry"}

        self.assertRaises(ValueError,blockinfo.grief_check,connection,"#123",minutes=-10) # Minutes less than 0

class TestBlockinfo(unittest.TestCase):
    def test_grief_check1(self):
        connection = Mock()
        connection.colors = True
        connection.protocol = Mock()
        connection.protocol.players = {124:"Jerry"} # Wrong id/name for Jerry here

        self.assertRaises(CommandError,blockinfo.grief_check,connection,"#123",minutes=123)
