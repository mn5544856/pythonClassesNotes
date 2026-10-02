# Lesson 41: `dataclass` — Deep Understanding

Ab hum Python ka **`dataclass`** properly samjhenge. Ye especially tab useful hai jab tumhari class ka main purpose **data hold karna** ho aur tum manually bohat saara boilerplate `__init__`, `__repr__`, `__eq__` waghera nahi likhna chahte.

---

## 1. Normal class mein problem

Without dataclass:

```python
class Employee:

    def __init__(self, name, salary, department):
        self.name = name
        self.salary = salary
        self.department = department

    def __repr__(self):
        return (
            f"Employee("
            f"name={self.name!r}, "
            f"salary={self.salary!r}, "
            f"department={self.department!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented

        return (
            self.name == other.name
            and self.salary == other.salary
            and self.department == other.department
        )
```

Kaafi code likhna pada.

---

# 2. `@dataclass`

Ab:

```python
from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    salary: float
    department: str
```

Bas.

Python automatically useful methods generate kar deta hai.

Conceptually:

```text
@dataclass
     ↓
class ko process karo
     ↓
__init__()
__repr__()
__eq__()
etc.
```

---

# 3. Automatically `__init__()`

```python
employee = Employee(
    "Ali",
    5000,
    "HVAC"
)
```

Dataclass automatically equivalent initialization provide karti hai:

```python
employee.name
employee.salary
employee.department
```

Output conceptually:

```text
Ali
5000
HVAC
```

---

# 4. Automatically `__repr__()`

```python
print(employee)
```

Output:

```text
Employee(name='Ali', salary=5000, department='HVAC')
```

Normal class mein ye output automatically nahi milta.

---

# 5. Automatically `__eq__()`

```python
e1 = Employee("Ali", 5000, "HVAC")
e2 = Employee("Ali", 5000, "HVAC")
```

Then:

```python
print(e1 == e2)
```

Result:

```text
True
```

Kyun?

Dataclass fields ko compare karti hai.

---

# 6. Dataclass ka basic mental model

```text
@dataclass
    ↓
"Ye class mainly data represent karti hai"
    ↓
Python boilerplate generate kar de
```

---

# 7. Field annotations important hain

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature: float
    status: str
```

Yahan:

```text
equipment_id → str
temperature  → float
status       → str
```

Annotations dataclass ke fields define karne mein use hoti hain.

---

# 8. Default values

Tum default value de sakte ho:

```python
@dataclass
class Equipment:
    equipment_id: str
    status: str = "OFF"
```

Ab:

```python
ahu = Equipment("AHU-01")
```

to:

```python
ahu.status
```

result:

```text
OFF
```

Aur explicitly:

```python
ahu = Equipment("AHU-01", "ON")
```

to:

```text
ON
```

---

# 9. Field ordering rule

Ye important hai.

Correct:

```python
@dataclass
class Employee:
    name: str
    department: str
    salary: float = 5000
```

Yahan required fields pehle aur default field baad mein.

Problematic:

```python
@dataclass
class Employee:
    salary: float = 5000
    name: str
```

Conceptually generated `__init__` mein:

```python
def __init__(self, salary=5000, name):
```

jaisa invalid ordering ho jayega.

Rule:

> **Non-default fields pehle, default fields baad mein.**

Ye inheritance mein bhi important ho jata hai.

---

# 10. `field()`

Advanced control ke liye:

```python
from dataclasses import dataclass, field
```

Example:

```python
@dataclass
class Employee:
    name: str
    skills: list[str] = field(default_factory=list)
```

---

# 11. `default_factory`

Ye bohat important hai.

Galat pattern:

```python
@dataclass
class Employee:
    skills: list[str] = []
```

Mutable default ko is tarah define nahi karna chahiye.

Correct:

```python
@dataclass
class Employee:
    skills: list[str] = field(default_factory=list)
```

Ab:

```python
e1 = Employee("Ali")
e2 = Employee("Ahmed")
```

Dono ko separate lists milengi.

```text
e1.skills → separate list
e2.skills → separate list
```

---

# 12. `default_factory` ka mental model

```python
field(default_factory=list)
```

ko read karo:

> "Har new object ke liye `list()` call karke nayi list banao."

Similarly:

```python
field(default_factory=dict)
```

means:

> Har object ke liye naya dictionary banao.

---

# 13. Example: Work Order

Tumhare work-order context mein:

```python
from dataclasses import dataclass, field


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

Ab:

```python
wo = WorkOrder(
    "WO-1001",
    "HVAC",
    "AHU inspection",
    "Mechanical Room",
    "34"
)
```

Automatically:

```text
comment → ""
tags → []
```

---

# 14. `__post_init__()`

Kabhi kabhi tum chahte ho:

> Dataclass ka automatic `__init__()` complete hone ke baad additional processing ho.

Uske liye:

```python
@dataclass
class Employee:
    name: str
    salary: float

    def __post_init__(self):
        if self.salary < 0:
            raise ValueError("Salary negative nahi ho sakti")
```

Flow:

```text
Employee(...)
    ↓
generated __init__()
    ↓
fields assign
    ↓
__post_init__()
```

---

# 15. `__post_init__()` practical example

```python
@dataclass
class Temperature:
    celsius: float

    def __post_init__(self):
        if self.celsius < -273.15:
            raise ValueError(
                "Temperature absolute zero se kam nahi ho sakta"
            )
```

Now:

```python
t = Temperature(22.5)
```

valid.

But:

```python
t = Temperature(-300)
```

raises:

```text
ValueError
```

---

# 16. `__post_init__()` calculation ke liye bhi

```python
@dataclass
class Equipment:
    supply_temp: float
    return_temp: float
    delta_t: float = field(init=False)

    def __post_init__(self):
        self.delta_t = self.supply_temp - self.return_temp
```

Create:

```python
ahu = Equipment(14.0, 22.0)
```

Then:

```python
ahu.delta_t
```

result:

```text
-8.0
```

Yahan `delta_t` constructor mein manually nahi dena.

---

# 17. `init=False`

```python
delta_t: float = field(init=False)
```

Meaning:

> Is field ko generated `__init__()` mein parameter mat banao.

So generated constructor conceptually:

```python
Equipment(
    supply_temp,
    return_temp
)
```

not:

```python
Equipment(
    supply_temp,
    return_temp,
    delta_t
)
```

---

# 18. `repr=False`

Kabhi field ko printed representation mein nahi dikhana.

```python
@dataclass
class Employee:
    name: str
    salary: float = field(repr=False)
```

Then:

```python
print(employee)
```

salary representation mein hide ho sakti hai.

Useful jab kisi field ko normal representation mein show nahi karna ho.

---

# 19. `compare=False`

Default mein dataclass `__eq__()` fields compare karta hai.

Tum kisi field ko comparison se exclude kar sakte ho:

```python
@dataclass
class Employee:
    name: str
    department: str
    last_login: str = field(compare=False)
```

Ab equality comparison mein `last_login` ignore ho sakta hai.

---

# 20. `frozen=True`

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

Ab:

```python
point = Point(10, 20)
```

Aur:

```python
point.x = 50
```

allowed nahi hoga.

Conceptually object ko **immutable-like** bana diya.

---

# 21. `frozen=True` ka matlab

```text
Normal dataclass
↓
fields change ho sakte hain

frozen dataclass
↓
fields reassign nahi karne chahiye
```

Example:

```python
@dataclass(frozen=True)
class EquipmentID:
    value: str
```

Useful jab object ko value-object ki tarah treat karna ho.

---

# 22. `frozen` absolute security nahi

`frozen=True` ko:

> security mechanism

mat samjho.

Ye normal attribute assignment ko prevent karta hai through generated methods.

Python mein advanced mechanisms ke through internals manipulate kiye ja sakte hain.

Practical programming ke liye ise:

> **immutability intent / controlled immutable object**

samjho.

---

# 23. `order=True`

Dataclass comparison methods generate kar sakti hai.

```python
@dataclass(order=True)
class Temperature:
    value: float
```

Then:

```python
t1 = Temperature(20)
t2 = Temperature(25)

print(t1 < t2)
```

Result:

```text
True
```

Dataclass ordering fields ke according generate hoti hai.

---

# 24. `slots=True`

Modern Python mein:

```python
@dataclass(slots=True)
class Equipment:
    equipment_id: str
    temperature: float
```

Ye normal class ke `__dict__` based dynamic attributes ki jagah slots use kar sakti hai.

Conceptually:

```text
@dataclass
↓
normal instance storage

@dataclass(slots=True)
↓
slot-based instance storage
```

Ye tumhare previous `__slots__` lesson se directly connected hai.

---

# 25. `slots=True` ka benefit

Potential benefits:

* per-instance memory overhead reduce ho sakta hai
* arbitrary attributes normally prevent hote hain
* fixed object layout

Example:

```python
equipment = Equipment("AHU-01", 22.5)
```

Then arbitrary:

```python
equipment.random_value = 100
```

normally allowed nahi hoga with slots-only setup.

---

# 26. `kw_only=True`

Ye useful hai jab tum chahte ho constructor arguments keyword se diye jayen.

```python
@dataclass(kw_only=True)
class Equipment:
    equipment_id: str
    temperature: float
```

Then:

```python
equipment = Equipment(
    equipment_id="AHU-01",
    temperature=22.5
)
```

Instead of relying on positional order.

Large applications mein readability improve ho sakti hai.

---

# 27. Dataclass ka generated code conceptually

Agar:

```python
@dataclass
class Employee:
    name: str
    salary: float
```

to Python roughly ye responsibilities generate karta hai:

```text
Employee
├── __init__()
├── __repr__()
└── __eq__()
```

Exact generated implementation ko manually likhe code ke identical samajhna zaroori nahi; conceptually ye methods provide kiye jate hain.

---

# 28. Dataclass + inheritance

Dataclasses inheritance support karti hain.

```python
@dataclass
class Equipment:
    equipment_id: str


@dataclass
class AHU(Equipment):
    airflow: float
```

Now:

```python
ahu = AHU(
    equipment_id="AHU-01",
    airflow=5000
)
```

Inherited field:

```text
equipment_id
```

aur child field:

```text
airflow
```

dono constructor ka part ban sakte hain.

---

# 29. Dataclass vs `TypedDict`

Ab previous lesson connect karo.

### `TypedDict`

```python
class EquipmentData(TypedDict):
    equipment_id: str
    temperature: float
```

Data:

```python
{
    "equipment_id": "AHU-01",
    "temperature": 22.5
}
```

### Dataclass

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature: float
```

Data:

```python
Equipment(
    "AHU-01",
    22.5
)
```

Difference:

```text
TypedDict
→ dictionary-shaped data

dataclass
→ Python object-shaped data
```

---

# 30. Dataclass vs normal class

| Feature              | Normal Class | Dataclass            |
| -------------------- | ------------ | -------------------- |
| `__init__` automatic | ❌            | ✅                    |
| `__repr__` automatic | ❌            | ✅                    |
| `__eq__` automatic   | ❌            | ✅                    |
| Defaults             | Manual       | Easy                 |
| Validation           | Manual       | `__post_init__` etc. |
| Methods              | ✅            | ✅                    |
| Inheritance          | ✅            | ✅                    |
| Data-focused         | Depends      | Yes                  |

Important:

> Dataclass bhi normal Python class hi hoti hai.

`@dataclass` class ko replace nahi karta; class ko **transform/configure** karta hai.

---

# 31. Dataclass vs `NamedTuple`

Ye bhi useful distinction hai.

`NamedTuple`:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
```

Generally tuple-like immutable data structure hota hai.

Dataclass:

```python
@dataclass
class Point:
    x: int
    y: int
```

normal object-style data container hota hai.

---

# 32. Tumhare HVAC architecture mein

Ek clean design:

```python
from dataclasses import dataclass


@dataclass
class Equipment:
    equipment_id: str
    equipment_type: str
    floor: str
    area: str
```

Then:

```python
ahu = Equipment(
    equipment_id="AHU-01",
    equipment_type="AHU",
    floor="34",
    area="Mechanical Room"
)
```

Agar behavior bhi chahiye:

```python
@dataclass
class Equipment:
    equipment_id: str
    status: str = "OFF"

    def start(self):
        self.status = "ON"
```

Ab:

```python
ahu = Equipment("AHU-01")
ahu.start()
```

Ye demonstrate karta hai:

> Dataclass sirf passive data ke liye restricted nahi hai. Methods bhi add kar sakte ho.

---

# 33. `field()` ka mental model

```python
field(
    default=...,
    default_factory=...,
    init=...,
    repr=...,
    compare=...
)
```

Basically:

> **Field ke behavior ko customize karo.**

Common options:

```text
default
↓
default value

default_factory
↓
new value generate karo

init=False
↓
constructor mein mat lo

repr=False
↓
repr mein hide

compare=False
↓
equality/order comparison mein ignore
```

---

# 34. Complete practical example

```python
from dataclasses import dataclass, field


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
```

Create:

```python
ahu = Equipment(
    equipment_id="AHU-01",
    equipment_type="AHU",
    temperature=22.5
)
```

Then:

```python
ahu.start()

print(ahu)
```

Conceptually:

```text
Equipment(
    equipment_id='AHU-01',
    equipment_type='AHU',
    temperature=22.5,
    status='ON',
    tags=[]
)
```

---

# 35. Aaj ka mental model

```text
@dataclass
    ↓
normal class
    +
automatic data-related methods
```

Important features:

```text
@dataclass
↓
basic dataclass

field()
↓
field customization

default_factory
↓
fresh mutable value per object

__post_init__()
↓
initialization ke baad processing

frozen=True
↓
immutable-like object

slots=True
↓
slot-based storage

kw_only=True
↓
keyword-only constructor fields
```

### Sabse important distinction:

```text
TypedDict
→ dictionary ka shape

dataclass
→ Python object ka structure

Protocol
→ object ki capability/interface

Generic
→ reusable type parameterization
```

---

### Next Lesson 42

Ab hum **`Enum` + `Literal` + `StrEnum`** ko deeply samjhenge.

Example:

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

Aur dekhenge ke **`Literal["auto", "manual"]` aur `Enum` mein actual difference kya hai**, especially HVAC/BMS modes ke context mein.

# Lesson 42: `Enum` + `Literal` + `StrEnum`

Ab hum **fixed values** ko properly represent karna samjhenge.

Ye tumhare HVAC/BMS examples mein bohat useful hai, jaise:

```text
AUTO
MANUAL
OFF
ON
ALARM
```

Python mein in fixed choices ko represent karne ke 3 important approaches hain:

```text
Literal
Enum
StrEnum
```

---

# 1. Sabse pehle problem samjho

Suppose:

```python
def set_mode(mode: str):
    ...
```

Ab theoretically koi bhi string aa sakti hai:

```python
set_mode("auto")
set_mode("manual")
set_mode("hello")
set_mode("xyz")
```

Lekin actual system mein sirf:

```text
auto
manual
```

allowed hain.

Is problem ke liye `Literal` useful hai.

---

# 2. `Literal`

Tumne pehle `Literal` padha tha:

```python
from typing import Literal
```

Example:

```python
Mode = Literal["auto", "manual"]
```

Ab:

```python
def set_mode(mode: Mode):
    ...
```

Type checker ko pata hai:

```text
allowed:
├── "auto"
└── "manual"
```

Example:

```python
set_mode("auto")      # valid
set_mode("manual")   # valid
```

Lekin:

```python
set_mode("random")
```

static type checker ke perspective se incorrect hai.

---

# 3. `Literal` kya karta hai?

Important:

> `Literal` **exact value** ko type-level par represent karta hai.

Example:

```python
Literal[10]
```

means exact value:

```text
10
```

not:

```text
koi bhi int
```

Similarly:

```python
Literal["auto"]
```

means exact string:

```text
"auto"
```

---

# 4. Multiple Literal values

```python
Mode = Literal[
    "auto",
    "manual",
    "off"
]
```

Now:

```python
def set_mode(mode: Mode):
    ...
```

Allowed:

```python
set_mode("auto")
set_mode("manual")
set_mode("off")
```

Not allowed according to static typing:

```python
set_mode("test")
```

---

# 5. Problem: values repeat ho sakti hain

Suppose tumhare project mein 10 jagah:

```python
"auto"
"manual"
"off"
```

likh rahe ho.

Ye **magic strings** ban sakti hain.

Example:

```python
if mode == "auto":
    ...

if mode == "manual":
    ...

if mode == "off":
    ...
```

Large application mein typo ka risk hota hai:

```python
"manul"
```

---

# 6. `Enum`

Is situation mein `Enum` useful hai.

```python
from enum import Enum


class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"
```

Ab:

```python
Mode.AUTO
Mode.MANUAL
Mode.OFF
```

use kar sakte ho.

---

# 7. Enum member kya hai?

```python
Mode.AUTO
```

sirf string `"auto"` nahi hai.

Ye:

```text
Mode ka member
```

hai.

Example:

```python
print(Mode.AUTO)
```

Output generally:

```text
Mode.AUTO
```

Aur:

```python
print(Mode.AUTO.value)
```

