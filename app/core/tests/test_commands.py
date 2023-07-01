"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command  # Call command
from django.db.utils import OperationalError  # Depeending on the state of db
from django.test import SimpleTestCase  # Test case without Testing Database


# Mocking and/or overwriting the behavior of the check function.
# The self.check() function is a helper
# function from BaseCommand class from Django.
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Tests commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db is available."""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    # Mocking and/or overwriting the behavior of time.sleep.
    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db."""
        # First 2 times call_command will raise Psycopg2Error,
        # next 3 times will raise OperationalError,
        # and the last time will return True.
        # These are arbitrary values.
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        # Call command
        call_command("wait_for_db")
        # Two Assertions:
        # Check if patched_check was called 6 times.
        # We call it 6 times because we have 2 for one error,
        # 3 fot the other and finally 1 for the success.
        self.assertEqual(patched_check.call_count, 6)

        # Check if patched_check was called with database='default'
        patched_check.assert_called_with(databases=["default"])
