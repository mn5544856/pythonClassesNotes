# Lesson 21: `Optional`, `Union`, `Literal`, `Final`, `ClassVar`, `Any`, `Never`, `NoReturn`

Ab hum `typing` ke un types ko samjhenge jo real Python projects mein bohat use hote hain.

---

# 1. `Optional`

`Optional[T]` ka matlab:

> Value `T` ho sakti hai **ya `None`**.

Example:

```python
from typing import Optional

name: Optional[str]
```

Matlab:

```text
name → str
ya
name → None
```

Ye roughly equivalent hai:

```python
name: str | None
```

Modern Python mein `str | None` zyada common hai.

---

## Example

```python
def get_employee_name(employee_id: int) -> Optional[str]:
    if employee_id == 1:
        return "Ali"

    return None
```

Yahan function:

```text
employee mil gaya → str
employee nahi mila → None
```

---

# 2. `Optional` ka common use

```python
class Employee:

    def __init__(
        self,
        name: str,
        manager: Optional[str] = None
    ):
        self.name = name
        self.manager = manager
```

Ab:

```python
emp1 = Employee("Ali")
```

valid hai.

```python
emp2 = Employee("Ahmed", "Usman")
```

bhi valid hai.

Yani:

```text
manager:
    str
    OR
    None
```

---

# 3. Important: Optional ka matlab "optional parameter" nahi

Ye misconception common hai.

```python
name: Optional[str]
```

ka matlab:

> `name` `str` ya `None` ho sakta hai.

Ye automatically parameter ko optional nahi banata.

Example:

```python
def test(name: Optional[str]):
    ...
```

Yahan `name` argument dena phir bhi zaroori hai.

Agar argument optional banana hai:

```python
def test(name: Optional[str] = None):
    ...
```

Ab argument omit bhi kar sakte ho.

---

# 4. `Union`

`Union` ka matlab:

> Value multiple possible types mein se kisi ek type ki ho sakti hai.

Old style:

```python
from typing import Union

value: Union[int, str]
```

Matlab:

```text
int
OR
str
```

Modern Python:

```python
value: int | str
```

---

## Example

```python
def show_id(value: int | str):
    print(value)
```

Dono:

```python
show_id(100)
show_id("WO-100")
```

valid types hain.

---

# 5. `Optional` actually `Union` ka special case hai

Ye:

```python
Optional[str]
```

conceptually:

```python
Union[str, None]
```

hai.

Modern syntax:

```python
str | None
```

So:

```text
Optional[T]
     =
Union[T, None]
```

---

# 6. `Union` kab useful hai?

Suppose work-order ID kabhi integer hai:

```python
1001
```

aur kabhi string:

```python
"WO-1001"
```

Function:

```python
def process_work_order(
    work_order_id: int | str
):
    ...
```

Type checker ko clear information milti hai.

---

# 7. `Literal`

Ab `Literal`.

`Literal` ka matlab:

> Sirf **specific fixed values** allowed hain.

Example:

```python
from typing import Literal

status: Literal["open", "closed"]
```

Ab allowed values:

```text
"open"
"closed"
```

Lekin:

```python
status = "running"
```

type checker ke perspective se invalid hai.

---

# 8. `Literal` ka practical example

```python
def set_mode(
    mode: Literal["auto", "manual"]
):
    print(mode)
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

---

# 9. HVAC example

Honeywell/Building Automation type situation mein:

```python
from typing import Literal

def set_fan_mode(
    mode: Literal["auto", "manual", "off"]
):
    ...
```

Ab function ko explicitly pata hai ke allowed modes:

```text
auto
manual
off
```

hain.

Ye `str` se zyada precise hai.

Compare:

```python
mode: str
```

vs:

```python
mode: Literal["auto", "manual", "off"]
```

Second wala much more restrictive/type-safe hai.

---

# 10. `Final`

`Final` ka purpose:

> Kisi variable ko type-checking ke perspective se **reassign nahi karna chahiye**.

Example:

```python
from typing import Final

MAX_RETRIES: Final = 3
```

Phir:

```python
MAX_RETRIES = 10
```

type checker warning de sakta hai.

Mental model:

```text
Final
 ↓
"Is value ko dobara assign mat karo."
```

---

# 11. `Final` constant ke liye useful hai

Example:

```python
API_VERSION: Final = "v1"
DEFAULT_TIMEOUT: Final = 30
```

Ye indicate karta hai:

> Ye values configuration/constants hain; code mein reassign nahi honi chahiye.

---

# 12. `Final` runtime security nahi hai

Important:

```python
MAX_RETRIES: Final = 3
```

Python runtime par automatically variable ko immutable lock nahi karta.

Tum technically assignment kar sakte ho.

`Final` mainly:

```text
type checker
+
developer intent
```

ke liye hai.

---

# 13. `ClassVar`

Ab `ClassVar`.

Ye tumhare **class variable vs instance variable** wale lesson se directly connected hai.

Example:

```python
from typing import ClassVar

class Employee:

    company: ClassVar[str] = "ABC"

    def __init__(self, name: str):
        self.name = name
```

Yahan:

```python
company
```

class variable hai.

Aur:

```python
name
```

instance variable hai.

---

# 14. `ClassVar` kyun use karte hain?

Type checker ko clearly batane ke liye:

```python
company: ClassVar[str]
```

ka matlab:

> Ye value class-level hai, instance-level nahi.

Example:

```python
class Employee:

    company: ClassVar[str] = "ABC"
```

Use:

```python
print(Employee.company)
```

Lekin conceptually:

```python
emp = Employee()
```

ke instance-specific state mein `company` nahi hona chahiye.

---

# 15. ClassVar ka important rule

`ClassVar` ko generic type ke saath confuse mat karo.

```python
class Employee:
    company: ClassVar[str]
```

means:

```text
company → class variable
type    → str
```

---

# 16. `Any`

Ab sabse common type:

```python
from typing import Any
```

`Any` ka matlab:

> Type checker is value ko almost kisi bhi type ki tarah accept kare.

Example:

```python
value: Any
```

`value` ho sakta hai:

```text
int
str
list
dict
Employee
...
```

---

# 17. `Any` powerful hai, lekin carefully use karo

Example:

```python
def process(data: Any):
    ...
```

Isse type information weak ho jati hai.

Agar:

```python
data.foo.bar.xyz()
```

likh diya, type checker bohat si problems detect nahi karega.

Isliye:

```text
Any
↓
maximum flexibility
↓
minimum type safety
```

---

# 18. `Any` vs `object`

Ye important comparison hai.

### `Any`

```python
value: Any
```

Type checker ko basically kehte ho:

> "Is value ke type ko aggressively check mat karo."

### `object`

```python
value: object
```

Matlab:

> "Value koi bhi Python object ho sakti hai, lekin operations karne se pehle type narrow karo."

Example:

```python
value: object = "Hello"
```

Tum directly:

```python
value.upper()
```

type checker ke perspective se nahi kar sakte, kyun ke `object` ke paas `.upper()` guaranteed nahi.

Lekin:

```python
if isinstance(value, str):
    print(value.upper())
```

ab safe hai.

So:

```text
Any
→ type checking ko relax karta hai

object
→ broad type hai, lekin type checking maintain karta hai
```

---

# 19. `Never`

Ab advanced concept:

```python
from typing import Never
```

`Never` ka matlab:

> Aisi situation jahan **koi value return nahi hoti**.

Example:

```python
def fail(message: str) -> Never:
    raise RuntimeError(message)
```

Ye function normal return nahi karta.

---

# 20. `Never` ka common use

Infinite loop:

```python
def run_forever() -> Never:
    while True:
        print("Running...")
```

Function theoretically kabhi return nahi karega.

Another example:

```python
def impossible(value: Never) -> str:
    ...
```

Yahan `Never` ka deeper type-system meaning hai:

> Is function ko normal valid value milni hi nahi chahiye.

---

# 21. `NoReturn`

Purane Python typing code mein tum:

```python
from typing import NoReturn
```

dekh sakte ho.

Example:

```python
def fail(message: str) -> NoReturn:
    raise RuntimeError(message)
```

`NoReturn` historically indicate karta tha:

> Function return nahi karta.

Modern typing ecosystem mein `Never` preferred hai for this concept.

Isliye naye code mein tum aksar:

```python
-> Never
```

dekhoge.

---

# 22. `Never` vs `NoReturn`

Simple learning:

```text
NoReturn
→ old/common annotation for non-returning function

Never
→ modern typing concept for impossible/no-value situations
```

Existing projects mein `NoReturn` mile to confuse nahi hona.

---

# 23. `Literal` vs `Enum`

Ye bhi useful comparison hai.

### Literal

```python
mode: Literal["auto", "manual"]
```

Simple fixed values.

### Enum

```python
from enum import Enum

class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

Enum actual named members provide karta hai.

```text
Literal
→ typing constraint

Enum
→ actual Python enumeration type
```

Agar complex domain logic ho to `Enum` useful ho sakta hai.

---

# 24. Sab ko ek practical example mein combine karte hain

```python
from typing import (
    ClassVar,
    Final,
    Literal,
    Optional
)


class Equipment:

    SYSTEM_NAME: ClassVar[Final[str]] = "BMS"

    def __init__(
        self,
        equipment_id: str,
        temperature: Optional[float] = None,
        mode: Literal["auto", "manual"] = "auto"
    ):
        self.equipment_id = equipment_id
        self.temperature = temperature
        self.mode = mode
```

Yahan:

### `ClassVar`

```python
SYSTEM_NAME
```

class-level variable.

### `Final`

```python
SYSTEM_NAME
```

reassign nahi karna chahiye.

### `Optional`

```python
temperature
```

ho sakta hai:

```text
float
```

ya:

```text
None
```

### `Literal`

```python
mode
```

sirf:

```text
"auto"
"manual"
```

---

# 25. Example

```python
ahu = Equipment(
    "AHU-01",
    temperature=22.5,
    mode="auto"
)
```

Conceptually:

```text
equipment_id → str
temperature  → float | None
mode         → "auto" | "manual"
```

---

# 26. Complete `typing` map

Ab tumhare pehle wale import ko connect karte hain:

```python
from typing import (
    Any,
    Dict,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Union,
    TypeVar,
    Generic,
    TypedDict,
    Sequence,
    Iterator,
    Callable,
    ClassVar,
    Final,
    Literal,
    Never,
)
```

Inka simple meaning:

| Type             | Meaning                                 |
| ---------------- | --------------------------------------- |
| `Any`            | Type checking almost bypass             |
| `TypeVar`        | Generic type placeholder                |
| `Generic`        | Generic class/function structure        |
| `Optional`       | `T` or `None`                           |
| `Union`          | Multiple possible types                 |
| `Literal`        | Specific fixed values                   |
| `Final`          | Reassignment nahi honi chahiye          |
| `ClassVar`       | Class-level variable                    |
| `TypedDict`      | Dictionary structure/type               |
| `Protocol`       | Structural interface                    |
| `Mapping`        | Readable key-value abstraction          |
| `MutableMapping` | Modifiable key-value abstraction        |
| `Sequence`       | Ordered/indexable collection            |
| `Iterable`       | `for` se iterate ho sakta hai           |
| `Iterator`       | `next()` se next value deta hai         |
| `Callable`       | Function ki tarah call ho sakta hai     |
| `Never`          | No possible normal value/return         |
| `Tuple`          | Typed tuple, e.g. `Tuple[str, int]`     |
| `Dict`           | Typed dictionary, e.g. `Dict[str, int]` |

---

# 27. Modern Python syntax

Agar tum Python 3.10+ use kar rahe ho, purane syntax ki jagah modern syntax aksar cleaner hai.

### Old:

```python
Optional[str]
```

### Modern:

```python
str | None
```

---

### Old:

```python
Union[int, str]
```

### Modern:

```python
int | str
```

---

### Old:

```python
List[int]
```

### Modern:

```python
list[int]
```

---

### Old:

```python
Dict[str, int]
```

### Modern:

```python
dict[str, int]
```

---

### Old:

```python
Tuple[str, int]
```

### Modern:

```python
tuple[str, int]
```

Isliye modern Python code mein tum aksar:

```python
list[str]
dict[str, int]
tuple[str, int]
str | None
int | float
```

dekho ge.

---

# Final mental model

```text
                 Python Typing
                      │
       ┌──────────────┼──────────────┐
       │              │              │
    Type choice    Structure       Behavior
       │              │              │
   Union          TypedDict       Protocol
   Optional       ClassVar        Callable
   Literal
   Final
       │
   TypeVar
   Generic
```

Aur sabse important:

```text
Optional
→ T ya None

Union
→ T ya U

Literal
→ exact allowed values

Final
→ reassign nahi

ClassVar
→ class-level state

Any
→ type checking loose

TypeVar
→ type relationship preserve

Protocol
→ required behavior/interface

TypedDict
→ dictionary structure
```

**Next Lesson 22:** `Variance` — `Covariant`, `Contravariant`, aur `Invariant`. Ye `Generic`, `TypeVar`, `Sequence`, `Mapping` aur `Callable` ko ek deeper level par connect karega, aur explain karega ke **`list[Dog]` ko `list[Animal]` kyun automatically treat nahi kar sakte.**

# Lesson 22: Variance — Covariant, Contravariant, Invariant

Ye Python typing ka thora advanced topic hai. Iska main purpose ye samajhna hai ke **generic types ke darmiyan inheritance relationship kab preserve hota hai aur kab nahi**.

Is lesson ko samajhne ke liye pehle ek simple hierarchy banate hain.

---

## 1. `Animal` aur `Dog`

```python
class Animal:
    pass


class Dog(Animal):
    pass
```

Yahan:

```text
Animal
   ↑
  Dog
```

Matlab:

```python
dog = Dog()
```

ko `Animal` ke taur par treat kar sakte hain:

```python
animal: Animal = dog
```

Ye normal inheritance hai.

---

# 2. Ab `list` mein problem

Maan lo:

```python
dogs: list[Dog]
animals: list[Animal]
```

Question:

> Kya `list[Dog]` ko `list[Animal]` assign kar sakte hain?

Intuitively tum keh sakte ho:

```text
Dog is an Animal
```

to:

```text
list[Dog] should be list[Animal]
```

Lekin **nahi**.

---

# 3. Kyun?

Suppose Python allow kar de:

```python
dogs: list[Dog] = [Dog()]

animals: list[Animal] = dogs
```

Ab:

```python
animals.append(Animal())
```

Humne `animals` mein ek generic `Animal` add kar diya.

Lekin asal object:

```text
dogs
```

hone chahiye tha:

```text
sirf Dog
```

Ab `dogs` ke andar:

```text
Dog
Dog
Animal  ← problem
```

aa gaya.

Isi wajah se mutable `list` ko normally **invariant** treat kiya jata hai.

---

# 4. Invariant kya hai?

Simple definition:

> Generic type ka subtype relationship automatically generic container par apply nahi hota.

```text
Dog <: Animal

but

list[Dog] ≠ subtype of list[Animal]
```

Yahan:

```text
<:
```

ka matlab roughly:

> "is a subtype of"

---

# 5. Invariant ka mental model

```text
Dog → Animal

lekin

list[Dog] ─X→ list[Animal]
```

`list` mutable hai:

```python
dogs.append(...)
dogs[0] = ...
```

