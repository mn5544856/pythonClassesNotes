# Python OOP — Lessons 41-50 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 41: `dataclass` — Deep Understanding

## 1. Normal Class Mein Problem

```python
class Employee:
    def __init__(self, name, salary, department):
        self.name = name
        self.salary = salary
        self.department = department

    def __repr__(self):
        return f"Employee(name={self.name!r}, salary={self.salary!r}, department={self.department!r})"

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return (self.name == other.name and self.salary == other.salary and self.department == other.department)
```

**Explanation:**
- `__init__` → manually likhna pada
- `__repr__` → manually likhna pada
- `__eq__` → manually likhna pada
- Bohat boilerplate

## 2. `@dataclass`

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    salary: float
    department: str
```

**Explanation:**
- `@dataclass` → decorator
- Python automatically `__init__`, `__repr__`, `__eq__` generate karta hai

## 3. Automatic `__init__`

```python
employee = Employee("Ali", 5000, "HVAC")
print(employee.name)        # Ali
print(employee.salary)      # 5000
print(employee.department)  # HVAC
```

**Explanation:**
- `Employee("Ali", 5000, "HVAC")` → automatically `__init__` chala

## 4. Automatic `__repr__`

```python
print(employee)
```

**Output:**
```
Employee(name='Ali', salary=5000, department='HVAC')
```

## 5. Automatic `__eq__`

```python
e1 = Employee("Ali", 5000, "HVAC")
e2 = Employee("Ali", 5000, "HVAC")
print(e1 == e2)   # True
```

**Explanation:**
- Fields compare hue

## 6. Default Values

```python
@dataclass
class Equipment:
    equipment_id: str
    status: str = "OFF"

ahu = Equipment("AHU-01")
print(ahu.status)   # OFF
```

**Explanation:**
- `status: str = "OFF"` → default value

## 7. Field Ordering Rule

```python
# Correct
@dataclass
class Employee:
    name: str
    department: str
    salary: float = 5000

# Problematic
@dataclass
class Employee:
    salary: float = 5000
    name: str
```

**Explanation:**
- Non-default fields pehle
- Default fields baad mein

## 8. `field()`

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    name: str
    skills: list[str] = field(default_factory=list)
```

**Explanation:**
- `field()` → field customize

## 9. `default_factory`

```python
# Wrong
@dataclass
class Employee:
    skills: list[str] = []   # Mutable default

# Correct
@dataclass
class Employee:
    skills: list[str] = field(default_factory=list)
```

**Explanation:**
- `default_factory=list` → har object ke liye nayi list

## 10. Work Order Example

```python
@dataclass
class WorkOrder:
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: str = ""
    tags: list[str] = field(default_factory=list)
```

## 11. `__post_init__()`

```python
@dataclass
class Employee:
    name: str
    salary: float

    def __post_init__(self):
        if self.salary < 0:
            raise ValueError("Salary negative nahi ho sakti")
```

**Flow:**
```
Employee(...)
    ↓
__init__()
    ↓
fields assign
    ↓
__post_init__()
```

## 12. `__post_init__()` Calculation

```python
@dataclass
class Equipment:
    supply_temp: float
    return_temp: float
    delta_t: float = field(init=False)

    def __post_init__(self):
        self.delta_t = self.supply_temp - self.return_temp

ahu = Equipment(14.0, 22.0)
print(ahu.delta_t)   # -8.0
```

**Explanation:**
- `field(init=False)` → constructor mein nahi
- `__post_init__` → calculate

## 13. `init=False`

```python
delta_t: float = field(init=False)
```

**Explanation:**
- Generated `__init__` mein parameter nahi

## 14. `repr=False`

```python
@dataclass
class Employee:
    name: str
    salary: float = field(repr=False)
```

**Explanation:**
- `repr()` mein salary hide

## 15. `compare=False`

```python
@dataclass
class Employee:
    name: str
    department: str
    last_login: str = field(compare=False)
```

**Explanation:**
- `__eq__` mein `last_login` ignore

## 16. `frozen=True`

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

point = Point(10, 20)
point.x = 50   # Error
```

**Explanation:**
- Immutable-like

## 17. `order=True`

```python
@dataclass(order=True)
class Temperature:
    value: float

t1 = Temperature(20)
t2 = Temperature(25)
print(t1 < t2)   # True
```

## 18. `slots=True`

```python
@dataclass(slots=True)
class Equipment:
    equipment_id: str
    temperature: float
```

**Explanation:**
- `__slots__` jaisa behavior

## 19. `kw_only=True`

```python
@dataclass(kw_only=True)
class Equipment:
    equipment_id: str
    temperature: float

equipment = Equipment(equipment_id="AHU-01", temperature=22.5)
```

**Explanation:**
- Keyword-only constructor

## 20. Dataclass + Inheritance

```python
@dataclass
class Equipment:
    equipment_id: str

@dataclass
class AHU(Equipment):
    airflow: float

ahu = AHU(equipment_id="AHU-01", airflow=5000)
```

## 21. Dataclass vs `TypedDict`

```
TypedDict → dictionary shape
Dataclass → object shape
```

## 22. Dataclass vs Normal Class

| Feature | Normal | Dataclass |
|---------|--------|-----------|
| `__init__` | Manual | Auto |
| `__repr__` | Manual | Auto |
| `__eq__` | Manual | Auto |
| Data-focused | Depends | Yes |

## 23. Dataclass vs `NamedTuple`

```
NamedTuple → tuple-like immutable
Dataclass → object-style
```

## 24. HVAC Example

```python
@dataclass
class Equipment:
    equipment_id: str
    equipment_type: str
    floor: str
    area: str

ahu = Equipment(
    equipment_id="AHU-01",
    equipment_type="AHU",
    floor="34",
    area="Mechanical Room"
)
```

## 25. Methods Bhi Add

```python
@dataclass
class Equipment:
    equipment_id: str
    status: str = "OFF"

    def start(self):
        self.status = "ON"

ahu = Equipment("AHU-01")
ahu.start()
```

## 26. Complete Example

```python
@dataclass(slots=True)
class Equipment:
    equipment_id: str
    equipment_type: str
    temperature: float
    status: str = "OFF"
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.temperature < -273.15:
            raise ValueError("Invalid temperature")

    def start(self):
        self.status = "ON"

ahu = Equipment(equipment_id="AHU-01", equipment_type="AHU", temperature=22.5)
ahu.start()
print(ahu)
```

## 27. Mental Model

```
@dataclass → normal class + auto data methods
field() → field customize
default_factory → fresh value
__post_init__ → after init processing
frozen=True → immutable-like
slots=True → slot storage
kw_only=True → keyword-only
```

---

# Lesson 42: `Enum` + `Literal` + `StrEnum`

## 1. Problem

```python
def set_mode(mode: str):
    ...
