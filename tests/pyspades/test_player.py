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

    def test_on_input_data_recieved1(self):
        ply = player.ServerConnection(Mock(), Mock())
        input_cont = contained.InputData()
        self.assertEqual(ply.on_input_data_recieved(input_cont), None) #hp is none
        ply.set_hp(10)
        ply.world_object = Mock()
        ply.world_object.velocity = Mock()
        ply.world_object.velocity.z = 0
        ply.player_id = 1
        input_cont.jump = True

        ply.on_input_data_recieved(input_cont)
        self.assertTrue(input_cont.jump)
        ply.world_object.velocity.z = 1
        ply.on_input_data_recieved(input_cont)
        self.assertFalse(input_cont.jump) #should have changed to false due to velocity

    #testing last return None
    def test_on_input_data_recieved2(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.filter_visibility_data = True
        ply.world_object = Mock()
        ply.freeze_animation = True
        ply.set_hp(10)
        ply.player_id = 1
        input_cont = contained.InputData()
        self.assertEqual(ply.on_input_data_recieved(input_cont), None)


    #testing to build a block
    def test_on_block_action_received1(self):
        ply = player.ServerConnection(Mock(), Mock())
        block_cont = contained.BlockAction()
        self.assertEqual(ply.on_block_action_recieved(block_cont), None) #hp is none
        ply.set_hp(10)
        ply.world_object = Mock()
        ply.world_object.position.x = 1
        ply.world_object.position.y = 1
        ply.world_object.position.z = 1
        ply.blocks = 10
        ply.player_id = 1
        block_cont.value = player.BUILD_BLOCK
        block_cont.x = 1
        block_cont.y = 2
        block_cont.z = 1
        ply.on_block_action_recieved(block_cont)
        self.assertEqual(ply.blocks, 9) #a block has been placed


    #testing to destroy block
    def test_on_block_action_received2(self):

        def destroyA(x, y, z):
            return 1
        def destroyB(x, y, z):
            return 0

        ply = player.ServerConnection(Mock(), Mock())
        block_cont = contained.BlockAction()
        ply.set_hp(10)
        ply.world_object = Mock()
        ply.world_object.position.x = 1
        ply.world_object.position.y = 1
        ply.world_object.position.z = 1
        ply.tool = player.SPADE_TOOL
        ply.total_blocks_removed = 2
        ply.blocks = 10
        ply.player_id = 1
        ply.protocol.map.destroy_point = destroyA
        block_cont.value = player.DESTROY_BLOCK
        block_cont.x = 1
        block_cont.y = 2
        block_cont.z = 1
        ply.on_block_action_recieved(block_cont)
        self.assertEqual(ply.total_blocks_removed, 3) #a block has been removed with DESTROY_BLOCK
        block_cont.value = player.SPADE_DESTROY
        ply.on_block_action_recieved(block_cont)
        self.assertEqual(ply.total_blocks_removed, 6) #3 blocks destroyed with SPADE_DESTROY
        ply.protocol.map.destroy_point = destroyB
        ply.on_block_action_recieved(block_cont)
        self.assertEqual(ply.total_blocks_removed, 6) #no block removed


    #test1 in on position update recieved, Return None
    def test_on_position_update_received1(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object= Mock()
        ply.set_hp(10)
        ply.player_id = 1
        input_ply = contained.PositionData()
        ply.x = 1
        ply.y = 1
        ply.z = 1
        self.assertEqual(ply.on_position_update_recieved(input_ply), None)

    #tests to set last_position_update to other than default value None
    def test_on_position_update_received2(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.set_hp(10)
        ply.last_position_update = 1
        input_ply = contained.PositionData()
        ply.x = 1
        ply.y = 1
        ply.z = 1
        self.assertFalse(ply.on_position_update_recieved(input_ply), None)  # Since we've updated position, this should be false.

    #Inverse of above tests, last_position_update is None here
    def test_on_position_update_received3(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.player_id = 1
        ply.set_hp(10)
        ply.x = 1
        ply.y = 1
        ply.z = 1
        input_ply = contained.PositionData()
        self.assertEqual(ply.on_position_update_recieved(input_ply), None)  # Since we've not updated position, this should be equal.

    def test_grenade_exploded(self):
        ply = player.ServerConnection(Mock(), Mock())
        ply.world_object = Mock()
        ply.world_object.create_object()
        ply.world_object.position.x = 1
        ply.world_object.position.y = 1
        ply.world_object.position.z = 1
        ply.world_object.velocity.x = 0
        ply.world_object.velocity.y = 0
        ply.world_object.velocity.z = 1
        grenade = ply.world_object.protocol.world.create_object(
            ply.world_object.world.Grenade, contained.value,
            ply.world_object.Vertex3(*contained.position), None,
            ply.world_object.Vertex3(*contained.velocity), ply.world_object.grenade_exploded)
        ply.grenades = 1
        ply.set_team(1)
        ply.set_location(2)
        self.assertEqual(ply.grenade_exploded(grenade), None) #No hp set.
        ply.set_hp(10)
        self.assertTrue(ply.grenade_exploded(grenade))




