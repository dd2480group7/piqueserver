from types import MethodType
import unittest
from unittest.mock import Mock
from piqueserver.commands import command, _alias_map, get_team, get_player, get_truthy


class TestCommandDecorator(unittest.TestCase):
    def test_admin_only(self):
        @command(admin_only=True)
        def test():
            pass
        want = set()
        want.add('admin')
        self.assertEqual(test.user_types, want)

    def test_command_name(self):
        @command()
        def test():
            pass
        self.assertEqual(test.command_name, 'test')

    def test_command_rename(self):
        @command('notatest')
        def test():
            pass
        self.assertEqual(test.command_name, 'notatest')

    def test_command_alias(self):
        @command('name', 'n')
        def test():
            pass
        self.assertEqual(_alias_map['n'], 'name')

class TestUtilityFunctions(unittest.TestCase):
    def setup(self):
        connection = Mock()
        connection.protocol = Mock()
        
        connection.protocol.team_1 = Mock()
        connection.protocol.team_1.name = "Barcelona"
        
        connection.protocol.team_2 = Mock()
        connection.protocol.team_2.name = "RealMadrid"
        
        connection.protocol.team_spectator = Mock()
        connection.protocol.team_spectator.name = "Spectators"
        
        connection.protocol.spectator_team = connection.protocol.team_spectator # see pyspades/server.py
        
        return {'connection': connection}
    
    def test_get_team(self):
        """
        Function being tested: piqueserver/commands.py:get_team(BaseConnection connection, str value)
        
        Inferred requirements:
            if value matches the name of team 1 or "1" (case insensitive), should return team 1 object
            if value matches the name of team 2 or "2" (case insensitive), should return team 2 object
            if value matches the name of the spectator team or "spec" (case insensitive), should return spectator team object
        """
        
        connection = self.setup()['connection']
        
        t1name = connection.protocol.team_1.name
        t2name = connection.protocol.team_2.name
        tspecname = connection.protocol.team_spectator.name
        
        self.assertEqual(get_team(connection, t1name), connection.protocol.team_1)
        self.assertEqual(get_team(connection, t1name.upper()), connection.protocol.team_1)
        self.assertEqual(get_team(connection, t1name.lower()), connection.protocol.team_1)
        self.assertEqual(get_team(connection, "1"), connection.protocol.team_1)
        
        self.assertEqual(get_team(connection, t2name), connection.protocol.team_2)
        self.assertEqual(get_team(connection, t2name.upper()), connection.protocol.team_2)
        self.assertEqual(get_team(connection, t2name.lower()), connection.protocol.team_2)
        self.assertEqual(get_team(connection, "2"), connection.protocol.team_2)
        
        self.assertEqual(get_team(connection, tspecname), connection.protocol.team_spectator)
        self.assertEqual(get_team(connection, tspecname.upper()), connection.protocol.team_spectator)
        self.assertEqual(get_team(connection, tspecname.lower()), connection.protocol.team_spectator)
        self.assertEqual(get_team(connection, "spec"), connection.protocol.team_spectator)
        
        self.assertRaises(Exception, get_team, connection, "")
        self.assertRaises(Exception, get_team, connection, "123abc")

    def test_get_player(self):
        """
        Function being tested: piqueserver/commands.py:get_player(BaseProtocol protocol,
                                                                  str value[,
                                                                  spectators])

        Explicit requirements:
            Given a name (string) or ID (string matching #<int>), returns matching player connection
            object. If a name is given and no player has the exact name, but exactly one player
            has a name that contains the specified name as a substring, returns the player object
            for that player.

        Inferred requirements:
            Substring matches are case-insensitive
            Throws exception if 1) a nonexistant ID is given
                                2) a name is given that does not match a player name and does not
                                   appear as a substring in any player name
                                3) a name is given that does not match a player name and appears as
                                   a substring in more than one player name
        """

        class players:
            def __init__(self, *names):
                self.the_values = list()
                self.add(*names)

            def add(self, *names):
                for name in names:
                    player = Mock()
                    player.name = name
                    player.world_object = Mock()

                    if name[0:10] == 'spectator:':
                        player.name = name[10:]
                        player.world_object = None

                    self.the_values.append(player)

            def values(self):
                return self.the_values

            def __getitem__(self, key):
                if type(key) == int:
                    return self.the_values[key]
                else:
                    for val in self.the_values:
                        if val.name == key:
                            return val

                    raise KeyError()

        connection = self.setup()['connection']
        connection.protocol.players = players("kalle", "pelle", "nisse", "spectator:viggo")

        self.assertEqual(get_player(connection.protocol, "#0").name, "kalle")
        self.assertEqual(get_player(connection.protocol, "kalle").name, "kalle")
        self.assertEqual(get_player(connection.protocol, "KaLLe").name, "kalle")
        self.assertEqual(get_player(connection.protocol, "#1").name, "pelle")
        self.assertEqual(get_player(connection.protocol, "pelle").name, "pelle")
        self.assertEqual(get_player(connection.protocol, "pEllE").name, "pelle")
        self.assertEqual(get_player(connection.protocol, "#2").name, "nisse")
        self.assertEqual(get_player(connection.protocol, "nisse").name, "nisse")
        self.assertEqual(get_player(connection.protocol, "Nisse").name, "nisse")

        self.assertEqual(get_player(connection.protocol, "alle").name, "kalle")
        self.assertEqual(get_player(connection.protocol, "elle").name, "pelle")
        self.assertEqual(get_player(connection.protocol, "s").name, "nisse")

        self.assertRaises(Exception, get_player, connection.protocol, "Napoleon") # no match
        self.assertRaises(Exception, get_player, connection.protocol, "lle") # ambiguous
        self.assertRaises(Exception, get_player, connection.protocol, "#10") # no such key

        self.assertEqual(get_player(connection.protocol, "viggo").name, "viggo")
        self.assertRaises(Exception, get_player, connection.protocol, "viggo", False) # no such player when filtering out spectators

    def test_get_truthy(self):
        """
        Function being tested: piqueserver/commands.py:get_truthy(str value)
        
        Inferred requirements:
            Using case-insensitive matching, return True for a value that matches any of the
            strings "yes", "y" or "on", return False for a value that matches any of the strings
            "no", "n" or "off", for all other values return None
        """

        for value in ["yes", "YES", "Yes", "yES", "yEs", "y", "Y", "on", "ON", "On", "oN"]:
            self.assertTrue(get_truthy(value))

        for value in ["no", "NO", "No", "nO", "n", "N", "off", "OFF", "Off", "oFF", "oFf"]:
            self.assertFalse(get_truthy(value))

        for value in ["cats", "DOGS", "bIRDs", "DiNoSaUrS"]:
            self.assertEqual(get_truthy(value), None)