Isliye type safety maintain karne ke liye direct substitution allowed nahi.

---

# 6. `Sequence` different kyun hai?

Ab:

```python
from typing import Sequence
```

Maan lo:

```python
dogs: Sequence[Dog]
```

Aur function:

```python
def show_animals(
    animals: Sequence[Animal]
):
    ...
```

`Sequence` mostly **read-only abstraction** ki tarah use hoti hai.

Function:

```python
def show_animals(animals: Sequence[Animal]):
    for animal in animals:
        print(animal)
```

sirf read kar raha hai.

Isliye:

```text
Sequence[Dog]
       ↓
Sequence[Animal]
```

allowed ho sakta hai.

Ye **covariance** hai.

---

# 7. Covariant ka matlab

> Agar `Dog` → `Animal`, to generic container mein bhi `Container[Dog]` → `Container[Animal]` allowed ho.

Conceptually:

```text
Dog
 ↓
Animal

Sequence[Dog]
 ↓
Sequence[Animal]
```

---

# 8. `Sequence` covariant kyun ho sakti hai?

Kyunkay:

```python
animals: Sequence[Animal]
```

ke through tum normally:

```python
animals.append(...)
```

nahi kar sakte.

Yani caller sequence ke andar arbitrary `Animal` insert nahi kar sakta.

Isliye safety maintain hoti hai.

---

# 9. Simple example

```python
class Animal:
    def speak(self):
        print("Animal sound")


class Dog(Animal):
    def speak(self):
        print("Woof")
```

Ab:

```python
dogs: list[Dog] = [
    Dog(),
    Dog()
]
```

Tum isko read-only interface ke through de sakte ho:

```python
animals: Sequence[Animal] = dogs
```

Function:

```python
def print_animals(
    animals: Sequence[Animal]
):
    for animal in animals:
        animal.speak()
```

Use:

```python
print_animals(dogs)
```

Conceptually safe hai.

---

# 10. `TypeVar` mein covariance

Ab generic class khud banate hain.

```python
from typing import TypeVar, Generic

T_co = TypeVar(
    "T_co",
    covariant=True
)
```

`_co` naam convention hai.

Tum technically koi aur naam rakh sakte ho:

```python
T = TypeVar("T", covariant=True)
```

Lekin:

```text
T_co
```

dekh kar developer ko immediately pata chal jata hai ke:

> Ye covariant TypeVar hai.

---

# 11. Covariant generic class

```python
from typing import Generic, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Box(Generic[T_co]):

    def __init__(self, value: T_co):
        self._value = value

    def get(self) -> T_co:
        return self._value
```

Yahan Box value ko **provide/read** karta hai.

---

# 12. `Box[Dog]` vs `Box[Animal]`

Agar:

```python
dog_box: Box[Dog]
```

hai to covariance ki wajah se conceptually:

```python
animal_box: Box[Animal] = dog_box
```

allowed ho sakta hai.

Kyun?

Kyunkay:

```python
animal_box.get()
```

se jo object milega woh kam az kam `Animal` hoga.

Actually woh `Dog` hai, jo `Animal` hai.

Safe.

---

# 13. Covariance ka real mental model

Covariance mostly:

```text
PRODUCER
```

ke saath associated hai.

Producer:

> "Main tumhein `T` provide karta hoon."

Example:

```python
def get(self) -> T:
    return self._value
```

---

# 14. Contravariance

Ab opposite direction.

Contravariance initially confusing lagti hai, lekin function example se easy hoti hai.

```text
Covariance
→ output / producer

Contravariance
→ input / consumer
```

---

# 15. Consumer kya hota hai?

Suppose:

```python
class Animal:
    pass


class Dog(Animal):
    pass
```

Ek function jo `Animal` accept karta hai:

```python
def handle_animal(animal: Animal):
    print("Handling animal")
```

Ye:

```python
handle_animal(Dog())
```

accept kar sakta hai.

Kyun?

Dog is an Animal.

---

# 16. `Callable` mein contravariance

Suppose:

```python
from typing import Callable
```

Humare paas:

```python
AnimalHandler = Callable[[Animal], None]
```

Matlab function ko `Animal` accept karna chahiye.

Ab:

```python
def handle_animal(animal: Animal):
    print("Animal handled")
```

Ye function:

```text
Animal
```

accept karta hai.

To ye `Dog` ko bhi handle kar sakta hai.

---

# 17. Lekin Dog-only handler?

```python
def handle_dog(dog: Dog):
    print("Dog handled")
```

Ye sirf `Dog` accept karta hai.

Agar koi caller expect kar raha hai:

```python
Callable[[Animal], None]
```

to `handle_dog` safely substitute nahi kar sakte.

Kyun?

Caller keh sakta hai:

```python
handler(Cat())
```

Aur `handle_dog()` Cat handle nahi kar sakta.

---

# 18. Isi wajah se contravariance

Function input types ka relationship **opposite direction** mein hota hai.

Simplified:

```text
Animal
  ↑
 Dog
```

Input/consumer context mein:

```text
Callable[[Animal], None]
          ↓
can handle Dog too
```

Lekin:

```text
Callable[[Dog], None]
```

ko generic Animal handler ki jagah use nahi kar sakte.

---

# 19. Contravariant TypeVar

Syntax:

```python
T_contra = TypeVar(
    "T_contra",
    contravariant=True
)
```

Example:

```python
from typing import Generic, TypeVar

T_contra = TypeVar(
    "T_contra",
    contravariant=True
)


class Handler(Generic[T_contra]):

    def handle(self, value: T_contra):
        print(value)
```

Yahan `Handler` ka main role:

```text
T ko consume karna
```

hai.

---

# 20. Covariant vs Contravariant

Ye table yaad rakho:

| Variance      | Main role            | Direction          |
| ------------- | -------------------- | ------------------ |
| Covariant     | Producer / output    | Same direction     |
| Contravariant | Consumer / input     | Opposite direction |
| Invariant     | Read + write / mixed | No substitution    |

Mental shortcut:

```text
CO = OUT
CONTRA = IN
INVARIANT = BOTH
```

Ye exact universal rule nahi hai, lekin generics samajhne ke liye bohat useful mnemonic hai.

---

# 21. Invariant

Ab third:

```text
Invariant
```

Agar:

```text
Dog <: Animal
```

to:

```text
Box[Dog]
```

automatically:

```text
Box[Animal]
```

nahi banega.

Example:

```python
T = TypeVar("T")

class Storage(Generic[T]):

    def get(self) -> T:
        ...

    def set(self, value: T):
        ...
```

Yahan class:

```text
T ko produce bhi karti hai
T ko consume bhi karti hai
```

Isliye generic type ko safely covariant ya contravariant banana possible nahi.

Default `TypeVar`:

```python
T = TypeVar("T")
```

**invariant** hota hai.

---

# 22. Storage example

```python
class Storage(Generic[T]):

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    def set(self, value: T) -> None:
        self.value = value
```

Suppose:

```python
dog_storage: Storage[Dog]
```

Agar isko:

```python
animal_storage: Storage[Animal]
```

maan liya jaye, to:

```python
animal_storage.set(Cat())
```

ho sakta hai.

Phir actual:

```text
dog_storage
```

ke andar Cat aa jayegi.

Unsafe.

Isliye invariant.

---

# 23. Ek diagram

```text
                 Animal
                /      \
              Dog      Cat


COVARIANT
Sequence[Dog]
      ↓
Sequence[Animal]


INVARIANT
list[Dog]
      X
list[Animal]


CONTRAVARIANT
Consumer[Animal]
      ↓
Consumer[Dog]
```

Last direction initially weird lag sakti hai.

Isko "consumer ki capability" ke perspective se dekho:

```text
Animal consumer
```

Dog ko consume kar sakta hai.

Lekin:

```text
Dog consumer
```

har Animal ko consume nahi kar sakta.

---

# 24. HVAC example

Maan lo:

```python
class Equipment:
    pass


class AHU(Equipment):
    pass


class VAV(Equipment):
    pass
```

### Producer

```python
class EquipmentProvider(Generic[T_co]):

    def get(self) -> T_co:
        ...
```

Provider:

```text
Equipment provide karta hai
```

Covariance useful ho sakti hai.

---

### Consumer

```python
class EquipmentHandler(Generic[T_contra]):

    def handle(self, equipment: T_contra):
        ...
```

Handler:

```text
Equipment consume karta hai
```

Contravariance relevant ho sakti hai.

---

### Storage

```python
class EquipmentStorage(Generic[T]):
    
    def get(self) -> T:
        ...
    
    def set(self, value: T):
        ...
```

Ye:

```text
read + write
```

karta hai.

So invariant.

---

# 25. `Mapping` interesting example

Typing system mein kuch generic abstractions naturally covariance/contravariance use karti hain.

For example:

```python
Mapping[K, V]
```

conceptually keys ko input side aur values ko output side par use karta hai.

`Mapping` ka type behavior isliye `dict` se zyada nuanced hai.

Tumhe har built-in generic ki variance memorize karne ki zaroorat nahi.

Important lesson ye hai:

> **Interface ka use kis direction mein ho raha hai—produce, consume, ya dono?**

---

# 26. `list` vs `Sequence` phir se

Ab previous lesson ka connection clear hona chahiye.

### `list`

```python
list[T]
```

mutable:

```python
items.append(...)
items[0] = ...
```

Isliye invariant.

### `Sequence`

```python
Sequence[T]
```

primarily read/index abstraction:

```python
items[0]
len(items)
```

Isliye covariance possible.

---

# 27. `Callable` ka deeper connection

`Callable` mein:

```python
Callable[[Input], Output]
```

do different directions hain:

```text
Input
 ↓
consumer

Output
 ↓
producer
```

Isi wajah se function types ko samajhne mein variance important hai.

Example:

```python
Callable[[Animal], Dog]
```

mein:

```text
Animal
→ input

Dog
→ output
```

Input contravariant behavior follow karta hai.

Output covariant behavior follow karta hai.

---

# 28. Isko abhi kitna yaad rakhna hai?

Tumhein initially ye 3 lines yaad rakhni hain:

```text
Covariant
→ output / producer
→ same direction

Contravariant
→ input / consumer
→ opposite direction

Invariant
→ read + write
→ no automatic substitution
```

Example:

```text
Sequence → covariance
list     → invariance
Callable → input/output variance
```

---

# 29. `TypeVar` ke saath connection

Tumne Lesson 19 mein dekha:

```python
T = TypeVar("T")
```

Default:

```text
Invariant
```

Covariant:

```python
T_co = TypeVar(
    "T_co",
    covariant=True
)
```

Contravariant:

```python
T_contra = TypeVar(
    "T_contra",
    contravariant=True
)
```

So:

```text
TypeVar
   │
   ├── invariant
   ├── covariant
   └── contravariant
```

---

# 30. Final cheat sheet

```text
Dog <: Animal
```

### Covariant

```text
Container[Dog]
      ↓
Container[Animal]
```

Producer / output.

### Contravariant

```text
Consumer[Animal]
      ↓
Consumer[Dog]
```

Consumer / input.

### Invariant

```text
Container[Dog]
      X
Container[Animal]
```

Read + write.

---

## Ek line mein pura lesson

> **Covariance mein type hierarchy same direction mein chalti hai, contravariance mein opposite direction mein, aur invariance mein generic types ke darmiyan automatic substitution allowed nahi hoti.**

**Next Lesson 23:** Python **generators + `yield` + `send()` + `yield from`** — ismein hum `Iterable`, `Iterator`, generator function aur `next()` ko practically connect karenge.

# Lesson 23: Generators, `yield`, `next()` aur `yield from`

Ab hum `Iterable` aur `Iterator` ko practically samjhenge. Ye Python mein **memory-efficient data processing** ke liye bohat important concept hai.

---

## 1. Normal function vs Generator function

Normal function:

```python
def numbers():
    return [1, 2, 3]
```

Call:

```python
result = numbers()

print(result)
```

Output:

```text
[1, 2, 3]
```

Yahan poori list ek saath memory mein ban gayi.

---

## 2. Generator function

Ab `return` ki jagah `yield`:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Ab:

```python
result = numbers()

print(result)
```

Tumhein list nahi milegi.

`result` ek **generator object** hoga.

```text
numbers()
   ↓
generator
```

---

# 3. `yield` kya karta hai?

`yield` ka simple meaning:

> Function ki execution ko temporarily pause karo aur ek value bahar do.

Example:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Flow:

```text
generator start
     ↓
yield 1
     ↓
pause
     ↓
yield 2
     ↓
pause
     ↓
yield 3
     ↓
pause/end
```

---

# 4. `next()` se value nikalna

```python
def numbers():
    yield 1
    yield 2
    yield 3


g = numbers()

print(next(g))
```

Output:

```text
1
```

Phir:

```python
print(next(g))
```

Output:

```text
2
```

Phir:

```python
print(next(g))
```

Output:

```text
3
```

---

# 5. Fourth `next()`

Ab:

```python
print(next(g))
```

karoge to:

```text
StopIteration
```

aayega.

Kyun?

Generator ke paas aur values nahi hain.

---

# 6. Important: Generator ek Iterator hai

Ye relationship yaad rakho:

```text
Generator
    ↓
Iterator
    ↓
Iterable
```

Generator object:

```python
g = numbers()
```

ke paas:

```python
next(g)
```

work karta hai.

Isliye generator iterator protocol follow karta hai.

---

# 7. `for` loop generator ke saath

Normally tum manually:

```python
next(g)
```

nahi karte.

```python
for number in numbers():
    print(number)
```

Output:

```text
1
2
3
```

`for` loop internally iterator mechanism use karta hai.

Conceptually:

```text
iter()
 ↓
next()
 ↓
next()
 ↓
next()
 ↓
StopIteration
```

---

# 8. Generator vs List

Ye bohat important difference hai.

### List

```python
numbers = [1, 2, 3, 4, 5]
```

Values already stored hain.

### Generator

```python
def numbers():
    for i in range(1, 6):
        yield i
```

Values **one-by-one generate** hoti hain.

Mental model:

```text
List
→ sab data pehle ready

Generator
→ jab zaroorat ho tab next data
```

---

# 9. Memory ka advantage

Suppose:

```python
numbers = [x for x in range(1_000_000)]
```

Yahan million values ki collection memory mein create hoti hai.

Generator:

```python
numbers = (x for x in range(1_000_000))
```

values ko lazily produce karta hai.

```text
List
→ eager

Generator
→ lazy
```

---

# 10. Lazy evaluation

**Lazy** ka matlab:

> Result ko tab calculate karo jab uski zaroorat ho.

Example:

```python
def numbers():
    print("1 generate")
    yield 1

    print("2 generate")
    yield 2
```

Ab:

```python
g = numbers()
```

par function body immediately normally execute nahi hoti.

Phir:

```python
print(next(g))
```

Output:

```text
1 generate
1
```

Phir:

```python
print(next(g))
```

Output:

```text
2 generate
2
```

Yani computation demand par hui.

---

# 11. Generator ka state preserve hota hai

Ye `yield` ka powerful feature hai.

```python
def counter():
    print("Start")

    yield 1

    print("Middle")

    yield 2

    print("End")
```

```python
g = counter()
```

First:

```python
next(g)
```

Output:

```text
Start
1
```

