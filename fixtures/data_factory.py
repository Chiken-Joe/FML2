import random
import string
from datetime import datetime, timedelta

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_email():
    domains = ["example.com", "test.com", "demo.org"]
    return f"{random_string(10)}@{random.choice(domains)}"

def random_username():
    return random_string(8).capitalize()

def random_password():
    return random_string(12)

def random_post_title():
    templates = ["My thoughts on {}", "A story about {}", "Why {} is the best"]
    topic = random_string(5)
    return random.choice(templates).format(topic)

def random_post_content():
    return " ".join(random_string(random.randint(3, 8)) for _ in range(10))

def random_comment():
    templates = ["I agree!", "This is so true", "LOL", "Couldn't agree more", "Interesting..."]
    return random.choice(templates)

def random_status():
    statuses = ["contemplating_the_void", "pretending_to_work", "on_the_verge", "running_on_caffeine"]
    return random.choice(statuses)