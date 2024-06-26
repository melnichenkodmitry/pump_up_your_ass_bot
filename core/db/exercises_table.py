from sqlalchemy import Table, MetaData, Column, Integer, Text, DateTime

exercises = Table(
    'exercises',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('exercise_name', Text, unique=True),
    Column('inventory_name', Text),
    Column('created_at', DateTime)
)
