Bilkul. Hum **Lesson 81 se 90** tak **ek ek karke**, Roman Urdu mein **concept → syntax → practical example → faida → common mistakes → OOP/real-world connection** ke sath karenge.

### Sequence

1. **Lesson 81:** `typing.override`
2. **Lesson 82:** `mypy` deeply
3. **Lesson 83:** `pyright` / `basedpyright`
4. **Lesson 84:** `pyre` / `pytype`
5. **Lesson 85:** Type Stubs — `.pyi`, `typeshed`
6. **Lesson 86:** Runtime Type Checking
7. **Lesson 87:** `threading` — Thread, Lock, RLock, Semaphore, Event
8. **Lesson 88:** `Condition`, `Barrier`, `Timer`
9. **Lesson 89:** `queue`
10. **Lesson 90:** `multiprocessing` — Process, Pool, Queue, Pipe

Hum **Lesson 81** se start karte hain.

# Lesson 81 — `typing.override`

## 1. `override` kya hai?

`override` Python typing ka ek **explicit marker** hai jo batata hai:

> "Ye child class ka method intentionally parent class ke method ko override kar raha hai."

Example:

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

Yahan:

```python
@override
def speak(...)
```

ka matlab hai:

**Dog ka `speak()` method, Animal ke `speak()` ko override kar raha hai.**

---

# 2. `override` khud method ko change nahi karta

Ye bohat important point hai.

```python
@override
def speak(self):
    return "Bark"
```

`@override` runtime par method ka behavior change nahi karta.

Ye primarily **type checker ko information deta hai**.

For example:

```text
Parent
  │
  │ speak()
  ▼
Child
  │
  │ @override
  ▼
speak()
```

Type checker check karta hai:

> Kya parent mein waqai `speak()` exist karta hai?

---

# 3. `@override` ke baghair problem

Suppose parent class:

```python
class Animal:

    def speak(self) -> str:
        return "Animal"
```

Aur child mein galti se:

```python
class Dog(Animal):

    def speek(self) -> str:
        return "Bark"
```

Notice:

```text
speak   ← parent
speek   ← child
```

Sirf spelling mistake ki wajah se method override nahi hua.

Python normally isay error nahi samjhega.

```python
dog = Dog()

print(dog.speak())
```

Output:

```text
Animal
```

Developer shayad expect kar raha tha:

```text
Bark
```

Lekin typo ki wajah se parent method chal raha hai.

---

# 4. `@override` yahan useful hai

```python
from typing import override


class Animal:

    def speak(self) -> str:
        return "Animal"


class Dog(Animal):

    @override
    def speek(self) -> str:
        return "Bark"
```

Ab type checker kahega:

```text
Method "speek" is marked as override,
but no base method is overridden
```

Yani:

> "Tum keh rahe ho ye override hai, lekin parent mein `speek()` naam ka method hai hi nahi."

Ye **typo detection** ka bohat useful mechanism hai.

---

# 5. `override` ka real faida

Socho large project hai:

```python
class HVACController:

    def start(self):
        ...

    def stop(self):
        ...

    def set_temperature(self, temperature: float):
        ...
```

Child:

```python
class AHUController(HVACController):

    @override
    def start(self):
        ...

    @override
    def stop(self):
        ...

    @override
    def set_temperature(self, temperature: float):
        ...
```

Ab parent API change ho:

```python
class HVACController:

    def start(self):
        ...

    def stop(self):
        ...

    def set_setpoint(self, temperature: float):
        ...
```

Parent mein:

```text
set_temperature()
       ↓
rename
       ↓
set_setpoint()
```

Child mein purana:

```python
@override
def set_temperature(...):
```

Type checker immediately bata sakta hai:

> Ye ab parent method override nahi kar raha.

Is tarah `@override` **refactoring safety** deta hai.

---

# 6. `override` aur inheritance

Basic structure:

```python
class Parent:

    def show(self):
        print("Parent")


class Child(Parent):

    @override
    def show(self):
        print("Child")
```

Object:

```python
obj = Child()

obj.show()
```

Output:

```text
Child
```

Yahan normal Python inheritance hi kaam kar rahi hai.

`@override` sirf explicitly document karta hai:

```text
Child.show()
       │
       └── overrides Parent.show()
```

---

# 7. Parent method ka signature bhi important hai

Suppose:

```python
class Parent:

    def calculate(self, x: int) -> int:
        return x * 2
```

Child:

```python
class Child(Parent):

    @override
    def calculate(self, x: str) -> str:
        return x.upper()
```

Yahan method ka naam same hai:

```text
calculate
```

Lekin contract completely different hai:

```text
Parent:
int → int

Child:
str → str
```

Type checker is design ko flag kar sakta hai because overriding method ko parent ke substitutability rules follow karne hote hain.

Ye humein tumhare pehle wale concepts se connect karta hai:

**Liskov Substitution Principle (LSP)**.

---

# 8. `override` aur LSP

Tumne pehle inheritance, covariance aur contravariance padha tha.

Ab connection dekho:

```text
Parent
  │
  │ contract
  ▼
Child
  │
  │ override
  ▼
same conceptual contract
```

Agar parent kehta hai:

```python
def process(value: int) -> str:
    ...
```

Child ko arbitrary incompatible contract nahi banana chahiye.

`@override` type checker ko opportunity deta hai ke wo inheritance relationship ko verify kare.

---

# 9. `override` vs normal method

### Without override

```python
class Parent:

    def run(self):
        ...


class Child(Parent):

    def run(self):
        ...
```

Python ke liye perfectly valid.

### With override

```python
from typing import override


class Parent:

    def run(self):
        ...


class Child(Parent):

    @override
    def run(self):
        ...
```

Ab developer explicitly keh raha hai:

> "Main intentionally parent ka `run()` replace kar raha hoon."

---

# 10. `override` documentation bhi hai

Large codebase mein kisi developer ko child class mile:

```python
class AHU(AHUBase):

    @override
    def start(self):
        ...
```

Usay immediately samajh aa jata hai:

```text
start()
  ↓
parent se inherited contract
  ↓
child intentionally customize kar raha hai
```

Is liye `@override`:

* type safety
* refactoring safety
* readability
* documentation
* typo detection

mein useful hai.

---

# 11. `typing.override` vs old approaches

Modern Python mein:

```python
from typing import override
```

Use kiya ja sakta hai.

Older Python versions mein commonly:

```python
typing_extensions
```

se compatibility provide ki jati thi.

Example:

```python
from typing_extensions import override
```

Agar project older Python versions support karta ho to ye approach useful ho sakti hai.

---

# 12. `@override` ko yaad rakhne ka simple formula

```text
Inheritance
     ↓
Parent method
     ↓
Child same method
     ↓
@override
     ↓
"Main intentionally parent method override kar raha hoon"
```

### Sabse important baat:

`@override` **Python ko override karna nahi sikhata**.

Python already inheritance ke through override karta hai.

`@override` **type checker ko tumhari intention batata hai**.

---

## 13. Real-world example

```python
from typing import override


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
```

Use:

```python
ahu = AHU()

print(ahu.start())
print(ahu.stop())
```

Output:

```text
AHU fan started
AHU fan stopped
```

Yahan:

```text
Equipment
    │
    ├── start()
    └── stop()
          │
          ▼
         AHU
          │
          ├── @override start()
          └── @override stop()
```

---

# 14. Ek important distinction

`@override` **runtime validation system nahi hai**.

Yani ye:

```python
@override
def start(self):
    ...
```

automatically production mein ye guarantee nahi karta ke method correctly override hua hai.

Iska major purpose **static type checking** hai.

Isliye ye tools ke sath powerful hai:

```text
Python code
    ↓
@override
    ↓
mypy / pyright / basedpyright
    ↓
errors detect
```

Aur isi wajah se **Lesson 82 — `mypy` deeply** naturally next step hai.

### Lesson 81 ka core concept

> **`@override` = "Child class mein ye method parent class ke method ko intentionally override karta hai; type checker is relationship ko verify kare."**

Agle lesson mein hum **Lesson 82: `mypy` deeply — configuration, `mypy.ini`, `pyproject.toml`, strict mode, plugins, error codes, `reveal_type`, gradual typing** ko detail mein dekhenge.
# Lesson 82 — `mypy` Deeply

### Configuration, Plugins, Strict Mode

`mypy` Python ka **static type checker** hai.

Simple words mein:

> Python code run kiye baghair `mypy` tumhare type hints ko check karta hai aur possible type errors pehle hi bata deta hai.

Example:

```python
def add(a: int, b: int) -> int:
    return a + b


result = add("10", 20)
```

Python normally function define karne par error nahi deta. Lekin:

```bash
mypy app.py
```

type checker kahega ke `"10"` `int` nahi hai.

---

# 1. `mypy` ka basic workflow

```text
Python source code
       ↓
Type hints
       ↓
mypy
       ↓
Static analysis
       ↓
Type errors / warnings
```

Important:

```text
mypy ≠ Python interpreter
mypy ≠ unit testing
mypy ≠ runtime validation
```

Ye **static analysis** hai.

---

# 2. Install

Windows par:

```bash
python -m pip install mypy
```

Check:

```bash
mypy --version
```

Ya:

```bash
python -m mypy --version
```

---

# 3. Sabse simple example

File:

```python
# app.py

def multiply(a: int, b: int) -> int:
    return a * b


x = multiply(10, 5)

y = multiply("10", 5)
```

Run:

```bash
mypy app.py
```

Conceptually output:

```text
app.py:9: error:
Argument 1 to "multiply" has incompatible type "str";
expected "int"
```

Yani error **program run hone se pehle** detect ho gaya.

---

# 4. `mypy` ka sabse important concept — static typing

Python dynamically typed language hai.

```python
x = 10
x = "hello"
x = [1, 2, 3]
```

Python allow karta hai.

Lekin type hints ke through hum intention express karte hain:

```python
x: int = 10
```

Phir:

```python
x: int = "hello"
```

`mypy` isay flag kar sakta hai.

---

# 5. Function return type checking

```python
def get_temperature() -> float:
    return "25"
```

`mypy` kahega:

```text
Incompatible return value type
```

Correct:

```python
def get_temperature() -> float:
    return 25.0
```

---

# 6. `mypy` sirf variables nahi check karta

Ye bhi check karta hai:

### Function arguments

```python
def start_motor(speed: int):
    ...
```

### Return values

```python
def get_speed() -> int:
    ...
```

### Attributes

```python
class Motor:
    speed: int
```

### Classes

```python
class AHU:
    ...
```

### Inheritance

```python
class Child(Parent):
    ...
```

### Generic types

```python
list[int]
dict[str, float]
```

### Protocols

```python
Protocol
```

### Overloads

```python
@overload
```

### `TypedDict`

```python
TypedDict
```

etc.

---

# 7. `mypy` without configuration

Tum directly:

```bash
mypy app.py
```

chala sakte ho.

Lekin real projects mein usually configuration file hoti hai.

Common options:

```text
mypy.ini
pyproject.toml
setup.cfg
```

Modern projects mein `pyproject.toml` bohat common hai.

---

# 8. `mypy.ini`

Example:

```ini
[mypy]

python_version = 3.12

strict = true
```

Ab:

```bash
mypy .
```

project ke code ko check karega.

---

# 9. `pyproject.toml`

Modern approach:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

Phir:

```bash
mypy .
```

Mypy configuration automatically read kar sakta hai.

---

# 10. `strict = true`

Ye bohat important hai.

Normal:

```bash
mypy app.py
```

relatively relaxed ho sakta hai.

Strict mode:

```ini
[mypy]
strict = true
```

zyada type checking enable karta hai.

Conceptually:

```text
Normal mypy
   ↓
basic type checking

strict mypy
   ↓
basic
+
missing annotations
+
untyped functions
+
implicit Any
+
override problems
+
etc.
```

---

# 11. Strict mode kyun useful hai?

Example:

```python
def calculate(x):
    return x * 2
```

Normal project mein ye potentially accept ho sakta hai.

Lekin strict mode mein missing annotation problem ban sakti hai.

Better:

```python
def calculate(x: int) -> int:
    return x * 2
```

Ab code ka contract clear hai.

---

# 12. `Any` ka problem

Ye:

```python
def process(value: Any):
    ...
```

type safety ko weaken karta hai.

Because:

```text
Any
 ↓
almost anything allowed
```

Example:

```python
from typing import Any

x: Any = 10

x = "hello"
x = []
x = object()
```

`Any` basically type checker ko kehta hai:

> "Is value ke type ko aggressively check mat karo."

Strict mode ka ek important purpose hai **unnecessary Any ko reduce karna**.

---

# 13. `disallow_untyped_defs`

Configuration:

```ini
[mypy]
disallow_untyped_defs = true
```

Ab:

```python
def calculate(x):
    return x * 2
```

problem.

Correct:

```python
def calculate(x: int) -> int:
    return x * 2
```

---

# 14. `disallow_any_generics`

Example:

```python
def process(items: list):
    ...
```

Better:

```python
def process(items: list[int]):
    ...
```

Strict typing mein generic containers ko precise banana important hai.

---

# 15. `no_implicit_optional`

Ye concept bohat important hai.

Suppose:

```python
def greet(name: str = None):
    ...
```

Modern typing ke perspective se ye logically problematic hai because:

```text
name:
str
ya
None
```

hona chahiye.

Better:

```python
def greet(name: str | None = None):
    ...
```

Yani:

```text
str | None
```

explicitly batata hai ke `None` allowed hai.

---

# 16. `warn_return_any`

Suppose:

```python
from typing import Any


def get_value() -> Any:
    return 10


def calculate() -> int:
    return get_value()
```

`Any` return type ki wajah se type safety weak ho sakti hai.

Strict configuration is tarah ke situations ko detect karne mein madad karti hai.

---

# 17. Error codes

Mypy errors ko codes ke sath show kar sakta hai.

Example concept:

```text
[assignment]
[arg-type]
[return-value]
[override]
```

Useful command:

```bash
mypy --show-error-codes app.py
```

Example:

```text
error: Argument 1 has incompatible type "str"; expected "int" [arg-type]
```

Ab tum specific error ko target kar sakte ho.

---

# 18. Specific error ignore karna

Suppose genuinely exception hai:

```python
value = something()  # type: ignore[arg-type]
```

Yahan:

```text
type: ignore
```

blindly use karne ke bajaye:

```text
type: ignore[arg-type]
```

better hai.

Kyun?

Because tum clearly bata rahe ho:

> Main specifically `arg-type` warning ko ignore kar raha hoon.

---

# 19. `reveal_type()`

Tumne pehle `reveal_type` padha tha.

Mypy mein ye extremely useful debugging tool hai.

```python
x = 100

reveal_type(x)
```

Mypy bata sakta hai:

```text
Revealed type is "builtins.int"
```

Example:

```python
items = [1, 2, 3]

reveal_type(items)
```

Result conceptually:

```text
list[int]
```

Ye runtime debugging nahi hai.

`reveal_type()` primarily **type checker ke liye** hai.

---

# 20. Type narrowing

Example:

```python
def process(value: str | int) -> None:

    if isinstance(value, str):
        reveal_type(value)

    else:
        reveal_type(value)
```

Mypy samajhta hai:

```text
if branch
    ↓
str

else
    ↓
int
```

Ye tumhare pehle wale:

**TypeGuard / TypeIs / narrowing**

concept se directly connected hai.

---

# 21. Mypy + `@override`

Lesson 81 ka connection:

```python
from typing import override


class Parent:

    def start(self) -> None:
        ...


class Child(Parent):

    @override
    def start(self) -> None:
        ...
```

Mypy inheritance relationship ko check karta hai.

Agar:

```python
@override
def starts(self):
    ...
```

ho:

Mypy bata sakta hai ke parent mein `starts()` exist nahi karta.

---

# 22. Mypy + Protocol

Example:

```python
from typing import Protocol


class Startable(Protocol):

    def start(self) -> None:
        ...


class Motor:

    def start(self) -> None:
        print("Motor started")
```

Function:

```python
def run(device: Startable) -> None:
    device.start()
```

Mypy samajhta hai:

```text
Motor
  │
  │ has start()
  ▼
compatible with Startable
```

Ye **structural typing** hai.

---

# 23. Mypy + Generic

```python
from typing import TypeVar

T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]
```

Mypy inference kar sakta hai:

```python
x = first([1, 2, 3])
```

