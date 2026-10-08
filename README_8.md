# Python OOP — Lessons 71-80 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 71: `typing.get_type_hints()` — Runtime Type Hints

## 1. Basic Concept

```python
def get_temperature(value: float) -> float:
    return value

from typing import get_type_hints

print(get_type_hints(get_temperature))
```

**Output:**
```
{'value': <class 'float'>, 'return': <class 'float'>}
```

**Explanation:**
- `get_type_hints()` → runtime par annotations retrieve aur resolve

## 2. `__annotations__` se Difference

```python
print(get_temperature.__annotations__)
```

**Output:**
```python
{"value": float, "return": float}
```

**Explanation:**
- `__annotations__` → raw data
- `get_type_hints()` → resolved

## 3. Mental Model

```
__annotations__ → raw
get_type_hints() → resolved
```

## 4. `list` Example

```python
def get_equipment_ids() -> list[str]:
    return ["AHU-001", "AHU-002"]

hints = get_type_hints(get_equipment_ids)
print(hints)
```

**Output:**
```
{'return': list[str]}
```

## 5. Parameters aur Return

```python
def calculate_airflow(fans: int, airflow_per_fan: float) -> float:
    return fans * airflow_per_fan

hints = get_type_hints(calculate_airflow)
# fans → int, airflow_per_fan → float, return → float
```

## 6. Real-World Use

```
Function → Type hints → Runtime framework → Validation/serialization
```

## 7. HVAC Example

```python
def create_ahu(equipment_id: str, floor: int, airflow: float) -> dict:
    return {...}

hints = get_type_hints(create_ahu)
# equipment_id → str, floor → int, airflow → float, return → dict
```

## 8. `Annotated` ke Saath

```python
from typing import Annotated

Airflow = Annotated[float, "CFM"]

def set_airflow(value: Airflow):
    pass

print(get_type_hints(set_airflow))
# Metadata strip ho sakti hai
```

## 9. `include_extras=True`

```python
hints = get_type_hints(set_airflow, include_extras=True)
# Annotated metadata preserve
```

## 10. Kyun Useful

```python
Airflow = Annotated[float, "CFM", "Range: 0-5000"]

hints = get_type_hints(set_airflow, include_extras=True)
# Type = float, Unit = CFM, Range = 0-5000
```

## 11. Forward References

```python
def get_ahu() -> "AHU":
    ...

get_ahu.__annotations__   # "AHU" (string)

hints = get_type_hints(get_ahu)
# AHU (resolved type)
```

## 12. `TYPE_CHECKING` Connection

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU

def get_ahu() -> AHU:
    ...

# get_type_hints() runtime par AHU resolve karne ki koshish karega
# Problem ho sakti hai agar AHU runtime par available nahi
```

## 13. Runtime Resolver

```
Annotation: "AHU"
    ↓
get_type_hints()
    ↓
"AHU ko actual class se resolve karo"
    ↓
AHU
```

## 14. Class ke Saath

```python
class AHU:
    equipment_id: str
    floor: int
    airflow: float

hints = get_type_hints(AHU)
# equipment_id → str, floor → int, airflow → float
```

## 15. Dataclass ke Saath

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    floor: int
    airflow: float

hints = get_type_hints(Equipment)
```

## 16. TypedDict ke Saath

```python
from typing import TypedDict, get_type_hints

class EquipmentData(TypedDict):
    equipment_id: str
    floor: int
    airflow: float

hints = get_type_hints(EquipmentData)
```

## 17. Runtime Validation Example

```python
def create_equipment(equipment_id: str, floor: int, airflow: float):
    pass

hints = get_type_hints(create_equipment)
# Framework data check kar sakta hai
```

## 18. `get_type_hints()` ≠ Validation

```python
hints = get_type_hints(create_equipment)
# Sirf type info
# floor = "34" automatically reject nahi
```

## 19. `get_type_hints()` ≠ Conversion

```python
# value = "2500"
# Annotation = float
# Convert nahi karega
```

## 20. `get_type_hints()` vs `reveal_type()`

```
reveal_type()     → static debugging
get_type_hints()  → runtime annotation inspection
```

## 21. `__annotations__` vs `get_type_hints()`

| Feature | `__annotations__` | `get_type_hints()` |
|---------|-------------------|-------------------|
| Runtime | Yes | Yes |
| Raw | Yes | No |
| Forward refs | Maybe | Yes |
| `Annotated` | Raw | `include_extras=True` |
| Framework use | Possible | Better |

## 22. Inheritance Example

```python
class Equipment:
    equipment_id: str

class AHU(Equipment):
    airflow: float

hints = get_type_hints(AHU)
# equipment_id → str, airflow → float
```

## 23. Practical Architecture

```
@dataclass Equipment
       ↓
get_type_hints()
       ↓
field names + types
       ↓
runtime schema
       ↓
API validation/serialization
```

## 24. `Annotated` + `get_type_hints()`

```python
@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float

Airflow = Annotated[float, "CFM", Range(0, 5000)]

class AHU:
    airflow: Airflow

hints = get_type_hints(AHU, include_extras=True)
```

## 25. Security/Performance

```
get_type_hints() → complex forward refs
                → overhead
                → cache karna better
```

## 26. Complete Example

```python
@dataclass
class AHU:
    equipment_id: str
    floor: int
    airflow: Annotated[float, "CFM", Range(0, 5000)]

hints = get_type_hints(AHU, include_extras=True)

for field_name, field_type in hints.items():
    print(field_name, "=>", field_type)
```

## 27. One-Line

```
get_type_hints(obj)
→ Runtime par annotations resolve karke dictionary form mein do
```

## 28. Golden Rule

```
reveal_type(x)              → type checker ka dimaag dekho
get_type_hints(obj)         → runtime annotations read karo
get_type_hints(obj, include_extras=True)  → Annotated metadata bhi
```

---

# Lesson 72: `get_args()` + `get_origin()` — Generic Introspection

## 1. Basic Idea

```python
list[int]
  ↓
origin = list
args   = int
```

## 2. Import

```python
from typing import get_args, get_origin
```

## 3. `get_origin()`

```python
from typing import get_args, get_origin

T = list[int]
print(get_origin(T))   # <class 'list'>
```

**Explanation:**
- Generic ka base/original type

## 4. `get_args()`

```python
print(get_args(list[int]))         # (int,)
print(get_args(dict[str, float]))  # (str, float)
```

**Explanation:**
- Generic ke andar parameters

## 5. Dono Saath

```
dict[str, int]
      │
      ├── origin → dict
      └── args   → (str, int)
```

## 6. Comparison

| Function | Sawal |
|----------|-------|
| `get_origin()` | Base kya hai? |
| `get_args()` | Parameters kya hain? |

## 7. Simple Types

```python
get_origin(int)   # None
get_args(int)     # ()
```

## 8. `list[int]`

