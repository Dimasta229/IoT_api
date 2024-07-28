from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from config import DATABASE

db = PostgresqlExtDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class BaseModel(Model):
    class Meta:
        database = db

class ApiUser(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

class Location(BaseModel):
    name = CharField()

class Device(BaseModel):
    name = CharField()
    type = CharField()
    login = CharField(null=True)
    password = CharField(null=True)
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(ApiUser, backref='devices')

def initialize_database():
    db.connect()
    db.create_tables([ApiUser, Location, Device], safe=True)

def populate_initial_data():
    if not Location.select().exists():
        Location.create(name='Default Location')
    if not ApiUser.select().exists():
        ApiUser.create(name='Default User', email='user@example.com', password='securepassword')