approximately:

```text
T = int
x = int
```

Aur:

```python
name = first(["Ali", "Ahmed"])
```

```text
T = str
name = str
```

---

# 24. Mypy plugins

Ab advanced part.

Mypy ko plugins ke through kuch libraries/frameworks ke special typing behavior samjhaya ja sakta hai.

Concept:

```text
Mypy
  │
  ├── normal type analysis
  │
  └── plugin
        ↓
     special library behavior
```

Historically plugins ka use kuch frameworks/libraries ke advanced typing patterns ke liye hua hai.

Example conceptual configuration:

```ini
[mypy]
plugins = some_plugin
```

Plugin configuration project/library-specific hoti hai; blindly plugin add nahi karna chahiye.

---

# 25. Mypy aur runtime mein difference

Ye sabse important distinction hai:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Mypy:

```text
static analysis
```

Python:

```text
runtime execution
```

Agar external data aaye:

```python
user_input = input()
```

Mypy automatically runtime par user ko force nahi karega ke integer hi enter kare.

Agar actual runtime validation chahiye:

```text
mypy
   ≠
runtime validation
```

Isi wajah se **Lesson 86 — typeguard / beartype / pydantic** important hoga.

---

# 26. Mypy ka architecture mentally aise samjho

```text
                 Python Code
                     │
                     ▼
                 Type Hints
                     │
                     ▼
                   mypy
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Variables   Functions   Classes
          │          │          │
          └──────────┼──────────┘
                     ▼
              Type Inference
                     │
                     ▼
              Type Checking
                     │
                     ▼
              Error / Success
```

---

# 27. Practical project configuration

Aik serious project mein tum kuch is tarah rakh sakte ho:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
show_error_codes = true
```

Run:

```bash
mypy .
```

Aur specific file:

```bash
mypy app.py
```

---

# 28. Mypy ko yaad rakhne ka formula

```text
mypy
 │
 ├── Static type checker
 │
 ├── Type inference
 │
 ├── Type validation
 │
 ├── Generic checking
 │
 ├── Protocol checking
 │
 ├── Inheritance checking
 │
 ├── @override checking
 │
 ├── Strict mode
 │
 ├── Error codes
 │
 ├── Configuration
 │
 └── Plugins
```

### One-line concept

> **`mypy` Python code ko execute kiye baghair type system ke rules ke against analyze karta hai.**

Aur tumhari series mein iska natural next step hai:

# Lesson 83 — `pyright` / `basedpyright`

Ismein hum dekhenge ke **mypy aur Pyright mein actual difference kya hai**, type inference kis ka strong hai, VS Code integration, strict mode, configuration aur **basedpyright kyun exist karta hai**.
# Lesson 83 — `pyright` / `basedpyright`

### Alternative Type Checkers

Ab hum `mypy` ke baad **Pyright** ko samjhte hain.

Basic idea:

```text
Python code
    │
    ├── mypy
    │
    ├── pyright
    │
    └── basedpyright
```

Teeno ka major purpose **static type checking** hai, lekin inki implementation, configuration aur analysis behavior different hai.

---

# 1. Pyright kya hai?

**Pyright** Python ka static type checker hai.

Iska purpose:

> Python code ko execute kiye baghair type-related problems detect karna.

Example:

```python
def add(a: int, b: int) -> int:
    return a + b


result = add("10", 20)
```

Pyright detect karega ke:

```text
"10" → str
10   → int
```

lekin function expect karta hai:

```text
int
```

---

# 2. Pyright aur Python ka relation

Important:

```text
Python
  ↓
runtime language

Pyright
  ↓
static analyzer
```

Pyright tumhara program execute karke normal runtime error find nahi karta.

Ye code ko analyze karta hai.

---

# 3. Pyright install

Pyright Node.js ecosystem se originate hua hai.

NPM ke through:

```bash
npm install -g pyright
```

Check:

```bash
pyright --version
```

Python environment mein bhi Pyright ko use karne ke alternative installation approaches available hain, lekin project setup ke hisaab se installation choose karna better hota hai.

---

# 4. Basic usage

File:

```python
# app.py

def multiply(a: int, b: int) -> int:
    return a * b


result = multiply("10", 5)
```

Run:

```bash
pyright app.py
```

Conceptually:

```text
Argument of type "Literal['10']"
cannot be assigned to parameter "a" of type "int"
```

Yani Pyright ne problem detect kar li.

---

# 5. Pyright ka important feature — strong inference

Pyright ka ek major strength **type inference** hai.

Example:

```python
numbers = [1, 2, 3]
```

Pyright infer kar sakta hai:

```text
numbers → list[int]
```

Phir:

```python
first = numbers[0]
```

infer:

```text
first → int
```

Tumhein har jagah explicitly:

```python
numbers: list[int]
first: int
```

likhne ki zaroorat nahi.

---

# 6. Type inference kya hota hai?

Tumne pehle `TypeVar`, generics aur `reveal_type` padha hai.

Example:

```python
x = 10
```

Checker infer karta hai:

```text
x → int
```

Example:

```python
name = "Nouman"
```

infer:

```text
name → str
```

Example:

```python
items = [1, 2, 3]
```

infer:

```text
list[int]
```

Ye **type inference** hai.

---

# 7. `pyrightconfig.json`

Pyright project configuration ke liye commonly:

```text
pyrightconfig.json
```

use karta hai.

Example:

```json
{
    "include": [
        "src"
    ],
    "exclude": [
        "**/__pycache__"
    ],
    "typeCheckingMode": "strict"
}
```

Phir:

```bash
pyright
```

Pyright configuration read karke project analyze karega.

---

# 8. `typeCheckingMode`

Pyright mein important setting:

```json
"typeCheckingMode": "strict"
```

Modes conceptually:

```text
off
basic
standard
strict
```

Strict mode:

```json
{
    "typeCheckingMode": "strict"
}
```

zyada aggressive type checking karta hai.

---

# 9. Basic vs Strict

Example:

```python
def calculate(value):
    return value * 2
```

Basic checking mein kuch situations tolerate ho sakti hain.

Strict checking mein missing type information ko zyada seriously treat kiya ja sakta hai.

Better:

```python
def calculate(value: int) -> int:
    return value * 2
```

---

# 10. Pyright + VS Code

Pyright ka ecosystem **VS Code** ke sath bohat strong hai.

VS Code mein Python development ke dauran:

```text
code
 ↓
Pyright language analysis
 ↓
diagnostics
 ↓
editor mein underline
```

Example:

```python
x: int = "hello"
```

Editor immediately type error highlight kar sakta hai.

Iska advantage ye hai ke tumhe har baar:

```bash
pyright app.py
```

manually run karne ki zaroorat nahi padti.

---

# 11. Language Server concept

Yahan ek important concept hai:

### Type checker

```text
pyright
```

### Language server

```text
Pyright-based language intelligence
```

Editor ko ye information mil sakti hai:

* type information
* autocomplete
* diagnostics
* go to definition
* symbol information
* documentation
* references

Isliye Pyright ka practical development experience strong hai.

---

# 12. `reveal_type` concept

Pyright mein bhi type investigation ki facility hai.

Example:

```python
numbers = [1, 2, 3]

reveal_type(numbers)
```

Checker type report kar sakta hai:

```text
list[int]
```

Ye tumhare previous Lesson 72 ke:

```text
reveal_type()
```

concept se directly connected hai.

---

# 13. Type narrowing

Pyright type narrowing bhi karta hai.

Example:

```python
def process(value: str | int):

    if isinstance(value, str):
        value.upper()
    else:
        value.bit_length()
```

Checker samajhta hai:

```text
if
 ↓
str

else
 ↓
int
```

Ye tumhare:

```text
TypeGuard
TypeIs
isinstance()
Union narrowing
```

concepts se related hai.

---

# 14. `Literal`

Example:

```python
from typing import Literal


def set_mode(
    mode: Literal["auto", "manual"]
) -> None:
    ...
```

Valid:

```python
set_mode("auto")
set_mode("manual")
```

Invalid:

```python
set_mode("random")
```

Pyright literal constraints ko analyze kar sakta hai.

---

# 15. `TypedDict`

Example:

```python
from typing import TypedDict


class Equipment(TypedDict):
    id: str
    floor: int
```

Then:

```python
equipment: Equipment = {
    "id": "AHU-01",
    "floor": 34
}
```

Pyright keys aur values ko type-check kar sakta hai.

Agar:

```python
equipment = {
    "id": 100,
    "floor": "34"
}
```

to errors detect honge.

---

# 16. Protocol

Tumne `Protocol` deeply padha hai.

Example:

```python
from typing import Protocol


class Startable(Protocol):

    def start(self) -> None:
        ...
```

Aur:

```python
class Motor:

    def start(self) -> None:
        print("Started")
```

Function:

```python
def run(device: Startable):
    device.start()
```

Pyright structural compatibility analyze kar sakta hai:

```text
Motor
  │
  ├── start()
  │
  ▼
matches Startable
```

---

# 17. Generic inference

Example:

```python
from typing import TypeVar

T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]
```

Call:

```python
number = first([10, 20, 30])
```

Checker infer:

```text
T = int
number = int
```

Aur:

```python
name = first(["Ali", "Ahmed"])
```

infer:

```text
T = str
name = str
```

---

# 18. Pyright vs mypy

Ab important comparison:

| Feature                   | mypy       | Pyright              |
| ------------------------- | ---------- | -------------------- |
| Static type checking      | ✅          | ✅                    |
| Type inference            | Strong     | Very strong          |
| Generics                  | ✅          | ✅                    |
| Protocol                  | ✅          | ✅                    |
| TypedDict                 | ✅          | ✅                    |
| `@override`               | ✅          | ✅                    |
| Strict checking           | ✅          | ✅                    |
| VS Code integration       | Good       | Excellent            |
| `pyproject.toml`          | ✅          | ✅                    |
| Dedicated config          | `mypy.ini` | `pyrightconfig.json` |
| Language-server ecosystem | Good       | Very strong          |

Ye table absolute "better/worse" ranking nahi hai. Dono ke type-system interpretations aur diagnostics mein differences hain.

---

# 19. Mypy aur Pyright ek hi project mein?

Technically:

```text
Project
   │
   ├── mypy
   │
   └── pyright
```

dono run kiye ja sakte hain.

Lekin beginner project mein normally unnecessary complexity hai.

Kyun?

Dono kabhi kabhi same code par different diagnostics de sakte hain.

Example:

```text
mypy
  ↓
OK

Pyright
  ↓
warning/error
```

Ya opposite.

Isliye team ko usually ek primary checker choose karna chahiye.

---

# 20. `basedpyright` kya hai?

Ab third naam:

```text
basedpyright
```

BasedPyright, Pyright ka **community-maintained fork** hai jo Pyright ke upar additional checking/configuration/features provide karta hai.

Conceptually:

```text
Pyright
   │
   └── fork
         ↓
    BasedPyright
```

Isliye:

```text
Python
  │
  ├── mypy
  ├── pyright
  └── basedpyright
```

teen alternatives samjho.

---

# 21. BasedPyright kyun bana?

Basic philosophy:

> Pyright ke type-checking foundation ko maintain karte hue additional strictness aur developer-focused improvements provide karna.

BasedPyright projects mein especially useful ho sakta hai jahan developers **strong static typing** aur stricter diagnostics chahte hain.

---

# 22. BasedPyright configuration

BasedPyright Pyright-compatible configuration concepts use karta hai.

Example:

```json
{
    "include": ["src"],
    "typeCheckingMode": "strict"
}
```

Command:

```bash
basedpyright
```

---

# 23. Pyright vs BasedPyright

Simple mental model:

```text
Pyright
   ↓
Microsoft-originated Python type checker

BasedPyright
   ↓
Pyright-based community fork
   ↓
additional checks / stricter philosophy
```

BasedPyright ko Pyright ka completely different type checker samajhna sahi nahi hoga.

---

# 24. Pyright ka real-world example

Suppose tumhara HVAC project hai:

```python
from dataclasses import dataclass


@dataclass
class AHU:
    name: str
    airflow: float
    running: bool


def start_ahu(ahu: AHU) -> None:
    ahu.running = True
```

Ab:

```python
ahu = AHU(
    name="AHU-01",
    airflow=1200.0,
    running=False
)

start_ahu(ahu)
```

Type checker samajhta hai:

```text
ahu
 ↓
AHU

airflow
 ↓
float

running
 ↓
bool
```

Agar galti se:

```python
ahu = AHU(
    name="AHU-01",
    airflow="1200",
    running=False
)
```

to static checker problem detect karega:

```text
str
 ↓
expected float
```

---

# 25. `mypy` → `pyright` mental connection

Tum Lesson 82 mein ye seekh chuke ho:

```text
mypy
 │
 ├── configuration
 ├── strict
 ├── error codes
 ├── plugins
 └── type analysis
```

Ab Pyright:

```text
pyright
 │
 ├── configuration
 ├── typeCheckingMode
 ├── strict
 ├── inference
 ├── narrowing
 ├── editor integration
 └── diagnostics
```

---

# 26. Sabse important difference

Ek beginner ke liye simple rule:

### Mypy

```text
"Python typing ka traditional/static type checker"
```

### Pyright

```text
"Fast, powerful type inference + excellent editor integration"
```

### BasedPyright

```text
"Pyright-based checker with a stricter/community-driven approach"
```

Ye oversimplification hai, lekin learning ke liye useful mental model hai.

---

# 27. Kab kaunsa use karna?

### Mypy

Agar:

```text
existing Python project
+
strong typing
+
mature ecosystem
```

to Mypy excellent choice hai.

### Pyright

Agar:

```text
VS Code
+
excellent type inference
+
interactive development
```

important hai, Pyright strong choice hai.

### BasedPyright

Agar:

```text
very strict typing
+
additional diagnostics
+
Pyright-compatible ecosystem
```

chahiye, BasedPyright consider kar sakte ho.

---

# 28. Lesson 83 ka core concept

```text
             Static Type Checking
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      mypy         pyright     basedpyright
        │            │            │
   mature         inference     stricter
   checker        + editor      Pyright fork
```

**Important:** Ye teeno Python ko replace nahi karte. Ye Python code ko **analyze** karte hain.

### Ek line mein:

> **Pyright Python ka powerful static type checker hai, jabke BasedPyright Pyright-based community fork hai jo additional strictness aur checks provide karta hai.**

**Next: Lesson 84 — `pyre` / `pytype`**, jahan hum dekhenge ke ye dono kya hain, kis ne banaye, unka type inference approach kya hai, aur `mypy`/`pyright` ke muqable mein kahan fit hote hain.
# Lesson 84 — `pyre` / `pytype`

### Other Python Type Checkers

Ab hum do aur static type checkers dekhenge:

```text
Python Type Checkers
│
├── mypy
├── pyright
├── basedpyright
├── pyre
└── pytype
```

In sab ka basic goal similar hai:

> **Python code ko run kiye baghair uske types ko analyze karna.**

Lekin architecture aur philosophy different hai.

---

# 1. `pyre` kya hai?

**Pyre** ek Python static type checker hai jo Meta (Facebook) ne develop kiya tha.

Basic idea:

```text
Python source
      ↓
Pyre
      ↓
Static type analysis
      ↓
Type errors
```

Pyre ka focus historically **large Python codebases** aur fast incremental type checking par raha hai.

---

# 2. Pyre ka basic example

```python
def add(a: int, b: int) -> int:
    return a + b
```

Correct.

Lekin:

```python
result = add("10", 20)
```

Pyre type mismatch identify kar sakta hai.

Concept:

```text
"10"
 ↓
str

expected
 ↓
int
```

---

# 3. Pyre ka naam

Pyre ko roughly:

```text
Py + RE
```

ke naam se yaad kar sakte ho, lekin practical learning mein naam se zyada important iska role hai:

> **Python static type checker.**

---

# 4. Pyre ka configuration

Pyre projects mein configuration file commonly:

```text
.pyre_configuration
```

use karti hai.

Example conceptual configuration:

```json
{
    "source_directories": [
        "src"
    ]
}
```

Phir project ko Pyre se analyze kiya ja sakta hai.

---

# 5. Pyre aur annotations

Example:

```python
def calculate(value: int) -> int:
    return value * 2
```

Pyre:

```text
value → int
return → int
```

ko track karta hai.

Agar:

```python
def calculate(value: int) -> int:
    return "hello"
