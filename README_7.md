# Python OOP — Lessons 61-70 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 61: `Generic` + `TypeVar` + `Protocol` + Variance

## 1. Problem

```python
def get_first(items):
    return items[0]

print(get_first([10, 20, 30]))   # 10
print(get_first(["Ali", "Ahmed"]))  # Ali
```

**Explanation:**
- Runtime sahi
- Lekin type checker ko type information nahi

## 2. `TypeVar`

```python
from typing import TypeVar

T = TypeVar("T")

def get_first(items: list[T]) -> T:
    return items[0]
```

**Explanation:**
- `T` → placeholder
- `list[int]` → `T = int` → output `int`
- `list[str]` → `T = str` → output `str`

## 3. Faida

```python
# Bad
def get_first(items: list) -> object:
    ...

# Good
T = TypeVar("T")

def get_first(items: list[T]) -> T:
    return items[0]
```

**Explanation:**
- Input-output relationship preserve

## 4. `Generic`

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

int_box = Box[int](100)
name_box = Box[str]("Ali")
```

## 5. `Generic[T]`

```python
class Box(Generic[T]):
```

**Explanation:**
- `Box[int]`, `Box[str]`, `Box[User]` possible

## 6. Practical Example

```python
class Response(Generic[T]):
    def __init__(self, data: T):
        self.data = data

    def get_data(self) -> T:
        return self.data

response = Response[int](200)
# response.get_data() → int
```

## 7. `Protocol`

```python
from typing import Protocol

class Savable(Protocol):
    def save(self) -> None:
        ...

class User:
    def save(self) -> None:
        print("User saved")
```

**Explanation:**
- `User` inherit nahi kiya
- Structure match → compatible

## 8. Structural vs Inheritance

```python
# Inheritance
class User(Savable):
    ...

# Structural
class User:
    def save(self) -> None:
        ...
```

```
Inheritance → "I am a Savable"
Protocol → "I behave like Savable"
```

## 9. Generic + Protocol

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...
    def get(self) -> T:
        ...

class UserRepository:
    def save(self, item: User) -> None:
        print("Saving user")
    def get(self) -> User:
        return User()
```

## 10. Problem: Direction

```python
def save(self, item: T): ...  # T input
def get(self) -> T: ...        # T output
```

**Explanation:**
- T input + output dono
- Variance concept

## 11. Variance

```
Covariance
Contravariance
Invariance
```

## 12. Covariance

```
Dog → Animal
Box[Dog] → Box[Animal]  (same direction)
```

## 13. Covariant TypeVar

```python
T_co = TypeVar("T_co", covariant=True)

class Producer(Generic[T_co]):
    def get(self) -> T_co:
        ...
```

**Explanation:**
- Data produce karta hai
- `Producer[Dog]` → `Producer[Animal]` safe

## 14. Contravariance

```python
T_contra = TypeVar("T_contra", contravariant=True)

class Consumer(Generic[T_contra]):
    def consume(self, item: T_contra) -> None:
        ...
```

**Explanation:**
- Input leta hai
- `Consumer[Animal]` → `Consumer[Dog]`

## 15. Real-life

```python
class Animal: pass
class Dog(Animal): pass

class AnimalHandler:
    def handle(self, animal: Animal):
        print("Handling animal")

dog = Dog()
handler.handle(dog)   # OK
```

## 16. Invariance

```
Dog → Animal
Box[Dog] ✕ Box[Animal]
```

**Explanation:**
- Mutable containers
- `list[Dog]` ≠ `list[Animal]`

## 17. Generic + Protocol + Variance

```python
T_co = TypeVar("T_co", covariant=True)

class Producer(Protocol[T_co]):
    def produce(self) -> T_co:
        ...

class Email: pass

class EmailProducer:
    def produce(self) -> Email:
        return Email()
```

## 18. Consumer

```python
T_contra = TypeVar("T_contra", contravariant=True)

class Consumer(Protocol[T_contra]):
    def consume(self, item: T_contra) -> None:
        ...

class MessageConsumer:
    def consume(self, item: object) -> None:
        print("Processing message")
```

## 19. Diagram

```
Animal
/      \
Dog      Cat

COVARIANCE:
Producer[Dog] → Producer[Animal]

CONTRAVARIANCE:
Consumer[Animal] → Consumer[Dog]

INVARIANCE:
Box[Dog] ✕ Box[Animal]
```

## 20. `Generic` vs `Protocol`

```
Generic → type parameterization
Protocol → required behavior
```

## 21. Combine Kyun

```
Behavior + Type preserve
```

## 22. Practical Architecture

```python
T = TypeVar("T")

class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...
    def get(self, item_id: str) -> T:
        ...
```

```
Repository[Equipment]
Repository[WorkOrder]
Repository[Employee]
```

## 23. Loose Coupling

```python
def process_equipment(repo: Repository[Equipment]):
    equipment = repo.get("AHU-001")
    ...
```

**Explanation:**
- Database/API/Sheets unknown
- Sirf `Repository[Equipment]` required

## 24. TypeVar Bound

```python
T = TypeVar("T", bound=Equipment)
```

**Explanation:**
- `Equipment` ya subclass

## 25. Bound vs Constraints

```python
# Bound
T = TypeVar("T", bound=Animal)

# Constraints
T = TypeVar("T", int, str)
```

```
Bound → family ke subtypes
Constraints → specified options
```

## 26. Generic + Bound

```python
T = TypeVar("T", bound=Equipment)

class EquipmentRepository(Generic[T]):
    def save(self, equipment: T) -> None:
        print("Saving equipment")
```

## 27. Protocol + Generic + Bound

```python
T = TypeVar("T", bound=Equipment)

class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...
    def get(self, item_id: str) -> T:
        ...
```

## 28. Complete Architecture

```python
T = TypeVar("T", bound=Equipment)

class Repository(Protocol[T]):
    def save(self, item: T) -> None: ...
    def get(self, item_id: str) -> T: ...

class InMemoryRepository(Generic[T]):
    def __init__(self):
        self.items: dict[str, T] = {}

    def save(self, item: T) -> None:
        self.items[item.equipment_id] = item

    def get(self, item_id: str) -> T:
        return self.items[item_id]

ahu_repo = InMemoryRepository[AHU]()
```

## 29. `Any` vs Generic

```
Any → type checking weaken
Generic → type relationship preserve
```

## 30. Mental Model

```
Type System
├── TypeVar → type relationship
├── Protocol → behavior
└── Generic → reusable
     ↓
Variance
├── Covariant → output
├── Contravariant → input
└── Invariant → both
```

## 31. Golden Rules

```
TypeVar → type represent
Generic → type-parameterized
Protocol → required behavior
Covariance → producer/output
Contravariance → consumer/input
Invariance → no substitution
bound → type family restrict
```

---

# Lesson 62: `TypeGuard` + `TypeIs` + Type Narrowing

## 1. Type Narrowing

```python
def process(value: int | str):
    if isinstance(value, int):
        print(value + 10)   # int
```

**Explanation:**
- `if` ke andar type narrow

## 2. Narrowing Meaning

```
int | str
    ├── True → int
    └── False → str
```

## 3. Custom Function Problem

```python
def is_string(value):
    return isinstance(value, str)

def process(value: int | str):
    if is_string(value):
        print(value.upper())   # Type checker ko pata nahi
```

## 4. `TypeGuard`

```python
from typing import TypeGuard

def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)

def process(value: object):
    if is_string(value):
        print(value.upper())   # value: str
```

## 5. Mental Model

```python
def is_string(value: object) -> bool:
    # True/False only
```

vs:

```python
def is_string(value: object) -> TypeGuard[str]:
    # True → value is str
```

## 6. Runtime Kya Karta Hai