output:

```text
auto
```

So:

```text
Mode.AUTO
↓
Enum member

Mode.AUTO.value
↓
actual stored value
"auto"
```

---

# 8. `Enum` ka basic structure

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

Mental model:

```text
Mode
│
├── AUTO
│    └── value = "auto"
│
└── MANUAL
     └── value = "manual"
```

---

# 9. Comparison

Important:

```python
Mode.AUTO == Mode.AUTO
```

True.

But:

```python
Mode.AUTO == "auto"
```

normally `Enum` ke case mein False hota hai.

Kyun?

Because:

```text
Mode.AUTO
```

aur:

```text
"auto"
```

different objects/types hain.

---

# 10. `.value`

Agar API ko actual string bhejni ho:

```python
mode = Mode.AUTO

print(mode.value)
```

Result:

```text
auto
```

Example:

```python
send_to_api(mode.value)
```

---

# 11. Enum iterate kar sakte ho

```python
for mode in Mode:
    print(mode)
```

Output:

```text
Mode.AUTO
Mode.MANUAL
Mode.OFF
```

Agar values:

```python
for mode in Mode:
    print(mode.value)
```

Output:

```text
auto
manual
off
```

---

# 12. Enum membership

```python
print(Mode.AUTO in Mode)
```

True.

Aur:

```python
list(Mode)
```

se members mil sakte hain.

---

# 13. `Enum` ka practical HVAC example

```python
from enum import Enum


class HVACMode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"
```

Class:

```python
class AHU:

    def __init__(self):
        self.mode = HVACMode.AUTO

    def set_mode(self, mode: HVACMode):
        self.mode = mode
```

Use:

```python
ahu = AHU()

ahu.set_mode(HVACMode.MANUAL)
```

Ab mode arbitrary string nahi.

---

# 14. Enum ka benefit

Instead of:

```python
ahu.set_mode("manual")
```

tum likhte ho:

```python
ahu.set_mode(HVACMode.MANUAL)
```

Isse code mein meaning clearer ho jata hai.

---

# 15. `Literal` vs `Enum`

Ye bohat important comparison hai.

### Literal

```python
Mode = Literal["auto", "manual"]
```

Focus:

```text
type checking
```

Ye actual runtime object/value representation nahi banata.

---

### Enum

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

Focus:

```text
runtime representation
+
named constants
+
grouping
```

---

# 16. Simple mental model

```text
Literal
↓
"Kaunsi exact values allowed hain?"

Enum
↓
"Allowed values ko named runtime members bana do."
```

---

# 17. `Enum` mein methods bhi ho sakte hain

Enum sirf values nahi rakhta.

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"

    def is_automatic(self):
        return self is Mode.AUTO
```

Now:

```python
mode = Mode.AUTO

print(mode.is_automatic())
```

Result:

```text
True
```

Yani Enum bhi class-based behavior rakh sakta hai.

---

# 18. Enum ke andar properties

Example:

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"

    @property
    def description(self):
        if self is Mode.AUTO:
            return "Automatic control"
        return "Manual control"
```

Then:

```python
Mode.AUTO.description
```

returns:

```text
Automatic control
```

---

# 19. `auto()`

Kabhi actual values important nahi hoti aur sirf unique members chahiye.

```python
from enum import Enum, auto


class Status(Enum):
    OFF = auto()
    ON = auto()
    ALARM = auto()
```

Python values automatically assign karega.

Conceptually:

```text
OFF   → 1
ON    → 2
ALARM → 3
```

Exact values ko business/API contract ke liye rely karna ho to explicit values dena usually clearer hota hai.

---

# 20. `StrEnum`

Python 3.11+ mein:

```python
from enum import StrEnum
```

Example:

```python
class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"
```

Ye Enum members ko string-oriented behavior deta hai.

Example:

```python
mode = Mode.AUTO

print(mode)
```

Generally:

```text
auto
```

milta hai, unlike ordinary `Enum` jahan representation:

```text
Mode.AUTO
```

hoti hai.

---

# 21. `Enum` vs `StrEnum`

Normal:

```python
class Mode(Enum):
    AUTO = "auto"
```

`Mode.AUTO` actual enum member hai.

`StrEnum`:

```python
class Mode(StrEnum):
    AUTO = "auto"
```

Enum member **string behavior bhi** provide karta hai.

Mental model:

```text
Enum
↓
named runtime value

StrEnum
↓
named runtime value
+
string behavior
```

---

# 22. API ke context mein `StrEnum`

Suppose API expects:

```json
{
    "mode": "auto"
}
```

`StrEnum` convenient ho sakta hai:

```python
class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
```

Then:

```python
mode = Mode.AUTO
```

String-oriented APIs ke saath ye natural fit ho sakta hai.

---

# 23. Important: `StrEnum` Python version

`StrEnum` Python **3.11** mein introduce hua.

Tumhare modern Python environment mein ye relevant hai, lekin agar project older Python version support karta ho to compatibility check karna hota hai.

---

# 24. `Literal` + `Enum` ek saath?

Kabhi function Enum expect kare:

```python
def set_mode(mode: HVACMode):
    ...
```

Aur kabhi raw API string:

```python
def send_mode(mode: Literal["auto", "manual"]):
    ...
```

Ye two different layers ho sakti hain:

```text
Application layer
↓
HVACMode.AUTO

API layer
↓
"auto"
```

Conversion:

```python
api_value = HVACMode.AUTO.value
```

---

# 25. Enum aur `Literal` ka architecture

Ek clean system:

```text
User/Application
      ↓
HVACMode.AUTO
      ↓
Enum
      ↓
.value
      ↓
"auto"
      ↓
API / BMS
```

Isse internal code mein named constants aur external system mein expected raw value dono maintain ho sakte hain.

---

# 26. `Literal` kab use karna?

Agar choices:

* choti hain
* simple hain
* primarily type checking ke liye hain
* runtime object ki zaroorat nahi

Example:

```python
def set_speed(
    speed: Literal["low", "medium", "high"]
):
    ...
```

Ye simple aur clear hai.

---

# 27. `Enum` kab use karna?

Agar:

* values application-wide repeatedly use hongi
* named constants chahiye
* runtime identity/grouping chahiye
* methods/properties chahiye
* business/domain model banana hai

Example:

```python
class AlarmState(Enum):
    NORMAL = "normal"
    WARNING = "warning"
    ALARM = "alarm"
```

---

# 28. `StrEnum` kab useful?

Jab:

```text
named enum members
+
string values
+
API/JSON/string-oriented systems
```

chahiye.

Example:

```python
class EquipmentStatus(StrEnum):
    ON = "on"
    OFF = "off"
    FAULT = "fault"
```

---

# 29. Enum + dataclass

Ye bhi combine ho sakte hain.

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
```

Create:

```python
ahu = Equipment("AHU-01")
```

Then:

```python
ahu.status
```

is:

```text
Status.OFF
```

Aur:

```python
ahu.status.value
```

is:

```text
"off"
```

---

# 30. Enum + pattern matching

Modern Python mein `match` ke saath bhi use kar sakte ho:

```python
def handle_status(status: Status):

    match status:
        case Status.ON:
            print("Running")

        case Status.OFF:
            print("Stopped")
```

Ye domain logic ko readable bana sakta hai.

---

# 31. Enum vs constants

Without Enum:

```python
AUTO = "auto"
MANUAL = "manual"
OFF = "off"
```

Problem: related values ek formal type/group mein nahi hain.

With Enum:

```python
class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"
```

Ab:

```text
Mode
├── AUTO
├── MANUAL
└── OFF
```

Ek logical domain type mil gaya.

---

# 32. Aaj ka comparison

| Feature              | `Literal` | `Enum`           | `StrEnum`  |
| -------------------- | --------- | ---------------- | ---------- |
| Static type checking | ✅         | ✅                | ✅          |
| Runtime members      | ❌         | ✅                | ✅          |
| Named constants      | Limited   | ✅                | ✅          |
| Exact fixed values   | ✅         | ✅                | ✅          |
| String-oriented      | N/A       | Normal Enum nahi | ✅          |
| Methods/properties   | ❌         | ✅                | ✅          |
| API string use       | Simple    | `.value`         | Convenient |

---

# 33. Sabse important mental model

```text
Literal
"Sirf ye values allowed hain."

Enum
"In values ko named runtime members banao."

StrEnum
"Named Enum members + string behavior."
```

Example:

```python
Mode = Literal["auto", "manual"]
```

versus:

```python
class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

versus:

```python
class Mode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"
```

---

## Final connection

Ab tumhare previous typing concepts ko ek saath dekho:

```text
TypedDict
    ↓
dictionary ka structure

dataclass
    ↓
object ka data structure

Protocol
    ↓
object ki required capability

Generic
    ↓
type ko reusable banao

TypeVar
    ↓
generic type placeholder

Literal
    ↓
exact allowed values

Enum / StrEnum
    ↓
named runtime values
```

### Next Lesson 43

Ab hum **`collections.abc`** ko deeply cover karenge:

```python
Iterable
Iterator
Sequence
MutableSequence
Mapping
MutableMapping
Set
Callable
```

Aur sabse important question solve karenge:

> **`Iterable`, `Iterator`, `Sequence`, `Mapping` mein actual difference kya hai aur Python function mein `list` ke bajaye `Sequence` ya `Iterable` kab use karna chahiye?**

# Lesson 43: `Iterable`, `Iterator`, `Sequence`, `Mapping` — Deep Understanding

Ye lesson tumhare pehle wale question:

```python
from typing import Iterable, Iterator, Sequence, Mapping, MutableMapping, Callable
```

ko properly connect karega.

Sabse pehle ek important baat:

> `list` ek concrete data structure hai, jab ke `Iterable`, `Sequence`, `Mapping` etc. **interfaces/capabilities** ko describe karte hain.

---

# 1. `Iterable` kya hai?

Simple definition:

> Jis object ko `for` loop mein iterate kar sakte ho, woh generally `Iterable` hai.

Examples:

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

`list` iterable hai.

String:

```python
for char in "ABC":
    print(char)
```

String bhi iterable hai.

Dictionary:

```python
data = {"name": "Ali", "age": 30}

for key in data:
    print(key)
```

Dictionary bhi iterable hai.

---

# 2. `Iterable` ka core protocol

Conceptually:

```text
Iterable
   ↓
__iter__()
   ↓
Iterator
```

Python mein:

```python
iter(obj)
```

object se iterator obtain karta hai.

Example:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)
```

Ab:

```python
next(iterator)
```

gives:

```text
10
```

phir:

```python
next(iterator)
```

gives:

```text
20
```

---

# 3. `Iterable` aur `Iterator` same nahi hain

Ye bohat important hai.

### Iterable

> "Mere andar se iterator bana sakte ho."

### Iterator

> "Main next item provide kar sakta hoon."

Diagram:

```text
Iterable
   │
   │ iter()
   ↓
Iterator
   │
   │ next()
   ↓
Values
```

---

# 4. Example

```python
numbers = [10, 20, 30]
```

`numbers`:

```text
Iterable
```

Then:

```python
it = iter(numbers)
```

`it`:

```text
Iterator
```

Then:

```python
next(it)
```

→ `10`

```python
next(it)
```

→ `20`

```python
next(it)
```

→ `30`

Then:

```python
next(it)
```

raises:

```text
StopIteration
```

---

# 5. `for` loop internally kya karta hai?

Jab tum likhte ho:

```python
for x in numbers:
    print(x)
```

conceptually Python kuch is tarah ka process karta hai:

```python
iterator = iter(numbers)

while True:
    try:
        x = next(iterator)
        print(x)
    except StopIteration:
        break
```

Isliye:

```text
for
↓
iter()
↓
next()
↓
StopIteration
```

---

# 6. `Iterator` khud bhi `Iterable` hota hai

Iterator ke paas:

```text
__iter__()
__next__()
```

hote hain.

Usually:

```python
iter(iterator)
```

same iterator return karta hai.

So:

```text
Iterator ⊂ Iterable
```

Conceptually:

```text
Iterable
├── list
├── tuple
├── str
├── dict
├── set
└── iterator
```

---

# 7. `Sequence`

Ab `Sequence` stronger concept hai.

```python
from collections.abc import Sequence
```

Sequence generally:

> ordered collection jisme positional/index-based access hota hai.

Examples:

```python
list
tuple
str
```

Example:

```python
numbers = [10, 20, 30]

numbers[0]
```

→ `10`

Aur:

```python
numbers[1]
```

→ `20`

---

# 8. Sequence ki capabilities

Typical sequence:

```text
ordered
   +
indexing
   +
iteration
   +
length
```

Example:

```python
numbers[0]
len(numbers)
```

Aur generally membership:

```python
20 in numbers
```

---

# 9. `Iterable` vs `Sequence`

Ye important hai.

### Iterable

Sirf itna assume karo:

```text
for loop possible
```

### Sequence

Zyada guarantees:

```text
for loop
+
indexing
+
length
+
ordered sequence behavior
```

Diagram:

```text
Iterable
   ↑
   │
Sequence
```

Sequence ek more specific collection concept hai.

---

# 10. Example: function mein `list` kyun nahi?

Suppose:

```python
def first_item(items: list[str]) -> str:
    return items[0]
```

Ye sirf `list[str]` accept karne ka type contract deta hai.

Lekin function ko actually list ki zaroorat nahi.

Usko sirf chahiye:

```text
ordered
+
indexable
```

To better:

```python
from collections.abc import Sequence

def first_item(items: Sequence[str]) -> str:
    return items[0]
```

Ab ye list ke ilawa tuple ke saath bhi kaam karega:

```python
first_item(["Ali", "Ahmed"])
first_item(("Ali", "Ahmed"))
```

---

# 11. Ye principle important hai

> **Function ko jitni capability chahiye, utna hi general interface type karo.**

Agar sirf iteration chahiye:

```python
Iterable[str]
```

Agar indexing chahiye:

```python
Sequence[str]
```

Agar key-value access chahiye:

```python
Mapping[str, int]
```

Ye software design mein **programming to an interface / abstraction** ke concept se related hai.

---

# 12. `Iterable` example

Suppose:

```python
def print_items(items: Iterable[str]) -> None:

    for item in items:
        print(item)
```

Ab input ho sakta hai:

```python
print_items(["A", "B"])
```

tuple:

```python
print_items(("A", "B"))
```

set:

```python
print_items({"A", "B"})
```

generator:

```python
print_items(x for x in ["A", "B"])
```

Kyun?

Function ko sirf:

```text
iteration
```

chahiye.

---

# 13. Agar `Sequence` use karein?

```python
def print_first(items: Sequence[str]) -> str:
    return items[0]
```

Ab generator suitable nahi:

```python
print_first(x for x in ["A", "B"])
```

Kyun?

Generator generally indexable Sequence nahi hai.

---

# 14. `Mapping`

Ab dictionary side.

```python
from collections.abc import Mapping
```

`Mapping` ka concept:

> key → value relationship.

Example:

```python
employee = {
    "name": "Ali",
    "salary": 5000
}
```

Ye mapping hai.

---

# 15. Mapping ki core capability

```text
key
 ↓
value
```

Example:

```python
employee["name"]
```

→ `"Ali"`

Aur:

```python
employee["salary"]
```

→ `5000`

---

# 16. `dict` vs `Mapping`

`dict` concrete implementation hai.

`Mapping` interface/abstract collection concept hai.

```text
Mapping
├── dict
├── other mapping implementations
└── custom mappings
```

Agar function ko sirf read access chahiye:

```python
def show_name(data: Mapping[str, str]):
    print(data["name"])
```

to function ko specifically `dict` ki zaroorat nahi.

---

# 17. `Mapping` read-oriented hai

Conceptually:

```text
Mapping
↓
read key → value
```

Example:

```python
data["name"]
data.get("name")
data.keys()
data.values()
data.items()
```

---

# 18. `MutableMapping`

Ab:

```python
from collections.abc import MutableMapping
```

`MutableMapping` ka matlab:

> Mapping + values/entries modify karne ki capability.

Example:

```python
data = {
    "name": "Ali",
    "salary": 5000
}

data["salary"] = 6000
```

Yahan modification ho rahi hai.

---

# 19. Mapping vs MutableMapping

```text
Mapping
↓
read-oriented

MutableMapping
↓
read + modify
```

Example:

```python
def show(data: Mapping[str, int]):
    ...
```

Function data ko read kar sakta hai.

Aur:

```python
def update(data: MutableMapping[str, int]):
    data["salary"] = 6000
```

function mutation expect kar raha hai.

---

# 20. `Sequence` vs `MutableSequence`

Same concept.

### Sequence

```text
ordered + indexable
```

### MutableSequence

```text
ordered + indexable + modification
```

Example:

```python
from collections.abc import MutableSequence
```

List is a mutable sequence.

```python
numbers = [10, 20, 30]