```

to return type mismatch detect ho sakta hai.

---

# 6. Pyre ka important concept — incremental checking

Large project imagine karo:

```text
100 files
1000 files
10000 files
```

Agar har choti modification par poora project dobara analyze ho to expensive ho sakta hai.

Pyre ka architecture **incremental type checking** ko strongly support karta hai.

Concept:

```text
Initial check
     ↓
Entire project

Later:
small change
     ↓
affected code
     ↓
incremental analysis
```

Ye large codebase ke liye useful hai.

---

# 7. Pyre + strict typing

Pyre mein type checking ko gradually introduce kiya ja sakta hai.

Real-world project mein:

```text
Untyped Python
      ↓
Partial annotations
      ↓
More annotations
      ↓
Static checking
      ↓
Stronger type safety
```

Ye tumhare **gradual typing** concept se directly connected hai.

---

# 8. Pyre ka `Any` concept

Python typing mein:

```python
from typing import Any

value: Any
```

type checker ko limited information deta hai.

General concept:

```text
Any
 ↓
type information weak
```

Large projects mein static checker ka ek important goal hota hai ke gradually:

```text
Any
 ↓
specific types
```

ki taraf move kiya jaye.

---

# 9. Pyre ka architecture

Simple mental model:

```text
             Python Project
                    │
                    ▼
                  Pyre
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Type inference       Type checking
          │                   │
          └─────────┬─────────┘
                    ▼
                  Errors
```

---

# 10. Ab `pytype`

`pytype` Google ka Python type checker hai.

Iska interesting feature ye hai ke ye **existing Python code se types infer karne** par strong focus rakhta hai.

Concept:

```text
Python code
    ↓
pytype
    ↓
Type inference
    ↓
Type errors / type information
```

---

# 11. Pytype ka important difference

Suppose tumhare paas:

```python
def calculate(x):
    return x * 2
```

Tumne annotation nahi di:

```python
x: int
```

ya:

```python
x: float
```

Phir bhi pytype code ko analyze karke type information infer karne ki koshish karta hai.

Yani:

```text
mypy/pyright
     │
     ├── annotations
     └── inference

pytype
     │
     └── inference from Python code
```

Ye simplified comparison hai; modern checkers sab inference karte hain.

---

# 12. Pytype ka example

```python
def double(x):
    return x * 2
```

Agar:

```python
result = double(10)
```

to pytype code flow se type information infer karne ki koshish karta hai.

Conceptually:

```text
10
 ↓
int
 ↓
x
 ↓
x * 2
 ↓
int
```

---

# 13. Pytype ka special historical role

Python ke bohat se existing projects originally:

```python
def function(x):
    ...
```

jaise unannotated code se start hue.

Aise projects mein static analysis ko gradually introduce karne ke liye inference-based tools useful hote hain.

Pytype isi philosophy mein important raha hai.

---

# 14. Pytype aur `.pyi`

Pytype type stub files ke sath bhi work kar sakta hai.

Tumhara Lesson 85 isi concept ko deeply cover karega:

```text
module.py
module.pyi
```

`.pyi` ka matlab:

> **Type information provide karna without implementation details.**

Example:

```python
# math_utils.pyi

def add(a: int, b: int) -> int: ...
```

Implementation alag ho sakti hai.

---

# 15. Pyre vs Pytype

Ab direct comparison:

| Feature               | Pyre                  | Pytype          |
| --------------------- | --------------------- | --------------- |
| Static analysis       | ✅                     | ✅               |
| Type inference        | ✅                     | ✅               |
| Gradual typing        | ✅                     | ✅               |
| Large projects        | Strong focus          | Useful          |
| Existing untyped code | ✅                     | Strong focus    |
| Configuration         | `.pyre_configuration` | `pytype` config |
| Origin                | Meta                  | Google          |

---

# 16. Mypy vs Pyright vs Pyre vs Pytype

Ab tumhare paas four major concepts hain:

| Checker        | Simple mental model                                 |
| -------------- | --------------------------------------------------- |
| `mypy`         | Traditional, mature static type checker             |
| `pyright`      | Fast analysis + strong inference/editor integration |
| `basedpyright` | Pyright-based stricter community fork               |
| `pyre`         | Large-codebase/incremental analysis focus           |
| `pytype`       | Inference-heavy analysis of Python code             |

Ye table **absolute ranking nahi** hai. Real differences version, configuration aur project architecture ke hisaab se change ho sakte hain.

---

# 17. Same Python code, different checkers

Suppose:

```python
def calculate(x):
    return x * 2
```

Different checkers is code ko different levels par analyze kar sakte hain.

```text
             calculate(x)
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      mypy       pyright    pytype
        │          │          │
   annotations   inference   inference
        │          │          │
        └──────────┼──────────┘
                   ▼
              diagnostics
```

Isliye:

> **Static type checker ek single universal Python compiler nahi hai.**

Har checker apna analysis engine use karta hai.

---

# 18. Gradual typing ka connection

Tumne pehle `Any` aur type hints padhe hain.

Python mein tum:

```python
def old_code(x):
    return x
```

se start kar sakte ho.

Phir:

```python
def better_code(x: int) -> int:
    return x
```

Phir:

```python
def better_code(x: int) -> int:
    ...
```

Static checker gradually introduce kiya ja sakta hai.

Is concept ko:

> **Gradual typing**

kehte hain.

---

# 19. Static checker vs runtime checker

Ye distinction ab aur important ho gayi hai.

### Static

```text
mypy
pyright
basedpyright
pyre
pytype
```

Code run kiye baghair analysis.

### Runtime

```text
typeguard
beartype
pydantic
```

Actual runtime values ko validate kar sakte hain.

Example:

```text
Static:
"Is variable ka declared/inferred type kya hai?"

Runtime:
"Is waqt actual value ka type/shape kya hai?"
```

---

# 20. Example — external data

Suppose HVAC API se data aa raha hai:

```python
data = api.get_equipment()
```

External API theoretically bhej sakti hai:

```json
{
    "temperature": "25"
}
```

jabke tum expect kar rahe ho:

```text
temperature → float
```

Static checker external system ko magically control nahi kar sakta.

Yahan runtime validation useful hoti hai.

```text
External API
     ↓
Runtime validation
     ↓
Validated object
     ↓
Static typed Python code
```

Isi liye **Lesson 86** bohat important hai.

---

# 21. Pyre ka practical architecture

Large application:

```text
project/
│
├── src/
│   ├── hvac/
│   ├── equipment/
│   └── controls/
│
├── tests/
│
└── .pyre_configuration
```

Pyre:

```text
             Project
                │
                ▼
               Pyre
                │
        ┌───────┴───────┐
        ▼               ▼
   Type inference   Type checking
        │               │
        └───────┬───────┘
                ▼
            Diagnostics
```

---

# 22. Pytype ka mental model

```text
Python source
      │
      ▼
  Control/data flow
      │
      ▼
 Type inference
      │
      ▼
  Type information
      │
      ▼
  Error detection
```

Yani pytype ko samajhne ke liye **program flow + inference** important concepts hain.

---

# 23. Kya humein sab checkers seekhne chahiye?

**Conceptually: haan.**

Lekin practically:

```text
Deep learning:
    1 primary checker

Understanding:
    baqi checkers
```

Tumhare liye:

```text
mypy
 ↓
deep

pyright
 ↓
deep comparison

pyre / pytype
 ↓
conceptual understanding
```

Ye better learning strategy hai.

---

# 24. Lesson 84 ka core map

```text
Python Static Type Checking
│
├── mypy
│   └── mature/general-purpose
│
├── pyright
│   └── inference + editor ecosystem
│
├── basedpyright
│   └── Pyright-based stricter fork
│
├── pyre
│   └── incremental / large-codebase focus
│
└── pytype
    └── inference-heavy analysis
```

### One-line summary

> **Pyre aur pytype dono Python static type analysis tools hain; Pyre large-scale/incremental analysis ke liye jana jata hai, jabke pytype Python code se type information infer karne par strong focus rakhta hai.**

---

## Next — Lesson 85

Ab hum ek **bohat important professional concept** par aayenge:

**`.pyi` Type Stub Files + `typeshed`**

Ismein hum dekhenge:

```text
.py
.pyi
typeshed
stdlib stubs
third-party stubs
stub-only packages
py.typed
```

aur sabse important sawal:

> **Agar Python library ke andar implementation mein type hints nahi hain, to mypy/pyright ko us library ke functions ke types ka pata kaise chalta hai?**
# Lesson 85 — Type Stubs

## `.pyi` Files + `typeshed`

Ye lesson Python typing architecture ka **bohat important** part hai.

Tumne ab tak dekha:

```text
typing
   ↓
type hints
   ↓
mypy / pyright
   ↓
static checking
```

Ab sawal:

> Agar kisi library ke actual `.py` code mein type hints hi na hon, to `mypy` ya `pyright` ko us library ke types kaise pata chalte hain?

Answer:

```text
Type Stubs
```

---

# 1. Type Stub kya hota hai?

Type stub ek special file hoti hai:

```text
.pyi
```

Iska purpose:

> **Code ki implementation nahi, balki uski type information provide karna.**

Example actual Python file:

```python
# calculator.py

def add(a, b):
    return a + b


def multiply(a, b):
    return a * b
```

Is code mein type hints nahi hain.

Hum separate stub bana sakte hain:

```python
# calculator.pyi

def add(a: int, b: int) -> int: ...

def multiply(a: int, b: int) -> int: ...
```

Ab type checker ko pata hai:

```text
add:
int + int → int

multiply:
int + int → int
```

---

# 2. `.py` vs `.pyi`

Sabse important difference:

### `.py`

Implementation:

```python
def add(a, b):
    return a + b
```

### `.pyi`

Type interface:

```python
def add(a: int, b: int) -> int: ...
```

Mental model:

```text
.py
 │
 ├── implementation
 ├── logic
 └── runtime code


.pyi
 │
 ├── signatures
 ├── types
 └── interface information
```

---

# 3. `.pyi` mein `...` kyun?

Example:

```python
def add(a: int, b: int) -> int: ...
```

Yahan:

```python
...
```

implementation nahi hai.

Ye basically keh raha hai:

> "Function exist karta hai, iska signature ye hai."

Actual implementation `.py` mein ho sakti hai.

---

# 4. Complete example

Suppose:

```text
project/
│
├── calculator.py
└── calculator.pyi
```

`calculator.py`:

```python
def add(a, b):
    return a + b
```

`calculator.pyi`:

```python
def add(a: int, b: int) -> int: ...
```

Application:

```python
from calculator import add

result = add(10, 20)
```

Checker infer karega:

```text
10       → int
20       → int
add()    → int
result   → int
```

---

# 5. Wrong call

Ab:

```python
result = add("10", 20)
```

Actual implementation dynamically execute ho sakti hai.

Lekin type checker `.pyi` dekhega:

```python
def add(a: int, b: int) -> int: ...
```

aur bolega:

```text
"10" → str
expected → int
```

Yani `.pyi` **static type checker ko contract deta hai**.

---

# 6. Stub ka matlab interface

Isko OOP ke context mein samjho.

Tumne pehle:

```text
ABC
Protocol
Interface-like design
```

padha hai.

`.pyi` bhi conceptually **interface description** jaisa hai.

```text
Implementation
     │
     ▼
calculator.py

Public interface
     │
     ▼
calculator.pyi
```

Lekin `.pyi` Python runtime ka traditional interface mechanism nahi hai.

Ye primarily **static typing ecosystem** ke liye hai.

---

# 7. Classes bhi `.pyi` mein define ho sakti hain

Actual:

```python
# motor.py

class Motor:

    def __init__(self, speed):
        self.speed = speed

    def start(self):
        print("Started")
```

Stub:

```python
# motor.pyi

class Motor:

    speed: int

    def __init__(self, speed: int) -> None: ...

    def start(self) -> None: ...
```

Ab checker ko pata:

```text
Motor.speed → int
Motor.start() → None
```

---

# 8. Variables bhi stub mein

```python
MAX_SPEED: int
DEFAULT_NAME: str
```

Example:

```python
# settings.pyi

MAX_SPEED: int
DEFAULT_NAME: str
```

Implementation:

```python
# settings.py

MAX_SPEED = 3000
DEFAULT_NAME = "AHU"
```

---

# 9. Constants

Stub:

```python
DEBUG: bool
VERSION: str
```

Implementation:

```python
DEBUG = True
VERSION = "1.0"
```

Type checker ko interface mil jata hai.

---

# 10. Overload bhi `.pyi` mein

Tumne `typing.overload` padha tha.

Example:

```python
from typing import overload

@overload
def get_value(x: int) -> int: ...

@overload
def get_value(x: str) -> str: ...
```

Stub mein ye especially natural hota hai kyunki stub ka purpose hi signatures describe karna hai.

---

# 11. `.pyi` implementation nahi rakhta

Generally:

```python
# WRONG IDEA

def add(a: int, b: int) -> int:
    return a + b
```

Stub ka main purpose implementation provide karna nahi hai.

Typical:

```python
def add(a: int, b: int) -> int: ...
```

Yani:

```text
.pyi = WHAT
.py  = HOW
```

Ye bohat useful formula hai.

> **`.pyi` batata hai "kya available hai"; `.py` batata hai "kaise implement hua".**

---

# 12. `typeshed` kya hai?

Ab main concept.

```text
typeshed
```

ek large collection/project hai jahan Python standard library aur kuch common third-party packages ke **type information/stubs** maintain ki jati hain.

Mental model:

```text
             typeshed
                │
       ┌────────┴────────┐
       ▼                 ▼
 Standard library    Third-party
    stubs              stubs
```

---

# 13. Standard library ko type information kaise milti hai?

Suppose:

```python
import os

path = os.path.join("D:", "test")
```

Tumne `os.path.join()` ki implementation open nahi ki.

Phir bhi:

```text
pyright
mypy
```

ko pata hota hai ke function ka expected signature kya hai.

Iske peeche standard-library type information/stubs ka ecosystem hai.

Yahan `typeshed` important role play karta hai.

---

# 14. Example — `os`

Conceptually stub mein kuch is type ki information ho sakti hai:

```python
def join(a: str, *paths: str) -> str: ...
```

Ab type checker samajh sakta hai:

```python
result = os.path.join("D:", "Python")
```

Result:

```text
str
```

---

# 15. `typeshed` sirf `.pyi` files ka random folder nahi

Ye ek organized project/ecosystem hai.

Iska major purpose:

```text
Python ecosystem
       ↓
standard library APIs
       ↓
type information
       ↓
static type checkers
```

ko support karna hai.

---

# 16. Third-party libraries aur stubs

Suppose koi old library hai:

```python
import old_library
```

Aur library ke code mein:

```python
def calculate(value):
    ...
```

type annotations nahi.

Community ya maintainers separate stub package provide kar sakte hain.

Example naming pattern:

```text
types-<package-name>
```

Historically Python typing ecosystem mein `types-...` packages common hain.

Example concept:

```bash
pip install types-somepackage
```

Iska matlab:

```text
actual package
+
separate typing information
```

---

# 17. Stub-only package

Suppose actual library:

```text
some_library
```

aur uski type information:

```text
types-some-library
```

To:

```text
some_library
       │
       ├── runtime implementation
       │
       └── types-some-library
                 │
                 └── .pyi
```

Type checker dono concepts ko combine karke static analysis karta hai.

---

# 18. `py.typed`

Ab ek **very important professional concept**.

Suppose tum khud library bana rahe ho:

```text
my_library/
│
├── __init__.py
├── motor.py
└── py.typed
```

`py.typed` ek marker file hai.

Iska meaning roughly:

> **"Ye package type information provide karta hai aur type checkers ko iski typing ko consume karna chahiye."**

---

# 19. `py.typed` file ke andar kya hota hai?

Usually:

```text
py.typed
```

empty marker file hoti hai.

Iska purpose content provide karna nahi, **package metadata/marker** ke taur par typing support indicate karna hai.

---

# 20. Example library

Structure:

```text
hvac_lib/
│
├── __init__.py
├── ahu.py
├── vav.py
└── py.typed
```

`ahu.py`:

```python
class AHU:

    def start(self) -> None:
        print("Started")
```

Ab jab doosra developer install kare:

```bash
pip install hvac_lib
```

type checker package ki typing ko consume kar sakta hai, assuming package properly distributed/configured hai.

---

# 21. Inline typing vs stub typing

Do approaches:

### Approach 1 — inline

```python
# motor.py

