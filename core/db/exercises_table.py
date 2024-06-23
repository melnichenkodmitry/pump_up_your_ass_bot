from sqlalchemy import Table, MetaData, Column, Integer, Text

exercises = Table(
    'exercises',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('name', Text, unique=True)
)