```

**Explanation:**
- Koi bhi string aa sakti hai
- `"auto"`, `"manual"`, `"xyz"` — sab allowed

## 2. `Literal`

```python
from typing import Literal

Mode = Literal["auto", "manual"]

def set_mode(mode: Mode):
    ...

set_mode("auto")     # OK
set_mode("manual")   # OK
set_mode("random")   # Error
```

**Explanation:**
- `Literal["auto", "manual"]` → sirf ye values
- Type checker enforce

## 3. Multiple Literal Values

```python
Mode = Literal["auto", "manual", "off"]
```

## 4. Magic Strings Problem

```python
if mode == "auto":
    ...
if mode == "manual":
    ...
```

**Explanation:**
- Typo risk: `"manul"`

## 5. `Enum`

```python
from enum import Enum

class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"
```

**Explanation:**
- `Mode.AUTO` → enum member
- Named constants

## 6. Enum Member

```python
print(Mode.AUTO)         # Mode.AUTO
print(Mode.AUTO.value)   # auto
```

**Explanation:**
- `Mode.AUTO` → member
- `Mode.AUTO.value` → stored value

## 7. Comparison

```python
Mode.AUTO == Mode.AUTO   # True
Mode.AUTO == "auto"      # False
```

**Explanation:**
- `Mode.AUTO` aur `"auto"` different objects

## 8. `.value`

```python
mode = Mode.AUTO
print(mode.value)   # auto
send_to_api(mode.value)
```

## 9. Iterate

```python
for mode in Mode:
    print(mode)

# Mode.AUTO
# Mode.MANUAL
# Mode.OFF
```

## 10. HVAC Example

```python
class HVACMode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"

class AHU:
    def __init__(self):
        self.mode = HVACMode.AUTO

    def set_mode(self, mode: HVACMode):
        self.mode = mode

ahu = AHU()
ahu.set_mode(HVACMode.MANUAL)
```

## 11. `Literal` vs `Enum`

```
Literal → type checking, exact values
Enum → runtime members, named constants
```

## 12. Enum Methods

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"

    def is_automatic(self):
        return self is Mode.AUTO

mode = Mode.AUTO
print(mode.is_automatic())   # True
```

## 13. Enum Properties

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"

    @property
    def description(self):
        if self is Mode.AUTO:
            return "Automatic control"
        return "Manual control"

print(Mode.AUTO.description)   # Automatic control
```

## 14. `auto()`

```python
from enum import Enum, auto

class Status(Enum):
    OFF = auto()
    ON = auto()
    ALARM = auto()
```

## 15. `StrEnum`

```python
from enum import StrEnum

class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"

mode = Mode.AUTO
print(mode)   # auto
```

**Explanation:**
- String behavior + enum members

## 16. `Enum` vs `StrEnum`

```
Enum → named member
StrEnum → named member + string behavior
```

## 17. API Context

```python
class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"

mode = Mode.AUTO
# JSON: {"mode": "auto"}
```

## 18. `Literal` + `Enum`

```python
def set_mode(mode: HVACMode):
    ...

def send_mode(mode: Literal["auto", "manual"]):
    ...

api_value = HVACMode.AUTO.value
```

## 19. Architecture

```
Application → HVACMode.AUTO → .value → "auto" → API
```

## 20. `Literal` Kab

```
Choti choices
Simple type checking
Runtime object nahi
```

## 21. `Enum` Kab

```
Application-wide values
Named constants
Runtime identity
Methods/properties
```

## 22. `StrEnum` Kab

```
Named enum + string values + API/JSON
```

## 23. Enum + Dataclass

```python
from dataclasses import dataclass
from enum import StrEnum

class Status(StrEnum):
    ON = "on"
    OFF = "off"

@dataclass
class Equipment:
    equipment_id: str
    status: Status = Status.OFF

ahu = Equipment("AHU-01")
print(ahu.status)         # Status.OFF
print(ahu.status.value)   # off
```

## 24. Enum + Pattern Matching

```python
def handle_status(status: Status):
    match status:
        case Status.ON:
            print("Running")
        case Status.OFF:
            print("Stopped")
```

## 25. Enum vs Constants

```python
# Without
AUTO = "auto"
MANUAL = "manual"

# With
class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
```

## 26. Comparison Table

| Feature | `Literal` | `Enum` | `StrEnum` |
|---------|-----------|--------|-----------|
| Static checking | ✅ | ✅ | ✅ |
| Runtime members | ❌ | ✅ | ✅ |
| Named constants | Limited | ✅ | ✅ |
| String-oriented | N/A | ❌ | ✅ |
| Methods | ❌ | ✅ | ✅ |

## 27. Mental Model

```
Literal → "Sirf ye values"
Enum → "Named runtime members"
StrEnum → "Named + string behavior"
```

---

# Lesson 43: `Iterable`, `Iterator`, `Sequence`, `Mapping`

## 1. `Iterable`

```python
numbers = [10, 20, 30]
for number in numbers:
    print(number)
```

**Explanation:**
- `list` iterable hai

## 2. `Iterable` Protocol

```
Iterable → __iter__() → Iterator
```

```python
numbers = [10, 20, 30]
iterator = iter(numbers)
print(next(iterator))   # 10
```

## 3. `Iterable` vs `Iterator`

```
Iterable → "iterator bana sakte ho"
Iterator → "next item provide karta hai"
```

## 4. Example

```python
numbers = [10, 20, 30]   # Iterable
it = iter(numbers)        # Iterator
print(next(it))           # 10
print(next(it))           # 20
print(next(it))           # 30
print(next(it))           # StopIteration
```

## 5. `for` Loop Internally

```python
iterator = iter(numbers)
while True:
    try:
        x = next(iterator)
        print(x)
    except StopIteration:
        break
```

## 6. `Iterator` Bhi `Iterable`

```
Iterator ⊂ Iterable
```

## 7. `Sequence`

```python
from collections.abc import Sequence

numbers = [10, 20, 30]
print(numbers[0])   # 10
print(len(numbers)) # 3
```

**Explanation:**
- Ordered + indexable + iterable

## 8. `Iterable` vs `Sequence`

```
Iterable → for loop
Sequence → for + index + length
```

## 9. Function Design

```python
# Specific
def first_item(items: list[str]) -> str:
    return items[0]

# Better
from collections.abc import Sequence

def first_item(items: Sequence[str]) -> str:
    return items[0]
```

## 10. `Iterable` Example

```python
from collections.abc import Iterable

def print_items(items: Iterable[str]) -> None:
    for item in items:
        print(item)

print_items(["A", "B"])
print_items(("A", "B"))
print_items({"A", "B"})
print_items(x for x in ["A", "B"])
```

## 11. `Sequence` Example

```python
def print_first(items: Sequence[str]) -> str:
    return items[0]

# print_first(x for x in ["A", "B"])  # Error
```

## 12. `Mapping`

```python
from collections.abc import Mapping