def start(speed: int) -> None:
    ...
```

Type information directly implementation mein.

### Approach 2 — stub

```python
# motor.py

def start(speed):
    ...
```

aur:

```python
# motor.pyi

def start(speed: int) -> None: ...
```

Type information separate.

---

# 22. Stub kab useful hota hai?

### Case 1 — Existing untyped library

```text
old_library
    ↓
no annotations
    ↓
.pyi
```

### Case 2 — C extension

Aisi library jiska runtime implementation Python mein directly available nahi.

```text
C/C++ implementation
       ↓
Python API
       ↓
.pyi
```

Type checker ko API samjhane ke liye stubs useful hote hain.

### Case 3 — Generated code

Generated/runtime code ko separately type describe karna.

### Case 4 — Public API hide karna

Implementation complex ho sakti hai:

```text
1000 lines implementation
       ↓
small public API
       ↓
.pyi
```

---

# 23. C extension example

Ye important professional use case hai.

Suppose:

```text
fastmath
```

actually C/C++ mein implemented hai.

Python mein:

```python
import fastmath

result = fastmath.add(10, 20)
```

Type checker ko C implementation ka source directly Python typing ke liye useful form mein nahi mil sakta.

Stub:

```python
# fastmath.pyi

def add(a: int, b: int) -> int: ...
```

Ab:

```text
C implementation
      │
      ▼
runtime behavior

.pyi
      │
      ▼
static type information
```

---

# 24. Stub aur runtime ka relationship

Ye bohat important hai:

```text
                    Runtime
                       │
                       ▼
                    .py / C
                       │
                       │
                    executes
                       │
                       ▼
                   actual value


                    Static
                       │
                       ▼
                     .pyi
                       │
                       │
                    describes
                       │
                       ▼
                  expected types
```

`.pyi` **runtime implementation ko replace nahi karta**.

---

# 25. Type checker stub ko priority kyun de sakta hai?

Agar package ke paas:

```text
module.py
module.pyi
```

dono hon, type-checking ecosystem `.pyi` ko interface/type information ke source ke taur par use kar sakta hai.

Example:

```python
# module.py

def add(a, b):
    return a + b
```

```python
# module.pyi

def add(a: int, b: int) -> int: ...
```

Static checker:

```text
add()
 ↓
.pyi
 ↓
int, int → int
```

---

# 26. Stub mein private implementation details nahi dene padte

Suppose actual:

```python
def calculate(x):
    temp1 = x * 10
    temp2 = temp1 + 50
    return temp2
```

Public API sirf:

```python
def calculate(x: float) -> float: ...
```

Stub mein internal variables ki zaroorat nahi.

Isliye stubs **API surface** ko represent karte hain.

---

# 27. Stub = contract

Isko tum OOP + Protocol ke sath connect karo:

```text
Protocol
   ↓
expected behavior

.pyi
   ↓
expected API/types
```

Dono ka purpose identical nahi hai, lekin mental concept similar hai:

> **"Consumer ko kya interface mil raha hai?"**

---

# 28. `typeshed` ka architecture mentally

```text
                    typeshed
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   Standard library             Stubs
      typing info             for ecosystem
          │                         │
          ▼                         ▼
      os / sys /                 packages
      pathlib /                 etc.
      json / ...
          │
          └────────────┬────────────┘
                       ▼
                Type Checkers
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
            mypy    pyright   others
```

---

# 29. `typeshed` aur `mypy` ka relation

Important:

> `typeshed` **mypy nahi hai**.

```text
typeshed
    ↓
type information/stubs

mypy
    ↓
type checker
```

Mypy in type definitions ko use kar sakta hai.

Isi tarah doosre type checkers bhi appropriate stub sources consume kar sakte hain.

---

# 30. `typeshed` aur Pyright

Similarly:

```text
typeshed
    ↓
standard library type information
    ↓
Pyright
```

Pyright ko standard library APIs ke types understand karne mein stub information help karti hai.

---

# 31. Stub package ka simple example

Suppose:

```text
somepackage/
├── __init__.py
└── api.py
```

No annotations:

```python
def get_equipment(id):
    ...
```

Separate typing package:

```text
types-somepackage/
└── api.pyi
```

Stub:

```python
def get_equipment(id: str) -> Equipment: ...
```

Ab consumer ko type safety mil sakti hai.

---

# 32. Stub aur `Protocol` mein difference

Ye confuse mat karna.

### Protocol

Tum behavior define karte ho:

```python
class Startable(Protocol):
    def start(self) -> None: ...
```

### Stub

Tum module/library ka API describe karte ho:

```python
def start() -> None: ...
```

Simple:

```text
Protocol
→ structural interface

.pyi
→ module/package type interface
```

---

# 33. Stub aur `ABC`

Similarly:

```text
ABC
 ↓
runtime inheritance/interface mechanism

Protocol
 ↓
static structural interface

.pyi
 ↓
external/static API description
```

Ye teen related ideas hain, lekin same cheez nahi.

---

# 34. Professional project mein complete picture

Imagine:

```text
MyProject
│
├── src/
│   ├── hvac/
│   │   ├── ahu.py
│   │   ├── vav.py
│   │   └── py.typed
│   │
│   └── app.py
│
├── tests/
│
└── pyproject.toml
```

External package:

```text
third_party/
│
└── package
      │
      └── type stubs
```

Standard library:

```text
typeshed
```

Type checker:

```text
mypy / pyright
```

Overall:

```text
                 Python Project
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
     Own typing    Third-party    Standard
       .py           stubs        library
         │             │             │
         │             │         typeshed
         └─────────────┼─────────────┘
                       ▼
                 Type Checker
                       │
                       ▼
                  Diagnostics
```

---

# 35. Sabse important 7 terms

Is lesson ke ye terms yaad rakho:

| Term           | Meaning                                      |
| -------------- | -------------------------------------------- |
| `.py`          | Runtime implementation                       |
| `.pyi`         | Type stub/interface description              |
| `typeshed`     | Collection/project of type information       |
| `py.typed`     | Package typing-support marker                |
| stub package   | Separate package containing type information |
| inline typing  | Types directly `.py` mein                    |
| external stubs | Types separate `.pyi` mein                   |

---

# 36. One-line formulas

### `.py`

> **How the program works**

### `.pyi`

> **What API/type contract exists**

### `typeshed`

> **Common Python APIs ke type definitions ka ecosystem**

### `py.typed`

> **Package declares that its inline typing is intended for type checkers**

---

# 37. Lesson 85 ka final mental model

```text
                     Python Library
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       implementation                type info
             │                           │
            .py                         .pyi
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    Static Type Checker
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
              mypy      pyright     pyre
```

### Sabse important concept:

> **`.pyi` file implementation nahi hoti; ye static type checker ko library ke public API, signatures, classes, variables aur types ka contract provide karti hai. `typeshed` standard-library aur related ecosystem ke type information ko organize/provide karta hai.**

---

## Next — Lesson 86

Ab hum **Runtime Type Checking** par jayenge:

```text
typeguard
beartype
pydantic
```

Aur sabse important difference samjhenge:

```text
mypy / pyright
        ↓
compile-time style static analysis

typeguard / beartype
        ↓
runtime checking

pydantic
        ↓
runtime validation + parsing + models
```

Yahan hum dekhenge ke **API se aane wale `dict`/JSON data ko actual validated Python object mein kaise convert kiya jata hai**, jo tumhare Python + HVAC/API work ke liye particularly useful concept hai.
# Lesson 86 — Runtime Type Checking

## `typeguard` + `beartype` + `pydantic`

Ab tak hum **static type checking** par thay:

```text
mypy
pyright
basedpyright
pyre
pytype
```

Ab ek important shift hai:

```text
STATIC                         RUNTIME
────────────────────────────────────────────
mypy                           typeguard
pyright                        beartype
basedpyright                   pydantic
pyre
pytype
```

Sabse pehle fundamental difference samjho.

---

# 1. Static vs Runtime Type Checking

Suppose:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Aur:

```python
result = add("10", 20)
```

### Static checker

```text
mypy
  ↓
code ko analyze karega
  ↓
"str diya gaya hai, int expected hai"
```

### Runtime checker

Program actually run hota hai:

```text
Python
  ↓
add("10", 20)
  ↓
runtime par actual value check
  ↓
error
```

Yani:

> **Static checker source code ko analyze karta hai; runtime checker actual waqt par values ko check karta hai.**

---

# 2. Type hints khud runtime validation nahi karte

Ye bohat important hai.

```python
def set_temperature(value: float) -> None:
    print(value)
```

Ab:

```python
set_temperature("25")
```

Python automatically ye nahi kehta:

```text
❌ "25" is not float
```

Type annotation:

```python
value: float
```

mostly type information hai.

Python automatically har function call par type enforcement nahi karta.

---

# 3. `typeguard` kya hai?

`typeguard` Python ke **runtime type checking** ke liye library hai.

Concept:

```text
Function
   ↓
type annotations
   ↓
typeguard
   ↓
runtime checking
```

Example:

```python
from typeguard import typechecked


@typechecked
def add(a: int, b: int) -> int:
    return a + b
```

Ab:

```python
add(10, 20)
```

valid.

Lekin:

```python
add("10", 20)
```

runtime par type error generate ho sakta hai.

---

# 4. `@typechecked`

Sabse basic mechanism:

```python
from typeguard import typechecked


@typechecked
def calculate(value: int) -> int:
    return value * 2
```

Correct:

```python
calculate(10)
```

Incorrect:

```python
calculate("10")
```

Runtime checking activate ho jati hai.

---

# 5. Static + runtime dono saath

Professional project mein:

```text
               Python Code
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       mypy                 runtime
          │                   │
          ▼                   ▼
   static checking       typeguard
                              │
                              ▼
                        actual values
```

Example:

```python
from typeguard import typechecked


@typechecked
def calculate(value: int) -> int:
    return value * 2
```

Static:

```text
mypy
 ↓
function contract check
```

Runtime:

```text
typeguard
 ↓
actual argument check
```

Dono complementary hain.

---

# 6. `typeguard` return values bhi check kar sakta hai

Example:

```python
from typeguard import typechecked


@typechecked
def get_temperature() -> float:
    return "25"
```

Function annotation keh raha hai:

```text
return → float
```

Lekin actual:

```text
str
```

return ho raha hai.

Runtime checker is mismatch ko detect kar sakta hai.

---

# 7. `typeguard` nested types

Modern Python:

```python
def process(values: list[int]) -> None:
    ...
```

Runtime type checking ka purpose sirf:

```text
list?
```

nahi hota.

Type information:

```text
list[int]
```

mein element type bhi relevant hai.

Example:

```python
process([1, 2, 3])
```

valid.

Potentially:

```python
process([1, "2", 3])
```

type contract violate karta hai.

Runtime type checking libraries nested type structures ko inspect kar sakti hain.

---

# 8. `typeguard` ka main use

Useful situations:

### APIs

```text
API
 ↓
Python function
 ↓
typeguard
```

### Plugin systems

Unknown code tumhare function ko call kar raha hai.

### Dynamic applications

Runtime values external sources se aa rahi hain.

### Development/testing

Unexpected values jaldi detect karna.

---

# 9. Ab `beartype`

`beartype` bhi Python runtime type checking library hai.

Iska basic pattern:

```python
from beartype import beartype


@beartype
def add(a: int, b: int) -> int:
    return a + b
```

Then:

```python
add(10, 20)
```

valid.

Lekin:

```python
add("10", 20)
```

runtime type violation generate kar sakta hai.

---

# 10. `@beartype` ka concept

```text
@beartype
    ↓
function
    ↓
runtime type checking
```

Similar pattern:

```text
@typechecked
    ↓
runtime checking
```

versus:

```text
@beartype
    ↓
runtime checking
```

---

# 11. `typeguard` vs `beartype`

Dono ka purpose similar hai:

|                            | `typeguard`    | `beartype`  |
| -------------------------- | -------------- | ----------- |
| Runtime checking           | ✅              | ✅           |
| Type annotations use       | ✅              | ✅           |
| Decorator                  | `@typechecked` | `@beartype` |
| Nested types               | ✅              | ✅           |
| Static checker replacement | ❌              | ❌           |

Important:

> Dono **mypy/pyright ka replacement nahi** hain.

---

# 12. Runtime cost

Static checking:

```text
mypy
↓
development/CI
↓
runtime performance impact ≈ none
```

Runtime checking:

```text
typeguard
beartype
↓
actual program execution
↓
type checks
↓
some runtime overhead
```

Isliye production architecture mein runtime checking selectively use karna important hai.

---

# 13. Ab sabse important: Pydantic

Ab:

```text
pydantic
```

Ye sirf simple runtime type checker nahi hai.

Pydantic ka major focus:

> **Data validation, parsing/coercion, structured models, serialization/deserialization.**

Example:

```python
from pydantic import BaseModel


class Equipment(BaseModel):
    equipment_id: str
    temperature: float
    running: bool
```

Ab:

```python
equipment = Equipment(
    equipment_id="AHU-01",
    temperature=24.5,
    running=True
)
```

Tumhare paas structured validated object hai.

---

# 14. Pydantic ka real power

Suppose API se:

```python
data = {
    "equipment_id": "AHU-01",
    "temperature": "24.5",
    "running": True
}
```

Notice:

```text
temperature = "24.5"
```

string hai.

Model:

```python
from pydantic import BaseModel


class Equipment(BaseModel):
    equipment_id: str
    temperature: float
    running: bool
```

Then:

```python
equipment = Equipment(**data)
```

Pydantic input ko validate/parse kar sakta hai according to its model configuration.

Result:

```python
equipment.temperature
```

structured field ban jata hai.

---

# 15. Pydantic = model

Mental model:

```text
Raw data
   ↓
Pydantic Model
   ↓
Validation / parsing
   ↓
Structured object
```

Example:

```text
JSON
 ↓
dict
 ↓
Equipment(...)
 ↓
validated model
```

---

# 16. Invalid data

Suppose:

```python
data = {
    "equipment_id": "AHU-01",
    "temperature": "abc",
    "running": True
}
```

Model:

```python
class Equipment(BaseModel):
    equipment_id: str
    temperature: float
    running: bool
```

Pydantic kahega:

```text
temperature
    ↓
cannot be parsed/validated as float
```

Aur validation error provide karega.

---

# 17. Missing fields

Suppose:

```python
data = {
    "equipment_id": "AHU-01"
}
```

Lekin model:

```python
class Equipment(BaseModel):
    equipment_id: str
    temperature: float
    running: bool
```

Required fields missing hain.

Pydantic validation error deta hai.

---

# 18. Pydantic aur dataclass

Tumne `dataclass` deeply padha hai.

Compare:

### Dataclass

```python
from dataclasses import dataclass


@dataclass
class Equipment:
    name: str
    temperature: float
```

Ye primarily:

```text
data container
```

hai.

### Pydantic

```python
from pydantic import BaseModel


class Equipment(BaseModel):
    name: str
    temperature: float
```

Ye:

```text
data model
+
validation
+
parsing
+
serialization
```

provide karta hai.

---

# 19. Dataclass vs Pydantic

| Feature               |                   `dataclass` |  Pydantic |
| --------------------- | ----------------------------: | --------: |
| Data container        |                             ✅ |         ✅ |
| Type annotations      |                             ✅ |         ✅ |
| Automatic `__init__`  |                             ✅ |         ✅ |
| Runtime validation    | Basic/no automatic validation |         ✅ |
| Parsing external data |                       Limited |         ✅ |
| JSON workflows        |                  Manual/tools |    Strong |
| API models            |                      Possible | Excellent |

---

# 20. Pydantic + API

Ye real-world mein bohat important hai.

Suppose HVAC API:

```json
{
    "equipment_id": "AHU-01",
    "floor": 34,
    "temperature": 23.7,
    "airflow": 1200.5,
    "running": true
}
```

Model:

```python
from pydantic import BaseModel


class AHUData(BaseModel):
    equipment_id: str
    floor: int
    temperature: float
    airflow: float
    running: bool
