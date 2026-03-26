from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djongo import models
from django.conf import settings
from pymongo import MongoClient

# Define test data
USERS = [
    {"username": "superman", "email": "superman@dc.com", "first_name": "Clark", "last_name": "Kent", "team": "dc"},
    {"username": "batman", "email": "batman@dc.com", "first_name": "Bruce", "last_name": "Wayne", "team": "dc"},
    {"username": "wonderwoman", "email": "wonderwoman@dc.com", "first_name": "Diana", "last_name": "Prince", "team": "dc"},
    {"username": "ironman", "email": "ironman@marvel.com", "first_name": "Tony", "last_name": "Stark", "team": "marvel"},
    {"username": "spiderman", "email": "spiderman@marvel.com", "first_name": "Peter", "last_name": "Parker", "team": "marvel"},
    {"username": "captainamerica", "email": "captainamerica@marvel.com", "first_name": "Steve", "last_name": "Rogers", "team": "marvel"},
]
TEAMS = [
    {"name": "marvel", "members": ["ironman", "spiderman", "captainamerica"]},
    {"name": "dc", "members": ["superman", "batman", "wonderwoman"]},
]
ACTIVITIES = [
    {"user": "superman", "activity": "Flight", "duration": 60},
    {"user": "batman", "activity": "Martial Arts", "duration": 45},
    {"user": "ironman", "activity": "Suit Training", "duration": 30},
]
LEADERBOARD = [
    {"user": "superman", "score": 100},
    {"user": "ironman", "score": 95},
    {"user": "batman", "score": 90},
]
WORKOUTS = [
    {"name": "Strength Training", "suggested_for": ["superman", "captainamerica"]},
    {"name": "Agility Drills", "suggested_for": ["spiderman", "wonderwoman"]},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Create unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