employee = {"name": "Ali", "salary": 5000}
print(employee["name"])   # Ali
```

## 13. `dict` vs `Mapping`

```python
def show_name(data: Mapping[str, str]):
    print(data["name"])
```

**Explanation:**
- `Mapping` → read-only abstraction

## 14. `MutableMapping`

```python
from collections.abc import MutableMapping

def update(data: MutableMapping[str, int]):
    data["salary"] = 6000
```

## 15. `Mapping` vs `MutableMapping`

```
Mapping → read
MutableMapping → read + modify
```

## 16. `Sequence` vs `MutableSequence`

```
Sequence → ordered + indexable
MutableSequence → + modify
```

## 17. Hierarchy

```
Iterable
├── Sequence
│   └── MutableSequence
└── other iterables

Mapping
└── MutableMapping
```

## 18. `Callable`

```python
from collections.abc import Callable

def add(a, b):
    return a + b

print(callable(add))   # True
```

## 19. Callable Objects

```python
class Calculator:
    def __call__(self, a, b):
        return a + b

calc = Calculator()
print(calc(10, 20))   # 30
```

## 20. Callable Annotation

```python
def execute(
    operation: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return operation(a, b)
```

## 21. Custom Iterator

```python
class Counter:
    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

counter = Counter(3)
for value in counter:
    print(value)
# 0
# 1
# 2
```

## 22. Generator vs Custom Iterator

```python
# Manual
class Counter:
    def __iter__(self): return self
    def __next__(self): ...

# Generator
def counter():
    yield 0
    yield 1
    yield 2
```

## 23. `Iterable` Function Design

```python
def create_folders(rows: Iterable[WorkOrder]):
    for row in rows:
        ...
```

## 24. `Sequence` Kab

```python
def process(rows: Sequence[WorkOrder]):
    first = rows[0]
```

## 25. `Mapping` Kab

```python
def process(row: Mapping[str, str]):
    work_order = row["Work Order Number"]
```

## 26. `TypedDict` vs `Mapping`

```
TypedDict → exact known keys
Mapping → generic key/value
```

## 27. `dict` vs `Mapping` vs `TypedDict`

| Type | Focus |
|------|-------|
| `dict` | Concrete |
| `Mapping` | Read-only interface |
| `MutableMapping` | Mutable interface |
| `TypedDict` | Specific schema |

## 28. `list` vs `Sequence` vs `Iterable`

| Type | Capability |
|------|-----------|
| `Iterable[T]` | iterate |
| `Sequence[T]` | iterate + index |
| `MutableSequence[T]` | + modify |

## 29. Design Principle

```python
# Specific
def total(numbers: list[int]) -> int:
    return sum(numbers)

# Better
def total(numbers: Iterable[int]) -> int:
    return sum(numbers)
```

## 30. Capability Ladder

```
Iterable → "I can iterate"
Sequence → "I can iterate + index"
MutableSequence → "I can iterate + index + modify"

Mapping → "I can read key/value"
MutableMapping → "I can read + modify"

Callable → "I can be called"
```

## 31. Modern Imports

```python
from collections.abc import (
    Iterable,
    Iterator,
    Sequence,
    MutableSequence,
    Mapping,
    MutableMapping,
    Callable,
)
```

## 32. Final Mental Map

```
Iterable → iter() → Iterator → next()

Sequence → ordered + indexable

Mapping → key → value

Callable → object()
```

**Key Point:** Function ko jitni capability chahiye, utna general type karo.

---

# Lesson 44: ABC + `collections.abc` + `Protocol`

## 1. ABC

```python
from abc import ABC, abstractmethod

class Equipment(ABC):
    @abstractmethod
    def start(self):
        pass

# equipment = Equipment()  # Error
```

## 2. Child Class

```python
class AHU(Equipment):
    def start(self):
        print("AHU started")

ahu = AHU()
ahu.start()   # AHU started
```

## 3. ABC Contract

```python
class Equipment(ABC):
    @abstractmethod
    def start(self): pass

    @abstractmethod
    def stop(self): pass
```

## 4. `collections.abc`

```python
from collections.abc import Iterable, Sequence, Mapping, Iterator, Callable
```

## 5. `Sequence`

```python
from collections.abc import Sequence

numbers = [10, 20, 30]
isinstance(numbers, Sequence)   # True
```

## 6. `ABC.register()`

```python
class Equipment(ABC):
    pass

class Sensor:
    pass

Equipment.register(Sensor)
isinstance(Sensor(), Equipment)   # True
```

## 7. Virtual Subclass

```
Equipment
    :
    : registered
    ↓
  Sensor
```

## 8. `Protocol`

```python
from typing import Protocol

class Startable(Protocol):
    def start(self) -> None:
        ...

class AHU:
    def start(self) -> None:
        print("AHU started")
```

**Explanation:**
- `AHU` inherit nahi kiya
- Structure match

## 9. ABC vs Protocol

**ABC:**
```
explicit inheritance + runtime hierarchy
```

**Protocol:**
```
structural typing + loose coupling
```

## 10. Nominal vs Structural

**Nominal:**
```python
class AHU(Equipment):
    ...
```

**Structural:**
```python
class AHU:
    def start(self): ...
```

## 11. Mental Model

```
ABC → "Who are you?"
Protocol → "What can you do?"
```

## 12. Runtime `isinstance()`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):
    def start(self) -> None: ...

isinstance(ahu, Startable)   # True
```

## 13. Limitation

```
@runtime_checkable → basic structure check
Full static validation nahi
```

## 14. ABC + Protocol Together

```python
class Equipment(ABC):
    @abstractmethod
    def start(self) -> None: pass

class Monitorable(Protocol):
    def get_status(self) -> str: ...

class AHU(Equipment):
    def start(self):
        print("AHU started")
    def get_status(self) -> str:
        return "ON"
```

## 15. ABC Kab

```
Strong hierarchy
Shared implementation
Domain model
```

## 16. Protocol Kab

```
Different classes
Same capability
Loose coupling
```

## 17. `collections.abc` Role

```
Iterable, Iterator, Sequence, Mapping, Callable
```

## 18. Custom Collection

```python
from collections.abc import Sequence

class EquipmentList(Sequence):
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

equipment = EquipmentList(["AHU-01", "AHU-02", "VAV-01"])
print(equipment[0])   # AHU-01
print(len(equipment)) # 3
```

## 19. Protocol Version

```python
class Startable(Protocol):
    def start(self) -> None: ...

class Fan:
    def start(self):
        print("Fan started")
```

## 20. Comparison Table

| Concept | Purpose |
|---------|---------|
| `ABC` | Explicit hierarchy |
| `abstractmethod` | Required implementation |
| `collections.abc` | Standard interfaces |
| `Protocol` | Structural typing |
| `register()` | Virtual subclass |
| `@runtime_checkable` | Limited runtime check |

## 21. ABC + Dataclass

```python
@dataclass
class Equipment(ABC):
    equipment_id: str

    @abstractmethod
    def start(self):
        pass

@dataclass
class AHU(Equipment):
    temperature: float

    def start(self):
        print(f"{self.equipment_id} started")

ahu = AHU("AHU-01", 22.5)
```

## 22. Architecture

```
ABC → Inheritance-oriented
Protocol → Capability-oriented
collections.abc → Standard interfaces
```

## 23. HVAC Example

```python
class Startable(Protocol):
    def start(self) -> None: ...

class AHU:
    def start(self):
        print("AHU ON")

def start_device(device: Startable):
    device.start()

start_device(AHU())
```

## 24. Final Mental Map

```
ABC → explicit inheritance + contract
Protocol → structural typing
collections.abc → standard capabilities
```

**One-line:** ABC → "hierarchy ka member bano"; Protocol → "capability do".

---

# Lesson 45: `list` vs `deque` vs `set` vs `dict`

## 1. `list`

```python
numbers = [10, 20, 30, 40]
numbers[0]        # 10
numbers.append(50)
```

**Complexity:**
| Op | Complexity |
|----|-----------|
| `items[i]` | O(1) |
| `append()` | O(1) amortized |
| `pop()` | O(1) end |
| `insert(0, x)` | O(n) |
| `pop(0)` | O(n) |
| `x in list` | O(n) |

## 2. List Front Problem

```python
queue = [1, 2, 3, 4, 5]
queue.pop(0)   # Elements shift
```

## 3. `deque`

```python
from collections import deque

queue = deque([1, 2, 3])
queue.append(4)
queue.appendleft(0)
# [0, 1, 2, 3, 4]

queue.pop()        # 4
queue.popleft()    # 0
```

## 4. `list` vs `deque`

```
list → mostly RIGHT efficient
deque → BOTH ends efficient
```

## 5. Queue Example

```python
from collections import deque

work_orders = deque()
work_orders.append("WO-1001")
work_orders.append("WO-1002")

wo = work_orders.popleft()   # WO-1001
```

## 6. Stack

```python
stack = []
stack.append("A")
stack.append("B")
stack.append("C")
stack.pop()   # "C"
```

```
Queue → deque
Stack → list
```

## 7. `set`

```python
numbers = {10, 20, 30}
# {10, 20, 30}

numbers = {10, 20, 20, 30}
# {10, 20, 30}
```

## 8. Set Membership

```python
20 in numbers   # O(1) average
```

## 9. Set Kab

```python
equipment_ids = {"AHU-01", "AHU-02", "VAV-01"}
if "AHU-01" in equipment_ids:
    print("Already exists")
```

## 10. Set Indexing Nahi

```python
numbers[0]   # Error
```

## 11. Set Operations

```python
a = {1, 2, 3}
b = {3, 4, 5}

a | b   # {1, 2, 3, 4, 5}
a & b   # {3}
a - b   # {1, 2}
a ^ b   # {1, 2, 4, 5}
```

## 12. `dict`

```python
employee = {
    "name": "Ali",
    "salary": 5000,
    "department": "HVAC"
}
print(employee["name"])   # Ali
```

## 13. Dict Complexity

| Op | Typical |
|----|---------|
| lookup | O(1) |
| insert | O(1) |
| update | O(1) |
| delete | O(1) |

## 14. `dict` vs `set`

```
dict → key → value
set → value
```

## 15. `defaultdict`

```python
from collections import defaultdict

data = defaultdict(list)
data["HVAC"].append("AHU-01")
data["HVAC"].append("AHU-02")
data["Electrical"].append("DB-01")

# {"HVAC": ["AHU-01", "AHU-02"], "Electrical": ["DB-01"]}
```

## 16. Work-Order Grouping

```python
work_orders_by_floor = defaultdict(list)
work_orders_by_floor["Floor 34"].append("WO-1001")
work_orders_by_floor["Floor 34"].append("WO-1002")
```

## 17. `defaultdict(int)`

```python
count = defaultdict(int)
count["AHU"] += 1
count["AHU"] += 1
count["VAV"] += 1
# {"AHU": 2, "VAV": 1}
```

## 18. `Counter`

```python
from collections import Counter

equipment = ["AHU", "VAV", "AHU", "FCU", "AHU", "VAV"]
counter = Counter(equipment)
# AHU → 3, VAV → 2, FCU → 1
```

## 19. `most_common`

```python
counter.most_common(2)
# [("AHU", 3), ("VAV", 2)]
```

## 20. `Counter` vs `defaultdict(int)`

```
defaultdict(int) → general counting
Counter → dedicated frequency
```

## 21. `OrderedDict`

```python
from collections import OrderedDict

# Modern dict already ordered
od = OrderedDict()
od.move_to_end("key")
```

## 22. `namedtuple`

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x)   # 10
```

## 23. Comparison Table

| Structure | Purpose |
|-----------|---------|
| `list` | ordered collection |
| `deque` | both-ends operations |
| `set` | unique values |
| `dict` | key → value |
| `defaultdict` | auto defaults |
| `Counter` | frequency |

## 24. Decision Tree

```
Ordered → list
Both-ends → deque
Unique → set
Key lookup → dict
Auto defaults → defaultdict
Frequency → Counter
```

## 25. Performance Mental Model

```
list → index fast, front slow
deque → both ends fast
set → membership fast
dict → key lookup fast
```

## 26. Work-Order Architecture

```python
work_orders_by_id = {}       # dict lookup
processed_ids = set()        # uniqueness
pending = deque()            # queue
by_floor = defaultdict(list) # grouping
counts = Counter()           # counting
```

## 27. Decision

```
"Data hai to list" ❌
"Mujhe kya operation karna hai?" ✅
```

## 28. Duplicates Remove

```python
equipment_ids = ["AHU-01", "AHU-02", "AHU-01"]
unique_ids = list(dict.fromkeys(equipment_ids))
# ["AHU-01", "AHU-02"]
```

## 29. Big Picture

```
collections.abc → capability
collections → concrete structures
```

## 30. Quick Revision

```
list → ordered + mutable
deque → double-ended queue
set → unique + membership
dict → key → value
defaultdict → dict + default
Counter → frequency
```

---

# Lesson 46: Hashing + `__hash__()` + `__eq__()`

## 1. Hash

```python
hash("AHU-01")   # Some integer
```

**Explanation:**
- Object → hash() → integer

## 2. `hash()` Function

```python
hash(100)         # OK
hash("hello")     # OK
hash((1, 2))      # OK
hash([1, 2])      # TypeError: unhashable
```

## 3. Hashable

```python
10              # Hashable
"AHU-01"        # Hashable
(1, 2)          # Hashable
frozenset({1, 2})  # Hashable
```

## 4. Unhashable

```python
hash([1, 2, 3])   # TypeError
hash({"a": 1})    # TypeError
```

## 5. Hashing Use

```python
equipment = {
    "AHU-01": "Running",
    "AHU-02": "Stopped"
}
equipment["AHU-01"]   # Fast lookup
```

## 6. Hash Table Mental Model

```
"AHU-01"
    ↓
  hash
    ↓