Function `yield 1` ke baad pause hai.

Second:

```python
next(g)
```

Output:

```text
Middle
2
```

Python ko yaad hai ke execution kahan pause hui thi.

---

# 12. `yield` vs `return`

### `return`

```python
def test():
    return 10
    return 20
```

Sirf:

```text
10
```

milega.

Function terminate ho gaya.

### `yield`

```python
def test():
    yield 10
    yield 20
```

Pehli value ke baad function pause hota hai.

Phir next request par continue karta hai.

```text
yield
→ pause + value

return
→ terminate + value
```

---

# 13. Generator expression

List comprehension:

```python
numbers = [x * 2 for x in range(10)]
```

Generator expression:

```python
numbers = (x * 2 for x in range(10))
```

Difference:

```text
[ ... ]
→ list

( ... )
→ generator expression
```

---

# 14. Example

```python
numbers = (x * 2 for x in range(5))

for x in numbers:
    print(x)
```

Output:

```text
0
2
4
6
8
```

Lekin values lazily generate hoti hain.

---

# 15. Real-world example: CSV rows

Suppose tumhare paas bohat large CSV hai.

Bad approach:

```python
rows = load_entire_csv()
```

Agar file bohat large ho to memory problem aa sakti hai.

Generator approach:

```python
def read_rows(file):
    for line in file:
        yield line
```

Ab:

```python
for row in read_rows(file):
    process(row)
```

Ek waqt mein ek row process kar sakte ho.

Ye data-processing scripts mein bohat useful hai.

---

# 16. Tumhare Work Order project ka example

Maan lo:

```python
def work_orders(rows):
    for row in rows:
        yield row
```

Phir:

```python
for row in work_orders(output_data):
    create_folder(row)
```

Agar `output_data` bohat large ho, generator approach processing ko lazy rakh sakti hai.

---

# 17. Generator mein condition

Example:

```python
def even_numbers(numbers):
    for number in numbers:
        if number % 2 == 0:
            yield number
```

Use:

```python
for number in even_numbers(range(10)):
    print(number)
```

Output:

```text
0
2
4
6
8
```

Yahan generator sirf required values produce kar raha hai.

---

# 18. Generator pipeline

Generators ko chain karna bohat powerful hai.

Example:

```python
def numbers():
    for i in range(10):
        yield i
```

Filter:

```python
def even(numbers):
    for number in numbers:
        if number % 2 == 0:
            yield number
```

Transform:

```python
def square(numbers):
    for number in numbers:
        yield number * number
```

Ab:

```python
data = square(even(numbers()))
```

Aur:

```python
for value in data:
    print(value)
```

Output:

```text
0
4
16
36
64
```

Flow:

```text
numbers()
   ↓
even()
   ↓
square()
   ↓
for loop
```

Ye **lazy pipeline** hai.

---

# 19. `yield from`

Ab next important feature:

```python
yield from
```

Suppose:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Dusra generator:

```python
def all_numbers():
    yield from numbers()
```

Ab:

```python
for x in all_numbers():
    print(x)
```

Output:

```text
1
2
3
```

---

# 20. `yield from` ka simple meaning

```python
yield from numbers()
```

roughly:

> "Is iterable/generator ki values ko one-by-one yield karo."

Instead of:

```python
def all_numbers():
    for x in numbers():
        yield x
```

tum likh sakte ho:

```python
def all_numbers():
    yield from numbers()
```

---

# 21. Multiple generators combine karna

```python
def temperatures():
    yield 22.5
    yield 23.0


def pressures():
    yield 250
    yield 255


def sensor_data():
    yield from temperatures()
    yield from pressures()
```

Ab:

```python
for value in sensor_data():
    print(value)
```

Output:

```text
22.5
23.0
250
255
```

---

# 22. `yield from` aur list

`yield from` sirf generator ke liye nahi.

```python
def numbers():
    yield from [10, 20, 30]
```

Ab:

```python
list(numbers())
```

Output:

```text
[10, 20, 30]
```

Kyun ke list bhi iterable hai.

---

# 23. `send()` — advanced generator feature

Ab generator ka powerful part.

Generator sirf value **bahar nahi deta**.

Tum generator ke andar value **bhej bhi sakte ho**.

Syntax:

```python
generator.send(value)
```

Example:

```python
def receiver():
    value = yield
    print("Received:", value)
```

Start:

```python
g = receiver()
```

Pehle:

```python
next(g)
```

zaroori hai.

Kyun?

Generator ko first `yield` tak start karna hota hai.

Phir:

```python
g.send(100)
```

Output:

```text
Received: 100
```

---

# 24. `yield` expression

Ye:

```python
value = yield
```

thoda different hai.

Yahan `yield` sirf value produce nahi kar raha.

Ye expression bhi hai.

Flow:

```text
generator
   ↓
yield
   ↓
pause
   ↓
send(100)
   ↓
yield expression = 100
   ↓
value = 100
```

---

# 25. `yield` ke saath send

Example:

```python
def calculator():
    total = 0

    while True:
        value = yield total
        total += value
```

Start:

```python
calc = calculator()
```

First:

```python
print(next(calc))
```

Output:

```text
0
```

Ab:

```python
print(calc.send(10))
```

Output:

```text
10
```

Phir:

```python
print(calc.send(20))
```

Output:

```text
30
```

Phir:

```python
print(calc.send(5))
```

Output:

```text
35
```

Generator state maintain kar raha hai.

---

# 26. Iska mental model

```text
next()
  ↓
generator se value lo

send(value)
  ↓
generator ke andar value bhejo
```

Yani generator ek tarah ka:

```text
two-way communication mechanism
```

bhi ban sakta hai.

---

# 27. `Iterable`, `Iterator`, `Generator`

Ab previous lessons connect karo.

### Iterable

```text
for loop mein use ho sakta hai
```

### Iterator

```text
next() se next value deta hai
```

### Generator

```text
yield se iterator easily create karta hai
```

Diagram:

```text
Iterable
   │
   ├── list
   ├── tuple
   ├── set
   └── generator
              ↓
           Iterator
              ↓
            next()
```

---

# 28. Generator function ko identify kaise karein?

Agar function ke andar:

```python
yield
```

hai:

```python
def data():
    yield 10
```

to woh normal function call par direct result nahi deta.

```python
g = data()
```

returns generator object.

---

# 29. Generator ka major benefit

```text
1. Lazy evaluation
2. Low memory usage
3. Large files/data processing
4. Streaming
5. Data pipelines
6. Infinite sequences
```

---

# 30. Infinite generator

Ye interesting example:

```python
def counter():
    number = 0

    while True:
        yield number
        number += 1
```

Ab:

```python
g = counter()
```

Tum theoretically endlessly:

```python
next(g)
```

kar sakte ho:

```text
0
1
2
3
4
5
...
```

Yahan list banana impossible/undesirable hota:

```python
list(range(...))
```

lekin generator lazily values provide kar sakta hai.

---

# 31. `isinstance` se check

```python
from collections.abc import Iterator

g = (x for x in range(5))

print(isinstance(g, Iterator))
```

Conceptually:

```text
True
```

Aur:

```python
from collections.abc import Iterable

print(isinstance(g, Iterable))
```

bhi:

```text
True
```

---

# 32. `typing.Iterable` vs `collections.abc.Iterable`

Modern Python code mein runtime checks ke liye aksar:

```python
from collections.abc import Iterable, Iterator
```

use kiya jata hai.

Typing annotations mein bhi `collections.abc` types modern Python mein commonly preferred hain.

Example:

```python
from collections.abc import Iterable

def process(data: Iterable[str]):
    ...
```

---

# 33. Practical Work Order example

Suppose:

```python
def valid_rows(rows):
    for row in rows:
        if row[0]:
            yield row
```

Phir:

```python
valid = valid_rows(output_data)
```

Ab tum:

```python
for row in valid:
    print(row)
```

kar sakte ho.

Agar rows million hain, filtering ka result ek huge list banane ki zaroorat nahi.

---

# 34. Generator vs List Comprehension

### List comprehension

```python
result = [
    x * 2
    for x in range(1_000_000)
]
```

Memory mein result collection.

### Generator expression

```python
result = (
    x * 2
    for x in range(1_000_000)
)
```

Lazy.

So:

```text
Need all results immediately?
→ list

Process one-by-one?
→ generator
```

---

# Final Cheat Sheet

```text
yield
→ value do + function pause

next(generator)
→ next value lo

send(value)
→ generator ke andar value bhejo

yield from
→ doosre iterable/generator se values forward karo

Generator
→ lazy iterator

Iterable
→ for loop possible

Iterator
→ next() possible
```

### Sabse important flow:

```text
def function():
    yield value
        ↓
function()
        ↓
Generator object
        ↓
next()
        ↓
value
        ↓
pause
        ↓
next()
        ↓
next value
```

Aur `yield from`:

```text
Generator A
    ↓
yield from
    ↓
Generator B
    ↓
values one-by-one
```

**Next Lesson 24:** Python **async/await, Coroutine, `asyncio`, `await`, Task aur Event Loop** — yani generator ke baad Python asynchronous programming ka architecture kaise kaam karta hai.

# Lesson 24: `async`, `await`, Coroutine aur Event Loop

Ab hum Python ke **asynchronous programming** mein enter karte hain.

Ye topic especially useful hai jab program ko:

* API calls karni hon
* network requests karni hon
* files/network se data lena ho
* multiple I/O operations handle karni hon
* ek kaam ke wait ke dauran doosra kaam karna ho

Sab se pehle ek important distinction:

```text
Normal function
→ synchronous

async function
→ coroutine

asyncio
→ event loop ke through coroutines ko run karta hai
```

---

## 1. Synchronous programming

Normal Python code:

```python
import time

def task(name):
    print(name, "start")
    time.sleep(2)
    print(name, "end")


task("A")
task("B")
```

Flow:

```text
Task A start
    ↓
2 sec wait
    ↓
Task A end
    ↓
Task B start
    ↓
2 sec wait
    ↓
Task B end
```

Total roughly:

```text
4 seconds
```

Yahan program `time.sleep()` ke waqt **block** ho raha hai.

---

# 2. `async def`

Async function banane ke liye:

```python
async def task():
    print("Task running")
```

Lekin ek important point:

```python
task()
```

karne se function normally execute nahi hota.

Ye ek **coroutine object** return karta hai.

```python
result = task()

print(result)
```

Conceptually:

```text
task()
   ↓
Coroutine object
```

---

# 3. Coroutine kya hai?

Coroutine ko simple words mein:

> Aisa asynchronous computation jise pause aur resume kiya ja sakta hai.

Example:

```python
async def task():
    print("Start")
    await something()
    print("End")
```

Flow:

```text
Start
  ↓
await
  ↓
pause
  ↓
other async work
  ↓
resume
  ↓
End
```

Ye `yield` ke concept se related hai, lekin coroutine ka purpose asynchronous coordination hai.

---

# 4. `await` kya karta hai?

`await` ka basic idea:

> Is asynchronous operation ke complete hone ka wait karo, lekin event loop ko doosre async tasks run karne do.

Example conceptual:

```python
async def download():
    data = await get_data()
    return data
```

Jab:

```python
await get_data()
```

par wait ho raha hai, event loop doosre ready tasks ko run kar sakta hai.

---

# 5. `asyncio`

Python mein asynchronous programming ka major standard library framework:

```python
import asyncio
```

Simple example:

```python
import asyncio

async def hello():
    print("Hello")


asyncio.run(hello())
```

`asyncio.run()` coroutine ko run karne ke liye event loop setup/run karta hai.

---

# 6. `asyncio.sleep()`

Async code mein:

```python
time.sleep(2)
```

ke bajaye usually:

```python
await asyncio.sleep(2)
```

use karte hain.

Example:

```python
import asyncio

async def task():
    print("Start")
    await asyncio.sleep(2)
    print("End")

asyncio.run(task())
```

Important:

```text
time.sleep()
→ thread ko block karta hai

await asyncio.sleep()
→ coroutine ko pause karta hai
→ event loop doosra async work kar sakta hai
```

---

# 7. Do async tasks

Ab interesting part:

```python
import asyncio

async def task(name):
    print(name, "start")
    await asyncio.sleep(2)
    print(name, "end")


async def main():
    await task("A")
    await task("B")


asyncio.run(main())
```

Ye ab bhi roughly:

```text
A start
wait 2 sec
A end
B start
wait 2 sec
B end
```

So approximately **4 seconds**.

Sirf `async def` likhne se automatically parallel execution nahi hoti.

Ye bohat important point hai.

---

# 8. Concurrent execution

Ab `create_task()` use karte hain:

```python
import asyncio

async def task(name):
    print(name, "start")
    await asyncio.sleep(2)
    print(name, "end")


async def main():
    task1 = asyncio.create_task(task("A"))
    task2 = asyncio.create_task(task("B"))

    await task1
    await task2


asyncio.run(main())
```

Ab flow roughly:

```text
A start
B start

     ↓
both waiting

2 seconds

     ↓
A end
B end
```

Total roughly:

```text
2 seconds
```

instead of 4.

---

# 9. Event Loop

Ab main concept:

## Event Loop

Event loop ka kaam hai:

```text
coroutines/tasks ko manage karna
```

Simplified:

```text
             Event Loop
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
    Task A    Task B    Task C
       │         │         │
       ↓         ↓         ↓
    waiting   ready     waiting
       │         │
       └─────────┘
             ↓
       jo ready hai
       usko run karo
```

Agar Task A network response ka wait kar raha hai:

```text
Task A
  ↓
await network
  ↓
pause
```

Event loop:

```text
"Task A wait kar raha hai,
main Task B chala deta hoon."
```

---

# 10. CPU vs I/O

Async programming ka sabse important use case:

```text
I/O-bound work
```

Examples:

```text
HTTP request
Database query
Network communication
File I/O
Socket
API response
```

CPU-heavy work:

```text
Huge mathematical calculation
Image processing
Machine learning computation
Large compression task
```

ke liye `asyncio` automatically CPU ko parallel nahi karta.

---

# 11. Important misconception

Ye:

```python
async def calculate():
    for i in range(1_000_000_000):
        ...
```

automatically CPU parallelism nahi deta.

Agar coroutine continuously CPU ka kaam karti rahe aur:

```python
await
```

na kare, to event loop ko doosre tasks ka chance nahi milega.

---

# 12. `await` = cooperative multitasking

Asyncio mein tasks khud cooperate karte hain.

Example:

```python
async def task():
    await something()
```

Task keh raha hai:

> "Main abhi wait kar raha hoon. Tum doosra task chala lo."

Isko:

```text
cooperative multitasking
```

kehte hain.

---

# 13. `asyncio.gather()`

Multiple coroutines ko concurrently run karne ka convenient method:

```python
import asyncio

async def task(name):
    await asyncio.sleep(2)
    return f"{name} done"


async def main():
    results = await asyncio.gather(
        task("A"),
        task("B"),
        task("C")
    )

    print(results)


asyncio.run(main())
```

Result:

```text
['A done', 'B done', 'C done']
```

Teeno tasks roughly same 2-second waiting period mein run ho sakte hain.

---

# 14. `gather()` ka mental model

```text
gather(
    task A,
    task B,
    task C
)
       ↓
run concurrently
       ↓
wait for all
       ↓
results
```