```python
T = list[int]
print(get_origin(T))   # <class 'list'>
print(get_args(T))     # (<class 'int'>,)
```

## 9. `dict[str, int]`

```python
T = dict[str, int]
print(get_origin(T))   # <class 'dict'>
print(get_args(T))     # (<class 'str'>, <class 'int'>)
```

## 10. `tuple`

```python
T = tuple[str, int]
print(get_origin(T))   # tuple
print(get_args(T))     # (str, int)
```

## 11. Variable-Length Tuple

```python
T = tuple[int, ...]
print(get_args(T))   # (int, Ellipsis)
```

## 12. `Union`

```python
T = int | str
print(get_args(T))     # (int, str)
print(get_origin(T))   # types.UnionType
```

## 13. `Optional`

```python
from typing import Optional, get_args

T = Optional[int]
print(get_args(T))   # (int, NoneType)
```

## 14. `Annotated`

```python
from typing import Annotated, get_args, get_origin

T = Annotated[int, "Celsius"]
print(get_origin(T))   # Annotated
print(get_args(T))     # (int, "Celsius")
```

## 15. Multiple Metadata

```python
T = Annotated[float, "CFM", "HVAC", "0-5000"]
print(get_args(T))
# (float, "CFM", "HVAC", "0-5000")
```

## 16. `Literal`

```python
from typing import Literal

T = Literal["ON", "OFF"]
print(get_origin(T))   # Literal
print(get_args(T))     # ("ON", "OFF")
```

## 17. `Callable`

```python
from collections.abc import Callable

T = Callable[[int, str], bool]
print(get_origin(T))   # collections.abc.Callable
```

## 18. Nested Generics

```python
T = list[dict[str, int]]
print(get_origin(T))   # list
print(get_args(T))     # (dict[str, int],)

inner = get_args(T)[0]
print(get_origin(inner))   # dict
print(get_args(inner))     # (str, int)
```

## 19. Recursive Introspection

```
list[dict[str, int]]
       │
       └── dict[str, int]
              │
              ├── str
              └── int
```

## 20. Generic TypeVar

```python
from typing import TypeVar

T = TypeVar("T")
print(get_origin(T))   # None
print(get_args(T))     # ()
```

## 21. Generic Class

```python
class Repository(Generic[T]):
    ...

T = Repository[int]
print(get_origin(T))   # Repository
print(get_args(T))     # (int,)
```

## 22. Practical Faida

```python
Repository[AHU]
# Framework discover kar sakta hai:
# origin → Repository
# args   → (AHU,)
```

## 23. HVAC Example

```python
class EquipmentRepository(Generic[T]):
    pass

class AHU:
    pass

repo_type = EquipmentRepository[AHU]
print(get_origin(repo_type))   # EquipmentRepository
print(get_args(repo_type))     # (AHU,)
```

## 24. `get_type_hints()` + `get_args()`

```python
def process(data: list[dict[str, int]]) -> dict[str, float]:
    ...

hints = get_type_hints(process)
data_type = hints["data"]
# list[dict[str, int]]

print(get_origin(data_type))   # list
print(get_args(data_type))     # (dict[str, int],)
```

## 25. Runtime Schema Generator

```
list[dict[str, int]]
    ↓
List
 └── Dict
      ├── Key: str
      └── Value: int
```

## 26. Simple Function

```python
def inspect_type(tp):
    print("Type:", tp)
    print("Origin:", get_origin(tp))
    print("Args:", get_args(tp))

inspect_type(list[int])
# Type: list[int]
# Origin: <class 'list'>
# Args: (<class 'int'>,)
```

## 27. `__origin__` / `__args__`

```python
# Modern prefer:
get_origin(T)
get_args(T)
```

## 28. `typing.List` vs `list`

```python
from typing import List
T = List[int]   # Old
T = list[int]   # Modern
```

## 29. `Union` vs `Annotated` vs `Literal`

```python
int | str                  # args → (int, str)
Annotated[int, "Celsius"]  # args → (int, "Celsius")
Literal["ON", "OFF"]       # args → ("ON", "OFF")
```

## 30. Combination

```python
origin = get_origin(tp)
args = get_args(tp)
```

## 31. Type Parser

```python
def describe(tp):
    origin = get_origin(tp)
    args = get_args(tp)

    if origin is None:
        return str(tp)

    if origin is list:
        return f"List of {describe(args[0])}"

    if origin is dict:
        return f"Dict with {describe(args[0])} keys and {describe(args[1])} values"

    return str(tp)
```

## 32. `Annotated` Framework Example

```python
Airflow = Annotated[float, "CFM", "0-5000"]
origin = get_origin(Airflow)   # Annotated
args = get_args(Airflow)       # (float, "CFM", "0-5000")

base_type = args[0]            # float
metadata = args[1:]            # ("CFM", "0-5000")
```

## 33. Rule

```
get_args() → always "types" nahi
          → Literal values, Annotated metadata, etc.
```

## 34. `get_origin()` Rule

```
list[int]           → list
dict[str, int]      → dict
int | str           → UnionType
Annotated[int, ...] → Annotated
Literal["ON"]       → Literal
```

## 35. Lessons 70-72 Combined

```
Lesson 70 → reveal_type(x)
Lesson 71 → get_type_hints(func)
Lesson 72 → get_origin(tp) + get_args(tp)
```

## 36. Final Model

```
TYPE SYSTEM
    ↓
get_type_hints()
    ↓
list[dict[str, int]]
    ├── get_origin() → list
    └── get_args()   → dict[str, int]
                            ├── get_origin() → dict
                            └── get_args()   → (str, int)
```

## 37. Golden Rule

```
get_origin(tp) → outer/base construct
get_args(tp)   → andar ke parameters
```

---

# Lesson 73: `typing.NewType` — Distinct Type Aliases

## 1. Basic Idea

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
equipment_id = EquipmentID("AHU-001")
```

**Explanation:**
- `EquipmentID` → distinct static type
- Runtime → `str`

## 2. Purpose

```python
UserID = NewType("UserID", int)
OrderID = NewType("OrderID", int)
```

**Explanation:**
- Dono underlying `int`
- Logically different

## 3. Normal Alias vs NewType

```python
# Type Alias
EquipmentID = str   # Same type

# NewType
EquipmentID = NewType("EquipmentID", str)   # Distinct
```

## 4. Practical Example

```python
def move_equipment(equipment_id: EquipmentID, floor: FloorNumber):
    ...

move_equipment(floor, equipment_id)   # Static checker error
```

## 5. Real-World Problem

```python
def get_equipment(equipment_id: int):
    ...

user_id = 100
get_equipment(user_id)   # Valid without NewType
```

## 6. HVAC Example

```python
EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)
FloorID = NewType("FloorID", int)

def get_equipment(equipment_id: EquipmentID):
    ...