```python
def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

**Explanation:**
- `TypeGuard` khud runtime magic nahi
- Actual condition khud likhni

## 7. TypeGuard + List

```python
from typing import TypeGuard

def is_str_list(items: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in items)

items: list[object] = ["Ali", "Ahmed"]

if is_str_list(items):
    for item in items:
        print(item.upper())
```

## 8. Generic TypeGuard

```python
T = TypeVar("T")

def is_non_empty(items: list[T]) -> TypeGuard[list[T]]:
    return len(items) > 0
```

## 9. `TypeIs`

```python
from typing import TypeIs

def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

## 10. TypeGuard vs TypeIs

```
TypeGuard → True branch narrow
TypeIs → True + False branch narrow
```

## 11. TypeIs Example

```python
def is_string(value: int | str) -> TypeIs[str]:
    return isinstance(value, str)

def process(value: int | str):
    if is_string(value):
        print(value.upper())   # str
    else:
        print(value + 10)      # int
```

## 12. TypeGuard Difference

```python
def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)

# True → str
# False → not narrowed (TypeIs jaisa nahi)
```

## 13. TypeIs Mathematical

```
Input = int | str
Target = str

True:  (int | str) ∩ str = str
False: (int | str) - str = int
```

## 14. TypeGuard Focus

```
TypeGuard[T] → True branch focus
```

## 15. Example

```python
def is_int(value: object) -> TypeGuard[int]:
    return isinstance(value, int)

def calculate(value: object):
    if is_int(value):
        print(value + 100)
```

## 16. TypeIs Input Compatibility

```python
def is_string(value: int | str) -> TypeIs[str]:
    ...
```

```
Input possibilities: int, str
Target: str
```

## 17. TypeGuard Surprising Feature

```python
def is_str_list(value: list[object]) -> TypeGuard[list[str]]:
    ...
```

**Explanation:**
- `list[object]` aur `list[str]` invariant
- Phir bhi custom guard manual guarantee

## 18. Powerful

```python
def is_valid_equipment_list(items: list[object]) -> TypeGuard[list[Equipment]]:
    return all(isinstance(item, Equipment) for item in items)
```

## 19. TypeGuard + Protocol

```python
class Savable(Protocol):
    def save(self) -> None: ...

def is_savable(value: object) -> TypeGuard[Savable]:
    return hasattr(value, "save")

if is_savable(value):
    value.save()
```

## 20. `@runtime_checkable`

```python
@runtime_checkable
class Savable(Protocol):
    def save(self) -> None: ...

isinstance(obj, Savable)
```

**Explanation:**
- Runtime presence check
- Signature full verify nahi

## 21. Flow-Sensitive Narrowing

```python
def process(value: int | str):
    if isinstance(value, int):
        return value + 10
    return value.upper()
```

## 22. TypeGuard + Tuple

```python
def is_pair(value: tuple[object, ...]) -> TypeGuard[tuple[str, str]]:
    return len(value) == 2 and all(isinstance(x, str) for x in value)

value: tuple[object, ...]
if is_pair(value):
    a, b = value
    print(a.upper())
```

## 23. TypeGuard + Dict

```python
def is_user(data: dict[str, object]) -> TypeGuard[dict[str, str]]:
    return isinstance(data.get("name"), str) and isinstance(data.get("email"), str)
```

## 24. Comparison Table

| Feature | `TypeGuard` | `TypeIs` |
|---------|-------------|----------|
| True narrow | ✅ | ✅ |
| False narrow | ❌ | ✅ |
| Subtype required | ❌ | ✅ |
| Custom | ✅ | ✅ |
| Runtime magic | ❌ | ❌ |

## 25. Memory Trick

```
TypeGuard → "True hai to is type ko maan lo"
TypeIs → "True mein ye, False mein ye hata do"
```

## 26. TypeIs as isinstance Wrapper

```python
def is_special_string(value) -> TypeIs[str]:
    ...
```

## 27. API Data Validation

```python
def is_valid_equipment(data: object) -> TypeGuard[Equipment]:
    return isinstance(data, Equipment)

if is_valid_equipment(data):
    print(data.equipment_id)
```

## 28. Validation Function

```python
def is_X(value: Input) -> TypeGuard[X]:
    ...
```

```
Input → runtime validation → True → X
```

## 29. TypeGuard Trust

```python
def fake_guard(value: object) -> TypeGuard[str]:
    return True   # DANGEROUS
```

**Explanation:**
- Programmer promise
- Wrong implementation → runtime error

## 30. TypeGuard Kya Nahi Karta

```
TypeGuard → type convert nahi
TypeGuard → runtime validation nahi
```

## 31. Lesson 58 Connection

```
Generic repository → returns unknown
       ↓
runtime validation
       ↓
TypeGuard / TypeIs
       ↓
specific type
```

## 32. Final Model

```
TYPE NARROWING
├── Built-in: isinstance()
└── Custom: TypeGuard / TypeIs
     ↓
Specific type
     ↓
safer operations
```

## 33. Golden Rules

```
TypeGuard[T] → True → T
TypeIs[T] → True T, False not T
isinstance → normal narrow
issubclass → class narrow
Custom predicate → TypeGuard/TypeIs
```

---

# Lesson 63: `match` / `case` — Structural Pattern Matching

## 1. Basic `match`

```python
def get_status(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"
```

## 2. `case _`

```python
case _:
    print("Something else")
```

**Explanation:**
- Wildcard (koi bhi)

## 3. Match vs Switch

```
Match → pattern + structure + destructuring
```

## 4. Variable Capture

```python
value = 100
match value:
    case x:
        print(x)   # 100
```

**Explanation:**
- `x` → capture

## 5. `case x` vs `case 100`

```python
case 100:   # Exact match
case x:     # Capture
```

## 6. Sequence Pattern

```python
data = [10, 20, 30]
match data:
    case [10, 20, 30]:
        print("Exact list")
```

## 7. Capture List

```python
data = [10, 20]
match data:
    case [x, y]:
        print(x, y)   # 10 20
```

## 8. `*rest`

```python
data = [10, 20, 30, 40, 50]
match data:
    case [first, *rest]:
        print(first)   # 10
        print(rest)    # [20, 30, 40, 50]
```

## 9. Start + Middle + End

```python
match data:
    case [first, *middle, last]:
        print(first, middle, last)
```

## 10. Tuple Matching

```python
point = (10, 20)
match point:
    case (x, y):
        print(x, y)
```

## 11. OR Pattern

```python
match status:
    case "success" | "ok":
        print("Operation successful")
    case "error":
        print("Operation failed")
```

## 12. OR + Capture

```python
case ("yes", value) | ("no", value):
    ...
```

**Explanation:**
- Same capture name

## 13. Guard

```python
value = 15
match value:
    case x if x > 10:
        print("Greater than 10")
    case x:
        print("10 or less")
```

## 14. Guard Practical

```python
temperature = 25
match temperature:
    case x if x < 18:
        print("Cold")
    case x if x <= 24:
        print("Normal")
    case x if x <= 30:
        print("Warm")
    case _:
        print("Hot")
```

## 15. Dictionary Pattern

```python
data = {"name": "Ali", "age": 30}
match data:
    case {"name": name, "age": age}:
        print(name, age)
```

## 16. Extra Keys

```python
data = {"name": "Ali", "age": 30, "city": "Riyadh"}
match data:
    case {"name": name, "age": age}:
        print(name, age)   # Extra keys OK
```

## 17. `**rest`

```python
match data:
    case {"name": name, **rest}:
        print(name)
        print(rest)
```

## 18. Nested Pattern

```python
data = {"employee": {"name": "Ali", "department": "HVAC"}}
match data:
    case {"employee": {"name": name, "department": department}}:
        print(name, department)
```

## 19. API Response Example

