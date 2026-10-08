# Python OOP — Lessons 81-90 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 81: `typing.override`

## 1. `override` Kya Hai

```python
from typing import override

class Animal:
    def speak(self) -> str:
        return "Animal sound"

class Dog(Animal):
    @override
    def speak(self) -> str:
        return "Bark"
```

**Explanation:**
- `@override` → child class ka method parent ko override kar raha hai
- Type checker ko batata hai

## 2. `override` Method Change Nahi Karta

```
@override → runtime behavior change nahi
@override → type checker information
```

## 3. `@override` Ke Baghair Problem

```python
class Animal:
    def speak(self) -> str:
        return "Animal"

class Dog(Animal):
    def speek(self) -> str:   # Typo!
        return "Bark"

dog = Dog()
print(dog.speak())   # Animal (parent method)
```

**Explanation:**
- `speek` ≠ `speak`
- Override nahi hua
- Python error nahi dega

## 4. `@override` Yahan Useful

```python
class Dog(Animal):
    @override
    def speek(self) -> str:   # Type checker error
        return "Bark"
```

**Type checker:**
```
Method "speek" is marked as override,
but no base method is overridden
```

## 5. Real Faida

```python
class HVACController:
    def start(self): ...
    def stop(self): ...
    def set_temperature(self, temperature: float): ...

class AHUController(HVACController):
    @override
    def start(self): ...
    @override
    def stop(self): ...
    @override
    def set_temperature(self, temperature: float): ...
```

**Parent API change:**
```python
# set_temperature() rename → set_setpoint()
```

**Type checker:**
```
Ye ab parent method override nahi kar raha
```

## 6. Override + Inheritance

```python
class Parent:
    def show(self):
        print("Parent")

class Child(Parent):
    @override
    def show(self):
        print("Child")

obj = Child()
obj.show()   # Child
```

## 7. Signature Important

```python
class Parent:
    def calculate(self, x: int) -> int:
        return x * 2

class Child(Parent):
    @override
    def calculate(self, x: str) -> str:   # Error
        return x.upper()
```

**Explanation:**
- Parent: `int → int`
- Child: `str → str`
- LSP violation

## 8. LSP Connection

```
Parent contract
      ↓
Child same contract
      ↓
@override verify
```

## 9. `override` vs Normal

```python
# Without
class Child(Parent):
    def run(self): ...

# With
from typing import override

class Child(Parent):
    @override
    def run(self): ...
```

## 10. Documentation

```python
class AHU(AHUBase):
    @override
    def start(self):
        ...
```

**Developer ko clear:**
```
start() → parent se inherited contract
        → child intentionally customize
```

## 11. Old Approaches

```python
from typing_extensions import override   # Older Python
```

## 12. Formula

```
Inheritance → Parent method → Child same method → @override
```

**Key Point:** `@override` Python ko override nahi sikhata. Type checker ko intention batata hai.

## 13. Real Example

```python
class Equipment:
    def start(self) -> str:
        return "Equipment started"

    def stop(self) -> str:
        return "Equipment stopped"

class AHU(Equipment):
    @override
    def start(self) -> str:
        return "AHU fan started"

    @override
    def stop(self) -> str:
        return "AHU fan stopped"

ahu = AHU()
print(ahu.start())   # AHU fan started
```

## 14. Important Distinction

```
@override → runtime validation nahi
@override → static type checking
```

## 15. Core Concept

```
@override = "Child class mein ye method parent ko intentionally override karta hai"
```

---

# Lesson 82: `mypy` Deeply

## 1. Basic Workflow

```
Python source → Type hints → mypy → Static analysis → Errors
```

## 2. Install

```bash
python -m pip install mypy
mypy --version
```

## 3. Simple Example

```python
def multiply(a: int, b: int) -> int:
    return a * b

x = multiply("10", 5)   # Error
```

```bash
mypy app.py
```

**Output:**
```
app.py:9: error: Argument 1 to "multiply" has incompatible type "str"; expected "int"
```

## 4. Static Typing

```python
x: int = 10       # OK
x: int = "hello"  # Error
```

## 5. Return Type Checking

```python
def get_temperature() -> float:
    return "25"   # Error

def get_temperature() -> float:
    return 25.0   # OK
```

## 6. Mypy Kya Check Karta Hai

```
Function arguments
Return values
Attributes
Classes
Inheritance
Generic types
Protocols
Overloads
TypedDict
```

## 7. Configuration Files

```
mypy.ini
pyproject.toml
setup.cfg
```

## 8. `mypy.ini`

```ini
[mypy]
python_version = 3.12
strict = true
```

## 9. `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

## 10. `strict = true`

```
Normal mypy → basic
Strict mypy → basic + missing annotations + implicit Any + override problems
```

## 11. Strict Mode Example

```python
# Normal → potentially OK
def calculate(x):
    return x * 2

# Strict → problem
def calculate(x: int) -> int:
    return x * 2
```

## 12. `Any` Ka Problem

```python
from typing import Any

def process(value: Any):
    ...

x: Any = 10
x = "hello"
x = []
```

**Explanation:**
- `Any` → type checking weaken

## 13. `disallow_untyped_defs`

```ini
[mypy]
disallow_untyped_defs = true
```

```python
def calculate(x):   # Problem
    return x * 2

def calculate(x: int) -> int:   # OK
    return x * 2
```

## 14. `disallow_any_generics`

```python
def process(items: list):        # Problem
    ...

def process(items: list[int]):   # OK
    ...
```

## 15. `no_implicit_optional`

```python
def greet(name: str = None):   # Problem
    ...

def greet(name: str | None = None):   # OK
    ...
```

## 16. `warn_return_any`

```python
def get_value() -> Any:
    return 10

def calculate() -> int:
    return get_value()   # Warning
```

## 17. Error Codes

```bash
mypy --show-error-codes app.py
```

**Output:**
```
error: Argument 1 has incompatible type "str"; expected "int" [arg-type]
```

Codes:
```
[assignment]
[arg-type]
[return-value]
[override]
```

## 18. Specific Error Ignore

```python
value = something()  # type: ignore[arg-type]
```

