from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import db, Hero, Power, HeroPower

# Create engine and bind to the session
engine = create_engine('sqlite:///app.db')
db.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Seeding powers
powers = [
    Power(name="super strength", description="gives the wielder super-human strengths"),
    Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
    Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
    Power(name="elasticity", description="can stretch the human body to extreme lengths"),
]
session.bulk_save_objects(powers)
session.commit()

# Seeding heroes
heroes = [
    Hero(name="Kamala Khan", super_name="Ms. Marvel"),
    Hero(name="Doreen Green", super_name="Squirrel Girl"),
    Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
    Hero(name="Janet Van Dyne", super_name="The Wasp"),
    Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
    Hero(name="Carol Danvers", super_name="Captain Marvel"),
    Hero(name="Jean Grey", super_name="Dark Phoenix"),
    Hero(name="Ororo Munroe", super_name="Storm"),
    Hero(name="Kitty Pryde", super_name="Shadowcat"),
    Hero(name="Elektra Natchios", super_name="Elektra"),
]
session.bulk_save_objects(heroes)
session.commit()

# Adding powers to heroes
strengths = ["Strong", "Weak", "Average"]
for hero in session.query(Hero).all():
    for _ in range(1, 4):
        power = session.query(Power).order_by(db.func.random()).first()
        hero_power = HeroPower(hero=hero, power=power, strength=strengths.pop())
        session.add(hero_power)
session.commit()

print("🦸‍♀️ Done seeding!")

# Close the session
session.close()