get_equipment(work_order_id)   # Static checker error
```

## 7. Runtime Kya Hota Hai

```python
x = EquipmentID("AHU-001")
print(type(x))   # <class 'str'>
```

**Explanation:**
- NewType → new class nahi
- Static distinction only

## 8. Class Nahi Hai

```python
# NewType
EquipmentID = NewType("EquipmentID", str)

# Actual class
class EquipmentID(str):
    pass
```

## 9. Function ki Tarah

```python
EquipmentID("AHU-001")   # Constructor jaisa
```

**Explanation:**
- Conversion nahi
- Type distinction

## 10. Conversion Nahi

```python
EquipmentID(100)   # "100" nahi banega
```

## 11. `NewType` vs `cast()`

```
NewType → new distinct static type define
cast → existing value ka static type assert
```

## 12. `NewType` vs `TypeAlias`

```
TypeAlias → same type, different name
NewType → different static type identity
```

## 13. Comparison Table

| Feature | Type Alias | NewType | Subclass |
|---------|------------|---------|----------|
| Distinct static | ❌ | ✅ | ✅ |
| New runtime class | ❌ | ❌ | ✅ |
| Runtime behavior | Same | Same underlying | Customizable |
| Methods | ❌ | ❌ | ✅ |

## 14. `isinstance()`

```python
x = EquipmentID("AHU-001")
isinstance(x, str)   # True

isinstance(x, EquipmentID)   # Not possible as class
```

## 15. Function Example

```python
def load_equipment(equipment_id: EquipmentID):
    print(equipment_id)

equipment_id = EquipmentID("AHU-001")
load_equipment(equipment_id)
```

## 16. Wrong Type

```python
WorkOrderID = NewType("WorkOrderID", str)

def get_equipment(equipment_id: EquipmentID):
    ...

work_order_id = WorkOrderID("WO-1001")
get_equipment(work_order_id)   # Error
```

## 17. Generic + NewType

```python
EquipmentID = NewType("EquipmentID", str)

class Repository(Generic[T]):
    def get(self, item_id: T) -> T:
        ...

repo = Repository[EquipmentID]()
```

## 18. Domain-Driven Design

```python
AccountID = NewType("AccountID", int)
UserID = NewType("UserID", int)
InvoiceID = NewType("InvoiceID", int)
```

## 19. Banking Example

```python
def get_account(customer_id: CustomerID, account_id: AccountID):
    ...

customer = CustomerID(10)
account = AccountID(500)

get_account(customer, account)   # OK

get_account(account, customer)   # Error
```

## 20. API Example

```python
EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)

# Boundary: JSON → str → NewType → domain layer
```

## 21. Runtime Validation Nahi

```python
EquipmentID = NewType("EquipmentID", str)
equipment_id = EquipmentID(123)   # Automatically valid
```

## 22. `NewType` vs `Annotated`

```
NewType → distinct static type
Annotated → type + metadata
```

## 23. `NewType` vs `Literal`

```
Literal → specific values
NewType → semantic/domain type
```

## 24. `NewType` vs Dataclass

```python
# NewType — lightweight
EquipmentID = NewType("EquipmentID", str)

# Dataclass — behavior + validation
@dataclass(frozen=True)
class EquipmentID:
    value: str
```

## 25. Kab Use

```
UserID
CustomerID
EquipmentID
WorkOrderID
InvoiceID
```

## 26. Kab Na Use

```
Runtime validation chahiye
Custom methods chahiye
Parsing/formatting chahiye
Complex state chahiye
```

## 27. Deep Mental Model

```python
str → technical type
NewType → domain semantics
```

## 28. Complete Example

```python
EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)
FloorNumber = NewType("FloorNumber", int)

def get_equipment(equipment_id: EquipmentID):
    ...

equipment_id = EquipmentID("MEP-AHU-001")
work_order_id = WorkOrderID("WO-2026-001")

get_equipment(equipment_id)   # OK
get_equipment(work_order_id)  # Error
```

## 29. Lesson 67 Connection

```python
# Type Alias
type EquipmentID = str   # Nickname

# NewType
EquipmentID = NewType("EquipmentID", str)   # Domain identity
```

## 30. Final Comparison

```
str
├── Type Alias → same type
├── NewType → distinct static type
└── Class → actual runtime type
```

## 31. Golden Rule

```
TypeAlias → "Existing type ka doosra naam"
NewType → "Existing type par distinct static domain type"
Class → "Actual runtime object/type"
```

---

# Lesson 74: `NoReturn` vs `Never`

## 1. Core Idea

```
NoReturn → function normally return nahi karta
Never → type-level impossible/empty type
```

## 2. `NoReturn` Basic

```python
from typing import NoReturn

def stop_program() -> NoReturn:
    raise RuntimeError("Program stopped")
```

## 3. `None` vs `NoReturn`

```python
def log_message() -> None:
    print("Done")   # Successfully complete

def fail() -> NoReturn:
    raise RuntimeError()   # No normal return
```

## 4. Static Checker Role

```python
def fail(message: str) -> NoReturn:
    raise RuntimeError(message)

def process(value: int | None) -> int:
    if value is None:
        fail("Value missing")
    return value   # value != None
```

## 5. Control-Flow

```
value
├── None → fail() → X
└── int  → return
```

## 6. Common NoReturn Functions

```python
def panic() -> NoReturn:
    raise RuntimeError()

def fatal(message: str) -> NoReturn:
    raise SystemExit(message)

def run_forever() -> NoReturn:
    while True:
        pass
```

## 7. `NoReturn` with `return`

```python
def fail() -> NoReturn:
    return   # WRONG
```

## 8. `Never`

```python
from typing import Never
```

## 9. Mathematical Model

```python
int → {all integers}
str → {all strings}
Never → {}   # Empty
```

## 10. Top vs Bottom

```
Any → broad
object → all objects
Never → empty
```

## 11. `Never` as Impossible

```python
def impossible(value: Never) -> Never:
    raise AssertionError("Impossible")
```

## 12. Exhaustiveness Checking

```python
Status = Literal["ON", "OFF"]

def assert_never(value: Never) -> Never:
    raise AssertionError(f"Unexpected: {value}")

def handle_status(status: Status):
    if status == "ON":
        print("Running")
    elif status == "OFF":
        print("Stopped")
    else:
        assert_never(status)   # status: Never
```

## 13. Third Status Add

```python
Status = Literal["ON", "OFF", "FAULT"]

# else branch: status = "FAULT" (not Never)
# Type checker complain karega
```

## 14. HVAC Example

```python
HVACState = Literal["RUNNING", "STOPPED", "FAULT"]

def handle_state(state: HVACState):
    if state == "RUNNING":
        ...
    elif state == "STOPPED":
        ...
    elif state == "FAULT":
        ...
    else:
        assert_never(state)
```

## 15. `match` + `Never`

```python
def handle_state(state: HVACState):
    match state:
        case "RUNNING":
            ...
        case "STOPPED":
            ...
        case "FAULT":
            ...
        case _:
            assert_never(state)