**Explanation:**
- Specific error only
- Blind `type: ignore` avoid

## 19. `reveal_type()`

```python
x = 100
reveal_type(x)
```

**Mypy output:**
```
Revealed type is "builtins.int"
```

```python
items = [1, 2, 3]
reveal_type(items)
```

**Output:**
```
list[int]
```

## 20. Type Narrowing

```python
def process(value: str | int) -> None:
    if isinstance(value, str):
        reveal_type(value)   # str
    else:
        reveal_type(value)   # int
```

## 21. Mypy + `@override`

```python
class Parent:
    def start(self) -> None:
        ...

class Child(Parent):
    @override
    def start(self) -> None:
        ...
```

**Typo:**
```python
@override
def starts(self):   # Error
    ...
```

## 22. Mypy + Protocol

```python
from typing import Protocol

class Startable(Protocol):
    def start(self) -> None:
        ...

class Motor:
    def start(self) -> None:
        print("Motor started")

def run(device: Startable) -> None:
    device.start()
```

**Mypy:**
```
Motor → has start() → compatible with Startable
```

## 23. Mypy + Generic

```python
T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

x = first([1, 2, 3])       # T = int
name = first(["Ali", "Ahmed"])   # T = str
```

## 24. Mypy Plugins

```ini
[mypy]
plugins = some_plugin
```

## 25. Mypy vs Runtime

```
mypy → static analysis
Python → runtime execution
mypy ≠ runtime validation
```

## 26. Architecture

```
Python Code → Type Hints → mypy → Type Inference → Type Checking → Error/Success
```

## 27. Practical Configuration

```toml
[tool.mypy]
python_version = "3.12"
strict = true
show_error_codes = true
```

```bash
mypy .
mypy app.py
```

## 28. Formula

```
mypy → Static type checker
      → Type inference
      → Type validation
      → Strict mode
      → Error codes
      → Configuration
```

## 29. One-Line

```
mypy → Python code ko execute kiye baghair type system ke against analyze
```

---

# Lesson 83: `pyright` / `basedpyright`

## 1. Pyright Kya Hai

```
Pyright → Python static type checker
```

## 2. Pyright vs Python

```
Python → runtime language
Pyright → static analyzer
```

## 3. Install

```bash
npm install -g pyright
pyright --version
```

## 4. Basic Usage

```python
def multiply(a: int, b: int) -> int:
    return a * b

result = multiply("10", 5)   # Error
```

```bash
pyright app.py
```

**Output:**
```
Argument of type "Literal['10']" cannot be assigned to parameter "a" of type "int"
```

## 5. Strong Inference

```python
numbers = [1, 2, 3]
# numbers → list[int]

first = numbers[0]
# first → int
```

## 6. `pyrightconfig.json`

```json
{
    "include": ["src"],
    "exclude": ["**/__pycache__"],
    "typeCheckingMode": "strict"
}
```

## 7. `typeCheckingMode`

```
off
basic
standard
strict
```

## 8. Basic vs Strict

```python
# Basic → tolerate
def calculate(value):
    return value * 2

# Strict → missing type info problem
def calculate(value: int) -> int:
    return value * 2
```

## 9. VS Code Integration

```python
x: int = "hello"   # Editor highlight
```

## 10. Language Server

```
Pyright-based language intelligence
→ type information
→ autocomplete
→ diagnostics
→ go to definition
```

## 11. `reveal_type`

```python
numbers = [1, 2, 3]
reveal_type(numbers)   # list[int]
```

## 12. Type Narrowing

```python
def process(value: str | int):
    if isinstance(value, str):
        value.upper()   # str
    else:
        value.bit_length()   # int
```

## 13. `Literal`

```python
from typing import Literal

def set_mode(mode: Literal["auto", "manual"]) -> None:
    ...

set_mode("auto")     # OK
set_mode("random")   # Error
```

## 14. `TypedDict`

```python
from typing import TypedDict

class Equipment(TypedDict):
    id: str
    floor: int

equipment: Equipment = {
    "id": "AHU-01",
    "floor": 34
}
```

## 15. Protocol

```python
class Startable(Protocol):
    def start(self) -> None:
        ...

class Motor:
    def start(self) -> None:
        print("Started")

def run(device: Startable):
    device.start()
```

## 16. Generic Inference

```python
def first(items: list[T]) -> T:
    return items[0]

number = first([10, 20, 30])   # T = int
name = first(["Ali", "Ahmed"]) # T = str
```

## 17. Pyright vs Mypy

| Feature | mypy | Pyright |
|---------|------|---------|
| Static checking | ✅ | ✅ |
| Type inference | Strong | Very strong |
| VS Code | Good | Excellent |
| Config | `mypy.ini` | `pyrightconfig.json` |

## 18. Ek Project Mein Dono

```
Project → mypy + pyright
```

**Explanation:**
- Different diagnostics
- Team ko ek primary choose karna

## 19. `basedpyright`

```
Pyright → fork → basedpyright
```

**Explanation:**
- Community-maintained
- Additional strictness

## 20. BasedPyright Config

```json
{
    "include": ["src"],
    "typeCheckingMode": "strict"
}
```

```bash
basedpyright
```

## 21. Pyright vs BasedPyright

```
Pyright → Microsoft-originated
BasedPyright → Pyright-based community fork
```

## 22. HVAC Example

```python
@dataclass
class AHU:
    name: str
    airflow: float
    running: bool

def start_ahu(ahu: AHU) -> None:
    ahu.running = True

ahu = AHU(name="AHU-01", airflow=1200.0, running=False)
start_ahu(ahu)
```

**Error example:**
```python
ahu = AHU(name="AHU-01", airflow="1200", running=False)   # Error
```

## 23. Mypy → Pyright Connection

```
mypy → configuration, strict, error codes, plugins
pyright → configuration, typeCheckingMode, strict, inference, editor
```

## 24. Sabse Important Difference

```
Mypy → traditional static type checker
Pyright → fast, powerful inference + editor integration
BasedPyright → Pyright-based stricter fork
```

## 25. Kab Kaunsa