```python
response = {
    "status": "success",
    "data": {"id": 100, "name": "AHU-001"}
}

match response:
    case {"status": "success", "data": {"id": equipment_id, "name": name}}:
        print(equipment_id, name)
    case {"status": "error", "message": message}:
        print("Error:", message)
    case _:
        print("Unknown")
```

## 20. Class Pattern

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

point = Point(10, 20)
match point:
    case Point(x, y):
        print(x, y)
```

## 21. Keyword Class Pattern

```python
match point:
    case Point(x=10, y=20):
        print("Point found")
```

## 22. Class + Guard

```python
match point:
    case Point(x, y) if x > 0 and y > 0:
        print("First quadrant")
    case Point(x, y):
        print("Other quadrant")
```

## 23. Multiple Classes

```python
@dataclass
class AHU:
    id: str
    airflow: int

@dataclass
class Refrigerator:
    id: str
    temperature: float

equipment = AHU("AHU-01", 5000)

match equipment:
    case AHU(id, airflow):
        print("AHU:", id, airflow)
    case Refrigerator(id, temperature):
        print("Refrigerator:", id, temperature)
    case _:
        print("Unknown equipment")
```

## 24. Nested Class

```python
@dataclass
class Building:
    name: str
    equipment: object

building = Building("Tower A", AHU("AHU-01", 5000))

match building:
    case Building(name, AHU(id, airflow)):
        print(name, id, airflow)
```

## 25. Type Pattern

```python
value = "Ali"

match value:
    case int():
        print("Integer")
    case str():
        print("String")
    case float():
        print("Float")
    case _:
        print("Other")
```

## 26. Capture vs Type

```python
case str():        # Type check
case value:        # Capture
case str(value):   # Contextual
```

## 27. Literal Patterns

```python
case 10:
case "hello":
case True:
case None:
```

## 28. `None` Pattern

```python
result = None
match result:
    case None:
        print("No result")
    case value:
        print("Result:", value)
```

## 29. `_` vs Variable

```python
case _:   # Ignore
case x:   # Capture
```

## 30. Case Ordering

```python
match value:
    case 100:
        print("100")
    case x:
        print("Anything:", x)
```

**Explanation:**
- Specific pehle
- General baad mein

## 31. `_` Last

```python
match status:
    case "running":
        ...
    case "stopped":
        ...
    case _:
        ...
```

## 32. Sequence Exact Length

```python
case [a, b]:        # Exactly 2
case [a, b, *rest]: # 2+
```

## 33. `*rest` Behavior

```
[10] → first=10, rest=[]
[10, 20, 30] → first=10, rest=[20, 30]
```

## 34. Patterns

```python
case {"name": name}:       # Mapping
case [name]:               # Sequence
case (x, y):               # Tuple
case Employee(name, salary): # Class
```

## 35. Command Parser

```python
command = ("move", "AHU-01", 10)

match command:
    case ("move", equipment_id, value):
        print("Moving", equipment_id, value)
    case ("stop", equipment_id):
        print("Stopping", equipment_id)
    case ("status", equipment_id):
        print("Checking", equipment_id)
    case _:
        print("Unknown command")
```

## 36. Pattern + Guard

```python
command = ("set_temperature", "AHU-01", 22)

match command:
    case ("set_temperature", equipment_id, temp) if 18 <= temp <= 26:
        print(equipment_id, "temperature set to", temp)
    case ("set_temperature", equipment_id, temp):
        print("Invalid temperature")
    case _:
        print("Unknown command")
```

## 37. Match + Type Narrowing

```python
value: int | str

match value:
    case int():
        print(value + 10)
    case str():
        print(value.upper())
```

## 38. Match + Protocol

```
Protocol → static structural typing
match → concrete runtime structure
```

## 39. Match Kab

```
Multiple structural cases
Different object types
API/data parsing
Commands/events
Nested data
```

## 40. If Kab

```python
if temperature > 25:
    ...
```

**Explanation:**
- Simple condition → if

## 41. Mental Model

```
match subject
├── Literal
├── Structure
├── Class
└── Guard
```

## 42. Patterns Cheat Sheet

```python
case 200:              # Literal
case _:                # Wildcard
case x:                # Capture
case 200 | 201:        # OR
case [x, y]:           # List
case [x, *rest]:       # Variable list
case {"name": name}:   # Dictionary
case Employee(name):   # Class
case x if x > 10:      # Guard
```

## 43. Complete Example

```python
@dataclass
class AHU:
    id: str
    airflow: int

@dataclass
class Refrigerator:
    id: str
    temperature: float

def process_equipment(equipment):
    match equipment:
        case AHU(id, airflow) if airflow > 5000:
            print(id, "AHU has high airflow:", airflow)
        case AHU(id, airflow):
            print(id, "AHU airflow:", airflow)
        case Refrigerator(id, temperature) if temperature > 5:
            print(id, "temperature high:", temperature)
        case Refrigerator(id, temperature):
            print(id, "temperature normal:", temperature)
        case _:
            print("Unknown equipment")
```

## 44. Core 5

```
1. Literal → case 200
2. Capture → case x
3. Structural → case [x, y], case {"name": name}
4. Class → case Employee(name)
5. Guard → case x if x > 10
```

---

# Lesson 64: `dataclass` Advanced

## 1. Basic `dataclass`

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    name: str
    floor: str

equipment = Equipment("MEP-AHU-001", "AHU", "34F")
print(equipment)
```

**Output:**
```
Equipment(equipment_id='MEP-AHU-001', name='AHU', floor='34F')
```

## 2. Inheritance

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str

@dataclass
class AHU(Equipment):
    airflow: float

ahu = AHU("MEP-AHU-001", "34F", 1200)
print(ahu)
```

## 3. Real Architecture

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str

@dataclass
class AHU(Equipment):
    airflow: float

@dataclass
class VAV(Equipment):
    damper_position: float

@dataclass
class Refrigerator(Equipment):
    temperature: float
```

## 4. Field Ordering

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str = "Unknown"

@dataclass
class AHU(Equipment):
    airflow: float = 0.0   # Default required
```

## 5. `kw_only=True`

```python
@dataclass(kw_only=True)
class AHU(Equipment):
    airflow: float

ahu = AHU("AHU-001", "34F", airflow=1200)
```

## 6. `__match_args__`

```python
@dataclass
class Point:
    x: int
    y: int

point = Point(10, 20)

match point:
    case Point(x, y):
        print(x, y)   # 10 20
```

**Explanation:**
- `Point.__match_args__` → `('x', 'y')`

## 7. Manual `__match_args__`

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str

    __match_args__ = ("equipment_id", "status")

equipment = Equipment("AHU-001", "34F", "Running")

match equipment:
    case Equipment(equipment_id, status):
        print(equipment_id, status)
```

## 8. `match_args=False`

```python
@dataclass(match_args=False)
class Equipment:
    equipment_id: str
    floor: str
```

**Explanation:**
- Positional pattern disabled
- Keyword pattern allowed

## 9. `InitVar`

```python
from dataclasses import dataclass, InitVar

@dataclass
class Equipment:
    equipment_id: str
    raw_temperature: InitVar[float]

    def __post_init__(self, raw_temperature):
        print(raw_temperature)

equipment = Equipment("AHU-001", 24.5)
# 24.5
```

**Explanation:**
- `raw_temperature` permanent field nahi

## 10. `InitVar` Purpose

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature_f: float
    temperature_c: InitVar[float]

    def __post_init__(self, temperature_c):
        self.temperature_f = (temperature_c * 9 / 5) + 32

