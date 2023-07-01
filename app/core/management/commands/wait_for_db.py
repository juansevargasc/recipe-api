"""
Django command to wait for the database to be available.
"""
from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import (
    OperationalError,
)  # Django throws this error when DB is not ready


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")

        db_up = False

        while not db_up:
            try:
                # self.check() is a helper function
                # to check if the database is available.
                # It comes from BaseCommand class from Django.
                result = self.check(databases=["default"])
                self.stdout.write(f"self.check() result: {result}")
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)  # Sleep 1 second to the next iteration

        self.stdout.write(
            self.style.SUCCESS("Database available!")
        )  # self.style.SUCCESS() is a helper function to print in green color.
