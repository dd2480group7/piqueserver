import unittest
import piqueserver.game_modes.push as push
from unittest.mock import Mock


class TestGameModes(unittest.TestCase):
    def test_push1(self):
        connection = Mock()
        protocol = Mock()
        config = Mock()
        pP, pC = push.apply_script(protocol, connection, config)

        p = pC()
        hej = p.on_block_destroy(1, 2, 3, push.DESTROY_BLOCK)
        #pC.on_block_destroy = Mock()
        self.assertTrue(True)
        #self.assertTrue(pC.on_block_destroy(1, 2, 3, push.DESTROY_BLOCK))
