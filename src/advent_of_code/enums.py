from enum import Enum

class ResponseType(Enum):
    NOT_YET_SUBMITTED = 1
    NO_RESPONSE = 2
    CORRECT = 3
    INCORRECT = 4
    INCORRECT_TOO_HIGH = 5
    INCORRECT_TOO_LOW = 6
    WRONG_LEVEL = 7
    TOO_SOON = 8
    OTHER = 9