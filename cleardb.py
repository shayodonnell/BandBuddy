from app import app, db  # Import your Flask app and database instance

def clear_database():
    with app.app_context():
        # Get all tables and delete contents
        meta = db.metadata
        for table in meta.sorted_tables:
            print(f"Clearing table {table.name}...")
            db.session.execute(table.delete())
        db.session.commit()
        print("All tables cleared successfully.")

if __name__ == "__main__":
    clear_database()