some integer
    ↓
table location
    ↓
stored value
```

## 7. Set Membership

```python
equipment_ids = {"AHU-01", "AHU-02"}
"AHU-02" in equipment_ids   # Fast
```

## 8. Hash Collision

```
object A → hash 100
object B → hash 100
```

**Explanation:**
- Same hash → equality check

## 9. `__eq__()`

```python
class Employee:
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __eq__(self, other):
        return self.employee_id == other.employee_id

e1 = Employee("E001")
e2 = Employee("E001")
print(e1 == e2)   # True
```

## 10. `__hash__()`

```python
class Employee:
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __hash__(self):
        return hash(self.employee_id)

e1 = Employee("E001")
print(hash(e1))
```

## 11. `__eq__` + `__hash__` Rule

```
a == b → hash(a) == hash(b)
```

## 12. Reverse Not Required

```
hash(a) == hash(b) → a == b NOT required
```

## 13. Complete Example

```python
class Employee:
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return self.employee_id == other.employee_id

    def __hash__(self):
        return hash(self.employee_id)

e1 = Employee("E001")
e2 = Employee("E001")
e3 = Employee("E002")

print(e1 == e2)              # True
print(hash(e1) == hash(e2))  # True
```

## 14. Set Effect

```python
employees = {e1, e2, e3}
# e1 and e2 duplicate → only one remains
```

## 15. Dict Key

```python
data = {e1: "Manager"}
print(data[e2])   # Manager (same logical key)
```

## 16. Mutable Object Problem

```python
e = Employee("E001")
employees = {e}