numbers[0] = 100
numbers.append(40)
```

---

# 21. Important hierarchy

Conceptually:

```text
Iterable
│
├── Sequence
│   └── MutableSequence
│
└── other iterables
```

Aur:

```text
Mapping
└── MutableMapping
```

Exact ABC inheritance relationships ko implementation-specific assumptions se confuse nahi karna chahiye, lekin capability hierarchy ko is tarah samajhna useful hai.

---

# 22. `Callable`

Ab:

```python
from collections.abc import Callable
```

`Callable` means:

> Jise `()` se call kar sakte ho.

Example:

```python
def add(a, b):
    return a + b
```

Function callable hai:

```python
add(10, 20)
```

---

# 23. Callable sirf functions nahi

Previous lesson mein dekha:

```python
class Calculator:

    def __call__(self, a, b):
        return a + b
```

Now:

```python
calc = Calculator()
```

`calc` callable hai:

```python
calc(10, 20)
```

Kyun?

Because:

```text
calc
 ↓
__call__()
```

---

# 24. Type annotation

```python
from collections.abc import Callable

def execute(
    operation: Callable[[int, int], int],
    a: int,
    b: int
) -> int:

    return operation(a, b)
```

Yahan function expect karta hai:

```text
Callable
↓
2 int inputs
↓
int output
```

---

# 25. `Iterable` aur `Iterator` ka code

Tum khud custom iterator bana sakte ho:

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
```

Use:

```python
counter = Counter(3)

for value in counter:
    print(value)
```

Output:

```text
0
1
2
```

---

# 26. Yahan kya ho raha hai?

```text
Counter
 ↓
__iter__()
 ↓
Counter itself as iterator
 ↓
__next__()
 ↓
0
 ↓
__next__()
 ↓
1
 ↓
__next__()
 ↓
2
 ↓
StopIteration
```

Ye tumhare generators wale lesson se directly connected hai.

Generator automatically iterator protocol handle kar deta hai.

---

# 27. Generator vs custom Iterator

Manual:

```python
class Counter:

    def __iter__(self):
        return self

    def __next__(self):
        ...
```

Generator:

```python
def counter():
    yield 0
    yield 1
    yield 2
```

Generator mein Python iterator machinery ka bohat sa kaam automatically handle karta hai.

---

# 28. `Iterable` function design example

Tumhare work-order script mein:

```python
def create_folders(rows: Iterable[WorkOrder]):
    for row in rows:
        ...
```

Ye:

```python
list[WorkOrder]
```

se zyada flexible hai.

Ab rows source ho sakta hai:

```text
list
tuple
generator
CSV iterator
API stream
database result iterator
```

Function ko sirf iteration chahiye.

---

# 29. `Sequence` kab use karna?

Agar tum:

```python
rows[0]
rows[1]
len(rows)
```

kar rahe ho:

```python
def process(rows: Sequence[WorkOrder]):
    first = rows[0]
```

`Sequence` better abstraction hai.

---

# 30. `Mapping` kab use karna?

Agar:

```python
row["Work Order Number"]
row["Description"]
```

access karna hai:

```python
def process(row: Mapping[str, str]):
    work_order = row["Work Order Number"]
```

Mapping natural abstraction hai.

---

# 31. `TypedDict` aur `Mapping` ka connection

Previous lesson:

```python
class WorkOrder(TypedDict):
    work_order_number: str
    description: str
```

Ye **specific dictionary structure** describe karta hai.

Mapping:

```python
Mapping[str, str]
```

generic key/value capability describe karta hai.

So:

```text
TypedDict
↓
exact known keys

Mapping
↓
generic key/value interface
```

---

# 32. `dict` vs `Mapping` vs `TypedDict`

| Type             | Focus                               |
| ---------------- | ----------------------------------- |
| `dict`           | Concrete dictionary                 |
| `Mapping`        | Generic read-only mapping interface |
| `MutableMapping` | Generic mutable mapping interface   |
| `TypedDict`      | Specific dictionary schema          |

Example:

```text
dict
→ "Ye actual dictionary hai"

Mapping
→ "Mujhe key/value read karna hai"

MutableMapping
→ "Mujhe key/value modify bhi karna hai"

TypedDict
→ "Mujhe ye exact keys aur types chahiye"
```

---

# 33. `list` vs `Sequence` vs `Iterable`

Ye bhi memorize-worthy hai:

| Type                 | Capability              |
| -------------------- | ----------------------- |
| `Iterable[T]`        | iterate                 |
| `Sequence[T]`        | iterate + ordered/index |
| `MutableSequence[T]` | sequence + modify       |

Example:

```python
def f1(data: Iterable[int]):
    for x in data:
        ...
```

```python
def f2(data: Sequence[int]):
    x = data[0]
```

```python
def f3(data: MutableSequence[int]):
    data[0] = 100
```

---

# 34. Sabse important design principle

Suppose function:

```python
def total(numbers: list[int]) -> int:
    return sum(numbers)
```

Function ko actual mein list ki koi special capability chahiye nahi.

Usko sirf iteration chahiye.

Better:

```python
def total(numbers: Iterable[int]) -> int:
    return sum(numbers)
```

Ab generator bhi:

```python
total(x for x in range(100))
```

work kar sakta hai.

Ye **interface-oriented type design** hai.

---

# 35. Capability ladder

Isko ek mental model ki tarah dekho:

```text
Iterable
   ↓
"I can iterate"

Sequence
   ↓
"I can iterate + index"

MutableSequence
   ↓
"I can iterate + index + modify"
```

Mapping side:

```text
Mapping
   ↓
"I can read key/value"

MutableMapping
   ↓
"I can read + modify key/value"
```

Callable:

```text
Callable
   ↓
"I can be called with ()"
```

---

# 36. Modern imports

Tumne pehle `typing` se ye imports dekhe:

```python
from typing import Iterable, Iterator, Sequence, Mapping
```

Modern Python mein runtime collection ABCs ke liye generally:

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

prefer kiya jata hai.

Typing context mein annotations ke liye ye modern approach clean hai.

---

# 37. Final mental map

```text
Iterable
    │
    └── iter()
          ↓
       Iterator
          │
          └── next()

Sequence
    │
    ├── ordered
    ├── indexable
    └── iterable

MutableSequence
    │
    └── Sequence + modification

Mapping
    │
    └── key → value

MutableMapping
    │
    └── Mapping + modification

Callable
    │
    └── object()
```

### Ek line mein yaad rakho:

> **`Iterable` batata hai "iterate kar sakte ho", `Sequence` batata hai "ordered/indexable bhi hai", `Mapping` batata hai "key-value access hai", aur `Mutable...` versions modification ki capability add karte hain.**

### Next Lesson 44

Ab hum **Python Abstract Base Classes (`collections.abc` + `ABC`)** ko connect karenge:

```text
ABC
abstractmethod
collections.abc
virtual subclass
register()
__subclasshook__()
```

Aur samjhenge ke **`Protocol` aur ABC mein actual architectural difference kya hai**.

# Lesson 44: ABC + `collections.abc` + `Protocol` — Actual Difference

Ab hum previous lessons ko connect karte hain:

```text
ABC
Protocol
collections.abc
```

Ye teen concepts similar lagte hain, lekin inka purpose different hai.

---

# 1. ABC kya hota hai?

ABC = **Abstract Base Class**

Python mein:

```python
from abc import ABC, abstractmethod
```

Example:

```python
class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass
```

Ab `Equipment` ek abstract class hai.

```python
equipment = Equipment()
```

❌ Ye normally instantiate nahi ho sakti, kyunki `start()` abstract hai.

---

# 2. Child class ko method implement karna hoga

```python
class AHU(Equipment):

    def start(self):
        print("AHU started")
```

Ab:

```python
ahu = AHU()
ahu.start()
```

Output:

```text
AHU started
```

Mental model:

```text
ABC
 ↓
contract define karo
 ↓
child class
 ↓
contract implement karo
```

---

# 3. ABC ka main purpose

ABC ka purpose sirf type checking nahi hai.

Ye **runtime class hierarchy + contract** establish karta hai.

Example:

```python
class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
```

Ab har concrete equipment ko:

```text
start()
stop()
```

provide karna hoga.

---

# 4. `collections.abc` kya hai?

Python standard library mein already bohat se abstract collection interfaces defined hain.

Example:

```python
from collections.abc import Iterable
```

Aur:

```python
from collections.abc import Sequence
from collections.abc import Mapping
from collections.abc import MutableMapping
from collections.abc import Iterator
from collections.abc import Callable
```

Ye ABC-based collection interfaces hain.

---

# 5. Example: `Sequence`

Tumne previous lesson mein dekha:

```python
from collections.abc import Sequence
```

Conceptually `Sequence` ek interface/ABC hai jo sequence behavior describe karta hai.

Typical capabilities:

```text
indexing
length
iteration
```

Example:

```python
numbers = [10, 20, 30]

isinstance(numbers, Sequence)
```

List sequence behavior provide karti hai.

---

# 6. ABC ka `register()`

ABC ka ek interesting feature hai:

```python
ABC.register(...)
```

Example:

```python
from abc import ABC


class Equipment(ABC):
    pass
```

Ab kisi unrelated class ko virtual subclass register kar sakte ho:

```python
class Sensor:
    pass


Equipment.register(Sensor)
```

Ab:

```python
isinstance(Sensor(), Equipment)
```

`True` ho sakta hai.

Lekin important:

> `Sensor` ki actual inheritance chain mein `Equipment` add nahi hua.

Yani:

```python
class Sensor:
    pass
```

ab bhi source code mein `Equipment` inherit nahi karta.

---

# 7. Virtual subclass

Is concept ko:

> **Virtual subclass**

kehte hain.

Normal inheritance:

```text
Equipment
    ↑
   AHU
```

Virtual registration:

```text
Equipment
    :
    : registered
    ↓
  Sensor
```

Yahan relationship runtime ABC mechanism ke through recognize ki ja sakti hai, lekin normal class inheritance nahi hai.

---

# 8. `Protocol` se connection

Ab tumhara previous lesson:

```python
from typing import Protocol
```

Example:

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Aur:

```python
class AHU:

    def start(self) -> None:
        print("Started")
```

AHU ne:

```python
class AHU(Startable)
```

nahi likha.

Phir bhi static type checker ke liye:

```text
AHU
 ↓
has start()
 ↓
satisfies Startable
```

Ye **structural typing** hai.

---

# 9. ABC vs Protocol

Ye sabse important part hai.

### ABC

```python
class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass
```

Focus:

```text
explicit inheritance
+
runtime hierarchy
+
abstract contract
```

### Protocol

```python
class Startable(Protocol):

    def start(self):
        ...
```

Focus:

```text
structure/capability
+
static structural typing
+
loose coupling
```

---

# 10. Nominal vs Structural typing

Do important terms:

### Nominal typing

Relationship declared hota hai.

```python
class AHU(Equipment):
    ...
```

Python/type system ko explicitly bataya:

```text
AHU IS-A Equipment
```

Ye nominal relationship hai.

---

### Structural typing

Relationship methods/attributes se determine hota hai.

```python
class AHU:

    def start(self):
        ...
```

Agar required structure match karta hai:

```text
AHU has start()
```

to Protocol satisfy kar sakta hai.

---

# 11. Simple mental model

```text
ABC
↓
"Who are you?"
↓
"I am an Equipment."

Protocol
↓
"What can you do?"
↓
"I can start()."
```

Ye distinction bohat useful hai.

---

# 12. ABC mein inheritance zaroori hoti hai?

Normal ABC usage mein:

```python
class AHU(Equipment):
    ...
```

explicit inheritance use hoti hai.

Agar:

```python
class AHU:
    def start(self):
        ...
```

likho, to sirf `start()` hone se automatically `Equipment` ka subclass nahi ban jata.

---

# 13. Protocol mein inheritance zaroori nahi

```python
class Startable(Protocol):

    def start(self):
        ...
```

Then:

```python
class AHU:

    def start(self):
        print("AHU started")
```

AHU ko `Startable` inherit karne ki zaroorat nahi.

---

# 14. Runtime `isinstance()` difference

Protocol ke saath:

```python
isinstance(ahu, Startable)
```

normally runtime par allowed nahi hota unless:

```python
@runtime_checkable
```

use karo.

Example:

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Now:

```python
isinstance(ahu, Startable)
```

possible ho sakta hai.

---

# 15. Lekin ek important limitation

`@runtime_checkable` ka matlab ye nahi:

> Python runtime full type annotations verify karega.

Agar protocol:

```python
class Sensor(Protocol):

    def read(self) -> float:
        ...
```

hai, runtime structural check primarily required attribute/method presence ko check karta hai.

Ye necessarily verify nahi karta ke:

```python
read()
```

actually `float` hi return kar raha hai.

So:

```text
Static type checker
↓
more detailed type compatibility

Runtime protocol check
↓
mainly structural presence
```

---

# 16. ABC + Protocol same project mein

Ye dono ek project mein simultaneously use ho sakte hain.

Example:

```python
from abc import ABC, abstractmethod
from typing import Protocol


class Equipment(ABC):

    @abstractmethod
    def start(self) -> None:
        pass


class Monitorable(Protocol):

    def get_status(self) -> str:
        ...
```

Ab:

```python
class AHU(Equipment):

    def start(self):
        print("AHU started")

    def get_status(self) -> str:
        return "ON"
```

AHU:

```text
Equipment
↓
explicit inheritance

Monitorable
↓
structural compatibility
```

---

# 17. Ye architecture mein powerful kyun hai?

Suppose tumhare paas:

```text
AHU
VAV
Pump
Fan
Chiller
```

sab `start()` kar sakte hain.

Tumhe ek Protocol chahiye:

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab function:

```python
def start_equipment(item: Startable):
    item.start()
```

Is function ko farq nahi:

```text
AHU?
VAV?
Pump?
Fan?
```

Bas:

```text
start()
```

hona chahiye.

---

# 18. ABC kab better ho sakta hai?

Agar tum domain hierarchy define kar rahe ho:

```text
Equipment
├── AHU
├── VAV
├── Pump
└── Fan
```

Aur common behavior/state bhi hai:

```python
class Equipment(ABC):

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    @abstractmethod
    def start(self):
        pass
```

Yahan ABC natural hai.

Kyun?

Because tum actual domain hierarchy bana rahe ho.

---

# 19. Protocol kab better ho sakta hai?

Suppose tumhare paas unrelated classes hain:

```text
AHU
DatabaseConnection
APIClient
MockEquipment
TestDevice
```

Lekin sab mein:

```python
start()
```

available hai.

Tumhe inheritance force nahi karni.

Protocol:

```python
class Startable(Protocol):

    def start(self):
        ...
```

Useful hai.

---

# 20. `collections.abc` ka role

Ab previous lesson se connect karo.

Python ne common behaviors ke liye ready-made ABCs diye hue hain:

```text
Iterable
Iterator
Sequence
MutableSequence
Mapping
MutableMapping
Set
MutableSet
Callable
```

Isliye har baar khud:

```python
class MyIterable(ABC):
    ...
```

banane ki zaroorat nahi.

---

# 21. Example: custom collection

Suppose tum apna collection banana chahte ho:

```python
from collections.abc import Sequence


class EquipmentList(Sequence):

    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)
```

Ab:

```python
equipment = EquipmentList([
    "AHU-01",
    "AHU-02",
    "VAV-01"
])
```

Sequence behavior milta hai.

```python
equipment[0]
```

→

```text
AHU-01
```

Aur:

```python
len(equipment)
```

→

```text
3
```

---

# 22. Yahan ABC tumhare liye kya kar raha hai?

`Sequence` keh raha hai:

```text
Agar tum Sequence banna chahte ho
to required operations provide karo.
```

Tumne:

```python
__getitem__()
__len__()
```

implement kiye.

Ab Python ko pata hai ke object sequence behavior provide karta hai.

---

# 23. `Protocol` version

Same concept ko Protocol se define kar sakte ho:

```python
from typing import Protocol


class Startable(Protocol):

    def start(self) -> None:
        ...
```

Phir:

```python
class Fan:

    def start(self):
        print("Fan started")
```

Fan ko Protocol inherit karne ki zaroorat nahi.

---

# 24. ABC vs Protocol vs `collections.abc`

Ek table:

| Concept              | Main purpose                                 |
| -------------------- | -------------------------------------------- |
| `ABC`                | Explicit abstract class hierarchy            |
| `abstractmethod`     | Required implementation                      |
| `collections.abc`    | Standard collection interfaces/ABCs          |
| `Protocol`           | Structural typing / capability contract      |
| `register()`         | ABC virtual subclass registration            |
| `@runtime_checkable` | Protocol ka limited runtime structural check |

---

# 25. `ABC` vs `dataclass`

Previous lesson ke context mein:

```python
@dataclass
class Equipment:
    equipment_id: str
```

Dataclass ka focus:

```text
data
```

ABC ka focus:

```text
contract/hierarchy
```

Dono combine bhi ho sakte hain.

---

# 26. ABC + dataclass

Example:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Equipment(ABC):
    equipment_id: str

    @abstractmethod
    def start(self):
        pass
```

Child:

```python
@dataclass
class AHU(Equipment):
    temperature: float

    def start(self):
        print(f"{self.equipment_id} started")
