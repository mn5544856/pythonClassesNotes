Bilkul. Ab **Lesson 71 — `typing.get_type_hints()` — Runtime Type Hints**.

Yahan ek important difference hai:

* `reveal_type()` → **static type checker se poochta hai**
* `get_type_hints()` → **runtime par annotations ko read karta hai**

---

# Lesson 71 — `typing.get_type_hints()`

## 1. Basic concept

Normally agar function hai:

```python
def get_temperature(value: float) -> float:
    return value
```

to Python ke paas annotations ki information available hoti hai.

Aap:

```python
from typing import get_type_hints

print(get_type_hints(get_temperature))
```

kar sakte ho.

Result:

```text
{
    'value': <class 'float'>,
    'return': <class 'float'>
}
```

Yani:

```python
get_type_hints()
```

function/class ke **type annotations ko runtime par retrieve aur resolve** karta hai.

---

# 2. `__annotations__` se difference

Python mein direct bhi dekh sakte ho:

```python
def get_temperature(value: float) -> float:
    return value

print(get_temperature.__annotations__)
```

Result roughly:

```python
{
    "value": float,
    "return": float
}
```

To phir sawal:

> `get_type_hints()` ki zarurat kyun?

Kyunkay `get_type_hints()` annotations ko **resolve aur process** karta hai.

---

# 3. Basic difference

### `__annotations__`

Raw annotation information:

```python
get_temperature.__annotations__
```

### `get_type_hints()`

Resolved type hints:

```python
get_type_hints(get_temperature)
```

Mental model:

```text
__annotations__
      ↓
raw annotation data

get_type_hints()
      ↓
resolved / interpreted type hints
```

---

# 4. Example with `list`

```python
from typing import get_type_hints

def get_equipment_ids() -> list[str]:
    return ["AHU-001", "AHU-002"]
```

Ab:

```python
hints = get_type_hints(get_equipment_ids)

print(hints)
```

Result:

```text
{
    'return': list[str]
}
```

Aap specific:

```python
print(hints["return"])
```

kar sakte ho.

---

# 5. Parameters aur return type

Suppose:

```python
def calculate_airflow(
    fans: int,
    airflow_per_fan: float
) -> float:
    return fans * airflow_per_fan
```

Then:

```python
from typing import get_type_hints

hints = get_type_hints(calculate_airflow)

print(hints)
```

Conceptually:

```text
fans             → int
airflow_per_fan  → float
return           → float
```

Yani `get_type_hints()` se complete function typing information mil sakti hai.

---

# 6. Iska real-world use kya hai?

Ye bohot important hai.

`get_type_hints()` useful hai jab aap **runtime framework/tool** bana rahe ho jo annotations ko read karta hai.

For example:

```text
Function
   ↓
Type hints
   ↓
Runtime framework
   ↓
Validation / serialization / dependency injection
```

---

# 7. HVAC example

Maan lo:

```python
def create_ahu(
    equipment_id: str,
    floor: int,
    airflow: float
) -> dict:
    return {
        "equipment_id": equipment_id,
        "floor": floor,
        "airflow": airflow
    }
```

Ab:

```python
from typing import get_type_hints

hints = get_type_hints(create_ahu)

print(hints)
```

Aapko milta hai:

```text
equipment_id → str
floor        → int
airflow      → float
return       → dict
```

Ab aap runtime program mein is information ko use kar sakte ho.

---

# 8. `Annotated` ke saath — important

Humne previous lesson mein `Annotated` padha tha.

Example:

```python
from typing import Annotated

Airflow = Annotated[float, "CFM"]
```

Function:

```python
def set_airflow(value: Airflow):
    ...
```

Agar:

```python
from typing import get_type_hints

print(get_type_hints(set_airflow))
```

karo, to normally metadata include nahi hogi.

Yahan important parameter aata hai:

```python
include_extras=True
```

---

# 9. `include_extras=True`

```python
from typing import Annotated, get_type_hints

Airflow = Annotated[float, "CFM"]


def set_airflow(value: Airflow):
    pass


hints = get_type_hints(
    set_airflow,
    include_extras=True
)

print(hints)
```

Ab `Annotated` ka metadata preserve hota hai.

Conceptually:

```text
value
   ↓
Annotated[
    float,
    "CFM"
]
```

Without:

```python
get_type_hints(set_airflow)
```

metadata strip ho sakta hai.

With:

```python
get_type_hints(
    set_airflow,
    include_extras=True
)
```

metadata available rehta hai.

---

# 10. Ye kyun useful hai?

Suppose humne:

```python
from typing import Annotated

Airflow = Annotated[
    float,
    "CFM",
    "Range: 0-5000"
]
```

define kiya.

Ab runtime framework:

```python
hints = get_type_hints(
    set_airflow,
    include_extras=True
)
```

se metadata read kar sakta hai.

Phir framework decide kar sakta hai:

```text
Type = float
Unit = CFM
Range = 0-5000
```

Yani:

```text
Annotated
    +
get_type_hints()
    ↓
Runtime metadata system
```

---

# 11. Forward references

Ab `get_type_hints()` ka bohot important feature.

Suppose:

```python
def get_ahu() -> "AHU":
    ...
```

Yahan:

```python
"AHU"
```

ek **forward reference** hai.

Direct:

```python
get_ahu.__annotations__
```

mein string mil sakti hai:

```text
"AHU"
```

Lekin `get_type_hints()` try karta hai isko actual type mein resolve karne ka.

```python
hints = get_type_hints(get_ahu)
```

Agar `AHU` correctly available hai, to result actual:

```text
AHU
```

type ho sakta hai.

---

# 12. `TYPE_CHECKING` se connection

Previous lesson mein humne:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

padha tha.

Ab yahan subtle issue aa sakta hai.

Suppose:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU


def get_ahu() -> AHU:
    ...
```

Static type checker ke liye:

```text
AHU
```

available hai.

Lekin runtime par:

```text
AHU
```

import nahi hua.

Agar aap:

```python
get_type_hints(get_ahu)
```

run karoge, to `AHU` resolve karne mein problem aa sakti hai.

Yani:

> `TYPE_CHECKING` type checker ke liye import deta hai, lekin `get_type_hints()` runtime mein actual type resolve karne ki koshish karta hai.

Ye distinction bohot important hai.

---

# 13. Isliye `get_type_hints()` ko runtime resolver samjho

Mental model:

```text
Annotation:
"AHU"
      ↓
get_type_hints()
      ↓
"AHU ko actual class se resolve karo"
      ↓
AHU
```

Lekin actual class runtime namespace mein available honi chahiye.

---

# 14. Class ke saath

`get_type_hints()` sirf functions ke liye nahi.

Class ke annotations bhi read kar sakte ho.

```python
from typing import get_type_hints

class AHU:
    equipment_id: str
    floor: int
    airflow: float
```

Then:

```python
hints = get_type_hints(AHU)

print(hints)
```

Conceptually:

```text
equipment_id → str
floor        → int
airflow      → float
```

---

# 15. Dataclass ke saath

Ye aur practical hai.

```python
from dataclasses import dataclass
from typing import get_type_hints


@dataclass
class Equipment:
    equipment_id: str
    floor: int
    airflow: float
```

Ab:

```python
hints = get_type_hints(Equipment)
```

Result:

```text
equipment_id → str
floor        → int
airflow      → float
```

Aap runtime framework bana sakte ho jo dataclass fields ke types automatically inspect kare.

---

# 16. TypedDict ke saath

Previous lesson mein `TypedDict` padha tha.

```python
from typing import TypedDict, get_type_hints


class EquipmentData(TypedDict):
    equipment_id: str
    floor: int
    airflow: float
```

Then:

```python
hints = get_type_hints(EquipmentData)
```

Aapko:

```text
equipment_id → str
floor        → int
airflow      → float
```

mil jayega.

Ye API/schema tooling mein useful hai.

---

# 17. Runtime validation example

Ab ek practical example.

Hum type hints ko dekh kar basic validation karna chahte hain.

```python
from typing import get_type_hints


def create_equipment(
    equipment_id: str,
    floor: int,
    airflow: float
):
    pass
```

Ab:

```python
hints = get_type_hints(create_equipment)

print(hints)
```

Framework ko pata chal gaya:

```text
equipment_id → str
floor        → int
airflow      → float
```

Ab theoretical runtime validator:

```python
data = {
    "equipment_id": "AHU-001",
    "floor": 34,
    "airflow": 2500.0,
}
```

framework type hints ke against data check kar sakta hai.

Important:

> `get_type_hints()` khud validation nahi karta.

Ye sirf **type information provide** karta hai.

---

# 18. `get_type_hints()` ≠ validation

Ye distinction yaad rakho.

```python
hints = get_type_hints(create_equipment)
```

sirf batata hai:

```text
floor → int
```

Ye automatically:

```python
floor = "34"
```

ko reject nahi karta.

Validation ke liye aapko khud logic/framework chahiye.

---

# 19. `get_type_hints()` ≠ conversion

Agar:

```python
value = "2500"
```

aur annotation:

```python
float
```

hai, `get_type_hints()` `"2500"` ko:

```python
2500.0
```

mein convert nahi karega.

Ye sirf type information retrieve karta hai.

---

# 20. `get_type_hints()` vs `reveal_type()`

Ye Lesson 70 aur 71 ka most important comparison hai.

### `reveal_type()`

```python
reveal_type(value)
```

Question:

> **Static type checker `value` ko kis type ka samajh raha hai?**

Use:

```text
development
type debugging
inference checking
```

### `get_type_hints()`

```python
get_type_hints(function)
```

Question:

> **Runtime par function/class ki annotations kya hain?**

Use:

```text
runtime introspection
frameworks
validation systems
serialization
dependency injection
metadata processing
```

---

# 21. `__annotations__` vs `get_type_hints()`

| Feature                    | `__annotations__`        | `get_type_hints()`                |
| -------------------------- | ------------------------ | --------------------------------- |
| Runtime available          | Yes                      | Yes                               |
| Raw annotations            | Yes                      | No, resolved form                 |
| Forward references resolve | Not necessarily          | Yes, when resolvable              |
| `Annotated` metadata       | Raw/annotation dependent | `include_extras=True` se preserve |
| Inheritance handling       | Limited/raw              | More complete resolution          |
| Framework use              | Possible                 | Better choice                     |

Simple mental model:

```text
__annotations__
    ↓
"Raw annotation mujhe dikhao"

get_type_hints()
    ↓
"Annotations ko resolve karke usable form mein do"
```

---

# 22. Inheritance example

Suppose:

```python
from typing import get_type_hints


class Equipment:
    equipment_id: str


class AHU(Equipment):
    airflow: float
```

`AHU` ke type hints inspect karte waqt `get_type_hints()` inherited annotations ko account kar sakta hai.

Conceptually:

```text
AHU
├── equipment_id → str
└── airflow      → float
```

Isliye complex class hierarchies mein `get_type_hints()` direct `__annotations__` se zyada useful ho sakta hai.

---

# 23. Practical architecture

Aap ek generic runtime schema system imagine karo:

```text
@dataclass
Equipment
       ↓
get_type_hints()
       ↓
field names + types
       ↓
runtime schema
       ↓
API validation / serialization
```

Example:

```python
from dataclasses import dataclass
from typing import get_type_hints


@dataclass
class Equipment:
    equipment_id: str
    floor: int
    airflow: float


hints = get_type_hints(Equipment)

for name, type_ in hints.items():
    print(name, type_)
```

Output conceptually:

```text
equipment_id <class 'str'>
floor <class 'int'>
airflow <class 'float'>
```

Yani Python type annotations ko runtime mein **metadata source** ki tarah use kar sakte ho.

---

# 24. `Annotated` + `get_type_hints()` = powerful combination

Ye architecture mein particularly useful hai.

```python
from dataclasses import dataclass
from typing import Annotated, get_type_hints


@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float


Airflow = Annotated[
    float,
    "CFM",
    Range(0, 5000)
]


class AHU:
    airflow: Airflow
```

Ab:

```python
hints = get_type_hints(
    AHU,
    include_extras=True
)
```

Framework metadata inspect kar sakta hai:

```text
Type:
float

Metadata:
"CFM"
Range(0, 5000)
```

Isse aap ek custom HVAC configuration/validation framework bana sakte ho.

---

# 25. Important security/performance point

`get_type_hints()` annotations ko resolve karta hai, aur complex forward references/imports involved ho sakte hain.

Isliye blindly arbitrary untrusted annotations ko process karna ideal nahi.

Aur high-frequency runtime path mein har call par:

```python
get_type_hints(...)
```

karna unnecessary overhead ho sakta hai.

Agar same function repeatedly inspect karna ho, to result cache karna sensible ho sakta hai.

Example:

```python
hints = get_type_hints(create_equipment)

# baad mein same hints reuse karo
```

---

# 26. Ek complete example

```python
from dataclasses import dataclass
from typing import Annotated, get_type_hints


@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float


Airflow = Annotated[
    float,
    "CFM",
    Range(0, 5000)
]


@dataclass
class AHU:
    equipment_id: str
    floor: int
    airflow: Airflow
```

Runtime inspection:

```python
hints = get_type_hints(
    AHU,
    include_extras=True
)

for field_name, field_type in hints.items():
    print(field_name, "=>", field_type)
```

Conceptually:

```text
equipment_id => str
floor        => int
airflow      => Annotated[float, "CFM", Range(...)]
```

Yahan:

```python
get_type_hints()
```

ne class ki type information runtime par accessible bana di.

---

# 27. Ek line mein pura concept

```python
get_type_hints(obj)
```

ka matlab:

> **"Is function/class ke type annotations ko runtime par resolve karke mujhe dictionary ki form mein do."**

---

## `Lesson 70` vs `Lesson 71`

```text
Lesson 70
reveal_type()
     ↓
Static Type Debugging
     ↓
"What does the type checker think?"


Lesson 71
get_type_hints()
     ↓
Runtime Type Introspection
     ↓
"What annotations does this object have?"
```

### Golden rule

Agar aap **type checker ka dimaag dekhna** chahte ho:

```python
reveal_type(x)
```

Agar aap **runtime program mein annotations read karna** chahte ho:

```python
get_type_hints(obj)
```

Aur agar `Annotated` ka metadata bhi runtime par chahiye:

```python
get_type_hints(obj, include_extras=True)
```

**Lesson 71 ka core concept:** `get_type_hints()` type hints ko sirf documentation nahi rehne deta—runtime code un annotations ko **inspect aur use** kar sakta hai.
Bilkul. Ab **Lesson 72 — `typing.get_args()` + `get_origin()` — Generic Introspection**.

Ye lesson **`get_type_hints()` ka natural next step** hai.

`get_type_hints()` se humein complete type milta hai, aur `get_origin()` + `get_args()` se hum us type ke **andar ki structure** inspect kar sakte hain.

---

# Lesson 72 — `get_args()` + `get_origin()`

## 1. Sab se pehle basic idea

Maan lo:

```python
list[int]
```

Ye sirf `list` nahi hai.

Ismein do pieces hain:

```text
list[int]
  ↓
origin = list
args   = int
```

Yahan:

```python
get_origin(list[int])
```

→ `list`

Aur:

```python
get_args(list[int])
```

→ `(int,)`

---

# 2. Import

```python
from typing import get_args, get_origin
```

Example:

```python
from typing import get_args, get_origin

T = list[int]

print(get_origin(T))
print(get_args(T))
```

Conceptually output:

```text
<class 'list'>
(<class 'int'>,)
```

---

# 3. `get_origin()` kya karta hai?

`get_origin()` poochta hai:

> **"Ye generic type kis base/original type se bani hai?"**

Example:

```python
list[int]
```

mein:

```python
get_origin(list[int])
```

→

```python
list
```

---

### Examples

```python
get_origin(list[int])
```

→ `list`

```python
get_origin(dict[str, int])
```

→ `dict`

```python
get_origin(tuple[str, int])
```

→ `tuple`

```python
get_origin(set[float])
```

→ `set`

Mental model:

```text
list[int]
   ↓
get_origin()
   ↓
list
```

---

# 4. `get_args()` kya karta hai?

`get_args()` poochta hai:

> **"Is generic type ke andar kaun se type parameters hain?"**

Example:

```python
get_args(list[int])
```

→

```python
(int,)
```

Aur:

```python
get_args(dict[str, float])
```

→

```python
(str, float)
```

Yani:

```text
dict[str, float]
       ↓
get_args()
       ↓
(str, float)
```

---

# 5. Dono ko saath samjho

Sabse important mental model:

```text
dict[str, int]
      │
      ├── origin → dict
      │
      └── args   → (str, int)
```

Aur:

```text
list[float]
     │
     ├── origin → list
     │
     └── args   → (float,)
```

---

# 6. `get_origin()` vs `get_args()`

| Function       | Sawal                                       |
| -------------- | ------------------------------------------- |
| `get_origin()` | Generic ka base kya hai?                    |
| `get_args()`   | Generic ke andar parameters/types kya hain? |

Example:

```python
T = dict[str, float]
```

```python
get_origin(T)
```

→ `dict`

```python
get_args(T)
```

→ `(str, float)`

---

# 7. Simple types par kya hota hai?

Agar:

```python
get_origin(int)
```

to generally:

```text
None
```

Aur:

```python
get_args(int)
```

→

```text
()
```

Kyun?

Kyunkay:

```python
int
```

generic parameterized type nahi hai.

Mental model:

```text
int
 ↓
origin = None
args   = ()
```

---

# 8. `list[int]` ko todna

Ye example deeply samjho:

```python
T = list[int]
```

Internally conceptual structure:

```text
list[int]
│
├── origin
│      ↓
│     list
│
└── args
       ↓
      int
```

Code:

```python
from typing import get_args, get_origin

T = list[int]

origin = get_origin(T)
args = get_args(T)

print(origin)
print(args)
```

Result:

```text
<class 'list'>
(<class 'int'>,)
```

---

# 9. `dict[str, int]`

```python
T = dict[str, int]

print(get_origin(T))
print(get_args(T))
```

Result:

```text
<class 'dict'>
(<class 'str'>, <class 'int'>)
```

Yahan:

```text
dict
 ↑
origin
```

aur:

```text
str, int
 ↑    ↑
args
```

---

# 10. `tuple`

Tuple interesting hai.

```python
T = tuple[str, int]
```

Then:

```python
get_origin(T)
```

→

```text
tuple
```

Aur:

```python
get_args(T)
```

→

```text
(str, int)
```

---

# 11. Variable-length tuple

```python
T = tuple[int, ...]
```

Ab:

```python
get_args(T)
```

→

```text
(int, Ellipsis)
```

Yahan `...` Python ka:

```python
Ellipsis
```

object hai.

Meaning:

```text
tuple[int, ...]
```

=

> kisi bhi length ka tuple jisme har element `int` ho.

So:

```text
origin → tuple

args →
(
    int,
    Ellipsis
)
```

---

# 12. `Union`

Ab powerful example:

```python
T = int | str
```

```python
get_args(T)
```

→

```text
(int, str)
```

Aur modern Python mein:

```python
get_origin(T)
```

generally:

```text
types.UnionType
```

dega.

Yani:

```text
int | str
   ↓
origin → UnionType
args   → (int, str)
```

---

# 13. `Optional`

`Optional[int]` actually:

```python
Optional[int]
```

conceptually:

```python
int | None
```

So:

```python
from typing import Optional, get_args, get_origin

T = Optional[int]

print(get_origin(T))
print(get_args(T))
```

Arguments conceptually:

```text
(int, NoneType)
```

Important:

```python
None
```

type parameter ke form mein:

```python
type(None)
```

ya:

```python
NoneType
```

represent hota hai.

---

# 14. `Annotated`

Yahan `get_args()` bohot interesting ho jata hai.

```python
from typing import Annotated, get_args, get_origin

T = Annotated[int, "Celsius"]
```

Ab:

```python
get_origin(T)
```

→

```text
Annotated
```

Aur:

```python
get_args(T)
```

→ conceptually:

```text
(int, "Celsius")
```

Yani:

```text
Annotated[int, "Celsius"]
        │
        ├── origin → Annotated
        │
        └── args
              ├── int
              └── "Celsius"
```

---

# 15. Multiple metadata

```python
T = Annotated[
    float,
    "CFM",
    "HVAC",
    "0-5000"
]
```

Then:

```python
get_args(T)
```

gives conceptually:

```text
(
    float,
    "CFM",
    "HVAC",
    "0-5000"
)
```

Notice:

> Pehla argument underlying type hai, baqi metadata.

---

# 16. `Literal`

```python
from typing import Literal

T = Literal["ON", "OFF"]
```

Then:

```python
get_origin(T)
```

→ `Literal`

Aur:

```python
get_args(T)
```

→

```text
("ON", "OFF")
```

Yahan args **types nahi**, actual literal values hain.

Ye important distinction hai.

---

# 17. `Callable`

Example:

```python
from collections.abc import Callable