Ye especially API calls ke liye useful hota hai.

---

# 15. Real API example

Suppose tumhein 3 equipment APIs se data lena hai:

```text
AHU-01
VAV-01
VAV-02
```

Synchronous approach:

```text
API 1 → wait
API 2 → wait
API 3 → wait
```

Async approach:

```text
API 1 ─┐
API 2 ─┼→ concurrently waiting
API 3 ─┘
```

Agar network waiting dominant hai to overall response time significantly reduce ho sakta hai.

---

# 16. `create_task()` vs `gather()`

### `create_task()`

Explicitly ek Task schedule karta hai:

```python
task = asyncio.create_task(my_coroutine())
```

### `gather()`

Multiple awaitables ko collect/run karta hai:

```python
results = await asyncio.gather(
    task1(),
    task2(),
    task3()
)
```

Simple mental model:

```text
create_task
→ task ko schedule karo

gather
→ multiple async operations ko ek group ki tarah await karo
```

---

# 17. Coroutine vs Task

Ye distinction important hai.

### Coroutine

```python
async def work():
    ...
```

Call:

```python
coro = work()
```

returns coroutine object.

### Task

```python
task = asyncio.create_task(work())
```

Task event loop ke through scheduled execution ko represent karta hai.

Diagram:

```text
async def work()
       ↓
 coroutine function

work()
       ↓
 coroutine object

create_task(work())
       ↓
 Task
       ↓
 Event Loop
```

---

# 18. `await` kis cheez par use hota hai?

Usually kisi **awaitable** par.

Important awaitable concepts:

```text
Coroutine
Task
Future
```

Example:

```python
result = await task
```

Task complete hone ka wait.

---

# 19. Future

`Future` asyncio ka lower-level concept hai.

Simplified:

> Future ek placeholder hai jisme asynchronous operation ka result baad mein available hoga.

Conceptually:

```text
Future
  ↓
abhi result nahi
  ↓
operation complete
  ↓
result available
```

Beginner level par `Task` aur coroutine zyada important hain.

---

# 20. `async with`

Tumne pehle context managers mein:

```python
with resource:
    ...
```

dekha tha.

Async version:

```python
async with resource:
    ...
```

Ye asynchronous context manager use karta hai.

Ismein special methods:

```python
__aenter__()
__aexit__()
```

hote hain.

So:

```text
with
→ __enter__
→ __exit__

async with
→ __aenter__
→ __aexit__
```

---

# 21. `async for`

Normal:

```python
for item in items:
    ...
```

Async:

```python
async for item in items:
    ...
```

Iske peeche asynchronous iteration protocol hota hai:

```python
__aiter__()
__anext__()
```

Aur end par:

```text
StopAsyncIteration
```

Aata hai.

---

# 22. Normal vs Async protocols

Ab previous lessons connect karo:

```text
Normal iteration
    ↓
__iter__()
    ↓
__next__()
```

Async iteration:

```text
Async iteration
    ↓
__aiter__()
    ↓
__anext__()
```

Normal context manager:

```text
__enter__()
__exit__()
```

Async context manager:

```text
__aenter__()
__aexit__()
```

---

# 23. Async generator

Tumne previous lesson mein generator dekha:

```python
def numbers():
    yield 1
    yield 2
```

Async generator:

```python
async def numbers():
    yield 1
    yield 2
```

Use:

```python
async for number in numbers():
    print(number)
```

Yahan:

```text
async def + yield
```

→ async generator.

---

# 24. Real-world mental model

Suppose tum Power BI ke liye multiple data sources se data collect kar rahe ho:

```text
Saudi Exchange API
       ↓
Broker data
       ↓
Company data
       ↓
News API
```

Agar sab network I/O hai:

```text
Sequential:

API 1 → wait
        ↓
API 2 → wait
        ↓
API 3 → wait
        ↓
API 4 → wait
```

Async:

```text
API 1 ──────┐
API 2 ──────┤
API 3 ──────┼→ Event Loop
API 4 ──────┘
```

Jab ek API wait kar rahi hoti hai, doosri request progress kar sakti hai.

---

# 25. Async ka golden rule

Ye yaad rakho:

```text
async
→ coroutine define karta hai

await
→ coroutine ko asynchronously wait karwata hai

asyncio
→ event loop aur async infrastructure deta hai

create_task
→ coroutine ko scheduled task banata hai

gather
→ multiple async operations ko combine karta hai
```

---

# 26. Sabse important comparison

| Concept      | Meaning                           |
| ------------ | --------------------------------- |
| `def`        | normal function                   |
| `async def`  | coroutine function                |
| `return`     | function finish                   |
| `yield`      | generator pause + value           |
| `await`      | async operation ka wait           |
| `asyncio`    | async framework                   |
| Event Loop   | tasks/coroutines manage karta hai |
| Task         | scheduled coroutine               |
| Future       | future result ka placeholder      |
| `async for`  | async iteration                   |
| `async with` | async context manager             |

---

## Final mental model

```text
                 asyncio
                    │
              Event Loop
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Task A      Task B      Task C
        │           │           │
      await       await       ready
        │           │           │
      waiting     waiting      run
        │           │           │
        └───────────┴───────────┘
                    ↓
              Event Loop
              next ready task
```

Aur sabse important:

> **Asyncio ka main benefit I/O-bound work mein hai: jab ek task wait kar raha hota hai, event loop doosre ready task ko run kar sakta hai.**

**Next Lesson 25:** `asyncio` ko aur deep level par le jayenge: **Event Loop internally kaise kaam karta hai, `Task`, `Future`, cancellation, `timeout`, `asyncio.create_task()`, aur exception handling**.

# Lesson 25: `Task`, `Future`, Cancellation aur Timeout

Lesson 24 mein humne dekha:

```text
async def
await
asyncio
Event Loop
Task
gather()
```

Ab in concepts ko **andar se thora deeper** samajhte hain.

---

## 1. `Task` actually kya hai?

Jab tum likhte ho:

```python
async def work():
    await asyncio.sleep(2)
    return "Done"
```

Aur:

```python
coro = work()
```

to `coro` sirf **coroutine object** hai.

Ab:

```python
task = asyncio.create_task(work())
```

to asyncio is coroutine ko **schedule** kar deta hai.

Mental model:

```text
async def work()
       ↓
    function
       ↓
    work()
       ↓
 Coroutine
       ↓
create_task()
       ↓
   Task
       ↓
 Event Loop
```

---

# 2. Task ka result

Task complete hone ke baad:

```python
import asyncio

async def work():
    await asyncio.sleep(1)
    return "AHU data"


async def main():
    task = asyncio.create_task(work())

    result = await task

    print(result)


asyncio.run(main())
```

Output:

```text
AHU data
```

Yahan:

```python
result = await task
```

ka matlab:

> Task complete hone tak asynchronously wait karo aur uska result le lo.

---

# 3. Task ka status

Task ke kuch useful methods hain:

```python
task.done()
task.cancelled()
task.result()
```

Example:

```python
import asyncio

async def work():
    await asyncio.sleep(1)
    return "Complete"


async def main():
    task = asyncio.create_task(work())

    print(task.done())

    result = await task

    print(task.done())
    print(result)


asyncio.run(main())
```

Conceptually output:

```text
False
True
Complete
```

Start mein:

```python
task.done()
```

→ `False`

Complete hone ke baad:

```python
task.done()
```

→ `True`

---

# 4. `task.result()`

Agar task already complete ho:

```python
result = task.result()
```

result mil jata hai.

Example:

```python
task = asyncio.create_task(work())

await task

print(task.result())
```

Lekin agar task abhi complete nahi hua aur tum:

```python
task.result()
```

call kar do, to problem ho sakti hai.

Isliye generally:

```python
result = await task
```

safe/simple approach hai.

---

# 5. `asyncio.gather()`

Pichle lesson mein:

```python
results = await asyncio.gather(
    task1(),
    task2(),
    task3()
)
```

dekha tha.

Example:

```python
import asyncio

async def get_temperature(name):
    await asyncio.sleep(2)
    return f"{name}: 22°C"


async def main():
    results = await asyncio.gather(
        get_temperature("AHU-01"),
        get_temperature("AHU-02"),
        get_temperature("AHU-03")
    )

    print(results)


asyncio.run(main())
```

Output:

```text
[
    'AHU-01: 22°C',
    'AHU-02: 22°C',
    'AHU-03: 22°C'
]
```

Ye API/data collection mein bohat useful pattern hai.

---

# 6. Exception handling

Async function mein normal `try/except` hi use hota hai:

```python
import asyncio

async def work():
    raise ValueError("Sensor error")


async def main():
    try:
        await work()
    except ValueError as e:
        print("Error:", e)


asyncio.run(main())
```

Output:

```text
Error: Sensor error
```

Async hone se `try/except` ka basic concept change nahi hota.

---

# 7. Task mein exception

Example:

```python
import asyncio

async def work():
    raise ValueError("Connection failed")


async def main():
    task = asyncio.create_task(work())

    try:
        await task
    except ValueError as e:
        print("Error:", e)


asyncio.run(main())
```

Yahan exception task ke andar occur hui.

Jab:

```python
await task
```

kiya, exception caller ko mil gayi.

---

# 8. Task cancellation

Kabhi humein running task ko stop karna hota hai.

Example:

```python
import asyncio

async def long_task():
    print("Task started")

    try:
        await asyncio.sleep(10)
        print("Task finished")

    except asyncio.CancelledError:
        print("Task cancelled")


async def main():
    task = asyncio.create_task(long_task())

    await asyncio.sleep(2)

    task.cancel()

    await task


asyncio.run(main())
```

Flow:

```text
Task start
   ↓
10 sec sleep
   ↓
2 sec passed
   ↓
task.cancel()
   ↓
CancelledError
   ↓
cleanup
```

---

# 9. `CancelledError`

Cancellation ke waqt asyncio task ke andar:

```python
asyncio.CancelledError
```

raise karta hai.

Isko handle kar sakte ho:

```python
try:
    ...
except asyncio.CancelledError:
    ...
```

Typical use:

```python
try:
    await something()
finally:
    cleanup()
```

Cancellation ke bawajood cleanup karna important ho sakta hai.

---

# 10. `cancel()` ka important point

Ye:

```python
task.cancel()
```

ka matlab ye nahi:

> "Isi millisecond mein function ko forcefully kill kar do."

Ye task ko cancellation request bhejta hai.

Task jab cancellation point par control deta hai, cancellation process hota hai.

Usually:

```python
await
```

important cancellation point hota hai.

---

# 11. Timeout

Suppose API ko maximum 5 seconds dene hain.

```python
import asyncio

async def api_call():
    await asyncio.sleep(10)
    return "Data"


async def main():
    try:
        result = await asyncio.wait_for(
            api_call(),
            timeout=5
        )
        print(result)

    except asyncio.TimeoutError:
        print("API timeout")


asyncio.run(main())
```

API 10 seconds leti hai.

Humne kaha:

```text
maximum = 5 seconds
```

To result:

```text
API timeout
```

---

# 12. Modern timeout syntax

Modern Python mein:

```python
async with asyncio.timeout(5):
    result = await api_call()
```

Example:

```python
import asyncio

async def api_call():
    await asyncio.sleep(10)
    return "Data"


async def main():
    try:
        async with asyncio.timeout(5):
            result = await api_call()

            print(result)

    except TimeoutError:
        print("Timeout")


asyncio.run(main())
```

Concept:

```text
Start operation
      ↓
5 second limit
      ↓
complete?
   /       \
 yes        no
 ↓          ↓
result    timeout
```

---

# 13. Timeout kyun important hai?

Real-world API:

```text
Your program
      ↓
Internet
      ↓
Server
```

Kabhi server:

* slow ho sakta hai
* unavailable ho sakta hai
* network issue ho sakta hai
* response nahi de sakta

Agar timeout na ho to application unnecessarily wait kar sakti hai.

Isliye:

```python
asyncio.timeout(...)
```

bohat useful hai.

---

# 14. `asyncio.sleep()` vs `time.sleep()`

Ye distinction strongly yaad rakho.

### Wrong pattern inside async code

```python
async def work():
    time.sleep(5)
```

`time.sleep()` event-loop thread ko block kar sakta hai.

### Async pattern

```python
async def work():
    await asyncio.sleep(5)
```

Ab coroutine pause hogi aur event loop doosra task run kar sakta hai.

Diagram:

```text
time.sleep()
    ↓
BLOCK EVENT LOOP


await asyncio.sleep()
    ↓
PAUSE COROUTINE
    ↓
EVENT LOOP FREE
```

---

# 15. Concurrency ≠ Parallelism

Ye bohat important concept hai.

### Concurrency

Multiple tasks progress kar sakte hain:

```text
Task A → wait → Task B → wait → Task A
```

### Parallelism

Multiple computations literally same time CPU cores par execute ho sakti hain:

```text
CPU Core 1 → Task A
CPU Core 2 → Task B
```

`asyncio` primarily:

```text
Concurrency
```

provide karta hai.

Ye automatically CPU parallelism nahi deta.

---

# 16. I/O-bound example

Suppose:

```text
AHU API → 2 sec
VAV API → 2 sec
Sensor API → 2 sec
```

Sequential:

```text
2 + 2 + 2 = ~6 sec
```

Concurrent async:

```text
roughly ~2 sec
```

because waiting periods overlap ho sakte hain.

---

# 17. CPU-bound example

Suppose:

```python
def heavy_calculation():
    for i in range(1_000_000_000):
        ...
```

Asyncio isko automatically 4 CPU cores par divide nahi karega.

CPU-heavy work ke liye usually concepts:

```text
threading
multiprocessing
ProcessPoolExecutor
```

relevant hote hain.

Lekin unko abhi mix nahi karte.

---

# 18. HVAC practical example

Suppose BMS se teen points read karne hain:

```python
import asyncio

async def read_point(point):
    print("Reading", point)

    await asyncio.sleep(2)

    return {
        "point": point,
        "value": 22
    }


async def main():

    results = await asyncio.gather(
        read_point("AHU-01.TEMP"),
        read_point("AHU-02.TEMP"),
        read_point("VAV-01.TEMP")
    )

    for result in results:
        print(result)


asyncio.run(main())
```

Conceptually:

```text
AHU-01.TEMP ─┐
AHU-02.TEMP ─┼→ Event Loop → results
VAV-01.TEMP ─┘
```

Ye pattern future mein API/data engineering work mein bohat useful hoga.

---

# 19. Task lifecycle

Ek task ko roughly:

```text
Created
   ↓
Scheduled
   ↓
Running
   ↓
Waiting
   ↓
Running
   ↓
Completed
```

Ya agar cancel ho:

```text
Running
   ↓
Cancellation requested
   ↓
Cancelled
```

Mental model:

```text
          ┌───────────┐
          │  Created  │
          └─────┬─────┘
                ↓
          ┌───────────┐
          │ Scheduled │
          └─────┬─────┘
                ↓
          ┌───────────┐
          │  Running  │
          └─────┬─────┘
                ↓
          ┌───────────┐
          │  Waiting  │
          └─────┬─────┘
                ↓
          ┌───────────┐
          │ Completed │
          └───────────┘
```

---

# 20. `asyncio.run()` ka role

Normally program ka entry point:

```python
asyncio.run(main())
```