```
Mypy → existing project, strong typing, mature ecosystem
Pyright → VS Code, inference, interactive development
BasedPyright → very strict typing, additional diagnostics
```

## 26. Core Concept

```
Static Type Checking
├── mypy
├── pyright
└── basedpyright
```

## 27. One-Line

```
Pyright → powerful static type checker
BasedPyright → Pyright-based community fork with additional strictness
```

---

# Lesson 84: `pyre` / `pytype`

## 1. `pyre` Kya Hai

```
Pyre → Meta (Facebook) ka Python static type checker
```

## 2. Basic Example

```python
def add(a: int, b: int) -> int:
    return a + b

result = add("10", 20)   # Error
```

## 3. Pyre Configuration

```
.pyre_configuration
```

```json
{
    "source_directories": ["src"]
}
```

## 4. Pyre Annotations

```python
def calculate(value: int) -> int:
    return value * 2
```

## 5. Incremental Checking

```
Initial check → entire project
Later change → affected code → incremental analysis
```

## 6. Pyre + Strict Typing

```
Untyped Python → Partial annotations → More annotations → Static checking
```

## 7. Pyre `Any` Concept

```python
from typing import Any

value: Any   # Type information weak
```

## 8. Pyre Architecture

```
Python Project → Pyre → Type inference + Type checking → Errors
```

## 9. `pytype`

```
pytype → Google ka Python type checker
pytype → inference-heavy
```

## 10. Pytype Important Difference

```python
def calculate(x):
    return x * 2
```

**Explanation:**
- No annotations
- Pytype infer karne ki koshish karta hai

## 11. Pytype Example

```python
def double(x):
    return x * 2

result = double(10)
# 10 → int → x → int → x * 2 → int
```

## 12. Pytype Special Role

```
Existing untyped Python code → inference-based analysis
```

## 13. Pytype + `.pyi`

```python
# math_utils.pyi
def add(a: int, b: int) -> int: ...
```

## 14. Pyre vs Pytype

| Feature | Pyre | Pytype |
|---------|------|--------|
| Static analysis | ✅ | ✅ |
| Type inference | ✅ | ✅ |
| Large projects | Strong focus | Useful |
| Untyped code | ✅ | Strong focus |
| Origin | Meta | Google |

## 15. Mypy vs Pyright vs Pyre vs Pytype

| Checker | Mental model |
|---------|--------------|
| `mypy` | Traditional, mature |
| `pyright` | Fast + strong inference |
| `basedpyright` | Pyright-based stricter fork |
| `pyre` | Large-codebase/incremental |
| `pytype` | Inference-heavy analysis |

## 16. Same Code, Different Checkers

```
calculate(x)
├── mypy → annotations
├── pyright → inference
└── pytype → inference
```

## 17. Gradual Typing

```
Untyped → Partial → More annotations → Static checking
```

## 18. Static vs Runtime

```
Static → mypy, pyright, basedpyright, pyre, pytype
Runtime → typeguard, beartype, pydantic
```

## 19. External Data Example

```python
data = api.get_equipment()
# External API: {"temperature": "25"}
# Expected: temperature → float
```

**Explanation:**
- Static checker external system control nahi kar sakta
- Runtime validation useful

## 20. Pyre Practical Architecture

```
project/
├── src/
├── tests/
└── .pyre_configuration
```

## 21. Pytype Mental Model

```
Python source → Control/data flow → Type inference → Type information → Error detection
```

## 22. Sab Checkers Seekhne Chahiye?

```
Deep learning → 1 primary checker
Understanding → baqi checkers
```

## 23. Core Map

```
Python Static Type Checking
├── mypy
├── pyright
├── basedpyright
├── pyre
└── pytype
```

## 24. One-Line

```
Pyre → large-scale/incremental analysis
Pytype → inference-heavy analysis
```

---

# Lesson 85: Type Stubs — `.pyi` + `typeshed`

## 1. Type Stub Kya Hai

```
.pyi → implementation nahi, type information
```

## 2. `.py` vs `.pyi`

```python
# calculator.py
def add(a, b):
    return a + b

# calculator.pyi
def add(a: int, b: int) -> int: ...
```

```
.py → implementation
.pyi → type interface
```

## 3. `...` Kyun

```python
def add(a: int, b: int) -> int: ...
```

**Explanation:**
- Implementation nahi
- Function exist karta hai

## 4. Complete Example

```
project/
├── calculator.py
└── calculator.pyi
```

## 5. Wrong Call

```python
result = add("10", 20)   # Type checker error
```

## 6. Stub = Interface

```
Implementation → calculator.py
Public interface → calculator.pyi
```

## 7. Classes `.pyi` Mein

```python
# motor.pyi
class Motor:
    speed: int
    def __init__(self, speed: int) -> None: ...
    def start(self) -> None: ...
```

## 8. Variables

```python
# settings.pyi
MAX_SPEED: int
DEFAULT_NAME: str
```

## 9. Constants

```python
DEBUG: bool
VERSION: str
```

## 10. Overload

```python
from typing import overload

@overload
def get_value(x: int) -> int: ...
@overload
def get_value(x: str) -> str: ...
```

## 11. `.pyi` Implementation Nahi

```
.pyi = WHAT
.py = HOW
```

## 12. `typeshed`

```
typeshed → standard library + third-party stubs
```

## 13. Standard Library

```python
import os
path = os.path.join("D:", "test")
# Type checker ko os.path.join signature pata
```

## 14. `typeshed` Structure

```
typeshed
├── Standard library
└── Third-party
```

## 15. Third-Party Stubs

```
pip install types-somepackage
```

```
actual package + separate typing information
```

## 16. Stub-Only Package

```
some_library → runtime
types-some-library → .pyi
```

## 17. `py.typed`

```
my_library/
├── __init__.py
├── motor.py
└── py.typed
```

**Explanation:**
- Marker file
- Type information provide karta hai

## 18. `py.typed` Content

```
Empty marker file
```

## 19. Library Example

```
hvac_lib/
├── __init__.py
├── ahu.py
├── vav.py
└── py.typed
```

## 20. Inline vs Stub

