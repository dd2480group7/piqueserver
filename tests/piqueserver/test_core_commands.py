from twisted.trial import unittest
from unittest.mock import Mock

from piqueserver import core_commands
import piqueserver.core_commands.movement as Movement


class DummyTest(unittest.TestCase):

    def setup(self):
        conn = Mock()
        conn.protocol = Mock()
    def test_get_ban_argument(self):
        conn = Mock()
        conn.protocol = Mock()
        conn.protocol.default_ban_time = 1423
        dur, reas = core_commands.get_ban_arguments(conn, ["120", "123"])
        self.assertEqual(dur, 120)
        self.assertEqual(reas, "123")

        dur, reas = core_commands.get_ban_arguments(conn, [])
        self.assertEqual(dur, 1423)
        self.assertEqual(reas, None)

        dur, reas = core_commands.get_ban_arguments(conn, ["hi", "you"])
        self.assertEqual(dur, 1423)
        self.assertEqual(reas, "hi you")

        # Does this make sense? Not sure it does
        # This is what the code does atm, anyway
        dur, reas = core_commands.get_ban_arguments(conn, ["perma", "you"])
        self.assertEqual(dur, None)
        self.assertEqual(reas, "you")

    def test_do_movement_params(self):
        '''
        Requirement: ValueError is raised if do_move is called with an erroneous
        amount of parameters.
        '''
        conn = Mock()
        conn.protocol = Mock()
        conn.protocol.map.get_height.return_value = 0
        player = Mock()

        #too many parameters -> should raise ValueError
        with self.assertRaises(ValueError) as e:
            Movement.do_move(conn, [player, 0 , 0, 0, 0])
        self.assertEquals(str(e.exception), "Wrong number of parameters!")

    def test_do_movement_player(self):
        '''
        Requirement: ValueError is raised if do_move is passed a connection-object
        that is not recognized.
        '''
        conn = Mock()
        conn.protocol = Mock()
        conn.protocol.map.get_height.return_value = 0
        conn.protocol.players = []

        #Player not recognized
        with self.assertRaises(ValueError, msg="") as e:
            Movement.do_move(conn, [0, 0, 0])
        self.assertEquals(str(e.exception), "")




