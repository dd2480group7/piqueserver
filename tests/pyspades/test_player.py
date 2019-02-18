"""
test pyspades/protocol.py
"""

from twisted.trial import unittest
from pyspades import player, server, contained
from pyspades.team import Team
from unittest.mock import Mock

class BaseConnectionTest(unittest.TestCase):
    def test_repr(self):
        ply = player.ServerConnection(Mock(), Mock())
        repr(ply)

    def test_team_join(self):
        prot = Mock()
        prot.team_class = Team
        server.ServerProtocol._create_teams(prot)
        # Some places still use the old name
        prot.players = {}

        for team in (prot.team_1, prot.team_2, prot.team_spectator):
            ply = player.ServerConnection(prot, Mock())
            ply.spawn = Mock()
            ex_ply = contained.ExistingPlayer()
            ex_ply.team = team.id
            ply.on_new_player_recieved(ex_ply)

            self.assertEqual(ply.team, team)

    #testing first return None
    def test_on_input_data_recieved1(self):
        ply = player.ServerConnection(Mock(), Mock())
        input_ply = contained.InputData()
        self.assertEqual(ply.on_input_data_recieved(input_ply), None)

    #testing change of jump due to velocity
    def test_on_input_data_recieved2(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.world_object.velocity = Mock()
        ply.world_object.velocity.z = 1
        ply.set_hp(10)
        ply.player_id = 1
        input_ply = contained.InputData()
        input_ply.jump = True

        self.assertTrue(input_ply.jump)
        ply.on_input_data_recieved(input_ply)
        self.assertFalse(input_ply.jump) #should have changed to false due to velocity
        ply.on_input_data_recieved(input_ply)

    #testing last return None
    def test_on_input_data_recieved3(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.filter_visibility_data = True
        ply.world_object = Mock()
        ply.freeze_animation = True
        ply.set_hp(10)
        ply.player_id = 1
        input_ply = contained.InputData()
        self.assertEqual(ply.on_input_data_recieved(input_ply), None)

    def test_on_position_update_received2(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.set_hp(10)
        ply.player_id = 1
        ply.last_position_update = 1
        input_ply = contained.PositionData()
        ply.x = 1
        ply.y = 2
        ply.z = 3
        self.assertFalse(ply.on_position_update_recieved(input_ply), None)  # Since we've updated position, this should be false.

    #Inverse of above tests, last_position_update is None here
    def test_on_position_update_received3(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.set_hp(10)
        input_ply = contained.PositionData()
        ply.x = 1
        ply.y = 2
        ply.z = 3
        self.assertEqual(ply.on_position_update_recieved(input_ply), None)  # Since we've not updated position, this should be equal.

    #test1 in on position update recieved, Return None
    def test_on_position_update_received1(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.set_hp(10)
        ply.player_id=1
        input_ply = contained.PositionData()
        ply.x = 1
        ply.y = 2
        ply.z = 3
        self.assertEqual(ply.on_position_update_recieved(input_ply), None)
            # tests to set last_position_update to other than default value None