```

## 16. `Never` Deeper

```python
x: Never   # Zero possible values (not None)
```

## 17. Historical Relationship

```
NoReturn → function non-return
Never → general bottom type
```

## 18. Same Function

```python
def fatal_old() -> NoReturn:
    raise RuntimeError()

def fatal_modern() -> Never:
    raise RuntimeError()
```

## 19. Key Distinction

```
NoReturn → control flow
Never → type theory
```

## 20. Subtlety

```
NoReturn ≠ old name
Never ≠ new name
```

## 21. `Never` Parameter

```python
def impossible_argument(value: Never):
    ...
```

## 22. `assert_never()` Pattern

```python
def assert_never(value: Never) -> Never:
    raise AssertionError(f"Unhandled: {value!r}")

Mode = Literal["AUTO", "MANUAL"]

def process(mode: Mode):
    if mode == "AUTO":
        ...
    elif mode == "MANUAL":
        ...
    else:
        assert_never(mode)
```

## 23. Flow Diagrams

```
NoReturn:
function → raise/infinite loop → X
normal return → never

Never:
Type space → int, str, None
Never → empty set
```

## 24. `None` vs `NoReturn` vs `Never`

| Type | Meaning |
|------|---------|
| `None` | Function returns no meaningful value |
| `NoReturn` | Function normally return nahi karta |
| `Never` | Koi valid value exist nahi |

## 25. Generic Context

```
int | str
├── int handled
└── str handled
     ↓
Never (remaining)
```

## 26. `Never` = Impossible Branch

```
Never → "ab kuch bhi possible nahi bacha"
```

## 27. `NoReturn` = Impossible Continuation

```
NoReturn → "execution continue nahi hogi"
```

## 28. Exception Handling

```python
def raise_error(message: str) -> NoReturn:
    raise ValueError(message)

def get_temperature(value: float | None) -> float:
    if value is None:
        raise_error("Missing")
    return value
```

## 29. Modern Style

```python
def raise_error(message: str) -> Never:
    raise ValueError(message)
```

## 30. `Never` as NoReturn Replacement

```
Never → broader concept
NoReturn → non-returning function
```

## 31. Real Architecture

```python
EquipmentState = Literal["RUNNING", "STOPPED", "ALARM", "MAINTENANCE"]

def assert_never(value: Never) -> Never:
    raise AssertionError(f"Unknown: {value}")

def handle_equipment_state(state: EquipmentState):
    match state:
        case "RUNNING":
            ...
        case "STOPPED":
            ...
        case "ALARM":
            ...
        case "MAINTENANCE":
            ...
        case _:
            assert_never(state)
```

## 32. Benefit

```
New state added → unhandled branch → type checker warning
```

## 33. `NoReturn` Benefit

```python
def fatal(message: str) -> NoReturn:
    raise RuntimeError(message)
```

## 34. Comparison

```
NoReturn → Function-level concept
Never → Type-level concept
```

## 35. One-Line

```
NoReturn → Function normal return nahi karta
Never → Bottom type with no valid value
```

## 36. Cheat Sheet

```python
from typing import NoReturn, Never

def fatal() -> NoReturn:
    raise RuntimeError()

def assert_never(value: Never) -> Never:
    raise AssertionError(value)
```

## 37. Golden Rule

```
NoReturn → control-flow
Never → type-space
```

---

# Lesson 75: `typing.ParamSpec` Advanced

## 1. Problem

```python
def calculate(a: int, b: int, c: float) -> float:
    return a + b + c
```

**Explanation:**
- Decorator ke andar parameters preserve karne hain

## 2. `ParamSpec`

```python
from typing import ParamSpec

P = ParamSpec("P")
```

**Explanation:**
- `P` → parameters specification

## 3. `TypeVar` vs `ParamSpec`

```
TypeVar → one type
ParamSpec → complete parameter specification
```

## 4. `Callable[P, T]`

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

def wrapper(func: Callable[P, T]) -> Callable[P, T]:
    ...
```

## 5. Basic Decorator

```python
def log_call(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print("Calling...")
        result = func(*args, **kwargs)
        print("Finished")
        return result
    return wrapper
```

## 6. `P.args`

```python
def wrapper(*args: P.args, **kwargs: P.kwargs):
    ...
```

**Explanation:**
- Positional parameters

## 7. `P.kwargs`

**Explanation:**
- Keyword parameters

## 8. Pair

```
P
├── P.args → positional
└── P.kwargs → keyword
```

## 9. Signature Preservation

```python
def get_equipment(equipment_id: str, floor: int, active: bool = True) -> dict:
    ...

get_equipment = logging_decorator(get_equipment)
# Same signature preserved
```

## 10. `...` vs `P`

```python
# Weak
Callable[..., T]

# Precise
Callable[P, T]
```

## 11. Comparison

```
Callable[..., T] → any parameters
Callable[P, T] → exactly P parameters
```

## 12. Logging Decorator

```python
def log_call(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_call
def calculate_airflow(supply: float, return_air: float) -> float:
    return supply - return_air
```

## 13. `*args` Ke Liye Nahi

```
ParamSpec → positional + keyword + structure
```

## 14. Extra Parameter Add

```python
def wrapper(user_id: str, *args: P.args, **kwargs: P.kwargs) -> T:
    ...
```

## 15. `Concatenate`

```python
from typing import Concatenate

def add_user_id(func: Callable[Concatenate[str, P], T]) -> Callable[P, T]:
    ...
```

## 16. `Concatenate` Example

```python
def with_user(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    ...
```

## 17. Injection Direction

```python
def inject_user(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        user = get_current_user()
        return func(user, *args, **kwargs)
    return wrapper
```

## 18. Dependency Injection

```
HTTP → middleware → auth → inject User → business function
```

## 19. Retry Decorator

```python
def retry(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except Exception:
                if attempt == 2:
                    raise
        raise RuntimeError("Unreachable")
    return wrapper

@retry
def read_temperature(equipment_id: str) -> float:
    ...
```

## 20. Caching

```python
def cache(func: Callable[P, T]) -> Callable[P, T]:
    ...
```

## 21. Authorization

```python
def require_admin(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    ...
```

## 22. Async

```python
def async_log(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        result = await func(*args, **kwargs)
        return result
    return wrapper
```

## 23. `ParamSpec` Return Type Nahi

```
P → parameter specification
T → return type
```

## 24. `ParamSpec` + `TypeVar`

```
P → parameters
T → return type
Callable[P, T] → P → T
```

## 25. Deeper

```
TypeVar → values/types relationship
ParamSpec → function signatures relationship
```

## 26. `ParamSpec` vs `Callable[..., T]`

```
Callable[..., T] → "parameters don't care"
Callable[P, T] → "exact relationship preserved"
```

## 27. `ParamSpec` vs TypeVar bound

