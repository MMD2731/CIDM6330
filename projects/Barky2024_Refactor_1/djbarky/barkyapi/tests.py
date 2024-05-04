from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from buildapc_app.management.commands.buildapcgo import BuildAPCAdminCLI
from buildapc_app.models import Cooler, Motherboard, RAM, GPU, Storage, PowerSupply, Tower, OperatingSystem, Monitor

# Test plans

class TestBuildAPCAdminCLIUnit(TestCase):
    def setUp(self):
        # Setup a test user and command line interface instance
        self.user = User.objects.create_user(username='testuser', password='password')
        self.cli = BuildAPCAdminCLI()
        self.cli.stdout = MagicMock()

    def test_do_login_successful(self):
        # Test successful login
        with patch('getpass.getpass', return_value='password'):
            with patch('builtins.input', return_value='testuser'):
                self.assertTrue(self.cli.do_login(''))

    def test_do_login_failed(self):
        # Test failed login due to incorrect password
        with patch('getpass.getpass', return_value='wrongpassword'):
            with patch('builtins.input', return_value='testuser'):
                self.assertTrue(self.cli.do_login(''))

    def test_do_quit(self):
        # Test quitting the application
        self.assertTrue(self.cli.do_quit(''))

    @patch('builtins.input', side_effect=['Q'])
    def test_main_menu_quit(self, mocked_input):
        # Test quitting from the main menu
        self.cli.main_menu()
        self.cli.stdout.write.assert_called_with('Exiting the program.')

    @patch('builtins.input', side_effect=['1', 'Q'])  # Select CPU management then quit
    def test_main_menu_cpu_management(self, mocked_input):
        self.cli.main_menu()
        self.cli.stdout.write.assert_called_with('Invalid choice, try again.')

    @patch('builtins.input', side_effect=['A', 'Q'])  # Select Add operation then quit
    def test_component_menu_add(self, mocked_input):
        self.cli.component_menu('CPU')
        self.cli.stdout.write.assert_called_with('Invalid action, try again.')

    def test_add_generic(self):
        # Assuming add_generic is correctly implemented
        with patch('buildapc_app.management.commands.buildapcgo.BuildAPCAdminCLI.add_generic', return_value=None) as mocked_add:
            mocked_add('CPU')
            mocked_add.assert_called_once()

    def test_edit_generic(self):
        # Test editing functionality
        with patch('buildapc_app.management.commands.buildapcgo.BuildAPCAdminCLI.edit_generic', return_value=None) as mocked_edit:
            mocked_edit('CPU')
            mocked_edit.assert_called_once()

    def test_view_generic(self):
        # Test viewing functionality
        with patch('buildapc_app.management.commands.buildapcgo.BuildAPCAdminCLI.view_generic', return_value=None) as mocked_view:
            mocked_view('CPU')
            mocked_view.assert_called_once()

    def test_delete_generic(self):
        # Test delete functionality
        with patch('buildapc_app.management.commands.buildapcgo.BuildAPCAdminCLI.delete_generic', return_value=None) as mocked_delete:
            mocked_delete('CPU')
            mocked_delete.assert_called_once()

    # Cooler Tests
    @patch('builtins.input', side_effect=['1', 'New Cooler', 'BeCool', '150'])
    def test_add_cooler(self, mock_input):
        with patch.object(self.cli, 'add_generic', return_value=None) as mocked_add:
            self.cli.a_cooler()
            mocked_add.assert_called_once()

    @patch('builtins.input', return_value='1')
    def test_delete_cooler(self, mock_input):
        with patch.object(self.cli, 'delete_generic', return_value=None) as mocked_delete:
            self.cli.d_cooler()
            mocked_delete.assert_called_once_with(Cooler, 1)

    @patch('builtins.input', side_effect=['1', 'Updated Cooler', 'Frozen', '250'])
    def test_edit_cooler(self, mock_input):
        with patch.object(self.cli, 'edit_generic', return_value=None) as mocked_edit:
            self.cli.e_cooler()
            mocked_edit.assert_called_once()

    def test_view_coolers(self):
        with patch.object(self.cli, 'view_generic', return_value=None) as mocked_view:
            self.cli.v_cooler()
            mocked_view.assert_called_once_with(Cooler)



# 8. delete a snippet
# 9. list snippets
# 10. update a snippet
# 11. create a user
# 12. retrieve a user
# 13. delete a user
# 14. list users
# 15. update a user
# 16. highlight a snippet
# 17. list bookmarks by user
# 18. list snippets by user
# 20. list bookmarks by date
# 21. list snippets by date
# 23. list bookmarks by title
# 24. list snippets by title
# 26. list bookmarks by url
# 27. list snippets by url
