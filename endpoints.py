from enum import Enum

class Endpoints(Enum):
    HELLO_WORLD_TEST = "HelloWorld_TEST"

    # override the __str__ method to return the value of the enum
    def __str__(self):
        return self.value