```

Then:

```python
ahu = AHUData(**api_data)
```

Ab:

```python
ahu.temperature
ahu.airflow
ahu.running
```

typed structured data ke through access kar sakte ho.

---

# 21. Static + Pydantic combination

Ye professional architecture hai:

```text
             External API
                  │
                  ▼
               JSON/dict
                  │
                  ▼
               Pydantic
                  │
          validation/parsing
                  │
                  ▼
          Typed Python object
                  │
          ┌───────┴────────┐
          ▼                ▼
        mypy             runtime
     / pyright          validation
```

Yahan:

```text
Pydantic
```

runtime data boundary ko protect karta hai.

Aur:

```text
mypy / pyright
```

internal code ke static contracts ko check karte hain.

---

# 22. TypeGuard vs Pydantic

Tumne `TypeGuard` pehle padha hai.

Example:

```python
from typing import TypeGuard


def is_int_list(value: object) -> TypeGuard[list[int]]:
    ...
```

Iska purpose:

```text
static type narrowing
```

Pydantic ka purpose:

```text
actual data validation/modeling
```

So:

```text
TypeGuard
 ↓
"Type checker ko batao ke ye value kis type ki hai"

Pydantic
 ↓
"Actual data ko validate/parse karke model banao"
```

---

# 23. `typeguard` vs `beartype` vs `pydantic`

Ab core comparison:

| Tool        | Main purpose                               |
| ----------- | ------------------------------------------ |
| `typeguard` | Runtime type checking                      |
| `beartype`  | Runtime type checking                      |
| `pydantic`  | Runtime data validation + parsing + models |

Mental shortcut:

```text
typeguard
    ↓
"Function call ka type check karo"

beartype
    ↓
"Function call ka type check karo efficiently"

pydantic
    ↓
"External/untrusted data ko validate karke structured model banao"
```

---

# 24. Example — same problem, three approaches

Input:

```python
data = {
    "temperature": "24.5"
}
```

### Typeguard

Typeguard generally function annotations ke runtime contract ko enforce karta hai:

```python
@typechecked
def process(temperature: float):
    ...
```

Agar string directly pass ki:

```python
process("24.5")
```

to runtime type checking issue aa sakta hai.

---

### Beartype

```python
@beartype
def process(temperature: float):
    ...
```

Again runtime contract enforcement.

---

### Pydantic

```python
class Sensor(BaseModel):
    temperature: float
```

Then:

```python
sensor = Sensor(**data)
```

Yahan focus raw data ko model mein convert/validate karna hai.

---

# 25. External boundary concept

Ye concept yaad rakho:

```text
                 TRUST BOUNDARY
                      │
External data ────────┤
                      │
                      ▼
                Validation
                      │
                      ▼
              Internal Python
```

Examples external data:

* REST API
* JSON
* CSV
* database
* user input
* configuration
* message queue

Yahan Pydantic bohat useful ho sakta hai.

---

# 26. Static type hints aur runtime reality

Ye distinction bohat important hai:

```python
temperature: float
```

iska matlab automatically ye nahi:

```text
"Python runtime hamesha float enforce karega."
```

Instead:

```text
type annotation
       ↓
information
       ↓
static checker can use it
```

Runtime validation ke liye:

```text
typeguard
beartype
pydantic
```

jaise tools use ho sakte hain.

---

# 27. Ek complete architecture

Tumhare equipment/HVAC type application ko imagine karo:

```text
Honeywell / API / Database
             │
             ▼
          Raw data
             │
             ▼
         Pydantic
             │
             ▼
      Validated models
             │
             ▼
      Business logic
             │
      ┌──────┴──────┐
      ▼             ▼
    mypy          pyright
      │             │
      └──────┬──────┘
             ▼
       Static safety
```

Optional function-boundary runtime checks:

```text
Business function
       │
       ▼
 typeguard / beartype
```

---

# 28. Ek important warning

Runtime type checking ko har jagah blindly use karna zaroori nahi.

Agar tum:

```python
@typechecked
```

har tiny internal function par laga do, to unnecessary runtime overhead aur complexity aa sakti hai.

Better architecture:

```text
External boundary
       ↓
strong validation

Internal trusted code
       ↓
static typing
```

---

# 29. `typeguard` vs `beartype` kab?

Agar requirement simply:

```text
runtime enforcement of annotations
```

hai, dono relevant options hain.

Selection project ki:

* performance needs
* supported typing features
* debugging experience
* ecosystem
* configuration

par depend karegi.

---

# 30. Pydantic kab?

Pydantic especially useful:

```text
API
↓
JSON
↓
validation
↓
models
```

Examples:

```text
FastAPI
configuration models
API schemas
database/API boundaries
JSON serialization
data validation
```

---

# 31. Lesson 86 ka complete map

```text
                  Runtime Type/Data Validation
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
         typeguard         beartype         pydantic
             │                │                │
       Type checking     Type checking     Data modeling
             │                │                │
             └────────────────┘                │
                      │                         │
                      ▼                         ▼
                 Runtime type             Validation +
                    checks                  parsing
                                                │
                                                ▼
                                         Structured models
```

Aur static side:

```text
mypy
pyright
basedpyright
pyre
pytype
     ↓
STATIC ANALYSIS
```

---

# 32. Sabse important formula

```text
Static typing
    ↓
"What should the type be?"

Runtime type checking
    ↓
"What is the actual type right now?"

Data validation
    ↓
"Is this external data valid, and can I turn it into my model?"
```

### Isliye:

> **`typeguard` aur `beartype` primarily runtime type checking ke tools hain, jabke Pydantic runtime data validation, parsing aur structured models ke liye hai.**

---

## Next: Lesson 87 — `threading`

Ab typing series se hum **Concurrency & Parallelism** mein enter karenge:

```text
threading
   ↓
Thread
   ↓
Lock
   ↓
RLock
   ↓
Semaphore
   ↓
Event
```

Aur sabse pehle hum **Thread kya hai, process se kya difference hai, GIL kya karta hai, aur ek hi Python program mein multiple threads actually kaise kaam karte hain** detail mein dekhenge.
# Lesson 87 — `threading`

## Thread, Lock, RLock, Semaphore, Event

Ab hum **Concurrency & Parallelism** section mein enter ho rahe hain.

Sabse pehle ek fundamental distinction:

```text
Concurrency
    ↓
Multiple tasks ka progress overlap karna

Parallelism
    ↓
Multiple tasks ka literally same time execute hona
```

Python mein `threading` primarily **concurrency** ke liye useful hai, especially **I/O-bound** work ke liye.

---

# 1. Thread kya hota hai?

Simple words mein:

> **Thread ek process ke andar execution ka ek independent path hota hai.**

Example:

```text
Process
│
├── Thread 1
├── Thread 2
└── Thread 3
```

Ek Python process ke andar multiple threads ho sakte hain.

---

# 2. Process vs Thread

### Process

```text
Process A
│
├── Memory
├── Resources
└── Thread(s)
```

### Thread

```text
Process
│
├── Thread 1
├── Thread 2
└── Thread 3
```

Threads same process ke resources/memory ko share karte hain.

Isliye communication easy ho sakti hai, lekin **shared data race conditions** bhi create kar sakta hai.

---

# 3. Real-world example

Suppose tumhare paas HVAC application hai:

```text
Task 1 → AHU data read
Task 2 → VAV data read
Task 3 → Temperature API
Task 4 → Database write
```

Sequential:

```text
AHU
 ↓
VAV
 ↓
API
 ↓
Database
```

Har task doosre ka wait kar raha hai.

Threads:

```text
             Program
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
    AHU        VAV       API
   Thread     Thread     Thread
```

Agar tasks I/O wait kar rahe hain, concurrency useful ho sakti hai.

---

# 4. Basic `threading.Thread`

Python:

```python
import threading


def worker():
    print("Worker running")


thread = threading.Thread(target=worker)

thread.start()
```

Yahan:

```python
threading.Thread(...)
```

Thread object banata hai.

Aur:

```python
thread.start()
```

thread ko start karta hai.

---

# 5. `start()` vs direct function call

Ye bohat important hai.

### Direct call

```python
worker()
```

Matlab current thread hi function execute karega.

### Thread

```python
thread.start()
```

Matlab thread scheduler ko naya thread start karne ke liye kaha gaya.

Concept:

```text
worker()
   ↓
current thread


Thread(target=worker).start()
   ↓
new thread
```

---

# 6. `run()` directly mat confuse karna

Agar:

```python
thread = threading.Thread(target=worker)
thread.start()
```

use karte ho to new thread start hota hai.

Lekin:

```python
thread.run()
```

directly call karne se normally tum thread ko independently start nahi kar rahe; method current execution flow mein call ho sakta hai.

Isliye normal usage:

```python
thread.start()
```

---

# 7. `join()`

Suppose:

```python
import threading


def worker():
    print("Working...")


thread = threading.Thread(target=worker)

thread.start()
thread.join()

print("Finished")
```

`join()` ka matlab:

> **Current thread wait kare jab tak target thread finish na ho jaye.**

Diagram:

```text
Main Thread
    │
    ├── start()
    │
    ▼
Worker Thread ───────► finish
    │
    └──────────────────┐
                       ▼
Main Thread ◄────── join()
                       │
                       ▼
                    continue
```

---

# 8. Multiple threads

```python
import threading


def worker(name):
    print(f"{name} started")


threads = []

for i in range(3):
    t = threading.Thread(
        target=worker,
        args=(f"Thread-{i}",)
    )

    threads.append(t)
    t.start()


for t in threads:
    t.join()
```

Concept:

```text
Main
 │
 ├── Thread-0
 ├── Thread-1
 └── Thread-2
```

Phir:

```python
for t in threads:
    t.join()
```

main thread sabka wait karta hai.

---

# 9. Thread ka `args`

Function:

```python
def worker(name):
    print(name)
```

Thread:

```python
threading.Thread(
    target=worker,
    args=("AHU-01",)
)
```

`args` tuple hona chahiye:

```python
args=("AHU-01",)
```

Comma important hai.

---

# 10. Threading I/O-bound tasks ke liye useful kyun?

Suppose:

```text
API request
   ↓
waiting...
```

CPU actually heavy calculation nahi kar raha.

Thread doosre task par progress kar sakta hai.

```text
Thread 1
API ───── waiting ───────── response

Thread 2
       database ─── response

Thread 3
             file ───── response
```

Yani waiting time overlap ho sakta hai.

---

# 11. CPU-bound aur GIL

Ab important Python concept:

```text
GIL
Global Interpreter Lock
```

CPython mein traditionally ek process ke andar Python bytecode execution ko GIL constrain karta hai.

Isliye CPU-heavy pure-Python work mein:

```text
10 threads
```

zaroori nahi ke:

```text
10 CPU cores par simultaneously Python bytecode execute
```

kar dein.

Isi liye CPU-bound work ke liye `multiprocessing` aksar better approach hoti hai.

---

# 12. I/O-bound vs CPU-bound

### I/O-bound

```text
HTTP request
Database
File
Socket
Network
```

Threading useful ho sakti hai.

### CPU-bound

```text
Huge calculation
Image processing
Complex computation
Scientific computation
```

Threads CPython mein GIL ki wajah se ideal solution nahi hote; processes ya native code/other concurrency approaches consider ki ja sakti hain.

---

# 13. Ab problem — shared data

Suppose:

```python
counter = 0
```

Do threads:

```text
Thread 1 → counter += 1
Thread 2 → counter += 1
```

Dono same variable access kar rahe hain.

Ye:

```text
shared state
```

hai.

Ab race condition ka possibility hota hai.

---

# 14. Race condition kya hai?

Simple:

> **Result execution timing/order par depend kare aur multiple threads shared state ko unsafely access karein to race condition ho sakti hai.**

Concept:

```text
counter = 0

Thread A ── read 0
Thread B ── read 0
Thread A ── write 1
Thread B ── write 1
```

Expected:

```text
2
```

Mila:

```text
1
```

Conceptually ye lost update hai.

---

# 15. `Lock`

Shared resource ko protect karne ke liye:

```python
import threading

lock = threading.Lock()
```

Use:

```python
with lock:
    counter += 1
```

Meaning:

```text
Lock acquire
    ↓
critical section
    ↓
Lock release
```

---

# 16. Critical section

Critical section wo code hai jahan shared resource access ho raha hai.

```python
with lock:
    counter += 1
```

Yahan:

```text
counter += 1
```

protected operation hai.

---

# 17. Complete Lock example

```python
import threading

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

print(counter)
```

Goal:

```text
200000
```

Lock shared update ko synchronize karta hai.

---

# 18. `with lock` kyun?

Instead of:

```python
lock.acquire()

try:
    counter += 1
finally:
    lock.release()
```

Python mein clean form:

```python
with lock:
    counter += 1
```

Ye context manager protocol use karta hai.

Tumhare previous OOP lessons se connection:

```text
with object:
    ...
```

means object context-management behavior provide karta hai.

---

# 19. Lock ka mental model

```text
              Shared Resource
                    │
              ┌─────┴─────┐
              ▼           ▼
          Thread A     Thread B
              │           │
              └─────┬─────┘
                    ▼
                   Lock
                    │
             only one enters
                    │
                    ▼
             Critical section
```

---

# 20. `RLock`

Ab:

```python
threading.RLock()
```

`RLock` = **Reentrant Lock**

Difference:

```text
Lock
    ↓
same thread dobara acquire kare
    ↓
problem/deadlock possibility
```

`RLock`:

```text
same thread
    ↓
multiple times acquire
    ↓
allowed
```

Lekin har acquire ka corresponding release hona chahiye.

---

# 21. `RLock` example

```python
import threading

lock = threading.RLock()


def outer():
    with lock:
        inner()


def inner():
    with lock:
        print("Inside inner")


outer()
```

Normal `Lock` ke sath same thread ke nested acquisition mein deadlock ho sakta hai.

`RLock` isi situation ko handle karta hai.

---

# 22. RLock ka mental model

```text
Thread A
   │
   ▼
acquire RLock
   │
   ▼
outer()
   │
   ▼
inner()
   │
   ▼
acquire RLock again
   │
   ▼
allowed
```

RLock internally ownership/recursion level track karta hai.

---

# 23. `Lock` vs `RLock`

|                        | Lock  | RLock                 |
| ---------------------- | ----- | --------------------- |
| Mutual exclusion       | ✅     | ✅                     |
| Same thread re-acquire | ❌     | ✅                     |
| Nested locking         | Risky | Supported             |
| Simpler                | ✅     | Slightly more complex |

Rule:

> Agar reentrant behavior ki zaroorat nahi, simple `Lock` usually preferable hai.

---

# 24. `Semaphore`

Ab:

```python
threading.Semaphore()
```

Lock:

```text
1 thread
```

Semaphore:

```text
N threads
```

tak resource access allow kar sakta hai.

Example:

```python
semaphore = threading.Semaphore(3)
```

Matlab conceptual:

```text
maximum 3 threads
      ↓
resource access
```

---

# 25. Semaphore ka HVAC example

Suppose external API ek waqt mein maximum 3 requests tolerate karni chahiye.

```python
import threading

semaphore = threading.Semaphore(3)
```

Worker:

```python
def fetch_data():
    with semaphore:
        # API call
        ...
```

Agar 10 threads hain:

```text
10 threads
   │
   ▼
Semaphore(3)
   │
   ├── Thread 1
   ├── Thread 2
   ├── Thread 3
   │
   └── baqi wait
```

Jab ek finish:

```text
Thread 1 leaves
     ↓
Thread 4 enters
```

---

# 26. Lock vs Semaphore

### Lock

```text
capacity = 1
```

### Semaphore(3)

```text
capacity = 3
```

Mental model:

```text
Lock
[ X ]
 1 slot

Semaphore(3)
[ X ][ X ][ X ]
 3 slots
```

---

# 27. `Event`

Ab:

```python
threading.Event()
```

Event ka concept:

> **Ek thread doosre thread ko signal de sakta hai ke koi condition/event ho chuka hai.**

Example:

```python
event = threading.Event()
```

Worker:

```python
event.wait()
```

Wait karega.

Another thread:

```python
event.set()
```

signal dega.

---

# 28. Event example

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

Flow:

```text
Worker
  │
  ▼
event.wait()
  │
  │ blocked/waiting
  │
  │
Main
  │
  ▼
event.set()
  │
  ▼
Worker wakes
```

---

# 29. `Event` ko boolean signal samjho

Conceptually:

```text
Event = False
```

Then:

```python
event.set()
```

means:

```text
Event = True
```

Worker:

```python
event.wait()
```

ka matlab:

> "Jab tak event set nahi hota, wait karo."

---

# 30. Event clear bhi ho sakta hai

```python
event.clear()
```

Conceptually:

```text
set
 ↓