hota hai.

Conceptually:

```text
asyncio.run(main())
       ↓
event loop create
       ↓
main coroutine run
       ↓
async tasks execute
       ↓
main complete
       ↓
event loop close
```

Isliye beginner-level application mein:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

common pattern hai.

---

# 21. Complete example

Ab sab concepts combine karte hain:

```python
import asyncio


async def read_equipment(equipment_id):
    print(f"{equipment_id}: reading...")

    try:
        await asyncio.sleep(2)

        return {
            "equipment_id": equipment_id,
            "temperature": 22
        }

    except asyncio.CancelledError:
        print(f"{equipment_id}: cancelled")
        raise


async def main():

    try:
        async with asyncio.timeout(5):

            results = await asyncio.gather(
                read_equipment("AHU-01"),
                read_equipment("AHU-02"),
                read_equipment("VAV-01")
            )

            for result in results:
                print(result)

    except TimeoutError:
        print("Operation timed out")


if __name__ == "__main__":
    asyncio.run(main())
```

Is example mein:

```text
async def
    ↓
coroutines

await
    ↓
asynchronous waiting

gather()
    ↓
multiple operations

timeout
    ↓
maximum waiting limit

CancelledError
    ↓
cancellation handling

asyncio.run()
    ↓
event loop execution
```

Sab ek hi architecture mein aa gaye.

---

# Quick Revision

```text
Coroutine
→ async def ka result

Task
→ scheduled coroutine

Event Loop
→ tasks ko manage karta hai

await
→ current coroutine ko pause karke event loop ko doosra kaam karne deta hai

gather()
→ multiple async operations ko concurrently wait karta hai

cancel()
→ task ko cancellation request

Timeout
→ operation ke liye maximum time

asyncio
→ Python ka asynchronous programming framework
```

### Ek line mein:

> **Asyncio ka idea ye hai ke program I/O ke wait mein idle na rahe; event loop us waqt doosre ready tasks ko chala sake.**

**Next Lesson 26:** hum **Async Iterator + Async Generator + `async for`** ko deep level par dekhenge, aur phir normal `Iterator/Generator` vs `AsyncIterator/AsyncGenerator` ka exact difference samjhenge.

# Lesson 26: Async Iterator, Async Generator aur `async for`

Pichli lesson mein humne `Task`, `Future`, cancellation aur timeout dekha. Ab hum **normal iteration aur asynchronous iteration** ko connect karte hain.

Sabse pehle basic difference:

```text
Normal Iterator
    ↓
iter()
    ↓
next()
    ↓
StopIteration
```

Async Iterator:

```text
Async Iterator
    ↓
aiter()
    ↓
anext()
    ↓
StopAsyncIteration
```

---

## 1. Normal `for` kaise kaam karta hai?

Tum likhte ho:

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Andar conceptually Python kuch is tarah karta hai:

```python
iterator = iter(numbers)

while True:
    try:
        number = next(iterator)
        print(number)
    except StopIteration:
        break
```

Yani:

```text
for
 ↓
iter()
 ↓
next()
 ↓
next()
 ↓
next()
 ↓
StopIteration
```

---

# 2. Async iteration kyun chahiye?

Suppose data ek local list mein nahi hai.

Data network/API se aa raha hai:

```text
Server
  ↓
data
  ↓
wait
  ↓
next data
  ↓
wait
  ↓
next data
```

Normal iterator blocking ho sakta hai.

Async iterator mein:

```python
async for
```

use karke har asynchronous result ka wait kiya ja sakta hai, bina poore event loop ko unnecessarily block kiye.

---

# 3. `async for`

Basic syntax:

```python
async for item in async_items:
    print(item)
```

Example:

```python
import asyncio

async def numbers():
    for i in range(3):
        await asyncio.sleep(1)
        yield i


async def main():
    async for number in numbers():
        print(number)


asyncio.run(main())
```

Output roughly:

```text
0
1
2
```

Har value ke darmiyan asynchronous wait ho raha hai.

---

# 4. Ye function kya hai?

```python
async def numbers():
    for i in range(3):
        await asyncio.sleep(1)
        yield i
```

Isko kehte hain:

**Async Generator**

Kyun?

Kyunkay ismein dono hain:

```text
async def
+
yield
```

---

# 5. Normal Generator vs Async Generator

### Normal generator

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Use:

```python
for x in numbers():
    print(x)
```

### Async generator

```python
async def numbers():
    yield 1
    yield 2
    yield 3
```

Use:

```python
async for x in numbers():
    print(x)
```

Difference:

| Normal          | Async                |
| --------------- | -------------------- |
| `def`           | `async def`          |
| `yield`         | `yield`              |
| `for`           | `async for`          |
| `next()`        | `anext()`            |
| `StopIteration` | `StopAsyncIteration` |
| synchronous     | asynchronous         |

---

# 6. `__aiter__()` aur `__anext__()`

Normal iterator protocol:

```python
__iter__()
__next__()
```

Async iterator protocol:

```python
__aiter__()
__anext__()
```

Example:

```python
class AsyncCounter:

    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __aiter__(self):
        return self

    async def __anext__(self):

        if self.current >= self.limit:
            raise StopAsyncIteration

        await asyncio.sleep(1)

        value = self.current
        self.current += 1

        return value
```

Use:

```python
async def main():

    async for number in AsyncCounter(3):
        print(number)
```

Output:

```text
0
1
2
```

---

# 7. `__aiter__()`

Ye batata hai:

> "Async iteration ke liye iterator kaun hai?"

Example:

```python
def __aiter__(self):
    return self
```

Yahan object khud async iterator hai.

Conceptually:

```text
async for
    ↓
__aiter__()
    ↓
iterator
```

---

# 8. `__anext__()`

Ye next value provide karta hai.

```python
async def __anext__(self):
    ...
```

Isliye ye asynchronous hai.

Example:

```python
await iterator.__anext__()
```

Agar value available hai:

```text
return value
```

Agar values khatam:

```python
raise StopAsyncIteration
```

---

# 9. `anext()`

Modern Python mein asynchronous iterator se manually next value lene ke liye:

```python
await anext(iterator)
```

Example:

```python
import asyncio

async def main():

    iterator = AsyncCounter(3)

    print(await anext(iterator))
    print(await anext(iterator))
    print(await anext(iterator))


asyncio.run(main())
```

Output:

```text
0
1
2
```

Agar phir:

```python
await anext(iterator)
```

kiya:

```text
StopAsyncIteration
```

aayegi.

---

# 10. `async for` actually kya kar raha hai?

Ye:

```python
async for item in iterator:
    print(item)
```

conceptually kuch is tarah hai:

```python
iterator = aiter(iterator)

while True:
    try:
        item = await anext(iterator)
        print(item)
    except StopAsyncIteration:
        break
```

Ye **bohat important mental model** hai.

Normal:

```text
for
 ↓
next()
```

Async:

```text
async for
 ↓
await anext()
```

---

# 11. Async Generator ka real benefit

Suppose API continuously data de rahi hai.

Agar tum:

```python
await get_all_data()
```

karte ho to ho sakta hai poora data memory mein collect ho.

Async generator:

```python
async for item in get_data():
    process(item)
```

se data **one-by-one** process ho sakta hai.

Mental model:

```text
API
 ↓
item 1 → process
 ↓
item 2 → process
 ↓
item 3 → process
 ↓
item 4 → process
```

Poora dataset ek saath memory mein rakhna zaroori nahi.

---

# 12. HVAC example

Suppose BMS se equipment readings stream ho rahi hain:

```python
import asyncio

async def read_equipment():

    equipment = [
        "AHU-01",
        "AHU-02",
        "VAV-01"
    ]

    for equipment_id in equipment:

        await asyncio.sleep(1)

        yield {
            "equipment_id": equipment_id,
            "temperature": 22
        }
```

Use:

```python
async def main():

    async for data in read_equipment():
        print(data)
```

Output:

```text
{'equipment_id': 'AHU-01', 'temperature': 22}
{'equipment_id': 'AHU-02', 'temperature': 22}
{'equipment_id': 'VAV-01', 'temperature': 22}
```

---

# 13. Async Generator Pipeline

Previous lesson mein normal generator pipeline dekhi thi:

```text
source
 ↓
filter
 ↓
transform
 ↓
output
```

Async version:

```text
API
 ↓
async generator
 ↓
filter
 ↓
transform
 ↓
async consumer
```

Example:

```python
async def numbers():

    for i in range(10):
        await asyncio.sleep(0.1)
        yield i
```

Filter:

```python
async def even_numbers(source):

    async for number in source:

        if number % 2 == 0:
            yield number
```

Consumer:

```python
async def main():

    async for number in even_numbers(numbers()):
        print(number)
```

Output:

```text
0
2
4
6
8
```

Ye **asynchronous pipeline** hai.

---

# 14. Async Generator + `await`

Ek important rule:

Async generator ke andar:

```python
await
```

bhi use kar sakte ho:

```python
async def data():

    result = await get_data()

    yield result
```

Normal generator:

```python
def data():
    result = get_data()
    yield result
```

Async generator:

```python
async def data():
    result = await get_data()
    yield result
```

---

# 15. Normal Generator vs Coroutine vs Async Generator

Ye teen concepts confuse mat karna.

### Generator

```python
def func():
    yield value
```

→ multiple values lazily produce karta hai.

### Coroutine

```python
async def func():
    return value
```

→ asynchronous operation represent karta hai.

### Async Generator

```python
async def func():
    yield value
```

→ asynchronously multiple values produce karta hai.

Table:

| Type            | Syntax               | Use             |
| --------------- | -------------------- | --------------- |
| Generator       | `def + yield`        | lazy values     |
| Coroutine       | `async def + return` | async operation |
| Async Generator | `async def + yield`  | async stream    |

---

# 16. Async Generator ko `await` nahi karte

Ye common mistake hai:

```python
data = await numbers()
```

Agar `numbers()` async generator hai, to directly `await` nahi karte.

Instead:

```python
async for value in numbers():
    ...
```

Kyun?

Because async generator **multiple values** produce karta hai.

Coroutine generally ek result deti hai:

```text
Coroutine
    ↓
await
    ↓
one result
```

Async generator:

```text
Async Generator
    ↓
async for
    ↓
value
    ↓
value
    ↓
value
```

---

# 17. `asyncio` ka complete architecture

Ab tak ke lessons ko connect karo:

```text
                 asyncio
                    │
              Event Loop
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
     Task A       Task B       Task C
       │            │
     await        await
       │            │
       ↓            ↓
    waiting      waiting
```

Aur data stream:

```text
Async Generator
      ↓
 async for
      ↓
  process item
      ↓
  process item
      ↓
  process item
```

---

# 18. Real-world API example

Imagine tum multiple pages API se read kar rahe ho:

```python
async def fetch_pages():

    for page in range(1, 4):

        data = await fetch_api(page)

        yield data
```

Consumer:

```python
async def main():

    async for page_data in fetch_pages():

        process(page_data)
```

Flow:

```text
API Page 1
    ↓
process
    ↓
API Page 2
    ↓
process
    ↓
API Page 3
    ↓
process
```

Ye large datasets ke liye useful architecture hai.

---

# 19. `async for` + timeout

Async iteration ko timeout ke andar bhi run kar sakte ho:

```python
async def main():

    try:
        async with asyncio.timeout(10):

            async for data in read_equipment():
                print(data)

    except TimeoutError:
        print("Reading timeout")
```

Yahan poori operation ko:

```text
10 seconds
```

ka limit diya gaya hai.

---

# 20. Ek bohat important distinction

### Generator

Memory efficient:

```python
def numbers():
    for i in range(1_000_000):
        yield i
```

### Async Generator

Memory efficient **aur asynchronous**:

```python
async def numbers():
    for i in range(1_000_000):
        await asyncio.sleep(0)
        yield i
```

Lekin `async` sirf isliye use nahi karna ke data bohat bada hai.

Reason:

```text
Generator
→ memory efficiency / lazy evaluation

Async Generator
→ lazy evaluation + asynchronous production
```

---

# Final Mental Model

```text
NORMAL
======

Iterable
   ↓
iter()
   ↓
Iterator
   ↓
next()
   ↓
value
   ↓
StopIteration


ASYNC
=====

Async Iterable
   ↓
aiter()
   ↓
Async Iterator
   ↓
await anext()
   ↓
value
   ↓
StopAsyncIteration
```

Aur:

```text
def + yield
    ↓
Generator

async def + return
    ↓
Coroutine

async def + yield
    ↓
Async Generator
```

### Sabse important line:

> **`async for` basically asynchronous version of `for` hai: har next value ko `await` karke receive karta hai, aur event loop ko beech mein doosre tasks run karne ka chance deta hai.**

**Next Lesson 27:** **Decorators** — `@decorator`, function ko wrap karna, `*args/**kwargs`, `functools.wraps`, parameterized decorators, aur phir class decorators.

# Lesson 27: Decorators — `@decorator`

Ab hum Python ke ek bohat important feature par aate hain: **Decorators**.

Decorators ka use tum real Python projects mein bohat dekhoge:

```python
@property
@classmethod
@staticmethod
@abstractmethod
```

Ye sab decorator syntax use karte hain.

---

## 1. Decorator kya hota hai?

Simple definition:

> **Decorator ek function/class ko modify ya enhance karta hai bina uska original code directly change kiye.**

Mental model:

```text
Original Function
       ↓
   Decorator
       ↓
Enhanced Function
```

Example:

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper
```

Ab:

```python
@decorator
def hello():
    print("Hello")
```

Call:

```python
hello()
```

Output:

```text
Before
Hello
After
```

---

# 2. `@decorator` actually kya karta hai?

Ye:

```python
@decorator
def hello():
    print("Hello")
```

conceptually equivalent hai:

```python
def hello():
    print("Hello")

hello = decorator(hello)
```

Ye point **bohat important** hai.

`@decorator` koi magic keyword nahi hai.

Basically:

```text
function
   ↓
decorator(function)
   ↓
new function
   ↓
same name
```

---

# 3. Function bhi object hai

Python mein function bhi object hai:

```python
def hello():
    print("Hello")
```

Tum:

```python
print(hello)
```

kar sakte ho.

Function ko variable mein rakh sakte ho:

```python
x = hello

x()
```

Output:

```text
Hello
```

Isi wajah se function ko doosre function mein pass kar sakte ho.

---

# 4. Function as argument

Example:

```python
def hello():
    print("Hello")


def execute(func):
    func()


execute(hello)
```

Output:

```text
Hello
```

Yahan:

```python
execute(hello)
```

mein `hello` function argument ke taur par pass hua.

Is concept ko kehte hain:

**Higher-order function**

---

# 5. Basic decorator

Ab:

```python
def decorator(func):

    def wrapper():
        print("Before function")

        func()

        print("After function")

    return wrapper
```

Use:

```python
@decorator
def hello():
    print("Hello")
```

Call:

```python
hello()
```

Output:

```text
Before function
Hello
After function
```

Flow:

```text
hello()
   ↓
wrapper()
   ↓
Before
   ↓
original hello()
   ↓
After
```

---

# 6. `wrapper` ka role

Decorator ke andar:

```python
def wrapper():
```

ek replacement function hai.

Original:

```python
hello()
```

ab internally:

```text
wrapper()
   ↓