T = Callable[[int, str], bool]
```

Conceptually:

```text
Callable
   │
   ├── arguments → [int, str]
   │
   └── return    → bool
```

`get_origin()`:

```text
collections.abc.Callable
```

aur `get_args()` structure ko expose karta hai.

Yani `get_args()` ko sirf simple `list[int]` ke liye nahi, **complex generic types** inspect karne ke liye bhi use kiya jata hai.

---

# 18. Nested generics

Ab important example:

```python
T = list[dict[str, int]]
```

Outer structure:

```text
list[
    dict[str, int]
]
```

### Origin

```python
get_origin(T)
```

→

```text
list
```

### Args

```python
get_args(T)
```

→

```text
(dict[str, int],)
```

Ab us argument ko dobara inspect karo:

```python
inner = get_args(T)[0]

get_origin(inner)
```

→

```text
dict
```

Aur:

```python
get_args(inner)
```

→

```text
(str, int)
```

---

# 19. Recursive introspection

Yahan se real power start hoti hai.

Aap recursively type structure inspect kar sakte ho:

```text
list[dict[str, int]]
       │
       └── dict[str, int]
              │
              ├── str
              └── int
```

Algorithm roughly:

```text
1. origin nikalo
2. args nikalo
3. har arg ko dobara inspect karo
4. jab args empty ho jayein → basic type
```

Ye schema generators aur validation frameworks mein useful technique hai.

---

# 20. Generic TypeVar

Suppose:

```python
from typing import TypeVar

T = TypeVar("T")
```

Ab:

```python
get_origin(T)
```

generally:

```text
None
```

Aur:

```python
get_args(T)
```

→

```text
()
```

Kyunke `T` khud parameterized generic expression nahi hai.

---

# 21. Generic class

Previous lessons mein:

```python
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(Generic[T]):
    ...
```

Ab:

```python
Repository[int]
```

inspect kar sakte ho.

```python
T = Repository[int]
```

Then conceptually:

```python
get_origin(T)
```

→

```text
Repository
```

Aur:

```python
get_args(T)
```

→

```text
(int,)
```

Yani:

```text
Repository[int]
       │
       ├── origin → Repository
       └── args   → (int,)
```

Ye **Generic introspection** ka exact example hai.

---

# 22. Iska practical faida kya hai?

Suppose framework ko ye type diya gaya:

```python
Repository[AHU]
```

Framework runtime par discover karna chahta hai:

> Repository kis type ke objects handle kar raha hai?

Use:

```python
origin = get_origin(Repository[AHU])
args = get_args(Repository[AHU])
```

Result conceptually:

```text
origin → Repository
args   → (AHU,)
```

Ab framework ko pata chal gaya:

```text
Repository → AHU
```

---

# 23. HVAC example

Maan lo:

```python
from typing import Generic, TypeVar

T = TypeVar("T")


class EquipmentRepository(Generic[T]):
    pass


class AHU:
    pass
```

Ab:

```python
repo_type = EquipmentRepository[AHU]
```

Inspect:

```python
from typing import get_args, get_origin

print(get_origin(repo_type))
print(get_args(repo_type))
```

Conceptually:

```text
EquipmentRepository
(AHU,)
```

Yani runtime tooling determine kar sakti hai:

```text
Repository ka entity type = AHU
```

---

# 24. `get_type_hints()` + `get_args()` + `get_origin()`

Ab previous lesson ke saath combine karte hain.

```python
from typing import get_type_hints


def process(data: list[dict[str, int]]) -> dict[str, float]:
    ...
```

Pehle:

```python
hints = get_type_hints(process)
```

Ab:

```python
data_type = hints["data"]
```

`data_type`:

```text
list[dict[str, int]]
```

Ab:

```python
get_origin(data_type)
```

→

```text
list
```

Aur:

```python
get_args(data_type)
```

→

```text
(dict[str, int],)
```

Phir inner:

```python
inner = get_args(data_type)[0]
```

Then:

```python
get_origin(inner)
```

→ `dict`

```python
get_args(inner)
```

→ `(str, int)`

---

# 25. Runtime schema generator ka concept

Ab imagine karo hum ek function bana rahe hain:

```python
def describe_type(tp):
    ...
```

Input:

```python
list[dict[str, int]]
```

Output:

```text
List
 └── Dict
      ├── Key: str
      └── Value: int
```

Is type of tooling ke foundation mein:

```python
get_origin()
get_args()
```

bohot important hain.

---

# 26. Simple introspection function

Concept samajhne ke liye:

```python
from typing import get_args, get_origin


def inspect_type(tp):
    origin = get_origin(tp)
    args = get_args(tp)

    print("Type:", tp)
    print("Origin:", origin)
    print("Args:", args)
```

Use:

```python
inspect_type(list[int])
```

Output conceptually:

```text
Type: list[int]
Origin: list
Args: (<class 'int'>,)
```

Aur:

```python
inspect_type(dict[str, float])
```

```text
Type: dict[str, float]
Origin: dict
Args: (<class 'str'>, <class 'float'>)
```

---

# 27. `get_origin()` aur `__origin__`

Aapko kabhi code mein:

```python
T.__origin__
```

ya:

```python
T.__args__
```

dikh sakta hai.

Lekin modern code mein generally prefer:

```python
get_origin(T)
get_args(T)
```

Kyun?

Kyunkay ye **public typing introspection API** hai aur different typing constructs ko consistently handle karne ke liye designed hai.

---

# 28. `typing.List` vs `list`

Old style:

```python
from typing import List

T = List[int]
```

Modern:

```python
T = list[int]
```

`get_origin()`/`get_args()` ke saath introspection karte waqt dono typing forms ko encounter karna possible hai, especially old codebases mein.

Isliye generic introspection code ko sirf:

```python
if tp is list:
```

jaisi assumptions par nahi banana chahiye.

---

# 29. `Union` aur `Annotated` ka difference

Dono mein `get_args()` use hota hai, lekin meaning different hai.

### Union

```python
int | str
```

```text
args → (int, str)
```

Meaning:

> Allowed alternatives.

### Annotated

```python
Annotated[int, "Celsius"]
```

```text
args → (int, "Celsius")
```

Meaning:

> Underlying type + metadata.

### Literal

```python
Literal["ON", "OFF"]
```

```text
args → ("ON", "OFF")
```

Meaning:

> Exact allowed values.

Isliye **sirf `get_args()` ka result dekhna enough nahi**; `get_origin()` se context samajhna hota hai.

---

# 30. Ye combination yaad rakho

```python
origin = get_origin(tp)
args = get_args(tp)
```

Phir:

```text
origin
  ↓
"What kind of typing construct is this?"

args
  ↓
"What parameters/data are inside it?"
```

---

# 31. Practical type parser

Ek simple conceptual parser:

```python
from typing import get_args, get_origin


def describe(tp):

    origin = get_origin(tp)
    args = get_args(tp)

    if origin is None:
        return str(tp)

    if origin is list:
        return f"List of {describe(args[0])}"

    if origin is dict:
        return (
            f"Dictionary with "
            f"{describe(args[0])} keys and "
            f"{describe(args[1])} values"
        )

    return str(tp)
```

Ab:

```python
describe(list[int])
```

→

```text
List of <class 'int'>
```

Aur:

```python
describe(dict[str, float])
```

→

```text
Dictionary with <class 'str'> keys and <class 'float'> values
```

Ye sirf demonstration hai, lekin isi idea ko complex frameworks mein much deeper banaya jata hai.

---

# 32. `Annotated` runtime framework example

Maan lo:

```python
from typing import Annotated

Airflow = Annotated[
    float,
    "CFM",
    "0-5000"
]
```

Ab:

```python
origin = get_origin(Airflow)
args = get_args(Airflow)
```

Conceptually:

```text
origin → Annotated

args →
(
    float,
    "CFM",
    "0-5000"
)
```

Framework:

```python
base_type = args[0]
metadata = args[1:]
```

Ab:

```text
base_type → float
metadata  → ("CFM", "0-5000")
```

Ye previous Lesson 71 ke `include_extras=True` concept ka natural extension hai.

---

# 33. `get_args()` ka ek important rule

`get_args()` ka result **always "types" nahi hota**.

Examples:

```python
get_args(list[int])
```

→ types

```python
get_args(Literal["ON", "OFF"])
```

→ values

```python
get_args(Annotated[int, "CFM"])
```

→ type + metadata

```python
get_args(tuple[int, ...])
```

→ type + `Ellipsis`

Isliye:

> `get_args()` ko "generic ke andar jo parameters hain" samjho, sirf "types" nahi.

---

# 34. `get_origin()` ka bhi important rule

`get_origin()` hamesha simple class return nahi karta.

Different typing constructs mein result different ho sakta hai.

Examples conceptually:

```text
list[int]
    → list

dict[str, int]
    → dict

int | str
    → UnionType

Annotated[int, ...]
    → Annotated

Literal["ON"]
    → Literal
```

Isliye introspection code ko construct-specific logic ki zarurat pad sakti hai.

---

# 35. Lesson 70, 71, 72 ko ek saath dekho

Ab teen lessons connect ho rahe hain:

### Lesson 70

```python
reveal_type(x)
```

**Static debugging**

> Type checker x ko kya samajhta hai?

### Lesson 71

```python
get_type_hints(func)
```

**Runtime annotation inspection**

> Function/class ki annotations kya hain?

### Lesson 72

```python
get_origin(tp)
get_args(tp)
```

**Type structure inspection**

> Is annotation ke andar structure kya hai?

---

# Final mental model

```text
                    TYPE SYSTEM
                         │
                         ▼
                get_type_hints()
                         │
                         ▼
                  list[dict[str, int]]
                         │
                 ┌───────┴───────┐
                 ▼               ▼
           get_origin()      get_args()
                 │               │
                 ▼               ▼
                list       dict[str, int]
                                 │
                          get_origin()
                                 ↓
                                dict
                                 │
                           get_args()
                                 ↓
                            (str, int)
```

### Golden rule:

```python
get_origin(tp)
```

= **outer/base typing construct**

```python
get_args(tp)
```

= **us construct ke andar ke parameters**

Aur jab dono ko `get_type_hints()` ke saath combine karte ho, to aap Python ke **runtime type structure ko programmatically inspect** kar sakte ho.

**Practical applications:** schema generators, runtime validators, serializers, dependency-injection systems, API frameworks, generic repositories, aur custom typing-aware frameworks.
Bilkul. Ab **Lesson 73 — `typing.NewType` — Distinct Type Aliases**.

Ye topic `TypeAlias` se related hai, lekin **dono ka purpose fundamentally different** hai.

---

# Lesson 73 — `typing.NewType`

## 1. Sab se pehle basic idea

Maan lo hamare paas:

```python
equipment_id: str
floor: str
```

Dono `str` hain.

Problem ye hai ke logically dono alag cheezen hain:

```text
Equipment ID ≠ Floor
```

Lekin normal Python typing mein:

```python
EquipmentID = str
Floor = str
```

dono basically same type hain.

`NewType` ka purpose hai:

> **Existing type ke upar ek distinct static type identity banana.**

---

# 2. Basic syntax

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
```

Ab:

```python
equipment_id = EquipmentID("AHU-001")
```

Yahan:

```text
EquipmentID
    ↓
based on str
```

Lekin static type checker ke nazdeek:

```text
EquipmentID
```

ek distinct type hai.

---

# 3. Simple example

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)

equipment_id = EquipmentID("AHU-001")

print(equipment_id)
```

Runtime value:

```text
AHU-001
```

Lekin type checker ke liye:

```text
EquipmentID
```

hai.

---

# 4. `NewType` ka main purpose

Maan lo:

```python
UserID = NewType("UserID", int)
OrderID = NewType("OrderID", int)
```

Dono underlying type:

```text
int
```

hain.

Lekin logically:

```text
UserID ≠ OrderID
```

Ab function:

```python
def get_user(user_id: UserID):
    ...
```

Agar accidentally:

```python
order_id = OrderID(100)

get_user(order_id)
```

to static type checker warning/error de sakta hai.

Ye **NewType ka sabse important faida** hai.

---

# 5. Normal type alias se difference

Ye bohot important hai.

### Type alias

```python
EquipmentID = str
```

Meaning:

```text
EquipmentID = str
```

Bas ek doosra naam.

### NewType

```python
EquipmentID = NewType("EquipmentID", str)
```

Meaning:

```text
EquipmentID
     ↓
distinct static type
     ↓
underlying type = str
```

Comparison:

```text
TypeAlias
    ↓
same type, different name

NewType
    ↓
different static type identity
```

---

# 6. Ye difference practical kyun hai?

Suppose:

```python
def move_equipment(
    equipment_id: EquipmentID,
    floor: FloorNumber
):
    ...
```

Definitions:

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
FloorNumber = NewType("FloorNumber", int)
```

Ab:

```python
equipment_id = EquipmentID("AHU-001")
floor = FloorNumber(34)

move_equipment(equipment_id, floor)
```

Correct.

Lekin:

```python
move_equipment(floor, equipment_id)
```

static type checker ko problem milegi.

Kyun?

Because:

```text
EquipmentID ≠ FloorNumber
```

even though underlying values are:

```text
str
int
```

---

# 7. Real-world "wrong value, right base type" problem

Ye NewType ka real benefit hai.

Suppose:

```python
UserID = NewType("UserID", int)
EquipmentID = NewType("EquipmentID", int)
```

Agar NewType na hota:

```python
def get_equipment(equipment_id: int):
    ...
```

To:

```python
user_id = 100
get_equipment(user_id)
```

perfectly valid lagta.

Lekin business logic mein:

```text
UserID 100
```

aur:

```text
EquipmentID 100
```

completely different concepts hain.

NewType static checker ko ye distinction samjhata hai.

---

# 8. HVAC example

Facility-management system mein:

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)
FloorID = NewType("FloorID", int)
```

Ab:

```python
equipment_id = EquipmentID("MEP-AHU-001")
work_order_id = WorkOrderID("WO-2026-1001")
floor_id = FloorID(34)
```

Functions:

```python
def close_work_order(work_order_id: WorkOrderID):
    ...


def get_equipment(equipment_id: EquipmentID):
    ...


def get_floor(floor_id: FloorID):
    ...
```

Ab accidentally:

```python
get_equipment(work_order_id)
```

static checker ko wrong lagega.

Ye large systems mein **domain-level safety** provide karta hai.

---

# 9. Runtime par kya hota hai?

Yahan ek very important point:

`NewType` **runtime mein new class nahi banata**.

Example:

```python
EquipmentID = NewType("EquipmentID", str)

x = EquipmentID("AHU-001")
```

Runtime par `x` effectively `str` hi hai.

```python
print(type(x))
```

generally:

```text
<class 'str'>
```

Yani:

```text
NewType
   ↓
static distinction
   ↓
runtime new class nahi
```

---

# 10. Ye `class` nahi hai

Agar aap likho:

```python
class EquipmentID(str):
    pass
```

to actual runtime class create hoti hai.

Lekin:

```python
EquipmentID = NewType("EquipmentID", str)
```

mein actual subclass object/class hierarchy create nahi hoti.

Comparison:

```text
NewType
    → static typing distinction

class EquipmentID(str)
    → actual runtime class
```

---

# 11. `NewType` function ki tarah dikhta hai

Ye:

```python
EquipmentID("AHU-001")
```

dekhne mein constructor jaisa lagta hai.

Lekin iska purpose conversion nahi.

Aap:

```python
value = EquipmentID("AHU-001")
```

karte ho.

Underlying runtime value still string hai.

---

# 12. `NewType` conversion nahi karta

Suppose:

```python
EquipmentID = NewType("EquipmentID", str)
```

Aap:

```python
EquipmentID(100)
```

ko normal runtime conversion:

```text
100 → "100"
```

samajhne ki galti mat karna.

`NewType`:

```text
str conversion
```

nahi karta.

Ye:

```text
type distinction
```

ke liye hai.

---

# 13. `NewType` vs `cast()`

Ye bhi important comparison hai.

### `NewType`

```python
EquipmentID = NewType("EquipmentID", str)
```

Aap **new distinct static type define** kar rahe ho.

### `cast()`

```python
from typing import cast

equipment_id = cast(EquipmentID, value)
```

Aap existing value ko checker se keh rahe ho:

> "Is value ko EquipmentID samjho."

Yani:

```text
NewType
    ↓
type define karta hai

cast
    ↓
existing value ka static type assert karta hai
```

---

# 14. `NewType` vs `TypeAlias`

Ye Lesson 67 se connect hota hai.

### Type Alias

```python
type EquipmentID = str
```

Meaning:

```text
EquipmentID
      ↓
same as str
```

No distinct type identity.

### NewType

```python
EquipmentID = NewType("EquipmentID", str)
```

Meaning:

```text
EquipmentID
      ↓
distinct static type
      ↓
based on str
```

---

# 15. Ek table

| Feature                         | Type Alias      | NewType               | Subclass        |
| ------------------------------- | --------------- | --------------------- | --------------- |
| Syntax                          | `type ID = str` | `NewType(...)`        | `class ID(str)` |
| Distinct static type            | ❌               | ✅                     | ✅               |
| New runtime class               | ❌               | ❌                     | ✅               |
| Runtime behavior                | Same            | Same underlying value | Customizable    |
| Methods add kar sakte?          | ❌               | ❌                     | ✅               |
| Lightweight domain distinction  | ❌               | ✅                     | Possible        |
| Runtime `isinstance()` identity | ❌               | ❌                     | ✅               |

---

# 16. `isinstance()` ke saath

Ye important limitation hai.

Suppose:

```python
EquipmentID = NewType("EquipmentID", str)
```

Aap:

```python
x = EquipmentID("AHU-001")
```

karte ho.

Runtime par:

```python
isinstance(x, str)
```

→ `True`

Lekin:

```python
isinstance(x, EquipmentID)
```

use normal runtime class ki tarah treat nahi kar sakte.

Kyunke `EquipmentID` actual runtime class nahi hai.

---

# 17. `NewType` + functions

Good architecture example:

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)


def load_equipment(
    equipment_id: EquipmentID
):
    print(equipment_id)
```

Use:

```python
equipment_id = EquipmentID("AHU-001")

load_equipment(equipment_id)
```

Type-safe domain boundary.

---

# 18. Wrong type example

```python
WorkOrderID = NewType("WorkOrderID", str)
EquipmentID = NewType("EquipmentID", str)


def get_equipment(equipment_id: EquipmentID):
    ...
```

Then:

```python
work_order_id = WorkOrderID("WO-1001")

get_equipment(work_order_id)
```

Runtime par dono strings ho sakte hain.

Lekin static checker ke liye:

```text
WorkOrderID
     ≠
EquipmentID
```

Ye exactly woh safety hai jo simple alias provide nahi karta.

---

# 19. Generic ke saath

NewType ko Generic concepts ke saath bhi combine kiya ja sakta hai.

```python
from typing import Generic, NewType, TypeVar

EquipmentID = NewType("EquipmentID", str)

T = TypeVar("T")


class Repository(Generic[T]):

    def get(self, item_id: T) -> T:
        ...
```

Ab:

```python
repo = Repository[EquipmentID]()
```

Conceptually:

```text
Repository
    ↓
EquipmentID
```

Type system domain relationship preserve kar sakta hai.

---

# 20. NewType ka best use: Domain-Driven Design

Ye concept **Domain-Driven Design (DDD)** mein especially useful hai.

Normal primitive types:

```python
str
int
float
```

business meaning lose kar dete hain.

Example:

```python
def transfer(
    source_account: int,
    destination_account: int,
    amount: float
):
    ...
```

Problem:

```text
int → account ID?
int → user ID?
int → invoice ID?
```

Sab same primitive hain.

NewType:

```python
AccountID = NewType("AccountID", int)
UserID = NewType("UserID", int)
InvoiceID = NewType("InvoiceID", int)
```

Ab domain language type system mein aa jati hai.

---

# 21. Banking example

```python
from typing import NewType

AccountID = NewType("AccountID", int)
CustomerID = NewType("CustomerID", int)
```

Function:

```python
def get_account(
    customer_id: CustomerID,
    account_id: AccountID
):
    ...
```

Ab:

```python
customer = CustomerID(10)
account = AccountID(500)

get_account(customer, account)
```

Correct.

Accidental:

```python
get_account(account, customer)
```

static checker detect kar sakta hai.

---

# 22. API example

Suppose API returns:

```python
{
    "equipment_id": "MEP-AHU-001",
    "work_order_id": "WO-1001"
}
```

Dono:

```text
str
```

hain.

Lekin internal application:

```python
EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)
```

use kar sakti hai.

Boundary par:

```text
API JSON
   ↓
str
   ↓
NewType
   ↓
domain layer
```

