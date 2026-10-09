from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):
    def start(self) -> None:
        ...

class AHU:
    def start(self):
        print("AHU ON")

ahu = AHU()
print(isinstance(ahu, Startable))