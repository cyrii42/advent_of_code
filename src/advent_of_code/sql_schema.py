from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, Table, Column, ForeignKey, UniqueConstraint, Text, Integer, Boolean

metadata_obj = MetaData()

puzzles_table = Table(
    'puzzles',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('year', Integer, nullable=False),
    Column('day', Integer, nullable=False),
    Column('title', Text),
    Column('part_1_description', Text),
    Column('part_1_solved', Boolean),
    Column('part_1_answer', Text),
    Column('part_2_description', Text),
    Column('part_2_solved', Boolean),
    Column('part_2_answer', Text),
    Column('example_text', Text),
    Column('input_text', Text),
    Column('raw_html', Text),
    Column('url', Text),
    UniqueConstraint('year', 'day'), 
)

answers_table = Table(
    'answers',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('puzzle_id', Integer, ForeignKey('puzzles.id'), nullable=False),
    Column('year', Integer, nullable=False),
    Column('day', Integer, nullable=False),
    Column('timestamp', Text, nullable=False),
    Column('level', Integer, nullable=False),
    Column('answer', Text, nullable=False),
    Column('correct', Boolean),
    Column('response_type', Text),
    Column('raw_response', Text),
    UniqueConstraint('puzzle_id', 'level', 'answer'), 
)

class Base(DeclarativeBase):
    pass

class PuzzleSQL(Base):
    __table__ = puzzles_table

class AnswerSQL(Base):
    __table__ = answers_table



if __name__ == '__main__':
    pass