True

clear
 ↓
False
```

Phir:

```python
event.wait()
```

dobara wait karega jab tak event set na ho.

---

# 31. Event ka real-world use

Suppose HVAC system startup:

```text
Controller
   ↓
connect to BMS
   ↓
ready
```

Worker threads:

```text
Thread A → AHU
Thread B → VAV
Thread C → alarms
```

Sab ko ek initialization complete hone ka wait karna hai.

```python
ready = threading.Event()
```

Initialization complete:

```python
ready.set()
```

Workers:

```python
ready.wait()
```

Ab sab continue kar sakte hain.

---

# 32. Lock vs Event

Ye confuse mat karna.

### Lock

```text
"Ek waqt mein kaun resource use karega?"
```

### Event

```text
"Condition/signal kab complete hua?"
```

Example:

```text
Lock
→ shared variable protect

Event
→ notification/synchronization
```

---

# 33. Semaphore vs Event

### Semaphore

```text
Kitne threads simultaneously enter kar sakte hain?
```

### Event

```text
Kab continue karna hai?
```

---

# 34. Chaaron ka master table

| Tool        | Main purpose                                                 |
| ----------- | ------------------------------------------------------------ |
| `Lock`      | One thread at a time / mutual exclusion                      |
| `RLock`     | Same thread multiple times lock acquire kar sakta hai        |
| `Semaphore` | Limited number of threads simultaneously resource use karein |
| `Event`     | Threads ko signal/notification dena                          |

---

# 35. Ek combined example

Imagine:

```text
HVAC API
maximum 3 concurrent requests
```

```python
import threading

api_limit = threading.Semaphore(3)
data_lock = threading.Lock()
ready = threading.Event()

data = []


def worker():
    ready.wait()

    with api_limit:
        result = "AHU data"

    with data_lock:
        data.append(result)
```

Main:

```python
ready.set()
```

Yahan:

```text
Event
 ↓
workers ko start signal

Semaphore
 ↓
maximum 3 API operations

Lock
 ↓
shared data list protect
```

---

# 36. Thread lifecycle

Basic lifecycle:

```text
Created
   ↓
start()
   ↓
Runnable / executing
   ↓
Finished
```

Example:

```python
thread = threading.Thread(target=worker)

# Created

thread.start()

# Running

thread.join()

# Finished
```

---

# 37. Daemon thread

Thread create karte waqt:

```python
thread = threading.Thread(
    target=worker,
    daemon=True
)
```

Daemon thread background-style thread hota hai jo process shutdown behavior mein special treatment rakhta hai.

Typical example:

```text
background monitoring
```

Lekin important work ko daemon thread par blindly depend nahi karna chahiye, kyunki process exit par daemon threads abruptly stop ho sakte hain.

---

# 38. `ThreadPoolExecutor`

Ye technically `concurrent.futures` ka part hai, `threading` module ka direct class nahi, lekin threading ka practical modern pattern hai.

Example:

```python
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    return x * 2


with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(worker, [1, 2, 3, 4]))
```

Mental model:

```text
ThreadPool
   │
   ├── Worker 1
   ├── Worker 2
   ├── Worker 3
   └── Worker 4
```

Ye next concurrency concepts mein useful hoga.

---

# 39. Threading ko OOP se connect karo

Tum OOP bhi deeply padh rahe ho.

`Thread` khud ek object hai:

```python
thread = threading.Thread(...)
```

Uske methods:

```python
thread.start()
thread.join()
```

Synchronization objects bhi objects hain:

```python
lock = threading.Lock()
event = threading.Event()
semaphore = threading.Semaphore(3)
```

Aur:

```python
with lock:
```

context manager protocol ka use karta hai.

Yani:

```text
OOP
 ↓
objects
 ↓
methods/protocols
 ↓
concurrency primitives
```

---

# 40. Sabse important warning — shared mutable state

Threading ka sabse dangerous area:

```text
multiple threads
       ↓
same mutable object
       ↓
race condition
```

Example:

```python
data = []
```

Agar multiple threads isay modify kar rahe hain:

```python
data.append(...)
```

to synchronization design ko carefully consider karna chahiye.

Har operation ko blindly lock karna bhi correct architecture nahi hota; shared-state design minimize karna often better hota hai.

---

# 41. Threading ka complete mental map

```text
                 threading
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Thread      Synchronization
        │               │
        │       ┌───────┼────────────┐
        │       ▼       ▼       ▼    ▼
        │     Lock    RLock  Semaphore Event
        │
        ▼
      start()
        │
        ▼
      join()
```

---

# 42. Ek line mein har concept

### Thread

> **Execution ka independent path within a process.**

### Lock

> **Ek waqt mein ek thread ko critical section access karne dena.**

### RLock

> **Same thread ko lock ko recursively/repeatedly acquire karne dena.**

### Semaphore

> **Limited number of threads ko resource access dena.**

### Event

> **Threads ke darmiyan signal/notification mechanism.**

---

## Lesson 87 ka sabse important point

```text
I/O-bound work
     ↓
threading useful

Shared data
     ↓
Lock / RLock

Limited resource
     ↓
Semaphore

"Ready ho gaya"
     ↓
Event

CPU-heavy Python work
     ↓
threading usually not the first choice
     ↓
multiprocessing / other approaches
```

**Next: Lesson 88 — `threading.Condition`, `Barrier`, `Timer`**. Ismein hum samjhenge ke `Condition` simple `Event` se kaise different hai, `Barrier` multiple threads ko ek point par kaise synchronize karta hai, aur `Timer` delayed/background execution kaise karta hai.
# Lesson 88 — `threading.Condition`, `Barrier`, `Timer`

Lesson 87 mein humne dekha:

```text
Thread
Lock
RLock
Semaphore
Event
```

Ab hum **advanced thread synchronization** par aate hain.

Sabse pehle ek important idea:

```text
Lock      → resource ko protect karo
Event     → signal do
Condition → condition change hone ka wait karo
Barrier   → multiple threads ko ek point par roko
Timer     → kuch delay ke baad function chalao
```

---

# 1. `Condition` kya hai?

`Condition` tab use hoti hai jab thread ko sirf signal ka wait nahi karna, balki **kisi specific condition ke true hone ka wait** karna ho.

Mental model:

```text
Thread
  │
  ▼
Condition check
  │
  ├── False → wait()
  │
  └── True  → continue
```

Example:

```text
Queue mein data available hai?
```

Agar nahi:

```text
worker → wait
```

Jab producer data add kare:

```text
producer → notify
```

Worker wake up hota hai aur condition dobara check karta hai.

---

# 2. Real-world HVAC example

Suppose ek monitoring system hai:

```text
Sensor Thread
      │
      ▼
Temperature data
      │
      ▼
Shared buffer
```

Aur processing thread:

```text
Processor Thread
      │
      ▼
"Data available hai?"
```

Agar data available nahi:

```text
Processor → wait
```

Sensor jab data add kare:

```text
Sensor → notify
```

Processor wake hota hai.

---

# 3. Basic `Condition`

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

Yahan:

```python
condition.wait()
```

ka matlab:

> "Condition satisfy hone tak mujhe wait karwao."

---

# 4. `wait()` kya karta hai?

Important point:

```python
with condition:
    condition.wait()
```

`wait()` current thread ko temporarily block karta hai.

Aur importantly, condition ka associated lock temporarily release hota hai, taake doosra thread shared state modify kar sake.

Conceptually:

```text
Consumer
   │
   ▼
lock acquire
   │
   ▼
condition false
   │
   ▼
wait()
   │
   ├── lock release
   │
   ▼
waiting
```

Producer:

```text
Producer
   │
   ▼
lock acquire
   │
   ▼
data add
   │
   ▼
notify()
```

Phir consumer wake hota hai.

---

# 5. `notify()`

Producer:

```python
condition.notify()
```

ka matlab:

> Waiting threads mein se ek ko wake-up signal do.

Agar multiple waiting threads ko wake karna ho:

```python
condition.notify_all()
```

---

# 6. `notify()` vs `notify_all()`

### `notify()`

```text
Waiting:
Thread A
Thread B
Thread C

notify()
   ↓
one thread wake
```

### `notify_all()`

```text
Waiting:
Thread A
Thread B
Thread C

notify_all()
   ↓
A + B + C wake
```

Lekin wake hone ka matlab ye nahi ke sab simultaneously critical section mein enter kar jayenge. Lock synchronization phir bhi apply hoti hai.

---

# 7. `while` kyun use karte hain?

Ye bohat important hai.

Correct:

```python
with condition:
    while not data:
        condition.wait()

    value = data.pop(0)
```

Sirf:

```python
if not data:
    condition.wait()
```

par depend karna generally unsafe design hai.

Reason:

Thread wake hone ke baad condition ko **dobara verify** karna chahiye.

Mental model:

```text
wake up
   ↓
condition check again
   ↓
still false?
   ↓
wait again
```

Isi liye condition variables ke saath standard pattern:

```python
while not condition:
    condition.wait()
```

---

# 8. Condition aur Event mein difference

Ye dono bohat confuse hote hain.

## Event

```text
"Signal aa gaya?"
```

Example:

```python
ready.wait()
```

## Condition

```text
"Shared state ab required condition mein hai?"
```

Example:

```python
while not data:
    condition.wait()
```

Difference:

```text
Event
   ↓
signal/state flag

Condition
   ↓
predicate + shared state + synchronization
```

---

# 9. Condition ka real use — Producer/Consumer

Ye classic concurrency pattern hai.

```text
Producer
   │
   ▼
   Queue/Buffer
   │
   ▼
Consumer
```

Producer:

```text
data produce
```

Consumer:

```text
data consume
```

Agar buffer empty:

```text
Consumer → wait
```

Agar data aa gaya:

```text
Producer → notify
```

Ye pattern software systems mein bohat common hai.

---

# 10. `Condition` internally Lock ke saath kaam karti hai

Tum explicitly lock de sakte ho:

```python
lock = threading.Lock()
condition = threading.Condition(lock)
```

Ya Python automatically associated lock create kar sakta hai:

```python
condition = threading.Condition()
```

Mental model:

```text
Condition
   │
   └── Lock
        │
        ├── wait()
        ├── notify()
        └── notify_all()
```

---

# 11. `Barrier`

Ab doosra concept:

```python
threading.Barrier
```

Barrier ka matlab:

> **Multiple threads ko ek synchronization point par wait karwana, jab tak required number of threads arrive na ho jayein.**

Example:

```python
barrier = threading.Barrier(3)
```

Matlab:

```text
3 participants
```

required hain.

---

# 12. Barrier ka real-world example

Suppose HVAC software mein 3 initialization tasks hain:

```text
Thread 1 → Load AHU configuration
Thread 2 → Load VAV configuration
Thread 3 → Load alarm configuration
```

Teeno complete hone ke baad hi main processing start karni hai.

```text
AHU config ───────┐
                  │
VAV config ───────┼──► Barrier ───► Continue
                  │
Alarm config ─────┘
```

Yahi Barrier ka perfect use case hai.

---

# 13. Basic Barrier example

```python
import threading
import time


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

Flow:

```text
AHU
 ↓
barrier.wait()

VAV
 ↓
barrier.wait()

Alarm
 ↓
barrier.wait()

       ↓
  All 3 arrived
       ↓
   Continue
```

---

# 14. Barrier ko gate samjho

Imagine ek gate hai:

```text
             GATE
              │
      ┌───────┼───────┐
      │       │       │
     AHU     VAV    Alarm
      │       │       │
      └───────┼───────┘
              │
       all arrived
              ↓
          gate opens
```

Agar sirf 2 threads aaye:

```text
AHU ──► wait
VAV ──► wait
Alarm ──► missing
```

Gate open nahi hoga.

---

# 15. Barrier vs Event

### Event

```text
One thread:
"Ready!"

Many threads:
"Okay, continue."
```

### Barrier

````text
Many threads:
"Main ready hoon."

Sab ready:

```text
"Ab sab continue karo."
````

Mental model:

```text
Event
    1 → many

Barrier
    many → all
```

---

# 16. Barrier vs Condition

### Condition

Dynamic condition:

```text
data available?
buffer full?
state changed?
```

### Barrier

Fixed number of participants:

```text
3 threads must arrive
```

Example:

```text
Condition:
"Temperature data available hai?"

Barrier:
"3 initialization workers complete hue?"
```

---

# 17. Barrier timeout

Barrier mein timeout bhi ho sakta hai:

```python
barrier = threading.Barrier(
    3,
    timeout=10
)
```

Agar required participants time par nahi aaye to barrier break/fail ho sakta hai.

Ye distributed-style synchronization mein useful ho sakta hai, lekin exception handling carefully design karni chahiye.

---

# 18. `Timer`

Ab third concept:

```python
threading.Timer
```

Timer ka matlab:

> **Specified delay ke baad function ko execute karna.**

Example:

```python
import threading


def hello():
    print("Hello")


timer = threading.Timer(5, hello)

timer.start()
```

Meaning:

```text
5 seconds
    ↓
hello()
```

---

# 19. Timer ko delayed thread samjho

Conceptually:

```text
Timer
  │
  ▼
wait 5 seconds
  │
  ▼
execute function
```

Ye synchronous:

```python
time.sleep(5)
hello()
```

se conceptually different hai.

---

# 20. `sleep()` vs `Timer`

### `sleep()`

```python
time.sleep(5)
hello()
```

Current thread 5 seconds wait karega.

### `Timer`

```python
timer = threading.Timer(5, hello)
timer.start()
```

Timer background execution mechanism provide karta hai.

Example:

```text
Main Thread
   │
   ├── continue working
   │
   ├── continue working
   │
   └── Timer fires → hello()
```

---

# 21. Timer ko cancel karna

Timer start karne ke baad:

```python
timer.cancel()
```

use kar sakte ho.

Example:

```python
timer = threading.Timer(10, hello)

timer.start()

timer.cancel()
```

Agar timer abhi fire nahi hua to cancellation usko prevent kar sakti hai.

---

# 22. HVAC example — delayed action

Suppose alarm trigger hone ke baad 10 seconds delay se action lena hai:

```python
def delayed_action():
    print("Checking AHU again")


timer = threading.Timer(
    10,
    delayed_action
)

timer.start()
```

Flow:

```text
Alarm
  ↓
Timer start
  ↓
10 sec
  ↓
Check AHU
```

---

# 23. Timer periodic scheduler nahi hai

Important:

```python
Timer(10, function)
```

ka matlab:

```text
10 seconds baad one execution
```

Ye automatically:

```text
10 sec
10 sec
10 sec
10 sec
...
```

repeat nahi karta.

Periodic scheduling ke liye different design chahiye.

---

# 24. Teenon ka comparison

| Tool        | Main purpose                                     |
| ----------- | ------------------------------------------------ |
| `Condition` | Shared state ki condition ka wait                |
| `Barrier`   | Fixed number of threads ka synchronization point |
| `Timer`     | Delay ke baad function execute karna             |

---

# 25. Sab synchronization tools ka complete map

Ab Lesson 87 + 88 ko combine karo:

```text
threading
│
├── Thread
│
├── Lock
│   └── one-at-a-time protection
│
├── RLock
│   └── reentrant locking
│
├── Semaphore
│   └── limited concurrency
│
├── Event
│   └── signal
│
├── Condition
│   └── condition-based waiting
│
├── Barrier
│   └── all participants synchronize
│
└── Timer
    └── delayed execution
```

---

# 26. Real-world architecture

Suppose tumhara BMS/HVAC monitoring program hai:

```text
                  Main Program
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      AHU           VAV            Alarm
     Thread         Thread          Thread
        │              │              │
        └──────────────┼──────────────┘
                       │
                  Shared Data
                       │
                    Lock
```

API limit:

```text
Semaphore(3)
```

System ready:

```text
Event
```

Data available:

```text
Condition
```

All initialization complete:

```text
Barrier
```

Delayed check:

```text
Timer
```

Ab tum actual concurrency architecture ko samajhna start kar rahe ho.

---

# 27. Sabse important conceptual difference

Isko yaad kar lo:

```text
Lock
"Kaun andar ja sakta hai?"

Semaphore
"Ek waqt mein kitne andar ja sakte hain?"

