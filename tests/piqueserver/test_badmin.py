import unittest
import piqueserver.scripts.badmin as badmin
from unittest.mock import Mock


class TestBadmin(unittest.TestCase):
    # Requires time to be positive
    def test_score_grief1(self):
        connection = Mock()
        connection.colors = True
        connection.protocol.players = []

        player = Mock()

        self.assertRaises(ValueError,badmin.score_grief,connection,player,time=-10)

    # Give grief score to player
    def test_score_grief2(self):
        connection = Mock()
        connection.colors = True
        connection.protocol.players = []

        player = Mock()
        player.blocks_removed = []
        player.name = "Jerry"
        player.team_id = 123

        self.assertEqual(0,badmin.score_grief(connection,player))

    # Give grief score to player - blocks destroyed
    def test_score_grief3(self):
        connection = Mock()
        connection.colors = True
        connection.protocol.players = []

        player = Mock()

        block = ("Name",123)

        player.blocks_removed = [[110,block]]
        player.name = "Jerry"
        player.team.id = 123
        badmin.reactor = Mock()

        def returnZero():
            return 0

        badmin.reactor.seconds = returnZero

        self.assertEqual(6,badmin.score_grief(connection,player,time=1))