```

Now:

```python
ahu = AHU("AHU-01", 22.5)
```

---

# 27. Important architectural distinction

Isko strongly remember karo:

```text
ABC
↓
Inheritance-oriented design

Protocol
↓
Capability-oriented design

collections.abc
↓
Standard collection capability interfaces
```

---

# 28. Tumhare Python journey mein connection

Ab tak:

```text
Inheritance
     ↓
Polymorphism
     ↓
Abstraction
     ↓
ABC
     ↓
Protocol
     ↓
Structural typing
     ↓
collections.abc
```

Ye sab ek doosre se connected hain.

---

# 29. Real-world HVAC example

Suppose:

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

AHU:

```python
class AHU:

    def start(self):
        print("AHU ON")
```

Pump:

```python
class Pump:

    def start(self):
        print("Pump ON")
```

Fan:

```python
class Fan:

    def start(self):
        print("Fan ON")
```

Function:

```python
def start_device(device: Startable):
    device.start()
```

Ab:

```python
start_device(AHU())
start_device(Pump())
start_device(Fan())
```

Same interface:

```text
start()
```

different implementations.

Ye:

```text
Protocol
+
Structural typing
+
Polymorphism
```

ka combination hai.

---

# 30. Final mental map

```text
ABC
│
├── explicit inheritance
├── abstract methods
├── runtime hierarchy
└── virtual subclass registration

Protocol
│
├── structural typing
├── capability/interface
├── inheritance required nahi
└── static type checking

collections.abc
│
├── Iterable
├── Iterator
├── Sequence
├── Mapping
├── MutableMapping
└── Callable
```

### One-line rule

> **ABC kehta hai "is hierarchy ka member ho aur ye contract implement karo"; Protocol kehta hai "mujhe inheritance se matlab nahi, bas required capability provide karo."**

---

## Next Lesson 45

Ab hum **`collections` ke concrete data structures** dekhenge:

```text
list
tuple
deque
set
frozenset
dict
defaultdict
Counter
OrderedDict
```

Aur especially:

> **`list` vs `deque` vs `set` vs `dict` ko performance aur use-case ke perspective se kab choose karna hai?**

# Lesson 45: `list` vs `deque` vs `set` vs `dict` + `collections`

Ab hum Python ke **real data structures** ko performance aur use-case ke perspective se samjhenge.

Sabse pehle ek important distinction:

```text
collections.abc
↓
interface / capability

collections
↓
concrete data structures / utilities
```

---

# 1. `list`

Sabse common collection:

```python
numbers = [10, 20, 30, 40]
```

`list`:

```text
ordered
indexable
mutable
duplicates allowed
```

Example:

```python
numbers[0]
```

→ `10`

Modify:

```python
numbers[0] = 100
```

Add:

```python
numbers.append(50)
```

---

# 2. `list` ka performance model

Important operations:

| Operation      | Typical complexity |
| -------------- | -----------------: |
| `items[i]`     |               O(1) |
| `append()`     |     O(1) amortized |
| `pop()`        |      O(1) from end |
| `insert(0, x)` |               O(n) |
| `pop(0)`       |               O(n) |
| `x in list`    |               O(n) |

Yahan `O(n)` ka matlab roughly:

> data size barhe to operation ka work proportionally barhta hai.

---

# 3. List ka common problem

Suppose:

```python
queue = [1, 2, 3, 4, 5]
```

Agar:

```python
queue.pop(0)
```

karte ho, baqi elements ko shift karna pad sakta hai.

```text
[1, 2, 3, 4, 5]
 ↑ remove

[2, 3, 4, 5]
 ↑
elements shift
```

Agar tum repeatedly front se items remove kar rahe ho, `list` ideal structure nahi.

---

# 4. `deque`

Python mein:

```python
from collections import deque
```

`deque` = **double-ended queue**.

```python
queue = deque([1, 2, 3])
```

Tum dono ends se efficiently add/remove kar sakte ho:

```python
queue.append(4)
queue.appendleft(0)
```

Result:

```text
[0, 1, 2, 3, 4]
```

Remove:

```python
queue.pop()
```

last se.

Aur:

```python
queue.popleft()
```

first se.

---

# 5. `list` vs `deque`

### List

```python
items.append(x)
items.pop()
```

end operations ke liye excellent.

### Deque

```python
items.append(x)
items.appendleft(x)

items.pop()
items.popleft()
```

dono ends ke liye efficient.

Mental model:

```text
list
LEFT ←──────→ RIGHT
        efficient mostly at RIGHT

deque
LEFT ←──────→ RIGHT
  efficient    efficient
```

---

# 6. Queue example

Agar work orders queue mein aa rahe hain:

```python
from collections import deque

work_orders = deque()

work_orders.append("WO-1001")
work_orders.append("WO-1002")
work_orders.append("WO-1003")
```

Process first work order:

```python
wo = work_orders.popleft()
```

Result:

```text
WO-1001
```

Ye queue ke liye natural design hai:

```text
FIFO
First In → First Out
```

---

# 7. Stack

Stack ke liye `list` bohat useful hai.

```python
stack = []

stack.append("A")
stack.append("B")
stack.append("C")
```

Pop:

```python
stack.pop()
```

→ `"C"`

Ye:

```text
LIFO
Last In → First Out
```

hai.

So:

```text
Queue → deque
Stack → list
```

common choice hai.

---

# 8. `set`

Ab:

```python
numbers = {10, 20, 30}
```

`set` ka main purpose:

> unique values ka collection.

Duplicates automatically remove:

```python
numbers = {10, 20, 20, 30}
```

Conceptually:

```text
{10, 20, 30}
```

---

# 9. Set ka important feature

Membership checking:

```python
20 in numbers
```

Average case mein approximately:

```text
O(1)
```

hota hai.

Compare:

```python
20 in some_list
```

list mein typically:

```text
O(n)
```

---

# 10. Set kab use karo?

Agar question hai:

> "Kya ye value already exist karti hai?"

Set excellent choice hai.

Example:

```python
equipment_ids = {
    "AHU-01",
    "AHU-02",
    "VAV-01"
}
```

Check:

```python
if "AHU-01" in equipment_ids:
    print("Already exists")
```

---

# 11. Set indexing nahi karta

Ye nahi kar sakte:

```python
numbers[0]
```

❌

Kyun?

Set ka focus:

```text
unique membership
```

hai, positional ordering/indexing nahi.

---

# 12. Set operations

Set ki mathematical operations bohat useful hain.

```python
a = {1, 2, 3}
b = {3, 4, 5}
```

### Union

```python
a | b
```

→

```text
{1, 2, 3, 4, 5}
```

### Intersection

```python
a & b
```

→

```text
{3}
```

### Difference

```python
a - b
```

→

```text
{1, 2}
```

---

# 13. Symmetric difference

```python
a ^ b
```

→

```text
{1, 2, 4, 5}
```

Meaning:

> Jo dono mein common nahi hain.

---

# 14. `dict`

Dictionary:

```python
employee = {
    "name": "Ali",
    "salary": 5000,
    "department": "HVAC"
}
```

Main concept:

```text
key → value
```

Access:

```python
employee["name"]
```

→ `"Ali"`

---

# 15. Dictionary ka performance

Typical average-case:

| Operation | Typical |
| --------- | ------: |
| lookup    |    O(1) |
| insert    |    O(1) |
| update    |    O(1) |
| delete    |    O(1) |

Worst-case complexities more nuanced hain, lekin practical usage mein hash-table behavior ki wajah se dictionary lookup generally very fast hota hai.

---

# 16. `dict` vs `set`

Actually conceptually dono hash-based structures hain.

Dictionary:

```text
key → value
```

Set:

```text
value
```

Example:

```python
employee = {
    "E001": "Ali",
    "E002": "Ahmed"
}
```

Set:

```python
employees = {
    "E001",
    "E002"
}
```

Mental model:

```text
dict = lookup table

set = membership table
```

---

# 17. `defaultdict`

Ab `collections` ka useful tool:

```python
from collections import defaultdict
```

Normal dictionary mein:

```python
data = {}

data["HVAC"].append("AHU-01")
```

❌ Error, kyunki `"HVAC"` key abhi exist nahi karti.

---

# 18. `defaultdict(list)`

```python
from collections import defaultdict

data = defaultdict(list)

data["HVAC"].append("AHU-01")
data["HVAC"].append("AHU-02")
data["Electrical"].append("DB-01")
```

Result conceptually:

```python
{
    "HVAC": ["AHU-01", "AHU-02"],
    "Electrical": ["DB-01"]
}
```

`defaultdict` automatically missing key ke liye default value create kar deta hai.

---

# 19. Work-order grouping example

Tumhare work-order data ke liye:

```python
from collections import defaultdict

work_orders_by_floor = defaultdict(list)

work_orders_by_floor["Floor 34"].append("WO-1001")
work_orders_by_floor["Floor 34"].append("WO-1002")
work_orders_by_floor["Floor 41"].append("WO-1003")
```

Ab:

```python
work_orders_by_floor["Floor 34"]
```

→

```text
["WO-1001", "WO-1002"]
```

Ye grouping ke liye bohat useful hai.

---

# 20. `defaultdict(int)`

Counting ke liye:

```python
from collections import defaultdict

count = defaultdict(int)

count["AHU"] += 1
count["AHU"] += 1
count["VAV"] += 1
```

Result:

```python
{
    "AHU": 2,
    "VAV": 1
}
```

Kyun?

```python
int()
```

default:

```text
0
```

return karta hai.

---

# 21. `Counter`

Counting ke liye Python mein direct tool bhi hai:

```python
from collections import Counter
```

Example:

```python
equipment = [
    "AHU",
    "VAV",
    "AHU",
    "FCU",
    "AHU",
    "VAV"
]

counter = Counter(equipment)
```

Result conceptually:

```text
AHU → 3
VAV → 2
FCU → 1
```

---

# 22. Most common

```python
counter.most_common(2)
```

returns top 2 frequent items.

Example:

```text
[
    ("AHU", 3),
    ("VAV", 2)
]
```

Data analysis mein ye useful hai.

---

# 23. `Counter` vs `defaultdict(int)`

Dono counting kar sakte hain.

### `defaultdict(int)`

General-purpose dictionary with default integer.

### `Counter`

Specifically frequency counting ke liye designed.

Mental model:

```text
defaultdict(int)
→ generic counting/grouping tool

Counter
→ dedicated frequency counter
```

---

# 24. `OrderedDict`

```python
from collections import OrderedDict
```

Historical context:

Older Python versions mein normal `dict` insertion ordering guarantee nahi karta tha.

Modern Python mein:

> normal `dict` insertion order preserve karta hai.

Isliye normal applications mein `OrderedDict` ki zaroorat pehle se kam hai.

Lekin `OrderedDict` ke kuch specialized behavior/methods ab bhi useful hain, jaise:

```python
move_to_end()
```

---

# 25. `namedtuple`

`collections` mein:

```python
from collections import namedtuple
```

Example:

```python
Point = namedtuple("Point", ["x", "y"])

p = Point(10, 20)
```

Access:

```python
p.x
p.y
```

Ye lightweight tuple-like structure hai.

Lekin modern Python mein data-focused objects ke liye `dataclass` aksar zyada flexible choice hoti hai.

---

# 26. `list` vs `deque` vs `set` vs `dict`

Ye table save kar lo:

| Structure     | Main purpose                       |
| ------------- | ---------------------------------- |
| `list`        | ordered collection                 |
| `deque`       | fast operations at both ends       |
| `set`         | unique values / membership         |
| `dict`        | key → value lookup                 |
| `defaultdict` | dictionary with automatic defaults |
| `Counter`     | frequency counting                 |

---

# 27. Decision tree

Agar tumhara question hai:

### "Mujhe ordered items chahiye"

```text
list
```

### "Mujhe dono ends se queue operations chahiye"

```text
deque
```

### "Mujhe unique values chahiye"

```text
set
```

### "Mujhe key se value find karni hai"

```text
dict
```

### "Mujhe missing keys automatically initialize karni hain"

```text
defaultdict
```

### "Mujhe frequency count karni hai"

```text
Counter
```

---

# 28. Performance mental model

```text
list
↓
index access → fast
front insertion/removal → expensive

deque
↓
front + back → fast
random indexing → not its main strength

set
↓
membership → fast average

dict
↓
key lookup → fast average
```

---

# 29. Tumhare work-order project mein

Suppose:

```text
100,000 work orders
```

### Sequential processing

```python
for row in rows:
    ...
```

`Iterable` enough ho sakta hai.

### Work-order lookup

```python
work_orders_by_id["WO-12345"]
```

`dict`.

### Already processed IDs

```python
processed_ids = set()
```

### Queue

```python
pending = deque()
```

### Group by floor

```python
by_floor = defaultdict(list)
```

### Count equipment types

```python
Counter(equipment_types)
```

Ye ek real architecture ban sakta hai:

```text
                 Work Orders
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
       dict          set          deque
      lookup       uniqueness      queue
        │
        ↓
 defaultdict
    grouping
        │
        ↓
    Counter
    counting
```

---

# 30. `list` ko har jagah use karna zaroori nahi

Beginners commonly:

```python
everything = []
```

se start karte hain.

Lekin data structure selection actually problem ke operation par depend karta hai.

Question ye hona chahiye:

> **Mujhe data ke saath kya operation frequently karna hai?**

Not:

> "Data hai, to list bana deta hoon."

---

# 31. Example decision

Suppose:

```python
equipment_ids = ["AHU-01", "AHU-02", "AHU-01"]
```

Agar goal hai duplicates remove karna:

```python
unique_ids = set(equipment_ids)
```

Agar original order important hai aur duplicates remove karne hain, simple `set()` alone se order semantics ko blindly rely nahi karna chahiye; modern Python mein ek common approach:

```python
unique_ids = list(dict.fromkeys(equipment_ids))
```

Result:

```text
["AHU-01", "AHU-02"]
```

Yahan `dict` ki insertion-order property ka use ho raha hai.

---

# 32. One big picture

Ab previous lessons ko connect karo:

```text
collections.abc
       ↓
"What capability does this object provide?"
       ↓
Iterable
Sequence
Mapping
Callable
       ↓
collections
       ↓
"What concrete structure should I use?"
       ↓
list
deque
set
dict
Counter
defaultdict
```

Ye distinction professional Python code mein bohat important hai.

---

## Quick revision

```text
list
→ ordered + mutable + index

deque
→ double-ended queue

set
→ unique + membership

dict
→ key → value

defaultdict
→ dict + automatic default

Counter
→ frequency counting
```

### Next Lesson 46

Ab hum **Hashing + `__hash__()` + `__eq__()`** deeply samjhenge.

Ye directly explain karega:

```python
x in set
data[key]
```

itna fast **kyun** hota hai, aur ye bhi:

> **Kyun mutable objects ko normally dictionary key ya set member nahi banana chahiye?**

# Lesson 46: Hashing + `__hash__()` + `__eq__()`

Ab hum samjhenge ke Python mein:

```python
x in set
```

aur:

```python
data[key]
```

itna fast **kyun** hota hai.

Is lesson ka central concept hai:

> **Hash table**

Aur isi ke through `set` aur `dict` ka internal behavior samajh aayega.

---

# 1. Hash kya hota hai?

Hash ek integer-like value hoti hai jo kisi object se calculate ki ja sakti hai.

Python mein:

```python
hash("AHU-01")
```

Example output:

```text
-123456789
```

Exact number Python run ke context/version/process ke hisaab se different ho sakta hai.

Important ye number nahi hai.

Important concept:

```text
object
   ↓
hash()
   ↓
integer
```

---

# 2. `hash()` function

Python:

```python
hash(100)
```

```python
hash("hello")
```

```python
hash((1, 2))
```

kuch hash value return kar sakte hain.

Lekin:

```python
hash([1, 2])
```

❌ error:

```text
TypeError: unhashable type: 'list'
```

Iska reason baad mein clear hoga.

---

# 3. Hashable kya hota hai?

Simple definition:

> **Hashable object wo hota hai jiska hash stable reh sakta hai aur jise set member ya dictionary key ke taur par use kiya ja sakta hai.**

Examples:

```python
10
"AHU-01"
(1, 2)
frozenset({1, 2})
```

Usually hashable.

---

# 4. Unhashable objects

Common examples:

```python
list
dict
set
```

Example:

```python
hash([1, 2, 3])
```

❌

```text
TypeError: unhashable type: 'list'
```

Similarly:

```python
hash({"a": 1})
```

❌

---

# 5. Hashing ka use kahan hota hai?

Primarily:

```text
dict
set
```

Example:

```python
equipment = {
    "AHU-01": "Running",
    "AHU-02": "Stopped"
}
```

Yahan:

```python
equipment["AHU-01"]
```

key `"AHU-01"` ke hash ko use karke lookup efficiently perform kiya jata hai.

---

# 6. Simple hash-table mental model

Actual implementation Python ke version/implementation par depend karti hai, lekin learning ke liye:

```text
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

Isliye dictionary ko roughly:

```text
key → hash → location → value
```

samajh sakte ho.

---

# 7. Set bhi similar idea use karta hai

