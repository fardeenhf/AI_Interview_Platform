# Database Migration Script
# Run this to add the skills column to existing users

from app import app, db, User
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """Add skills column to users table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if skills column exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]

            if 'skills' not in columns:
                logger.info("Adding skills column to users table...")
                # Add skills column using SQLAlchemy 2.0+ syntax
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE users ADD COLUMN skills TEXT DEFAULT ""'))
                    conn.commit()
                logger.info("Skills column added successfully!")
            else:
                logger.info("Skills column already exists.")

            # Test the migration
            users = User.query.all()
            logger.info(f"Found {len(users)} users in database")

        except Exception as e:
            logger.error(f"Migration failed: {str(e)}")
            return False

    return True

if __name__ == "__main__":
    if migrate_database():
        print("✅ Database migration completed successfully!")
    else:
        print("❌ Database migration failed!")