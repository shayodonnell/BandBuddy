from app import app, db
from app.models import Band, BandAd, User, Post  # Import your models
from datetime import datetime  # Import datetime

def populate_database():
    with app.app_context():
        # Clear existing data
        db.session.query(Post).delete()
        db.session.query(BandAd).delete()
        db.session.query(Band).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Placeholder users
        users = [
            User(name="Alice", email="alice@example.com", password="password123"),
            User(name="Bob", email="bob@example.com", password="securepass"),
            User(name="Charlie", email="charlie@example.com", password="mypassword"),
            User(name="Diana", email="diana@example.com", password="supersecret"),
            User(name="Eve", email="eve@example.com", password="hackproof"),
        ]

        # Add users to database
        for user in users:
            db.session.add(user)

        db.session.commit()

        # Placeholder bands with owner IDs (1 to 5 corresponding to users above)
        bands = [
            Band(name="The Rockers", genre="Rock", description="A high-energy rock band.", owner=1),
            Band(name="Jazz Masters", genre="Jazz", description="Smooth and classy jazz performances.", owner=2),
            Band(name="Pop Divas", genre="Pop", description="Top pop hits and powerful vocals.", owner=3),
            Band(name="Classical Ensemble", genre="Classical", description="Beautiful classical music.", owner=4),
            Band(name="Metal Mayhem", genre="Metal", description="Hardcore metal with electrifying solos.", owner=5),
        ]

        # Add bands to database
        for band in bands:
            db.session.add(band)

        db.session.commit()

        # Placeholder ads and posts interleaved
        mixed_entries = [
            BandAd(
                band=1,
                lookingfor="Guitarist",
                deadline=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
                date=datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
            ),
            Post(
                content="Looking for a guitarist for my band!",
                image="https://images.unsplash.com/photo-1621586556026-98b104442283?q=80&w=3536&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                author=1,
                date=datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
            ),
            BandAd(
                band=2,
                lookingfor="Saxophonist",
                deadline=datetime.strptime("2025-01-15", "%Y-%m-%d").date(),
                date=datetime.strptime("2024-12-02", "%Y-%m-%d").date(),
            ),
            Post(
                content="Excited to start jamming with new members!",
                image="https://images.unsplash.com/photo-1651694721718-7a72df522ae3?q=80&w=3387&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                author=2,
                date=datetime.strptime("2024-12-02", "%Y-%m-%d").date(),
            ),
            BandAd(
                band=3,
                lookingfor="Drummer",
                deadline=datetime.strptime("2024-12-20", "%Y-%m-%d").date(),
                date=datetime.strptime("2024-12-03", "%Y-%m-%d").date(),
            ),
            Post(
                content="Does anyone know where to find good drummers?",
                image="https://images.unsplash.com/photo-1718946918946-f4fa72f6abec?q=80&w=3524&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                author=3,
                date=datetime.strptime("2024-12-03", "%Y-%m-%d").date(),
            ),
            BandAd(
                band=4,
                lookingfor="Violinist",
                deadline=datetime.strptime("2025-02-01", "%Y-%m-%d").date(),
                date=datetime.strptime("2024-12-04", "%Y-%m-%d").date(),
            ),
            Post(
                content="We need a saxophonist for our jazz band.",
                image="https://images.unsplash.com/photo-1566856528819-5b1f3f235a7d?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                author=4,
                date=datetime.strptime("2024-12-04", "%Y-%m-%d").date(),
            ),
            BandAd(
                band=5,
                lookingfor="Vocalist",
                deadline=datetime.strptime("2024-12-25", "%Y-%m-%d").date(),
                date=datetime.strptime("2024-12-05", "%Y-%m-%d").date(),
            ),
            Post(
                content="Vocalists, where are you? Hit us up!",
                image="https://images.unsplash.com/photo-1542813813-1f873f401e9b?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                author=5,
                date=datetime.strptime("2024-12-05", "%Y-%m-%d").date(),
            ),
        ]

        # Add mixed entries to database
        for entry in mixed_entries:
            db.session.add(entry)

        db.session.commit()

        print("Database populated with mixed posts and ads successfully.")

if __name__ == "__main__":
    populate_database()