Set:

```python
equipment_ids = {
    "AHU-01",
    "AHU-02",
    "VAV-01"
}
```

Check:

```python
"AHU-02" in equipment_ids
```

Conceptually:

```text
"AHU-02"
    ↓
hash
    ↓
candidate location
    ↓
check equality if necessary
```

Isi wajah se average-case membership fast hoti hai.

---

# 8. Hash alone enough nahi hota

Ye bohat important hai.

Suppose do different objects ka same hash aa gaya:

```text
object A → hash 100
object B → hash 100
```

Isko:

> **hash collision**

kehte hain.

Python ko phir actual equality check bhi karni pad sakti hai.

Yahan:

```python
__eq__()
```

important ho jata hai.

---

# 9. `__eq__()`

Tumne dunder methods mein pehle dekha:

```python
def __eq__(self, other):
    ...
```

Ye:

```python
==
```

operator ko control karta hai.

Example:

```python
class Employee:

    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __eq__(self, other):
        return self.employee_id == other.employee_id
```

Now:

```python
e1 = Employee("E001")
e2 = Employee("E001")
```

Then:

```python
e1 == e2
```

→ `True`

---

# 10. `__hash__()` kya karta hai?

Object ke liye hash define karta hai:

```python
class Employee:

    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __hash__(self):
        return hash(self.employee_id)
```

Ab object potentially hashable ho sakta hai.

Example:

```python
e1 = Employee("E001")

print(hash(e1))
```

---

# 11. `__eq__` + `__hash__` ka relationship

Ye golden rule yaad rakho:

> Agar `a == b` hai, to ideally `hash(a) == hash(b)` bhi hona chahiye.

Example:

```text
e1.employee_id = "E001"
e2.employee_id = "E001"
```

Agar:

```python
e1 == e2
```

True hai,

to:

```python
hash(e1) == hash(e2)
```

bhi hona chahiye.

---

# 12. Lekin reverse zaroori nahi

Agar:

```python
hash(a) == hash(b)
```

to iska matlab ye nahi ke:

```python
a == b
```

must be True.

Kyun?

Because hash collisions possible hain.

So:

```text
equal objects
→ same hash required

same hash
→ equal hona required nahi
```

---

# 13. Real example

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
```

Now:

```python
e1 = Employee("E001")
e2 = Employee("E001")
e3 = Employee("E002")
```

Then:

```python
e1 == e2
```

→ `True`

and:

```python
hash(e1) == hash(e2)
```

→ `True`

---

# 14. Set mein iska effect

```python
employees = {e1, e2, e3}
```

Since:

```text
e1 == e2
```

and same hash:

```text
e1
e2
```

logical perspective se duplicate hain.

Set mein unique identity/equality semantics ke according ek hi logical entry remain karegi.

Conceptually:

```text
E001
E001  ← duplicate
E002
```

→

```text
E001
E002
```

---

# 15. Dictionary key mein bhi same principle

```python
data = {
    e1: "Manager"
}
```

Then:

```python
data[e2]
```

Agar:

```python
e1 == e2
```

aur hashes compatible hain,

to `e2` corresponding dictionary entry ko locate kar sakta hai.

---

# 16. Mutable object ka problem

Ab important problem.

Suppose:

```python
class Employee:

    def __init__(self, employee_id):
        self.employee_id = employee_id

    def __hash__(self):
        return hash(self.employee_id)

    def __eq__(self, other):
        return self.employee_id == other.employee_id
```

Create:

```python
e = Employee("E001")
```

Set:

```python
employees = {e}
```

Ab:

```python
e.employee_id = "E999"
```

Problem!

Pehle object ka hash based tha:

```text
"E001"
```

Ab hash based hai:

```text
"E999"
```

Object set mein purani hash-based position ke context mein inserted tha.

Ab lookup behavior broken/unpredictable ho sakta hai.

---

# 17. Isi liye mutable hash keys dangerous hain

Agar object's hash/equality state change ho sakti hai while it is inside a set/dict:

```text
insert
 ↓
hash based on state A
 ↓
state changes
 ↓
hash based on state B
 ↓
lookup inconsistency
```

Isliye:

> Dictionary keys aur set members ko aisi state par base nahi karna chahiye jo membership ke dauran mutate ho sakti ho.

---

# 18. `tuple` kyun hashable ho sakta hai?

Example:

```python
point = (10, 20)
hash(point)
```

possible hai.

Lekin tuple ke andar elements bhi appropriately hashable hone chahiye.

Example:

```python
hash((1, 2, 3))
```

works.

Lekin:

```python
hash(([1, 2], 3))
```

❌

Kyun?

Tuple immutable hai, lekin uske andar list mutable/unhashable hai.

---

# 19. Immutable ka relation

Common mental model:

```text
immutable
↓
state change nahi hoti
↓
hash stable reh sakta hai
↓
hashable hone ka chance
```

Lekin:

> **Immutable automatically hashable ka universal synonym nahi hai.**

Hashability ka actual rule object ke hash/equality implementation se related hai.

---

# 20. `str` hashable

```python
hash("AHU-01")
```

works.

String immutable hai.

Isliye dictionary key:

```python
equipment = {
    "AHU-01": "ON"
}
```

natural hai.

---

# 21. `int` hashable

```python
hash(100)
```

works.

So:

```python
data = {
    100: "AHU"
}
```

valid hai.

---

# 22. `list` unhashable

```python
items = [1, 2, 3]
```

List mutable hai.

Agar list ko hash-based structure mein key bana diya jaye aur baad mein contents change ho jayein, hash consistency ka issue aa sakta hai.

Isliye:

```python
data = {
    [1, 2, 3]: "test"
}
```

❌

---

# 23. `frozenset`

Normal:

```python
set
```

mutable hai.

Isliye:

```python
hash({1, 2})
```

❌

Lekin:

```python
fs = frozenset({1, 2})
hash(fs)
```

possible hai.

`frozenset` immutable set-like structure hai.

---

# 24. Custom class ka default behavior

Agar tum simple class likho:

```python
class Employee:
    pass
```

then:

```python
e1 = Employee()
e2 = Employee()
```

Normally:

```python
e1 == e2
```

False hoga, kyunki default object identity semantics use hoti hain.

Aur such objects normally hashable bhi hote hain based on their identity semantics.

Conceptually:

```text
e1
≠
e2
```

even if both same class ke hain.

---

# 25. Jab `__eq__` override karte ho

Ye important Python behavior hai.

Agar tum:

```python
class Employee:

    def __eq__(self, other):
        return self.employee_id == other.employee_id
```

define karte ho, to Python hashing ke rules change kar sakta hai.

Aise case mein class automatically unhashable ho sakti hai unless compatible `__hash__` explicitly provide kiya jaye.

Example:

```python
e = Employee("E001")

hash(e)
```

potentially:

```text
TypeError: unhashable type
```

Agar `__hash__` provide nahi kiya.

---

# 26. Ye kyun?

Python ka safety principle roughly:

```text
Custom equality
+
mutable/uncertain equality state
=
hash-based collection mein dangerous
```

Isliye Python blindly hashability allow nahi karta.

---

# 27. `dataclass` ke saath connection

Previous lesson mein tumne dataclass padha.

Example:

```python
from dataclasses import dataclass

@dataclass
class Employee:
    employee_id: str
    salary: float
```

Dataclass automatically:

```text
__init__
__repr__
__eq__
```

generate kar sakta hai.

Lekin hash behavior configuration par depend karta hai.

Yahan `frozen=True` important ho sakta hai.

---

# 28. Frozen dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Employee:
    employee_id: str
    salary: float
```

Ab:

```python
e = Employee("E001", 5000)
```

fields ko normally modify nahi kar sakte:

```python
e.salary = 6000
```

❌

Frozen dataclasses hash-based use cases ke liye suitable ho sakti hain when their fields are themselves appropriately hashable.

---

# 29. Hash + equality mental model

Isko diagram se yaad rakho:

```text
             Object
                │
        ┌───────┴────────┐
        ↓                ↓
    __eq__()          __hash__()
        │                │
        ↓                ↓
  "same hai?"       "hash kya hai?"
        │                │
        └───────┬────────┘
                ↓
          set / dict
```

---

# 30. Dictionary lookup simplified

Suppose:

```python
data = {
    "AHU-01": "Running"
}
```

Aur:

```python
data["AHU-01"]
```

Conceptually:

```text
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

Ye exact internal implementation diagram nahi, balki conceptual model hai.

---

# 31. Set membership simplified

```python
ids = {"AHU-01", "VAV-01"}
```

Then:

```python
"AHU-01" in ids
```

Conceptually:

```text
"AHU-01"
    ↓
hash
    ↓
candidate location
    ↓
equality check if needed
    ↓
True
```

---

# 32. `O(1)` ka matlab kya hai?

Tumne previous lesson mein suna:

```text
dict lookup → average O(1)
set membership → average O(1)
```

Iska matlab:

> Data 100 se 1000 ya 100000 items tak grow karne par lookup ka average work linear scan ki tarah proportionally nahi barhta.

Compare list:

```python
"AHU-999" in huge_list
```

Potentially:

```text
AHU-001
AHU-002
AHU-003
...
AHU-999
```

ko sequentially check karna pad sakta hai.

So:

```text
list membership → O(n)

set/dict lookup → average O(1)
```

---

# 33. Lekin `O(1)` magic nahi hai

Hash table mein collisions ho sakti hain.

Isliye theoretical/worst-case behavior more complicated hai.

Professional rule:

> `dict` aur `set` ke liye **average-case O(1)** ya expected constant-time lookup kehna accurate hai.

---

# 34. Tumhare work-order project mein

Suppose 500,000 work orders hain.

Agar tum:

```python
work_orders = [
    ...
]
```

mein repeatedly search karte ho:

```python
find_work_order("WO-500000")
```

to list scan expensive ho sakta hai.

Better:

```python
work_orders_by_id = {
    "WO-1001": {...},
    "WO-1002": {...},
    ...
}
```

Then:

```python
work_orders_by_id["WO-500000"]
```

fast average lookup provide karta hai.

---

# 35. Equipment IDs ke liye `set`

Suppose tum check karna chahte ho:

```text
"MEP-KHN-REF04"
```

already process hua hai ya nahi.

Use:

```python
processed_ids = set()
```

Then:

```python
if equipment_id in processed_ids:
    ...
```

Membership check ke liye set natural hai.

---

# 36. `__eq__` aur `__hash__` ka golden rule

### Rule 1

Agar:

```python
a == b
```

True hai, then:

```python
hash(a) == hash(b)
```

hona chahiye.

### Rule 2

Agar object hash-based collection mein hai:

```text
set
dict key
```

to uski hash-relevant equality state ko mutate nahi karna chahiye.

### Rule 3

Same hash ka matlab necessarily equality nahi:

```text
same hash
≠
same object/equal object
```

because collisions possible hain.

---

# 37. `is` vs `==`

Ye bhi yahan important hai.

```python
a is b
```

means:

> Kya dono exact same object hain?

```python
a == b
```

means:

> Kya dono logically equal hain?

Example:

```python
a = [1, 2]
b = [1, 2]
```

Then:

```python
a == b
```

→ `True`

but:

```python
a is b
```

→ `False`

Hash/equality concepts mein `==` important hai; object identity `is` alag concept hai.

---

# 38. Final architecture

Ab `set`/`dict` ko deeper level par samjho:

```text
             set / dict
                 │
                 ↓
              hashing
                 │
          ┌──────┴──────┐
          ↓             ↓
      __hash__       __eq__
          │             │
          ↓             ↓
     candidate       equality
      location         check
```

Aur:

```text
mutable hash-relevant state
          ↓
      dangerous
          ↓
set/dict lookup inconsistency
```

---

## Quick revision

```text
hash()
→ object ka hash value

__eq__()
→ equality define karta hai

__hash__()
→ hash define karta hai

set
→ hash + equality

dict
→ hash + equality

hashable
→ set member / dict key ban sakta hai

unhashable
→ list, dict, set jaise mutable built-ins
```

### Sabse important line:

> **`dict` aur `set` fast hone ka core idea hash table hai; `__hash__()` candidate location find karne mein aur `__eq__()` actual equality verify karne mein role play karta hai.**

### Next Lesson 47

Ab hum **`copy` vs `deepcopy` + shallow copy + references + mutable/immutable objects** samjhenge.

Ye especially important hai kyunki tumne `list`, `dict`, dataclass aur mutable data structures padhe hain. Ismein ye clear hoga ke:

```python
b = a
b = a.copy()
b = copy.deepcopy(a)
```

teenon mein actual difference kya hai.

# Lesson 47: `copy` vs `deepcopy` + References

Ab hum ek bohat important Python concept samjhenge:

```python
b = a
```

vs

```python
b = a.copy()
```

vs

```python
b = copy.deepcopy(a)
```

In teenon ko samajhna zaroori hai, especially jab `list`, `dict`, dataclass aur nested data structures use karte ho.

---

# 1. Sabse pehle: Python variable kya store karta hai?

Python variable ko simple tareeqe se:

> **object ka reference/name binding**

samjho.

Example:

```python
a = [10, 20, 30]
```

Conceptually:

```text
a ───────→ [10, 20, 30]
```

`a` khud list nahi hai.

`a` ek name hai jo list object ko refer kar raha hai.

---

# 2. `b = a`

Ab:

```python
a = [10, 20, 30]

b = a
```

Kya new list bani?

**Nahi.**

Diagram:

```text
        ┌──────────────┐
a ─────→│              │
        │ [10, 20, 30] │
b ─────→│              │
        └──────────────┘
```

Dono names **same object** ko refer kar rahe hain.

---

# 3. Proof: `is`

```python
a = [10, 20, 30]
b = a

print(a is b)
```

Output:

```text
True
```

`is` check karta hai:

> Kya dono exact same object hain?

---

# 4. Ab mutation dekho

```python
a = [10, 20, 30]
b = a

a.append(40)
```

Ab:

```python
print(b)
```

Output:

```text
[10, 20, 30, 40]
```

Kyun?

Because:

```text
a ─────┐
       ↓
   SAME LIST
       ↑
b ─────┘
```

`a` ne same object modify kiya.

---

# 5. `b = a` ko copy mat samjho

Ye:

```python
b = a
```

**copy nahi hai**.

Ye:

```text
same object
+
second reference/name
```

hai.

---

# 6. `copy()`

Ab:

```python
a = [10, 20, 30]

b = a.copy()
```

Ab new list banegi:

```text
a ─────→ [10, 20, 30]

b ─────→ [10, 20, 30]
```

Do separate list objects.

---

# 7. `is` check

```python
print(a is b)
```

Output:

```text
False
```

Lekin:

```python
print(a == b)
```

Output:

```text
True
```

Because:

```text
is → same object?
== → same value?
```

---

# 8. Mutation ab independent hai

```python
a = [10, 20, 30]
b = a.copy()

a.append(40)
```

Now:

```python
print(a)
```

→

```text
[10, 20, 30, 40]
```

But:

```python
print(b)
```

→

```text
[10, 20, 30]
```

---

# 9. Shallow copy

`copy()` generally **shallow copy** banata hai.

Example:

```python
import copy

a = [1, 2, 3]

b = copy.copy(a)
```

For a simple flat list:

```text
a → [1, 2, 3]

b → [1, 2, 3]
```

Fine.

Lekin nested structure mein difference aata hai.

---

# 10. Nested list

```python
a = [
    [1, 2],
    [3, 4]
]
```

Agar:

```python
b = a.copy()
```

to structure conceptually:

```text
a ─────→ outer list
           │
           ├──→ [1, 2]
           │
           └──→ [3, 4]

b ─────→ new outer list
           │
           ├──→ [1, 2]  ← SAME inner object
           │
           └──→ [3, 4]  ← SAME inner object
```

Yahan important point:

> Outer list copy hui, inner lists copy nahi hui.

---

# 11. Proof

```python
a = [
    [1, 2],
    [3, 4]
]

b = a.copy()

print(a is b)
```

→

```text
False
```

Lekin:

```python
print(a[0] is b[0])
```

→

```text
True
```

Outer objects different hain.

Inner object same hai.

---

# 12. Problem

Ab:

```python
a[0].append(99)
```

Then:

```python
print(a)
```

→

```text
[[1, 2, 99], [3, 4]]
```

Aur:

```python
print(b)
```

bhi:

```text
[[1, 2, 99], [3, 4]]
```

Kyun?

Inner list shared thi.

---

# 13. `deepcopy`

Nested objects ko independently copy karna ho to:

```python
import copy

b = copy.deepcopy(a)
```

Conceptually:

```text
a
│
└── outer list
     ├── inner list A
     └── inner list B


b
│
└── NEW outer list
     ├── NEW inner list A
     └── NEW inner list B
```

Nested mutable objects bhi copy ho jate hain.

---

# 14. Example

```python
import copy

a = [
    [1, 2],
    [3, 4]
]

b = copy.deepcopy(a)

