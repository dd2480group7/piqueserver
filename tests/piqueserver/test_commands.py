import unittest
from unittest.mock import Mock
from piqueserver.commands import command, _alias_map, get_team


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