Ab internal code mein accidental mixing kam hoti hai.

---

# 23. `NewType` runtime validation nahi karta

Ye bahut important warning hai.

```python
EquipmentID = NewType("EquipmentID", str)

equipment_id = EquipmentID(123)
```

NewType khud ye guarantee nahi deta ke:

```text
123
```

valid equipment ID hai.

Ye sirf static typing construct hai.

Agar actual validation chahiye:

```python
if not isinstance(value, str):
    raise TypeError(...)
```

ya proper validation library/domain class use karo.

---

# 24. `NewType` aur `Annotated`

Dono ko confuse mat karo.

### NewType

```python
EquipmentID = NewType("EquipmentID", str)
```

Meaning:

> `EquipmentID` ek distinct static type hai.

### Annotated

```python
EquipmentID = Annotated[str, "Equipment ID"]
```

Meaning:

> `str` ke saath metadata attach hai.

So:

```text
NewType
   ↓
identity distinction

Annotated
   ↓
metadata
```

---

# 25. `NewType` aur `Literal`

Ye bhi different hain.

```python
Status = Literal["ON", "OFF"]
```

Meaning:

> Sirf ye exact values allowed hain.

Whereas:

```python
EquipmentID = NewType("EquipmentID", str)
```

Meaning:

> Ye string domain-wise EquipmentID hai.

So:

```text
Literal
   ↓
allowed values

NewType
   ↓
semantic/domain type
```

---

# 26. `NewType` aur dataclass

Agar aapko sirf semantic identity chahiye:

```python
EquipmentID = NewType("EquipmentID", str)
```

Agar aapko actual behavior/validation chahiye:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class EquipmentID:
    value: str
```

Dataclass/class ka benefit:

```text
methods
validation
custom behavior
runtime identity
```

NewType ka benefit:

```text
lightweight
static-only distinction
underlying runtime value same
```

---

# 27. Kab NewType use karna chahiye?

Good candidates:

```text
UserID
CustomerID
EquipmentID
WorkOrderID
InvoiceID
AccountID
ProductCode
SerialNumber
```

Jab:

1. Underlying type simple ho.
2. Runtime behavior ki zarurat na ho.
3. Different domain concepts accidentally mix ho sakte hon.
4. Static type checking se safety chahiye.

---

# 28. Kab NewType nahi use karna chahiye?

Agar aapko:

* runtime validation
* custom methods
* custom operators
* parsing
* formatting behavior
* invariants
* complex state

chahiye, to actual class/value object better ho sakta hai.

Example:

```python
class Temperature:
    ...
```

instead of:

```python
Temperature = NewType("Temperature", float)
```

Agar temperature ko validate karna hai:

```text
-273.15°C se neeche allowed nahi
```

to actual domain class zyada suitable ho sakti hai.

---

# 29. `NewType` ka deep mental model

Normal:

```python
str
```

sirf technical type batata hai:

```text
"ye text hai"
```

NewType:

```python
EquipmentID = NewType("EquipmentID", str)
```

type system ko semantic meaning deta hai:

```text
"ye text hai"
        +
"ye Equipment ID hai"
```

Isi liye NewType ko **domain semantics for primitive values** ke liye powerful samjho.

---

# 30. Complete HVAC example

```python
from typing import NewType


EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)
FloorNumber = NewType("FloorNumber", int)


def get_equipment(equipment_id: EquipmentID):
    print(f"Loading {equipment_id}")


def close_work_order(work_order_id: WorkOrderID):
    print(f"Closing {work_order_id}")


def get_floor(floor: FloorNumber):
    print(f"Floor {floor}")
```

Correct:

```python
equipment_id = EquipmentID("MEP-AHU-001")
work_order_id = WorkOrderID("WO-2026-001")
floor = FloorNumber(34)

get_equipment(equipment_id)
close_work_order(work_order_id)
get_floor(floor)
```

Accidental:

```python
get_equipment(work_order_id)
```

Static checker ko batayega:

```text
Expected:
EquipmentID

Got:
WorkOrderID
```

Yahi NewType ka practical value hai.

---

# 31. Lesson 67 se connection

Humne pehle padha tha:

```python
type EquipmentID = str
```

Ye:

```text
Type Alias
```

hai.

Ab:

```python
EquipmentID = NewType("EquipmentID", str)
```

Ye:

```text
Distinct Static Type
```

hai.

### Mental shortcut:

```text
type EquipmentID = str
        ↓
"str ka nickname"

NewType("EquipmentID", str)
        ↓
"str-based new domain identity"
```

---

# 32. Final comparison

```text
str
 │
 ├── Type Alias
 │      type EquipmentID = str
 │      ↓
 │      same type
 │
 ├── NewType
 │      EquipmentID = NewType("EquipmentID", str)
 │      ↓
 │      distinct static type
 │
 └── Class
        class EquipmentID(str)
        ↓
        actual runtime type
```

### Golden rule

**`TypeAlias`**:

> "Ye existing type ka doosra naam hai."

**`NewType`**:

> "Ye existing type par based ek distinct static domain type hai."

**Class**:

> "Ye actual runtime object/type hai."

Aur NewType ka sabse bada faida:

> **`UserID`, `EquipmentID`, `WorkOrderID`, `InvoiceID` jaise same-underlying-type values ko accidentally mix hone se static type checker ke through rokna.**
Bilkul. Ab **Lesson 74 — `typing.NoReturn` vs `Never` — Deeply**.

Ye dono dekhne mein almost same lagte hain, lekin **type-system mein inka role different hai**.

---

# Lesson 74 — `NoReturn` vs `Never`

## 1. Sabse pehle core idea

Dono ka relation un situations se hai jahan **normal value return nahi hoti**.

Lekin:

```python
NoReturn
```

ka main meaning hai:

> **Ye function normally return nahi karta.**

Jabke:

```python
Never
```

ka deeper meaning hai:

> **Ye type-level impossible/empty type hai — is type ka koi valid value nahi hota.**

Simple mental model:

```text
NoReturn
   ↓
Function behavior
"ye function return nahi karega"

Never
   ↓
Type-system concept
"yahan koi possible value/type nahi"
```

---

# 2. `NoReturn` basic example

```python
from typing import NoReturn


def stop_program() -> NoReturn:
    raise RuntimeError("Program stopped")
```

Function:

```python
stop_program()
```

kabhi normal:

```python
return value
```

nahi karega.

Iska reason:

```python
raise RuntimeError(...)
```

hai.

---

# 3. `NoReturn` ka naam confusing kyun hai?

`NoReturn` ka matlab:

> "Function ka return type `None` hai"

**nahi**.

Ye:

```python
NoReturn
```

aur:

```python
None
```

completely different hain.

### `None`

Function successfully return kar sakta hai:

```python
def log_message() -> None:
    print("Done")
```

Flow:

```text
function
   ↓
successfully complete
   ↓
None
```

### `NoReturn`

```python
def fail() -> NoReturn:
    raise RuntimeError()
```

Flow:

```text
function
   ↓
exception / infinite loop / termination
   ↓
normal return kabhi nahi
```

---

# 4. `None` vs `NoReturn`

Ye distinction pakka yaad karo:

```text
None
    ↓
"return value nahi hai"

NoReturn
    ↓
"normal return hota hi nahi"
```

Example:

```python
def save() -> None:
    print("Saved")
```

Ye complete hota hai.

Lekin:

```python
def fatal_error() -> NoReturn:
    raise RuntimeError()
```

ye complete nahi hota.

---

# 5. `NoReturn` ka static type checker mein role

Ye sirf documentation nahi.

Type checker ko flow information milti hai.

Example:

```python
from typing import NoReturn


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def process(value: int | None) -> int:
    if value is None:
        fail("Value missing")

    return value
```

Yahan type checker samajh sakta hai:

```text
value is None
      ↓
fail()
      ↓
function does not return
      ↓
remaining path par value != None
```

Isliye:

```python
return value
```

safe/narrowed ho sakta hai.

---

# 6. Control-flow perspective

Isko flow diagram se dekho:

```text
             value
               │
        ┌──────┴──────┐
        │             │
      None           int
        │             │
      fail()        return
        │
        X
```

`fail()` ke baad execution normally continue nahi hoti.

`NoReturn` type checker ko ye batata hai.

---

# 7. Common `NoReturn` functions

Typical examples:

### Exception raiser

```python
def panic() -> NoReturn:
    raise RuntimeError()
```

### Fatal error handler

```python
def fatal(message: str) -> NoReturn:
    raise SystemExit(message)
```

### Infinite loop

```python
def run_forever() -> NoReturn:
    while True:
        pass
```

Theoretically ye bhi normal return nahi karta.

---

# 8. Important: `NoReturn` function ke andar `return` nahi hona chahiye

Ye logically wrong hai:

```python
def fail() -> NoReturn:
    return
```

Kyun?

`NoReturn` ka contract hi hai:

```text
normal return impossible
```

Agar function normal return karta hai to annotation ka meaning violate hota hai.

---

# 9. Ab `Never`

Modern Python typing mein:

```python
from typing import Never
```

`Never` ko samajhne ke liye **empty type** ka concept samjho.

Suppose type:

```python
str | int
```

possible values:

```text
str
int
```

Lekin:

```python
Never
```

mein:

```text
possible values = 0
```

Yani:

```text
Never = empty set of values
```

---

# 10. Mathematical mental model

Type ko set of possible values samjho.

```text
int
↓
{all possible integers}

str
↓
{all possible strings}

Never
↓
{}
```

`Never` ka set empty hai.

Isliye `Never` ko:

> **bottom type**

bhi kaha jata hai.

---

# 11. Top type vs bottom type

Typing theory mein useful concept:

```text
Any
 ↓
bohot broad / almost anything

object
 ↓
all normal Python objects

...

Never
 ↓
empty / impossible
```

Conceptually:

```text
       Any
        │
      object
        │
   many types
        │
       ...
        │
      Never
```

Lekin `Any` aur `Never` ko simple hierarchy mein literally opposite endpoints samajhna oversimplification ho sakta hai. Important idea ye hai:

```text
Any   → type information ko relax karta hai
Never → possible values ko zero kar deta hai
```

---

# 12. `Never` as impossible branch

Example:

```python
from typing import Never


def impossible(value: Never) -> Never:
    raise AssertionError("Impossible")
```

Agar kisi point par type checker kehta hai:

```text
value: Never
```

to iska meaning hai:

> Is point tak valid execution mein value exist nahi kar sakti.

---

# 13. Exhaustiveness checking

`Never` ka ek powerful use **exhaustive handling** hai.

Suppose:

```python
from typing import Literal


Status = Literal["ON", "OFF"]
```

Function:

```python
def handle_status(status: Status):
    if status == "ON":
        print("Running")
    elif status == "OFF":
        print("Stopped")
```

Agar hum prove karna chahte hain ke koi third case possible nahi:

```python
from typing import Never


def assert_never(value: Never) -> Never:
    raise AssertionError(f"Unexpected value: {value}")
```

Then:

```python
def handle_status(status: Status):
    if status == "ON":
        print("Running")

    elif status == "OFF":
        print("Stopped")

    else:
        assert_never(status)
```

Type checker ko pata hai:

```text
status:
"ON" | "OFF"
```

`ON` handle ho gaya.

`OFF` handle ho gaya.

Remaining:

```text
Never
```

Isliye:

```python
assert_never(status)
```

valid hai.

---

# 14. Agar third status add kar dein?

Suppose:

```python
Status = Literal["ON", "OFF", "FAULT"]
```

Ab function:

```python
def handle_status(status: Status):
    if status == "ON":
        print("Running")

    elif status == "OFF":
        print("Stopped")

    else:
        assert_never(status)
```

Ab type checker complain karega.

Kyun?

Because `else` mein:

```text
status = "FAULT"
```

possible hai.

Aur:

```python
assert_never()
```

sirf:

```text
Never
```

accept karta hai.

Ye **exhaustiveness checking** hai.

---

# 15. HVAC example

Ye aapke HVAC context mein bohot useful hai.

```python
from typing import Literal, Never


HVACState = Literal[
    "RUNNING",
    "STOPPED",
    "FAULT"
]


def assert_never(value: Never) -> Never:
    raise AssertionError(f"Unexpected state: {value}")
```

Handler:

```python
def handle_state(state: HVACState):

    if state == "RUNNING":
        print("AHU running")

    elif state == "STOPPED":
        print("AHU stopped")

    elif state == "FAULT":
        print("AHU fault")

    else:
        assert_never(state)
```

Ab agar future mein:

```python
HVACState = Literal[
    "RUNNING",
    "STOPPED",
    "FAULT",
    "MAINTENANCE"
]
```

add kiya aur handler update nahi kiya, static checker missing case identify kar sakta hai.

Ye large systems mein valuable hai.

---

# 16. `match` ke saath `Never`

Previous lesson mein humne `match/case` padha tha.

Ab dono concepts combine karo.

```python
from typing import Literal, Never


HVACState = Literal[
    "RUNNING",
    "STOPPED",
    "FAULT"
]


def assert_never(value: Never) -> Never:
    raise AssertionError(f"Unexpected value: {value}")
```

Then:

```python
def handle_state(state: HVACState):

    match state:

        case "RUNNING":
            print("Running")

        case "STOPPED":
            print("Stopped")

        case "FAULT":
            print("Fault")

        case _:
            assert_never(state)
```

Concept:

```text
RUNNING → handled
STOPPED → handled
FAULT   → handled
other   → Never
```

Agar type checker correctly narrow karta hai, `_` branch mein `state` `Never` ban sakta hai.

---

# 17. `Never` ka deeper meaning

Yahan ek subtle concept hai.

Agar:

```python
x: Never
```

hai, to iska matlab ye nahi:

> "x ki value `None` hai."

Balki:

> **"Valid program state mein x ka koi possible value nahi."**

Difference:

```text
None
↓
one specific value

Never
↓
zero possible values
```

---

# 18. `NoReturn` aur `Never` ka historical relationship

Purane Python typing code mein:

```python
NoReturn
```

mainly functions ke liye use hota tha:

```python
def fatal() -> NoReturn:
    ...
```

Modern typing mein:

```python
Never
```

more general bottom type hai.

Isliye modern code mein aapko:

```python
Never
```

functions ke return annotation mein bhi mil sakta hai:

```python
def fatal() -> Never:
    raise RuntimeError()
```

Aur:

```python
Never
```

parameters ke liye bhi use ho sakta hai:

```python
def impossible(value: Never) -> Never:
    ...
```

Yahi major conceptual difference hai.

---

# 19. Same function with `NoReturn` and `Never`

```python
from typing import NoReturn, Never


def fatal_old_style() -> NoReturn:
    raise RuntimeError()


def fatal_modern_style() -> Never:
    raise RuntimeError()
```

Dono ka practical intent:

```text
normal return nahi hota
```

Lekin typing semantics mein `Never` **general bottom type** hai.

---

# 20. `NoReturn` vs `Never` — key distinction

### `NoReturn`

Focus:

```text
function control flow
```

Meaning:

> Function normally return nahi karta.

### `Never`

Focus:

```text
type theory / impossible type
```

Meaning:

> Koi value is type ki ho hi nahi sakti.

---

# 21. Ek important subtlety

Ye kehna:

```text
NoReturn = old name
Never = new name
```

**poori tarah accurate nahi hai.**

Better:

```text
NoReturn
   ↓
non-returning function annotation

Never
   ↓
bottom / impossible type
```

Modern typing mein `Never` broader concept hai.

---

# 22. Function parameter mein `Never`

Ye interesting example hai:

```python
from typing import Never


def impossible_argument(value: Never):
    ...
```

Kis valid value ko pass karoge?

```text
int ❌
str ❌
None ❌
object ❌
```

Because:

```text
Never = no valid values
```

Aisi function usually **exhaustiveness checking** ke liye useful hoti hai.

---

# 23. `assert_never()` pattern

Aap reusable helper bana sakte ho:

```python
from typing import Never


def assert_never(value: Never) -> Never:
    raise AssertionError(
        f"Unhandled value: {value!r}"
    )
```

Phir:

```python
from typing import Literal

Mode = Literal[
    "AUTO",
    "MANUAL"
]


def process(mode: Mode):

    if mode == "AUTO":
        print("Automatic")

    elif mode == "MANUAL":
        print("Manual")

    else:
        assert_never(mode)
```

Iska purpose:

```text
future changes
       ↓
new Literal value
       ↓
unhandled branch
       ↓
static checker warning
```

---

# 24. `Never` aur `NoReturn` flow diagram

### `NoReturn`

```text
function call
     │
     ▼
  operation
     │
     ├── raise ──────── X
     │
     └── infinite loop X

normal return
     ↓
    never
```

### `Never`

```text
Type space
     │
     ├── int
     ├── str
     ├── None
     └── ...
     
Never
  ↓
empty set
  ↓
no possible value
```

---

# 25. `None` vs `NoReturn` vs `Never`

Ye teenon ek saath yaad karo:

| Type       | Meaning                                           |
| ---------- | ------------------------------------------------- |
| `None`     | Function successfully returns no meaningful value |
| `NoReturn` | Function normally return nahi karta               |
| `Never`    | Koi valid value exist nahi karti                  |

Example:

```python
def log() -> None:
    print("Done")
```

```python
def fatal() -> NoReturn:
    raise RuntimeError()
```

```python
def assert_never(value: Never) -> Never:
    raise AssertionError()
```

---

# 26. `Never` aur `NoReturn` ko Generic context mein samjho

Suppose:

```python
def process(value: int | str):
    ...
```

Narrowing ke baad agar type checker determine kar leta hai:

```text
value = int
```

ya:

```text
value = str
```

aur koi third possibility nahi bachi, remaining type conceptually:

```text
Never
```

ho sakti hai.

Yani `Never` **type narrowing ka endpoint** ban sakta hai.

```text
int | str
   │
   ├── int handled
   └── str handled
          ↓
       remaining
          ↓
        Never
```

---

# 27. `Never` = impossible branch

Ye sentence yaad rakho:

> **`Never` aksar type narrowing ke baad "ab kuch bhi possible nahi bacha" ko represent karta hai.**

Isi wajah se:

```python
assert_never(value)
```

pattern powerful hai.

---

# 28. `NoReturn` = impossible continuation

Aur:

> **`NoReturn` aksar function ke baad "execution continue nahi hogi" ko represent karta hai.**

Compare:

```text
Never
 ↓
"No value is possible"

NoReturn
 ↓
"No normal return is possible"
```

Ye dono concepts ko confuse nahi karna.

---

# 29. Exception handling example

```python
from typing import NoReturn


def raise_error(message: str) -> NoReturn:
    raise ValueError(message)


def get_temperature(value: float | None) -> float:

    if value is None:
        raise_error("Temperature missing")

    return value
```

Static checker ko pata hai:

```text
value = None
      ↓
raise_error()
      ↓
NoReturn
      ↓
path ends
```

remaining path:

```text
value = float
```

isliye:

```python
return value
```

safe hai.

---

# 30. Modern style

Agar aap modern Python typing likh rahe ho, to non-returning function ke liye `Never` bhi use kiya ja sakta hai:

```python
from typing import Never


def raise_error(message: str) -> Never:
    raise ValueError(message)
```

Lekin existing code/documentation mein:

```python
NoReturn
```

abhi bhi important hai, aur aapko dono concepts samajhne chahiye.

---

# 31. `Never` ko `NoReturn` ka replacement samajhna?

Partially, but carefully.

Function:

```python
def fatal() -> Never:
    raise RuntimeError()
```

valid modern typing style ho sakta hai.

Lekin conceptual reason ye nahi hona chahiye:

> "Never bas NoReturn ka new spelling hai."

Better:

```text
NoReturn
    → non-returning function concept

Never
    → bottom type
    → impossible values
    → impossible branches
    → exhaustive checking
    → non-returning function return type
```

---

# 32. Real architecture example

Suppose building-management system mein states:

```python
from typing import Literal, Never

EquipmentState = Literal[
    "RUNNING",
    "STOPPED",
    "ALARM",
    "MAINTENANCE"
]
```

Handler:

```python
def assert_never(value: Never) -> Never:
    raise AssertionError(
        f"Unknown equipment state: {value}"
    )


def handle_equipment_state(
    state: EquipmentState
):

    match state:

        case "RUNNING":
            print("Normal operation")

        case "STOPPED":
            print("Equipment stopped")

        case "ALARM":
            print("Alarm active")

        case "MAINTENANCE":
            print("Maintenance mode")

        case _:
            assert_never(state)
```

Ab future mein:

```python
EquipmentState = Literal[
    "RUNNING",
    "STOPPED",
    "ALARM",
    "MAINTENANCE",
    "OFFLINE"
]
```

add kar diya.

Agar handler mein `OFFLINE` add nahi kiya, type checker exhaustive handling issue identify kar sakta hai.

Ye large codebases mein bohot valuable hai.

---

# 33. `match` + `Never` ka architecture benefit

Without exhaustive checking:

```text
New state added
      ↓
