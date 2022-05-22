from enum import Enum
from wprofile.person import Person

class WPErrorCode(Enum):
    EXISTS = 1
    NOT_EXISTS = 2

# container class for many Person objects
class People:
    def __init__(self, PeopleList: list = None):
        self.people_dict = dict()
        if PeopleList is None:
            return
        for person in PeopleList:
            self.people_dict[person.name] = person

    def add(self, person: Person):
        existing = self.people_dict.get(person.name, None)
        if existing is not None:
            return WPErrorCode.EXISTS
        else:
            self.people_dict[person.name] = person

    def find(self, name: str):
        return self.people_dict.get(name, None)

    def contains(self, name: str):
        return self.people_dict.get(name, None) is not None

    def __len__(self):
        if self.people_dict is None:
            return 0
        else:
            return len(self.people_dict)

    def dict(self):
        return self.people_dict

if __name__ == "__main__":
    madhu = Person("madhu", "9176573999", "trufflemadhu@gmail.com", None)
    deepika = Person("deepika", "9632549340", "deepikarathnakar10@gmail.com", None)
    my_people_list = [madhu, deepika]
    for person in my_people_list:
        print(person)