```
TypeVar → "F = some callable"
ParamSpec → "P = callable's parameters"
```

## 28. Keyword-Only

```python
def configure(equipment_id: str, *, temperature: float, enabled: bool):
    ...

# ParamSpec preserves structure
```

## 29. Positional-Only

```python
def read(equipment_id: str, /, timeout: float):
    ...

# P preserves parameter kinds
```

## 30. Biggest Faida

```python
@log
def f1(...): ...

@log
def f2(...): ...

@log
def f3(...): ...
```

- Har function ki signatures preserved

## 31. `functools.wraps`

```python
from functools import wraps

def log_call(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        ...
    return wrapper
```

## 32. Very Important

```
ParamSpec → static typing
Runtime validation nahi
```

## 33. Runtime Nahi

```
Validation, conversion, logging, DI → ParamSpec khud nahi
```

## 34. Mental Model

```
f
├── P (parameters)
└── T (return type)

Decorator:
Callable[P, T] → Callable[P, T]
```

## 35. Complete Example

```python
P = ParamSpec("P")
T = TypeVar("T")

class User:
    pass

def get_current_user() -> User:
    return User()

def authorized(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        user = get_current_user()
        return func(user, *args, **kwargs)
    return wrapper

@authorized
def update_temperature(user: User, equipment_id: str, temperature: float) -> str:
    return f"{user} updated {equipment_id} to {temperature}"

# Caller:
update_temperature("AHU-01", 22.5)
```

## 36. Ultimate Mental Model

```
TypeVar → values/types relationship
ParamSpec → function signatures preserve
```

## 37. Golden Rule

```
P = parameters
T = return type
Callable[P, T] → P → T
Decorator: Callable[P, T] → Callable[P, T]
```

---

# Lesson 76: `typing.Concatenate` — Partial ParamSpec

## 1. `Concatenate`

```python
from typing import Concatenate
Concatenate[FixedType, P]
```

**Explanation:**
- `FixedType + P`

## 2. `ParamSpec` Connection

```python
P = ParamSpec("P")
T = TypeVar("T")
Callable[P, T]
```

## 3. Simple Example

```python
def process(equipment_id: str, temperature: float) -> None:
    ...

# Conceptually P = (equipment_id: str, temperature: float)
```

## 4. Direction

```
Concatenate[User, P] → User + P
Not: P + User
```

## 5. Actual Use

```python
class User:
    pass

def update_equipment(user: User, equipment_id: str, temperature: float) -> str:
    return "Updated"
```

## 6. Full Decorator

```python
P = ParamSpec("P")
T = TypeVar("T")

def get_current_user() -> User:
    return User()

def inject_user(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        user = get_current_user()
        return func(user, *args, **kwargs)
    return wrapper

@inject_user
def update_equipment(user: User, equipment_id: str, temperature: float) -> str:
    return f"{user} updated {equipment_id} to {temperature}"

# Caller:
update_equipment("AHU-01", 22.5)
```

## 7. Magic

```
Original: User + P → T
Decorator: P → T
```

## 8. `Callable` Reading

```python
Callable[Concatenate[User, P], T]
# = Callable[User + P, T]
```

## 9. Input/Output

```python
def inject_user(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    ...
```

```
Input: User + P → T
Output: P → T
```

## 10. `ParamSpec` Alone Se Nahi

```
Concatenate[User, P] → User + P
```

## 11. "Prefix" Mental Model

```
P = (A, B, C)
Concatenate[X, P] = (X, A, B, C)
```

## 12. Multiple Fixed

```python
Concatenate[User, Request, P] = (User, Request) + P
```

## 13. Real API Example

```python
def api_context(func: Callable[Concatenate[User, Request, P], T]) -> Callable[P, T]:
    ...
```

## 14. Authentication

```python
def authenticated(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    ...
```

## 15. Authorization

```python
def require_admin(func: Callable[Concatenate[User, P], T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        user = get_current_user()
        if not user.is_admin:
            raise PermissionError("Admin required")
        return func(user, *args, **kwargs)
    return wrapper
```

## 16. Dependency Injection

```
Caller → P → Decorator → User + Database + P → Business Function
```

## 17. Logger Injection

```python
def inject_logger(func: Callable[Concatenate[Logger, P], T]) -> Callable[P, T]:
    ...
```

## 18. Database Transaction

```python
def with_database(func: Callable[Concatenate[Database, P], T]) -> Callable[P, T]:
    ...
```

## 19. Signature Transformation

```
ParamSpec → capture
Concatenate → transform
```

## 20. Decorator Transformation

```
(User, P) → T
     ↓
Decorator (remove/inject User)
     ↓
P → T
```

## 21. `Concatenate` Naam

```
Concatenate → join together
User + P
```

## 22. Restriction

```
FIXED PREFIX + P
Not: P[0] + FIXED + P[1:]
```

## 23. `Callable` Context

```python
Callable[Concatenate[User, P], T]
```

## 24. Runtime Behavior

```
Concatenate → runtime DI nahi
Wrapper manually likhna padta hai
```

## 25. Validation Nahi

```
Concatenate → automatically User check nahi karega
```

## 26. `Concatenate` vs `TypeVar`

```
TypeVar → type
ParamSpec → parameters
Concatenate → fixed + parameters
```

## 27. `Concatenate` vs `*args`

```python
# Runtime
def wrapper(*args):
    ...

# Typing
def wrapper(*args: P.args, **kwargs: P.kwargs):
    ...
```

## 28. Context Injection

```python
class BuildingContext:
    def __init__(self, building: str):
        self.building = building

def inject_context(func: Callable[Concatenate[BuildingContext, P], T]) -> Callable[P, T]:
    ...
```

## 29. Middleware

```
Request → auth middleware → User injection → authz middleware
       → Database injection → Business function
```

## 30. Strongest Use Case

```
Decorator required context/dependency provide karta hai
User, Request, Database, Logger, Transaction
```

## 31. Injection vs Removal

```
Original: User + P → T
External: P → T
Internally: User still exists
```

## 32. Full Example

```python
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

def inject_dependencies(func: Callable[Concatenate[User, Database, P], T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        user = get_user()
        db = get_database()
        return func(user, db, *args, **kwargs)
    return wrapper

@inject_dependencies
def update_equipment(user: User, db: Database, equipment_id: str, temperature: float) -> bool:
    return True

# External:
update_equipment("AHU-01", 22.5)
```

## 33. Formula

```
ParamSpec → P = unknown parameter list
Concatenate → A + P
Callable → P → T
Combined → (A + P) → T
Decorator output → P → T
```

## 34. Lesson 75 Connection

```
Callable[P, T] → P → T
Callable[Concatenate[User, P], T] → User + P → T
-> Callable[P, T] → P → T
```

## 35. Faida

```
1. Type-safe DI
2. Typed decorators
3. Middleware
4. Authorization
5. Database/session injection
6. Framework architecture
7. Refactoring safety
```