equipment = Equipment("REF-001", 0, 4)
print(equipment.temperature_f)   # 39.2
```

## 11. `__post_init__`

```
__init__() → fields assign → __post_init__() → processing
```

## 12. `InitVar` vs Normal Field

```
Normal field → Input → Store
InitVar → Input → Process → Discard
```

## 13. `InitVar` Config Example

```python
@dataclass
class Equipment:
    equipment_id: str
    name: str
    config: InitVar[dict]

    def __post_init__(self, config):
        self.name = config.get("name", self.name)
```

## 14. `ClassVar`

```python
from typing import ClassVar

@dataclass
class Equipment:
    equipment_id: str
    status: str

    allowed_statuses: ClassVar[set[str]] = {
        "Running", "Stopped", "Fault", "Maintenance"
    }
```

**Explanation:**
- Instance field nahi
- `__init__` mein nahi

## 15. `ClassVar` Access

```python
Equipment.allowed_statuses
equipment.allowed_statuses   # Technically
```

## 16. `ClassVar` Importance

```python
@dataclass
class Equipment:
    equipment_id: str
    total_created: ClassVar[int] = 0
```

## 17. `ClassVar` Mutable

```python
@dataclass
class Equipment:
    equipment_id: str
    types: ClassVar[list[str]] = ["AHU", "VAV", "FCU"]
```

## 18. `ClassVar` vs Normal

```
Normal field → Har object ka apna
ClassVar → Class ka shared
```

## 19. All 4 Concepts

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str

    allowed_statuses: ClassVar[set[str]] = {"Running", "Stopped", "Fault"}

@dataclass
class AHU(Equipment):
    airflow: float
    raw_status: InitVar[str] = ""

    def __post_init__(self, raw_status):
        if raw_status:
            self.status = raw_status.upper()

ahu = AHU(
    equipment_id="AHU-001",
    floor="34F",
    status="unknown",
    airflow=1200,
    raw_status="running"
)
print(ahu)
```

## 20. `match/case` + Dataclass

```python
match ahu:
    case AHU(equipment_id, floor, status, airflow):
        print(equipment_id, floor, status, airflow)
```

## 21. Keyword Matching

```python
match ahu:
    case AHU(equipment_id="AHU-001", status="RUNNING"):
        print("AHU running")
```

## 22. `__match_args__` + Inheritance

```python
match ahu:
    case AHU(equipment_id, floor, airflow):
        ...
```

## 23. `InitVar` + Inheritance

```python
@dataclass
class Equipment:
    equipment_id: str
    config: InitVar[dict]

    def __post_init__(self, config):
        print("Equipment config:", config)

@dataclass
class AHU(Equipment):
    airflow: float

    def __post_init__(self, config):
        super().__post_init__(config)
        print("AHU airflow:", self.airflow)
```

## 24. `InitVar` vs `ClassVar`

```
InitVar → constructor input, persistent field nahi
ClassVar → class-level data, instance field nahi
```

## 25. Complete Example

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str

    allowed_statuses: ClassVar[set[str]] = {"RUNNING", "STOPPED", "FAULT"}

@dataclass
class AHU(Equipment):
    airflow: float
    raw_status: InitVar[str] = ""

    def __post_init__(self, raw_status):
        if raw_status:
            self.status = raw_status.upper()
        if self.status not in self.allowed_statuses:
            raise ValueError(f"Invalid status: {self.status}")
```

## 26. `match/case` Integration

```python
match ahu:
    case AHU(equipment_id=id, status="RUNNING", airflow=airflow) if airflow > 1000:
        print(f"{id}: High airflow AHU")
    case AHU(status="RUNNING"):
        print("AHU running")
    case AHU(status="FAULT"):
        print("AHU fault")
    case _:
        print("Other equipment")
```

## 27. Mental Model

```
DATACLASS
├── Inheritance → parent + child
├── InitVar → temporary constructor input
├── ClassVar → shared class data
└── __match_args__ → match/case integration
```

## 28. Short Definitions

| Concept | Meaning |
|---------|---------|
| `@dataclass` | Data-oriented class simplify |
| Inheritance | Parent fields reuse |
| `__match_args__` | Positional match order |
| `InitVar` | Constructor-only input |
| `__post_init__` | After init processing |
| `ClassVar` | Class-level variable |
| `match_args=False` | Disable positional |
| `kw_only=True` | Keyword-only fields |

## 29. Golden Rules

```
Inheritance → parent fields pehle
InitVar → temporary input
ClassVar → shared data
__match_args__ → positional matching
match_args=False → disable positional
kw_only → explicit keyword args
```

---

# Lesson 65: `typing.overload` — Function Overloading

## 1. Problem

```python
def get_value(value):
    if isinstance(value, int):
        return value * 2
    if isinstance(value, str):
        return value.upper()

get_value(10)       # 20
get_value("hello")  # HELLO
```

**Explanation:**
- Runtime sahi
- Type checker ko relationship nahi pata

## 2. Basic `overload`

```python
from typing import overload

@overload
def get_value(value: int) -> int:
    ...

@overload
def get_value(value: str) -> str:
    ...

def get_value(value: int | str) -> int | str:
    if isinstance(value, int):
        return value * 2
    return value.upper()
```

**Explanation:**
- `get_value(10)` → `int`
- `get_value("hello")` → `str`

## 3. `...` Meaning

```python
@overload
def get_value(value: int) -> int:
    ...
```

**Explanation:**
- Type signature declaration
- Implementation nahi

## 4. Actual Implementation

```python
@overload
def get_value(value: int) -> int: ...
@overload
def get_value(value: str) -> str: ...

def get_value(value: int | str) -> int | str:
    ...
```

## 5. Important Rule

```
@overload → runtime separately implement nahi
@overload → type checker ke liye signatures
```

## 6. Mental Model

```
overload
├── int input → int output
└── str input → str output
     ↓
Actual implementation
```

## 7. Faida

```python
# Without overload
def get_value(value: int | str) -> int | str: ...

x = get_value(10)   # x: int | str

# With overload
@overload
def get_value(value: int) -> int: ...
@overload
def get_value(value: str) -> str: ...

x = get_value(10)   # x: int
```

## 8. Union vs Overload

```
Union → possible types
Overload → input/output relationship
```

## 9. HVAC Example

```python
@dataclass
class AHU:
    equipment_id: str

@dataclass
class VAV:
    equipment_id: str

@overload
def get_equipment(equipment_type: str) -> AHU: ...

@overload
def get_equipment(equipment_type: int) -> VAV: ...

def get_equipment(equipment_type: str | int) -> AHU | VAV:
    if isinstance(equipment_type, str):
        return AHU(equipment_type)
    return VAV(str(equipment_type))
```

## 10. Multiple Overloads

```python
@overload
def convert(value: int) -> float: ...
@overload
def convert(value: float) -> int: ...
@overload
def convert(value: str) -> str: ...

def convert(value: int | float | str) -> float | int | str:
    if isinstance(value, int):
        return float(value)
    if isinstance(value, float):
        return int(value)
    return value.upper()
```

## 11. Overload Order

```python
# Specific → broad
@overload
def process(value: str) -> str: ...
@overload
def process(value: object) -> object: ...
```

## 12. `bool` vs `int`

```python
@overload
def check(value: bool) -> str: ...
@overload
def check(value: int) -> int: ...
```

**Explanation:**
- `bool` `int` ka subclass
- Specific pehle

## 13. `Literal` + Overload

```python
from typing import Literal, overload

@overload
def get_data(detailed: Literal[True]) -> dict: ...
@overload
def get_data(detailed: Literal[False]) -> str: ...

def get_data(detailed: bool) -> dict | str:
    if detailed:
        return {"id": "AHU-001", "airflow": 1200}
    return "AHU-001"
```

## 14. `Literal` Mental Model

```
detailed=True → dict
detailed=False → str
```

## 15. `None` + Overload

```python
@overload
def find_equipment(equipment_id: str, required: Literal[True]) -> AHU: ...
@overload
def find_equipment(equipment_id: str, required: Literal[False]) -> AHU | None: ...