Compiler/type checker
      ↓
maybe no warning
      ↓
runtime bug
```

With `Never` pattern:

```text
New state added
      ↓
unhandled branch
      ↓
assert_never()
      ↓
type checker warning
      ↓
developer fixes handler
```

Yani `Never` **future maintenance safety** improve kar sakta hai.

---

# 34. `NoReturn` ka architecture benefit

Centralized error function:

```python
def fatal(message: str) -> NoReturn:
    raise RuntimeError(message)
```

Phir:

```python
def process_equipment(data):

    if not data:
        fatal("Equipment data missing")

    # type checker understands:
    # fatal() never returns

    ...
```

Isse control-flow analysis accurate hoti hai.

---

# 35. Most important comparison

```text
                  NoReturn
                     │
                     ▼
            Function-level concept
                     │
            "Normal return nahi"
                     │
                     │
                     ▼
                  Never
                     │
                     ▼
             Type-level concept
                     │
        "No possible valid value"
```

Lekin ye diagram exact subtype hierarchy nahi batata; sirf conceptual relationship samjhata hai.

---

# 36. One-line definitions

### `NoReturn`

> **Ye function normal execution mein kabhi return nahi karta.**

### `Never`

> **Ye bottom type hai jisme koi possible valid value nahi hoti.**

---

# 37. Final cheat sheet

```python
from typing import NoReturn, Never
```

### Function that never returns

```python
def fatal() -> NoReturn:
    raise RuntimeError()
```

### Impossible value/branch

```python
def assert_never(value: Never) -> Never:
    raise AssertionError(value)
```

### Exhaustive checking

```python
match state:
    case "ON":
        ...
    case "OFF":
        ...
    case _:
        assert_never(state)
```

### `None`

```python
def save() -> None:
    ...
```

means:

```text
successfully returns
but no meaningful return value
```

---

## Final mental model

```text
None
│
└── "Function complete ho gaya, value = None"


NoReturn
│
└── "Function complete hone se pehle control flow terminate/escape ho gaya"


Never
│
└── "Type system ke according yahan koi possible value nahi"
```

**Sabse important distinction:**

> **`NoReturn` execution/control-flow ke baare mein hai. `Never` possibility/type-space ke baare mein hai.**

Aur isi wajah se `Never` ka use **exhaustive `match`, `Literal` states, type narrowing aur impossible branches** mein particularly powerful hai.
# Lesson 75 — `typing.ParamSpec` Advanced

Ab hum **`ParamSpec`** ko basic level se nahi, balki **deep/architecture level** par samjhenge.

`ParamSpec` ka main purpose hai:

> **Kisi function ke complete parameters ko capture karke, unhi parameters ko kisi doosre function mein preserve karna.**

Ye especially **decorators, wrappers, middleware, dependency injection, logging, retry systems, caching aur async wrappers** mein important hai.

---

# 1. Pehle problem samjho

Suppose hamare paas function hai:

```python
def calculate(a: int, b: int, c: float) -> float:
    return a + b + c
```

Ab hum decorator banana chahte hain:

```python
def log_call(func):
    ...
```

Problem ye hai ke decorator ke andar function ke parameters ka exact structure kaise preserve karein?

Simple:

```python
def log_call(func: Callable) -> Callable:
    ...
```

se type information lose ho sakti hai.

Type checker ko ye accurately pata nahi chalega ke:

```python
calculate(10, 20, 2.5)
```

valid hai aur:

```python
calculate("hello", 20, 2.5)
```

invalid hai.

Yahan `ParamSpec` kaam aata hai.

---

# 2. `ParamSpec` kya capture karta hai?

```python
from typing import ParamSpec
```

Phir:

```python
P = ParamSpec("P")
```

`P` function ke **parameters ka specification** represent karta hai.

Mental model:

```text
P
↓
function ke parameters ka complete package
```

Example:

```python
def calculate(
    a: int,
    b: int,
    c: float
) -> float:
    ...
```

Conceptually:

```text
P =
(
    a: int,
    b: int,
    c: float
)
```

Lekin `P` sirf types ka tuple nahi hai. Ye function signature ke **parameter structure** ko preserve karta hai.

---

# 3. `TypeVar` vs `ParamSpec`

Ye sabse important distinction hai.

### `TypeVar`

```python
T = TypeVar("T")
```

Ek **type** represent karta hai.

```python
def identity(value: T) -> T:
    return value
```

Yahan:

```text
T = value ka type
```

---

### `ParamSpec`

```python
P = ParamSpec("P")
```

**function ke parameters** represent karta hai.

```python
def decorator(func: Callable[P, T]) -> Callable[P, T]:
    ...
```

Yahan:

```text
T → return type

P → complete parameter list
```

Mental model:

```text
TypeVar
   ↓
one type

ParamSpec
   ↓
complete function parameter specification
```

---

# 4. `Callable[P, T]`

Ab ye syntax dekho:

```python
Callable[P, T]
```

Iska meaning:

> Aisa callable jiske parameters `P` hain aur return type `T` hai.

Example:

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")
```

Then:

```python
def wrapper(func: Callable[P, T]) -> Callable[P, T]:
    ...
```

Yani:

```text
input:
function(P → T)

output:
function(P → T)
```

Decorator ne function ke:

* parameters preserve kiye
* return type preserve kiya

---

# 5. Basic decorator

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def log_call(func: Callable[P, T]) -> Callable[P, T]:

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print("Calling function...")
        result = func(*args, **kwargs)
        print("Finished")
        return result

    return wrapper
```

Yahan teen important cheezein hain:

```python
Callable[P, T]
```

```python
*args: P.args
```

```python
**kwargs: P.kwargs
```

---

# 6. `P.args`

`P.args` represent karta hai:

> **Captured function ke positional arguments**

Example:

```python
def calculate(a: int, b: int):
    ...
```

Decorator ke wrapper mein:

```python
def wrapper(*args: P.args, **kwargs: P.kwargs):
```

`args` captured positional parameters ko represent karega.

Conceptually:

```text
calculate(10, 20)

args
 ↓
(10, 20)
```

Lekin type system ke perspective mein:

```text
args: P.args
```

original function ke positional parameter structure se linked hai.

---

# 7. `P.kwargs`

`P.kwargs` represent karta hai:

> **Captured function ke keyword arguments**

Example:

```python
def create_ahu(
    name: str,
    airflow: float,
    floor: str
):
    ...
```

Call:

```python
create_ahu(
    name="AHU-01",
    airflow=2500,
    floor="34"
)
```

Wrapper mein:

```python
**kwargs: P.kwargs
```

original function ke keyword parameter structure ko preserve karta hai.

---

# 8. `P.args` aur `P.kwargs` pair hain

Ye dono generally saath use hote hain:

```python
def wrapper(
    *args: P.args,
    **kwargs: P.kwargs
):
    return func(*args, **kwargs)
```

Mental model:

```text
P
├── P.args
│     └── positional parameters
│
└── P.kwargs
      └── keyword parameters
```

---

# 9. Sabse powerful point: exact signature preservation

Suppose:

```python
def get_equipment(
    equipment_id: str,
    floor: int,
    active: bool = True
) -> dict:
    ...
```

Decorator:

```python
def logging_decorator(
    func: Callable[P, T]
) -> Callable[P, T]:

    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        print("Calling...")
        return func(*args, **kwargs)

    return wrapper
```

Apply:

```python
get_equipment = logging_decorator(get_equipment)
```

Conceptually type checker ko pata hai:

```text
get_equipment(
    equipment_id: str,
    floor: int,
    active: bool = True
) -> dict
```

Decorator ne signature ka relationship destroy nahi kiya.

---

# 10. `ParamSpec` decorator ke liye bana hi kyun?

Traditional typing mein problem thi:

```python
Callable[..., T]
```

Example:

```python
def decorator(func: Callable[..., T]) -> Callable[..., T]:
    ...
```

`...` ka matlab roughly:

> Parameters ke exact details ko ignore karo.

Yani:

```text
Callable[..., T]
       ↓
"parameters kuch bhi ho sakte hain"
```

Problem:

```text
type safety ↓
```

`ParamSpec`:

```python
Callable[P, T]
```

kehta hai:

```text
"jo parameters original function ke hain,
woh exactly preserve karo."
```

---

# 11. `Callable[..., T]` vs `Callable[P, T]`

### Weak version

```python
Callable[..., T]
```

Meaning:

```text
Any parameters
+
return T
```

### Precise version

```python
Callable[P, T]
```

Meaning:

```text
Exactly P parameters
+
return T
```

Isliye decorators mein:

```python
ParamSpec
```

much more powerful hai.

---

# 12. Practical logging decorator

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def log_call(func: Callable[P, T]) -> Callable[P, T]:

    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        print(f"Calling {func.__name__}")

        result = func(
            *args,
            **kwargs
        )

        print(f"Finished {func.__name__}")

        return result

    return wrapper
```

Use:

```python
@log_call
def calculate_airflow(
    supply: float,
    return_air: float
) -> float:

    return supply - return_air
```

Call:

```python
result = calculate_airflow(
    2500,
    800
)
```

Type relationship remains:

```text
calculate_airflow
(
    float,
    float
)
→ float
```

---

# 13. `ParamSpec` sirf `*args` ke liye nahi

Ye misconception avoid karo.

`ParamSpec`:

```text
positional
+
keyword
+
parameter structure
```

ko collectively preserve karta hai.

Isliye:

```python
*args: P.args
**kwargs: P.kwargs
```

common implementation pattern hai.

---

# 14. Decorator jo extra parameter add kare

Ab interesting problem.

Suppose original:

```python
def calculate(
    a: int,
    b: int
) -> int:
    return a + b
```

Ab decorator chahta hai:

```text
original parameters
+
user_id
```

Yani wrapper:

```python
wrapper(user_id, a, b)
```

Yahan simple:

```python
Callable[P, T]
```

directly enough nahi hota because wrapper ka signature original se **different** ho gaya.

Example:

```python
def wrapper(
    user_id: str,
    *args: P.args,
    **kwargs: P.kwargs
) -> T:
    ...
```

Yahan conceptual signature:

```text
str + P
```

hai.

---

# 15. `ParamSpec` Concatenate

Is problem ke liye:

```python
Concatenate
```

use hota hai.

```python
from typing import Concatenate
```

Example:

```python
P = ParamSpec("P")
T = TypeVar("T")
```

Decorator:

```python
def add_user_id(
    func: Callable[Concatenate[str, P], T]
) -> Callable[P, T]:
    ...
```

Lekin direction ko carefully samajhna zaroori hai.

`Concatenate` ka concept hai:

```text
Concatenate[ExtraParameter, P]
```

means:

```text
ExtraParameter + original P
```

---

# 16. `Concatenate` practical example

Suppose original function:

```python
def process(
    equipment_id: str,
    value: float
) -> None:
    ...
```

Aur decorator internal `User` inject karta hai.

Concept:

```python
def wrapper(
    user: User,
    equipment_id: str,
    value: float
):
    ...
```

Typing:

```python
P = ParamSpec("P")
T = TypeVar("T")


def with_user(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:
    ...
```

Yahan:

```text
Concatenate[User, P]
```

means:

```text
User + P
```

---

# 17. Important: parameter injection direction

Ye bohot important architecture pattern hai.

Suppose actual implementation:

```python
def process(
    user: User,
    equipment_id: str
) -> None:
    ...
```

Decorator:

```python
def inject_user(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:

    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        user = get_current_user()

        return func(
            user,
            *args,
            **kwargs
        )

    return wrapper
```

Now:

```python
@inject_user
def process(
    user: User,
    equipment_id: str
) -> None:
    ...
```

Caller sirf:

```python
process("AHU-001")
```

likhega.

Internally:

```text
process("AHU-001")
       ↓
wrapper
       ↓
get_current_user()
       ↓
func(user, "AHU-001")
```

---

# 18. `ParamSpec` + dependency injection

Ye enterprise Python mein bohot useful pattern hai.

Example:

```text
HTTP request
     ↓
middleware
     ↓
authentication
     ↓
inject User
     ↓
business function
```

Original function:

```python
def update_equipment(
    user: User,
    equipment_id: str,
    temperature: float
) -> None:
    ...
```

External caller:

```python
update_equipment(
    "AHU-001",
    22.5
)
```

Decorator internally `User` provide karta hai.

`ParamSpec` remaining parameters preserve karta hai:

```text
P =
(equipment_id: str, temperature: float)
```

---

# 19. `ParamSpec` + retry decorator

Very practical.

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def retry(
    func: Callable[P, T]
) -> Callable[P, T]:

    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        for attempt in range(3):
            try:
                return func(
                    *args,
                    **kwargs
                )
            except Exception:
                if attempt == 2:
                    raise

        raise RuntimeError("Unreachable")

    return wrapper
```

Use:

```python
@retry
def read_temperature(
    equipment_id: str
) -> float:
    ...
```

Result remains conceptually:

```text
read_temperature(str) -> float
```

---

# 20. `ParamSpec` + caching

```python
def cache(
    func: Callable[P, T]
) -> Callable[P, T]:

    ...
```

Yahan cache decorator ko original function ke parameters preserve karne hain because cache key parameters se banegi.

Concept:

```text
P
 ↓
arguments
 ↓
cache key
 ↓
function
 ↓
T
```

---

# 21. `ParamSpec` + authorization

Suppose:

```python
def delete_equipment(
    user: User,
    equipment_id: str
) -> None:
    ...
