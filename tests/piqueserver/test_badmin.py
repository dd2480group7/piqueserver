import unittest
import piqueserver.scripts.badmin as badmin
from unittest.mock import Mock


class TestBadmin(unittest.TestCase):
    def test_score_grief1(self):
        connection = Mock()
        connection.colors = True
        connection.protocol.players = []

        player = Mock()

        self.assertRaises(ValueError,badmin.score_grief,connection,player,time=-10)

    def test_score_grief2(self):
        connection = Mock()
        connection.colors = True
        connection.protocol.players = []

        player = Mock()
        player.blocks_removed = []
        player.name = "Jerry"
        player.team_id = 123

        self.assertEqual(0,badmin.score_grief(connection,player))

    def test_score_grief3(self):
        connection = Mock()
        connection.colors = True
        connection.protocol.players = []

        player = Mock()
        player.blocks_removed = [[110,None]]
        player.name = "Jerry"
        player.team.id = 123
        badmin.reactor = Mock()

        def returnZero():
            return 0

        badmin.reactor.seconds = returnZero

        self.assertEqual(0,badmin.score_grief(connection,player,time=1))