Event
"Kya signal aa gaya?"

Condition
"Kya required state ab true hai?"

Barrier
"Kya sab participants ready hain?"

Timer
"Kitni der baad function chalana hai?"
```

---

## Lesson 88 ka final mental model

```text
                    THREADING
                       │
        ┌──────────────┼───────────────┐
        │              │               │
     Protect         Wait           Coordinate
        │              │               │
     Lock          Condition        Barrier
     RLock         Event
     Semaphore
                                      │
                                   Delayed
                                      │
                                    Timer
```

**Next Lesson 89 — `queue`: `Queue`, `LifoQueue`, `PriorityQueue`**. Yeh particularly important hai kyun ke `queue` shared data ko threads ke darmiyan safely pass karne ka standard pattern deta hai, aur Producer–Consumer architecture ko properly implement karna isi mein aata hai.
# Lesson 89 — `queue`

## `Queue`, `LifoQueue`, `PriorityQueue`

Ab hum threading ka ek **bohat important practical concept** par aa gaye hain.

Lesson 87–88 mein humne seekha:

```text
Thread
Lock
RLock
Semaphore
Event
Condition
Barrier
Timer
```

Ab sawal:

> Agar multiple threads ko **data safely ek doosre ko dena ho**, to kya karein?

Yahan `queue` ka role aata hai.

---

# 1. Queue kya hoti hai?

Simple definition:

> **Queue ek thread-safe data structure hai jahan ek thread data put karta hai aur doosra thread data receive karta hai.**

Basic model:

```text
Producer
    │
    ▼
┌───────────────┐
│     Queue     │
└───────────────┘
    │
    ▼
Consumer
```

Example:

```text
Sensor Thread
     │
     │ temperature data
     ▼
   Queue
     │
     │
     ▼
Processing Thread
```

---

# 2. Queue ki sabse important property

Python ki `queue` module ki queues **thread-safe** hoti hain.

Matlab multiple threads safely:

```python
queue.put(...)
```

aur:

```python
queue.get()
```

kar sakte hain.

Tumhe basic producer-consumer communication ke liye manually har access par `Lock` lagane ki zaroorat nahi hoti.

---

# 3. Import

```python
import queue
```

Basic queue:

```python
q = queue.Queue()
```

---

# 4. `put()`

Queue mein data add:

```python
q.put("AHU-01")
```

Queue:

```text
┌────────────┐
│ AHU-01     │
└────────────┘
```

Aur:

```python
q.put("AHU-02")
```

Ab:

```text
┌────────────┐
│ AHU-01     │ ← first
├────────────┤
│ AHU-02     │ ← second
└────────────┘
```

---

# 5. `get()`

Queue se item nikalna:

```python
item = q.get()
```

Agar queue:

```text
AHU-01
AHU-02
AHU-03
```

hai to:

```python
q.get()
```

return karega:

```text
AHU-01
```

Phir:

```python
q.get()
```

return karega:

```text
AHU-02
```

---

# 6. Ye FIFO hai

Default `Queue`:

> **FIFO = First In, First Out**

```text
put("A")
put("B")
put("C")
```

Queue:

```text
A → B → C
```

Get:

```text
get() → A
get() → B
get() → C
```

Real-world example:

```text
Customer 1
Customer 2
Customer 3
```

Jo pehle aya, normally pehle serve hoga.

---

# 7. Simple example

```python
import queue

q = queue.Queue()

q.put("AHU-01")
q.put("AHU-02")
q.put("AHU-03")

print(q.get())
print(q.get())
print(q.get())
```

Output:

```text
AHU-01
AHU-02
AHU-03
```

---

# 8. Queue aur list mein difference

Tum keh sakte ho:

> "Ye kaam list se bhi ho sakta hai."

Technically list data store kar sakti hai, lekin multi-threaded producer-consumer communication ke liye `Queue` specifically designed hai.

### List

```python
data = []
```

Tumhe synchronization ka design khud manage karna pad sakta hai.

### Queue

```python
q = queue.Queue()
```

Thread-safe queue operations already provide karti hai.

Mental model:

```text
list
 ↓
general-purpose container

Queue
 ↓
thread communication / producer-consumer
```

---

# 9. Producer–Consumer pattern

Ye `queue` ka **sabse important use case** hai.

```text
Producer
   │
   │ put()
   ▼
┌─────────┐
│  Queue  │
└─────────┘
   │
   │ get()
   ▼
Consumer
```

Example HVAC:

```text
BMS reader
    │
    ▼
Queue
    │
    ▼
Data processor
    │
    ▼
Database
```

---

# 10. Producer

Producer data generate karta hai:

```python
def producer(q):
    for i in range(5):
        q.put(f"Sensor-{i}")
```

Consumer:

```python
def consumer(q):
    for _ in range(5):
        item = q.get()
        print("Processing:", item)
```

---

# 11. Threads ke saath complete example

```python
import queue
import threading
import time


q = queue.Queue()


def producer():
    for i in range(5):
        item = f"Temperature-{i}"
        q.put(item)
        print("Produced:", item)
        time.sleep(0.5)


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

Flow:

```text
Producer
   │
   ├── put()
   ├── put()
   ├── put()
   ▼
 Queue
   │
   ├── get()
   ├── get()
   └── get()
   ▼
Consumer
```

---

# 12. `task_done()`

Ab important method:

```python
q.task_done()
```

Iska matlab:

> Queue se jo item `get()` kiya tha, us item ki processing complete ho gayi.

Example:

```python
item = q.get()

try:
    process(item)
finally:
    q.task_done()
```

Ye particularly important hai jab:

```python
q.join()
```

use karte ho.

---

# 13. `queue.join()`

Suppose:

```python
q.put("A")
q.put("B")
q.put("C")
```

Aur consumer process kar raha hai.

Main thread:

```python
q.join()
```

ka wait karega jab tak queue ke saare queued tasks ke corresponding:

```python
task_done()
```

calls nahi ho jate.

Flow:

```text
put A
put B
put C
   │
   ▼
Queue
   │
   ▼
Consumer
   │
   ├── get A → task_done()
   ├── get B → task_done()
   └── get C → task_done()
                 │
                 ▼
              join()
              returns
```

---

# 14. `join()` vs `task_done()`

Ye distinction yaad rakho:

```text
get()
 ↓
item mila

task_done()
 ↓
item ki processing complete

join()
 ↓
sab queued tasks complete hone ka wait
```

---

# 15. Queue empty ho to `get()` kya karega?

Normally:

```python
q.get()
```

agar queue empty hai to consumer **wait/block** karega.

Example:

```text
Queue:
empty

Consumer:
get()
  ↓
waiting...
```

Jab producer:

```python
q.put("AHU-01")
```

karega:

```text
Producer
   ↓
put()
   ↓
Queue
   ↓
Consumer wakes
```

Ye producer-consumer pattern ka powerful feature hai.

---

# 16. `get_nowait()`

Agar tum wait nahi karna chahte:

```python
q.get_nowait()
```

Agar queue empty ho:

```python
queue.Empty
```

exception aa sakti hai.

Example:

```python
try:
    item = q.get_nowait()
except queue.Empty:
    print("Queue empty")
```

---

# 17. `put_nowait()`

Similarly:

```python
q.put_nowait(item)
```

blocking ke baghair put karne ki koshish karta hai.

Bounded queue full ho to:

```python
queue.Full
```

exception aa sakti hai.

---

# 18. Queue ka maximum size

Tum queue ko bounded bana sakte ho:

```python
q = queue.Queue(maxsize=3)
```

Matlab:

```text
Maximum 3 items
```

Queue:

```text
[A][B][C]
```

Agar full hai aur producer:

```python
q.put("D")
```

karta hai, normal blocking behavior mein producer wait karega jab tak space available na ho.

---

# 19. Bounded Queue kyun useful hai?

Suppose sensor bohat fast data produce kar raha hai:

```text
Producer
1000 items/sec
```

Consumer:

```text
100 items/sec
```

Agar unlimited queue ho:

```text
Queue
100
1000
5000
10000
...
```

Memory pressure badh sakta hai.

Bounded queue:

```python
queue.Queue(maxsize=100)
```

backpressure create kar sakti hai.

---

# 20. Backpressure kya hai?

Simple:

> Producer ko slow/downstream capacity ke mutabiq wait karwana.

```text
Fast Producer
     │
     ▼
 Queue(maxsize=3)
     │
     ▼
Slow Consumer
```

Queue full:

```text
Producer
   ↓
WAIT
```

Consumer item remove karta hai:

```text
Queue space available
   ↓
Producer continue
```

Ye distributed systems aur concurrent systems mein important concept hai.

---

# 21. `LifoQueue`

Ab doosri queue:

```python
q = queue.LifoQueue()
```

LIFO:

> **Last In, First Out**

Example:

```python
q.put("A")
q.put("B")
q.put("C")
```

Order:

```text
C
B
A
```

Kyuki last item pehle niklega.

---

# 22. LifoQueue ka real-world mental model

Stack jaisa:

```text
   C ← top
   B
   A
```

`get()`:

```text
C
```

Phir:

```text
B
```

Phir:

```text
A
```

---

# 23. Queue vs LifoQueue

```text
Queue
FIFO
A → B → C

LifoQueue
LIFO
C → B → A
```

Use case:

### FIFO

Normal task processing:

```text
Request 1
Request 2
Request 3
```

### LIFO

Latest task ko priority deni ho:

```text
old state
new state
latest state
```

---

# 24. `PriorityQueue`

Ab interesting one:

```python
q = queue.PriorityQueue()
```

Ismein items priority ke according nikalte hain.

Example:

```python
q.put((3, "Normal"))
q.put((1, "Critical"))
q.put((2, "Warning"))
```

Get:

```python
print(q.get())
print(q.get())
print(q.get())
```

Result conceptually:

```text
(1, "Critical")
(2, "Warning")
(3, "Normal")
```

Smaller number = higher priority in this basic pattern.

---

# 25. HVAC alarm example

Suppose:

```text
Priority 1 → Critical
Priority 2 → Warning
Priority 3 → Information
```

Queue:

```python
q = queue.PriorityQueue()

q.put((3, "Filter reminder"))
q.put((1, "AHU fault"))
q.put((2, "High temperature"))
```

Consumer:

```python
priority, message = q.get()
```

Sabse pehle:

```text
1 → AHU fault
```

process hoga.

---

# 26. PriorityQueue ka important rule

Agar tuple:

```python
(priority, data)
```

hai, Python priority ke basis par ordering karega.

Example:

```python
(1, "Critical")
(2, "Warning")
(3, "Info")
```

Lekin agar same priority ho:

```python
(1, object_a)
(1, object_b)
```

to second element ki comparison problematic ho sakti hai agar objects comparable nahi hain.

Isliye robust design mein explicit tie-breaker use karna useful hota hai.

Example:

```python
import itertools
import queue

counter = itertools.count()

q = queue.PriorityQueue()

q.put((1, next(counter), "Critical A"))
q.put((1, next(counter), "Critical B"))
```

Ab ordering:

```text
priority
   ↓
sequence number
   ↓
data
```

---

# 27. Teeno queues ka comparison

| Queue           | Order    | Typical use          |
| --------------- | -------- | -------------------- |
| `Queue`         | FIFO     | Normal tasks         |
| `LifoQueue`     | LIFO     | Latest task first    |
| `PriorityQueue` | Priority | Important task first |

Mental model:

```text
Queue
A B C
↓
A B C


LifoQueue
A B C
↓
C B A


PriorityQueue
3 1 2
↓
1 2 3
```

---

# 28. Queue vs Condition

Ye bhi important hai.

Tum manually:

```text
Lock
+
Condition
+
list
```

use karke producer-consumer bana sakte ho.

Lekin:

```python
queue.Queue()
```

already thread-safe producer-consumer abstraction provide karti hai.

So:

```text
Manual approach
    ↓
Lock + Condition + list

Higher-level abstraction
    ↓
queue.Queue
```

Isliye normal producer-consumer use case mein Queue simpler hai.

---

# 29. Queue ka OOP connection

Tumne pehle Python protocols aur OOP study ki hai.

`Queue` ek class ka object hai:

```python
q = queue.Queue()
```

Aur methods:

```python
q.put()
q.get()
q.task_done()
q.join()
```

Yani:

```text
Class
 ↓
Object
 ↓
Methods
 ↓
Thread-safe abstraction
```

Tumhe internal locking manually manage nahi karni padti.

---

# 30. Multiple producers, multiple consumers

Queue ka real power yahan hai:

```text
Producer 1 ──┐
Producer 2 ──┼──► Queue ──┬──► Consumer 1
Producer 3 ──┘            ├──► Consumer 2
                           └──► Consumer 3
```

Example:

```text
3 sensor threads
      ↓
    Queue
      ↓
3 processing threads
```

Ye scalable architecture ka basic pattern hai.

---

# 31. Complete practical architecture

Suppose:

```text
AHU reader
VAV reader
Chiller reader
```

data generate karte hain.

```text
AHU Thread ──────┐
VAV Thread ──────┼──► Queue
Chiller Thread ──┘       │
                         ▼
                  Processing Thread
                         │
                         ▼
                     Database
```

Code skeleton:

```python
import queue
import threading

data_queue = queue.Queue()


def reader(name):
    for i in range(10):
        data_queue.put((name, i))


def processor():
    for _ in range(30):
        equipment, value = data_queue.get()

        try:
            print(
                f"Processing {equipment}: {value}"
            )
        finally:
            data_queue.task_done()
```

Ye architecture real applications mein bohat common hai.

---

# 32. Queue ka golden pattern

Producer:

```python
q.put(data)
```

Consumer:

```python
data = q.get()

try:
    process(data)
finally:
    q.task_done()
```

Main:

```python
q.join()
```

Mental model:

```text
PUT
 ↓
GET
 ↓
PROCESS
 ↓
TASK_DONE
 ↓
JOIN
```

---

# 33. Queue aur shared mutable state

Lesson 87 mein humne kaha tha:

```text
shared mutable state
      ↓
race condition
```

Queue ek important alternative provide karti hai:

```text
Thread A
   ↓
queue.put(data)
   ↓
Queue
   ↓
queue.get()
   ↓
Thread B
```

Yani threads direct same list/dict ko modify karne ke bajaye messages/tasks exchange kar sakte hain.

Is architecture ko broadly:

> **message passing**

kehte hain.

---

# 34. Message passing

Instead of:

```text
Thread A
   ↓
shared object
   ↑
Thread B
```

better architecture ho sakti hai:

```text
Thread A
   ↓
message
   ↓
Queue
   ↓
Thread B
```

Ye concurrency design ko simpler aur safer bana sakta hai.

---

# 35. `queue` ka complete mental map

```text
                    queue
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
        Queue     LifoQueue   PriorityQueue
          │           │            │
         FIFO        LIFO       Priority
          │           │            │
          ▼           ▼            ▼
      A → B → C    C → B → A    1 → 2 → 3
```

---

# 36. Lesson 87–89 ko combine karo

Ab tumhare paas:

```text
Thread
   │
   ├── Lock
   ├── RLock
   ├── Semaphore
   ├── Event
   ├── Condition
   ├── Barrier
   └── Timer

Communication
   │
   └── Queue
       ├── Queue
       ├── LifoQueue
       └── PriorityQueue
```

---

## Sabse important distinction

```text
Lock
→ shared resource protect

Condition
→ condition ka wait

Event
→ signal

Barrier
→ sab threads ka synchronization point

Semaphore
→ limited concurrent access

Timer
→ delayed execution

Queue
→ thread-safe data/task passing
```

### Aur Queue ke andar:

```text
Queue
→ FIFO

LifoQueue
→ LIFO

PriorityQueue
→ priority order
```

**Next Lesson 90 — `multiprocessing`: Process, `Process`, `Pool`, `Queue`, `Pipe`**. Wahan hum dekhenge ke `threading` aur `multiprocessing` mein fundamental difference kya hai, GIL CPU-bound tasks ko kaise affect karta hai, aur processes ke darmiyan data kaise communicate hota hai.
# Lesson 90 — `multiprocessing`

## Process, `Process`, `Pool`, `Queue`, `Pipe`

Ab hum **Threading ke baad Multiprocessing** par aa gaye hain.

Ye distinction bohat important hai:

```text
threading
   ↓
same process ke andar multiple threads

multiprocessing
   ↓
multiple processes
```