func()
```

ban gaya.

Isliye wrapper original function ke around additional behavior add karta hai.

---

# 7. Practical example: Logging

Suppose tum dekhna chahte ho ke kaunsa function run hua.

```python
def logger(func):

    def wrapper():
        print("Running:", func.__name__)
        return func()

    return wrapper
```

Use:

```python
@logger
def check_temperature():
    print("Temperature checked")
```

Call:

```python
check_temperature()
```

Output:

```text
Running: check_temperature
Temperature checked
```

Ye real applications mein logging ke basic concept jaisa hai.

---

# 8. Problem: Function ke arguments

Ab suppose:

```python
def add(a, b):
    return a + b
```

Agar hum simple decorator use karein:

```python
def decorator(func):

    def wrapper():
        return func()

    return wrapper
```

To:

```python
@decorator
def add(a, b):
    return a + b
```

call:

```python
add(10, 20)
```

problem hogi.

Kyun?

Kyunkay:

```python
wrapper()
```

arguments accept nahi kar raha.

---

# 9. `*args` aur `**kwargs`

Generic decorator banane ke liye:

```python
def decorator(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

Ab:

```python
@decorator
def add(a, b):
    return a + b
```

Use:

```python
print(add(10, 20))
```

Output:

```text
30
```

---

# 10. `*args` kya kar raha hai?

Agar:

```python
add(10, 20)
```

to wrapper:

```python
wrapper(10, 20)
```

receive karega.

```python
def wrapper(*args):
```

mein:

```python
args = (10, 20)
```

banega.

Phir:

```python
func(*args)
```

tuple ko unpack karega:

```python
func(10, 20)
```

---

# 11. `**kwargs`

Agar:

```python
add(a=10, b=20)
```

to:

```python
kwargs = {
    "a": 10,
    "b": 20
}
```

Aur:

```python
func(**kwargs)
```

banega:

```python
func(a=10, b=20)
```

Isliye generic decorator mein:

```python
def wrapper(*args, **kwargs):
```

bohat common hai.

---

# 12. Return value preserve karna

Decorator mein:

```python
return func(*args, **kwargs)
```

important hai.

Example:

```python
def logger(func):

    def wrapper(*args, **kwargs):

        print("Calling function")

        result = func(*args, **kwargs)

        print("Function complete")

        return result

    return wrapper
```

Agar:

```python
@logger
def add(a, b):
    return a + b
```

to:

```python
result = add(10, 20)

print(result)
```

Output:

```text
Calling function
Function complete
30
```

---

# 13. `functools.wraps`

Ek important problem hai.

Decorator ke baad:

```python
add.__name__
```

kabhi:

```text
wrapper
```

return kar sakta hai.

Kyun?

Kyunkay `add` ab wrapper function ban chuka hai.

Solution:

```python
from functools import wraps
```

Then:

```python
def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print("Calling:", func.__name__)

        return func(*args, **kwargs)

    return wrapper
```

Ab:

```python
@logger
def add(a, b):
    return a + b
```

`add.__name__` properly:

```text
add
```

rahega.

---

# 14. `@wraps` kya karta hai?

Simple:

```text
Original function ki metadata
          ↓
      @wraps
          ↓
Wrapper mein preserve
```

Metadata mein important cheezen:

```text
__name__
__doc__
```

etc.

Isliye production decorators mein:

```python
@wraps(func)
```

use karna good practice hai.

---

# 15. Decorator with timing

Ab useful real-world example.

```python
import time
from functools import wraps


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(
            f"{func.__name__} took {end - start:.4f} seconds"
        )

        return result

    return wrapper
```

Use:

```python
@timer
def calculate():
    time.sleep(2)
    return 100
```

Then:

```python
result = calculate()
```

Output approximately:

```text
calculate took 2.0001 seconds
```

Function ka original code:

```python
def calculate():
    time.sleep(2)
    return 100
```

change nahi hua.

Decorator ne external behavior add kar diya.

---

# 16. Multiple decorators

Ek function par multiple decorators ho sakte hain:

```python
@decorator1
@decorator2
def hello():
    print("Hello")
```

Important:

Ye conceptually:

```python
hello = decorator1(
            decorator2(
                hello
            )
        )
```

ke equivalent hai.

Yani **bottom decorator pehle apply hota hai**.

Flow:

```text
hello
 ↓
decorator2
 ↓
decorator1
```

---

# 17. Decorator with parameters

Ab advanced part.

Suppose tum chahte ho:

```python
@repeat(3)
def hello():
    print("Hello")
```

Yahan `repeat` ko `3` mil raha hai.

```python
def repeat(times):

    def decorator(func):

        def wrapper(*args, **kwargs):

            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator
```

Use:

```python
@repeat(3)
def hello():
    print("Hello")
```

Output:

```text
Hello
Hello
Hello
```

---

# 18. Ismein 3 levels kyun hain?

Ye initially confusing hota hai.

```python
def repeat(times):          # 1
```

Ye decorator configuration hai.

```python
def decorator(func):        # 2
```

Ye actual function receive karta hai.

```python
def wrapper(*args, **kwargs):  # 3
```

Ye function ko actually run karta hai.

Structure:

```text
repeat(3)
   ↓
decorator
   ↓
wrapper
   ↓
original function
```

Isko yaad rakho:

```text
Decorator with arguments
        ↓
Decorator factory
        ↓
Decorator
        ↓
Wrapper
```

---

# 19. HVAC example

Suppose BMS equipment command ko log karna hai:

```python
from functools import wraps


def log_command(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print("Command:", func.__name__)

        result = func(*args, **kwargs)

        print("Command completed")

        return result

    return wrapper
```

Use:

```python
class AHU:

    @log_command
    def start(self):
        print("AHU started")

    @log_command
    def stop(self):
        print("AHU stopped")
```

Call:

```python
ahu = AHU()

ahu.start()
```

Output:

```text
Command: start
AHU started
Command completed
```

Yahan original `start()` ka code same raha.

Decorator ne:

```text
logging
```

add kar di.

---

# 20. Decorator vs Inheritance

Ye difference important hai.

### Inheritance

```python
class AHU(Equipment):
```

Relationship:

```text
AHU IS-A Equipment
```

### Decorator

```python
@log_command
def start():
```

Relationship:

```text
start function
     ↓
extra behavior
```

Decorator ka purpose generally:

```text
existing behavior ko wrap/enhance karna
```

Inheritance ka purpose:

```text
class relationship + reuse/extension
```

---

# 21. Decorator vs `@property`

Tumne pehle:

```python
@property
def salary(self):
    ...
```

dekha tha.

Ab samajh aa raha hai ke:

```python
@property
```

bhi decorator syntax hai.

Conceptually:

```python
salary = property(salary)
```

Yani decorator function ko receive karta hai aur modified object return karta hai.

Isi tarah:

```python
@classmethod
def create(...):
```

conceptually:

```python
create = classmethod(create)
```

Aur:

```python
@staticmethod
def calculate(...):
```

conceptually:

```python
calculate = staticmethod(calculate)
```

---

# 22. Decorator ka powerful use

Real Python applications mein decorators commonly use hote hain:

```text
Logging
Authentication
Authorization
Caching
Timing
Validation
Retry
Transaction management
Routing
Permission checks
```

Example:

```python
@authenticated
def delete_equipment():
    ...
```

Conceptually:

```text
User
 ↓
authenticated
 ↓
allowed?
 ├── No → reject
 └── Yes
      ↓
delete_equipment()
```

---

# 23. Decorator ka golden mental model

Sabse important structure:

```python
def decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Before

        result = func(*args, **kwargs)

        # After

        return result

    return wrapper
```

Aur usage:

```python
@decorator
def function(...):
    ...
```

Meaning:

```text
function
   ↓
decorator(function)
   ↓
wrapper
   ↓
function()
```

---

# Quick Revision

```text
Decorator
→ function/class ko wrap ya enhance karta hai

@decorator
→ decorator(function)

wrapper
→ original function ke around behavior

*args
→ positional arguments

**kwargs
→ keyword arguments

@wraps
→ original function ki metadata preserve karta hai

Decorator factory
→ decorator ko parameters dene ka pattern
```

### Ek line mein:

> **Decorator ka core idea hai: existing function ko replace kiye baghair uske around additional behavior add karna.**

**Next Lesson 28:** **Class Decorators + `__call__()`** — function decorator se class decorator tak jayenge, samjhenge ke object ko callable kaise banate hain, aur phir `@decorator` ke andar actual execution flow ko deeply trace karenge.

# Lesson 28: Class Decorators + `__call__()`

Ab hum decorators ko next level par lete hain.

Pichli lesson mein:

```python
@decorator
def hello():
    ...
```

dekha tha.

Ab hum dekhenge:

1. **Class decorator**
2. `__call__()`
3. Object ko function ki tarah call karna
4. Function decorator aur class decorator ka relation
5. Practical HVAC example
6. Decorator class ke andar state maintain karna

---

# 1. `__call__()` kya hai?

Normal object:

```python
class Employee:
    pass

emp = Employee()
```

Agar:

```python
emp()
```

likho to normally error aayega:

```text
TypeError: 'Employee' object is not callable
```

Lekin agar class mein:

```python
def __call__(self):
    ...
```

define kar do, to object ko function ki tarah call kar sakte ho.

Example:

```python
class Employee:

    def __call__(self):
        print("Employee called")


emp = Employee()

emp()
```

Output:

```text
Employee called
```

---

# 2. Mental model

Ye:

```python
emp()
```

conceptually:

```python
emp.__call__()
```

hai.

Bilkul waise hi jaise:

```python
len(obj)
```

→

```python
obj.__len__()
```

aur:

```python
obj == other
```

→

```python
obj.__eq__(other)
```

Aur:

```python
obj()
```

→

```python
obj.__call__()
```

---

# 3. `__call__()` with arguments

```python
class Calculator:

    def __call__(self, a, b):
        return a + b


calc = Calculator()

print(calc(10, 20))
```

Output:

```text
30
```

Yahan:

```python
calc(10, 20)
```

actually:

```python
calc.__call__(10, 20)
```

hai.

---

# 4. Object + state + callable behavior

`__call__()` ka ek major benefit ye hai ke object apni state maintain kar sakta hai.

Example:

```python
class Counter:

    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count


counter = Counter()

print(counter())
print(counter())
print(counter())
```

Output:

```text
1
2
3
```

Object ke andar:

```text
count = 0
   ↓
counter()
   ↓
count = 1
   ↓
counter()
   ↓
count = 2
```

---

# 5. Function vs callable object

Normal function:

```python
def add(a, b):
    return a + b
```

Call:

```python
add(10, 20)
```

Callable object:

```python
class Add:

    def __call__(self, a, b):
        return a + b
```

Call:

```python
add = Add()

add(10, 20)
```

Dono ka interface same:

```text
add(10, 20)
```

Lekin second case mein `add` ek **object** hai.

---

# 6. Callable kya hota hai?

Python mein check kar sakte ho:

```python
callable(add)
```

Example:

```python
def hello():
    pass

print(callable(hello))
```

Output:

```text
True
```

Class instance:

```python
class Test:

    def __call__(self):
        pass


obj = Test()

print(callable(obj))
```

Output:

```text
True
```

Agar `__call__()` nahi hai:

```python
class Test:
    pass

obj = Test()

print(callable(obj))
```

Output:

```text
False
```

---

# 7. Ab class decorator

Ab tak function decorator:

```python
def decorator(func):
    ...
```

Ab class ko decorator ki tarah use karte hain.

Example:

```python
def add_logging(cls):

    cls.logged = True

    return cls
```

Use:

```python
@add_logging
class Employee:
    pass
```

Ye:

```python
@add_logging
class Employee:
    pass
```

conceptually:

```python
class Employee:
    pass

Employee = add_logging(Employee)
```

---

# 8. Class decorator class ko modify karta hai

Example:

```python
def add_company(cls):

    cls.company = "ABC"

    return cls


@add_company
class Employee:
    pass


emp = Employee()

print(emp.company)
```

Output:

```text
ABC
```

Decorator ne class mein:

```python
company
```

add kar diya.

---

# 9. Class decorator vs function decorator

### Function decorator

```python
@logger
def start():
    ...
```

Function ko modify/wrap karta hai.

### Class decorator

```python
@register
class AHU:
    ...
```

Class ko modify/register karta hai.

Comparison:

```text
Function decorator
        ↓
    function

Class decorator
        ↓
      class
```

---

# 10. Practical: Equipment registration

Suppose HVAC system mein equipment classes register karni hain.

```python
equipment_registry = {}
```

Decorator:

```python
def register_equipment(cls):

    equipment_registry[cls.__name__] = cls

    return cls
```

Now:

```python
@register_equipment
class AHU:
    pass


@register_equipment
class VAV:
    pass
```

Registry:

```python
print(equipment_registry)
```

Conceptually:

```text
{
    "AHU": <class AHU>,
    "VAV": <class VAV>
}
```

Yani class create hote hi automatically registry mein register ho gayi.

---

# 11. Ye real frameworks mein kyun useful hai?

Large systems mein manually:

```python
registry["AHU"] = AHU
registry["VAV"] = VAV
registry["Pump"] = Pump
```

karna inconvenient ho sakta hai.

Decorator:

```python
@register
class AHU:
    ...
```

se class automatically register ho sakti hai.

Ye pattern frameworks aur plugin systems mein common hai.

---

# 12. Class decorator with modification

Example:

```python
def add_status(cls):

    def status(self):
        return f"{self.__class__.__name__} is running"

    cls.status = status

    return cls
```

Use:

```python
@add_status
class AHU:
    pass
```

Ab:

```python
ahu = AHU()

print(ahu.status())
```

Output:

```text
AHU is running
```

Decorator ne class ke andar method add kar diya.

---

# 13. Class decorator jo class wrap kare

Class decorator sirf class modify nahi karta; class ko replace bhi kar sakta hai.

Example:

```python
def decorate(cls):

    class Wrapper:
        def __init__(self, *args, **kwargs):
            print("Creating object")
            self.obj = cls(*args, **kwargs)

        def __getattr__(self, name):
            return getattr(self.obj, name)

    return Wrapper
```

Use:

```python
@decorate
class Employee:

    def __init__(self, name):
        self.name = name
```

Then:

```python
emp = Employee("Ali")

print(emp.name)
```

Flow:

```text
Employee
   ↓
class decorator
   ↓
Wrapper
   ↓
Wrapper object
   ↓
original Employee object
```

Ye thora advanced pattern hai.

---

# 14. `__call__()` + decorator

Ab dono concepts combine karte hain.

Class ko decorator banaya ja sakta hai:

```python
class Logger:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Before")
        result = self.func(*args, **kwargs)
        print("After")
        return result
```

Use:

```python
@Logger
def hello():
    print("Hello")
```

Remember:

```python
@Logger
def hello():
    ...
```

means:

```python
hello = Logger(hello)
```

Ab `hello` function nahi raha.

Ab:

```text
hello
 ↓
Logger object
```

Lekin Logger object ke paas:

```python
__call__()
```

hai.

Isliye:

```python
hello()
```

work karta hai.

---

# 15. Ye internally kaise work karta hai?

Code:

```python
class Logger:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Before")

        result = self.func(*args, **kwargs)

        print("After")

        return result
```

Decorator:

```python
@Logger
def hello():
    print("Hello")
```

Actually:

```python
hello = Logger(hello)
```

Ab:

```python
hello()
```

actually:

```python
hello.__call__()
```

Then:

```python
self.func()
```

original `hello()` execute karta hai.

Flow:

```text
original hello()
      ↓
Logger(hello)
      ↓
Logger object
      ↓
hello()
      ↓
Logger.__call__()
      ↓
self.func()
      ↓
original hello()
```

**Ye decorator architecture ka bohat important pattern hai.**

---

# 16. Class-based decorator with arguments

Ab:

```python
@Logger("START")
def hello():
    print("Hello")
```

Ismein class:

```python
class Logger:

    def __init__(self, message):
        self.message = message

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            print(self.message)
            return func(*args, **kwargs)

        return wrapper
```

Use:

```python
@Logger("Running function")
def hello():
    print("Hello")
```

Output:

```text
Running function
Hello
```

Yahan thora different structure hai:

```text
Logger("Running function")
        ↓
Logger object
        ↓
__call__(hello)
        ↓
wrapper
```

---

# 17. Function decorator vs class-based decorator

### Function-based

```python
def logger(func):

    def wrapper(*args, **kwargs):
        ...
        return func(*args, **kwargs)

    return wrapper
```

### Class-based

```python
class Logger:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        ...
        return self.func(*args, **kwargs)
```

Class-based decorator ka benefit:

```text
state maintain kar sakta hai
```

Example:

```python
class Counter:

    def __init__(self, func):
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print("Calls:", self.calls)
        return self.func(*args, **kwargs)
```

Use:

```python
@Counter
def hello():
    print("Hello")
```

Call:

```python
hello()
hello()
hello()
```

Output:

```text
Calls: 1
Hello
Calls: 2
Hello
Calls: 3
Hello
```

Yahan decorator object ne state maintain ki:

```python
self.calls
```

---

# 18. `functools.update_wrapper`

Class-based decorators mein ek issue ye hai ke metadata automatically preserve nahi hoti.

Isliye:

```python
from functools import update_wrapper
```

use kiya ja sakta hai.

Example:

```python
class Logger:

    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print("Calling:", self.func.__name__)
        return self.func(*args, **kwargs)
```

Ab original function ki metadata decorator object par copy ho sakti hai.

---

# 19. HVAC practical example

Suppose har BMS command ka count maintain karna hai:

```python
class CommandCounter:

    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):

        self.count += 1

        print(
            f"{self.func.__name__} called {self.count} time(s)"
        )

        return self.func(*args, **kwargs)
```

Use:

```python
class AHU:

    @CommandCounter
    def start(self):
        print("AHU started")
```

Then:

```python
ahu = AHU()

ahu.start()
ahu.start()
```

Output:

```text
start called 1 time(s)
AHU started

start called 2 time(s)
AHU started
```

Yahan decorator object har call ka state maintain kar raha hai.

---

# 20. `__call__()` ka broader use

`__call__()` sirf decorators ke liye nahi hai.

Machine-learning style:

```python
model(input_data)
```

often internally callable object ho sakta hai.

Validation:

```python
validator(value)
```

Configuration:

```python
config(key)
```

Pipeline:

```python
processor(data)
```

Yani:

```text
Object
+
__call__()
=
Function-like Object
```

---

# 21. Callable object vs function

Function:

```python
def square(x):
    return x * x
```

Callable class:

```python
class Square:

    def __call__(self, x):
        return x * x
```

Dono:

```python
square(5)
```

aur:

```python
Square()(5)
```

jaisa interface de sakte hain.

Lekin class-based version state maintain kar sakta hai:

```python
class Square:

    def __init__(self):
        self.calls = 0

    def __call__(self, x):
        self.calls += 1
        return x * x
```

---

# 22. Ek important connection

Tumne Lesson 10 mein:

```python
__call__()
```

dekha tha.

Ab decorator lesson mein iska actual use samajh aa gaya:

```text
__call__()
   ↓
object ko callable banata hai
   ↓
class-based decorator possible
```

Aur:

```text
@Logger
def hello():
```

actually:

```text
hello = Logger(hello)
```

Isliye `hello()` chalane ke liye:

```python
Logger.__call__()
```

important hai.

---

# Final mental model

```text
                 DECORATOR
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
   Function decorator    Class decorator
          │                   │
          ↓                   ↓
       wrapper             class modify
                              or
                           class replace


Class-based decorator
        ↓
   __init__(func)
        ↓
   store function
        ↓
    __call__()
        ↓
   execute function
```

### Sabse important 4 lines:

```python
@Logger
def hello():
    ...
```

means:

```python
hello = Logger(hello)
```

Then:

```python
hello()
```

means effectively:

```python
hello.__call__()
```

Aur `__call__()` ke andar:

```python
self.func(...)
```

original function execute karta hai.

**Next Lesson 29:** **Closures + `nonlocal`** — decorator ke andar `wrapper` ko outer function ke variables kaise milte hain, closure actually kya hota hai, aur decorator aur closure ka deep connection.

# Lesson 29: Closures + `nonlocal`

Ab hum decorators ke **andar ka اصل mechanism** samjhenge.

Pichli lesson mein humne dekha:

```python
@Logger
def hello():
    ...
```

aur function decorators mein:

```python
def decorator(func):

    def wrapper():
        return func()

    return wrapper
```

Sawal ye hai:

> `wrapper()` ke andar `func` available kaise rehta hai, jab `decorator()` already finish ho chuka hota hai?

Iska jawab hai:

**Closure.**

---

# 1. Closure kya hota hai?

Simple definition:

> **Closure ek inner function hota hai jo apne outer function ke variables ko yaad rakhta hai, even jab outer function finish ho chuka ho.**

Example:

```python
def outer():
    message = "Hello"

    def inner():
        print(message)

    return inner
```

Ab:

```python
func = outer()
func()
```

Output:

```text
Hello
```

Interesting part:

```python
outer()
```

already finish ho gaya.

Phir bhi:

```python
func()
```

ke andar:

```python
message
```

available hai.

Ye **closure** hai.

---

# 2. Isko step-by-step dekho

Code:

```python
def outer():
    message = "Hello"

    def inner():
        print(message)

    return inner
```

Flow:

```text
outer()
   ↓
message = "Hello"
   ↓
inner function create
   ↓
inner return
   ↓
outer finish
```

Ab:

```python
func = outer()
```

`func` ke paas `inner` function hai.

Aur `inner` apne surrounding environment se:

```text
message = "Hello"
```

ko remember karta hai.

Phir:

```python
func()
```

→ `Hello`

---

# 3. Closure ke 3 important parts

Closure ke liye generally:

```text
Outer function
      ↓
Local variable
      ↓
Inner function
      ↓
Inner function uses outer variable
```

Example:

```python
def multiplier(x):

    def multiply(value):
        return value * x

    return multiply
```

Yahan:

```python
x
```

outer variable hai.

Aur:

```python
multiply()
```

us `x` ko use kar raha hai.

---

# 4. Multiple closures

Ab interesting example:

```python
def multiplier(x):

    def multiply(value):
        return value * x

    return multiply
```

Create:

```python
double = multiplier(2)
triple = multiplier(3)
```

Ab:

```python
print(double(10))
print(triple(10))
```

Output:

```text
20
30
```

Mental model:

```text
multiplier(2)
   ↓
double
   ↓
remembers x = 2


multiplier(3)
   ↓
triple
   ↓
remembers x = 3
```

Yani har closure ka apna captured environment ho sakta hai.

---

# 5. Closure + decorator

Ab pichli lesson ka decorator dekho:

```python
def logger(func):

    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)

    return wrapper
```

Yahan:

```python
func
```

outer function ka variable hai.

Aur:

```python
wrapper()
```

usko use kar raha hai.

Therefore:

```text
logger()
   ↓
func captured
   ↓
wrapper returned
   ↓
logger finished
   ↓
wrapper still remembers func
```

**Ye decorator ka closure mechanism hai.**

---

# 6. Exactly kya remember hota hai?

Example:

```python
def logger(func):

    def wrapper():
        print("Function:", func.__name__)
        return func()

    return wrapper
```

`wrapper` remember karta hai:

```text
func
```

Ye `func` closure ka **free variable** hai.

Tum inspect bhi kar sakte ho:

```python
print(wrapper.__closure__)
```

Agar closure hai to Python internal closure information show karega.

---

# 7. `__closure__`

Example:

```python
def outer():
    x = 10

    def inner():
        return x

    return inner


func = outer()

print(func.__closure__)
```

`__closure__` closure ke captured values se related information provide karta hai.

Aur:

```python
func.__code__.co_freevars
```

se free variable names dekh sakte ho.

Example:

```python
print(func.__code__.co_freevars)
```

Conceptually:

```text
('x',)
```

Yani `x` outer scope se aa raha hai.

---

# 8. `nonlocal` kyun chahiye?

Ab important problem.

Suppose:

```python
def counter():

    count = 0

    def increment():
        count += 1
        return count

    return increment
```

Ye error dega.

Kyun?

Python `increment()` ke andar:

```python
count += 1
```

ko assignment samajhta hai.

Yani Python assume karta hai:

```text
count
→ local variable
```

Lekin `count` actually outer function ka variable hai.

---

# 9. `nonlocal`

Is problem ka solution:

```python
def counter():

    count = 0

    def increment():

        nonlocal count

        count += 1

        return count

    return increment
```

Ab:

```python
counter_fn = counter()

print(counter_fn())
print(counter_fn())
print(counter_fn())
```

Output:

```text
1
2
3
```

`nonlocal` ka matlab:

> "Ye variable current function ka local variable nahi; nearest enclosing function ka variable hai."

---

# 10. `nonlocal` vs `global`

Ye dono confuse mat karna.

### `nonlocal`

Outer function ke variable ko modify karta hai:

```python
def outer():

    x = 10

    def inner():
        nonlocal x
        x += 1
```

Scope:

```text
global
  ↓
outer
  ↓
inner
```

`nonlocal`:

```text
inner → outer
```

---

### `global`

Module/global scope ke variable ko modify karta hai:

```python
x = 10

def change():

    global x

    x += 1
```

Scope:

```text
global
  ↑
function
```

---

# 11. `nonlocal` ka mental model

```text
GLOBAL
  │
  └── outer()
        │
        │ x = 10
        │
        └── inner()
              │
              │ nonlocal x
              ↓
           modify outer x
```

---

# 12. Closure as state

Closures ka ek powerful use:

> **Private state maintain karna.**

Example:

```python
def counter():

    count = 0

    def increment():

        nonlocal count

        count += 1

        return count

    return increment
```

Use:

```python
counter1 = counter()
counter2 = counter()

print(counter1())
print(counter1())

print(counter2())
print(counter2())
```

Output:

```text
1
2
1
2
```

Why?

Because:

```text
counter1
→ apna count

counter2
→ apna count
```

Dono independent closures hain.

---

# 13. Closure vs Class

Same functionality class se bhi bana sakte ho.

### Closure

```python
def counter():

    count = 0

    def increment():

        nonlocal count

        count += 1
        return count

    return increment
```

### Class

```python
class Counter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count
```

Dono:

```python
counter()
```

ya:

```python
counter.increment()
```

se state maintain karte hain.

Difference:

```text
Closure
→ function + captured state

Class
→ object + attributes + methods
```

---

# 14. HVAC example

Suppose tum equipment readings ka count maintain karna chahte ho:

```python
def create_reader(equipment_id):

    count = 0

    def read():

        nonlocal count

        count += 1

        print(
            equipment_id,
            "reading number:",
            count
        )

    return read
```

Create:

```python
ahu_reader = create_reader("AHU-01")
vav_reader = create_reader("VAV-01")
```

Run:

```python
ahu_reader()
ahu_reader()

vav_reader()
```

Output:

```text
AHU-01 reading number: 1
AHU-01 reading number: 2
VAV-01 reading number: 1
```

Har reader ka apna state hai.

---

# 15. Closure + configuration

Ye pattern bhi bohat useful hai:

```python
def create_validator(minimum):

    def validate(value):

        return value >= minimum

    return validate
```

Create:

```python
temperature_validator = create_validator(18)
pressure_validator = create_validator(100)
```

Use:

```python
print(temperature_validator(22))
print(temperature_validator(15))
```

Output:

```text
True
False
```

Yahan:

```text
temperature_validator
→ remembers minimum = 18
```

---

# 16. Decorator with configuration = Closure

Pichli lesson mein humne:

```python
@repeat(3)
def hello():
    ...
```

dekha tha.

Uska implementation:

```python
def repeat(times):

    def decorator(func):

        def wrapper(*args, **kwargs):

            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    return decorator
```

Ab clearly dekho:

```text
repeat(times)
      ↓
decorator(func)
      ↓
wrapper()
```

`wrapper()` ko dono values chahiye:

```text
times
func
```

Aur dono outer scopes se aa rahe hain.

Isliye ye nested functions **closure** create karte hain.

---

# 17. `nonlocal` decorator example

Ab ek decorator jo function calls count kare:

```python
from functools import wraps


def count_calls(func):

    count = 0

    @wraps(func)
    def wrapper(*args, **kwargs):

        nonlocal count

        count += 1

        print("Call:", count)

        return func(*args, **kwargs)

    return wrapper
```

Use:

```python
@count_calls
def start_ahu():
    print("AHU started")
```

Then:

```python
start_ahu()
start_ahu()
start_ahu()
```

Output:

```text
Call: 1
AHU started

Call: 2
AHU started

Call: 3
AHU started
```

Yahan `count` function calls ke darmiyan preserve ho raha hai.

---

# 18. Closure vs global variable

Bad/simple approach:

```python
count = 0

def increment():
    global count
    count += 1
```

Problem:

```text
global state
→ kahin se bhi modify ho sakta hai
```

Closure:

```python
def counter():

    count = 0

    def increment():

        nonlocal count
        count += 1

        return count

    return increment
```

Ab `count` directly bahar accessible nahi.

```text
Outside
   ↓
increment()
   ↓
captured count
```

Ye state ko encapsulate karne ka ek tareeqa hai.

---

# 19. Closure aur Encapsulation

Tumne pehle **encapsulation** padha tha.

Class mein:

```python
class Counter:

    def __init__(self):
        self._count = 0
```

Closure mein:

```python
def counter():

    count = 0
```

`count` directly outer code se accessible nahi.

Yani closure bhi limited/private-like state create kar sakta hai.

Lekin class zyada structured hoti hai jab multiple operations/state chahiye.

---

# 20. `nonlocal` kab use hota hai?

Jab:

```text
Current function
       ↓
outer function ka variable
       ↓
modify karna hai
```

Use:

```python
nonlocal variable
```

Example:

```python
def outer():

    value = 10

    def inner():

        nonlocal value
        value += 5

    return inner
```

Agar sirf read karna hai:

```python
def outer():

    value = 10

    def inner():
        return value
```

to `nonlocal` ki zaroorat nahi.

`nonlocal` mainly **rebinding/modification** ke liye hai.

---

# 21. `nonlocal` vs mutable object

Ek interesting Python detail:

```python
def outer():

    data = []

    def inner():
        data.append(10)
```

Yahan `nonlocal` nahi chahiye.

Kyun?

`data` variable ko reassign nahi kar rahe:

```text
data → same list
```

sirf list mutate kar rahe ho:

```python
data.append(10)
```

Lekin:

```python
data = [10]
```

karoge to `nonlocal data` chahiye hoga.

Important distinction:

```text
Mutation
→ object ko change karna

Rebinding
→ variable ko naye object se bind karna
```

---

# 22. Closure ka complete flow

Example:

```python
def power(exponent):

    def calculate(number):
        return number ** exponent

    return calculate
```

Then:

```python
square = power(2)
cube = power(3)
```

Flow:

```text
power(2)
   ↓
exponent = 2
   ↓
calculate created
   ↓
square
   ↓
remembers exponent = 2
```

And:

```text
power(3)
   ↓
exponent = 3
   ↓
calculate created
   ↓
cube
   ↓
remembers exponent = 3
```

Then:

```python
square(5)
```

→ `25`

```python
cube(5)
```

→ `125`

---

# 23. Closure ka relation decorators se

Ye connection yaad rakho:

```text
Nested Function
       ↓
Outer variable ko capture karta hai
       ↓
Closure
       ↓
Decorator ke wrapper ko state/context milta hai
```

Isliye decorators samajhne ke liye closures important hain.

---

# Quick Revision

```text
Closure
→ inner function + captured outer variables

nonlocal
→ nearest enclosing function ke variable ko modify karo

global
→ module/global variable ko modify karo

Nested function
→ function ke andar function

Decorator
→ closure ka common practical use

Captured variable
→ outer scope ka variable jo inner function remember karta hai
```

### Sabse important example:

```python
def counter():

    count = 0

    def increment():

        nonlocal count
        count += 1

        return count

    return increment
```

```python
c = counter()

print(c())  # 1
print(c())  # 2
print(c())  # 3
```

Yahan `counter()` finish hone ke baad bhi `count` zinda rehta hai, kyunki `increment()` us value ko **closure ke through capture** karta hai.

**Next Lesson 30:** **Scope aur LEGB Rule** — Local, Enclosing, Global, Built-in; Python variable ko exactly kis order mein search karta hai, aur `global`/`nonlocal` ka LEGB se exact connection.

# Python Scope aur LEGB Rule

**Scope** ka matlab hai:

> Python mein kisi variable ka **naam kahan accessible hai** aur Python us naam ko **kahan search karega**.

Example:

```python
x = 10

def test():
    print(x)

test()
```

Output:

```text
10
```

`test()` ke andar `x` directly define nahi hai, isliye Python bahar search karta hai.

Isi searching ka rule hai:

# LEGB

```text
L → Local
E → Enclosing
G → Global
B → Built-in
```

Python kisi name ko normally isi order mein search karta hai:

```text
Local
  ↓
Enclosing
  ↓
Global
  ↓
Built-in
```

---

# 1. L = Local Scope

Local ka matlab:

> Variable current function ke andar bana hai.

```python
def employee():
    name = "Ali"
    print(name)

employee()
```

Yahan:

```python
name = "Ali"
```

`employee()` ka **local variable** hai.

Ye bahar accessible nahi:

```python
def employee():
    name = "Ali"

employee()

print(name)
```

Error:

```text
NameError
```

Kyun?

```text
name
 ↓
sirf employee() ke local scope mein
```

---

# 2. E = Enclosing Scope

Ye tab hota hai jab **function ke andar function** ho.

Example:

```python
def outer():

    x = 10

    def inner():
        print(x)

    inner()

outer()
```

`inner()` ke andar:

```python
print(x)
```

Python pehle Local scope mein `x` dhoondta hai.

Nahi mila.

Phir **Enclosing scope** mein jata hai:

```text
inner()
   ↓
Local → x nahi
   ↓
outer() → x mil gaya
```

Output:

```text
10
```

---

# 3. Enclosing ka simple diagram

```text
Global
  │
  └── outer()
        │
        │ x = 10
        │
        └── inner()
              │
              │ print(x)
              ↓
           x = 10
```

Yahan `outer()` ka scope `inner()` ke liye **Enclosing Scope** hai.

---

# 4. Closure se connection

Pichli lesson mein humne closure dekha tha:

```python
def outer():

    x = 10

    def inner():
        return x

    return inner
```

`inner()`:

```python
return x
```

kar raha hai.

`x` Local nahi hai.

Python:

```text
L → x nahi
E → x mil gaya
```

Isi enclosing variable ko inner function capture kar sakta hai.

---

# 5. G = Global Scope

Function ke bahar, module/file level par variable:

```python
x = 100

def test():
    print(x)

test()
```

Output:

```text
100
```

Yahan:

```python
x = 100
```

global scope mein hai.

Function ke andar `x` nahi mila:

```text
L → nahi
E → nahi
G → mil gaya
```

---

# 6. B = Built-in Scope

Agar Local, Enclosing aur Global mein bhi name nahi mila, Python **Built-in scope** mein search karta hai.

Example:

```python
def test():
    print(len([1, 2, 3]))

test()
```

`len` humne define nahi kiya.

Python:

```text
L → len nahi
E → len nahi
G → len nahi
B → len mil gaya
```

`len()` Python ka built-in function hai.

Examples:

```python
print()
len()
sum()
max()
min()
str()
int()
list()
dict()
```

Ye built-in namespace mein available hote hain.

---

# 7. Complete LEGB example

```python
x = "Global"

def outer():

    x = "Enclosing"

    def inner():

        x = "Local"

        print(x)

    inner()

outer()
```

Output:

```text
Local
```

Kyun?

Python `inner()` ke andar `x` search karta hai:

```text
L → x mil gaya
```

Isliye baaki scopes tak jane ki zaroorat nahi.

---

# 8. Local remove kar do

```python
x = "Global"

def outer():

    x = "Enclosing"

    def inner():

        print(x)

    inner()

outer()
```

Ab:

```text
L → x nahi
E → x mil gaya
```

Output:

```text
Enclosing
```

---

# 9. Enclosing bhi remove kar do

```python
x = "Global"

def outer():

    def inner():

        print(x)

    inner()

outer()
```

Ab:

```text
L → nahi
E → nahi
G → mil gaya
```

Output:

```text
Global
```

---

# 10. Global bhi remove kar do

```python
def outer():

    def inner():

        print(len([1, 2, 3]))

    inner()

outer()
```

`len`:

```text
L → nahi
E → nahi
G → nahi
B → mil gaya
```

Output:

```text
3
```

---

# 11. LEGB ka complete example

```python
x = "Global"

def outer():

    x = "Enclosing"

    def inner():

        x = "Local"

        print(x)

    inner()

outer()
```

Search:

```text
inner()
   ↓
Local
   ↓
x = "Local"
```

Python yahin stop kar deta hai.

---

# 12. Name lookup vs variable assignment

Yahan ek **bohat important difference** hai.

Read karna:

```python
print(x)
```

aur assign karna:

```python
x = 20
```

same nahi hain.

Example:

```python
x = 10

def test():
    print(x)

test()
```

Output:

```text
10
```

Lekin:

```python
x = 10

def test():
    x = 20
    print(x)

test()

print(x)
```

Output:

```text
20
10
```

Kyun?

Function ke andar:

```python
x = 20
```

ne **new local variable** bana diya.

Global `x` change nahi hua.

---

# 13. Ye beginners ke liye bohat important rule hai

Function ke andar:

```python
x = value
```

likhne par Python normally `x` ko **local variable** treat karta hai.

Example:

```python
x = 10

def test():
    x = 20
```

Ye global `x` ko update nahi karta.

---

# 14. `global` keyword

Agar tum intentionally global variable modify karna chahte ho:

```python
x = 10

def test():

    global x

    x = 20

test()

print(x)
```

Output:

```text
20
```

`global x` Python ko batata hai:

> Is function mein `x` local nahi, global `x` hai.

---

# 15. `global` kyun chahiye?

Ye code:

```python
x = 10

def test():
    x = 20
```

mein:

```text
x = 20
```

local variable create karta hai.

Lekin:

```python
x = 10

def test():
    global x
    x = 20
```

mein:

```text
x = 20
```

global variable ko rebind karta hai.

---

# 16. `nonlocal`

Ab enclosing scope.

```python
def outer():

    x = 10

    def inner():

        nonlocal x
        x = 20

    inner()

    print(x)


outer()
```

Output:

```text
20
```

`inner()` ne `outer()` ke `x` ko modify kiya.

```text
Global
  ↓
outer()
  x = 10
  ↓
inner()
  nonlocal x
  ↓
outer ka x = 20
```

---

# 17. `global` vs `nonlocal`

Ye table yaad rakho:

| Keyword    | Kis scope ko target karta hai? |
| ---------- | ------------------------------ |
| Nothing    | Local                          |
| `nonlocal` | Enclosing function             |
| `global`   | Global/module                  |

Example:

```python
x = 100

def outer():

    x = 50

    def inner():

        nonlocal x
        x = 20

    inner()
    print(x)

outer()
```

Output:

```text
20
```

Global:

```text
100
```

Enclosing:

```text
20
```

---

# 18. `UnboundLocalError`

Ye Python ka ek bohat important scope error hai.

Example:

```python
x = 10

def test():

    print(x)

    x = 20

test()
```

Tum soch sakte ho:

> Pehle global `x` print hoga, phir local `x` banega.

Lekin Python isko aise interpret karta hai:

```text
test()
 ↓
x assignment exists
 ↓
Python x ko local treat karta hai
 ↓
print(x)
 ↓
local x abhi value-less
```

Result:

```text
UnboundLocalError
```

---

# 19. Ye kyun hota hai?

Function ke andar:

```python
x = 20
```

ki wajah se Python compile-time par `x` ko local variable recognize karta hai.

Isliye:

```python
print(x)
```

global `x` nahi leta.

Mental model:

```text
def test():

    print(x)   ← local x?
    
    x = 20     ← yes, local assignment
```

Isliye error.

---

# 20. `global` se solve

Agar tum global `x` use karna chahte ho:

```python
x = 10

def test():

    global x

    print(x)
    x = 20

test()
```

Output:

```text
10
```

Ab `x` explicitly global hai.

---

# 21. Scope aur `if` / `for`

Python mein `if` aur `for` normally **new scope create nahi karte**.

Example:

```python
if True:
    x = 10

print(x)
```

Output:

```text
10
```

Similarly:

```python
for i in range(3):
    x = i

print(x)
```

Output:

```text
2
```

Yahan `x` function scope/module scope mein hi rahta hai.

---

# 22. Function scope different hai

```python
def test():

    x = 10

test()

print(x)
```

Error:

```text
NameError
```

Kyun?

`def` ek new local scope create karta hai.

---

# 23. Class scope thora different hai

Classes ka scope normal function scope jaisa nahi behave karta.

Example:

```python
class Employee:

    company = "ABC"

    def show(self):
        print(company)
```

`show()` ke andar directly `company` normally class namespace se LEGB ke `E` level par nahi milta.

Usually:

```python
self.company
```

ya:

```python
Employee.company
```

use karte hain.

Ye distinction important hai:

```text
Function nesting
→ Enclosing scope

Class body
→ normal enclosing function scope nahi
```

---

# 24. `self` scope nahi hai

Ye bhi clear kar lo.

```python
class Employee:

    def __init__(self, name):
        self.name = name
```

`self` koi special scope nahi.

`self` simply ek **local parameter** hai.

Conceptually:

```python
Employee.__init__(employee_object, "Ali")
```

Isliye:

```text
self
↓
Local variable / parameter
```

Aur:

```python
self.name
```

object ke attribute ko access karta hai.

---

# 25. Built-in shadowing

Global scope mein:

```python
len = 100
```

ab:

```python
print(len([1, 2, 3]))
```

problem karega.

Kyun?

LEGB:

```text
L → len nahi
E → nahi
G → len = 100  ← mil gaya
B → yahan nahi gaya
```

Isliye Python built-in `len()` tak nahi pohoncha.

Ye kehlata hai:

**Shadowing**

---

# 26. Shadowing example

```python
x = "Global"

def test():

    x = "Local"

    print(x)

test()
```

Output:

```text
Local
```

Local `x` ne global `x` ko shadow kar diya.

```text
Global x
    ↓
shadowed
    ↑
Local x
```

---

# 27. Built-in ko shadow karna avoid karo

Bad:

```python
list = [1, 2, 3]
```

Phir:

```python
list("ABC")
```

problem karega.

Similarly avoid names like:

```text
list
dict
str
int
sum
len
input
id
```

as your own variables/functions, especially broad scopes mein.

---

# 28. LEGB + Closure + Decorator

Ab pichli 2 lessons connect karo.

```python
def decorator(func):

    message = "Running"

    def wrapper():

        print(message)
        return func()

    return wrapper
```

`wrapper()` ke andar:

### `message`

```text
L → nahi
E → message mil gaya
```

### `func`

```text
L → nahi
E → func mil gaya
```

Isliye closure work karta hai.

---

# 29. Complete LEGB diagram

```text
                 Built-in
                    ↑
                 Global
                    ↑
               Enclosing
                    ↑
                  Local
                    ↑
                 current
                function
```

Python name lookup:

```text
L
↓
E
↓
G
↓
B
↓
NameError
```

Agar kisi level par name mil gaya:

```text
STOP
```

---

# 30. Real example

```python
company = "Global Company"

def outer():

    company = "Facility Company"

    def employee():

        company = "HVAC Company"

        print(company)

    employee()

outer()
```

Output:

```text
HVAC Company
```

Search:

```text
employee()
    ↓
Local
    ↓
"HVAC Company"
```

Agar local remove:

```python
def employee():
    print(company)
```

then:

```text
Local → no
Enclosing → "Facility Company"
```

Agar enclosing bhi remove:

```text
Global → "Global Company"
```

---

# 31. LEGB ka practical debugging method

Jab Python bole:

```text
NameError: name 'x' is not defined
```

to manually check:

```text
1. Local mein x hai?
2. Enclosing function mein x hai?
3. Global mein x hai?
4. Built-in mein x hai?
```

Agar kahin nahi:

```text
NameError
```

---

# 32. Scope ka golden rule

Ye 5 points yaad rakho:

```text
1. Function new local scope banata hai.

2. Nested function enclosing scope ko access kar sakta hai.

3. Function ke bahar module-level names global scope mein hote hain.

4. Python missing name ko L → E → G → B order mein search karta hai.

5. Assignment function ke andar normally local binding create karta hai.
```

---

# Final Mental Model

```text
                Python Name Lookup

                       x
                       ↓
                  ┌────────┐
                  │ Local  │
                  └───┬────┘
                      │ no
                      ↓
                ┌───────────┐
                │ Enclosing │
                └─────┬─────┘
                      │ no
                      ↓
                 ┌────────┐
                 │ Global │
                 └───┬────┘
                     │ no
                     ↓
                ┌──────────┐
                │ Built-in │
                └────┬─────┘
                     │ no
                     ↓
                 NameError
```

Aur:

```text
global
→ Global scope ko modify/rebind karo

nonlocal
→ Enclosing function ka variable modify/rebind karo

LEGB
→ Python name ko search karne ka order
```

### Ek line mein:

> **Scope batata hai variable kahan accessible hai; LEGB batata hai Python kisi name ko dhoondte waqt kis order mein scopes check karega.**
