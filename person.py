
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    phone_no: str
    email: str
    picture: bytearray