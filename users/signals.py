import sqlite3
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def save_user_to_external_db(sender, instance, created, **kwargs):
    if created:
        conn = sqlite3.connect('external_user.db')  # Make sure path is correct
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS external_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO external_users (username, email) VALUES (?, ?)
        ''', (instance.username, instance.email))
        conn.commit()
        conn.close()