## 36. Final Comparison

| Construct | Purpose |
|-----------|---------|
| `TypeVar` | Type relationship |
| `ParamSpec` | Function parameter specification |
| `P.args` | Positional args |
| `P.kwargs` | Keyword args |
| `Concatenate` | Fixed + ParamSpec |
| `Callable[P, T]` | P → T |
| `Callable[Concatenate[X, P], T]` | X + P → T |

## 37. Golden Rule

```
TypeVar → "T kya type hai?"
ParamSpec → "P function ke kaun se parameters?"
Concatenate → "P ke aagay kaunsa fixed parameter?"
Callable → "Ye parameters kis return type ko produce karte hain?"
```

---

# Lesson 77: `typing.Unpack` + `TypedDict` Unpacking

## 1. Normal `**dict`

```python
config = {"equipment_id": "AHU-01", "temperature": 22.5}

def update_equipment(equipment_id, temperature):
    ...

update_equipment(**config)
```

## 2. `TypedDict`

```python
from typing import TypedDict

class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float
    enabled: bool
```

## 3. `Unpack`

```python
from typing import Unpack

def update_equipment(**kwargs: Unpack[EquipmentConfig]) -> None:
    ...
```

**Explanation:**
- kwargs mein wohi keys aur types

## 4. Mental Model

```
TypedDict → { a: int, b: str }
Unpack → **kwargs: a: int, b: str
```

## 5. Basic Example

```python
def update_equipment(**kwargs: Unpack[EquipmentConfig]) -> None:
    print(kwargs["equipment_id"])
    print(kwargs["temperature"])

update_equipment(equipment_id="AHU-01", temperature=22.5)
```

## 6. `**kwargs: dict` Se Better

```python
# Vague
def update_equipment(**kwargs: dict):
    ...

# Precise
def update_equipment(**kwargs: Unpack[EquipmentConfig]):
    ...
```

## 7. Keyword Schema

```
TypedDict → keyword arguments ka schema
Unpack → schema ko **kwargs mein expand
```

## 8. Runtime Kya

```
Unpack → runtime unpack nahi
**config → actual unpacking
```

## 9. TypedDict vs Normal Dict

```python
# Generic dict
config = {"equipment_id": "AHU-01", "airflow": 2500.0}

# TypedDict
class AHUConfig(TypedDict):
    equipment_id: str
    airflow: float
```

## 10. Signature Imagine

```python
def configure(**kwargs: Unpack[AHUConfig]):
    ...

# Conceptually:
def configure(*, equipment_id: str, airflow: float):
    ...
```

## 11. `*` Connection

```python
def configure(*, equipment_id: str, airflow: float):
    ...

# Caller:
configure(equipment_id="AHU-01", airflow=2500)
```

## 12. Required Fields

```python
class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float

# Both required
```

## 13. Optional Fields

```python
from typing import NotRequired, TypedDict, Unpack

class EquipmentConfig(TypedDict):
    equipment_id: str
    temperature: float
    enabled: NotRequired[bool]
```

## 14. `NotRequired` vs `Optional`

```
NotRequired → key optional
Optional → key present, value None allowed
```

## 15. Example

```python
class Config(TypedDict):
    name: str
    enabled: NotRequired[bool]

# Valid: {"name": "AHU-01"}
# Valid: {"name": "AHU-01", "enabled": True}
# Invalid: {"name": "AHU-01", "enabled": None}
```

## 16. `Unpack` + `Required`

```python
from typing import Required

class EquipmentConfig(TypedDict, total=False):
    equipment_id: Required[str]
    temperature: float
```

## 17. API Payload

```python
class EquipmentPayload(TypedDict):
    equipment_id: str
    floor: str
    temperature: float
    active: bool

def send_update(**payload: Unpack[EquipmentPayload]):
    ...

send_update(equipment_id="AHU-01", floor="34", temperature=22.5, active=True)
```

## 18. Configuration System

```python
class HVACSettings(TypedDict):
    setpoint: float
    airflow: float
    fan_speed: int

def configure_ahu(**settings: Unpack[HVACSettings]):
    ...

configure_ahu(setpoint=22.0, airflow=2500.0, fan_speed=75)
```

## 19. Wrong Types

```python
configure_ahu(setpoint="22", ...)   # Error
```

## 20. Unknown Keys

```python
configure_ahu(..., color="red")   # Extra key error
```

## 21. `Unpack` Sirf TypedDict Ke Liye Nahi

```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple("Ts")
tuple[Unpack[Ts]]
```

## 22. `TypeVarTuple` + `Unpack`

```python
Ts = TypeVarTuple("Ts")

class Container(Generic[*Ts]):
    ...
```

## 23. `Unpack` vs `*` Runtime

```
Runtime: *values → actual unpack
Type-level: Unpack[Ts] → type info unpack
```

## 24. `Unpack` vs `ParamSpec`

```
ParamSpec → complete function signature
Unpack[TypedDict] → dictionary → keyword params
```

## 25. `ParamSpec` vs `Unpack`

```python
# ParamSpec
P = ParamSpec("P")
def decorator(func: Callable[P, T]) -> Callable[P, T]: ...

# Unpack
class Config(TypedDict):
    host: str
    port: int

def connect(**config: Unpack[Config]):
    ...
```

## 26. `Concatenate` vs `Unpack`

```
Concatenate → parameter specifications combine
Unpack → type-level contents expand
```

## 27. API + Service

```python
class EquipmentPayload(TypedDict):
    equipment_id: str
    temperature: float

def update_equipment(**payload: Unpack[EquipmentPayload]) -> bool:
    equipment_id = payload["equipment_id"]
    temperature = payload["temperature"]
    return True

payload: EquipmentPayload = {"equipment_id": "AHU-01", "temperature": 22.5}
update_equipment(**payload)
```

## 28. Major Faida

```
Before:
def update(**kwargs): ...

After:
def update(**kwargs: Unpack[EquipmentPayload]): ...
```

## 29. Function Call Relationship

```python
class UserOptions(TypedDict):
    name: str
    age: int

def create_user(**options: Unpack[UserOptions]):
    ...

options: UserOptions = {"name": "Nouman", "age": 30}
create_user(**options)
```

## 30. `dict[str, object]` Se Better

```python
# Weak
dict[str, object]

# Strong
class UserOptions(TypedDict):
    name: str
    age: int
```

## 31. Architecture Benefit

```
TypedDict world → Unpack → Function kwargs world
```

## 32. Limitation

```
TypedDict → runtime validation nahi
Unpack → runtime validation nahi
```

## 33. `TypedDict` + `Unpack` vs Dataclass

```
TypedDict + Unpack → JSON, API payload, kwargs
Dataclass → domain object, state, methods
```

## 34. Advanced Optional API

