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

    def test_grief_check2(self):
        connection = Mock()
        connection.colors = True
        connection.protocol = Mock()
        connection.protocol.players = {124:"Jerry"} # Wrong id/name for Jerry here

        self.assertRaises(CommandError,blockinfo.grief_check,connection,"#123",minutes=123)

    def test_grief_check3(self):
        connection = Mock()
        connection.colors = []

        player = Mock()
        player.__str__ = "name"
        player.blocks_removed = []
        player.name = "Jacob"
        player.last_switch = 0
        player.teamkill_times = [124]
        player.team.id = "Team Edward"
        player.team.name = "Team Edward"


        def seconds():
            return 0

        blockinfo.seconds = seconds

        connection.protocol.players = ["",player]
        self.assertEqual(blockinfo.grief_check(connection,"#1",minutes=123),"Jacob removed no blocks in the last 123.0 minutes. Jacob joined Team Edward team less than a second ago, and killed 1 teammates in the last 123.0 minutes.")