```

Decorator:

```python
def require_admin(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:
    ...
```

Flow:

```text
caller
 ↓
equipment_id
 ↓
wrapper
 ↓
current user
 ↓
authorization
 ↓
original function
```

`ParamSpec` ensures remaining function parameters preserve hote hain.

---

# 22. `ParamSpec` + async

Ye particularly important hai.

Suppose:

```python
from typing import Awaitable

P = ParamSpec("P")
T = TypeVar("T")
```

Async decorator:

```python
from collections.abc import Awaitable, Callable


def async_log(
    func: Callable[P, Awaitable[T]]
) -> Callable[P, Awaitable[T]]:

    async def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        print("Starting")

        result = await func(
            *args,
            **kwargs
        )

        print("Finished")

        return result

    return wrapper
```

Original:

```python
@async_log
async def get_temperature(
    equipment_id: str
) -> float:
    ...
```

Relationship:

```text
input parameters
      ↓
      P
      ↓
async function
      ↓
Awaitable[T]
      ↓
wrapper
```

---

# 23. Important: `ParamSpec` return type nahi hai

Ye mistake mat karna:

```python
P = ParamSpec("P")
```

`P` return type nahi hai.

Wrong mental model:

```text
P = any type
```

Correct:

```text
P = parameter specification
```

Return ke liye:

```python
T = TypeVar("T")
```

Example:

```python
Callable[P, T]
```

means:

```text
P → T
```

---

# 24. `ParamSpec` + `TypeVar`

Dono commonly pair hote hain:

```python
P = ParamSpec("P")
T = TypeVar("T")
```

Then:

```python
Callable[P, T]
```

Architecture:

```text
          Function
         /        \
        P          T
        │          │
   parameters   return type
```

Example:

```python
Callable[
    [str, int],
    float
]
```

Conceptually:

```text
P = (str, int)
T = float
```

---

# 25. `ParamSpec` vs `TypeVar` deeper

### `TypeVar`

Relationship:

```python
def identity(x: T) -> T:
```

means:

```text
input type = output type
```

### `ParamSpec`

Relationship:

```python
def decorator(
    func: Callable[P, T]
) -> Callable[P, T]:
```

means:

```text
original parameters
      ↓
preserve them
      ↓
wrapped parameters
```

So:

```text
TypeVar
→ values/types ke relationship

ParamSpec
→ function signatures ke relationship
```

---

# 26. `ParamSpec` vs `Callable[..., T]`

### `Callable[..., T]`

```text
"I don't care about parameters"
```

### `Callable[P, T]`

```text
"I care about the exact parameter relationship"
```

Therefore:

```python
def decorator(
    func: Callable[..., T]
) -> Callable[..., T]:
```

is less precise.

While:

```python
def decorator(
    func: Callable[P, T]
) -> Callable[P, T]:
```

preserves the signature relationship.

---

# 27. `ParamSpec` vs `TypeVar` bound to Callable

A common question:

Could we do:

```python
F = TypeVar("F", bound=Callable[..., object])
```

Yes, but it doesn't give the same parameter-level precision as:

```python
P = ParamSpec("P")
T = TypeVar("T")
```

`TypeVar` says:

```text
F = some callable type
```

`ParamSpec` says:

```text
P = callable ke parameters
```

This difference matters when writing generic decorators.

---

# 28. `ParamSpec` and keyword-only parameters

Suppose:

```python
def configure(
    equipment_id: str,
    *,
    temperature: float,
    enabled: bool
) -> None:
    ...
```

Yahan:

```text
equipment_id
    ↓
positional / positional-or-keyword

temperature
enabled
    ↓
keyword-only
```

`ParamSpec` ka purpose hi parameter specification preserve karna hai.

Wrapper:

```python
def wrapper(
    *args: P.args,
    **kwargs: P.kwargs
) -> T:
    return func(*args, **kwargs)
```

Original signature ka parameter structure preserve hota hai.

---

# 29. `ParamSpec` aur positional-only parameters

Python mein:

```python
def read(
    equipment_id: str,
    /,
    timeout: float
):
    ...
```

`/` ke baad parameters keyword bhi ho sakte hain.

Parameter kinds:

```text
POSITIONAL_ONLY
POSITIONAL_OR_KEYWORD
VAR_POSITIONAL
KEYWORD_ONLY
VAR_KEYWORD
```

`ParamSpec` ka major advantage ye hai ke decorator manually ye structure recreate karne ke bajaye **original parameter specification ko preserve** kar sakta hai.

Ye decorators ke liye huge benefit hai.

---

# 30. `ParamSpec` ka biggest real-world faida

Imagine 100 functions:

```python
@log
def f1(...):
    ...

@log
def f2(...):
    ...

@log
def f3(...):
    ...
```

Agar decorator properly typed hai:

```python
P = ParamSpec("P")
T = TypeVar("T")


def log(
    func: Callable[P, T]
) -> Callable[P, T]:
    ...
```

to har function ki:

```text
parameters
+
return type
```

relationship preserve hoti hai.

Decorator reusable hai.

---

# 31. `functools.wraps` bhi use karo

Runtime metadata preserve karne ke liye:

```python
from functools import wraps
```

Example:

```python
def log_call(
    func: Callable[P, T]
) -> Callable[P, T]:

    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        print("Calling...")
        return func(*args, **kwargs)

    return wrapper
```

Yahan:

```text
ParamSpec
↓
static typing

wraps
↓
runtime function metadata
```

Dono ka role different hai.

---

# 32. Very important distinction

`ParamSpec` runtime mein arguments ko magically inspect nahi karta.

Ye:

```python
P = ParamSpec("P")
```

runtime validation framework nahi hai.

Ye primarily:

```text
static typing
```

ke liye hai.

Type checker:

* mypy
* pyright
* basedpyright

etc. `P` ko use karke signatures analyze karte hain.

---

# 33. `ParamSpec` runtime mein kya nahi karta?

Ye automatically:

```text
argument validation
```

nahi karta.

Ye automatically:

```text
conversion
```

nahi karta.

Ye automatically:

```text
logging
```

nahi karta.

Ye automatically:

```text
dependency injection
```

nahi karta.

Ye sirf type system ko relationship describe karta hai.

---

# 34. Deep mental model

Suppose function:

```python
def f(
    a: int,
    b: str,
    *,
    active: bool
) -> float:
    ...
```

Think:

```text
              f
        ┌─────┴─────┐
        │           │
        P           T
        │           │
        │         float
        │
        ├── a: int
        ├── b: str
        └── active: bool
```

Decorator:

```python
Callable[P, T]
```

means:

```text
same P
same T
```

Wrapper:

```python
*args: P.args
**kwargs: P.kwargs
```

means:

```text
P ko unpack karke
actual function ko forward karo
```

---

# 35. One complete architecture example

HVAC API logging + authorization:

```python
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar


P = ParamSpec("P")
T = TypeVar("T")


class User:
    def __init__(self, name: str):
        self.name = name


def get_current_user() -> User:
    return User("Admin")


def authorized(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:

    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        user = get_current_user()

        print(
            f"Authorized user: {user.name}"
        )

        return func(
            user,
            *args,
            **kwargs
        )

    return wrapper
```

Business function:

```python
@authorized
def update_temperature(
    user: User,
    equipment_id: str,
    temperature: float
) -> str:

    return (
        f"{user.name} updated "
        f"{equipment_id} to {temperature}"
    )
```

Caller:

```python
result = update_temperature(
    "AHU-01",
    22.5
)
```

Flow:

```text
update_temperature("AHU-01", 22.5)
                 │
                 ▼
             wrapper
                 │
                 ▼
         get_current_user()
                 │
                 ▼
              User
                 │
                 ▼
func(user, "AHU-01", 22.5)
                 │
                 ▼
               str
```

Typing:

```text
User + P → T
```

where:

```text
P = (equipment_id: str, temperature: float)

T = str
```

This is exactly the type of architecture where `ParamSpec` shines.

---

# 36. `ParamSpec` ka ultimate mental model

Isko ek line mein yaad karo:

> **`TypeVar` function ke values/types ko relate karta hai, jabke `ParamSpec` function ke complete parameters/signature ko preserve karta hai.**

Aur:

```text
P = parameters
T = return type

Callable[P, T]
      ↓
P → T
```

Decorator:

```python
Callable[P, T]
        ↓
wrapper
        ↓
Callable[P, T]
```

means:

> **"Main function ko wrap kar raha hoon, lekin uske parameters aur return type ka relationship preserve kar raha hoon."**

### Advanced extension:

```python
Concatenate[User, P]
```

means:

> **"Original parameter specification `P` ke saath ek additional parameter prepend karo."**

Isliye `ParamSpec` ka real power sirf `P.args` aur `P.kwargs` nahi hai — **iska core purpose higher-order functions aur decorators mein function-signature relationships ko type-safe tareeqe se preserve karna hai.**
# Lesson 76 — `typing.Concatenate` — Partial ParamSpec

Ab **`ParamSpec` ke baad `Concatenate`** naturally samajh aayega.

Sabse pehle ek correction/clarification:

> **`Concatenate` ko "Partial ParamSpec" kehna useful mental model hai, lekin technically `Concatenate` khud partial `ParamSpec` nahi hai.**
> Ye `ParamSpec` ke parameters ke **aagay fixed parameters add/prepend** karne ka typing construct hai.

---

# 1. `Concatenate` kya karta hai?

Import:

```python
from typing import Concatenate
```

Basic syntax:

```python
Concatenate[FixedType, P]
```

Iska meaning:

```text
FixedType + P
```

Agar:

```python
P = (str, float)
```

conceptually ho, to:

```python
Concatenate[User, P]
```

ka matlab:

```text
(User, str, float)
```

Yani:

```text
original parameters
       ↓
P = (str, float)

Concatenate
       ↓
(User, str, float)
```

---

# 2. `ParamSpec` se connection

Previous lesson mein:

```python
P = ParamSpec("P")
T = TypeVar("T")
```

aur:

```python
Callable[P, T]
```

samjha tha.

Iska matlab:

```text
P → function ke parameters
T → return type
```

Ab agar humein:

```text
P
```

ke **start mein ek fixed parameter** add karna ho:

```text
User + P
```

to:

```python
Callable[Concatenate[User, P], T]
```

use karte hain.

---

# 3. Sabse simple example

Original function:

```python
def process(
    equipment_id: str,
    temperature: float
) -> None:
    ...
```

Conceptually:

```text
P =
(
    equipment_id: str,
    temperature: float
)
```

Ab internal function ko `User` bhi chahiye:

```python
def process(
    user: User,
    equipment_id: str,
    temperature: float
) -> None:
    ...
```

Conceptually:

```text
Concatenate[User, P]
```

means:

```text
User
 +
equipment_id: str
 +
temperature: float
```

---

# 4. Important direction

Ye yaad rakho:

```python
Concatenate[User, P]
```

means:

```text
User + P
```

**P + User nahi.**

Example:

```text
P = (str, float)

Concatenate[User, P]

= (User, str, float)
```

Not:

```text
(str, float, User)
```

---

# 5. `Concatenate` ka actual use decorator mein hota hai

Suppose:

```python
class User:
    pass
```

Business function:

```python
def update_equipment(
    user: User,
    equipment_id: str,
    temperature: float
) -> str:
    return "Updated"
```

Caller ideally sirf:

```python
update_equipment(
    "AHU-01",
    22.5
)
```

provide kare.

`User` decorator automatically provide kare.

---

# 6. Full decorator

```python
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar


P = ParamSpec("P")
T = TypeVar("T")


def get_current_user() -> User:
    return User()


def inject_user(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:

    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        user = get_current_user()

        return func(
            user,
            *args,
            **kwargs
        )

    return wrapper
```

Ab:

```python
@inject_user
def update_equipment(
    user: User,
    equipment_id: str,
    temperature: float
) -> str:

    return (
        f"{user} updated "
        f"{equipment_id} to {temperature}"
    )
```

Caller:

```python
update_equipment(
    "AHU-01",
    22.5
)
```

---

# 7. Yahan actual magic kya hua?

Original function:

```text
User + P → T
```

Decorator ke baad external function:

```text
P → T
```

Yani decorator ne:

```text
User
```

**consume/inject** kar diya.

Diagram:

```text
                Original function

             User + P
                │
                ▼
                T


                Decorator

Caller
  │
  │ P
  ▼
wrapper
  │
  ├── automatically creates User
  │
  ▼
User + P
  │
  ▼
original function
  │
  ▼
T
```

Ye `Concatenate` ka sabse important use case hai.

---

# 8. `Callable` ko line-by-line padho

```python
Callable[
    Concatenate[User, P],
    T
]
```

Isko right-to-left nahi, structure mein padho:

```text
Callable[
    parameters,
    return
]
```

parameters:

```python
Concatenate[User, P]
```

which means:

```text
User + P
```

return:

```python
T
```

Therefore:

```text
Callable[User + P, T]
```

---

# 9. Decorator ka input/output

Ye line:

```python
def inject_user(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:
```

bohot powerful hai.

Input:

```text
User + P → T
```

Output:

```text
P → T
```

So decorator:

```text
(User + P → T)
        ↓
     inject_user
        ↓
(P → T)
```

Ye hi `Concatenate` ka core pattern hai.

---

# 10. `ParamSpec` alone se ye problem kyun nahi solve hoti?

Agar:

```python
P = ParamSpec("P")
```

to:

```python
Callable[P, T]
```

original parameters ko preserve karta hai.

Lekin humein kehna hai:

```text
fixed parameter
+
original parameters
```

Yani:

```text
User + P
```

`ParamSpec` alone:

```python
Callable[P, T]
```

itna expressive nahi hai.

`Concatenate` ye relationship express karta hai:

```python
Callable[Concatenate[User, P], T]
```

---

# 11. `Concatenate` ko "prefix" samjho

Sabse easy mental model:

```text
Concatenate = prefix add karna
```

Example:

```text
P
↓
(A, B, C)
```

Then:

```text
Concatenate[X, P]
```

becomes conceptually:

```text
(X, A, B, C)
```

So:

```text
Concatenate
      ↓
fixed parameters
      +
ParamSpec
```

---

# 12. Multiple fixed parameters

Sirf ek parameter zaroori nahi.

```python
Concatenate[User, Request, P]
```

Conceptually:

```text
User + Request + P
```

Agar:

```text
P = (equipment_id: str, value: float)
```

to:

```text
(User, Request, str, float)
```

ho jayega.

---

# 13. Real API example

Suppose business function:

```python
def update_temperature(
    user: User,
    request: Request,
    equipment_id: str,
    temperature: float
) -> bool:
    ...
```

Typing:

```python
P = ParamSpec("P")
T = TypeVar("T")
```

Decorator:

```python
def api_context(
    func: Callable[
        Concatenate[User, Request, P],
        T
    ]
) -> Callable[P, T]:
    ...
```

Flow:

```text
Caller
  │
  ├── equipment_id
  └── temperature
          │
          ▼
      wrapper
          │
          ├── User
          ├── Request
          │
          ▼
User + Request + P
          │
          ▼
business function
```

Ye web frameworks, service layers aur middleware architecture mein useful pattern hai.

---

# 14. Authentication example

Suppose function:

```python
def delete_equipment(
    user: User,
    equipment_id: str
) -> None:
    ...
```

Decorator:

```python
def authenticated(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:
    ...
```

Ab caller:

```python
delete_equipment("AHU-001")
```

internally:

```text
"AHU-001"
     │
     ▼
wrapper
     │
     ├── current_user
     │
     ▼
func(
    current_user,
    "AHU-001"
)
```

Type relationship:

```text
Original:
User + P → T

External:
P → T
```

---

# 15. Authorization example

Authentication ke baad authorization:

```python
def require_admin(
    func: Callable[Concatenate[User, P], T]
) -> Callable[P, T]:

    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        user = get_current_user()

        if not user.is_admin:
            raise PermissionError(
                "Admin required"
            )

        return func(
            user,
            *args,
            **kwargs
        )

    return wrapper
```

Business function:

```python
@require_admin
def delete_equipment(
    user: User,
    equipment_id: str
) -> None:
    ...
```

Caller:

```python
delete_equipment("AHU-01")
```

`User` caller se nahi aa raha.

Decorator inject karta hai.

---

# 16. Dependency Injection

`Concatenate` ko Dependency Injection ke context mein samjho.

Suppose:

```text
Business function:
User + Database + P → T
```

External caller ko sirf:

```text
P
```

dena hai.

Architecture:

```text
Caller
  │
  │ P
  ▼
Decorator
  │
  ├── User
  ├── Database
  │
  ▼
User + Database + P
  │
  ▼
Business Function
  │
  ▼
T
```

Typing:

```python
Callable[
    Concatenate[User, Database, P],
    T
]
```

Output:

```python
Callable[P, T]
```

---

# 17. Logging + injected dependency

Imagine:

```python
def service(
    logger: Logger,
    equipment_id: str,
    floor: int
) -> bool:
    ...
```

Decorator:

```python
def inject_logger(
    func: Callable[
        Concatenate[Logger, P],
        T
    ]
) -> Callable[P, T]:
    ...
```

Original:

```text
Logger + P → T
```

External:

```text
P → T
```

---

# 18. Database transaction example

Suppose:

```python
def save_equipment(
    db: Database,
    equipment_id: str,
    value: float
) -> bool:
    ...
```

Decorator:

```python
def with_database(
    func: Callable[
        Concatenate[Database, P],
        T
    ]
) -> Callable[P, T]:
    ...
```

Flow:

```text
save_equipment(
    "AHU-01",
    22.5
)

        ↓

wrapper

        ↓

database = get_database()

        ↓

func(
    database,
    "AHU-01",
    22.5
)
```

---

# 19. `Concatenate` + `ParamSpec` = signature transformation

Ye advanced mental model hai.

`ParamSpec`:

```text
P
```

original signature capture karta hai.

`Concatenate`:

```text
Fixed + P
```

signature ko transform karta hai.

So:

```text
ParamSpec
   ↓
capture

Concatenate
   ↓
transform
```

---

# 20. Decorator transformation

Imagine:

```text
Original:
(User, P) → T
```

Decorator:

```text
remove/inject User
```

External:

```text
P → T
```

Yani `Concatenate` decorator ki **input signature** describe karta hai.

```python
Callable[
    Concatenate[User, P],
    T
]
```

---

# 21. `Concatenate` ka naam kyun?

Naam literally explain karta hai:

```text
Concatenate
=
join together
```

Example:

```text
User
+
P
```

becomes:

```text
User + P
```

Agar:

```text
P = (str, float)
```

then:

```text
Concatenate[User, P]
```

conceptually:

```text
(User, str, float)
```

---

# 22. `Concatenate` arbitrary parameters ko beech mein insert karta hai?

Yahan ek important restriction hai.

Typical form:

```python
Concatenate[Fixed1, Fixed2, P]
```

means fixed parameters **P se pehle**.

Ye general-purpose:

```text
P ke beech mein parameter insert karo
```

mechanism nahi hai.

Mental model:

```text
FIXED PREFIX + P
```

not:

```text
P[0] + FIXED + P[1:]
```

---

# 23. `Concatenate` ka use `Callable` ke saath

Important syntax:

```python
Callable[
    Concatenate[User, P],
    T
]
```

`Concatenate` ko normally isi callable parameter specification context mein dekha jata hai.

Don't think:

```python
Concatenate[User, P]
```

as an ordinary runtime container.

Ye typing construct hai.

---

# 24. Runtime behavior

Jaise `ParamSpec`:

```python
P = ParamSpec("P")
```

runtime dependency injection nahi karta.

Similarly:

```python
Concatenate[User, P]
```

runtime par function parameters automatically change nahi karta.

Aapko actual wrapper likhna padega:

```python
def wrapper(
    *args: P.args,
    **kwargs: P.kwargs
):
    user = get_current_user()

    return func(
        user,
        *args,
        **kwargs
    )
```

Typing aur runtime behavior separate hain.

---

# 25. `Concatenate` validation nahi karta

Ye:

```python
Concatenate[User, P]
```

automatically check nahi karega:

```text
User actually User hai?
```

Runtime validation aapki responsibility hai.

Example:

```python
user = get_current_user()
```

actual object hona chahiye.

---

# 26. `Concatenate` vs `TypeVar`

`TypeVar`:

```python
T = TypeVar("T")
```

type relationship.

`ParamSpec`:

```python
P = ParamSpec("P")
```

parameter relationship.

`Concatenate`:

```python
Concatenate[User, P]
```

parameter specification ko fixed prefix ke saath combine karta hai.

```text
TypeVar
   ↓
type

ParamSpec
   ↓
parameters

Concatenate
   ↓
fixed parameters + parameters
```

---

# 27. `Concatenate` vs `*args`

Runtime Python mein:

```python
def wrapper(*args):
    ...
```

sirf values capture karta hai.

Typing mein:

```python
def wrapper(
    *args: P.args,
    **kwargs: P.kwargs
):
```

type checker ko original function ke parameter relationship se connect karta hai.

`Concatenate` usse ek step aur aagay le jata hai:

```text
User + P
```

---

# 28. Advanced decorator: context injection

Facility-management example:

```python
class BuildingContext:
    def __init__(self, building: str):
        self.building = building
```

Business function:

```python
def get_equipment(
    context: BuildingContext,
    equipment_id: str
) -> dict:
    ...
```

Decorator:

```python
def inject_context(
    func: Callable[
        Concatenate[BuildingContext, P],
        T
    ]
) -> Callable[P, T]:
    ...
```

Caller:

```python
get_equipment("MEP-KHN-REF04")
```

Internally:

```text
equipment_id
     │
     ▼
 wrapper
     │
     ▼
BuildingContext
     │
     ▼
BuildingContext + equipment_id
     │
     ▼
function
```

---

# 29. Middleware architecture

`Concatenate` middleware ke liye natural fit hai.

Example:

```text
Request
   ↓
Authentication middleware
   ↓
User injection
   ↓
Authorization middleware
   ↓
Database injection
   ↓
Business function
```

Conceptual signature transformation:

```text
Business:
User + DB + P → T

External:
P → T
```

Typing:

```python
Callable[
    Concatenate[User, Database, P],
    T
]
```

---

# 30. `Concatenate` ka strongest use case

Jab decorator:

> **function ko call karne ke liye required context/dependency khud provide karta hai**

Examples:

* `User`
* `Request`
* `Database`
* `Logger`
* `Transaction`
* `Session`
* `Context`
* `Config`

Then:

```python
Concatenate[Dependency, P]
```

extremely useful hai.

---

# 31. One subtle distinction: injection vs removal

Suppose:

```text
Original:
User + P → T
```

Decorator caller ko:

```text
P → T
```

expose karta hai.

Ye **runtime mein User ko remove nahi karta**.

Actually:

```text
Caller:
P

Wrapper:
User + P

Original:
User + P
```

So "remove" sirf **external callable signature** se hua.

Internally User still exists.

---

# 32. Full example with multiple dependencies

```python
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar


P = ParamSpec("P")
T = TypeVar("T")


class User:
    pass


class Database:
    pass


def get_user() -> User:
    return User()


def get_database() -> Database:
    return Database()


def inject_dependencies(
    func: Callable[
        Concatenate[User, Database, P],
        T
    ]
) -> Callable[P, T]:

    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:

        user = get_user()
        db = get_database()

        return func(
            user,
            db,
            *args,
            **kwargs
        )

    return wrapper
```

Business function:

```python
@inject_dependencies
def update_equipment(
    user: User,
    db: Database,
    equipment_id: str,
    temperature: float
) -> bool:

    print(equipment_id)
    print(temperature)

    return True
```

External API:

```python
update_equipment(
    "AHU-01",
    22.5
)
```

Type transformation:

```text
Original:

(User, Database, str, float) → bool


External:

(str, float) → bool
```

Yahan:

```text
P = (str, float)
```

and:

```text
Concatenate[User, Database, P]
```

means:

```text
(User, Database, str, float)
```

---

# 33. `ParamSpec` + `Concatenate` ko ek formula ki tarah yaad karo

### ParamSpec

```text
P = unknown-but-preserved parameter list
```

### Concatenate

```text
Concatenate[A, P]
=
A + P
```

### Callable

```text
Callable[P, T]
=
P → T
```

### Combined

```text
Callable[Concatenate[A, P], T]
=
(A + P) → T
```

Aur decorator output:

```text
Callable[P, T]
=
P → T
```

---

# 34. Previous lesson ke saath direct connection

Lesson 75:

```python
P = ParamSpec("P")
T = TypeVar("T")

Callable[P, T]
```

Meaning:

```text
P → T
```

Lesson 76:

```python
Callable[Concatenate[User, P], T]
```

Meaning:

```text
User + P → T
```

Aur:

```python
-> Callable[P, T]
```

Meaning:

```text
external caller ko P → T
```

Full picture:

```text
             Original Function
             
              User + P
                 │
                 ▼
                  T


                 ▲
                 │
             Decorator
                 │
                 ▼

              External API

                  P
                  │
                  ▼
                  T
```

---

# 35. `Concatenate` ka faida

### 1. Type-safe dependency injection

```text
User + P
```

ko accurately describe kar sakte ho.

### 2. Typed decorators

Decorator original signature relationship preserve karta hai.

### 3. Middleware

Request/user/session inject karna easy to model hota hai.

### 4. Authorization

User automatically provide karna.

### 5. Database/session injection

```text
DB + P
```

### 6. Framework architecture

Web frameworks, service layers aur dependency injection systems mein useful.

### 7. Refactoring safety

Function ke parameters change hone par type checker affected decorators ko detect karne mein help kar sakta hai.

---

# 36. Final comparison

| Construct                        | Main purpose                              |
| -------------------------------- | ----------------------------------------- |
| `TypeVar`                        | Type relationship                         |
| `ParamSpec`                      | Complete function parameter specification |
| `P.args`                         | Captured positional arguments             |
| `P.kwargs`                       | Captured keyword arguments                |
| `Concatenate`                    | Fixed parameters + `ParamSpec`            |
| `Callable[P, T]`                 | P parameters → T return                   |
| `Callable[Concatenate[X, P], T]` | X + P parameters → T return               |

---

# 37. Golden mental model

Isko yaad kar lo:

```text
TypeVar
   ↓
"T kya type hai?"

ParamSpec
   ↓
"P function ke kaun se parameters hain?"

Concatenate
   ↓
"P ke aagay kaunsa fixed parameter add hai?"

Callable
   ↓
"Ye parameters kis return type ko produce karte hain?"
```

So:

```python
Callable[
    Concatenate[User, Request, P],
    T
]
```

ko human language mein padho:

> **"Ye callable pehle `User` aur `Request` leta hai, phir original function ke parameters `P` leta hai, aur akhir mein `T` return karta hai."**

Aur decorator agar:

```python
-> Callable[P, T]
```

return karta hai, to:

> **"Caller ko `User` aur `Request` dene ki zarurat nahi; decorator unko internally inject karega."**

**Lesson 75 + 76 ka core pair:**

```text
ParamSpec = parameter list ko capture/preserve karo

Concatenate = us parameter list ke saath fixed prefix parameters joro
```

Yahi combination advanced, type-safe decorators ka foundation hai.
# Lesson 77 — `typing.Unpack` + `TypedDict` Unpacking

Ab hum `ParamSpec` aur `Concatenate` ke baad **`Unpack`** par aa gaye hain.

Is lesson ka main focus hai:

> **`TypedDict` ke keys ko `**kwargs` ke through type-safe tareeqe se unpack karna.**

Ye especially **configuration dictionaries, API payloads, function keyword arguments, settings aur structured data** mein useful hai.

---

# 1. Sabse pehle normal `**dict`

Python mein hum karte hain:

```python
config = {
    "equipment_id": "AHU-01",
    "temperature": 22.5,
}

def update_equipment(
    equipment_id,
    temperature
):
    ...
```

Call:

```python
update_equipment(**config)
```

`**config` dictionary ko unpack karta hai:

```text
config
  ↓
{
    "equipment_id": "AHU-01",
    "temperature": 22.5
}
  ↓ ** unpack
equipment_id="AHU-01"
temperature=22.5
```

Runtime Python ko pata hai keys kya hain.

Lekin static type checker ko exact structure kaise pata chale?

Yahan:

```python
Unpack
```

kaam aata hai.

---

# 2. `TypedDict` kya deta hai?

Previous lessons mein `TypedDict` padha tha.

Example:

```python
from typing import TypedDict


class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float
    enabled: bool
```

Ab:

```python
config: EquipmentConfig = {
    "equipment_id": "AHU-01",
    "temperature": 22.5,
    "enabled": True,
}
```

Type checker ko pata hai:

```text
equipment_id → str
temperature  → float
enabled      → bool
```

Lekin ab hum is dictionary ko function ke `**kwargs` ke form mein pass karna chahte hain.

---

# 3. `Unpack` yahan aata hai

Syntax:

```python
from typing import Unpack
```

Then:

```python
def update_equipment(
    **kwargs: Unpack[EquipmentConfig]
) -> None:
    ...
```

Iska conceptual meaning:

> `kwargs` ke andar wohi keys aur types hain jo `EquipmentConfig` mein defined hain.

Yani:

```python
**kwargs: Unpack[EquipmentConfig]
```

roughly:

```text
kwargs:
    equipment_id → str
    temperature  → float
    enabled      → bool
```

---

# 4. `Unpack` ka simple mental model

Normal:

```python
EquipmentConfig
```

means:

```text
ek TypedDict object
```

`Unpack`:

```python
Unpack[EquipmentConfig]
```

means:

```text
"Is TypedDict ke individual fields ko
kwargs ke parameters ki tarah spread karo."
```

Mental model:

```text
TypedDict
   ↓
{
    a: int,
    b: str
}

Unpack
   ↓

**kwargs:
    a: int
    b: str
```

---

# 5. Basic example

```python
from typing import TypedDict, Unpack


class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float


def update_equipment(
    **kwargs: Unpack[EquipmentConfig]
) -> None:

    print(kwargs["equipment_id"])
    print(kwargs["temperature"])
```

Call:

```python
update_equipment(
    equipment_id="AHU-01",
    temperature=22.5
)
```

Type checker ko pata hai:

```text
equipment_id → str
temperature → float
```

---

# 6. Ye normal `**kwargs: dict` se better kyun hai?

Agar hum likhein:

```python
def update_equipment(
    **kwargs: dict
):
    ...
```

to structure vague hai.

Type checker ko:

```text
kaunsi key?
kis type ki value?
required hai ya optional?
```

ka precise knowledge nahi hota.

Lekin:

```python
**kwargs: Unpack[EquipmentConfig]
```

se exact shape milti hai.

---

# 7. `TypedDict` + `Unpack` = keyword schema

Ye phrase yaad rakho:

> **`TypedDict` keyword arguments ka schema define kar sakta hai, aur `Unpack` us schema ko `**kwargs` mein expand karta hai.**

Example:

```python
class AHUConfig(TypedDict):
    equipment_id: str
    airflow: float
    temperature: float
```

Then:

```python
def configure(
    **kwargs: Unpack[AHUConfig]
):
    ...
```

Conceptually:

```text
configure(
    equipment_id: str,
    airflow: float,
    temperature: float
)
```

---

# 8. `Unpack` ka matlab runtime mein kya hai?

Important:

`Unpack` khud runtime par dictionary unpack nahi karta.

Actual unpacking:

```python
configure(**config)
```

Python karta hai.

`Unpack`:

```python
Unpack[AHUConfig]
```

type checker ko batata hai:

> `**kwargs` kis shape ka hai.

Yani:

```text
**config
   ↓
runtime operation

Unpack[AHUConfig]
   ↓
static typing information
```

---

# 9. TypedDict aur normal dict ka difference

Suppose:

```python
config = {
    "equipment_id": "AHU-01",
    "airflow": 2500.0,
}
```

Normal `dict`:

```text
generic dictionary
```

TypedDict:

```python
class AHUConfig(TypedDict):
    equipment_id: str
    airflow: float
```

means:

```text
specific dictionary shape
```

Aur:

```python
Unpack[AHUConfig]
```

means:

```text
specific dictionary shape
       ↓
keyword parameters
```

---

# 10. Function signature ko imagine karo

Ye:

```python
def configure(
    **kwargs: Unpack[AHUConfig]
):
    ...
```

ko mentally aise samjho:

```python
def configure(
    *,
    equipment_id: str,
    airflow: float
):
    ...
```

Yani `TypedDict` ke fields keyword parameters banne ka conceptual effect hai.

---

# 11. `*` ka connection

`**kwargs` naturally keyword arguments hain.

Suppose:

```python
def configure(
    *,
    equipment_id: str,
    airflow: float
):
    ...
```

Caller:

```python
configure(
    equipment_id="AHU-01",
    airflow=2500
)
```

Isi type ke keyword structure ko:

```python
TypedDict + Unpack
```

se describe kiya ja sakta hai.

---

# 12. Required fields

Default `TypedDict`:

```python
class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float
```

Dono required hain.

So:

```python
configure(
    equipment_id="AHU-01"
)
```

type checker missing:

```text
temperature
```

detect kar sakta hai.

---

# 13. Optional fields

`NotRequired` use kar sakte hain:

```python
from typing import NotRequired, TypedDict, Unpack


class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float
    enabled: NotRequired[bool]
```

Now:

```python
def configure(
    **kwargs: Unpack[EquipmentConfig]
):
    ...
```

Valid:

```python
configure(
    equipment_id="AHU-01",
    temperature=22.5
)
```

Also:

```python
configure(
    equipment_id="AHU-01",
    temperature=22.5,
    enabled=True
)
```

---

# 14. `NotRequired` vs `Optional`

Ye important distinction hai.

### `NotRequired`

```python
enabled: NotRequired[bool]
```

means:

> key itself optional hai.

### `Optional`

```python
enabled: bool | None
```

means:

> key required ho sakti hai, lekin value `None` ho sakti hai.

Difference:

```text
NotRequired
↓
key missing allowed

bool | None
↓
key present, value None allowed
```

---

# 15. Example

```python
class Config(TypedDict):
    name: str
    enabled: NotRequired[bool]
```

Valid:

```python
{
    "name": "AHU-01"
}
```

Valid:

```python
{
    "name": "AHU-01",
    "enabled": True
}
```

But:

```python
{
    "name": "AHU-01",
    "enabled": None
}
```

invalid hai, because:

```text
enabled → bool
```

not:

```text
bool | None
```

---

# 16. `Unpack` + `Required`

Agar `total=False` use karo:

```python
class EquipmentConfig(TypedDict, total=False):
    equipment_id: str
    temperature: float
```

Dono optional ho jayenge.

Lekin specific field ko required bana sakte ho:

```python
from typing import Required


class EquipmentConfig(TypedDict, total=False):
    equipment_id: Required[str]
    temperature: float
```

Ab:

```text
equipment_id → required
temperature → optional
```

`Unpack` isi structure ko preserve karta hai.

---

# 17. API payload example

Ye real-world use case hai.

Suppose API request:

```python
class EquipmentPayload(TypedDict):
    equipment_id: str
    floor: str
    temperature: float
    active: bool
```

Function:

```python
def send_update(
    **payload: Unpack[EquipmentPayload]
):
    ...
```

Call:

```python
send_update(
    equipment_id="AHU-01",
    floor="34",
    temperature=22.5,
    active=True
)
```

Ab function ke keyword payload ka static schema defined hai.

---

# 18. `Unpack` + configuration system

Suppose:

```python
class HVACSettings(TypedDict):
    setpoint: float
    airflow: float
    fan_speed: int
```

Function:

```python
def configure_ahu(
    **settings: Unpack[HVACSettings]
):
    ...
```

Call:

```python
configure_ahu(
    setpoint=22.0,
    airflow=2500.0,
    fan_speed=75
)
```

Type checker:

```text
setpoint → float
airflow → float
fan_speed → int
```

---

# 19. Wrong types

Suppose:

```python
configure_ahu(
    setpoint="22",
    airflow=2500.0,
    fan_speed=75
)
```

Type checker `setpoint` ke liye complain karega:

```text
expected float
got str
```

Ye `Unpack` ka practical benefit hai.

---

# 20. Unknown keys

Suppose:

```python
configure_ahu(
    setpoint=22.0,
    airflow=2500.0,
    fan_speed=75,
    color="red"
)
```

`HVACSettings` mein:

```text
color
```

defined nahi hai.

Static checker is extra keyword ko reject kar sakta hai.

Yani `TypedDict + Unpack`:

```text
known keys
+
known value types
+
required/optional status
```

preserve karta hai.

---

# 21. `Unpack` sirf TypedDict ke liye nahi

Ye important advanced point hai.

`Unpack` ka broader purpose hai:

> **A parameterized type ke contents ko type-level context mein expand karna.**

Example with tuple:

```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple("Ts")
```

Then:

```python
tuple[Unpack[Ts]]
```

variable-length type tuple ko represent kar sakta hai.

Ye `TypedDict` use case se broader concept hai.

---

# 22. `TypeVarTuple` + `Unpack`

Ye next-level typing hai.

```python
Ts = TypeVarTuple("Ts")
```

Suppose:

```python
class Container(Generic[*Ts]):
    ...
```

Yahan:

```python
Unpack[Ts]
```

type-level tuple of types ko expand karta hai.

Conceptually:

```text
Ts
↓
(int, str, float)

Unpack[Ts]
↓
int, str, float
```

Lekin **Lesson 77 ka primary focus `TypedDict` + `**kwargs`** hai.

`TypeVarTuple` ko hum alag depth mein cover kar sakte hain.

---

# 23. `Unpack` vs `*` runtime unpacking

Dono ko confuse mat karna.

Runtime:

```python
values = (10, 20, 30)

print(*values)
```

Python actual values unpack karta hai.

Type-level:

```python
Unpack[Ts]
```

type information unpack karta hai.

Similarly:

```python
config = {
    "name": "AHU"
}

func(**config)
```

runtime dictionary unpacking hai.

While:

```python
def func(**kwargs: Unpack[Config]):
    ...
```

static type annotation hai.

---

# 24. `Unpack` vs `ParamSpec`

Ye bhi important hai because previous lessons connected hain.

### `ParamSpec`

```python
P = ParamSpec("P")
```

represents:

```text
complete function parameter specification
```

### `Unpack[TypedDict]`

represents:

```text
TypedDict ke keys ko keyword parameters ke form mein expand karna
```

Mental model:

```text
ParamSpec
   ↓
existing function signature

Unpack[TypedDict]
   ↓
dictionary shape → keyword argument shape
```

---

# 25. `ParamSpec` vs `Unpack` example

### ParamSpec

```python
P = ParamSpec("P")
T = TypeVar("T")

def decorator(
    func: Callable[P, T]
) -> Callable[P, T]:
    ...
```

Yahan:

```text
P
↓
original function ke parameters
```

### Unpack

```python
class Config(TypedDict):
    host: str
    port: int


def connect(
    **config: Unpack[Config]
):
    ...
```

Yahan:

```text
Config
↓
host: str
port: int
```

---

# 26. `Concatenate` vs `Unpack`

Previous lesson:

```python
Concatenate[User, P]
```

means:

```text
User + P
```

Current:

```python
Unpack[Config]
```

means conceptually:

```text
Config fields
↓
expand into kwargs
```

So:

```text
Concatenate
→ parameter specifications ko combine karta hai

Unpack
→ type-level contents ko expand karta hai
```

---

# 27. Real architecture: API + service

Suppose API layer:

```python
class EquipmentPayload(TypedDict):
    equipment_id: str
    temperature: float
```

Service:

```python
def update_equipment(
    **payload: Unpack[EquipmentPayload]
) -> bool:

    equipment_id = payload["equipment_id"]
    temperature = payload["temperature"]

    print(equipment_id)
    print(temperature)

    return True
```

API data:

```python
payload: EquipmentPayload = {
    "equipment_id": "AHU-01",
    "temperature": 22.5,
}
```

Then:

```python
update_equipment(**payload)
```

Flow:

```text
JSON/API
   ↓
TypedDict
   ↓
EquipmentPayload
   ↓
**
   ↓
Unpack[EquipmentPayload]
   ↓
typed kwargs
   ↓
service
```

---

# 28. `TypedDict` + `Unpack` ka major faida

### Before

```python
def update(**kwargs):
    ...
```

Type information:

```text
unknown
```

### After

```python
def update(
    **kwargs: Unpack[EquipmentPayload]
):
    ...
```

Type information:

```text
equipment_id → str
temperature → float
```

Aur:

```text
required fields
optional fields
extra keys
```

sab static type checker ke liye visible ho sakte hain.

---

# 29. Function call aur TypedDict ke beech relationship

Suppose:

```python
class UserOptions(TypedDict):
    name: str
    age: int
```

and:

```python
def create_user(
    **options: Unpack[UserOptions]
):
    ...
```

Then:

```python
options: UserOptions = {
    "name": "Nouman",
    "age": 30
}
```

Call:

```python
create_user(**options)
```

Conceptually:

```text
options
{
    name: str,
    age: int
}

       ↓ **

create_user(
    name=str,
    age=int
)
```

---

# 30. Why not just use `dict[str, object]`?

Because:

```python
dict[str, object]
```

sirf ye batata hai:

```text
key = str
value = object
```

It doesn't tell checker:

```text
name → str
age → int
```

`TypedDict` tells it exact schema.

---

# 31. `Unpack` ka deeper architecture benefit

Ye **dictionary-shaped data aur function-shaped data ke beech bridge** banata hai.

```text
TypedDict world
       │
       │ Unpack
       ▼
Function kwargs world
```

Example:

```text
API payload
    ↓
TypedDict
    ↓
Unpack
    ↓
service function
```

Isliye modern typed Python applications mein ye useful hai.

---

# 32. One important limitation

`TypedDict` runtime validation nahi karta.

Example:

```python
class Config(TypedDict):
    temperature: float
```

Ye runtime par automatically ensure nahi karta:

```python
config["temperature"]
```

actually `float` hai.

Similarly:

```python
Unpack[Config]
```

runtime validation nahi karta.

Ye primarily:

```text
static typing
```

hai.

External JSON/API data ho to runtime validation ke liye dedicated validation/parsing approach chahiye.

---

# 33. `TypedDict` + `Unpack` vs dataclass

### TypedDict + Unpack

Good for:

```text
JSON
API payload
kwargs
configuration dictionaries
```

### Dataclass

Good for:

```text
domain object
state
methods
behavior
```

Example:

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature: float
```

vs:

```python
class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float
```

First:

```text
object
```

Second:

```text
dictionary shape
```

---

# 34. Advanced example with optional API parameters

```python
from typing import NotRequired, TypedDict, Unpack


class EquipmentUpdate(TypedDict):
    equipment_id: str
    temperature: float
    enabled: NotRequired[bool]
    comment: NotRequired[str]


def update_equipment(
    **data: Unpack[EquipmentUpdate]
) -> None:
    ...
```

Valid:

```python
update_equipment(
    equipment_id="AHU-01",
    temperature=22.5
)
```

Valid:

```python
update_equipment(
    equipment_id="AHU-01",
    temperature=22.5,
    enabled=True,
    comment="PPM adjustment"
)
```

Conceptually:

```text
Required:
    equipment_id
    temperature

Optional:
    enabled
    comment
```

---

# 35. `Unpack` + `TypedDict` ka complete mental model

```text
                TypedDict
                    │
                    │ defines
                    ▼
              dictionary shape
                    │
                    │ Unpack
                    ▼
               **kwargs
                    │
                    ▼
          function keyword parameters
```

Example:

```python
class Config(TypedDict):
    host: str
    port: int
```

then:

```python
def connect(
    **config: Unpack[Config]
):
    ...
```

means conceptually:

```text
connect(
    host: str,
    port: int
)
```

---

# 36. Teen concepts ko ek saath rakho

Ab tak ke lessons:

### `ParamSpec`

```text
P
↓
complete function parameter specification
```

### `Concatenate`

```text
Concatenate[X, P]
↓
X + P
```

### `Unpack`

```text
Unpack[Config]
↓
Config ke contents ko expand karo
```

Mental picture:

```text
ParamSpec
    ↓
Function signature

Concatenate
    ↓
Fixed prefix + signature

Unpack
    ↓
Structured type contents → expanded parameters/types
```

---

# 37. Most important syntax

```python
from typing import TypedDict, Unpack


class EquipmentConfig(TypedDict):
    equipment_id: str
    airflow: float
    enabled: bool


def configure(
    **config: Unpack[EquipmentConfig]
) -> None:
    ...
```

Call:

```python
configure(
    equipment_id="AHU-01",
    airflow=2500.0,
    enabled=True
)
```

Yahi **Lesson 77 ka core pattern** hai.

---

# 38. Final cheat sheet

```text
TypedDict
↓
dictionary ka exact static shape
```

```text
Unpack[TypedDict]
↓
TypedDict ke fields ko **kwargs ke shape mein expand karo
```

```text
**kwargs: Unpack[Config]
↓
kwargs ke known keys + exact value types
```

```text
NotRequired[T]
↓
key optional
```

```text
Required[T]
↓
key required
```

```text
ParamSpec
↓
function ke complete parameters
```

```text
Concatenate
↓
fixed prefix + ParamSpec
```

---

## Golden rule

> **`TypedDict` batata hai dictionary mein kya keys aur types hain; `Unpack` us dictionary ke schema ko `**kwargs` ke type-safe keyword parameters mein expand karta hai.**

Aur ek deeper connection:

```text
TypedDict + Unpack
        ↓
dictionary shape → function keyword shape

ParamSpec
        ↓
function parameter shape → preserve

Concatenate
        ↓
function parameter shape → prefix ke saath transform
```

Isliye **Lesson 75, 76 aur 77** ko ek family samjho:

```text
ParamSpec
   ↓
"parameters ko capture karo"

Concatenate
   ↓
"parameters ke start mein fixed types joro"

Unpack
   ↓
"structured type ko expand karo"
```
# Lesson 78 — `typing.TypeVarTuple` — Variadic Generics

Aaj hum **`TypeVarTuple`** ko start se deeply samjhenge. Ye Python typing ka advanced concept hai aur iska main purpose hai:

> **Generic type mein unknown number of types ko ek saath represent karna.**

Normal `TypeVar` ek type represent karta hai:

```python
T = TypeVar("T")
```

Lekin `TypeVarTuple` **multiple types ki sequence** represent karta hai:

```python
Ts = TypeVarTuple("Ts")
```

Yani:

```text
T
↓
ek type

Ts
↓
zero ya multiple types
```

---

# 1. Problem kya solve hoti hai?

Pehle ek normal generic function dekho:

```python
from typing import TypeVar

T = TypeVar("T")

def get_value(value: T) -> T:
    return value
```

Agar:

```python
x = get_value(10)
```

to:

```text
T = int
```

Aur:

```python
x = get_value("Hello")
```

to:

```text
T = str
```

Yahan sirf **ek type variable** hai.

Lekin maan lo hamare paas tuple hai:

```python
(10, "Ali", 25.5, True)
```

Is tuple ke types hain:

```text
int
str
float
bool
```

Ab question:

**Agar tuple ke andar types ki quantity fixed na ho to typing kaise karein?**

Example:

```python
(10, "Ali")
```

types:

```text
int, str
```

Aur:

```python
(10, "Ali", 25.5)
```

types:

```text
int, str, float
```

Aur:

```python
(10, "Ali", 25.5, True, "HVAC")
```

types:

```text
int, str, float, bool, str
```

Yahan normal `TypeVar` sufficient nahi hai.

Isi problem ke liye:

```python
TypeVarTuple
```

hai.

---

# 2. Basic syntax

```python
from typing import TypeVarTuple

Ts = TypeVarTuple("Ts")
```

Yahan:

```python
Ts
```

ek **type variable tuple** hai.

Isko mentally aise samjho:

```text
Ts = (T1, T2, T3, T4, ...)
```

Lekin actual number fixed nahi hai.

For example:

```text
Ts = ()
```

ya:

```text
Ts = (int,)
```

ya:

```text
Ts = (int, str)
```

ya:

```text
Ts = (int, str, float, bool)
```

Isliye isko **variadic** kaha jata hai.

---

# 3. Variadic ka meaning

"Variadic" ka simple meaning:

> **Number of items/types fixed nahi hai.**

Example function:

```python
def add(*values):
    ...
```

`values` mein kitne arguments aa sakte hain?

```python
add()
add(10)
add(10, 20)
add(10, 20, 30)
add(10, 20, 30, 40, 50)
```

Number variable hai.

Ye runtime mein **variadic arguments** hain.

`TypeVarTuple` isi concept ko **type level** par represent karta hai.

```text
*args
↓
runtime values ki variable quantity

TypeVarTuple
↓
type-level types ki variable quantity
```

---

# 4. `TypeVar` vs `TypeVarTuple`

Ye distinction bohat important hai.

### TypeVar

```python
T = TypeVar("T")
```

Ek type:

```text
T = int
```

### TypeVarTuple

```python
Ts = TypeVarTuple("Ts")
```

Multiple types ki sequence:

```text
Ts = (int, str, float)
```

Comparison:

```text
TypeVar
    ↓
    T
    ↓
    one type


TypeVarTuple
    ↓
    Ts
    ↓
    multiple types
```

---

# 5. `tuple[Unpack[Ts]]`

Ab TypeVarTuple ka sabse important syntax:

```python
tuple[Unpack[Ts]]
```

Example:

```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple("Ts")

def make_tuple(*values: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return values
```

Ye pehli baar thoda confusing lag sakta hai.

Isko slowly samjho.

---

# 6. `Unpack` yahan kya kar raha hai?

Suppose:

```text
Ts = (int, str, float)
```

To:

```python
Unpack[Ts]
```

conceptually:

```text
int, str, float
```

Aur:

```python
tuple[Unpack[Ts]]
```

conceptually:

```python
tuple[int, str, float]
```

So:

```python
def make_tuple(*values: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return values
```

ka matlab hai:

> Jo jitne types input mein aayein, output tuple mein unhi types ka sequence preserve karo.

---

# 7. Practical example

```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple("Ts")

def make_tuple(*values: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return values
```

Call:

```python
result = make_tuple(10, "Ali", 25.5)
```

Type checker conceptually infer karega:

```text
Ts = (int, str, float)
```

Therefore:

```text
result
↓
tuple[int, str, float]
```

Important point:

Ye sirf:

```python
tuple[object, ...]
```

nahi hai.

Type information preserve ho rahi hai.

---

# 8. Why not simply `tuple[T, ...]`?

Ye bohat important difference hai.

Agar:

```python
T = TypeVar("T")
```

to:

```python
tuple[T, ...]
```

ka matlab hai:

> Tuple mein zero ya more values hain, aur sab ka type same `T` hai.

Example:

```python
def numbers(values: tuple[T, ...]) -> tuple[T, ...]:
    return values
```

Valid:

```python
(1, 2, 3)
```

because:

```text
tuple[int, int, int]
```

Lekin mixed tuple:

```python
(1, "Ali", 25.5)
```

iske liye `tuple[T, ...]` appropriate nahi hai, because types different hain.

`TypeVarTuple` mixed heterogeneous tuple ko preserve kar sakta hai:

```text
(int, str, float)
```

---

# 9. `TypeVarTuple` ka real power

Suppose:

```python
def reverse(values):
    ...
```

Hum chahte hain:

```text
input:
tuple[int, str, float]

output:
tuple[float, str, int]
```

Yahan types ki **quantity bhi variable** hai aur **order bhi important** hai.

TypeVarTuple exactly isi tarah ke cases ke liye useful hai.

---

# 10. `*Ts` syntax

Modern Python typing mein aap `Unpack[Ts]` ke equivalent shorthand ke liye:

```python
*Ts
```

use kar sakte ho, jahan supported ho.

Example:

```python
from typing import TypeVarTuple

Ts = TypeVarTuple("Ts")

def make_tuple(*values: *Ts) -> tuple[*Ts]:
    return values
```

Conceptually:

```python
tuple[*Ts]
```

same idea express karta hai:

```python
tuple[Unpack[Ts]]
```

For learning, pehle ye mental model rakho:

```text
Unpack[Ts]
=
Ts ko expand karo
```

---

# 11. `TypeVarTuple` + `Unpack`

Suppose:

```text
Ts = (int, str, float)
```

Then:

```python
tuple[Unpack[Ts]]
```

becomes conceptually:

```python
tuple[int, str, float]
```

Aur:

```python
tuple[Unpack[Ts], bool]
```

conceptually:

```python
tuple[int, str, float, bool]
```

Yani `Unpack` type sequence ko expand karta hai.

---

# 12. TypeVarTuple sirf tuple ke liye nahi

Naam dekh kar lag sakta hai:

```text
TypeVarTuple
=
sirf tuple
```

Lekin actually ye **types ki variadic sequence** represent karta hai.

Iska use especially generic structures mein hota hai.

Examples:

```text
tuple shapes
array dimensions
matrix dimensions
database query results
heterogeneous records
function parameter-like type sequences
```

---

# 13. Array shape example

Ye TypeVarTuple ka famous use case hai.

Suppose numerical array:

```text
Array[float, 3, 224, 224]
```

meaning:

```text
3 channels
224 height
224 width
```

Ya:

```text
Array[float, 224, 224]
```

2D image.

Ya:

```text
Array[float, 10, 3, 224, 224]
```

5 dimensions.

Problem:

Number of dimensions fixed nahi hai.

Isliye:

```text
TypeVarTuple
```

perfect fit hai.

Conceptually:

```python
Shape = TypeVarTuple("Shape")
```

Then:

```python
Array[float, Unpack[Shape]]
```

could represent:

```text
Array[float, 224, 224]

Array[float, 3, 224, 224]

Array[float, 10, 3, 224, 224]
```

---

# 14. HVAC example

Aapke HVAC context mein imagine karo sensor data.

Ek equipment ke readings:

```python
(
    "AHU-01",
    22.5,
    1200,
    True
)
```

Types:

```text
str
float
int
bool
```

Agar different equipment types ke records mein fields ki quantity variable ho sakti hai, `TypeVarTuple` heterogeneous record typing ko represent karne mein useful ho sakta hai.

Example conceptually:

```text
EquipmentRecord[
    str,
    float,
    int,
    bool
]
```

meaning:

```text
Equipment ID → str
Temperature → float
Airflow → int
Running → bool
```

Another record:

```text
EquipmentRecord[
    str,
    float,
    int,
    bool,
    float
]
```

Extra pressure field bhi aa gaya.

Yahan fixed number of generic parameters sufficient nahi hota.

---

# 15. Database example

Imagine query result:

```python
row = (
    "MEP-KHN-REF04",
    "Refrigerator",
    34.5,
    True
)
```

Types:

```text
str
str
float
bool
```

Ek generic query abstraction potentially:

```text
Row[str, str, float, bool]
```

aur doosri query:

```text
Row[int, str]
```

Yahan variadic generic useful ho sakta hai.

---

# 16. `TypeVarTuple` vs `*args`

Ye distinction yaad rakho:

```python
def f(*args):
```

runtime concept hai.

```python
Ts = TypeVarTuple("Ts")
```

type-system concept hai.

So:

```text
*args
↓
runtime values

TypeVarTuple
↓
static types
```

Aur:

```python
*values: Unpack[Ts]
```

dono concepts ko connect karta hai:

```text
runtime:
multiple arguments

typing:
multiple corresponding types
```

---

# 17. `TypeVarTuple` vs `TypeVar`

Example:

```python
T = TypeVar("T")
```

Agar:

```python
T = int
```

to ek hi type.

But:

```python
Ts = TypeVarTuple("Ts")
```

could represent:

```text
Ts = (int, str, float, bool)
```

Table:

| Feature             | TypeVar              | TypeVarTuple      |
| ------------------- | -------------------- | ----------------- |
| Represents          | one type             | multiple types    |
| Quantity            | fixed 1              | variable          |
| Heterogeneous types | no sequence          | yes               |
| Example             | `T = int`            | `Ts = (int, str)` |
| Main use            | generic relationship | variadic generics |

---

# 18. `TypeVarTuple` vs `tuple[T, ...]`

Ye bhi important:

```python
tuple[T, ...]
```

means:

```text
same type repeated
```

Example:

```text
(int, int, int, int)
```

While:

```python
tuple[Unpack[Ts]]
```

means:

```text
different types allowed
```

Example:

```text
(int, str, float, bool)
```

Mental model:

```text
tuple[T, ...]
        ↓
same type, variable quantity


tuple[Unpack[Ts]]
        ↓
different types, variable quantity
```

---

# 19. `TypeVarTuple` vs `ParamSpec`

Dono superficially similar lagte hain because dono multiple things capture kar sakte hain.

But domain different hai.

### ParamSpec

Function parameters ke liye:

```python
P = ParamSpec("P")
```

Conceptually:

```text
(name: str, age: int, active: bool)
```

complete function parameter specification.

### TypeVarTuple

Types ki arbitrary sequence:

```python
Ts = TypeVarTuple("Ts")
```

Conceptually:

```text
(int, str, float, bool)
```

Comparison:

```text
ParamSpec
    ↓
function signature

TypeVarTuple
    ↓
type sequence
```

---

# 20. `TypeVarTuple` vs `Unpack`

Ye bhi confuse mat karna.

```python
Ts = TypeVarTuple("Ts")
```

defines:

> types ki variadic sequence.

While:

```python
Unpack[Ts]
```

means:

> us sequence ko expand karo.

So:

```text
TypeVarTuple
↓
container of type variables

Unpack
↓
expand those type variables
```

Example:

```python
Ts = TypeVarTuple("Ts")
```

Then:

```python
tuple[Unpack[Ts]]
```

means:

```text
tuple containing all types represented by Ts
```

---

# 21. Star operator ka mental model

Runtime Python mein:

```python
numbers = (1, 2, 3)

[*numbers]
```

means values unpack karna.

Typing mein:

```python
Ts = TypeVarTuple("Ts")
```

and:

```python
tuple[Unpack[Ts]]
```

means type sequence unpack karna.

So:

```text
runtime:

*values
↓
values expand


typing:

Unpack[Ts]
↓
types expand
```

Ye mental model bohat useful hai.

---

# 22. Important: TypeVarTuple runtime object nahi banata

Ye:

```python
Ts = TypeVarTuple("Ts")
```

koi actual tuple of runtime values nahi hai.

Ye:

```python
Ts = (int, str, float)
```

runtime assignment bhi nahi karta.

Ye **static typing metadata** hai.

Isliye:

```python
Ts
```

ko runtime data container samajhna mistake hai.

---

# 23. Real-world architecture mein faida

TypeVarTuple ka main benefit:

### 1. Variable number of type parameters

Fixed:

```python
class Pair(Generic[T1, T2]):
    ...
```

sirf 2 types.

Variadic:

```text
Record[T1, T2, T3, T4, ...]
```

arbitrary count.

---

### 2. Heterogeneous data preserve karna

Instead of:

```python
tuple[object, ...]
```

you can preserve:

```text
tuple[int, str, float, bool]
```

---

### 3. Type-safe transformations

Aap ek type sequence ko transform kar sakte ho.

Example concept:

```text
Input:
(int, str, float)

Transformation:
add bool at beginning

Output:
(bool, int, str, float)
```

Yahan variadic generic architecture powerful hoti hai.

---

### 4. Shape-aware numerical programming

Especially:

```text
NumPy-style arrays
tensor libraries
matrix operations
ML frameworks
```

mein dimensions ko type-level par represent karna useful hai.

---

# 24. Sabse important mental model

Isko yaad kar lo:

```text
TypeVar
    ↓
one unknown type

TypeVarTuple
    ↓
many unknown types

ParamSpec
    ↓
unknown function parameter specification

Unpack
    ↓
variadic type sequence ko expand karo
```

Aur:

```text
T
↓
int


Ts
↓
(int, str, float)
```

Then:

```python
tuple[Unpack[Ts]]
```

becomes conceptually:

```python
tuple[int, str, float]
```

---

# 25. Ek complete example

```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple("Ts")


def make_record(*values: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return values


record = make_record(
    "MEP-KHN-REF04",
    22.5,
    1200,
    True
)
```

Conceptually type inference:

```text
Ts
=
(
    str,
    float,
    int,
    bool
)
```

Therefore:

```text
record
=
tuple[
    str,
    float,
    int,
    bool
]
```

Notice kya preserve hua?

```text
1. number of types
2. type of each item
3. order of types
```

Yehi `TypeVarTuple` ki actual power hai.

---

# 26. One-line definition

Agar interview mein poocha jaye:

> **What is TypeVarTuple?**

To simple answer:

> **`TypeVarTuple` Python typing mein variadic generic type variable hai jo zero ya more type variables ki sequence ko represent karta hai, especially heterogeneous generic structures ke liye.**

Roman Urdu mein:

> **TypeVarTuple aisa type variable hai jo sirf ek type nahi, balki variable number mein multiple types ki sequence represent karta hai.**

---

## Next depth

Lesson 78 ka next advanced part naturally ye hoga:

```text
TypeVarTuple
    ↓
Unpack
    ↓
generic classes
    ↓
variadic generic classes
    ↓
TypeVarTuple + Generic
    ↓
TypeVarTuple + overload
    ↓
TypeVarTuple + TypeVar
    ↓
TypeVarTuple + ParamSpec
    ↓
tuple transformation
    ↓
array/matrix shape typing
```

Sabse important next concept **`TypeVarTuple` ke saath generic class banana** hai, kyunki wahaan clear hoga ke `Generic[*Ts]` actually kaise kaam karta hai.
# Lesson 79 — `typing.dataclass_transform` — Custom Dataclass Decorators

Aaj ka topic thoda advanced hai, lekin iska core concept simple hai:

> **`dataclass_transform` type checker ko batata hai ke hamara custom decorator/class decorator/framework, `@dataclass` jaisa behavior provide karta hai.**

Yani hum apna **custom dataclass system** bana sakte hain aur type checker ko bata sakte hain ke:

> "Is decorator ko dataclass ki tarah treat karo."

---

# 1. Pehle problem samjho

Normal Python mein:

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    temperature: float
```

`@dataclass` automatically useful methods generate karta hai, jaise:

```text
__init__()
__repr__()
__eq__()
```

So:

```python
e = Equipment("AHU-01", 22.5)
```

automatically kaam karta hai.

---

# 2. Lekin agar apna decorator banana ho?

Suppose hum facility-management application bana rahe hain.

Hum chahte hain:

```python
@model
class Equipment:
    equipment_id: str
    temperature: float
```

Aur hum chahte hain ke `@model`:

* constructor generate kare
* fields recognize kare
* defaults handle kare
* type checker ko dataclass jaisa behavior dikhaye

Runtime par hum ye functionality khud implement kar sakte hain.

Lekin problem hai:

**Static type checker ko kaise pata chalega ke `@model` dataclass jaisa hai?**

Yahan:

```python
dataclass_transform
```

ka role start hota hai.

---

# 3. Basic syntax

```python
from typing import dataclass_transform
```

Phir:

```python
@dataclass_transform()
def model(cls):
    ...
```

Ab type checker ko signal milta hai:

```text
@model
↓
dataclass-like transformation
```

---

# 4. `dataclass_transform()` khud dataclass nahi banata

Ye bohat important point hai.

Agar:

```python
from typing import dataclass_transform

@dataclass_transform()
def model(cls):
    return cls
```

to `dataclass_transform()` automatically:

```text
__init__
__repr__
__eq__
```

generate nahi karta.

Ye sirf **static typing information** provide karta hai.

Runtime behavior decorator ko khud implement karna hoga.

Mental model:

```text
dataclass
↓
runtime + typing behavior


dataclass_transform
↓
typing/type-checker behavior
```

Runtime transformation:

```text
aapka decorator
```

---

# 5. Simple custom decorator

Pehle runtime decorator:

```python
from dataclasses import dataclass

def model(cls):
    return dataclass(cls)
```

Ab:

```python
@model
class Equipment:
    equipment_id: str
    temperature: float
```

Runtime par `model()` internally:

```python
dataclass(cls)
```

call kar raha hai.

Lekin static type checker ko ye necessarily nahi pata ke:

```text
@model
```

constructor generate karega.

Isliye:

```python
from typing import dataclass_transform

@dataclass_transform()
def model(cls):
    return dataclass(cls)
```

Ab humne dono layers connect kar di:

```text
@model
    │
    ├── Runtime → dataclass()
    │
    └── Static typing → dataclass_transform()
```

---

# 6. Practical example

```python
from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform()
def model(cls):
    return dataclass(cls)


@model
class Equipment:
    equipment_id: str
    temperature: float


equipment = Equipment(
    "AHU-01",
    22.5
)
```

Type checker `Equipment(...)` ko dataclass-like constructor ke taur par understand kar sakta hai.

Conceptually:

```text
Equipment(
    equipment_id: str,
    temperature: float
)
```

---

# 7. Why is this needed?

Imagine large framework.

Aap directly:

```python
@dataclass
class User:
    ...
```

nahi karna chahte.

Instead framework apna decorator provide karta hai:

```python
@model
class User:
    ...
```

Examples of framework-style patterns:

```text
@model
@Entity
@Table
@schema
@component
@config
@document
```

Framework internally classes ko transform kar sakta hai.

Type checker ko agar ye transformation samajh nahi aati to developer ko incorrect warnings mil sakti hain.

`dataclass_transform` is gap ko solve karta hai.

---

# 8. `dataclass_transform` ka actual purpose

Iska purpose ye nahi:

> "Dataclass create karo."

Balki:

> "Type checker ko batao ke ye decorator dataclass-like class transformation perform karta hai."

Ye distinction bohat important hai.

---

# 9. `dataclass_transform` ke three common forms

Ye decorator teen major places par use ho sakta hai:

### 1. Function decorator

```python
@dataclass_transform()
def model(cls):
    ...
```

### 2. Class decorator

```python
@dataclass_transform()
class ModelBase:
    ...
```

### 3. Metaclass

```python
@dataclass_transform()
class ModelMeta(type):
    ...
```

Matlab dataclass-like behavior sirf ek simple function decorator tak limited nahi hai.

---

# 10. Custom field specifiers

Ab topic aur interesting ho jata hai.

Dataclass mein:

```python
from dataclasses import field

@dataclass
class Equipment:
    equipment_id: str
    temperature: float = field(default=20.0)
```

Custom framework apna field function bana sakta hai:

```python
def model_field(...):
    ...
```

Example:

```python
@dataclass_transform(
    field_specifiers=(model_field,)
)
def model(cls):
    ...
```

Yahan:

```python
field_specifiers=(model_field,)
```

type checker ko batata hai:

> `model_field` hamare framework ka dataclass-like field declaration mechanism hai.

---

# 11. Field specifier kyun?

Suppose framework:

```python
@model
class Equipment:
    equipment_id: str = model_field(...)
    temperature: float = model_field(default=20.0)
```

Framework ko samajh hai:

```text
equipment_id
temperature
```

fields hain.

Lekin type checker ko bhi ye semantics samajhni chahiye.

`field_specifiers` isi purpose ke liye hai.

---

# 12. `eq_default`

`dataclass_transform()` mein kuch parameters type checker ko expected dataclass behavior batate hain.

Example:

```python
@dataclass_transform(eq_default=True)
def model(cls):
    ...
```

Meaning conceptually:

> Agar user ne equality behavior explicitly specify nahi kiya, to generated model equality support karega.

Yani:

```python
a == b
```

expected behavior ka static model type checker ko diya ja raha hai.

---

# 13. `order_default`

Similarly:

```python
@dataclass_transform(order_default=True)
```

type checker ko indicate karta hai ke transformed classes ordering methods support kar sakti hain:

```python
<
<=
>
>=
```

Conceptually:

```python
equipment1 < equipment2
```

---

# 14. `kw_only_default`

Ye constructor behavior se related hai.

```python
@dataclass_transform(kw_only_default=True)
```

ka conceptual meaning:

> Fields by default keyword-only constructor parameters ho sakte hain.

Example:

```python
Equipment(
    equipment_id="AHU-01",
    temperature=22.5
)
```

instead of:

```python
Equipment(
    "AHU-01",
    22.5
)
```

---

# 15. `frozen_default`

```python
@dataclass_transform(frozen_default=True)
```

type checker ko indicate kar sakta hai ke transformed classes default taur par immutable/frozen semantics follow karti hain.

Conceptually:

```python
equipment.temperature = 25.0
```

type checker isko invalid maan sakta hai depending on framework semantics.

Again:

**`dataclass_transform` khud object ko freeze nahi karta.**

Runtime implementation ko karna padega.

---

# 16. Static typing vs runtime

Ye lesson ka sabse important concept hai.

Suppose:

```python
from typing import dataclass_transform

@dataclass_transform()
def model(cls):
    return cls
```

Aap soch sakte ho:

> "Ab class dataclass ban gayi?"

No.

Runtime:

```text
model()
↓
class unchanged
```

Type checker:

```text
model()
↓
dataclass-like semantics assume karo
```

Isliye:

```text
dataclass_transform
        ↓
       TYPE
       CHECKER
```

not:

```text
dataclass_transform
        ↓
     RUNTIME
```

---

# 17. Ek complete conceptual architecture

Imagine framework:

```python
from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform()
def model(cls):
    return dataclass(cls)
```

Then:

```python
@model
class WorkOrder:
    work_order_id: str
    description: str
    priority: int
```

Architecture:

```text
                 @model
                    │
          ┌─────────┴─────────┐
          │                   │
      Runtime             Type Checker
          │                   │
       dataclass()       dataclass-like
          │                 semantics
          │                   │
          └─────────┬─────────┘
                    ↓
              WorkOrder
```

Yahi real-world use hai.

---

# 18. Frameworks mein iska faida

Ye feature particularly useful hai jab framework apna model system banata hai.

Example architecture:

```text
Application
    │
    ├── Models
    │      ├── Equipment
    │      ├── WorkOrder
    │      └── Technician
    │
    └── Framework
           │
           └── @model
```

Developer:

```python
@model
class WorkOrder:
    number: str
    description: str
    priority: int
```

Framework internally:

```text
fields discover
constructor generate
validation setup
serialization setup
database mapping
```

Aur `dataclass_transform`:

```text
static analyzer ko semantics batata hai
```

---

# 19. SQLAlchemy-style thinking

Is concept ko ORM architecture se relate karna useful hai.

Imagine:

```python
@model
class Equipment:
    equipment_id: str
    name: str
    temperature: float
```

Framework internally:

```text
class annotations
       ↓
field discovery
       ↓
database mapping
       ↓
constructor / comparison / etc.
```

Type checker ko bhi batana hota hai:

```text
ye normal class nahi hai
ye transformed model hai
```

`dataclass_transform` isi category ke framework APIs ke liye designed hai.

---

# 20. `dataclass_transform` vs `dataclass`

Very important comparison:

| Feature                            | `@dataclass` | `@dataclass_transform` |
| ---------------------------------- | ------------ | ---------------------- |
| Runtime transformation             | Yes          | No                     |
| `__init__` generate karta hai      | Yes          | No                     |
| Type checker ko semantics deta hai | Yes          | Yes                    |
| Custom framework ke liye           | Limited      | Excellent              |
| Custom decorator support           | N/A          | Yes                    |
| Custom field specifiers            | `field()`    | `field_specifiers`     |

Simple mental model:

```text
@dataclass
    ↓
"Class ko actually transform karo"


@dataclass_transform
    ↓
"Type checker ko batao ke mera transformer
 dataclass jaisa behave karta hai"
```

---

# 21. `dataclass_transform` vs `Protocol`

Ye bhi confuse ho sakta hai.

### Protocol

Batata hai:

> Class ko kaunse attributes/methods provide karne chahiye?

Example:

```python
class Repository(Protocol):
    def save(self, item) -> None:
        ...
```

### dataclass_transform

Batata hai:

> Decorator/metaclass class ko dataclass-like fields/constructor semantics deta hai.

So:

```text
Protocol
↓
structure/interface


dataclass_transform
↓
class transformation semantics
```

---

# 22. `dataclass_transform` vs `Generic`

`Generic`:

```python
class Repository(Generic[T]):
    ...
```

means:

> Class generic type parameters support karti hai.

`dataclass_transform`:

```python
@dataclass_transform()
def model(cls):
    ...
```

means:

> Decorator dataclass-like transformation provide karta hai.

Dono completely different problems solve karte hain.

---

# 23. Constructor checking ka faida

Suppose:

```python
@dataclass_transform()
def model(cls):
    return dataclass(cls)


@model
class Equipment:
    equipment_id: str
    temperature: float
```

Expected constructor:

```python
Equipment(
    equipment_id: str,
    temperature: float
)
```

Agar developer:

```python
Equipment(
    123,
    "hot"
)
```

likhta hai, static type checker incorrect argument types detect kar sakta hai.

Yani custom framework ke bawajood:

```text
strong typing
```

preserve rehti hai.

---

# 24. Custom field specifier example

Conceptually:

```python
from typing import dataclass_transform


class Field:
    def __init__(self, default=None):
        self.default = default


def model_field(default=None):
    return Field(default)


@dataclass_transform(
    field_specifiers=(model_field,)
)
def model(cls):
    ...
```

Then:

```python
@model
class Equipment:
    equipment_id: str
    temperature: float = model_field(20.0)
```

Type checker ko pata hai:

```text
model_field()
↓
dataclass-like field declaration
```

---

# 25. Why not just use `dataclass`?

Good question.

Agar application simple hai:

```python
@dataclass
class Equipment:
    ...
```

to `dataclass_transform` ki zaroorat nahi.

Ye primarily useful hai jab:

```text
framework
ORM
validation library
dependency injection framework
serialization framework
model system
custom decorator system
```

apna dataclass-like mechanism provide karta hai.

---

# 26. Real-world mental model

Suppose aap apna framework bana rahe ho:

```python
@entity
class Equipment:
    id: str
    temperature: float
```

`@entity` internally:

```text
1. fields discover karta hai
2. __init__ create karta hai
3. validation add karta hai
4. database mapping karta hai
5. serialization add karta hai
```

Agar aap:

```python
@dataclass_transform()
def entity(cls):
    ...
```

likhte ho, to static type checker ko keh rahe ho:

> "`@entity` ke through transformed classes ko dataclass-like semantics ke saath analyze karo."

Ye **framework authoring feature** hai.

---

# 27. Ek aur important distinction: implementation vs declaration

`dataclass_transform` ko ek **contract/declaration** samjho.

```python
@dataclass_transform()
def entity(cls):
    ...
```

Ye essentially type checker ko contract deta hai:

```text
entity()
    ↓
class transformation
    ↓
dataclass-like behavior
```

Lekin actual implementation:

```python
def entity(cls):
    ...
```

aapko khud likhni hogi.

---

# 28. Golden mental model

Is lesson ke 4 concepts:

```text
@dataclass
    ↓
actual dataclass transformation


@dataclass_transform
    ↓
tell type checker about custom transformation


field_specifiers
    ↓
tell type checker about custom field declarations


custom decorator
    ↓
actual runtime transformation
```

---

# 29. Ek complete conceptual example

```python
from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform()
def model(cls):
    return dataclass(cls)


@model
class Equipment:
    equipment_id: str
    temperature: float


equipment = Equipment(
    "AHU-01",
    22.5
)

print(equipment)
```

Runtime flow:

```text
@model
   ↓
model(Equipment)
   ↓
dataclass(Equipment)
   ↓
generated __init__, __repr__, __eq__
```

Static typing flow:

```text
@model
   ↓
dataclass_transform
   ↓
type checker understands
dataclass-like behavior
```

Dono layers ko combine karna hi iska real purpose hai.

---

# 30. Lesson 79 ka final summary

```text
dataclass
    ↓
runtime dataclass behavior


dataclass_transform
    ↓
custom dataclass-like framework ko
type checker ke saath describe karna
```

### `TypeVarTuple` se connection

Pichli lesson mein:

```python
Ts = TypeVarTuple("Ts")
```

se humne **variable number of types** represent kiye.

Aaj:

```python
@dataclass_transform()
```

se hum **custom class transformation ki typing semantics** describe kar rahe hain.

Yani Python typing ka scope ab:

```text
TypeVar
    ↓
Generic
    ↓
Protocol
    ↓
TypeVarTuple
    ↓
ParamSpec
    ↓
dataclass_transform
```

tak aa gaya hai.

**One-line definition:**

> `dataclass_transform` ek typing decorator hai jo static type checkers ko batata hai ke koi custom decorator, base class, ya metaclass dataclass-jaisi class transformation aur field/constructor semantics provide karta hai—runtime transformation khud `dataclass_transform` nahi karta.
# Lesson 80 — `typing.deprecated` — Marking Deprecated APIs

Aaj ka topic **API design aur library maintenance** se related hai.

Ek simple problem se start karte hain:

Aapki library mein purana function hai:

```python
def get_temperature():
    ...
```

Lekin aapne iska better version bana diya:

```python
def get_temperature_celsius():
    ...
```

Ab aap chahte ho ke purana function **abhi immediately delete na ho**, lekin developers ko warning mile:

> "Ye API purani hai. Nayi API use karo."

Isi purpose ke liye Python typing mein:

```python
typing.deprecated
```

use hota hai.

---

# 1. Deprecated ka meaning

**Deprecated** ka matlab:

> API abhi available hai, lekin future mein remove/change ho sakti hai aur users ko iska alternative use karna chahiye.

Example:

```text
Old API
    ↓
still works
    ↓
but deprecated
    ↓
use new API
    ↓
eventually old API remove
```

Ye important hai:

```text
deprecated ≠ removed
```

Agar API removed hoti:

```python
old_function()
```

exist hi nahi karti.

Deprecated mein:

```python
old_function()
```

abhi exist karti hai.

---

# 2. Basic syntax

Modern Python typing mein:

```python
from typing import deprecated
```

Phir:

```python
@deprecated("Use new_function() instead.")
def old_function():
    ...
```

Example:

```python
from typing import deprecated


@deprecated("Use get_temperature_celsius() instead.")
def get_temperature():
    return 22.5
```

Ab developer ko signal milta hai:

```text
get_temperature()
        ↓
    DEPRECATED
        ↓
Use get_temperature_celsius()
```

---

# 3. Sabse important point

`typing.deprecated` ka primary purpose **static type checkers aur API documentation/tooling ko deprecation information dena** hai.

Ye automatically ye guarantee nahi karta ke:

```python
old_function()
```

runtime par warning zaroor print hogi.

Yani:

```text
typing.deprecated
        ↓
static/tooling metadata
```

not necessarily:

```text
typing.deprecated
        ↓
runtime warning
```

Agar aapko runtime warning chahiye, to `warnings` module use karna hota hai.

---

# 4. `typing.deprecated` vs `warnings.warn`

Ye distinction bohat important hai.

### `typing.deprecated`

```python
from typing import deprecated

@deprecated("Use new_function()")
def old_function():
    ...
```

Purpose:

```text
type checker / IDE / API tooling
```

### `warnings.warn`

```python
import warnings

def old_function():
    warnings.warn(
        "Use new_function() instead.",
        DeprecationWarning,
        stacklevel=2
    )
```

Purpose:

```text
runtime warning
```

So:

```text
deprecated
    ↓
static/API metadata


warnings.warn
    ↓
runtime behavior
```

---

# 5. Dono ko combine karna

Production library mein aap dono use kar sakte ho:

```python
from typing import deprecated
import warnings


@deprecated("Use get_temperature_celsius() instead.")
def get_temperature():
    warnings.warn(
        "get_temperature() is deprecated; "
        "use get_temperature_celsius() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return 22.5
```

Ab:

```text
IDE/type checker
        ↓
DEPRECATED

Runtime
        ↓
DeprecationWarning
```

Ye strong migration strategy hai.

---

# 6. Why deprecation zaroori hai?

Suppose aapki library ke 500 users hain.

Aapke paas:

```python
get_temperature()
```

hai.

Aap ise directly delete kar dete ho:

```text
Version 1
get_temperature()

Version 2
❌ get_temperature removed
```

Users ke existing code break ho sakte hain.

Better approach:

```text
Version 1
get_temperature()

Version 2
get_temperature() → deprecated
get_temperature_celsius() → new

Version 3
get_temperature() → maybe removed
```

Yani deprecation **migration period** provide karti hai.

---

# 7. Function ko deprecated karna

Simple:

```python
from typing import deprecated


@deprecated("Use calculate_airflow() instead.")
def airflow():
    return 1200
```

New API:

```python
def calculate_airflow():
    return 1200
```

Developer ko old API se new API ki taraf migrate karna hai.

---

# 8. Class ko deprecated karna

Sirf functions nahi.

Class bhi deprecated ho sakti hai:

```python
from typing import deprecated


@deprecated("Use ModernEquipment instead.")
class OldEquipment:
    pass
```

Then:

```python
equipment = OldEquipment()
```

Type-checking/IDE tooling deprecated status show kar sakti hai.

---

# 9. Method ko deprecated karna

```python
class Equipment:

    @deprecated("Use get_temperature_celsius() instead.")
    def get_temperature(self):
        return 22.5

    def get_temperature_celsius(self):
        return 22.5
```

Ab:

```python
equipment.get_temperature()
```

old API hai.

While:

```python
equipment.get_temperature_celsius()
```

new API hai.

---

# 10. Property ko deprecated karna

Conceptually same pattern:

```python
class Equipment:

    @property
    @deprecated("Use temperature_celsius instead.")
    def temperature(self):
        return 22.5
```

Yahan ek important lesson hai:

**Decorator order matter kar sakta hai**, because `property` aur deprecation decorator dono transformation kar rahe hain.

Aapko apne type checker/framework ke expected decorator behavior ke mutabiq order test karna chahiye.

---

# 11. Deprecated message kyun important hai?

Bad:

```python
@deprecated("Old API")
```

Better:

```python
@deprecated(
    "Use get_temperature_celsius() instead."
)
```

Best migration message:

```python
@deprecated(
    "Use get_temperature_celsius() instead; "
    "get_temperature() will be removed in v3.0."
)
```

Developer ko teen cheezen milti hain:

```text
1. Current API deprecated hai
2. Replacement kya hai
3. Future mein kya hoga
```

---

# 12. API lifecycle

Deprecation ko ek lifecycle samjho:

```text
NEW
 ↓
SUPPORTED
 ↓
DEPRECATED
 ↓
REMOVED
```

Example:

```text
v1.0
get_temperature()
SUPPORTED

v2.0
get_temperature()
DEPRECATED

v3.0
get_temperature()
REMOVED
```

Ye software versioning mein bohat common pattern hai.

---

# 13. HVAC example

Suppose aapki building automation library mein:

```python
get_supply_air_temp()
```

old API hai.

New API:

```python
get_supply_air_temperature()
```

Aap:

```python
from typing import deprecated


@deprecated(
    "Use get_supply_air_temperature() instead."
)
def get_supply_air_temp():
    return 18.5
```

New:

```python
def get_supply_air_temperature():
    return 18.5
```

Ab existing applications immediately break nahi hoti.

Lekin developers ko migration signal milta hai.

---

# 14. Equipment API example

Old:

```python
get_equipment()
```

New:

```python
get_equipment_by_id()
```

```python
from typing import deprecated


@deprecated(
    "Use get_equipment_by_id() instead."
)
def get_equipment():
    ...
```

Ye especially useful hai jab API bahut badi ho aur multiple developers use kar rahe hon.

---

# 15. Library developer vs application developer

`deprecated` ka use sabse zyada **library/framework developers** ke liye useful hai.

Agar aap:

```text
Python package
SDK
API client
ORM
HVAC framework
internal company library
```

maintain karte ho, to APIs time ke saath evolve hoti hain.

Aapko old APIs ko immediately delete karne ke bajaye controlled migration deni hoti hai.

---

# 16. Deprecation ka main benefit

### Benefit 1 — Backward compatibility

Purana code:

```python
old_function()
```

abhi chal sakta hai.

---

### Benefit 2 — Migration signal

IDE/type checker developer ko bata sakta hai:

```text
Deprecated
Use new_function()
```

---

### Benefit 3 — Better API evolution

Aap API improve kar sakte ho without suddenly breaking every user.

---

### Benefit 4 — Technical debt control

Purane APIs eventually remove kiye ja sakte hain.

```text
old API
   ↓
deprecated
   ↓
migration
   ↓
removed
```

---

# 17. `deprecated` aur `Final` ka difference

Pichli lessons mein `Final` dekha tha.

### `Final`

```python
MAX_TEMP: Final = 50
```

Meaning:

> Is name ko reassign nahi karna chahiye.

### `deprecated`

```python
@deprecated("Use new_api()")
def old_api():
    ...
```

Meaning:

> Ye API use mat karo; replacement available hai.

So:

```text
Final
    ↓
prevent reassignment


deprecated
    ↓
discourage API usage
```

---

# 18. `deprecated` aur `NoReturn`

`NoReturn`:

```python
def fail() -> NoReturn:
    raise RuntimeError()
```

Meaning:

> Function normally return nahi karta.

`deprecated`:

```python
@deprecated("Use new_api()")
def old_api():
    ...
```

Meaning:

> Function/API old hai, replacement use karo.

Completely different concepts.

---

# 19. `deprecated` aur `Annotated`

`Annotated`:

```python
from typing import Annotated

temperature: Annotated[float, "Celsius"]
```

Meaning:

> Type ke saath metadata attach karo.

`deprecated`:

```python
@deprecated("Use new_api()")
```

Meaning:

> API deprecated metadata provide karo.

Conceptually:

```text
Annotated
    ↓
type + metadata


deprecated
    ↓
API + deprecation metadata
```

---

# 20. Important: deprecation validation nahi hai

Ye:

```python
@deprecated("Use new_api()")
def old_api():
    ...
```

automatically verify nahi karta ke:

```python
new_api()
```

actually exist karta hai.

Aap ye likh sakte ho:

```python
@deprecated("Use xyz()")
def old_api():
    ...
```

even if `xyz()` exist hi nahi karta.

Isliye replacement message accurate hona developer ki responsibility hai.

---

# 21. Type checker ka role

Modern static typing ecosystem mein type checker:

```text
source code
    ↓
find deprecated symbol
    ↓
diagnostic / warning
```

de de sakta hai.

IDE:

```text
old_function()
```

ko visually deprecated show kar sakta hai.

Exact diagnostic behavior **type checker/IDE par depend karta hai**.

Yani `typing.deprecated` ek standardized typing-level signal hai, lekin har tool ka UI/diagnostic behavior identical hona zaroori nahi.

---

# 22. Generic function bhi deprecated ho sakta hai

Suppose:

```python
from typing import TypeVar, deprecated

T = TypeVar("T")


@deprecated("Use process_new() instead.")
def process(value: T) -> T:
    return value
```

Yahan generic typing aur deprecation ek saath kaam kar sakte hain:

```text
T
↓
generic relationship

deprecated
↓
API lifecycle metadata
```

---

# 23. Decorator ka deeper architecture

Ab ek important architecture samjho.

```python
@deprecated("Use new_api()")
def old_api():
    ...
```

Conceptually:

```text
old_api
   ↓
decorated with deprecation metadata
   ↓
type checker sees metadata
   ↓
developer gets deprecation information
```

Iska main target **API consumers** hain.

---

# 24. Deprecation is communication

Is concept ko sirf typing feature mat samjho.

Deprecation actually:

> **API evolution communication mechanism**

hai.

Aap consumer ko communicate kar rahe ho:

```text
"Ye API abhi kaam karti hai,
lekin future-oriented code mein ise use mat karo."
```

Isliye good deprecation message:

```text
Old API
+
Reason
+
Replacement
+
Removal timeline
```

provide karta hai.

---

# 25. Strong migration example

Suppose old:

```python
get_airflow()
```

New:

```python
get_airflow_cfm()
```

Deprecation:

```python
@deprecated(
    "get_airflow() is deprecated; "
    "use get_airflow_cfm() instead. "
    "The old API will be removed in v3.0."
)
def get_airflow():
    return get_airflow_cfm()
```

Yahan old function internally new implementation ko call bhi kar raha hai.

Architecture:

```text
old API
   ↓
deprecated
   ↓
new implementation
```

Ye migration ke liye clean pattern ho sakta hai.

---

# 26. `deprecated` ka golden mental model

Isko yaad rakho:

```text
deprecated
     ↓
"API abhi exist karti hai"
     +
"API future-oriented code mein use nahi karni"
     +
"replacement available hai"
```

Aur:

```text
deprecated
≠
removed

deprecated
≠
runtime warning necessarily

deprecated
≠
automatic replacement
```

---

# 27. Previous lessons se connection

Ab tak typing system kaafi powerful ho gaya hai:

```text
TypeVar
    ↓
generic relationship

TypeVarTuple
    ↓
multiple variable types

ParamSpec
    ↓
function parameter specification

Unpack
    ↓
type sequence expansion

dataclass_transform
    ↓
custom dataclass-like framework semantics

deprecated
    ↓
API lifecycle metadata
```

Yani `typing` sirf:

```text
"variable ka type kya hai?"
```

tak limited nahi hai.

Modern Python typing:

```text
types
+
relationships
+
control flow
+
metadata
+
framework semantics
+
API lifecycle
```

ko describe kar sakti hai.

---

## Final one-line definition

> **`typing.deprecated` ek typing-level decorator hai jo function, class ya doosri supported API ko deprecated mark karta hai taa-ke static type checkers, IDEs aur related tooling consumers ko batayein ke API purani hai aur preferably replacement use karni chahiye.**

Aur sabse important distinction:

```text
@deprecated(...)
        ↓
"Don't use this API for new code."

warnings.warn(...)
        ↓
"Runtime par warning generate karo."
```

Dono ko combine karne se **static migration guidance + runtime warning** dono mil sakte hain.