a[0].append(99)
```

Now:

```python
print(a)
```

→

```text
[[1, 2, 99], [3, 4]]
```

But:

```python
print(b)
```

→

```text
[[1, 2], [3, 4]]
```

---

# 15. Three concepts side-by-side

Suppose:

```python
a = [[1, 2], [3, 4]]
```

### Case 1

```python
b = a
```

```text
outer same
inner same
```

### Case 2

```python
b = a.copy()
```

```text
outer different
inner same
```

### Case 3

```python
b = copy.deepcopy(a)
```

```text
outer different
inner different
```

---

# 16. Diagram

```text
Original:
a
↓
[ [1,2], [3,4] ]


b = a

a ──┐
    ├──→ [ [1,2], [3,4] ]
b ──┘


b = a.copy()

a ─────→ [ [1,2], [3,4] ]
             ↑     ↑
b ─────→ [ same inner objects ]


b = deepcopy(a)

a ─────→ [ [1,2], [3,4] ]

b ─────→ [ [1,2], [3,4] ]
          ↑       ↑
       new objects
```

---

# 17. `copy.copy()` vs `.copy()`

Ye bhi useful distinction hai.

For many built-in containers:

```python
a.copy()
```

and:

```python
copy.copy(a)
```

shallow copy produce karte hain.

Example:

```python
import copy

b = copy.copy(a)
```

versus:

```python
b = a.copy()
```

Lekin `.copy()` har arbitrary object ke liye available nahi hota.

`copy.copy()` generic copying mechanism provide karta hai.

---

# 18. Dictionary

Dictionary mein:

```python
data = {
    "name": "Ali",
    "salary": 5000
}
```

Shallow copy:

```python
new_data = data.copy()
```

Ab:

```text
data     → dictionary A
new_data → dictionary B
```

Do separate dictionaries.

---

# 19. Nested dictionary

```python
data = {
    "employee": {
        "name": "Ali",
        "salary": 5000
    }
}
```

Now:

```python
new_data = data.copy()
```

Outer dictionary new hai.

Lekin:

```python
data["employee"] is new_data["employee"]
```

→ `True`

because nested dictionary shared hai.

---

# 20. Deepcopy

```python
new_data = copy.deepcopy(data)
```

Ab nested employee dictionary bhi independent hai.

```python
data["employee"] is new_data["employee"]
```

→ `False`

---

# 21. Work-order example

Suppose:

```python
work_order = {
    "number": "WO-1001",
    "equipment": {
        "id": "AHU-01",
        "status": "OFF"
    }
}
```

Tum template copy karna chahte ho:

```python
new_order = work_order.copy()
```

Phir:

```python
new_order["equipment"]["status"] = "ON"
```

Problem:

```python
work_order["equipment"]["status"]
```

bhi:

```text
ON
```

ho sakta hai.

Kyun?

Nested dictionary shared thi.

---

# 22. Agar completely independent copy chahiye

```python
new_order = copy.deepcopy(work_order)
```

Ab:

```python
new_order["equipment"]["status"] = "ON"
```

original:

```python
work_order["equipment"]["status"]
```

unchanged rahega.

---

# 23. Deepcopy har waqt use nahi karna

Ye important hai.

Beginner kabhi kabhi:

```python
copy.deepcopy(...)
```

har jagah use karna start kar deta hai.

Ye necessarily good nahi.

Deepcopy:

* extra memory use kar sakta hai
* CPU time le sakta hai
* complex object graphs mein expensive ho sakta hai
* kuch objects ko straightforwardly copy nahi kar sakta

Isliye pehle decide karo:

> Mujhe actual mein kitni independence chahiye?

---

# 24. Immutable objects

Immutable objects ko modify nahi kar sakte.

Examples:

```text
int
float
str
tuple
frozenset
```

Example:

```python
x = 10
```

Tum `10` object ko modify nahi kar rahe.

Agar:

```python
x = 20
```

likhte ho, name `x` ko doosre object se bind kar dete ho.

---

# 25. Assignment vs mutation

Ye distinction bohat important hai.

### Assignment

```python
x = 10
x = 20
```

Name ko rebind kar rahe ho.

### Mutation

```python
items = [1, 2]
items.append(3)
```

Existing list object modify kar rahe ho.

---

# 26. Mutable vs immutable

```text
Mutable
↓
existing object change ho sakta hai

Immutable
↓
existing object change nahi hota
```

Examples:

```text
list       → mutable
dict       → mutable
set        → mutable

str        → immutable
int        → immutable
tuple      → immutable
frozenset  → immutable
```

---

# 27. Tuple ka subtle point

Tuple immutable hai:

```python
t = (1, 2, 3)
```

Lekin tuple ke andar mutable object ho sakta hai:

```python
t = ([1, 2], [3, 4])
```

Tum:

```python
t[0] = [100, 200]
```

❌ nahi kar sakte.

Lekin:

```python
t[0].append(99)
```

possible hai.

Result:

```text
([1, 2, 99], [3, 4])
```

Kyun?

Tuple ka structure immutable hai, lekin inner list mutable hai.

---

# 28. Shallow copy ka real mental model

Shallow copy:

> **Container ko copy karo, references ko necessarily recursively copy mat karo.**

Example:

```text
outer container
      ↓
   COPY
      ↓
inner objects
      ↓
  shared references
```

---

# 29. Deep copy ka mental model

Deepcopy:

> **Nested object graph ko recursively copy karne ki koshish karta hai.**

```text
outer
 ↓
copy
 ↓
inner
 ↓
copy
 ↓
deeper
 ↓
copy
```

`deepcopy` internally memoization bhi use karta hai taa-ke repeated references aur cyclic structures ko handle kar sake.

---

# 30. Circular reference

Python mein object apne aap ko indirectly reference kar sakta hai:

```python
a = []
a.append(a)
```

Ab:

```text
a
↓
[ reference to a ]
```

Agar naive copying approach hoti to infinite recursion ho sakti thi.

`copy.deepcopy()` internally already-copied objects ka memo maintain karta hai, isliye cycles ko handle kar sakta hai in supported cases.

---

# 31. Dataclass ke saath

Previous lesson:

```python
from dataclasses import dataclass, field

@dataclass
class Equipment:
    equipment_id: str
    tags: list[str] = field(default_factory=list)
```

Suppose:

```python
ahu1 = Equipment("AHU-01", ["HVAC"])
```

Agar:

```python
ahu2 = copy.copy(ahu1)
```

to `tags` list shallow copy ki wajah se shared ho sakti hai.

```python
ahu2.tags.append("BMS")
```

Original `ahu1.tags` bhi affect ho sakti hai.

---

# 32. Deepcopy dataclass

```python
ahu2 = copy.deepcopy(ahu1)
```

Ab:

```python
ahu2.tags.append("BMS")
```

normally original object's tags ko affect nahi karega.

---

# 33. Copy protocol

Python objects copying customize bhi kar sakte hain.

Relevant special methods:

```python
__copy__()
__deepcopy__()
```

Example conceptually:

```python
class Equipment:

    def __copy__(self):
        ...

    def __deepcopy__(self, memo):
        ...
```

Ye advanced custom object behavior ke liye useful hai.

---

# 34. `copy.copy()` internally kya karta hai?

High-level mental model:

```text
copy.copy(obj)
       ↓
Python copy protocol
       ↓
__copy__() if supported
       ↓
shallow copy
```

Similarly:

```text
copy.deepcopy(obj)
       ↓
deep-copy machinery
       ↓
__deepcopy__()
       ↓
recursive copying
```

---

# 35. `copy` aur `=` ka biggest difference

```python
b = a
```

means:

```text
NO COPY
```

while:

```python
b = copy.copy(a)
```

means:

```text
SHALLOW COPY
```

and:

```python
b = copy.deepcopy(a)
```

means:

```text
DEEP COPY
```

---

# 36. One practical example

```python
import copy

equipment = {
    "id": "AHU-01",
    "points": {
        "temperature": 22.5,
        "damper": 50
    }
}
```

### Assignment

```python
a = equipment
```

```text
same object
```

### Shallow copy

```python
b = equipment.copy()
```

```text
new outer dict
same inner points dict
```

### Deep copy

```python
c = copy.deepcopy(equipment)
```

```text
new outer dict
new inner points dict
```

---

# 37. Quick test

Given:

```python
a = {
    "x": [1, 2]
}

b = a
c = a.copy()
d = copy.deepcopy(a)
```

Then:

```python
a is b
```

→ `True`

```python
a is c
```

→ `False`

```python
a["x"] is c["x"]
```

→ `True`

```python
a["x"] is d["x"]
```

→ `False`

Ye 4 lines **shallow vs deep copy ka core** samjha deti hain.

---

# 38. Work-order data mein practical rule

Agar tum:

```python
rows
```

ko sirf read/process kar rahe ho:

```python
for row in rows:
    ...
```

copy ki zaroorat hi nahi.

Agar independent outer list chahiye:

```python
new_rows = rows.copy()
```

Agar nested dictionaries/lists bhi independent chahiye:

```python
new_rows = copy.deepcopy(rows)
```

Lekin large datasets mein blindly `deepcopy()` avoid karo.

---

# 39. Final mental model

```text
a = b
↓
same object

copy.copy()
↓
shallow copy
↓
outer object new
↓
nested references may remain shared

copy.deepcopy()
↓
recursive copy
↓
nested mutable objects independent
```

### One-line rule:

> **`=` reference/binding deta hai, `.copy()` usually shallow copy deta hai, aur `deepcopy()` nested object graph ko recursively independent copy karta hai.**

---

## Next Lesson 48

Ab hum **Python memory model + garbage collection + reference counting + `weakref`** dekhenge:

```text
object
reference
reference count
GC
cyclic reference
weak reference
__del__
```

Aur ye samjhenge ke Python mein object **actually memory se kab remove hota hai**, aur:

> `del x` karne se object immediately delete hota hai ya nahi?

# Lesson 48: Python Memory Management + Reference Counting + Garbage Collection

Ab hum samjhenge ke Python mein object memory mein kaise rehta hai aur **kab remove hota hai**.

Core concepts:

```text
Object
  ↓
Reference
  ↓
Reference Count
  ↓
Garbage Collection
  ↓
Memory Cleanup
```

---

# 1. Object memory mein hota hai

Example:

```python
x = [10, 20, 30]
```

Conceptually:

```text
x ─────→ [10, 20, 30]
          object
```

`x` object nahi hai; `x` object ka reference/name binding hai.

---

# 2. Multiple references

```python
x = [10, 20, 30]

y = x
z = x
```

Ab:

```text
       ┌──────────────┐
x ────→│              │
y ────→│ [10,20,30]   │
z ────→│              │
       └──────────────┘
```

Ek hi list object hai.

Us object ko multiple references point kar rahe hain.

---

# 3. Reference count

CPython mein objects ke liye reference counting important memory-management mechanism hai.

Conceptually:

```text
x ──→ object
y ──→ object
z ──→ object

reference count ≈ 3
```

Check karne ke liye:

```python
import sys

x = [10, 20, 30]

print(sys.getrefcount(x))
```

Output exact number ko directly object ke logical references mat samjho, kyunki `getrefcount()` khud temporary reference create karta hai.

---

# 4. Reference remove karo

```python
x = [10, 20, 30]

y = x
z = x

del y
```

Ab:

```text
x ───→ object
z ───→ object
```

Ek reference kam ho gaya.

---

# 5. `del x` kya karta hai?

Ye bohat important hai.

```python
x = [10, 20, 30]

del x
```

`del x` ka matlab directly:

> "Memory mein object ko destroy karo"

**zaroori nahi.**

Actually:

> `del x` name/reference binding ko remove karta hai.

Agar koi aur reference hai:

```python
x = [10, 20, 30]
y = x

del x
```

to object abhi bhi exist karta hai:

```text
       ┌──────────────┐
       │ [10,20,30]   │
       └──────────────┘
              ↑
              y
```

---

# 6. Jab last reference bhi remove ho

```python
x = [10, 20, 30]
y = x

del x
del y
```

Ab normal reference-counting perspective mein object ka koi Python-level reference nahi bacha.

```text
No reference
     ↓
object unreachable
```

CPython mein reference count zero hone par object ki deallocation generally promptly hoti hai.

Lekin Python language level par exact memory reclamation timing ko CPython-specific behavior samajhna chahiye.

---

# 7. Garbage Collector kya karta hai?

Python mein ek **cyclic garbage collector** bhi hai.

Ye especially un objects ke liye useful hai jo:

> ek doosre ko reference karte hain, lekin program ke kisi reachable object se accessible nahi hain.

Example:

```python
a = []
b = []

a.append(b)
b.append(a)
```

Diagram:

```text
a ─────→ [ b ]
↑          │
│          ↓
└──── [ a ] ← b
```

Actually simplified:

```text
a → b
↑   ↓
└───┘
```

Cycle ban gaya.

---

# 8. Circular reference problem

Suppose:

```python
a = []
b = []

a.append(b)
b.append(a)
```

Ab:

```python
del a
del b
```

Kya cycle ke objects reachable hain?

Nahi.

Lekin objects ek doosre ko reference kar rahe hain.

Conceptually:

```text
a-object → b-object
    ↑         ↓
    └─────────┘

external references:
NONE
```

Ye **cyclic garbage** hai.

---

# 9. Garbage Collector ka role

Python ka cyclic GC unreachable reference cycles ko identify karke cleanup kar sakta hai.

Module:

```python
import gc
```

Useful functions:

```python
gc.collect()
```

Manually collection trigger kar sakta hai.

Example:

```python
import gc

gc.collect()
```

Lekin normal application code mein har jagah manually `gc.collect()` call karna usually zaroori nahi.

Python GC normally automatically manage karta hai.

---

# 10. Reference Counting vs GC

Ye distinction important hai.

### Reference counting

```text
reference count → 0
        ↓
object can be deallocated
```

### Cyclic GC

```text
A → B
↑   ↓
└───┘

external references nahi
        ↓
cyclic garbage detect
        ↓
cleanup
```

So:

```text
Reference counting
+
Cyclic garbage collector
```

CPython memory management ka important combination hai.

---

# 11. `gc.get_count()`

GC ke internal generation counters dekhne ke liye:

```python
import gc

print(gc.get_count())
```

Example output:

```text
(100, 5, 2)
```

Exact values runtime-dependent hain.

Is output ko simply:

> current GC tracking activity/counters

ke perspective se dekho.

---

# 12. `gc.collect()`

```python
import gc

collected = gc.collect()

print(collected)
```

Ye collected unreachable cyclic objects ki count return kar sakta hai.

Exact result environment aur objects par depend karega.

---

# 13. `__del__()`

Python mein class mein:

```python
def __del__(self):
    ...
```

define kiya ja sakta hai.

Example:

```python
class Employee:

    def __del__(self):
        print("Object cleanup")
```

Lekin ek important warning:

> `__del__()` ko deterministic resource management ke liye use nahi karna chahiye.

---

# 14. `__del__()` destructor jaisa hai?

Informally log isko "destructor" kehte hain.

Lekin C++ ke deterministic destructor model se directly compare karna misleading ho sakta hai.

Python mein:

```python
__del__()
```

object finalization hook hai.

Kab execute hoga, especially complex reference cycles/interpreter shutdown mein, predictable resource-management mechanism nahi hai.

---

# 15. File ke liye `__del__()` use mat karo

Bad design:

```python
class FileManager:

    def __del__(self):
        self.file.close()
```

Better:

```python
with open("data.txt") as file:
    data = file.read()
```

Yahan tumhara **Context Manager** lesson directly connect hota hai.

```text
Context Manager
→ deterministic resource lifecycle

Garbage Collector
→ memory/object cleanup
```

---

# 16. Memory cleanup vs resource cleanup

Ye distinction yaad rakho.

### Memory

```text
Python object
↓
GC/reference counting
```

### External resources

```text
file
database connection
socket
lock
network resource
```

Inke liye:

```text
with
try/finally
explicit close()
```

zyada appropriate hain.

---

# 17. Weak Reference

Ab interesting concept:

```python
import weakref
```

Normal reference:

```python
a = obj
```

object ko alive rakhne mein reference count contribute karta hai.

Weak reference:

```text
object ko reference karta hai
lekin normally object ko alive nahi rakhta
```

---

# 18. Simple example

```python
import weakref

class Equipment:
    pass

equipment = Equipment()

weak_equipment = weakref.ref(equipment)
```

Ab:

```python
weak_equipment()
```

object return kar sakta hai:

```text
<Equipment object ...>
```

Jab object alive hai.

---

# 19. Object remove hone ke baad

```python
del equipment
```

Agar koi strong reference nahi bacha, object deallocate ho sakta hai.

Then:

```python
weak_equipment()
```

→

```text
None
```

Conceptually:

```text
strong reference
→ object ko alive rakhta hai

weak reference
→ object ko observe/reference karta hai
→ alive rakhne ki ownership nahi deta
```

---

# 20. Weak reference ka use kahan?

Useful cases:

* caches
* object registries
* observer patterns
* relationships jahan ownership nahi chahiye
* avoiding unnecessary reference retention

Example architecture:

```text
Manager
   │
   ├── strong reference → important object
   │
