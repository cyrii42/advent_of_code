import datetime as dt
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class PuzzleSQL(Base):
    __tablename__ = 'puzzles'
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    day: Mapped[int]
    title: Mapped[Optional[str]]
    description_1: Mapped[Optional[str]]
    description_2: Mapped[Optional[str]]
    example: Mapped[Optional[str]]
    input: Mapped[Optional[str]]
    answers: Mapped[List["AnswerSQL"]] = relationship()

class AnswerSQL(Base):
    __tablename__ = 'answers'
    id: Mapped[int] = mapped_column(primary_key=True)
    puzzle_id: Mapped[int] = mapped_column(ForeignKey("puzzles.id"))
    timestamp: Mapped[dt.datetime]
    level: Mapped[int]
    answer: Mapped[str]
    answer_correct: Mapped[Optional[bool]]
    raw_response: Mapped[Optional[str]]
    

# class User(Base):
#     __tablename__ = "user_account"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String)
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = relationship(
#         back_populates="user", cascade="all, delete-orphan"
#     )
#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"