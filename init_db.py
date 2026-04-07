from app import db, User, app

with app.app_context():
    # Clear old data to start fresh
    db.drop_all()
    db.create_all()
    
    # Pre-loading 4 specific accounts you requested
    # Password for all is 12345 by default in the Model
    test_users = [
        User(name="Student User", email="student@dsuniversity.ac.in", role="student", attendance=75, team_id=10),
        User(name="Faculty Member", email="faculty@dsuniversity.ac.in", role="faculty"),
        User(name="Office Staff", email="office@dsuniversity.ac.in", role="office"),
        User(name="Management Admin", email="management@dsuniversity.ac.in", role="management")
    ]
    
    db.session.bulk_save_objects(test_users)
    db.session.commit()
    print("Database Initialized! 150-participant capacity ready.")
    print("Test Login: student@dsuniversity.ac.in | Pass: 12345")