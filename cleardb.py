from app import app, db

def clear_database():
    with app.app_context():
        meta = db.metadata
        for table in meta.sorted_tables:
            print(f"Clearing table {table.name}...")
            db.session.execute(table.delete())
        db.session.commit()
        print("All tables cleared successfully.")

if __name__ == "__main__":
    clear_database()