def find_equipment(equipment_id: str, required: bool) -> AHU | None:
    equipment = database_lookup(equipment_id)
    if equipment is None and required:
        raise ValueError("Equipment not found")
    return equipment
```

## 16. Overload vs Runtime Dispatch

```python
@overload
def foo(x: int) -> int: ...
@overload
def foo(x: str) -> str: ...

def foo(x):
    ...
```

**Explanation:**
- Runtime par ek implementation
- `@overload` static info only

## 17. Runtime Multiple Methods

```python
def process(value):
    if isinstance(value, int):
        return process_int(value)
    if isinstance(value, str):
        return process_string(value)
    raise TypeError("Unsupported type")
```

**Explanation:**
- `singledispatch` alternative

## 18. `typing.overload` vs `singledispatch`

```
typing.overload → static type checking
singledispatch → runtime dispatch
```

## 19. Overload + Generic

```python
T = TypeVar("T")

@overload
def first(items: list[T]) -> T: ...

def first(items):
    return items[0]
```

**Explanation:**
- Simple generic ke liye overload zaroori nahi

## 20. Overload + Sequence

```python
@overload
def get_result(value: int) -> tuple[int, str]: ...
@overload
def get_result(value: str) -> tuple[str, int]: ...

def get_result(value: int | str):
    if isinstance(value, int):
        return value, "number"
    return value, len(value)
```

## 21. Implementation Signature

```python
@overload
def convert(value: int) -> str: ...
@overload
def convert(value: float) -> str: ...

def convert(value: int | float) -> str:
    return str(value)
```

## 22. Implementation Return

```python
@overload
def convert(value: int) -> int: ...
@overload
def convert(value: str) -> str: ...

def convert(value: int | str) -> int | str:
    ...
```

## 23. Signatures vs Implementation

```
Overload signatures → PUBLIC TYPE API
Last function → RUNTIME IMPLEMENTATION
```

## 24. Real-World API

```python
@overload
def load_equipment(equipment_id: str, as_dict: Literal[True]) -> dict: ...
@overload
def load_equipment(equipment_id: str, as_dict: Literal[False]) -> Equipment: ...

def load_equipment(equipment_id: str, as_dict: bool) -> dict | Equipment:
    equipment = database_load(equipment_id)
    if as_dict:
        return {"equipment_id": equipment.equipment_id, "floor": equipment.floor}
    return equipment
```

## 25. Formula

```
Input A → Output A
Input B → Output B
Input C → Output C
```

## 26. Overload vs TypeGuard

```
TypeGuard → input inspect + narrow
Overload → different input signatures → return types
```

## 27. Overload vs Generic

```
Generic → type relationship preserve
Overload → multiple signatures
```

## 28. Overload vs Union

```
Union → input/output possibilities
Overload → input-output correlation
```

## 29. Work-Order Example

```python
@overload
def get_work_order(number: str, summary: Literal[True]) -> WorkOrderSummary: ...
@overload
def get_work_order(number: str, summary: Literal[False]) -> WorkOrder: ...

def get_work_order(number: str, summary: bool) -> WorkOrderSummary | WorkOrder:
    if summary:
        return WorkOrderSummary(number)
    return WorkOrder(number, "HVAC Preventive Maintenance")
```

## 30. Dangerous Mistake

```python
@overload
def get(x: int) -> str: ...
@overload
def get(x: int) -> int: ...
```

**Explanation:**
- Same input, contradictory return

## 31. Another Mistake

```python
@overload
def foo(x: int) -> int:
    return x * 2   # Wrong
```

**Explanation:**
- `@overload` implementation nahi

## 32. Final Model

```
ONE FUNCTION
├── Signature 1
├── Signature 2
└── Signature 3
     ↓
ONE implementation
```

## 33. Kab Use

```
Multiple calling patterns
Input→Output change
Literal-based return
Precise API typing
```

## 34. Kab Na Use

```
Simple Union sufficient
Generic[T] relationship
Runtime dispatch chahiye
```

## 35. One-line

```
Generic → generalize
TypeGuard → narrow
overload → multiple input→output contracts
```

---

# Lesson 66: `typing.cast()` — Type Casting

## 1. `cast()`

```python
from typing import cast

value = cast(int, something)
```

**Explanation:**
- Type checker ko batata hai
- Runtime change nahi

## 2. Simple Example

```python
value = "100"
number = cast(int, value)
print(number)   # 100
print(type(number))   # <class 'str'>
```

**Explanation:**
- Actual object same rehta hai

## 3. `cast()` vs `int()`

```python
# int() — Conversion
number = int("100")
type(number)   # <class 'int'>

# cast() — No conversion
number = cast(int, "100")
type(number)   # <class 'str'>
```

## 4. Analogy

```
BOX → actual object: String
cast(int, box) → label change only
```

## 5. Purpose

```python
def get_value() -> object:
    return 100

value = get_value()
number = cast(int, value)
```

**Explanation:**
- Programmer ko pata
- Type checker ko nahi

## 6. Runtime vs Static

```
Runtime: object same
Type checker: type assumption changes
```

## 7. Example

```python
def get_data() -> object:
    return "AHU-001"

data = get_data()
equipment_id = cast(str, data)
equipment_id.upper()
```

## 8. Cast Verify Nahi Karta

```python
data: object = 100
equipment_id = cast(str, data)
equipment_id.upper()   # AttributeError at runtime
```

## 9. Programmer Promise

```
cast() → "Type checker, trust me"
```

## 10. Cast vs TypeGuard

```
TypeGuard → runtime check + narrowing
cast → no check, assertion
```

## 11. Safe Narrowing

```python
if isinstance(value, str):
    print(value.upper())
```

## 12. Cast Common Use — dict

```python
data: object = {"equipment_id": "AHU-001", "airflow": 1200}
equipment_data = cast(dict[str, object], data)
equipment_data["equipment_id"]
```

## 13. External Data

```python
response: object = api.get_response()
response_data = cast(dict[str, object], response)
```

## 14. Structured Data Limitation

```python
data = cast(dict[str, object], response)
airflow = data["airflow"]   # Still object
```

**Explanation:**
- Further validation needed

## 15. Cast + Protocol

```python
class EquipmentController(Protocol):
    def start(self) -> None: ...

controller = get_controller()
controller = cast(EquipmentController, controller)
controller.start()
```

## 16. Protocol Cast Danger

```python
controller = cast(EquipmentController, wrong_object)
controller.start()   # Runtime error
```

## 17. Cast + TypeVar

```python
T = TypeVar("T")

def get_value(value: object) -> T:
    return cast(T, value)
```

**Explanation:**
- Careful use

## 18. Cast + None

```python
value: str | None = get_name()
name = cast(str, value)
name.upper()
```

**Explanation:**
- Agar actual `None` → runtime error

## 19. Better Alternative

```python
if value is None:
    raise ValueError("Name missing")
name = value
```

## 20. Common Misconception

```python
x = cast(int, "123")   # Same as int("123")?
# NO
```

## 21. Cast vs Assert

```python
# Assert — runtime check
assert isinstance(value, str)
value.upper()

# Cast — no check
value = cast(str, value)
value.upper()
```

## 22. Cast vs TypeIs

```
TypeIs → actual check + narrowing
cast → no check + assertion
```

## 23. Cast Kab Useful

```
Type checker info missing
Third-party typing incomplete
Framework/metaprogramming
Legacy code
```

## 24. Kab Na Use

```
Simple narrowing possible
Conversion chahiye
Validation chahiye
```

## 25. Cast ≠ Convert

```
CAST ≠ CONVERT
```

## 26. HVAC Example

```python
def load_equipment() -> object:
    return {"equipment_id": "AHU-001", "airflow": 1200}