```python
# Inline
def start(speed: int) -> None:
    ...

# Stub
# motor.pyi
def start(speed: int) -> None: ...
```

## 21. Stub Kab Useful

```
Existing untyped library
C extension
Generated code
Public API hide
```

## 22. C Extension Example

```python
# fastmath.pyi
def add(a: int, b: int) -> int: ...
```

```
C implementation → runtime
.pyi → static type information
```

## 23. Stub + Runtime

```
Runtime → .py / C → executes → actual value
Static → .pyi → describes → expected types
```

## 24. Stub Priority

```
module.py + module.pyi → .pyi used for type info
```

## 25. Private Details

```python
def calculate(x: float) -> float: ...
```

**Explanation:**
- Internal variables nahi
- Public API only

## 26. Stub = Contract

```
Protocol → expected behavior
.pyi → expected API/types
```

## 27. `typeshed` Architecture

```
typeshed
├── Standard library typing
└── Stubs for ecosystem
     ↓
Type Checkers
├── mypy
├── pyright
└── others
```

## 28. `typeshed` + Mypy

```
typeshed → type information
mypy → type checker
```

## 29. `typeshed` + Pyright

```
typeshed → standard library type info
pyright → consumes
```

## 30. Stub Package Example

```python
# types-somepackage/api.pyi
def get_equipment(id: str) -> Equipment: ...
```

## 31. Stub vs Protocol

```
Protocol → structural interface
.pyi → module/package type interface
```

## 32. Stub vs ABC

```
ABC → runtime inheritance
Protocol → static structural
.pyi → external/static API description
```

## 33. Professional Project

```
MyProject/
├── src/
│   └── hvac/
│       ├── ahu.py
│       ├── vav.py
│       └── py.typed
└── pyproject.toml
```

## 34. 7 Terms

| Term | Meaning |
|------|---------|
| `.py` | Runtime implementation |
| `.pyi` | Type stub |
| `typeshed` | Type info collection |
| `py.typed` | Package typing marker |
| Stub package | Separate type info |
| Inline typing | Types in `.py` |
| External stubs | Types in `.pyi` |

## 35. One-Line Formulas

```
.py → How the program works
.pyi → What API/type contract exists
typeshed → Common Python APIs' type definitions
py.typed → Package declares inline typing
```

## 36. Final Mental Model

```
Python Library
├── implementation → .py
└── type info → .pyi
     ↓
Static Type Checker
├── mypy
├── pyright
└── pyre
```

## 37. Core Concept

```
.pyi → static type checker ko library ka contract
typeshed → standard library type info organize
```

---

# Lesson 86: Runtime Type Checking

## 1. Static vs Runtime

```
STATIC: mypy, pyright, basedpyright, pyre, pytype
RUNTIME: typeguard, beartype, pydantic
```

## 2. Type Hints Runtime Validation Nahi

```python
def set_temperature(value: float) -> None:
    print(value)

set_temperature("25")   # Python automatically error nahi dega
```

## 3. `typeguard`

```python
from typeguard import typechecked

@typechecked
def add(a: int, b: int) -> int:
    return a + b

add(10, 20)     # OK
add("10", 20)   # Runtime error
```

## 4. `@typechecked`

```python
@typechecked
def calculate(value: int) -> int:
    return value * 2

calculate(10)     # OK
calculate("10")   # Error
```

## 5. Static + Runtime

```
Python Code
├── mypy → static checking
└── typeguard → runtime checking
```

## 6. Return Values

```python
@typechecked
def get_temperature() -> float:
    return "25"   # Runtime error
```

## 7. Nested Types

```python
def process(values: list[int]) -> None:
    ...

process([1, 2, 3])        # OK
process([1, "2", 3])      # Type contract violation
```

## 8. Typeguard Use

```
APIs
Plugin systems
Dynamic applications
Development/testing
```

## 9. `beartype`

```python
from beartype import beartype

@beartype
def add(a: int, b: int) -> int:
    return a + b

add(10, 20)     # OK
add("10", 20)   # Runtime error
```

## 10. `@beartype`

```
@beartype → runtime type checking
```

## 11. Typeguard vs Beartype

| Feature | `typeguard` | `beartype` |
|---------|-------------|------------|
| Runtime checking | ✅ | ✅ |
| Type annotations | ✅ | ✅ |
| Decorator | `@typechecked` | `@beartype` |
| Nested types | ✅ | ✅ |
| Static replacement | ❌ | ❌ |

## 12. Runtime Cost

```
Static → development/CI, runtime impact ≈ none
Runtime → actual execution, type checks, overhead
```

## 13. Pydantic

```python
from pydantic import BaseModel

class Equipment(BaseModel):
    equipment_id: str
    temperature: float
    running: bool

equipment = Equipment(
    equipment_id="AHU-01",
    temperature=24.5,
    running=True
)
```

## 14. Pydantic Real Power

```python
data = {
    "equipment_id": "AHU-01",
    "temperature": "24.5",   # String
    "running": True
}

equipment = Equipment(**data)
# temperature → parsed
```

## 15. Pydantic = Model

```
Raw data → Pydantic Model → Validation/parsing → Structured object
```

## 16. Invalid Data

```python
data = {
    "equipment_id": "AHU-01",
    "temperature": "abc",
    "running": True
}

Equipment(**data)   # Validation error
```

## 17. Missing Fields

```python
data = {"equipment_id": "AHU-01"}
Equipment(**data)   # Required fields missing error
```

## 18. Pydantic vs Dataclass

```
Dataclass → data container
Pydantic → data model + validation + parsing + serialization
```

## 19. Comparison

| Feature | `dataclass` | Pydantic |
|---------|-------------|----------|
| Data container | ✅ | ✅ |
| Type annotations | ✅ | ✅ |
| Runtime validation | Limited | ✅ |
| Parsing | Manual | ✅ |
| JSON workflows | Manual | Strong |

## 20. Pydantic + API

```python
class AHUData(BaseModel):
    equipment_id: str
    floor: int
    temperature: float
    airflow: float
    running: bool

ahu = AHUData(**api_data)
```

## 21. Static + Pydantic

