#!/usr/bin/env python
"""
Database migration script for server-panel.
Usage:
    python migrate_db.py init     # Initialize migrations
    python migrate_db.py migrate  # Create a migration
    python migrate_db.py upgrade  # Apply migrations
"""
import os
import sys
from app import create_app
from flask_migrate import init, migrate as create_migration, upgrade

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python migrate_db.py [init|migrate|upgrade]")
        sys.exit(1)

    command = sys.argv[1]

    with app.app_context():
        if command == 'init':
            print("Initializing migrations...")
            init()
            print("✓ Migrations initialized!")
        elif command == 'migrate':
            message = sys.argv[2] if len(sys.argv) > 2 else "Auto-generated migration"
            print(f"Creating migration: {message}")
            create_migration(message=message)
            print("✓ Migration created!")
        elif command == 'upgrade':
            print("Applying migrations...")
            upgrade()
            print("✓ Migrations applied!")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python migrate_db.py [init|migrate|upgrade]")
            sys.exit(1)
