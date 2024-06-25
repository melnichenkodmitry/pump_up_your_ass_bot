from sqlalchemy import Table, MetaData, Column, Integer, DateTime, Double

records = Table(
    'records',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('exercise_id', Integer),
    Column('repeats', Integer),
    Column('weight', Double),
    Column('approaches', Integer),
    Column('created_at', DateTime)
)