```
External API → JSON/dict → Pydantic → Typed object
                                ↓
                         mypy/pyright
```

## 22. TypeGuard vs Pydantic

```
TypeGuard → static narrowing
Pydantic → actual data validation/modeling
```

## 23. Comparison

| Tool | Purpose |
|------|---------|
| `typeguard` | Runtime type checking |
| `beartype` | Runtime type checking |
| `pydantic` | Validation + parsing + models |

## 24. Same Problem

```python
data = {"temperature": "24.5"}

# Typeguard
@typechecked
def process(temperature: float): ...

# Pydantic
class Sensor(BaseModel):
    temperature: float

sensor = Sensor(**data)
```

## 25. External Boundary

```
TRUST BOUNDARY
External data → Validation → Internal Python
```

## 26. Static vs Runtime Reality

```python
temperature: float
# Not automatically enforced at runtime
```

## 27. Complete Architecture

```
External API → Raw data → Pydantic → Validated models → Business logic
                                                       ↓
                                          mypy / pyright
```

## 28. Warning

```
Har internal function par runtime check → overhead
External boundary → strong validation
Internal → static typing
```

## 29. Typeguard vs Beartype

```
Selection → performance, features, ecosystem
```

## 30. Pydantic Kab

```
API, JSON, validation, models
FastAPI, configuration, schemas
```

## 31. Complete Map

```
Runtime Type/Data Validation
├── typeguard → type checking
├── beartype → type checking
└── pydantic → data modeling
```

## 32. Formula

```
Static → "What should the type be?"
Runtime → "What is the actual type right now?"
Validation → "Is this external data valid?"
```

## 33. Key Point

```
typeguard/beartype → runtime type checking
pydantic → runtime data validation + parsing + models
```

---

# Lesson 87: `threading` — Thread, Lock, RLock, Semaphore, Event

## 1. Concurrency vs Parallelism

```
Concurrency → Multiple tasks progress overlap
Parallelism → Multiple tasks literally same time
```

## 2. Thread

```
Process → Thread 1, Thread 2, Thread 3
```

## 3. Process vs Thread

```
Process → Memory, Resources, Thread(s)
Thread → Same process ke resources share
```

## 4. Real-World Example

```
AHU data read → VAV data read → Temperature API → Database write
```

Threads:
```
AHU → VAV → API
```

## 5. Basic `threading.Thread`

```python
import threading

def worker():
    print("Worker running")

thread = threading.Thread(target=worker)
thread.start()
```

## 6. `start()` vs Direct Call

```python
worker()            # Current thread
thread.start()      # New thread
```

## 7. `run()` Confuse Nahi

```python
thread.start()   # New thread
thread.run()     # Current flow
```

## 8. `join()`

```python
thread.start()
thread.join()
print("Finished")
```

**Explanation:**
- Current thread wait kare

## 9. Multiple Threads

```python
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"Thread-{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

## 10. Thread `args`

```python
threading.Thread(target=worker, args=("AHU-01",))
```

## 11. Threading I/O-Bound

```
API request → waiting → Thread doosra task
```

## 12. CPU-Bound aur GIL

```
GIL → Global Interpreter Lock
CPU-heavy → 10 threads ≠ 10 CPU cores
CPU-bound → multiprocessing better
```

## 13. I/O vs CPU

```
I/O-bound → HTTP, Database, File, Socket → threading
CPU-bound → Calculation → multiprocessing
```

## 14. Shared Data

```python
counter = 0

# Thread 1 → counter += 1
# Thread 2 → counter += 1
```

## 15. Race Condition

```
Thread A → read 0
Thread B → read 0
Thread A → write 1
Thread B → write 1
```

Expected: 2, Got: 1

## 16. `Lock`

```python
import threading
lock = threading.Lock()

with lock:
    counter += 1
```

## 17. Critical Section

```python
with lock:
    counter += 1
```

## 18. Complete Lock Example

```python
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start()
t2.start()
t1.join()
t2.join()
print(counter)   # 200000
```

## 19. `with lock` Kyun

```python
with lock:
    counter += 1
```

Clean form of acquire/release.

## 20. Lock Mental Model

```
Shared Resource
├── Thread A
└── Thread B
     ↓
Lock → only one enters → Critical section
```

## 21. `RLock`

```python
lock = threading.RLock()
```

**Explanation:**
- Reentrant Lock
- Same thread multiple times acquire

## 22. RLock Example

```python
lock = threading.RLock()

def outer():
    with lock:
        inner()

def inner():
    with lock:
        print("Inside inner")

outer()
```

## 23. RLock Mental Model

```
Thread A → acquire RLock → outer() → inner() → acquire RLock again → allowed
```

## 24. Lock vs RLock

| Feature | Lock | RLock |
|---------|------|-------|
| Mutual exclusion | ✅ | ✅ |
| Same thread re-acquire | ❌ | ✅ |
| Nested locking | Risky | Supported |
| Simpler | ✅ | More complex |

## 25. `Semaphore`

```python
semaphore = threading.Semaphore(3)
```

**Explanation:**
- N threads resource access

## 26. Semaphore HVAC Example

```python
semaphore = threading.Semaphore(3)

def fetch_data():
    with semaphore:
        # API call
        ...
```

```
10 threads → Semaphore(3) → 3 concurrent, 7 wait
```

## 27. Lock vs Semaphore

```
Lock → capacity = 1
Semaphore(3) → capacity = 3
```

## 28. `Event`

```python
event = threading.Event()
```

**Explanation:**
- Signal mechanism

## 29. Event Example

```python
import threading
import time

event = threading.Event()

def worker():
    print("Waiting...")
    event.wait()
    print("Signal received!")

t = threading.Thread(target=worker)
t.start()
time.sleep(2)
event.set()
t.join()
```

## 30. Event Boolean

```python
event.set()     # True
event.clear()   # False
event.wait()    # Wait until set
```

## 31. Event HVAC Use

```python
ready = threading.Event()

# Initialization complete:
ready.set()