e.employee_id = "E999"   # Hash changes!
# Lookup inconsistent
```

## 17. Dangerous Mutable Keys

```
insert → hash based on state A
state changes → hash based on state B
lookup inconsistency
```

## 18. Tuple Hashable

```python
hash((1, 2, 3))        # OK
hash(([1, 2], 3))      # Error (list inside)
```

## 19. Immutable Relation

```
immutable → stable hash possible
but immutable ≠ automatically hashable
```

## 20. `str` Hashable

```python
hash("AHU-01")   # OK
equipment = {"AHU-01": "ON"}
```

## 21. `int` Hashable

```python
hash(100)   # OK
data = {100: "AHU"}
```

## 22. `list` Unhashable

```python
data = {[1, 2, 3]: "test"}   # Error
```

## 23. `frozenset`

```python
fs = frozenset({1, 2})
hash(fs)   # OK
```

## 24. Default Class Behavior

```python
class Employee:
    pass

e1 = Employee()
e2 = Employee()
print(e1 == e2)   # False (identity)
```

## 25. `__eq__` Override

```python
class Employee:
    def __eq__(self, other):
        return self.employee_id == other.employee_id

e = Employee("E001")
hash(e)   # TypeError: unhashable (without __hash__)
```

## 26. Kyun?

```
Custom equality + uncertain hash state
= hash-based collection dangerous
```

## 27. Dataclass

```python
@dataclass
class Employee:
    employee_id: str
    salary: float
```

## 28. Frozen Dataclass

```python
@dataclass(frozen=True)
class Employee:
    employee_id: str
    salary: float

e = Employee("E001", 5000)
# e.salary = 6000  # Error
```

## 29. Hash + Equality Model

```
Object
├── __eq__() → "same hai?"
└── __hash__() → "hash kya?"
     ↓
set / dict
```

## 30. Dict Lookup

```
"AHU-01"
    ↓
hash()
    ↓
candidate location
    ↓
key comparison
    ↓
"Running"
```

## 31. Set Membership

```
"AHU-01" in ids
    ↓
hash
    ↓
candidate location
    ↓
equality check if needed
    ↓
True
```

## 32. `O(1)` Meaning

```
dict lookup → average O(1)
set membership → average O(1)
list membership → O(n)
```

## 33. `O(1)` Magic Nahi

```
Average-case O(1)
Worst-case nuanced
```

## 34. Work-Order Project

```python
work_orders_by_id = {
    "WO-1001": {...},
    "WO-1002": {...},
}
work_orders_by_id["WO-500000"]   # Fast
```

## 35. Processed IDs

```python
processed_ids = set()
if equipment_id in processed_ids:
    ...
```

## 36. Golden Rules

```
1. a == b → hash(a) == hash(b)

2. Same hash ≠ equal

3. Hash-based collection mein state mutate mat karo

4. Mutable objects normally unhashable
```

## 37. `is` vs `==`

```python
a = [1, 2]
b = [1, 2]
a == b   # True (value)
a is b   # False (identity)
```

## 38. Final Architecture

```
set / dict
    ↓
hashing
    ↓
__hash__ + __eq__
    ↓
candidate location + equality check
```

## 39. Quick Revision

```
hash() → hash value
__eq__() → equality
__hash__() → hash
set → hash + equality
dict → hash + equality
hashable → set member / dict key
unhashable → list, dict, set
```

**Key Point:** `dict` aur `set` fast hone ka core idea hash table hai.

---

# Lesson 47: `copy` vs `deepcopy` + References

## 1. Variable = Reference

```python
a = [10, 20, 30]
```

```
a ───────→ [10, 20, 30]
```

## 2. `b = a`

```python
a = [10, 20, 30]
b = a
```

```
a ─────┐
       ↓
   SAME LIST
       ↑