```python
class EquipmentUpdate(TypedDict):
    equipment_id: str
    temperature: float
    enabled: NotRequired[bool]
    comment: NotRequired[str]

def update_equipment(**data: Unpack[EquipmentUpdate]) -> None:
    ...

update_equipment(equipment_id="AHU-01", temperature=22.5)
update_equipment(equipment_id="AHU-01", temperature=22.5, enabled=True, comment="PPM")
```

## 35. Complete Mental Model

```
TypedDict → dictionary shape
Unpack → **kwargs
Function keyword parameters
```

## 36. Three Concepts

```
ParamSpec → function signature
Concatenate → fixed prefix + signature
Unpack → structured type contents expand
```

## 37. Most Important Syntax

```python
class EquipmentConfig(TypedDict):
    equipment_id: str
    airflow: float
    enabled: bool

def configure(**config: Unpack[EquipmentConfig]) -> None:
    ...

configure(equipment_id="AHU-01", airflow=2500.0, enabled=True)
```

## 38. Golden Rule

```
TypedDict → dictionary mein keys + types
Unpack → schema → type-safe keyword parameters
```

---

# Lesson 78: `typing.TypeVarTuple` — Variadic Generics

## 1. Problem

```python
def get_value(value: T) -> T:
    return value
```

**Explanation:**
- Single type

```python
(10, "Ali", 25.5, True)
# Types: int, str, float, bool
```

## 2. `TypeVarTuple`

```python
from typing import TypeVarTuple

Ts = TypeVarTuple("Ts")
```

**Explanation:**
- Multiple types sequence

## 3. Variadic

```
*args → runtime variable quantity
TypeVarTuple → type-level variable quantity
```

## 4. `TypeVar` vs `TypeVarTuple`

```
TypeVar → one type
TypeVarTuple → multiple types
```

## 5. `tuple[Unpack[Ts]]`

```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple("Ts")

def make_tuple(*values: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return values
```

## 6. `Unpack` Role

```
Ts = (int, str, float)
Unpack[Ts] = int, str, float
tuple[Unpack[Ts]] = tuple[int, str, float]
```

## 7. Practical Example

```python
result = make_tuple(10, "Ali", 25.5)
# Ts = (int, str, float)
# result: tuple[int, str, float]
```

## 8. `tuple[T, ...]` vs TypeVarTuple

```
tuple[T, ...] → same type repeated
tuple[Unpack[Ts]] → different types allowed
```

## 9. Real Power

```
Input: tuple[int, str, float]
Output: tuple[float, str, int]
```

## 10. `*Ts` Syntax

```python
def make_tuple(*values: *Ts) -> tuple[*Ts]:
    return values
```

## 11. `TypeVarTuple` + `Unpack`

```
Ts = (int, str, float)
Unpack[Ts] = int, str, float
```

## 12. Sirf Tuple Ke Liye Nahi

```
tuple shapes
array dimensions
matrix dimensions
database query results
```

## 13. Array Shape

```python
Shape = TypeVarTuple("Shape")
Array[float, Unpack[Shape]]
```

## 14. HVAC Example

```python
("AHU-01", 22.5, 1200, True)
# Types: str, float, int, bool
```

## 15. Database Example

```python
row = ("MEP-KHN-REF04", "Refrigerator", 34.5, True)
# Row[str, str, float, bool]
```

## 16. `TypeVarTuple` vs `*args`

```
*args → runtime values
TypeVarTuple → static types
*values: Unpack[Ts] → connects
```

## 17. Table

| Feature | TypeVar | TypeVarTuple |
|---------|---------|--------------|
| Represents | one | multiple |
| Quantity | 1 | variable |
| Heterogeneous | No | Yes |
| Example | `T = int` | `Ts = (int, str)` |

## 18. `tuple[T, ...]` vs TypeVarTuple

```
tuple[T, ...] → same type
tuple[Unpack[Ts]] → different types
```

## 19. `ParamSpec` vs `TypeVarTuple`

```
ParamSpec → function signature
TypeVarTuple → type sequence
```

## 20. `TypeVarTuple` vs `Unpack`

```
TypeVarTuple → container
Unpack → expand
```

## 21. Star Operator

```
Runtime: *values → expand
Typing: Unpack[Ts] → types expand
```

## 22. Runtime Nahi

```
TypeVarTuple → runtime data container nahi
```

## 23. Real-World Faida

```
1. Variable number of type parameters
2. Heterogeneous data preserve
3. Type-safe transformations
4. Shape-aware numerical programming
```

## 24. Mental Model

```
TypeVar → one type
TypeVarTuple → many types
ParamSpec → function params
Unpack → expand
```

## 25. Complete Example

```python
Ts = TypeVarTuple("Ts")

def make_record(*values: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return values

record = make_record("MEP-KHN-REF04", 22.5, 1200, True)
# Ts = (str, float, int, bool)
# record: tuple[str, float, int, bool]
```

## 26. One-Line

```
TypeVarTuple → variadic generic type variable
            → zero ya more types sequence
```

---

# Lesson 79: `typing.dataclass_transform` — Custom Dataclass Decorators

## 1. Problem

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature: float
```

**Explanation:**
- `@dataclass` → `__init__`, `__repr__`, `__eq__`

## 2. Custom Decorator

```python
@model
class Equipment:
    equipment_id: str
    temperature: float
```

**Explanation:**
- Type checker ko pata nahi

## 3. `dataclass_transform`

```python
from typing import dataclass_transform

@dataclass_transform()
def model(cls):
    ...
```

**Explanation:**
- Type checker signal

## 4. Runtime Nahi Banata

```python
@dataclass_transform()
def model(cls):
    return cls   # Sirf typing
```

## 5. Simple Decorator

```python
from dataclasses import dataclass

def model(cls):
    return dataclass(cls)
```

## 6. Practical

```python
from typing import dataclass_transform

@dataclass_transform()
def model(cls):
    return dataclass(cls)

@model
class Equipment:
    equipment_id: str
    temperature: float

equipment = Equipment("AHU-01", 22.5)
```

## 7. Why Needed

```
@model, @Entity, @Table, @schema, @component
```

## 8. Purpose

```
dataclass → actually transform
dataclass_transform → type checker ko batao
```

## 9. Three Forms

```python
# Function decorator
@dataclass_transform()
def model(cls): ...

# Class decorator
@dataclass_transform()
class ModelBase: ...

# Metaclass
@dataclass_transform()
class ModelMeta(type): ...
```

## 10. Field Specifiers

```python
def model_field(...):
    ...

@dataclass_transform(field_specifiers=(model_field,))
def model(cls):
    ...
```

## 11. Field Specifier Kyun

```python
@model
class Equipment:
    equipment_id: str = model_field(...)
    temperature: float = model_field(default=20.0)
```

## 12. `eq_default`

```python
@dataclass_transform(eq_default=True)
def model(cls):
    ...
