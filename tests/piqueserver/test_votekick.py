import unittest
from unittest.mock import Mock
import piqueserver.scripts.votekick as Votekick

class TestVotekick(unittest.TestCase):

    def test_start_VK_in_progress(self):
        '''
        Requirement: A VotekickFailure-exception is raised if Votekick.start is
        called when there is already a votekick in progress.
        '''
        player1 = Mock()
        player2 = Mock()
        player1.protocol = Mock()
        player1.protocol.votekick = Mock()

        with self.assertRaises(Votekick.VotekickFailure) as e:
            Votekick.Votekick.start(player1, player2)
        self.assertEquals(str(e.exception), Votekick.S_IN_PROGRESS)

    def test_start_VK_self(self):
        '''
        Requirement: A VotekickFailure-exception is raised if a player attempts
        to start a votekick for themselves.
        '''
        player = Mock()
        player.protocol = Mock()
        player.protocol.votekick = None
        with self.assertRaises(Votekick.VotekickFailure) as e:
            Votekick.Votekick.start(player, player)
        self.assertEquals(str(e.exception), Votekick.S_SELF_VOTEKICK)
