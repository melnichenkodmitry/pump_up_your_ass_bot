from sqlalchemy import Table, MetaData, Column, Integer, DateTime, Text

users = Table(
    'users',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('username', Text, unique=True),
    Column('first_name', Text),
    Column('last_name', Text),
    Column('reg_date', DateTime)
)