b ─────┘
```

## 3. `is` Check

```python
a = [10, 20, 30]
b = a
print(a is b)   # True
```

## 4. Mutation

```python
a = [10, 20, 30]
b = a
a.append(40)
print(b)   # [10, 20, 30, 40]
```

## 5. `b = a` Copy Nahi

```
b = a → same object + second reference
```

## 6. `copy()`

```python
a = [10, 20, 30]
b = a.copy()
```

```
a ─────→ [10, 20, 30]
b ─────→ [10, 20, 30]
```

## 7. `is` vs `==`

```python
print(a is b)   # False
print(a == b)   # True
```

## 8. Independent Mutation

```python
a = [10, 20, 30]
b = a.copy()
a.append(40)
print(a)   # [10, 20, 30, 40]
print(b)   # [10, 20, 30]
```

## 9. Shallow Copy

```python
import copy
a = [1, 2, 3]
b = copy.copy(a)
```

## 10. Nested List

```python
a = [[1, 2], [3, 4]]
b = a.copy()
```

```
a → outer list → [1, 2], [3, 4]
b → new outer → SAME inner objects
```

## 11. Proof

```python
a = [[1, 2], [3, 4]]
b = a.copy()
print(a is b)         # False
print(a[0] is b[0])   # True
```

## 12. Problem

```python
a[0].append(99)
print(a)   # [[1, 2, 99], [3, 4]]
print(b)   # [[1, 2, 99], [3, 4]] (same!)
```

## 13. `deepcopy`

```python
import copy
b = copy.deepcopy(a)
```

```
a → outer → inner A, inner B
b → NEW outer → NEW inner A, NEW inner B
```

## 14. Deepcopy Example

```python
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
a[0].append(99)
print(a)   # [[1, 2, 99], [3, 4]]
print(b)   # [[1, 2], [3, 4]]
```

## 15. Three Concepts

```python
b = a                # outer same, inner same
b = a.copy()         # outer diff, inner same
b = copy.deepcopy(a) # outer diff, inner diff
```

## 16. Diagram

```
b = a → same
b = a.copy() → outer new, inner shared
b = deepcopy(a) → all new
```

## 17. `copy.copy()` vs `.copy()`

```python
import copy
b = copy.copy(a)   # Generic
b = a.copy()       # Specific
```

## 18. Dictionary

```python
data = {"name": "Ali", "salary": 5000}
new_data = data.copy()
```

## 19. Nested Dictionary

```python
data = {"employee": {"name": "Ali"}}
new_data = data.copy()
print(data["employee"] is new_data["employee"])   # True
```

## 20. Deepcopy Dictionary

```python
new_data = copy.deepcopy(data)
print(data["employee"] is new_data["employee"])   # False
```

## 21. Work Order Example

```python
work_order = {
    "number": "WO-1001",
    "equipment": {"id": "AHU-01", "status": "OFF"}
}

new_order = work_order.copy()
new_order["equipment"]["status"] = "ON"
print(work_order["equipment"]["status"])   # ON (shared!)
```

## 22. Deepcopy

```python
new_order = copy.deepcopy(work_order)
new_order["equipment"]["status"] = "ON"
print(work_order["equipment"]["status"])   # OFF
```

## 23. Deepcopy Har Waqt Nahi

```
Deepcopy → memory + CPU + complex
Pehle decide: kitni independence chahiye?
```

## 24. Immutable Objects

```python
x = 10
x = 20   # Rebind, not mutate
```

## 25. Assignment vs Mutation

```python
x = 10
x = 20       # Assignment

items = [1, 2]
items.append(3)   # Mutation
```

## 26. Mutable vs Immutable

```
Mutable → list, dict, set
Immutable → str, int, tuple, frozenset
```

## 27. Tuple Subtle

```python
t = ([1, 2], [3, 4])
# t[0] = [100, 200]   # Error
t[0].append(99)        # OK
# ([1, 2, 99], [3, 4])
```

## 28. Shallow Copy Mental Model

```
outer container → COPY
inner objects → shared references
```

## 29. Deep Copy Mental Model

```
outer → copy
inner → copy
deeper → copy
```

## 30. Circular Reference

```python
a = []
a.append(a)
# deepcopy handles via memo
```

## 31. Dataclass

```python
@dataclass
class Equipment:
    equipment_id: str
    tags: list[str] = field(default_factory=list)

ahu1 = Equipment("AHU-01", ["HVAC"])
ahu2 = copy.copy(ahu1)
ahu2.tags.append("BMS")
print(ahu1.tags)   # ["HVAC", "BMS"] (shared!)
```

## 32. Deepcopy Dataclass

```python
ahu2 = copy.deepcopy(ahu1)
ahu2.tags.append("BMS")
print(ahu1.tags)   # ["HVAC"]
```

## 33. Copy Protocol

```python
class Equipment:
    def __copy__(self): ...
    def __deepcopy__(self, memo): ...
```

## 34. Copy vs `=`

```python
b = a                # NO COPY
b = copy.copy(a)     # SHALLOW COPY
b = copy.deepcopy(a) # DEEP COPY
```

## 35. Practical Example

```python
import copy

equipment = {
    "id": "AHU-01",
    "points": {"temperature": 22.5, "damper": 50}
}

a = equipment              # same
b = equipment.copy()       # outer new, inner shared
c = copy.deepcopy(equipment)  # all new
```

## 36. Quick Test

```python
a = {"x": [1, 2]}
b = a
c = a.copy()
d = copy.deepcopy(a)

print(a is b)         # True
print(a is c)         # False
print(a["x"] is c["x"])  # True
print(a["x"] is d["x"])  # False
```

## 37. Work-Order Rule

```python
# Read only
for row in rows: ...

# Independent outer
new_rows = rows.copy()

# Fully independent
new_rows = copy.deepcopy(rows)
```

## 38. Final Mental Model

```
= → same object
copy.copy() → shallow
copy.deepcopy() → recursive
```

**One-line:** `=` reference deta hai, `.copy()` shallow, `deepcopy()` recursive independent copy.

---

# Lesson 48: Memory Management + Reference Counting + GC

## 1. Object Memory

```python
x = [10, 20, 30]
```

```
x ─────→ [10, 20, 30]
```

## 2. Multiple References

```python
x = [10, 20, 30]
y = x
z = x
```

```
x ────→ object
y ────→ object
z ────→ object
```

## 3. Reference Count

```python
import sys
x = [10, 20, 30]
print(sys.getrefcount(x))
```

## 4. Reference Remove

```python
x = [10, 20, 30]
y = x
z = x
del y
# 2 references remain
```

## 5. `del x`

```python
x = [10, 20, 30]
y = x
del x
# Object still exists via y
```

## 6. Last Reference

```python
x = [10, 20, 30]
y = x
del x
del y
# No reference → deallocate
```

## 7. GC

```python
a = []
b = []
a.append(b)
b.append(a)
```

```
a → b
↑   ↓
└───┘
```

## 8. Circular Reference

```python
a = []
b = []
a.append(b)
b.append(a)

del a
del b
# Cyclic garbage
```

## 9. GC Role

```python
import gc
gc.collect()
```

## 10. Reference Counting vs GC

```
Reference counting → count 0 → dealloc
Cyclic GC → cycle detect → cleanup
```

## 11. `gc.get_count()`

```python
import gc
print(gc.get_count())
# (100, 5, 2)
```

## 12. `gc.collect()`

```python
collected = gc.collect()
print(collected)
```

## 13. `__del__()`

```python
class Employee:
    def __del__(self):
        print("Object cleanup")
```

**Warning:**
- Deterministic resource management ke liye nahi

## 14. `__del__()` Destructor Nahi

```
__del__ → finalization hook
C++ destructor ≠ Python __del__
```

## 15. File ke Liye `__del__()` Mat

```python
# Bad
class FileManager:
    def __del__(self):
        self.file.close()

# Good
with open("data.txt") as file:
    data = file.read()
```

## 16. Memory vs Resource Cleanup

```
Memory → GC
Files/locks → with / try-finally
```

## 17. Weak Reference

```python
import weakref

class Equipment:
    pass

