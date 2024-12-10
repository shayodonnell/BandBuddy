from app import app, db
from app.models import Band, Bandad, User, Post, Like, Interest  # Import your models
from datetime import datetime  # Import datetime
from werkzeug.security import generate_password_hash  # For password hashing

def populate_database():
    with app.app_context():
        try:
            # Clear existing data in the correct order to respect foreign key constraints
            db.session.query(Like).delete()
            db.session.query(Interest).delete()
            db.session.query(Post).delete()
            db.session.query(Bandad).delete()
            db.session.query(Band).delete()
            db.session.query(User).delete()
            db.session.commit()

            # Placeholder users with hashed passwords
            users = [
                User(name="Alice", email="alice@example.com", password=generate_password_hash("password123")),
                User(name="Bob", email="bob@example.com", password=generate_password_hash("securepass")),
                User(name="Charlie", email="charlie@example.com", password=generate_password_hash("mypassword")),
                User(name="Diana", email="diana@example.com", password=generate_password_hash("supersecret")),
                User(name="Eve", email="eve@example.com", password=generate_password_hash("hackproof")),
            ]

            # Add users to database
            db.session.add_all(users)
            db.session.commit()

            # Create a mapping from user names to user objects for easy reference
            user_map = {user.name: user for user in users}

            # Placeholder bands with owner references
            bands = [
                Band(name="The Rockers", genre="Rock", description="A high-energy rock band.", owner=user_map["Alice"].id),
                Band(name="Jazz Masters", genre="Jazz", description="Smooth and classy jazz performances.", owner=user_map["Bob"].id),
                Band(name="Pop Divas", genre="Pop", description="Top pop hits and powerful vocals.", owner=user_map["Charlie"].id),
                Band(name="Classical Ensemble", genre="Classical", description="Beautiful classical music.", owner=user_map["Diana"].id),
                Band(name="Metal Mayhem", genre="Metal", description="Hardcore metal with electrifying solos.", owner=user_map["Eve"].id),
            ]

            # Add bands to database
            db.session.add_all(bands)
            db.session.commit()

            # Create a mapping from band names to band objects for easy reference
            band_map = {band.name: band for band in bands}

            # Placeholder ads and posts interleaved, including posts without images
            mixed_entries = [
                # Bandads
                Bandad(
                    band=band_map["The Rockers"].id,
                    lookingfor="Guitarist",
                    deadline=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
                    date=datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
                ),
                # Posts with images
                Post(
                    content="Looking for a guitarist for my band!",
                    image="https://images.unsplash.com/photo-1621586556026-98b104442283?q=80&w=3536&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                    author=user_map["Alice"].id,
                    date=datetime.strptime("2024-12-01", "%Y-%m-%d").date(),
                ),
                Bandad(
                    band=band_map["Jazz Masters"].id,
                    lookingfor="Saxophonist",
                    deadline=datetime.strptime("2025-01-15", "%Y-%m-%d").date(),
                    date=datetime.strptime("2024-12-02", "%Y-%m-%d").date(),
                ),
                Post(
                    content="Excited to start jamming with new members!",
                    image="https://images.unsplash.com/photo-1651694721718-7a72df522ae3?q=80&w=3387&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                    author=user_map["Bob"].id,
                    date=datetime.strptime("2024-12-02", "%Y-%m-%d").date(),
                ),
                Bandad(
                    band=band_map["Pop Divas"].id,
                    lookingfor="Drummer",
                    deadline=datetime.strptime("2024-12-20", "%Y-%m-%d").date(),
                    date=datetime.strptime("2024-12-03", "%Y-%m-%d").date(),
                ),
                Post(
                    content="Does anyone know where to find good drummers?",
                    image="https://images.unsplash.com/photo-1718946918946-f4fa72f6abec?q=80&w=3524&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                    author=user_map["Charlie"].id,
                    date=datetime.strptime("2024-12-03", "%Y-%m-%d").date(),
                ),
                Bandad(
                    band=band_map["Classical Ensemble"].id,
                    lookingfor="Violinist",
                    deadline=datetime.strptime("2025-02-01", "%Y-%m-%d").date(),
                    date=datetime.strptime("2024-12-04", "%Y-%m-%d").date(),
                ),
                Post(
                    content="We need a saxophonist for our jazz band.",
                    image="https://images.unsplash.com/photo-1566856528819-5b1f3f235a7d?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                    author=user_map["Diana"].id,
                    date=datetime.strptime("2024-12-04", "%Y-%m-%d").date(),
                ),
                Bandad(
                    band=band_map["Metal Mayhem"].id,
                    lookingfor="Vocalist",
                    deadline=datetime.strptime("2024-12-25", "%Y-%m-%d").date(),
                    date=datetime.strptime("2024-12-05", "%Y-%m-%d").date(),
                ),
                Post(
                    content="Vocalists, where are you? Hit us up!",
                    image="https://images.unsplash.com/photo-1542813813-1f873f401e9b?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                    author=user_map["Eve"].id,
                    date=datetime.strptime("2024-12-05", "%Y-%m-%d").date(),
                ),
                # Additional Posts without images
                Post(
                    content="Open for new members! Join us for exciting performances.",
                    image=None,  # No image provided
                    author=user_map["Alice"].id,
                    date=datetime.strptime("2024-12-06", "%Y-%m-%d").date(),
                ),
                Post(
                    content="Seeking a talented bassist to complete our rhythm section.",
                    # Omitting the 'image' field implies it will be set to None
                    author=user_map["Bob"].id,
                    date=datetime.strptime("2024-12-07", "%Y-%m-%d").date(),
                ),
                Post(
                    content="Rehearsals every Friday night. All skill levels welcome!",
                    image=None,
                    author=user_map["Charlie"].id,
                    date=datetime.strptime("2024-12-08", "%Y-%m-%d").date(),
                ),
            ]

            # Sort mixed_entries by date to interleave Bandads and Posts based on their dates
            mixed_entries.sort(key=lambda x: x.date)

            # Add mixed entries to database in sorted order
            db.session.add_all(mixed_entries)
            db.session.commit()

            # Retrieve all posts and bandads for creating likes and interests
            all_posts = Post.query.all()
            all_bandads = Bandad.query.all()

            # Sample Likes: Users liking different posts
            likes = [
                Like(user_id=user_map["Bob"].id, post_id=all_posts[0].id),
                Like(user_id=user_map["Charlie"].id, post_id=all_posts[1].id),
                Like(user_id=user_map["Diana"].id, post_id=all_posts[2].id),
                Like(user_id=user_map["Eve"].id, post_id=all_posts[3].id),
                Like(user_id=user_map["Alice"].id, post_id=all_posts[4].id),
                Like(user_id=user_map["Diana"].id, post_id=all_posts[5].id),  # Like for a post without image
                Like(user_id=user_map["Eve"].id, post_id=all_posts[6].id),    # Like for a post without image
                Like(user_id=user_map["Alice"].id, post_id=all_posts[7].id),  # Like for a post without image
            ]

            # Add likes to database
            db.session.add_all(likes)
            db.session.commit()

            # Sample Interests: Users expressing interest in different band ads
            interests = [
                Interest(user_id=user_map["Charlie"].id, ad_id=all_bandads[0].id, date=datetime.utcnow()),
                Interest(user_id=user_map["Diana"].id, ad_id=all_bandads[1].id, date=datetime.utcnow()),
                Interest(user_id=user_map["Eve"].id, ad_id=all_bandads[2].id, date=datetime.utcnow()),
                Interest(user_id=user_map["Alice"].id, ad_id=all_bandads[3].id, date=datetime.utcnow()),
                Interest(user_id=user_map["Bob"].id, ad_id=all_bandads[4].id, date=datetime.utcnow()),
                Interest(user_id=user_map["Charlie"].id, ad_id=all_bandads[0].id, date=datetime.utcnow()),  # Additional interest
            ]

            # Add interests to database
            db.session.add_all(interests)
            db.session.commit()

            print("Database populated with users, bands, band ads, posts (with and without images), likes, and interests successfully.")

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while populating the database: {e}")

if __name__ == "__main__":
    populate_database()