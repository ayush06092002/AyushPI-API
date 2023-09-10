"""
Test custom Django management commands.    
"""

# Importing the 'patch' function from the 'unittest.mock' module for 
# mocking and patching during unit testing.
from unittest.mock import patch

# Importing the 'OperationalError' class from the 'psycopg2' 
# module and aliasing it as 'Psycopg2Error' for handling 
# database-related errors.
from psycopg2 import OperationalError as Psycopg2Error

# Importing the 'call_command' function from the 'django.core.management' 
# module for calling Django management commands programmatically.
from django.core.management import call_command

# Importing the 'OperationalError' class from the 'django.db.utils' 
# module for handling database-related errors in Django applications.
from django.db.utils import OperationalError

# Importing the 'SimpleTestCase' class from the 'django.test' 
# module for creating simple test cases in Django testing.
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for the database when the database is available"""
        
        # Setting the 'patched_check' function to return 'True' when called.
        patched_check.return_value = True
        
        # Calling the 'wait_for_db' command.
        call_command('wait_for_db')

        # Asserting that the 'patched_check' function has been called once.
        patched_check.assert_called_once_with(databases= ['default'])


    @patch('time.sleep')    
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting Operational Error"""

        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases= ['default'])