```

## 13. `order_default`

```python
@dataclass_transform(order_default=True)
```

## 14. `kw_only_default`

```python
@dataclass_transform(kw_only_default=True)
```

## 15. `frozen_default`

```python
@dataclass_transform(frozen_default=True)
```

## 16. Static vs Runtime

```
dataclass_transform → type checker
model() → runtime class unchanged
```

## 17. Complete Architecture

```
@model
├── Runtime: dataclass()
└── Type Checker: dataclass-like semantics
```

## 18. Frameworks

```
Application → Models → Framework → @model
```

## 19. ORM-Style

```
@model
class Equipment:
    equipment_id: str
    name: str

# Framework: fields, DB mapping, constructor
```

## 20. `dataclass_transform` vs `dataclass`

| Feature | `@dataclass` | `@dataclass_transform` |
|---------|--------------|------------------------|
| Runtime | Yes | No |
| `__init__` | Yes | No |
| Type semantics | Yes | Yes |
| Custom | Limited | Excellent |

## 21. `dataclass_transform` vs `Protocol`

```
Protocol → structure/interface
dataclass_transform → class transformation
```

## 22. `dataclass_transform` vs `Generic`

```
Generic → type parameters
dataclass_transform → dataclass-like transformation
```

## 23. Constructor Checking

```python
@model
class Equipment:
    equipment_id: str
    temperature: float

Equipment("AHU-01", 22.5)   # OK
Equipment(123, "hot")       # Error
```

## 24. Field Specifier Example

```python
class Field:
    def __init__(self, default=None):
        self.default = default

def model_field(default=None):
    return Field(default)

@dataclass_transform(field_specifiers=(model_field,))
def model(cls):
    ...

@model
class Equipment:
    equipment_id: str
    temperature: float = model_field(20.0)
```

## 25. Dataclass Kyun Nahi

```
Simple → @dataclass
Framework → dataclass_transform
```

## 26. Real-World Mental Model

```python
@entity
class Equipment:
    id: str
    temperature: float

# @entity: fields, __init__, validation, DB, serialization
```

## 27. Implementation vs Declaration

```
@dataclass_transform → contract
entity() → actual implementation
```

## 28. Mental Model

```
@dataclass → actual transformation
@dataclass_transform → type checker batata hai
field_specifiers → custom field declarations
custom decorator → runtime transformation
```

## 29. Complete Example

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

equipment = Equipment("AHU-01", 22.5)
print(equipment)
```

## 30. Final Summary

```
dataclass → runtime behavior
dataclass_transform → type checker semantics
```

## 31. One-Line

```
dataclass_transform → custom decorator/base/metaclass ko
dataclass-jaisa treat karne ka type checker ko batana
```

---

# Lesson 80: `typing.deprecated` — Marking Deprecated APIs

## 1. Deprecated Meaning

```
Deprecated → available, but future remove/change
Deprecated ≠ removed
```

## 2. Basic Syntax

```python
from typing import deprecated

@deprecated("Use new_function() instead.")
def old_function():
    ...
```

## 3. Important Point

```
typing.deprecated → static/tooling metadata
```

## 4. `typing.deprecated` vs `warnings.warn`

```python
# Static
@deprecated("Use new_function()")
def old_function():
    ...

# Runtime
import warnings

def old_function():
    warnings.warn("Use new_function()", DeprecationWarning, stacklevel=2)
```

## 5. Combine

```python
@deprecated("Use get_temperature_celsius() instead.")
def get_temperature():
    warnings.warn(
        "get_temperature() is deprecated; use get_temperature_celsius()",
        DeprecationWarning,
        stacklevel=2,
    )
    return 22.5
```

## 6. Migration Strategy

```
Version 1: get_temperature()
Version 2: get_temperature() → deprecated
           get_temperature_celsius() → new
Version 3: get_temperature() → removed
```

## 7. Function Deprecated

```python
@deprecated("Use calculate_airflow() instead.")
def airflow():
    return 1200
```

## 8. Class Deprecated

```python
@deprecated("Use ModernEquipment instead.")
class OldEquipment:
    pass
```

## 9. Method Deprecated

```python
class Equipment:
    @deprecated("Use get_temperature_celsius() instead.")
    def get_temperature(self):
        return 22.5

    def get_temperature_celsius(self):
        return 22.5
```

## 10. Property Deprecated

```python
class Equipment:
    @property
    @deprecated("Use temperature_celsius instead.")
    def temperature(self):
        return 22.5
```

**Explanation:**
- Decorator order test karo

## 11. Good Message

```python
@deprecated(
    "Use get_temperature_celsius() instead; "
    "get_temperature() will be removed in v3.0."
)
def get_temperature():
    ...
```

## 12. API Lifecycle

```
NEW → SUPPORTED → DEPRECATED → REMOVED
```

## 13. HVAC Example

```python
@deprecated("Use get_supply_air_temperature() instead.")
def get_supply_air_temp():
    return 18.5
```

## 14. Equipment API

```python
@deprecated("Use get_equipment_by_id() instead.")
def get_equipment():
    ...
```

## 15. Library vs Application

```
Library/framework → deprecated useful
Application → less common
```

## 16. Benefits

```
1. Backward compatibility
2. Migration signal
3. Better API evolution
4. Technical debt control
```

## 17. `deprecated` vs `Final`

```
Final → prevent reassignment
deprecated → discourage API usage
```

## 18. `deprecated` vs `NoReturn`

```
NoReturn → function doesn't return
deprecated → API old, use replacement
```

## 19. `deprecated` vs `Annotated`

```
Annotated → type + metadata
deprecated → API + deprecation metadata
```

## 20. Validation Nahi

```
@deprecated → automatically verify nahi
```

## 21. Type Checker Role

```
source → deprecated symbol → diagnostic
```

## 22. Generic + Deprecated

```python
T = TypeVar("T")

@deprecated("Use process_new() instead.")
def process(value: T) -> T:
    return value
```

## 23. Deeper Architecture

```
old_api → deprecation metadata → type checker → developer info
```

## 24. Deprecation Communication

```
API evolution communication mechanism
```

## 25. Strong Migration

```python
@deprecated(
    "get_airflow() is deprecated; "
    "use get_airflow_cfm() instead. "
    "The old API will be removed in v3.0."
)
def get_airflow():
    return get_airflow_cfm()
```

## 26. Golden Mental Model

```
deprecated → "API exist, but don't use"
           → "replacement available"
```

## 27. Connection

```
TypeVar → generic
TypeVarTuple → variable types
ParamSpec → function params
Unpack → type expansion
dataclass_transform → framework semantics
deprecated → API lifecycle
```

## 28. Final One-Line

```
typing.deprecated → typing-level decorator
                 → static/IDE/tooling signal
```

## 29. Important Distinction

```
@deprecated(...) → static migration guidance
warnings.warn(...) → runtime warning
```

---

**Ab ye guide complete hai (Lessons 71-80).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ Golden rules

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