Cache
   │
   └── weak reference → object
```

Object ke otherwise unreachable hone par weak reference automatically invalid ho sakta hai.

---

# 21. `WeakValueDictionary`

`weakref` ka useful structure:

```python
from weakref import WeakValueDictionary
```

Example:

```python
registry = WeakValueDictionary()
```

Conceptually:

```python
registry["AHU-01"] = ahu
```

Registry object ko weakly reference kar sakti hai.

Agar `ahu` ka koi strong reference nahi bacha, registry entry automatically disappear ho sakti hai.

---

# 22. HVAC example

Suppose:

```python
ahu = AHU("AHU-01")
```

Tum ek global registry maintain karte ho:

```python
registry["AHU-01"] = ahu
```

Agar normal dictionary hai:

```text
registry
   ↓
ahu
```

Registry khud object ko alive rakh sakti hai.

Agar registry sirf tracking/reference purpose ke liye hai aur ownership nahi karni, weak references useful ho sakte hain.

---

# 23. `weakref.ref`

Weak reference ko call kiya jata hai:

```python
weak_equipment()
```

not:

```python
weak_equipment
```

Kyun?

Because `weak_equipment` ek weak-reference object hai.

```text
weak_equipment
       ↓
weakref object
       ↓
   target object
```

Call:

```python
weak_equipment()
```

target return karta hai, agar target abhi alive hai.

---

# 24. Callback

Weak reference ke saath callback bhi diya ja sakta hai.

Conceptually:

```python
weakref.ref(obj, callback)
```

Jab referenced object finalize/deallocate hota hai, callback invoke ho sakta hai under the weakref mechanism.

Ye advanced observer/cache patterns mein useful ho sakta hai.

---

# 25. `id()` aur memory

Python mein:

```python
x = []
print(id(x))
```

`id()` current object's identity identifier return karta hai.

Often CPython mein ye memory address jaisa appear karta hai, lekin language-level guarantee sirf **unique identity identifier for the object's lifetime** ki hai.

Isliye:

> `id()` ko guaranteed raw memory address samajhna correct nahi.

---

# 26. Object lifetime

Simple mental model:

```text
create object
     ↓
strong references
     ↓
object reachable
     ↓
references remove
     ↓
object unreachable
     ↓
reference counting / GC
     ↓
cleanup/deallocation
```

---

# 27. `del` ko properly samjho

Example:

```python
a = []
b = a
```

Then:

```python
del a
```

Meaning:

```text
a ka binding remove
```

Not:

```text
object definitely destroyed
```

Because:

```text
b → object
```

still exists.

---

# 28. `del` variable vs object

```python
del a
```

is essentially about removing a name/binding.

Whereas:

```python
del obj.attribute
```

attribute ko remove karta hai.

And:

```python
del items[0]
```

collection se item remove karta hai.

So `del` ka exact effect context par depend karta hai.

---

# 29. Previous lessons se connection

Ab tumhare previous concepts connect ho rahe hain:

### Assignment

```python
b = a
```

→ same object reference.

### Copy

```python
b = a.copy()
```

→ shallow copy.

### Deepcopy

```python
b = copy.deepcopy(a)
```

→ recursive copying.

### Reference counting

```text
multiple references
→ object remains alive
```

### Garbage collection

```text
unreachable cycles
→ cleanup
```

### Weak reference

```text
reference without ownership
```

### Context manager

```text
resource lifecycle
```

---

# 30. Ek complete example

```python
import weakref

class Equipment:
    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

ahu = Equipment("AHU-01")

weak_ahu = weakref.ref(ahu)

print(weak_ahu().equipment_id)
```

Output:

```text
AHU-01
```

Ab:

```python
del ahu
```

Agar koi aur strong reference nahi hai, then:

```python
print(weak_ahu())
```

may produce:

```text
None
```

---

# 31. Important distinction

```text
Reference
```

aur:

```text
Ownership
```

same concept nahi hain.

Strong reference generally object ko reachable/alive rakhta hai.

Weak reference object ko observe/reference karta hai without keeping it alive.

---

# 32. Memory management ka final diagram

```text
                 Python Object
                      │
              ┌───────┴────────┐
              ↓                ↓
        Strong references   Weak references
              │                │
              ↓                ↓
        keep object alive   don't own object
              │
              ↓
       no strong references
              │
              ↓
        object unreachable
              │
        ┌─────┴─────┐
        ↓           ↓
   ref counting   cyclic GC
        │           │
        └─────┬─────┘
              ↓
         cleanup/deallocation
```

---

## Golden Rules

```text
1. del x ≠ guaranteed immediate object destruction

2. b = a ≠ copy

3. Reference counting handles many objects promptly in CPython.

4. Cyclic GC handles unreachable reference cycles.

5. __del__ deterministic cleanup ka replacement nahi.

6. Files/sockets/locks → context manager / explicit cleanup.

7. weakref object ko alive nahi rakhta.

8. id() identity deta hai; guaranteed raw memory address nahi.
```

### Next Lesson 49

Ab hum **Python Exceptions deeply** karenge:

```text
Exception hierarchy
BaseException
Exception
raise
try / except / else / finally
custom exceptions
raise ... from ...
exception chaining
```

Aur especially ye samjhenge:

> `raise` aur `return` mein actual conceptual difference kya hai, aur `raise ... from ...` kyun use hota hai?

# Lesson 49: Python Exceptions — `try`, `except`, `raise`, `else`, `finally`

Ab hum Python ka **Exception Handling system** deeply samjhenge.

Ye especially tumhare work-order script, file handling, API calls, Google Sheets aur data processing mein bohat important hai.

---

# 1. Exception kya hoti hai?

Exception ka matlab:

> Program execute ho raha tha, lekin koi unexpected/error condition aa gayi.

Example:

```python
x = 10
y = 0

result = x / y
```

Python:

```text
ZeroDivisionError
```

generate karega.

---

# 2. Exception aur normal result mein difference

Normal:

```python
result = 10 + 5
print(result)
```

Flow:

```text
10 + 5
 ↓
15
 ↓
continue
```

Exception:

```python
result = 10 / 0
```

Flow:

```text
10 / 0
 ↓
ERROR
 ↓
exception raised
 ↓
normal flow interrupt
```

---

# 3. Exception hierarchy

Python mein exceptions hierarchy hoti hai.

Simplified:

```text
BaseException
│
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
│
└── Exception
    │
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── IndexError
    ├── AttributeError
    ├── ZeroDivisionError
    ├── FileNotFoundError
    └── ...
```

Most application errors ke liye tum:

```python
except Exception:
```

use karte ho.

---

# 4. `BaseException` vs `Exception`

Normally:

```python
except Exception:
```

user/application errors handle karne ke liye appropriate hai.

`BaseException` ke andar kuch special control-flow exceptions bhi hain:

```text
SystemExit
KeyboardInterrupt
GeneratorExit
```

Isliye generally:

```python
except BaseException:
```

blindly use nahi karna chahiye.

---

# 5. Basic `try/except`

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Zero se divide nahi kar sakte")
```

Output:

```text
Zero se divide nahi kar sakte
```

Program exception ke bawajood controlled way mein continue kar sakta hai.

---

# 6. `try` ka kaam

```python
try:
    ...
```

ke andar woh code rakhte hain jahan expected exception aa sakti hai.

Example:

```python
try:
    number = int(input("Number: "))
except ValueError:
    print("Valid number enter karo")
```

Agar user:

```text
abc
```

enter kare:

```text
ValueError
```

catch ho jayegi.

---

# 7. `except` ka kaam

`except` batata hai:

> Agar specified exception aaye to kya karna hai?

Example:

```python
try:
    number = int("abc")
except ValueError:
    print("Conversion failed")
```

---

# 8. Multiple exceptions

```python
try:
    value = data["temperature"]
    result = 100 / value

except KeyError:
    print("Temperature key missing")

except ZeroDivisionError:
    print("Temperature zero hai")
```

Different problems ke liye different handling.

---

# 9. Multiple exception types ek `except` mein

Agar handling same ho:

```python
try:
    ...
except (ValueError, TypeError):
    print("Invalid input")
```

Yahan dono exceptions same handler use karengi.

---

# 10. `Exception as e`

Exception object ko variable mein capture kar sakte ho:

```python
try:
    number = int("abc")
except ValueError as e:
    print(e)
```

Output kuch aisa:

```text
invalid literal for int() with base 10: 'abc'
```

`e` exception object hai.

---

# 11. `type(e)`

```python
try:
    int("abc")
except Exception as e:
    print(type(e))
```

Output:

```text
<class 'ValueError'>
```

Aur:

```python
print(str(e))
```

error message deta hai.

---

# 12. `raise`

Ab important keyword:

```python
raise
```

`raise` manually exception generate karta hai.

Example:

```python
age = -5

if age < 0:
    raise ValueError("Age negative nahi ho sakti")
```

Output:

```text
ValueError: Age negative nahi ho sakti
```

---

# 13. `raise` kyun use karte hain?

Suppose function ko valid temperature chahiye:

```python
def set_temperature(temp):
    if temp < -273.15:
        raise ValueError("Invalid temperature")

    return temp
```

Now:

```python
set_temperature(-500)
```

exception raise karega.

---

# 14. `raise` vs `return`

Ye important difference hai.

### `return`

```python
def divide(a, b):
    if b == 0:
        return None
```

Normal function flow se value return hoti hai.

### `raise`

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("b cannot be zero")
```

Yahan normal flow interrupt hota hai.

Conceptually:

```text
return
→ caller ko result do

raise
→ caller ko exception signal karo
```

---

# 15. Custom Exception

Tum apni exception class bana sakte ho:

```python
class InvalidTemperatureError(Exception):
    pass
```

Then:

```python
def set_temperature(temp):
    if temp < -273.15:
        raise InvalidTemperatureError(
            "Temperature invalid hai"
        )
```

---

# 16. Custom exception kyun?

Suppose tumhare HVAC system mein:

```text
InvalidTemperature
InvalidDamperPosition
EquipmentOffline
CommunicationFailure
```

alag error categories hain.

Custom exceptions code ko clear bana deti hain.

Example:

```python
class EquipmentOfflineError(Exception):
    pass
```

Then:

```python
raise EquipmentOfflineError("AHU-01 offline hai")
```

---

# 17. Exception inheritance

Custom exceptions normally `Exception` se inherit karti hain:

```python
class EquipmentError(Exception):
    pass

class EquipmentOfflineError(EquipmentError):
    pass

class CommunicationError(EquipmentError):
    pass
```

Hierarchy:

```text
Exception
    │
    └── EquipmentError
          ├── EquipmentOfflineError
          └── CommunicationError
```

Ab:

```python
except EquipmentError:
```

dono child exceptions catch kar sakta hai.

---

# 18. `finally`

`finally` generally cleanup ke liye use hota hai.

```python
try:
    print("Work")
except Exception:
    print("Error")
finally:
    print("Cleanup")
```

`finally` normally execute hota hai whether exception occurred or not.

---

# 19. `try + except + finally`

```python
try:
    file = open("data.txt")
    data = file.read()

except FileNotFoundError:
    print("File nahi mili")

finally:
    print("Operation finished")
```

Lekin file ke liye better:

```python
with open("data.txt") as file:
    data = file.read()
```

Ye tumhare **context manager** lesson se directly connected hai.

---

# 20. `else`

Exception handling mein `else` bhi hota hai:

```python
try:
    result = 10 / 2

except ZeroDivisionError:
    print("Error")

else:
    print("Calculation successful")
```

`else` tab execute hota hai jab `try` successfully complete ho.

---

# 21. Complete structure

```python
try:
    ...
except SomeError:
    ...
else:
    ...
finally:
    ...
```

Flow:

```text
             try
              │
        ┌─────┴─────┐
        │           │
     success      error
        │           │
        ↓           ↓
      else       except
        │           │
        └─────┬─────┘
              ↓
           finally
```

---

# 22. `else` ka actual benefit

Suppose:

```python
try:
    data = load_data()
    process_data(data)

except ValueError:
    print("Invalid data")
```

Problem:

`try` ke andar `load_data()` aur `process_data()` dono hain.

Agar `process_data()` ke andar `ValueError` aaye, woh bhi same handler catch karega.

Kabhi kabhi tum specifically input/loading error handle karna chahte ho.

Better:

```python
try:
    data = load_data()

except ValueError:
    print("Loading failed")

else:
    process_data(data)
```

Ab `try` ka scope focused hai.

---

# 23. Exception propagation

Exception ko har function mein catch karna zaroori nahi.

Example:

```python
def divide(a, b):
    return a / b

def calculate():
    return divide(10, 0)

calculate()
```

Flow:

```text
calculate()
    ↓
divide()
    ↓
ZeroDivisionError
    ↓
calculate() mein handler nahi
    ↓
caller ke paas
```

Python call stack mein upar search karta hai.

---

# 24. Caller exception catch kar sakta hai

```python
def divide(a, b):
    return a / b

try:
    result = divide(10, 0)

except ZeroDivisionError:
    print("Cannot divide by zero")
```

Yahan `divide()` ne exception catch nahi ki.

Caller ne catch ki.

---

# 25. Exception propagation diagram

```text
main()
 │
 └── calculate()
       │
       └── divide()
              │
              └── ZeroDivisionError
                     ↑
                 no handler
                     │
                     ↑
               calculate()
                     │
                 no handler
                     │
                     ↑
                  main()
                     │
                  handler
                     ↓
                   catch
```

---

# 26. `raise` inside `except`

Kabhi error ko log karke dobara raise karna hota hai:

```python
try:
    value = int("abc")

except ValueError as e:
    print("Logging error:", e)
    raise
```

Yahan:

```python
raise
```

current exception ko **same exception** ke saath re-raise karta hai.

---

# 27. `raise` vs `raise e`

Important subtle difference.

Inside:

```python
except ValueError:
    raise
```

current exception re-raise hoti hai aur traceback preservation ke liye preferred form hai.

Whereas:

```python
except ValueError as e:
    raise e
```

explicitly exception object raise karta hai; traceback presentation/propagation semantics differ kar sakti hain.

Rule:

> Current exception ko simply re-raise karna ho → `raise` use karo.

---

# 28. Exception chaining: `raise ... from ...`

Ye advanced aur bohat useful concept hai.

Suppose:

```python
try:
    number = int("abc")

except ValueError as e:
    raise RuntimeError("Data processing failed") from e
```

Ab do levels hain:

```text
Original:
ValueError
     ↓
wrapped as
RuntimeError
```

---

# 29. `from` kyun use karte hain?

Suppose tumhari application layer mein:

```text
CSV parsing failed
```

important hai, lekin underlying reason:

```text
ValueError
```

bhi preserve karna hai.

```python
try:
    value = int("abc")

except ValueError as e:
    raise RuntimeError(
        "Work order data invalid hai"
    ) from e
```

Traceback conceptually batayega:

```text
ValueError
   ↓
The above exception caused
   ↓
RuntimeError
```

Isko **exception chaining** kehte hain.

---

# 30. `raise ... from None`

Kabhi underlying exception intentionally hide karni ho:

```python
try:
    ...
except ValueError:
    raise RuntimeError("Invalid configuration") from None
```

Isse explicit exception context display se suppress kiya ja sakta hai.

Use carefully, kyunki debugging information hide ho sakti hai.

---

# 31. `__cause__` aur `__context__`

Exception objects ke andar chaining information hoti hai.

Example:

```python
try:
    int("abc")
except ValueError as e:
    try:
        raise RuntimeError("Failed") from e
    except RuntimeError as new_error:
        print(new_error.__cause__)
```

`__cause__` original explicitly chained exception ko represent karta hai.

---

# 32. `__context__`

Agar ek exception handle karte waqt doosri exception raise ho jaye:

```python
try:
    int("abc")

except ValueError:
    {}["missing"]
```

to second exception ka context pehli exception se related ho sakta hai.

Conceptually:

```text
ValueError
   ↓
while handling it
   ↓
KeyError
```

Python exception context preserve karta hai.

---

# 33. Work-order example

Tumhare work-order script mein:

```python
def create_folder(work_order_number):
    if not work_order_number:
        raise ValueError("Work Order Number missing")

    ...
```

Caller:

```python
try:
    create_folder("")
except ValueError as e:
    print("Invalid work order:", e)
```

---

# 34. Better custom exception architecture

```python
class WorkOrderError(Exception):
    pass


class MissingWorkOrderNumberError(WorkOrderError):
    pass


class InvalidWorkOrderNumberError(WorkOrderError):
    pass
```

Then:

```python
def validate_work_order(number):

    if number is None:
        raise MissingWorkOrderNumberError(
            "Work Order Number missing"
        )

    if not isinstance(number, str):
        raise InvalidWorkOrderNumberError(
            "Work Order Number must be string"
        )
```

Caller:

```python
try:
    validate_work_order(number)

except WorkOrderError as e:
    print("Work Order problem:", e)
```

---

# 35. `except Exception` ka overuse

Ye avoid karo:

```python
try:
    ...
except Exception:
    pass