data = cast(dict[str, int | str], load_equipment())
```

## 27. Better — TypedDict

```python
class AHUData(TypedDict):
    equipment_id: str
    airflow: float

raw_data: object = load_equipment()
ahu_data = cast(AHUData, raw_data)
ahu_data["equipment_id"]   # str
ahu_data["airflow"]        # float
```

## 28. TypedDict Cast Danger

```python
# Actual API: {"airflow": "1200"}
# TypedDict: float
# cast → type checker khush
# runtime → str
```

## 29. Validation vs Cast

```
External data → Validation → Correct model → Business logic
```

## 30. Syntax

```python
cast(Type, expression)

cast(int, value)
cast(str, value)
cast(Equipment, value)
cast(list[str], value)
cast(dict[str, int], value)
```

## 31. Runtime Return

```python
value = "hello"
result = cast(int, value)
print(result is value)   # True
```

## 32. No Validation

```python
cast(int, value)
# Not: isinstance check
```

## 33. Connection

```
TypeVar → type relationship
Generic → reusable
Protocol → behavior
TypeGuard → narrowing
TypeIs → two-way
overload → input→output
cast → programmer assertion
```

## 34. Golden Rule

```
Type checker confused? → cast() MAY help
Runtime value uncertain? → cast() DOES NOT help
Conversion? → int(), str(), float()
Validation? → isinstance(), TypeGuard, TypeIs
```

## 35. Practical Example

```python
class EquipmentData(TypedDict):
    equipment_id: str
    floor: str
    airflow: float

raw = load_raw_data()
equipment = cast(EquipmentData, raw)
print(equipment["equipment_id"])
```

## 36. Core 5

```
1. cast → runtime conversion nahi
2. cast → static assertion
3. cast → runtime validation nahi
4. Wrong cast → runtime error
5. Better alternatives prefer karo
```

---

# Lesson 67: `typing.Annotated` + Metadata

## 1. Basic

```python
from typing import Annotated

temperature: Annotated[float, "Celsius"]
```

**Explanation:**
- Type: `float`
- Metadata: `"Celsius"`

## 2. Metadata Type Nahi

```python
Annotated[float, "Celsius"]
# Underlying: float
```

## 3. Kyun Banaya

```python
temperature: float   # Type checker: float
temperature: Annotated[float, "Celsius"]   # + "Celsius"
```

## 4. Multiple Metadata

```python
temperature: Annotated[
    float,
    "Celsius",
    "HVAC sensor",
    "validated"
]
```

## 5. HVAC Example

```python
airflow: Annotated[
    float,
    "unit=CFM",
    "min=0",
    "max=5000"
]
```

## 6. Arbitrary Objects

```python
class Range:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

airflow: Annotated[float, Range(0, 5000)]
```

## 7. Retrieve

```python
from typing import get_type_hints

def read_sensor(temperature: Annotated[float, "Celsius"]):
    pass

print(get_type_hints(read_sensor, include_extras=True))
```

## 8. `include_extras=True`

```python
get_type_hints(read_sensor)   # Strips metadata

get_type_hints(read_sensor, include_extras=True)
# Preserves metadata
```

## 9. `get_origin()` / `get_args()`

```python
from typing import Annotated, get_origin, get_args

Temperature = Annotated[float, "Celsius"]

print(get_origin(Temperature))
# <class 'typing.Annotated'>

print(get_args(Temperature))
# (float, 'Celsius')
```

## 10. `get_args()` Structure

```python
Annotated[float, "Celsius", "Sensor"]
# get_args → (float, "Celsius", "Sensor")
```

## 11. Custom Metadata

```python
@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float

Airflow = Annotated[float, Range(0, 5000)]
```

## 12. Multiple Metadata Objects

```python
@dataclass(frozen=True)
class Unit:
    name: str

Airflow = Annotated[
    float,
    Unit("CFM"),
    Range(0, 5000)
]
```

## 13. Type Alias

```python
Airflow = Annotated[
    float,
    Unit("CFM"),
    Range(0, 5000)
]

class AHU:
    airflow: Airflow
```

## 14. Type Safety Replace Nahi

```python
Temperature = Annotated[float, "Celsius"]
temperature: Temperature = "hello"   # Error
```

## 15. Metadata Automatically Enforce Nahi

```python
Airflow = Annotated[float, Range(0, 5000)]
airflow = 10000   # No automatic error
```

## 16. Validation Framework Role

```
Annotated → Metadata → Framework reads → Validation
```

## 17. Custom Validator

```python
@dataclass(frozen=True)
class MinValue:
    value: float

Temperature = Annotated[float, MinValue(-40)]
```

## 18. Real-World

```python
Temperature = Annotated[float, Unit("°C"), Range(-40, 80)]
Airflow = Annotated[float, Unit("CFM"), Range(0, 10000)]
DamperPosition = Annotated[float, Unit("%"), Range(0, 100)]

class AHUConfig:
    temperature: Temperature
    airflow: Airflow
    damper: DamperPosition
```

## 19. Annotated vs NewType

```python
# Annotated — same type + metadata
Temperature = Annotated[float, "Celsius"]

# NewType — distinct static type
Temperature = NewType("Temperature", float)
```

## 20. Annotated vs TypeAlias

```python
Temperature = float   # Simple alias

Temperature = Annotated[float, "Celsius"]   # Type + metadata
```

## 21. Function Parameters

```python
def set_temperature(temperature: Annotated[float, "Celsius", "Range: -40..80"]):
    ...
```

## 22. Return Type

```python
def read_airflow() -> Annotated[float, "CFM"]:
    return 1200.0
```

## 23. Nested Types

```python
values: Annotated[list[int], "Sensor readings"]
```

## 24. Element vs List

```python
# Entire list metadata
values: Annotated[list[int], "Sensor readings"]

# Individual elements
values: list[Annotated[int, "Sensor value"]]
```

## 25. Nested Example

```python
SensorValue = Annotated[float, "raw sensor value"]
values: list[SensorValue]
```

## 26. Metadata Ordering

```python
Temperature = Annotated[float, Unit("C"), Range(-40, 80), "HVAC"]
```

**Explanation:**
- Order preserve

## 27. Nested Annotated

```python
A = Annotated[int, "A"]
B = Annotated[A, "B"]
# Metadata: int + A + B
```

## 28. Decorators + Frameworks

```python
def create_work_order(
    number: Annotated[str, "Work Order Number"],
    priority: Annotated[int, Range(1, 5)]
):
    ...
```

## 29. Documentation

```python
def set_airflow(airflow: Annotated[float, Unit("CFM"), Range(0, 5000)]):
    ...
```

**Explanation:**
- Tooling auto-generate

## 30. Dependency Injection

```python
def endpoint(db: Annotated[Database, "inject database"]):
    ...
```

## 31. Security Metadata

```python
@dataclass(frozen=True)
class Permission:
    name: str

UserId = Annotated[int, Permission("equipment.read")]
```

## 32. Annotated + Literal

```python
status: Annotated[
    Literal["Running", "Stopped", "Fault"],
    "HVAC equipment status"
]
```

## 33. Annotated + Final

```python
MAX_AIRFLOW: Final[Annotated[float, Unit("CFM")]] = 5000.0
```

## 34. Annotated + ClassVar

```python
@dataclass
class AHU:
    airflow: Annotated[float, "CFM"]
    default_airflow: ClassVar[Annotated[float, "CFM"]] = 1200.0
```

## 35. Annotated vs cast

```python
# cast — type assertion
value = cast(Equipment, value)