equipment = Equipment()
weak_equipment = weakref.ref(equipment)
```

## 18. Weak Ref After Del

```python
del equipment
print(weak_equipment())   # None
```

## 19. Weak Ref Use

```
caches
registries
observer patterns
non-owning references
```

## 20. `WeakValueDictionary`

```python
from weakref import WeakValueDictionary
registry = WeakValueDictionary()
registry["AHU-01"] = ahu
```

## 21. HVAC Example

```python
registry["AHU-01"] = ahu
# Weak ref → object alive nahi rakhta
```

## 22. `weakref.ref`

```python
weak_equipment()   # Target return
```

## 23. Callback

```python
weakref.ref(obj, callback)
```

## 24. `id()`

```python
x = []
print(id(x))
```

**Note:** Identity, not necessarily raw memory address.

## 25. Object Lifetime

```
create → refs → reachable
remove refs → unreachable
ref counting + GC → cleanup
```

## 26. `del` Properly

```python
a = []
b = a
del a   # Binding remove, object alive via b
```

## 27. `del` Contexts

```python
del a                # Name remove
del obj.attribute    # Attribute remove
del items[0]         # Item remove
```

## 28. Previous Lessons Connection

```
b = a → same object
b = a.copy() → shallow
b = deepcopy → recursive
ref counting → alive
GC → cycles
weakref → non-owning
with → resource lifecycle
```

## 29. Complete Example

```python
import weakref

class Equipment:
    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

ahu = Equipment("AHU-01")
weak_ahu = weakref.ref(ahu)

print(weak_ahu().equipment_id)   # AHU-01
del ahu
print(weak_ahu())   # None
```

## 30. Reference vs Ownership

```
Strong ref → alive rakhta hai
Weak ref → observe only
```

## 31. Final Diagram

```
Object
├── Strong refs → alive
└── Weak refs → observe
     ↓
No strong → unreachable
     ↓
ref counting + cyclic GC
     ↓
cleanup
```

## 32. Golden Rules

```
1. del x ≠ immediate destruction
2. b = a ≠ copy
3. Reference counting prompt
4. Cyclic GC cycles
5. __del__ ≠ deterministic cleanup
6. Files → with
7. weakref doesn't keep alive
8. id() ≠ raw address
```

---

# Lesson 49: Python Exceptions

## 1. Exception

```python
x = 10
y = 0
result = x / y
# ZeroDivisionError
```

## 2. Exception Hierarchy

```
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── ValueError
    ├── TypeError
    ├── KeyError
    └── ...
```

## 3. `BaseException` vs `Exception`

```python
# Normally
except Exception:
    ...

# Not blindly
except BaseException:
    ...
```

## 4. Basic `try/except`

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Zero se divide nahi kar sakte")
```

## 5. `try`

```python
try:
    number = int(input("Number: "))
except ValueError:
    print("Valid number enter karo")
```

## 6. `except`

```python
try:
    number = int("abc")
except ValueError:
    print("Conversion failed")
```

## 7. Multiple Exceptions

```python
try:
    value = data["temperature"]
    result = 100 / value
except KeyError:
    print("Temperature key missing")
except ZeroDivisionError:
    print("Temperature zero hai")
```

## 8. Multiple Types

```python
except (ValueError, TypeError):
    print("Invalid input")
```

## 9. `Exception as e`

```python
try:
    number = int("abc")
except ValueError as e:
    print(e)
```

## 10. `type(e)`

```python
try:
    int("abc")
except Exception as e:
    print(type(e))   # <class 'ValueError'>
    print(str(e))
```

## 11. `raise`

```python
age = -5
if age < 0:
    raise ValueError("Age negative nahi ho sakti")
```

## 12. `raise` Use

```python
def set_temperature(temp):
    if temp < -273.15:
        raise ValueError("Invalid temperature")
    return temp
```

## 13. `raise` vs `return`

```
return → caller ko result
raise → caller ko exception
```

## 14. Custom Exception

```python
class InvalidTemperatureError(Exception):
    pass

def set_temperature(temp):
    if temp < -273.15:
        raise InvalidTemperatureError("Temperature invalid hai")
```

## 15. Custom Kyun

```
InvalidTemperature
InvalidDamperPosition
EquipmentOffline
CommunicationFailure
```

## 16. Exception Inheritance

```python
class EquipmentError(Exception):
    pass

class EquipmentOfflineError(EquipmentError):
    pass

class CommunicationError(EquipmentError):
    pass
```

## 17. `finally`

```python
try:
    print("Work")
except Exception:
    print("Error")
finally:
    print("Cleanup")
```

## 18. `try + except + finally`

```python
try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError:
    print("File nahi mili")
finally:
    print("Operation finished")
```

## 19. `else`

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error")
else:
    print("Calculation successful")
```

## 20. Complete Structure

```
try → success/error
except → error handling
else → success-only
finally → cleanup
```

## 21. `else` Benefit

```python
try:
    data = load_data()
except ValueError:
    print("Loading failed")
else:
    process_data(data)
```

## 22. Exception Propagation

```python
def divide(a, b):
    return a / b

def calculate():
    return divide(10, 0)