# Workers:
ready.wait()
```

## 32. Lock vs Event

```
Lock → "Kaun resource use karega?"
Event → "Condition/signal kab complete hua?"
```

## 33. Master Table

| Tool | Purpose |
|------|---------|
| `Lock` | Mutual exclusion |
| `RLock` | Reentrant locking |
| `Semaphore` | Limited concurrency |
| `Event` | Signal/notification |

## 34. Combined Example

```python
api_limit = threading.Semaphore(3)
data_lock = threading.Lock()
ready = threading.Event()

def worker():
    ready.wait()
    with api_limit:
        result = "AHU data"
    with data_lock:
        data.append(result)

ready.set()
```

## 35. Thread Lifecycle

```
Created → start() → Running → Finished → join()
```

## 36. Daemon Thread

```python
thread = threading.Thread(target=worker, daemon=True)
```

## 37. `ThreadPoolExecutor`

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(worker, [1, 2, 3, 4]))
```

## 38. OOP Connection

```
Thread → object
lock = threading.Lock() → object
with lock: → context manager
```

## 39. Warning

```
Multiple threads → same mutable object → race condition
```

## 40. Complete Mental Map

```
threading
├── Thread
└── Synchronization
    ├── Lock
    ├── RLock
    ├── Semaphore
    └── Event
```

## 41. One-Line Each

```
Thread → Independent execution path
Lock → One thread at a time
RLock → Same thread recursive acquire
Semaphore → Limited concurrent access
Event → Signal mechanism
```

---

# Lesson 88: `threading.Condition`, `Barrier`, `Timer`

## 1. `Condition`

```
Thread → Condition check → False → wait()
                       → True → continue
```

## 2. HVAC Example

```
Sensor Thread → Shared buffer
Processor Thread → "Data available?"
```

## 3. Basic Condition

```python
import threading

condition = threading.Condition()
data = []

def consumer():
    with condition:
        while not data:
            condition.wait()
        value = data.pop(0)
    print("Received:", value)

def producer():
    with condition:
        data.append("AHU-01")
        condition.notify()
```

## 4. `wait()`

```
Consumer → lock acquire → condition false → wait() → lock release
```

## 5. `notify()`

```python
condition.notify()   # One thread wake
condition.notify_all()   # All threads wake
```

## 6. `while` Kyun

```python
with condition:
    while not data:
        condition.wait()
    value = data.pop(0)
```

**Explanation:**
- Wake hone par condition verify

## 7. Condition vs Event

```
Event → "Signal aa gaya?"
Condition → "Shared state condition mein hai?"
```

## 8. Producer-Consumer

```
Producer → data produce → notify
Consumer → data consume → wait if empty
```

## 9. Condition + Lock

```python
condition = threading.Condition()   # Auto lock
condition = threading.Condition(lock)   # Explicit
```

## 10. `Barrier`

```python
barrier = threading.Barrier(3)
```

**Explanation:**
- 3 participants wait
- Sab arrive hone par continue

## 11. Barrier HVAC Example

```
AHU config ───────┐
VAV config ───────┼──► Barrier ───► Continue
Alarm config ─────┘
```

## 12. Basic Barrier

```python
barrier = threading.Barrier(3)

def worker(name):
    print(name, "started")
    time.sleep(1)
    print(name, "reached barrier")
    barrier.wait()
    print(name, "passed barrier")

threads = [
    threading.Thread(target=worker, args=("AHU",)),
    threading.Thread(target=worker, args=("VAV",)),
    threading.Thread(target=worker, args=("Alarm",)),
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

## 13. Barrier = Gate

```
GATE
├── AHU
├── VAV
└── Alarm
     ↓
All arrived → gate opens
```

## 14. Barrier vs Event

```
Event → 1 → many
Barrier → many → all
```

## 15. Barrier vs Condition

```
Condition → Dynamic condition
Barrier → Fixed participants
```

## 16. Barrier Timeout

```python
barrier = threading.Barrier(3, timeout=10)
```

## 17. `Timer`

```python
timer = threading.Timer(5, hello)
timer.start()
```

**Explanation:**
- 5 seconds baad hello()

## 18. Timer Delayed Thread

```
Timer → wait 5 seconds → execute function
```

## 19. `sleep()` vs `Timer`

```python
# sleep()
time.sleep(5)
hello()

# Timer
timer = threading.Timer(5, hello)
timer.start()
```

## 20. Timer Cancel

```python
timer = threading.Timer(10, hello)
timer.start()
timer.cancel()
```

## 21. HVAC Timer

```python
def delayed_action():
    print("Checking AHU again")

timer = threading.Timer(10, delayed_action)
timer.start()
```

## 22. Timer Periodic Nahi

```
Timer(10, function) → 10 sec baad one execution
Periodic → different design
```

## 23. Comparison

| Tool | Purpose |
|------|---------|
| `Condition` | Shared state condition wait |
| `Barrier` | All participants synchronize |
| `Timer` | Delayed execution |

## 24. Complete Map

```
threading
├── Thread
├── Lock
├── RLock
├── Semaphore
├── Event
├── Condition
├── Barrier
└── Timer
```

## 25. Real Architecture

```
Main Program
├── AHU Thread
├── VAV Thread
└── Alarm Thread
     ↓
Shared Data + Lock
```

```
API limit → Semaphore(3)
System ready → Event
Data available → Condition
All initialization → Barrier
Delayed check → Timer
```

## 26. Key Difference

```
Lock → "Kaun andar ja sakta hai?"
Semaphore → "Kitne andar ja sakte hain?"
Event → "Signal aa gaya?"
Condition → "Required state true hai?"
Barrier → "Sab participants ready?"
Timer → "Kitni der baad function?"
```

## 27. Final Model

```
THREADING
├── Protect → Lock, RLock, Semaphore
├── Wait → Condition, Event
├── Coordinate → Barrier
└── Delayed → Timer
```

---

# Lesson 89: `queue` — Queue, LifoQueue, PriorityQueue

## 1. Queue Kya Hai

```
Producer → Queue → Consumer
```

## 2. Thread-Safe

```python
q.put(...)   # Thread-safe
q.get()      # Thread-safe
```

## 3. Import

```python
import queue
q = queue.Queue()
```

## 4. `put()`

```python
q.put("AHU-01")
q.put("AHU-02")
```

## 5. `get()`

```python
item = q.get()   # AHU-01
```

## 6. FIFO

```
put("A") → put("B") → put("C")
get() → A → B → C
```

## 7. Simple Example

```python
q = queue.Queue()
q.put("AHU-01")
q.put("AHU-02")
q.put("AHU-03")