# Annotated — type + metadata
value: Annotated[Equipment, "loaded from database"]
```

## 36. Annotated vs TypeGuard

```
TypeGuard → runtime check + narrowing
Annotated → type + metadata
```

## 37. Production Example

```python
@dataclass(frozen=True)
class Unit:
    name: str

@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float

Airflow = Annotated[float, Unit("CFM"), Range(0, 5000)]
Temperature = Annotated[float, Unit("°C"), Range(-40, 80)]

@dataclass
class AHU:
    equipment_id: str
    airflow: Airflow
    temperature: Temperature
```

## 38. Limitation

```python
ahu = AHU("AHU-001", airflow=99999, temperature=-500)
# Automatic error nahi
```

## 39. Custom Validator

```
AHU → annotations inspect → Annotated → Range read → actual check
```

## 40. Deepest Concept

```
airflow: float   # WHAT TYPE?

airflow: Annotated[float, Unit("CFM"), Range(0, 5000)]
# WHAT TYPE? + WHAT EXTRA SEMANTIC INFO?
```

## 41. Comparison

| Feature | Purpose |
|---------|---------|
| `TypeVar` | Type relationship |
| `Generic` | Generic architecture |
| `Protocol` | Behavior contract |
| `TypeGuard` | Custom narrowing |
| `TypeIs` | Two-way narrowing |
| `overload` | Input→output signatures |
| `cast` | Static assertion |
| `Annotated` | Type + metadata |
| `Literal` | Specific values |
| `Final` | No reassign |

## 42. Golden Rule

```
Annotated[T, metadata]
→ T + extra information

Annotated ≠ conversion
Annotated ≠ automatic validation
Annotated ≠ new runtime class
Annotated = type + metadata
```

---

# Lesson 68: `typing.Self` — Self Type

## 1. Problem

```python
class Equipment:
    def set_status(self, status: str) -> "Equipment":
        self.status = status
        return self

class AHU(Equipment):
    def set_airflow(self, airflow: float):
        self.airflow = airflow
        return self

ahu = AHU()
ahu.set_status("Running").set_airflow(1200)   # Type checker problem
```

## 2. `Self`

```python
from typing import Self

class Equipment:
    def set_status(self, status: str) -> Self:
        self.status = status
        return self

class AHU(Equipment):
    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self

ahu = AHU()
ahu.set_status("Running").set_airflow(1200)   # OK
```

## 3. Mental Model

```
Self → current class ka actual type
```

## 4. Self vs Normal Return

```python
# Without Self
class Equipment:
    def reset(self) -> "Equipment":
        return self
# result → Equipment

# With Self
class Equipment:
    def reset(self) -> Self:
        return self
# ahu.reset() → AHU
```

## 5. Inheritance Preserve

```python
class Equipment:
    def start(self) -> Self:
        print("Equipment started")
        return self

class AHU(Equipment):
    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self

ahu = AHU()
ahu.start().set_airflow(1500)
```

## 6. Fluent API

```python
class Query:
    def filter(self, condition: str) -> Self:
        print("Filter:", condition)
        return self

    def order_by(self, field: str) -> Self:
        print("Order:", field)
        return self

    def limit(self, number: int) -> Self:
        print("Limit:", number)
        return self

query = Query()
query.filter("temperature > 25").order_by("temperature").limit(10)
```

## 7. Subclass

```python
class EquipmentQuery(Query):
    def equipment_type(self, name: str) -> Self:
        print("Equipment:", name)
        return self

query = EquipmentQuery()
query.filter("status = 'Running'").equipment_type("AHU").limit(10)
```

## 8. `Self` Return Type Nahi Sirf

```python
class Node:
    parent: Self | None
```

## 9. Classmethod + Self

```python
class Equipment:
    @classmethod
    def create(cls) -> Self:
        return cls()

class AHU(Equipment):
    pass

ahu = AHU.create()   # AHU
```

## 10. Reason

```
Equipment.create() → Self = Equipment
AHU.create() → Self = AHU
```

## 11. Factory Pattern

```python
class Equipment:
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(data["equipment_id"])

class AHU(Equipment):
    pass

ahu = AHU.from_dict({"equipment_id": "AHU-001"})
# Type: AHU
```

## 12. Self vs TypeVar

```python
# TypeVar — generic
T = TypeVar("T")
def identity(value: T) -> T:
    return value

# Self — current class/subclass
class Equipment:
    def reset(self) -> Self:
        return self
```

## 13. Deeper Difference

```python
# Old style
T = TypeVar("T", bound="Equipment")

class Equipment:
    def reset(self: T) -> T:
        return self

# Modern
class Equipment:
    def reset(self) -> Self:
        return self
```

## 14. Inheritance Chain

```python
class Equipment:
    def reset(self) -> Self:
        return self

class HVACEquipment(Equipment):
    pass

class AHU(HVACEquipment):
    pass

ahu = AHU()
result = ahu.reset()   # AHU
```

## 15. HVAC Builder

```python
class AHUConfig:
    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self

    def set_temperature(self, temperature: float) -> Self:
        self.temperature = temperature
        return self

config = AHUConfig().set_airflow(2500).set_temperature(22)
```

## 16. Subclass Add

```python
class AdvancedAHUConfig(AHUConfig):
    def set_filter_type(self, filter_type: str) -> Self:
        self.filter_type = filter_type
        return self

config = AdvancedAHUConfig().set_airflow(2500).set_filter_type("HEPA")
```

## 17. Runtime Kya

```python
class Equipment:
    def reset(self) -> Self:
        return self

# Runtime: self return
# Self: static typing only
```

## 18. Self vs self

```
self → runtime object
Self → static typing concept
```

## 19. Faide

```
Method chaining
Inheritance preserve
Factory methods
Builder pattern
Better static checking
```

## 20. Kab Use

```
Builder
Fluent API
ORM query
Configuration
Factory methods
Inheritance-heavy models
```

## 21. Warning

```
Simple classes → Self zaroori nahi
Subclass-preserving typing → Self power
```

## 22. Complete Example

```python
class Equipment:
    def __init__(self, equipment_id: str):
        self.equipment_id = equipment_id

    def start(self) -> Self:
        print(f"{self.equipment_id} started")
        return self

    def stop(self) -> Self:
        print(f"{self.equipment_id} stopped")
        return self

    @classmethod
    def create(cls, equipment_id: str) -> Self:
        return cls(equipment_id)

class AHU(Equipment):
    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self

ahu = AHU.create("AHU-001").start().set_airflow(2500).stop()
```

## 23. One-line

```python
def method(self) -> Self:
```

**"Jis actual class par call hua, usi type ka return."**

## 24. Mental Model

```
self → actual object
Self → actual object's class/type
```

## 25. Connection

```
TypeVar → generic relationship
Protocol → behavior
TypeGuard → narrow
Annotated → type + metadata
overload → input/output
cast → assertion
Self → current class/subclass
```

---

# Lesson 69: `typing.TYPE_CHECKING` — Circular Import Avoid

## 1. Circular Import

```python
# equipment.py
from ahu import AHU

class Equipment:
    def get_ahu(self) -> AHU:
        ...

# ahu.py
from equipment import Equipment

class AHU(Equipment):
    ...
```

**Explanation:**
- `Equipment → AHU → Equipment`

## 2. Problem

```
ImportError: cannot import name 'Equipment'
```

## 3. Sirf Type Hint Ke Liye

```python
# equipment.py
from ahu import AHU   # Sirf type hint ke liye

class Equipment:
    def get_ahu(self) -> AHU:
        ...
```

## 4. `TYPE_CHECKING`

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU

class Equipment:
    def get_ahu(self) -> "AHU":
        ...
```

## 5. Important Concept

```
TYPE_CHECKING → False at runtime
              → True for type checker
```

## 6. Practice

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU

class Equipment:
    def get_ahu(self) -> "AHU":
        return self.ahu