```

Ye dangerous hai.

Kyun?

Because tum errors silently ignore kar rahe ho.

Example:

```python
try:
    create_folder()
except Exception:
    pass
```

Agar folder creation fail hua:

```text
No message
No error
No clue
```

Debugging difficult ho jayegi.

---

# 36. Better approach

Specific exception:

```python
try:
    create_folder()

except PermissionError:
    print("Permission denied")

except FileNotFoundError:
    print("Path nahi mili")
```

Ya agar generic handling genuinely required ho:

```python
except Exception as e:
    print("Unexpected error:", e)
    raise
```

---

# 37. `except` order important hai

Wrong:

```python
try:
    ...
except Exception:
    print("General error")

except ValueError:
    print("Value error")
```

`ValueError` kabhi second handler tak nahi pohanchega.

Kyun?

Because:

```text
ValueError
   ↓
Exception ka subclass hai
```

Pehla handler already catch kar lega.

Correct:

```python
try:
    ...

except ValueError:
    ...

except Exception:
    ...
```

Specific → general.

---

# 38. Exception handling ka good pattern

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

Mental model:

```text
try
→ risky operation

except
→ error handling

else
→ success-only code

finally
→ cleanup
```

---

# 39. `return` + `finally`

Ek subtle behavior:

```python
def test():
    try:
        return "try"
    finally:
        print("finally")
```

Call:

```python
print(test())
```

Output:

```text
finally
try
```

Yani `return` execute hone se pehle `finally` run hota hai.

---

# 40. `finally` mein `return` avoid karo

Example:

```python
def test():
    try:
        return "try"
    finally:
        return "finally"
```

Result:

```text
finally
```

`finally` ka return original return ko override kar deta hai.

Isliye generally:

> `finally` block mein `return` use karna avoid karo.

---

# 41. Final mental model

```text
Exception
   ↓
unexpected/error condition
   ↓
raise
   ↓
search call stack
   ↓
matching except
   ↓
handle / transform / re-raise
```

And:

```text
try
 ├── error → except
 └── success → else
          ↓
       finally
```

### Golden rules

```text
1. raise → exception signal karta hai.

2. return → normal value/control flow deta hai.

3. except → matching exception handle karta hai.

4. else → sirf successful try ke baad.

5. finally → cleanup/finalization logic.

6. raise → current exception ko re-raise karta hai.

7. raise NewError(...) from e
   → exception chaining.

8. Specific exceptions ko prefer karo.

9. except Exception: pass
   → usually bad practice.

10. Resource cleanup ke liye context manager
    → with
    prefer karo.
```

## Next Lesson 50

Ab hum **Python Exception Design + Custom Exceptions + `ExceptionGroup` / `except*`** dekhenge.

Ismein especially ye samjhenge:

```python
class WorkOrderError(Exception):
    ...
```

ko proper application architecture mein kaise design karte hain, aur modern Python mein **multiple exceptions ko ek saath kaise handle** kiya ja sakta hai.

# Lesson 50: Custom Exceptions + `ExceptionGroup` + `except*`

Ab hum exception handling ka next level dekhenge.

Tumhare work-order/data-processing scripts ke liye sabse important cheez hai:

```text
Normal Exception
      ↓
Custom Exception
      ↓
Exception hierarchy
      ↓
Multiple exceptions
      ↓
ExceptionGroup
      ↓
except*
```

---

# 1. Custom Exception kyun banate hain?

Suppose tumhare work-order system mein errors hain:

```text
Work Order missing
Equipment ID missing
Invalid Floor
Invalid Work Order Number
Folder creation failed
```

Agar har jagah:

```python
raise ValueError(...)
```

use karo, to errors ka meaning mix ho jata hai.

Better:

```python
class WorkOrderError(Exception):
    pass
```

Ab tumhari application ke work-order related errors ka ek common base hai.

---

# 2. Exception hierarchy

Hum detailed hierarchy bana sakte hain:

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

Diagram:

```text
Exception
   │
   └── WorkOrderError
          │
          └── ValidationError
                 ├── MissingWorkOrderError
                 └── InvalidWorkOrderError
```

---

# 3. Iska faida kya?

Ab:

```python
except WorkOrderError:
```

poore work-order family ko catch kar sakta hai.

Aur:

```python
except MissingWorkOrderError:
```

sirf specific error handle karega.

Example:

```python
try:
    validate_work_order()

except MissingWorkOrderError:
    print("WO number missing")

except InvalidWorkOrderError:
    print("WO number invalid")

except WorkOrderError:
    print("Other work-order error")
```

Specific → general order important hai.

---

# 4. Custom Exception ko message do

Simple:

```python
class WorkOrderError(Exception):
    pass
```

Then:

```python
raise WorkOrderError("Work order process failed")
```

Exception ke paas message available hoga:

```python
try:
    raise WorkOrderError("WO-1001 failed")

except WorkOrderError as e:
    print(e)
```

Output:

```text
WO-1001 failed
```

---

# 5. Custom Exception mein data bhi rakh sakte ho

Ye bohat useful hai.

```python
class WorkOrderError(Exception):

    def __init__(self, work_order_number, message):
        self.work_order_number = work_order_number
        self.message = message

        super().__init__(message)
```

Ab:

```python
raise WorkOrderError(
    "WO-1001",
    "Folder create nahi hua"
)
```

Catch:

```python
try:
    ...
except WorkOrderError as e:
    print(e.work_order_number)
    print(e.message)
```

Output:

```text
WO-1001
Folder create nahi hua
```

---

# 6. `super().__init__(message)` kyun?

Ye line:

```python
super().__init__(message)
```

parent `Exception` ko message pass karti hai.

Isliye:

```python
print(e)
```

bhi message dega.

```text
Folder create nahi hua
```

Agar custom exception mein extra data rakh rahe ho, `super().__init__()` karna generally useful hai.

---

# 7. Better Work Order Example

```python
class WorkOrderError(Exception):
    pass


class MissingWorkOrderError(WorkOrderError):
    def __init__(self, row_number):
        self.row_number = row_number

        super().__init__(
            f"Work Order missing at row {row_number}"
        )
```

Use:

```python
raise MissingWorkOrderError(15)
```

Catch:

```python
except MissingWorkOrderError as e:
    print(e)
    print(e.row_number)
```

---

# 8. Exception ko data object ki tarah treat karna

Custom exception mein useful context store kar sakte ho:

```python
class EquipmentError(Exception):

    def __init__(self, equipment_id, message):
        self.equipment_id = equipment_id
        super().__init__(message)
```

Then:

```python
raise EquipmentError(
    "AHU-01",
    "Communication failed"
)
```

Ab caller ke paas:

```text
equipment_id = AHU-01
message = Communication failed
```

dono available hain.

---

# 9. `__str__()` customize karna

Exception ki display formatting bhi customize kar sakte ho:

```python
class EquipmentError(Exception):

    def __init__(self, equipment_id, message):
        self.equipment_id = equipment_id
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.equipment_id}: {self.message}"
```

Then:

```python
raise EquipmentError(
    "AHU-01",
    "Communication failed"
)
```

Print:

```text
AHU-01: Communication failed
```

---

# 10. Real application architecture

Tumhare work-order system mein structure kuch aisa ho sakta hai:

```text
Exception
│
└── WorkOrderError
    │
    ├── ValidationError
    │   ├── MissingFieldError
    │   └── InvalidFieldError
    │
    ├── FileOperationError
    │   ├── FolderCreationError
    │   └── PermissionError
    │
    └── DataSourceError
        ├── GoogleSheetError
        └── CSVError
```

Ab high-level code:

```python
try:
    process_work_orders()

except WorkOrderError as e:
    print("Work-order processing failed:", e)
```

Low-level details hide ho sakte hain.

---

# 11. Exception translation

Ye bohat useful architecture pattern hai.

Suppose Python ki built-in exception:

```python
FileNotFoundError
```

aayi.

Lekin tumhari application ko filesystem detail expose nahi karni.

Tum:

```python
try:
    open(path)

except FileNotFoundError as e:
    raise FileOperationError(
        f"Work order folder unavailable: {path}"
    ) from e
```

kar sakte ho.

Ab:

```text
FileNotFoundError
       ↓
application layer
       ↓
FileOperationError
```

Original reason lost nahi hua because:

```python
from e
```

use kiya.

---

# 12. Exception chaining recap

```python
raise FileOperationError("Folder unavailable") from e
```

Conceptually:

```text
Original exception
       ↓
       e
       ↓
New application-level exception
```

Ye layered applications mein bohat useful hai.

---

# 13. Ab `ExceptionGroup`

Ab modern Python ka important feature.

Suppose tumhare paas 3 work orders hain:

```text
WO-1001 → valid
WO-1002 → invalid
WO-1003 → invalid
```

Agar tum sequentially process karte ho:

```python
for order in orders:
    process(order)
```

to first error par function ruk sakta hai.

Lekin batch processing mein tum chahte ho:

> Saare orders process karo aur saare errors ek saath report karo.

Yahan `ExceptionGroup` useful hai.

---

# 14. Basic `ExceptionGroup`

```python
errors = [
    ValueError("Invalid floor"),
    ValueError("Missing equipment ID"),
]
```

ExceptionGroup:

```python
raise ExceptionGroup(
    "Work order validation failed",
    errors
)
```

Ek group mein multiple exceptions hain.

Conceptually:

```text
ExceptionGroup
│
├── ValueError
└── ValueError
```

---

# 15. `except ExceptionGroup` bhi possible hai

```python
try:
    raise ExceptionGroup(
        "Validation errors",
        [
            ValueError("Bad floor"),
            TypeError("Bad equipment ID")
        ]
    )

except ExceptionGroup as eg:
    print(eg)
```

Lekin modern Python mein special feature:

```python
except*
```

bhi hai.

---

# 16. `except*`

`except*` multiple exceptions ke group ke individual matching members handle karne ke liye use hota hai.

Example:

```python
try:
    raise ExceptionGroup(
        "Errors",
        [
            ValueError("Bad floor"),
            TypeError("Bad ID")
        ]
    )

except* ValueError as e:
    print("Value errors:", e)

except* TypeError as e:
    print("Type errors:", e)
```

Yahan dono types separately match ho sakti hain.

---

# 17. Normal `except` vs `except*`

### Normal `except`

```python
except ValueError:
```

normal exception flow ke liye.

### `except*`

```python
except* ValueError:
```

exception group ke matching members ke liye.

Mental model:

```text
except
→ one exception flow

except*
→ exception group ko type ke basis par split/match
```

---

# 18. ExceptionGroup ko work-order batch mein dekho

Suppose:

```python
orders = [
    "WO-1001",
    "WO-1002",
    "WO-1003"
]
```

Validation:

```python
def validate(order):
    ...
```

Potential results:

```text
WO-1001 → valid
WO-1002 → MissingFieldError
WO-1003 → InvalidFieldError
```

Tum errors collect kar sakte ho:

```python
errors = []

for order in orders:
    try:
        validate(order)

    except Exception as e:
        errors.append(e)

if errors:
    raise ExceptionGroup(
        "Batch validation failed",
        errors
    )
```

---

# 19. Is architecture ka faida

Without grouping:

```text
WO-1002 fails
↓
program stops
↓
WO-1003 not checked
```

With collection:

```text
WO-1001 → OK
WO-1002 → Error
WO-1003 → Error
        ↓
collect all
        ↓
ExceptionGroup
```

Batch processing ke liye useful.

---

# 20. ExceptionGroup nested bhi ho sakta hai

Exception groups tree structure rakh sakte hain:

```text
ExceptionGroup
│
├── ValidationError
│
├── ExceptionGroup
│   ├── ValueError
│   └── TypeError
│
└── FileNotFoundError
```

Isliye `except*` matching nested groups ke matching parts ko handle kar sakta hai.

---

# 21. `except*` ka important difference

`except*` normal exception handler ki tarah exactly same semantics nahi rakhta.

Iska purpose:

> ExceptionGroup ke andar matching exceptions ko extract/handle karna.

Example:

```python
try:
    raise ExceptionGroup(
        "Errors",
        [
            ValueError("A"),
            TypeError("B"),
            ValueError("C")
        ]
    )

except* ValueError as e:
    print("ValueError group handled")
```

`ValueError` members handler ko milenge, jabke unmatched exceptions propagate ho sakti hain.

---

# 22. `except` aur `except*` mix?

Ek hi `try` statement mein normal `except` aur `except*` clauses ko freely mix nahi kar sakte.

Isliye exception-group handling design karte waqt:

```text
normal exception handling
```

aur:

```text
ExceptionGroup handling
```

ko separate conceptual paths samjho.

---

# 23. `ExceptionGroup` kis Python version mein?

`ExceptionGroup` aur `except*` **Python 3.11+** mein introduce hue.

Agar tum modern Python use kar rahe ho, ye available hain.

Tumhare current JDK/Java work se unrelated hai—ye pure Python feature hai.

---

# 24. Custom `ExceptionGroup`

Tum custom exception group bhi subclass kar sakte ho, lekin normal applications mein built-in:

```python
ExceptionGroup
```

kaafi cases mein enough hota hai.

Simple custom hierarchy:

```python
class WorkOrderError(Exception):
    pass
```

Aur batch:

```python
raise ExceptionGroup(
    "Work Order errors",
    [
        MissingWorkOrderError(...),
        InvalidWorkOrderError(...)
    ]
)
```

---

# 25. Important: `ExceptionGroup` ka use har jagah nahi

Agar sirf ek error expected hai:

```python
raise ValueError(...)
```

simple exception hi use karo.

`ExceptionGroup` tab useful hai jab:

```text
multiple independent operations
+
multiple failures
+
batch/concurrent processing
```

ho.

---

# 26. Async se connection

Tumne pehle `asyncio`, Tasks aur concurrency padhi hai.

Suppose multiple async tasks concurrently fail:

```text
Task 1 → ValueError
Task 2 → TimeoutError
Task 3 → ConnectionError
```

Modern Python mein structured concurrency, especially `asyncio.TaskGroup`, multiple task failures ko exception groups ke form mein surface kar sakta hai.

Conceptually:

```text
TaskGroup
│
├── Task 1 → error
├── Task 2 → error
└── Task 3 → error
          ↓
    ExceptionGroup
```

Ye `ExceptionGroup` ko tumhari earlier async lessons se connect karta hai.

---

# 27. `TaskGroup` example

Python 3.11+:

```python
import asyncio

async def task1():
    raise ValueError("Task 1 failed")

async def task2():
    raise TypeError("Task 2 failed")

async def main():
    async with asyncio.TaskGroup() as group:
        group.create_task(task1())
        group.create_task(task2())

asyncio.run(main())
```

Multiple task failures exception-group mechanism ke through report ho sakti hain.

---

# 28. Handle async failures

Conceptually:

```python
try:
    await main()

except* ValueError as e:
    print("Value errors:", e)

except* TypeError as e:
    print("Type errors:", e)
```

Yahan previous lessons connect hote hain:

```text
asyncio
   ↓
TaskGroup
   ↓
multiple failures
   ↓
ExceptionGroup
   ↓
except*
```

---

# 29. Best design for your work-order script

Tumhare script ke context mein:

```python
class WorkOrderError(Exception):
    pass


class MissingWorkOrderNumberError(WorkOrderError):
    pass


class InvalidWorkOrderNumberError(WorkOrderError):
    pass


class FolderCreationError(WorkOrderError):
    pass
```

Processing:

```python
errors = []

for row_number, row in enumerate(rows, start=2):

    try:
        process_work_order(row)

    except WorkOrderError as e:
        errors.append(e)
```

After processing:

```python
if errors:
    raise ExceptionGroup(
        "Work order processing failed",
        errors
    )
```

Is approach se tum:

> **poori CSV process karke saare problematic rows ek saath identify kar sakte ho.**

Ye batch-data processing mein practical pattern hai.

---

# 30. Final mental model

```text
Exception
│
├── Built-in
│   ├── ValueError
│   ├── TypeError
│   └── KeyError
│
└── Custom
    └── WorkOrderError
        ├── ValidationError
        └── FolderCreationError
```

Normal:

```text
one operation
     ↓
one exception
     ↓
except
```

Batch:

```text
many operations
     ↓
many exceptions
     ↓
ExceptionGroup
     ↓
except*
```

### Golden rules

```text
1. Custom exception → application-specific meaning.

2. Exception hierarchy → related errors ko organize karo.

3. `raise ... from e`
   → original cause preserve karte hue higher-level error banao.

4. ExceptionGroup
   → multiple independent exceptions ko group karta hai.

5. except*
   → ExceptionGroup ke matching exception types handle karta hai.

6. Simple single error → normal Exception.

7. Batch/concurrent independent failures → ExceptionGroup useful.

8. Custom exceptions mein useful context store kar sakte ho.
```

## Next Lesson 51

Ab hum **Python logging** karenge:

```text
print()
   ↓
logging
   ↓
DEBUG
INFO
WARNING
ERROR
CRITICAL
   ↓
logger
handler
formatter
file logging
```

Aur ye dekhenge ke production Python application mein `print()` ki jagah **logging system** kyun use kiya jata hai.