print(q.get())   # AHU-01
print(q.get())   # AHU-02
print(q.get())   # AHU-03
```

## 8. Queue vs List

```
list → general-purpose container
Queue → thread communication / producer-consumer
```

## 9. Producer-Consumer Pattern

```
Producer → put() → Queue → get() → Consumer
```

## 10. Producer

```python
def producer(q):
    for i in range(5):
        q.put(f"Sensor-{i}")
```

## 11. Consumer

```python
def consumer(q):
    for _ in range(5):
        item = q.get()
        print("Processing:", item)
```

## 12. Complete Threading Example

```python
q = queue.Queue()

def producer():
    for i in range(5):
        item = f"Temperature-{i}"
        q.put(item)
        print("Produced:", item)

def consumer():
    for _ in range(5):
        item = q.get()
        print("Consumed:", item)
        q.task_done()

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()
t2.join()
```

## 13. `task_done()`

```python
item = q.get()
try:
    process(item)
finally:
    q.task_done()
```

## 14. `queue.join()`

```python
q.put("A")
q.put("B")
q.put("C")

q.join()   # All tasks complete
```

## 15. `join()` vs `task_done()`

```
get() → item mila
task_done() → processing complete
join() → sab queued tasks complete
```

## 16. Empty Queue

```python
q.get()   # Wait if empty
```

## 17. `get_nowait()`

```python
try:
    item = q.get_nowait()
except queue.Empty:
    print("Queue empty")
```

## 18. `put_nowait()`

```python
try:
    q.put_nowait(item)
except queue.Full:
    print("Queue full")
```

## 19. Maximum Size

```python
q = queue.Queue(maxsize=3)
```

## 20. Bounded Queue

```
Fast Producer → Queue(maxsize=100) → Slow Consumer
```

## 21. Backpressure

```
Queue full → Producer WAIT → Consumer remove → Producer continue
```

## 22. `LifoQueue`

```python
q = queue.LifoQueue()
q.put("A")
q.put("B")
q.put("C")

# C → B → A
```

## 23. LifoQueue Mental Model

```
Stack
C ← top
B
A
```

## 24. Queue vs LifoQueue

```
Queue → FIFO → A → B → C
LifoQueue → LIFO → C → B → A
```

## 25. `PriorityQueue`

```python
q = queue.PriorityQueue()
q.put((3, "Normal"))
q.put((1, "Critical"))
q.put((2, "Warning"))

# (1, "Critical")
# (2, "Warning")
# (3, "Normal")
```

## 26. HVAC Alarm Example

```python
q = queue.PriorityQueue()
q.put((3, "Filter reminder"))
q.put((1, "AHU fault"))
q.put((2, "High temperature"))

# AHU fault pehle
```

## 27. PriorityQueue Rule

```python
(1, object_a)
(1, object_b)   # Comparison issue
```

**Solution:**
```python
import itertools
counter = itertools.count()

q.put((1, next(counter), "Critical A"))
q.put((1, next(counter), "Critical B"))
```

## 28. Comparison

| Queue | Order | Use |
|-------|-------|-----|
| `Queue` | FIFO | Normal tasks |
| `LifoQueue` | LIFO | Latest task first |
| `PriorityQueue` | Priority | Important task first |

## 29. Queue vs Condition

```
Manual → Lock + Condition + list
Higher-level → queue.Queue
```

## 30. OOP Connection

```python
q = queue.Queue()   # Object
q.put()             # Method
q.get()             # Method
```

## 31. Multiple Producers/Consumers

```
Producer 1 ──┐
Producer 2 ──┼──► Queue ──┬──► Consumer 1
Producer 3 ──┘            ├──► Consumer 2
                           └──► Consumer 3
```

## 32. Complete Architecture

```
AHU Thread ──────┐
VAV Thread ──────┼──► Queue
Chiller Thread ──┘       │
                         ▼
                  Processing Thread
                         │
                         ▼
                     Database
```

## 33. Golden Pattern

```python
# Producer
q.put(data)

# Consumer
data = q.get()
try:
    process(data)
finally:
    q.task_done()

# Main
q.join()
```

## 34. Message Passing

```
Thread A → message → Queue → Thread B
```

## 35. Complete Mental Map

```
queue
├── Queue → FIFO
├── LifoQueue → LIFO
└── PriorityQueue → Priority
```

## 36. Important Distinction

```
Lock → shared resource protect
Condition → condition wait
Event → signal
Barrier → all threads sync
Semaphore → limited access
Timer → delayed execution
Queue → thread-safe data passing
```

## 37. Queue Internal Order

```
Queue → FIFO
LifoQueue → LIFO
PriorityQueue → priority order
```

---

# Lesson 90: `multiprocessing` — Process, Pool, Queue, Pipe

## 1. Process Kya Hai

```
Process → independent running program instance
Har process → apna memory space
```

## 2. Thread vs Process

```
Thread → shared memory
Process → separate memory
```

## 3. CPU-Bound Problem

```python
def calculate():
    for i in range(10_000_000):
        ...
```

```
Thread 1 ─┐
Thread 2 ─┼── GIL constraint
Thread 3 ─┘

Process 1 → CPU Core 1
Process 2 → CPU Core 2
```

## 4. Import

```python
import multiprocessing
```

## 5. Basic Process

```python
process = multiprocessing.Process(target=worker)
process.start()
process.join()
```

## 6. Basic Example

```python
import multiprocessing

def worker():
    print("Worker process running")

if __name__ == "__main__":
    process = multiprocessing.Process(target=worker)
    process.start()
    process.join()
    print("Finished")
```

## 7. `if __name__ == "__main__"`

**Explanation:**
- Windows par especially important
- Main code guard

## 8. Process Arguments

```python
def worker(name):
    print(f"Processing {name}")