calculate()
# Exception propagates up
```

## 23. Caller Catch

```python
try:
    result = divide(10, 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
```

## 24. Propagation Diagram

```
main → calculate → divide → Error
       ↑
       no handler
main → handler
```

## 25. `raise` Inside `except`

```python
try:
    value = int("abc")
except ValueError as e:
    print("Logging:", e)
    raise
```

## 26. `raise` vs `raise e`

```python
# Preferred
except ValueError:
    raise

# Explicit
except ValueError as e:
    raise e
```

## 27. `raise ... from ...`

```python
try:
    number = int("abc")
except ValueError as e:
    raise RuntimeError("Data processing failed") from e
```

## 28. `from` Kyun

```python
try:
    value = int("abc")
except ValueError as e:
    raise RuntimeError("Work order data invalid hai") from e
```

## 29. `raise ... from None`

```python
try:
    ...
except ValueError:
    raise RuntimeError("Invalid configuration") from None
```

## 30. `__cause__`

```python
try:
    int("abc")
except ValueError as e:
    try:
        raise RuntimeError("Failed") from e
    except RuntimeError as new_error:
        print(new_error.__cause__)
```

## 31. `__context__`

```python
try:
    int("abc")
except ValueError:
    {}["missing"]
# Second exception context
```

## 32. Work-Order Example

```python
def create_folder(work_order_number):
    if not work_order_number:
        raise ValueError("Work Order Number missing")
    ...

try:
    create_folder("")
except ValueError as e:
    print("Invalid work order:", e)
```

## 33. Custom Architecture

```python
class WorkOrderError(Exception):
    pass

class MissingWorkOrderNumberError(WorkOrderError):
    pass

class InvalidWorkOrderNumberError(WorkOrderError):
    pass
```

## 34. `except Exception` Overuse

```python
# Bad
try:
    create_folder()
except Exception:
    pass
```

## 35. Better

```python
try:
    create_folder()
except PermissionError:
    print("Permission denied")
except FileNotFoundError:
    print("Path nahi mili")
```

## 36. `except` Order

```python
# Specific → general
try:
    ...
except ValueError:
    ...
except Exception:
    ...
```

## 37. Good Pattern

```python
try:
    data = load_data()
except FileNotFoundError:
    print("File missing")
except ValueError:
    print("Invalid data")
else:
    process_data(data)
finally:
    cleanup()
```

## 38. `return` + `finally`

```python
def test():
    try:
        return "try"
    finally:
        print("finally")

print(test())
# finally
# try
```

## 39. `finally` `return` Avoid

```python
def test():
    try:
        return "try"
    finally:
        return "finally"
# Returns "finally"
```

## 40. Final Mental Model

```
Exception → raise
search stack → except
handle / transform / re-raise

try → error → except
     → success → else
     → finally
```

## 41. Golden Rules

```
1. raise → exception signal
2. return → normal value
3. except → handle
4. else → success
5. finally → cleanup
6. raise → re-raise
7. raise NewError from e → chaining
8. Specific exceptions prefer
9. except Exception: pass → bad
10. Resource cleanup → with
```

---

# Lesson 50: Custom Exceptions + `ExceptionGroup` + `except*`

## 1. Custom Kyun

```
Work Order missing
Equipment ID missing
Invalid Floor
Folder creation failed
```

## 2. Exception Hierarchy

```python
class WorkOrderError(Exception):
    pass

class ValidationError(WorkOrderError):
    pass

class MissingWorkOrderError(ValidationError):
    pass

class InvalidWorkOrderError(ValidationError):
    pass
```

## 3. Faida

```python
except WorkOrderError:              # Whole family
except MissingWorkOrderError:       # Specific
```

## 4. Custom Message

```python
class WorkOrderError(Exception):
    pass

raise WorkOrderError("Work order process failed")
```

## 5. Custom Data

```python
class WorkOrderError(Exception):
    def __init__(self, work_order_number, message):
        self.work_order_number = work_order_number
        self.message = message
        super().__init__(message)

raise WorkOrderError("WO-1001", "Folder create nahi hua")

try:
    ...
except WorkOrderError as e:
    print(e.work_order_number)
    print(e.message)
```

## 6. `super().__init__(message)`

```python
super().__init__(message)
# print(e) → message
```

## 7. Work Order Example

```python
class MissingWorkOrderError(WorkOrderError):
    def __init__(self, row_number):
        self.row_number = row_number
        super().__init__(f"Work Order missing at row {row_number}")

raise MissingWorkOrderError(15)
```

## 8. Exception as Data

```python
class EquipmentError(Exception):
    def __init__(self, equipment_id, message):
        self.equipment_id = equipment_id
        super().__init__(message)
```

## 9. `__str__()` Customize

```python
class EquipmentError(Exception):
    def __init__(self, equipment_id, message):
        self.equipment_id = equipment_id
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.equipment_id}: {self.message}"
```

## 10. Architecture

```
Exception
└── WorkOrderError
    ├── ValidationError
    │   ├── MissingFieldError
    │   └── InvalidFieldError
    ├── FileOperationError
    └── DataSourceError
```

## 11. Exception Translation

```python
try:
    open(path)
except FileNotFoundError as e:
    raise FileOperationError(f"Work order folder unavailable: {path}") from e
```

## 12. Exception Chaining

```python
raise FileOperationError("Folder unavailable") from e
```

## 13. `ExceptionGroup`

```python
errors = [
    ValueError("Invalid floor"),
    ValueError("Missing equipment ID"),
]

raise ExceptionGroup("Work order validation failed", errors)
```

## 14. `except ExceptionGroup`

```python
try:
    raise ExceptionGroup("Validation errors", [ValueError("Bad floor"), TypeError("Bad equipment ID")])
except ExceptionGroup as eg:
    print(eg)
```

## 15. `except*`

```python
try:
    raise ExceptionGroup("Errors", [ValueError("Bad floor"), TypeError("Bad ID")])
except* ValueError as e:
    print("Value errors:", e)
except* TypeError as e:
    print("Type errors:", e)
```

## 16. `except` vs `except*`

```
except → one exception
except* → exception group matching
```

## 17. Batch Validation

```python
errors = []
for order in orders:
    try:
        validate(order)
    except Exception as e:
        errors.append(e)

if errors:
    raise ExceptionGroup("Batch validation failed", errors)
```

## 18. Faida

```
WO-1001 → OK
WO-1002 → Error
WO-1003 → Error
        ↓
ExceptionGroup
```

## 19. Nested Groups

```
ExceptionGroup
├── ValidationError
├── ExceptionGroup
│   ├── ValueError
│   └── TypeError
└── FileNotFoundError
```

## 20. `except*` Difference

```
except* → matching exceptions extract
```

## 21. Mix Nahi

```python
# Ek try mein except aur except* mix nahi
```

## 22. Version

```
ExceptionGroup + except* → Python 3.11+
```

## 23. Custom ExceptionGroup

```python
raise ExceptionGroup("Work Order errors", [MissingWorkOrderError(...), InvalidWorkOrderError(...)])
```

## 24. Har Jagah Nahi

```
Ek error → normal exception
Multiple independent → ExceptionGroup
```

## 25. Async Connection

```
Task 1 → ValueError
Task 2 → TimeoutError
Task 3 → ConnectionError
     ↓
ExceptionGroup
```

## 26. `TaskGroup`

```python
import asyncio

async def task1():
    raise ValueError("Task 1 failed")

async def main():
    async with asyncio.TaskGroup() as group:
        group.create_task(task1())

asyncio.run(main())
```

## 27. Handle Async

```python
try:
    await main()
except* ValueError as e:
    print("Value errors:", e)
```

## 28. Work-Order Best Design

```python
class WorkOrderError(Exception):
    pass

class MissingWorkOrderNumberError(WorkOrderError):
    pass

class InvalidWorkOrderNumberError(WorkOrderError):
    pass

class FolderCreationError(WorkOrderError):
    pass

errors = []
for row_number, row in enumerate(rows, start=2):
    try:
        process_work_order(row)
    except WorkOrderError as e:
        errors.append(e)

if errors:
    raise ExceptionGroup("Work order processing failed", errors)
```

## 29. Final Mental Model

```
Exception → Built-in / Custom
Custom → WorkOrderError → ValidationError
One op → except
Many ops → ExceptionGroup → except*
```

## 30. Golden Rules

```
1. Custom → application meaning
2. Hierarchy → related errors
3. raise ... from e → cause preserve
4. ExceptionGroup → multiple exceptions
5. except* → match group members
6. Simple error → normal Exception
7. Batch → ExceptionGroup
8. Custom mein context store
```

---

**Ab ye guide complete hai (Lessons 41-50).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ Golden rules

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