```

## 7. `from __future__ import annotations`

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU

class Equipment:
    def get_ahu(self) -> AHU:   # Quotes not needed
        ...
```

## 8. HVAC Example

```python
# equipment.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU
    from vav import VAV

class Equipment:
    def connected_ahu(self) -> AHU:
        ...
    def connected_vav(self) -> VAV:
        ...

# ahu.py
from equipment import Equipment

class AHU(Equipment):
    def start(self):
        print("AHU started")
```

## 9. TYPE_CHECKING Not Magic

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU

def check(obj):
    if isinstance(obj, AHU):   # Runtime error!
        ...
```

## 10. Kab Use

```python
if TYPE_CHECKING:
    from ahu import AHU
```

**Explanation:**
- Sirf type hints ke liye

## 11. Kab Na Use

```python
from ahu import AHU
ahu = AHU()   # Runtime required
```

## 12. Models Example

```python
# equipment.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from location import Location

class Equipment:
    location: Location

    def __init__(self, location: Location):
        self.location = location
```

## 13. Real Architecture

```
API → Service → Repository → Model
Equipment ↔ Location
Equipment ↔ WorkOrder
```

## 14. Runtime vs Type Dependency

```
Runtime → actual object/class
Type → annotation only
```

## 15. Mental Model

```
Normal import → runtime + type checker
TYPE_CHECKING → type checker only
```

## 16. Generic + TYPE_CHECKING

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from equipment import Equipment

T = TypeVar("T")

class Repository(Generic[T]):
    def get(self) -> T:
        ...
```

## 17. Protocol + TYPE_CHECKING

```python
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from equipment import Equipment

class EquipmentRepository(Protocol):
    def get(self, equipment_id: str) -> Equipment:
        ...
```

## 18. Difference

```
TYPE_CHECKING → runtime import hide
cast → existing object type
TypeGuard → runtime narrow
Protocol → behavior interface
```

## 19. Production Rule

```
Circular import? → runtime ya type-only?
Type-only → TYPE_CHECKING
Runtime bhi → refactor
```

## 20. Short Summary

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU
```

**"AHU ko type checker ke liye import, runtime par nahi."**

---

# Lesson 70: `typing.reveal_type()` — Debugging Types

## 1. Basic

```python
from typing import reveal_type

x = 100
reveal_type(x)
```

**Output (type checker):**
```
Revealed type is "int"
```

## 2. Print Nahi

```python
print(x)         # 100 (runtime value)
reveal_type(x)   # int (static type)
```

## 3. Simple Example

```python
name = "Muhammad"
reveal_type(name)   # str

temperature = 22.5
reveal_type(temperature)   # float
```

## 4. Type Inference

```python
equipment_id = "AHU-001"
reveal_type(equipment_id)   # str
```

## 5. Union

```python
value: int | str
reveal_type(value)   # int | str
```

## 6. Type Narrowing

```python
value: int | str

if isinstance(value, str):
    reveal_type(value)   # str
else:
    reveal_type(value)   # int
```

## 7. TypeGuard

```python
def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)

value: object

if is_string(value):
    reveal_type(value)   # str
```

## 8. TypeIs

```python
def is_string(value: int | str) -> TypeIs[str]:
    return isinstance(value, str)

value: int | str

if is_string(value):
    reveal_type(value)   # str
else:
    reveal_type(value)   # int
```

## 9. Generic

```python
T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

number = first([10, 20, 30])
reveal_type(number)   # int

name = first(["Ali", "Ahmed"])
reveal_type(name)   # str
```

## 10. Generic Architecture

```python
ahu_repo: Repository[AHU]
ahu = ahu_repo.get()
reveal_type(ahu)   # AHU
```

## 11. Self

```python
class Equipment:
    def reset(self) -> Self:
        return self

class AHU(Equipment):
    pass

ahu = AHU()
result = ahu.reset()
reveal_type(result)   # AHU
```

## 12. Literal

```python
status: Literal["ON", "OFF"] = "ON"
reveal_type(status)   # Literal['ON']
```

## 13. Overload

```python
@overload
def get_data(detailed: Literal[True]) -> dict: ...
@overload
def get_data(detailed: Literal[False]) -> str: ...

data = get_data(True)
reveal_type(data)   # dict

data = get_data(False)
reveal_type(data)   # str
```

## 14. TypedDict

```python
class EquipmentData(TypedDict):
    equipment_id: str
    airflow: float

equipment: EquipmentData = {"equipment_id": "AHU-001", "airflow": 2500.0}

reveal_type(equipment)   # EquipmentData
reveal_type(equipment["airflow"])   # float
```

## 15. Annotated

```python
Temperature = Annotated[float, "Celsius"]

temperature: Temperature = 22.5
reveal_type(temperature)   # float
```

## 16. Cast

```python
value = cast(str, some_value)
reveal_type(value)   # str
```

## 17. TYPE_CHECKING Difference

```
TYPE_CHECKING → runtime import control
reveal_type → inferred type inspect
```

## 18. Real Debugging

```python
def get_equipment():
    return {"id": "AHU-001", "airflow": 2500}

equipment = get_equipment()
reveal_type(equipment)
reveal_type(equipment["id"])
reveal_type(equipment["airflow"])
```

## 19. Large Code

```python
def process_equipment(data):
    if isinstance(data, dict):
        reveal_type(data)   # dict
    elif isinstance(data, list):
        reveal_type(data)   # list
```

## 20. Runtime Kya

```python
from typing import reveal_type

x = 100
result = reveal_type(x)
print(result)   # Some diagnostic
```

**Explanation:**
- Primary: static checking

## 21. Type Checker Difference

```
mypy, pyright, basedpyright
→ different diagnostic formats
```

## 22. reveal_type vs type

```python
# type() — runtime
print(type(x))   # <class 'int'>

# reveal_type() — static
reveal_type(x)   # int
```

## 23. Power

```python
reveal_type(variable)
```

**"Type checker, tum is variable ko kis type ka samajh rahe ho?"**

## 24. HVAC Example

```python
def get_airflow(value: int | float) -> int | float:
    return value

airflow = get_airflow(2500)
reveal_type(airflow)   # int or int | float depending on signature
```

## 25. Repository Example

```python
class Repository(Generic[T]):
    def __init__(self, item: T):
        self.item = item
    def get(self) -> T:
        return self.item

class AHU: pass

repo = Repository(AHU())
ahu = repo.get()
reveal_type(ahu)   # AHU
```

## 26. Unexpected Type

```
Expected: AHU
Got: Equipment or object
```

**Possible reasons:**
```
Wrong annotation
Missing generic parameter
Union too broad
Broad return type
Missing overload
Missing TypeGuard
cast required
Library typing incomplete
```

## 27. Complete Flow

```python
value: int | str | None

if value is not None:
    reveal_type(value)   # int | str

    if isinstance(value, str):
        reveal_type(value)   # str
```

## 28. Golden Rule

```
reveal_type() → production logic nahi
             → type debugging
```

## 29. Short Summary

| Tool | Purpose |
|------|---------|
| `type(x)` | Runtime actual type |
| `print(x)` | Runtime value |
| `reveal_type(x)` | Static inferred type |
| `cast(T, x)` | Type assertion |
| `TypeGuard` | Custom narrowing |
| `TypeIs` | Two-way narrowing |
| `TYPE_CHECKING` | Type-only imports |

## 30. One-line

```python
reveal_type(x)
```

**"Type checker, tumhare according `x` kis type ka hai?"**

## 31. Kab Useful

```
Generics debug
TypeGuard/TypeIs verify
Overloads verify
Self verify
Unions debug
Complex inference debug
```

---

**Ab ye guide complete hai (Lessons 61-70).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ Golden rules

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