p = multiprocessing.Process(target=worker, args=("AHU-01",))
p.start()
p.join()
```

## 9. Multiple Processes

```python
processes = []

for i in range(4):
    p = multiprocessing.Process(target=worker, args=(i,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
```

## 10. Process Memory Separate

```python
counter = 0

def worker():
    global counter
    counter += 1
    print(counter)

# Main process: counter = 0
# Child process: counter = 1 (separate)
```

## 11. Threading Difference

```
Threading → same process → shared counter
Processes → separate memory → separate counter
```

## 12. Isolated Memory Faida

```
Process crash → doosre process ki memory safe
```

## 13. `multiprocessing.Pool`

```
Main Process → Process Pool
              ├── P1
              ├── P2
              ├── P3
              └── P4
```

## 14. Basic Pool

```python
def square(x):
    return x * x

with multiprocessing.Pool(4) as pool:
    results = pool.map(square, [1, 2, 3, 4, 5])

print(results)   # [1, 4, 9, 16, 25]
```

## 15. `Pool.map()`

```python
pool.map(function, iterable)
```

## 16. Pool Real-World

```
1000 tasks → Process Pool → P1, P2, P3, P4
```

## 17. Thread Pool vs Process Pool

```
ThreadPool → I/O-bound
ProcessPool → CPU-bound
```

## 18. Multiprocessing Queue

```python
import multiprocessing

def worker(q):
    q.put("AHU-01")

if __name__ == "__main__":
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    print(q.get())   # AHU-01
    p.join()
```

## 19. Multiprocessing Queue vs Threading Queue

```
queue.Queue → threads
multiprocessing.Queue → processes
```

## 20. Process Communication

```
Process A → Memory A
Process B → Memory B
       ↓
Communication: Queue, Pipe, Manager, shared memory
```

## 21. `Pipe`

```python
parent_conn, child_conn = multiprocessing.Pipe()
```

```
Process A → parent_conn ║ Pipe ║ child_conn → Process B
```

## 22. Basic Pipe

```python
def worker(conn):
    conn.send("Hello from child")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()
    message = parent_conn.recv()
    print(message)   # Hello from child
    p.join()
```

## 23. `send()` and `recv()`

```python
conn.send(data)   # Data bhejo
conn.recv()       # Data receive
```

## 24. Pipe Bidirectional

```python
multiprocessing.Pipe()              # Duplex
multiprocessing.Pipe(duplex=False)  # One-way
```

## 25. Queue vs Pipe

```
Queue → multiple producers/consumers
Pipe → direct process-to-process
```

## 26. Comparison

| Feature | Queue | Pipe |
|---------|-------|------|
| Multiple producers | Good | Not primary |
| Multiple consumers | Good | Not primary |
| Direct process-to-process | Less direct | Excellent |
| Producer-consumer | Excellent | Possible |

## 27. Multiprocessing Architecture

```
Main Process → Task Queue
              ├── P1
              ├── P2
              └── P3
                   ↓
                Results
```

## 28. Pool + CPU-Bound

```python
def calculate(x):
    return x ** 2

with multiprocessing.Pool() as pool:
    results = pool.map(calculate, range(10))
```

## 29. Threading vs Multiprocessing

| | Threading | Multiprocessing |
|--|-----------|-----------------|
| Unit | Thread | Process |
| Memory | Shared | Separate |
| Communication | Easy | IPC |
| CPU-bound | Not ideal | Good |
| I/O-bound | Excellent | Possible |
| Startup | Lower | Higher |

## 30. GIL Final Mental Model

```
CPython → GIL → Python bytecode within one process

CPU-bound pure Python → multiple processes → CPU cores
I/O-bound → threads often efficient
```

## 31. Process vs Pool

```
Process → specific worker control
Pool → batch of tasks, workers managed
```

## 32. Queue vs Pipe

```
Queue → task/message distribution
Pipe → direct communication channel
```

## 33. Process Lifecycle

```
Created → start() → Running → Finished → join()
```

## 34. `is_alive()`

```python
if p.is_alive():
    print("Process still running")
```

## 35. `terminate()`

```python
p.terminate()
```

**Explanation:**
- Graceful shutdown ka substitute nahi

## 36. Daemon Process

```python
p = multiprocessing.Process(target=worker, daemon=True)
```

## 37. OOP Connection

```python
p = multiprocessing.Process(...)   # Object
p.start()                          # Method
pool = multiprocessing.Pool()      # Object
q = multiprocessing.Queue()        # Object
```

## 38. Full HVAC Architecture

```
BMS data → Main Process → Task Queue
                          ├── Process 1 → AHU analytics
                          └── Process 2 → VAV analytics
                                          ↓
                                    Result Queue
                                          ↓
                                     Main Process
```

## 39. Threading + Multiprocessing

```
Main Process
├── Thread → API I/O
├── Thread → Database I/O
└── Process Pool → CPU Tasks
```

## 40. Golden Decision Rule

```
I/O-bound → threading/async
CPU-heavy → multiprocessing
Workers data exchange → Queue
Direct 2 processes → Pipe
```

## 41. Complete Map

```
CONCURRENCY
├── threading
│   ├── Thread
│   ├── Lock
│   ├── RLock
│   ├── Semaphore
│   ├── Event
│   ├── Condition
│   ├── Barrier
│   └── Timer
├── queue
│   ├── Queue
│   ├── LifoQueue
│   └── PriorityQueue
└── multiprocessing
    ├── Process
    ├── Pool
    ├── Queue
    └── Pipe
```

## 42. Key Concepts

```
Thread → same process execution path
Process → independent environment
Lock → one at a time
RLock → reentrant
Semaphore → limited access
Event → signal
Condition → condition wait
Barrier → all sync
Queue → task passing
Pipe → direct process comm
```

## 43. Architecture

```
I/O-bound → Threading
CPU-bound → Multiprocessing
Producer → Consumer → Queue
Process A ↔ Process B → Pipe
```

---

**Ab ye guide complete hai (Lessons 81-90).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ Golden rules

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