Aur sabse important reason:

```text
CPU-bound Python work
       ↓
multiprocessing useful
```

---

# 1. Process kya hota hai?

Process ek **independent running program instance** hota hai.

Example:

```text
Operating System
│
├── Process A
│    ├── Thread
│    └── Thread
│
├── Process B
│    └── Thread
│
└── Process C
     └── Thread
```

Har process ka apna memory space hota hai.

---

# 2. Thread vs Process

### Thread

```text
Process
│
├── Thread A
├── Thread B
└── Thread C
```

Threads same process ki memory share karte hain.

### Process

```text
Process A          Process B
│                  │
Memory A           Memory B
```

Memory normally isolated hoti hai.

---

# 3. Sabse important difference

```text
Thread
→ shared memory

Process
→ separate memory
```

Iska faida:

Processes ek doosre ki memory ko accidentally directly modify nahi karte.

Lekin communication thodi zyada explicit hoti hai.

---

# 4. CPU-bound problem

Suppose:

```python
def calculate():
    for i in range(10_000_000):
        ...
```

Ye CPU-bound task hai.

Agar CPython mein multiple threads use karo:

```text
Thread 1 ─┐
Thread 2 ─┼── GIL constraint
Thread 3 ─┘
```

pure Python bytecode CPU work ko threads generally true multi-core parallelism nahi dete.

Processes:

```text
Process 1 → CPU Core 1
Process 2 → CPU Core 2
Process 3 → CPU Core 3
```

system resources aur workload ke mutabiq actual parallel execution possible hoti hai.

---

# 5. `multiprocessing` import

```python
import multiprocessing
```

Basic process:

```python
process = multiprocessing.Process(
    target=worker
)
```

Start:

```python
process.start()
```

Wait:

```python
process.join()
```

Bilkul threading ke pattern jaisa:

```text
Thread:
start()
join()

Process:
start()
join()
```

---

# 6. Basic Process example

```python
import multiprocessing


def worker():
    print("Worker process running")


if __name__ == "__main__":
    process = multiprocessing.Process(
        target=worker
    )

    process.start()
    process.join()

    print("Finished")
```

---

# 7. `if __name__ == "__main__":`

Windows par ye **especially important** hai.

```python
if __name__ == "__main__":
    ...
```

Multiprocessing process creation ke saath import/startup behavior ki wajah se main code ko guard karna zaroori hota hai.

Tum Windows use karte ho, isliye is pattern ko strongly yaad rakho.

---

# 8. Process ko arguments dena

```python
import multiprocessing


def worker(name):
    print(f"Processing {name}")


if __name__ == "__main__":
    p = multiprocessing.Process(
        target=worker,
        args=("AHU-01",)
    )

    p.start()
    p.join()
```

Same concept:

```python
args=("AHU-01",)
```

---

# 9. Multiple processes

```python
import multiprocessing


def worker(number):
    print(f"Worker {number}")


if __name__ == "__main__":
    processes = []

    for i in range(4):
        p = multiprocessing.Process(
            target=worker,
            args=(i,)
        )

        processes.append(p)
        p.start()

    for p in processes:
        p.join()
```

Architecture:

```text
Main Process
     │
     ├── Process 1
     ├── Process 2
     ├── Process 3
     └── Process 4
```

---

# 10. Process ki memory separate hai

Ye bohat important example hai:

```python
import multiprocessing

counter = 0


def worker():
    global counter
    counter += 1
    print(counter)


if __name__ == "__main__":
    p = multiprocessing.Process(
        target=worker
    )

    p.start()
    p.join()

    print(counter)
```

Tum expect kar sakte ho:

```text
1
1
```

Child process ka:

```python
counter += 1
```

main process ke `counter` ko normally modify nahi karta.

Kyun?

```text
Main Process
counter = 0

       separate memory

Child Process
counter = 0
```

---

# 11. Threading mein difference

Threading:

```text
Same process
     │
counter
     ▲
     │
Thread A
Thread B
```

Processes:

```text
Process A          Process B

counter = 0        counter = 0
```

Separate memory.

---

# 12. Isolated memory ka faida

Agar ek process:

```text
crash
```

karta hai to doosre process ki memory directly corrupt karne ka risk shared-memory threading ke muqable mein kam hota hai.

Lekin process failure handling phir bhi important hai.

---

# 13. `multiprocessing.Pool`

Agar tumhare paas bohat saare similar CPU tasks hain, manually:

```text
Process 1
Process 2
Process 3
...
```

create karna cumbersome ho sakta hai.

Isliye:

```python
multiprocessing.Pool
```

use kar sakte ho.

---

# 14. Pool ka concept

Pool:

```text
Main Process
     │
     ▼
  Process Pool
 ┌────┬────┬────┬────┐
 │ P1 │ P2 │ P3 │ P4 │
 └────┴────┴────┴────┘
```

Tasks pool ke workers ko distribute hote hain.

---

# 15. Basic Pool example

```python
import multiprocessing


def square(x):
    return x * x


if __name__ == "__main__":
    with multiprocessing.Pool(4) as pool:
        results = pool.map(
            square,
            [1, 2, 3, 4, 5]
        )

    print(results)
```

Result:

```text
[1, 4, 9, 16, 25]
```

---

# 16. `Pool.map()`

Concept:

```python
pool.map(function, iterable)
```

Example:

```python
pool.map(square, [1, 2, 3, 4])
```

Conceptually:

```text
1 → square → 1
2 → square → 4
3 → square → 9
4 → square → 16
```

Pool workers available resources ke mutabiq tasks execute karte hain.

---

# 17. Pool ka real-world example

Suppose tumhare paas:

```text
1000 equipment records
```

Aur har record par heavy CPU calculation karni hai:

```text
Equipment 1
Equipment 2
...
Equipment 1000
```

Pool:

```text
             1000 tasks
                 │
                 ▼
            Process Pool
       ┌────┬────┬────┬────┐
       │ P1 │ P2 │ P3 │ P4 │
       └────┴────┴────┴────┘
```

CPU-bound work mein useful architecture ho sakti hai.

---

# 18. Thread Pool vs Process Pool

Tumne Lesson 89 mein indirectly `ThreadPoolExecutor` dekha.

Concept:

```text
ThreadPool
→ I/O-bound workloads often useful

ProcessPool
→ CPU-bound workloads often useful
```

Python ka:

```python
from concurrent.futures import ProcessPoolExecutor
```

bhi isi pattern ka higher-level API hai.

---

# 19. Multiprocessing `Queue`

Processes ko data exchange karna ho to:

```python
multiprocessing.Queue()
```

use kar sakte ho.

Example:

```python
import multiprocessing


def worker(q):
    q.put("AHU-01")


if __name__ == "__main__":
    q = multiprocessing.Queue()

    p = multiprocessing.Process(
        target=worker,
        args=(q,)
    )

    p.start()

    print(q.get())

    p.join()
```

Output:

```text
AHU-01
```

---

# 20. Multiprocessing Queue vs threading Queue

Ye distinction:

```text
queue.Queue
    ↓
threads ke liye

multiprocessing.Queue
    ↓
processes ke darmiyan
```

Dono ka concept similar hai:

```text
Producer
   ↓
Queue
   ↓
Consumer
```

Lekin underlying communication mechanism different hai.

---

# 21. Process communication

Processes ki memory separate hoti hai:

```text
Process A
Memory A

Process B
Memory B
```

To data exchange ke liye communication mechanism chahiye.

Common options:

```text
Queue
Pipe
Manager
shared memory
```

Ab hum `Queue` samajh chuke hain.

Ab `Pipe`.

---

# 22. `Pipe`

`multiprocessing.Pipe()` do endpoints create karta hai.

```python
parent_conn, child_conn = multiprocessing.Pipe()
```

Mental model:

```text
Process A
   │
parent_conn
   │
   ║
   ║ Pipe
   ║
   │
child_conn
   │
Process B
```

---

# 23. Basic Pipe example

```python
import multiprocessing


def worker(conn):
    conn.send("Hello from child")
    conn.close()


if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(
        target=worker,
        args=(child_conn,)
    )

    p.start()

    message = parent_conn.recv()

    print(message)

    p.join()
```

Result:

```text
Hello from child
```

---

# 24. `send()` and `recv()`

Pipe endpoint par:

```python
conn.send(data)
```

data bhejo.

Aur:

```python
conn.recv()
```

data receive karo.

Mental model:

```text
Process A
send()
   │
   ▼
 ===== Pipe =====
   │
   ▼
recv()
Process B
```

---

# 25. Pipe bidirectional bhi ho sakti hai

Default:

```python
multiprocessing.Pipe()
```

duplex communication provide karti hai.

Yani dono sides send/receive kar sakti hain.

```text
Process A
  ↕
Pipe
  ↕
Process B
```

One-way communication bhi explicitly create ki ja sakti hai:

```python
multiprocessing.Pipe(duplex=False)
```

---

# 26. Queue vs Pipe

### Queue

```text
Multiple producers
       ↓
     Queue
       ↓
Multiple consumers
```

Task/message distribution ke liye useful.

### Pipe

```text
Process A
   ↕
Process B
```

Direct connection ke liye useful.

---

# 27. Simple comparison

| Feature                   | Queue       | Pipe            |
| ------------------------- | ----------- | --------------- |
| Multiple producers        | Good        | Not primary use |
| Multiple consumers        | Good        | Not primary use |
| Direct process-to-process | Less direct | Excellent       |
| Producer-consumer         | Excellent   | Possible        |
| Task distribution         | Excellent   | Less suitable   |

---

# 28. Multiprocessing aur Queue ka architecture

Suppose:

```text
Main Process
     │
     ▼
Task Queue
     │
 ┌───┼────┐
 ▼   ▼    ▼
P1  P2    P3
 │   │     │
 └───┼─────┘
     ▼
 Results
```

Ye CPU-heavy task processing architecture ho sakti hai.

---

# 29. `Pool` + CPU-bound calculation

Example conceptual:

```python
import multiprocessing


def calculate(x):
    return x ** 2


if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        results = pool.map(
            calculate,
            range(10)
        )

    print(results)
```

Pool worker processes available CPUs/resources ke mutabiq tasks execute karte hain.

---

# 30. Threading vs Multiprocessing — master comparison

|                   | Threading                                     | Multiprocessing            |
| ----------------- | --------------------------------------------- | -------------------------- |
| Unit              | Thread                                        | Process                    |
| Memory            | Shared                                        | Separate                   |
| Communication     | Relatively easy                               | Explicit IPC               |
| CPU-bound CPython | Usually not ideal for pure Python parallelism | Good candidate             |
| I/O-bound         | Excellent use case                            | Possible but often heavier |
| Startup overhead  | Lower                                         | Higher                     |
| Isolation         | Lower                                         | Higher                     |
| Shared state      | Easy but dangerous                            | More isolated              |
| Synchronization   | Lock, Event, Condition                        | Process-safe equivalents   |

---

# 31. GIL ka final mental model

Important:

```text
GIL ≠ Python mein parallelism impossible
```

Correct concept:

```text
CPython
   │
   └── GIL limits simultaneous execution
       of Python bytecode within one process
```

Isliye:

```text
CPU-bound pure Python
        ↓
multiple processes
        ↓
multiple CPU cores possible
```

While:

```text
I/O-bound
        ↓
threads often efficient
```

Modern Python mein kuch specialized exceptions aur newer interpreter configurations bhi exist karte hain, lekin standard CPython threading model samajhne ke liye ye basic rule strong starting point hai.

---

# 32. `Process` vs `Pool`

### `Process`

Jab tum specific process control karna chahte ho:

```python
Process(target=worker)
```

### `Pool`

Jab tumhare paas:

```text
many similar tasks
```

hon:

```python
Pool.map(...)
```

Mental model:

```text
Process
→ "Mujhe ye specific worker chahiye."

Pool
→ "Mere paas tasks ka batch hai; workers manage karo."
```

---

# 33. `Queue` vs `Pipe`

```text
Queue
→ task/message distribution

Pipe
→ direct communication channel
```

---

# 34. Process ka lifecycle

```text
Created
   │
   ▼
start()
   │
   ▼
Running
   │
   ▼
Finished
   │
   ▼
join()
```

Process object par useful properties/methods:

```python
p.start()
p.join()
p.is_alive()
p.terminate()
p.kill()
```

---

# 35. `is_alive()`

Check:

```python
if p.is_alive():
    print("Process still running")
```

Mental model:

```text
Process
   │
   ├── alive → True
   └── finished → False
```

---

# 36. `terminate()`

Parent process child process ko terminate kar sakta hai:

```python
p.terminate()
```

Lekin ye graceful application-level shutdown ka substitute nahi samajhna chahiye.

Agar process resources/files/database transactions use kar raha ho, cleanup design important hai.

---

# 37. `daemon` process

Process ko daemon bana sakte ho:

```python
p = multiprocessing.Process(
    target=worker,
    daemon=True
)
```

Concept threading ke daemon thread jaisa hai.

Lekin production architecture mein important work ke liye explicit lifecycle/shutdown management better hota hai.

---

# 38. OOP connection

Tumne OOP mein objects/classes padhe hain.

Yahan:

```python
p = multiprocessing.Process(...)
```

ek object hai.

Methods:

```python
p.start()
p.join()
p.is_alive()
```

Similarly:

```python
pool = multiprocessing.Pool()
```

ek pool object hai.

Aur:

```python
q = multiprocessing.Queue()
```

queue object hai.

Yani multiprocessing bhi Python ke normal OOP object model ko use karti hai.

---

# 39. Full architecture — HVAC example

Suppose tum heavy analytics kar rahe ho:

```text
BMS data
   │
   ▼
Main Process
   │
   ▼
Task Queue
   │
   ├───────────────┐
   ▼               ▼
Process 1       Process 2
AHU analytics   VAV analytics
   │               │
   └───────┬───────┘
           ▼
       Result Queue
           │
           ▼
       Main Process
```

Agar analytics CPU-heavy hai to multiprocessing architecture reasonable ho sakti hai.

---

# 40. Threading + Multiprocessing ek saath bhi ho sakte hain

Real applications mein:

```text
Main Process
     │
     ├── Thread → API I/O
     ├── Thread → Database I/O
     │
     └── Process Pool
          ├── CPU Task
          ├── CPU Task
          └── CPU Task
```

Yani ye mutually exclusive concepts nahi hain.

Architecture workload par depend karti hai.

---

# 41. Golden decision rule

```text
Question 1:
Kya task mostly waiting/I/O hai?

YES
 ↓
threading / async often consider


Question 2:
Kya task CPU-heavy pure Python hai?

YES
 ↓
multiprocessing often consider


Question 3:
Kya workers ke beech task/data exchange chahiye?

YES
 ↓
Queue


Question 4:
Kya exactly do processes ko direct communication chahiye?

YES
 ↓
Pipe
```

---

# 42. Lesson 87–90 ka complete map

Ab tumhari concurrency foundation:

```text
CONCURRENCY
│
├── threading
│   │
│   ├── Thread
│   ├── Lock
│   ├── RLock
│   ├── Semaphore
│   ├── Event
│   ├── Condition
│   ├── Barrier
│   └── Timer
│
├── queue
│   │
│   ├── Queue
│   ├── LifoQueue
│   └── PriorityQueue
│
└── multiprocessing
    │
    ├── Process
    ├── Pool
    ├── Queue
    └── Pipe
```

---

## Sabse important 10 concepts

```text
Thread
→ same process ka execution path

Process
→ independent execution environment

Lock
→ one thread at a time

RLock
→ same thread re-acquire kar sakta hai

Semaphore
→ limited concurrent access

Event
→ signal

Condition
→ condition-based waiting

Barrier
→ all participants synchronize

Queue
→ safe task/message passing

Pipe
→ direct process communication
```

### Aur sabse important architecture:

```text
I/O-bound
   ↓
Threading

CPU-bound
   ↓
Multiprocessing

Producer → Consumer
   ↓
Queue

Process A ↔ Process B
   ↓
Pipe
```

**Next lesson: Lesson 91 — `concurrent.futures`: `ThreadPoolExecutor`, `ProcessPoolExecutor`, `Future`, `submit()`, `map()`, `as_completed()`**. Ye modern Python mein threading/multiprocessing ko manually manage karne ke bajaye high-level concurrent programming ka important layer hai.
