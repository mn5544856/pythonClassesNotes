Bilkul. Ab **Lesson 58** exactly isi topic se start karte hain:

# Lesson 61 — `Generic` + `TypeVar` + `Protocol` + Variance

### Practical Architecture — Basic se Advanced

Is lesson ka goal sirf syntax yaad karna nahi hai. Hum samjhenge ke ye 4 concepts **mil kar type-safe architecture** kaise banate hain.

---

## 1. Sabse pehle problem samjho

Maan lo hamare paas ek function hai:

```python
def get_first(items):
    return items[0]
```

Ye kaam karega:

```python
print(get_first([10, 20, 30]))
```

Result:

```text
10
```

Aur:

```python
print(get_first(["Ali", "Ahmed"]))
```

Result:

```text
Ali
```

Runtime par koi problem nahi.

Lekin type checker ko kya pata hai?

Agar hum likhein:

```python
def get_first(items: list) -> object:
    return items[0]
```

toh type information weak ho gayi.

Hum chahte hain:

```text
list[int]    → int
list[str]    → str
list[User]   → User
```

Yahan se **Generic + TypeVar** ka concept shuru hota hai.

---

# 2. `TypeVar` kya hai?

`TypeVar` ka matlab simple language mein:

> **"Ek aisa type placeholder jo baad mein actual type ban jayega."**

Example:

```python
from typing import TypeVar

T = TypeVar("T")
```

Yahan:

```text
T
```

koi actual type nahi hai.

Ye placeholder hai.

Ab:

```python
def get_first(items: list[T]) -> T:
    return items[0]
```

Yahan relationship ban gayi:

```text
input ka element type
        ↓
        T
        ↓
output ka type
```

Agar:

```python
list[int]
```

di:

```text
T = int
```

Result:

```text
int
```

Agar:

```python
list[str]
```

di:

```text
T = str
```

Result:

```text
str
```

---

# 3. Iska actual faida

Without `TypeVar`:

```python
def get_first(items: list) -> object:
    ...
```

Type checker ko sirf pata:

```text
output = object
```

With `TypeVar`:

```python
T = TypeVar("T")

def get_first(items: list[T]) -> T:
    return items[0]
```

Type checker samajhta hai:

```text
list[int] → int
list[str] → str
list[float] → float
```

Yani `T` **input aur output ke darmiyan relationship preserve** kar raha hai.

---

# 4. `Generic` kya karta hai?

Ab `TypeVar` ko class ke saath use karte hain.

```python
from typing import Generic, TypeVar

T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

Ab:

```python
int_box = Box[int](100)
```

Conceptually:

```text
Box[T]

T = int

↓
 
Box[int]
```

Aur:

```python
name_box = Box[str]("Ali")
```

Conceptually:

```text
Box[T]

T = str

↓

Box[str]
```

---

# 5. `Generic[T]` ka matlab

Ye:

```python
class Box(Generic[T]):
```

ka matlab hai:

> `Box` ek generic class hai jo kisi type `T` ke saath kaam kar sakti hai.

Isliye:

```python
Box[int]
Box[str]
Box[float]
Box[User]
```

sab possible hain.

---

# 6. Generic class ka practical example

Maan lo API response system banana hai.

```python
from typing import Generic, TypeVar

T = TypeVar("T")


class Response(Generic[T]):
    def __init__(self, data: T):
        self.data = data

    def get_data(self) -> T:
        return self.data
```

Ab:

```python
response = Response[int](200)
```

Toh:

```python
response.get_data()
```

ka type:

```text
int
```

Aur:

```python
response = Response[str]("Success")
```

mein:

```python
response.get_data()
```

ka type:

```text
str
```

---

# 7. Ab `Protocol` add karte hain

Yahan architecture interesting hoti hai.

Suppose hum kehte hain:

> Mujhe aisi cheez chahiye jo `save()` method provide kare.

Hum inheritance force nahi karna chahte.

```python
from typing import Protocol


class Savable(Protocol):
    def save(self) -> None:
        ...
```

Ab:

```python
class User:
    def save(self) -> None:
        print("User saved")
```

`User` ne:

```python
Savable
```

inherit nahi kiya.

Phir bhi `User` compatible hai.

Isko kehte hain:

> **Structural typing**

---

# 8. Structural typing vs inheritance

Traditional inheritance:

```python
class User(Savable):
    ...
```

Yahan explicit relationship hai.

Protocol mein:

```python
class User:
    def save(self) -> None:
        ...
```

Agar required structure match karta hai, type checker compatible samajh sakta hai.

Simple rule:

```text
Inheritance:
"I am a Savable."

Protocol:
"I behave like a Savable."
```

Ye Python architecture mein bohat powerful hai.

---

# 9. Generic + Protocol

Ab dono ko combine karte hain.

Suppose humein repository chahiye:

```text
Repository[User]
Repository[Equipment]
Repository[Order]
```

Pehle:

```python
from typing import Protocol, TypeVar, Generic

T = TypeVar("T")


class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...
    
    def get(self) -> T:
        ...
```

Ab koi actual implementation:

```python
class UserRepository:
    def save(self, item: User) -> None:
        print("Saving user")

    def get(self) -> User:
        return User()
```

Conceptually:

```text
Repository[T]

T = User

↓

Repository[User]
```

---

# 10. Lekin yahan ek important problem hai

`T` kis direction mein use ho raha hai?

Repository mein:

```python
save(item: T)
```

`T` **input** hai.

Aur:

```python
get() -> T
```

`T` **output** hai.

Yani same `T`:

```text
input + output
```

mein use ho raha hai.

Ab variance ka concept aata hai.

---

# 11. Variance kya hai?

Variance basically ye determine karta hai:

> Generic type ke relationships ke andar subtype relationships kis direction mein allowed hain?

Teen types:

```text
Covariance
Contravariance
Invariance
```

Is lesson mein architecture ke context mein inhe samjho.

---

# 12. Covariance

Covariance mein direction same rehti hai.

Maan lo:

```text
Dog
  ↓
Animal
```

Dog, Animal ka subtype hai.

Covariant generic:

```text
Box[Dog]
   ↓
Box[Animal]
```

Conceptually:

```text
Dog → Animal

Box[Dog] → Box[Animal]
```

Yani same direction.

---

# 13. Covariance kab useful hai?

Jab generic object primarily **data produce** karta ho.

Example:

```python
from typing import TypeVar, Generic

T_co = TypeVar("T_co", covariant=True)


class Producer(Generic[T_co]):
    def get(self) -> T_co:
        ...
```

Ye:

```text
Producer[T]
```

data produce kar raha hai.

Example:

```text
Producer[Dog]
```

Dog produce karega.

Agar system ko `Animal` chahiye, toh Dog producer conceptually safe ho sakta hai because:

```text
Dog is an Animal
```

---

# 14. Contravariance

Ab direction ulat jaati hai.

```text
Dog → Animal
```

Lekin generic relationship:

```text
Consumer[Animal]
      ↓
Consumer[Dog]
```

Conceptually.

Kyun?

Because consumer **input leta hai**.

Example:

```python
T_contra = TypeVar(
    "T_contra",
    contravariant=True
)


class Consumer(Generic[T_contra]):
    def consume(self, item: T_contra) -> None:
        ...
```

Agar consumer:

```text
Animal
```

consume kar sakta hai, toh obviously:

```text
Dog
```

bhi consume kar sakta hai.

---

# 15. Real-life example

Suppose:

```python
class Animal:
    pass


class Dog(Animal):
    pass
```

Animal handler:

```python
class AnimalHandler:
    def handle(self, animal: Animal):
        print("Handling animal")
```

Ye Dog ko bhi handle kar sakta hai:

```python
dog = Dog()

handler.handle(dog)
```

Isliye input-oriented abstraction mein contravariance useful hoti hai.

---

# 16. Invariance

Invariance mein automatic substitution nahi hoti.

Example:

```text
Dog → Animal
```

Lekin:

```text
Box[Dog] ✕ Box[Animal]
```

aur:

```text
Box[Animal] ✕ Box[Dog]
```

dono automatically compatible nahi.

Mutable containers ke case mein ye especially important hai.

Imagine:

```python
dogs: list[Dog]
```

Agar Python allow kar de:

```python
animals: list[Animal] = dogs
```

toh:

```python
animals.append(Cat())
```

ab original `dogs` list mein `Cat` aa jayegi.

Ye unsafe hai.

Isi wajah se:

```text
list[Dog]
```

aur:

```text
list[Animal]
```

invariant relationship rakhte hain.

---

# 17. Generic + Protocol + Variance together

Ab actual architecture.

Suppose hum notification system bana rahe hain.

```python
from typing import Protocol, TypeVar, Generic


T_co = TypeVar(
    "T_co",
    covariant=True
)


class Producer(Protocol[T_co]):
    def produce(self) -> T_co:
        ...
```

Email message:

```python
class Email:
    pass
```

Producer:

```python
class EmailProducer:
    def produce(self) -> Email:
        return Email()
```

Architecture:

```text
Producer[T]
     │
     └── T = Email
```

Yani:

```text
Producer[Email]
```

---

# 18. Input architecture

Ab consumer:

```python
T_contra = TypeVar(
    "T_contra",
    contravariant=True
)


class Consumer(Protocol[T_contra]):
    def consume(self, item: T_contra) -> None:
        ...
```

Example:

```python
class MessageConsumer:
    def consume(self, item: object) -> None:
        print("Processing message")
```

Ye broad input accept karta hai.

Agar application ko kisi specific subtype ka consumer chahiye, broad consumer ka behavior useful ho sakta hai.

---

# 19. Covariant + Contravariant ko ek diagram mein dekho

```text
              Animal
             /      \
           Dog      Cat


Producer:

Producer[Dog]
     ↓
Producer[Animal]

SAME DIRECTION
= covariance
```

Consumer:

```text
Consumer[Animal]
     ↓
Consumer[Dog]

OPPOSITE DIRECTION
= contravariance
```

Aur invariant:

```text
Box[Dog]  ✕  Box[Animal]
```

---

# 20. `Generic` aur `Protocol` mein difference

Ye distinction bohat important hai.

### `Generic`

Focus:

> **Type parameterization**

Example:

```python
class Box(Generic[T]):
    ...
```

Meaning:

```text
Box[int]
Box[str]
Box[User]
```

---

### `Protocol`

Focus:

> **Required behavior/interface**

Example:

```python
class Savable(Protocol):
    def save(self) -> None:
        ...
```

Meaning:

```text
Mujhe farq nahi padta class ka naam kya hai.

Bas save() hona chahiye.
```

---

# 21. Dono ko combine kyun karte hain?

Because real architecture mein humein dono requirements hoti hain:

```text
Behavior bhi define karna hai
        +
Type bhi preserve karna hai
```

Example:

```python
T = TypeVar("T")


class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...

    def get(self) -> T:
        ...
```

Ab repository:

```text
Repository[User]
Repository[Order]
Repository[Equipment]
```

ban sakti hai.

---

# 22. Practical architecture

Maan lo facility management system hai.

Entities:

```python
class Equipment:
    ...


class WorkOrder:
    ...


class Employee:
    ...
```

Generic repository:

```python
T = TypeVar("T")


class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...

    def get(self, item_id: str) -> T:
        ...
```

Ab:

```text
Repository[Equipment]
Repository[WorkOrder]
Repository[Employee]
```

same abstraction use kar sakte hain.

Architecture:

```text
                  Repository[T]
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
Repository[Equipment]  Repository[WorkOrder]  Repository[Employee]
```

Ye **code reuse + type safety + loose coupling** provide karta hai.

---

# 23. Loose coupling ka actual faida

Suppose function:

```python
def process_equipment(
    repo: Repository[Equipment]
):
    equipment = repo.get("AHU-001")
    ...
```

Function ko ye nahi pata:

```text
Database?
API?
Google Sheets?
SQL?
File?
Memory?
```

Usko sirf pata:

```text
Repository[Equipment]
```

required hai.

Aap implementation change kar sakte ho:

```text
SQLRepository
APIRepository
MockRepository
GoogleSheetsRepository
```

jab tak required protocol satisfy karta hai.

Ye **Dependency Inversion / Dependency Injection style architecture** ke saath bohat useful hai.

---

# 24. TypeVar bounded bhi ho sakta hai

Ab advanced part.

```python
T = TypeVar("T", bound=Equipment)
```

Iska matlab:

```text
T koi bhi type ho sakta hai
lekin Equipment ka subtype hona chahiye.
```

Example:

```python
class Equipment:
    pass


class AHU(Equipment):
    pass


class Refrigerator(Equipment):
    pass
```

Valid:

```text
T = AHU
T = Refrigerator
```

Invalid conceptually:

```text
T = Employee
```

because:

```text
Employee
```

`Equipment` ka subtype nahi.

---

# 25. Bounded TypeVar vs constrained TypeVar

Ye advanced distinction yaad rakhna.

### Bound

```python
T = TypeVar("T", bound=Animal)
```

Meaning:

```text
Animal ya Animal ka subtype
```

---

### Constraints

```python
T = TypeVar("T", int, str)
```

Meaning:

```text
sirf int ya str
```

Yani:

```text
bound:
"family ke andar koi bhi subtype"

constraints:
"specified options mein se"
```

---

# 26. Generic + bound

Example:

```python
T = TypeVar(
    "T",
    bound=Equipment
)


class EquipmentRepository(Generic[T]):

    def save(self, equipment: T) -> None:
        print("Saving equipment")
```

Ab:

```python
class AHU(Equipment):
    pass
```

Then:

```python
repo = EquipmentRepository[AHU]()
```

valid architecture hai.

---

# 27. `Protocol` + Generic + Bound

Aur bhi powerful:

```python
T = TypeVar(
    "T",
    bound=Equipment
)


class Repository(Protocol[T]):

    def save(self, item: T) -> None:
        ...

    def get(self, item_id: str) -> T:
        ...
```

Ab protocol ke users ko guarantee milti hai:

```text
Repository
   ↓
sirf Equipment family ke types
```

---

# 28. Ek complete practical architecture

```python
from typing import Protocol, TypeVar, Generic


class Equipment:
    def __init__(self, equipment_id: str):
        self.equipment_id = equipment_id


class AHU(Equipment):
    pass


class Refrigerator(Equipment):
    pass


T = TypeVar("T", bound=Equipment)


class Repository(Protocol[T]):

    def save(self, item: T) -> None:
        ...

    def get(self, item_id: str) -> T:
        ...


class InMemoryRepository(Generic[T]):

    def __init__(self):
        self.items: dict[str, T] = {}

    def save(self, item: T) -> None:
        self.items[item.equipment_id] = item

    def get(self, item_id: str) -> T:
        return self.items[item_id]
```

Ab:

```python
ahu_repo = InMemoryRepository[AHU]()
```

Aur:

```python
ahu = AHU("AHU-001")

ahu_repo.save(ahu)

result = ahu_repo.get("AHU-001")
```

Type checker ke perspective se:

```text
ahu_repo
    ↓
InMemoryRepository[AHU]

get()
    ↓
AHU
```

Ye exactly woh benefit hai jo simple `Any` based code nahi de sakta.

---

# 29. `Any` vs Generic

Bad architecture:

```python
def get(self) -> Any:
    ...
```

`Any` basically type checker ko keh deta hai:

> "Is type ko check mat karo."

Generic:

```python
T = TypeVar("T")

def get(self) -> T:
    ...
```

kehta hai:

> "Actual type preserve karo."

Isliye large applications mein generic abstraction zyada precise hoti hai.

---

# 30. Lesson 58 ka complete mental model

Is poore lesson ko is architecture ki tarah yaad rakho:

```text
                         Type System
                              │
              ┌───────────────┴───────────────┐
              │                               │
          TypeVar                          Protocol
              │                               │
       type relationship                behavior/interface
              │                               │
              └──────────────┬────────────────┘
                             │
                          Generic
                             │
                    reusable abstraction
                             │
                          Variance
                             │
              ┌──────────────┼──────────────┐
              │              │              │
          Covariant      Contravariant   Invariant
              │              │              │
           output           input        input/output
```

### Ek line mein:

**`TypeVar`** → type ko represent karta hai
**`Generic`** → class/function ko type-parameterized banata hai
**`Protocol`** → required behavior define karta hai
**Covariance** → producer/output side
**Contravariance** → consumer/input side
**Invariance** → automatic substitution nahi
**`bound`** → TypeVar ko ek type family tak restrict karta hai

---

## Sabse important practical pattern

Agar aap architecture design kar rahe ho, toh ye pattern bohat powerful hai:

```python
T = TypeVar("T", bound=BaseModel)


class Repository(Protocol[T]):
    def save(self, item: T) -> None:
        ...

    def get(self, id: str) -> T:
        ...
```

Phir:

```text
Repository[User]
Repository[Equipment]
Repository[WorkOrder]
Repository[Invoice]
```

Aur implementation interchangeable reh sakti hai.

**Yehi Generic + TypeVar + Protocol ka real architectural purpose hai:** reusable abstraction banani, implementation se coupling kam karni, aur static type information ko end-to-end preserve karna.
Bilkul. Ab numbering ke hisaab se **Lesson 62** karte hain.

# Lesson 62 — `TypeGuard` + `TypeIs` + Type Narrowing

Is lesson ka main goal ye samajhna hai:

> **Python type checker ko kaise batayein ke kisi condition ke baad variable ka type aur specific ho gaya hai.**

Ye topic especially useful hai jab aap:

* `isinstance()` jaisi custom checking kar rahe ho
* `list[object]` ko `list[str]` jaisa narrow karna chahte ho
* Generic code likh rahe ho
* `Protocol` ke saath runtime checks kar rahe ho
* complex data validation kar rahe ho

---

# 1. Pehle Type Narrowing samjho

Maan lo:

```python
def process(value: int | str):
    ...
```

Yahan `value` do types mein se koi bhi ho sakta hai:

```text
int
OR
str
```

Ab:

```python
def process(value: int | str):

    if isinstance(value, int):
        print(value + 10)
```

`if` ke andar type checker samajhta hai:

```text
value: int
```

Aur `else` mein:

```python
else:
    print(value.upper())
```

yahan:

```text
value: str
```

Ye hai:

> **Type Narrowing**

---

# 2. Narrowing ka matlab

Initially:

```python
value: int | str
```

Condition:

```python
isinstance(value, int)
```

ke baad:

```text
True branch:

int
```

aur:

```text
False branch:

str
```

Diagram:

```text
int | str
    │
    ├── isinstance(..., int)
    │
    ├── True  → int
    │
    └── False → str
```

Yani type checker possibilities ko kam kar raha hai.

---

# 3. Problem: custom function

Ab hum `isinstance()` directly use nahi karna chahte.

Suppose:

```python
def is_string(value):
    return isinstance(value, str)
```

Phir:

```python
def process(value: int | str):

    if is_string(value):
        print(value.upper())
```

Runtime par code sahi hai.

Lekin static type checker ko necessarily pata nahi chalega ke:

```python
is_string(value) == True
```

ka matlab:

```text
value is str
```

hai.

Yahan `TypeGuard` kaam aata hai.

---

# 4. `TypeGuard`

Import:

```python
from typing import TypeGuard
```

Ab:

```python
def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

Important part:

```python
TypeGuard[str]
```

Ye type checker ko batata hai:

> Agar function `True` return kare, toh argument ko `str` samjho.

---

# 5. Example

```python
from typing import TypeGuard


def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)


def process(value: object):

    if is_string(value):
        print(value.upper())
```

`if` ke andar:

```text
value: str
```

ho gaya.

Isliye:

```python
value.upper()
```

valid hai.

---

# 6. `TypeGuard` ka mental model

Normal function:

```python
def is_string(value: object) -> bool:
```

sirf keh raha hai:

```text
True / False
```

Type checker ko type information nahi milti.

Lekin:

```python
def is_string(value: object) -> TypeGuard[str]:
```

keh raha hai:

```text
True
 ↓
value is str
```

Yani:

```text
bool
```

ke comparison mein:

```text
TypeGuard[str]
```

**type information bhi carry karta hai.**

---

# 7. Important: `TypeGuard` runtime mein kya karta hai?

Ye bohat important hai.

`TypeGuard` khud runtime par koi magical checking nahi karta.

Ye:

```python
TypeGuard[str]
```

runtime par `str` conversion nahi karta.

Aapko actual condition khud likhni hoti hai:

```python
return isinstance(value, str)
```

`TypeGuard` primarily **static type checker ke liye signal** hai.

---

# 8. `TypeGuard` ka powerful example: list

Ab interesting case.

Suppose:

```python
items: list[object]
```

Aur hum check karna chahte hain:

> Kya is list ke saare elements strings hain?

```python
from typing import TypeGuard


def is_str_list(
    items: list[object]
) -> TypeGuard[list[str]]:

    return all(
        isinstance(item, str)
        for item in items
    )
```

Ab:

```python
items: list[object] = [
    "Ali",
    "Ahmed",
    "Nouman"
]
```

Then:

```python
if is_str_list(items):
    for item in items:
        print(item.upper())
```

Inside `if`:

```text
items: list[str]
```

ho gaya.

---

# 9. TypeGuard ka sabse important use-case

Ye:

```python
list[object]
```

ko:

```python
list[str]
```

narrow kar sakta hai.

Diagram:

```text
list[object]
      │
      │ is_str_list()
      ↓
 list[str]
```

Ye simple `isinstance()` se possible nahi hota in the same way for the whole generic container.

---

# 10. Generic TypeGuard

Ab Lesson 58 ke `TypeVar` ko bhi connect karte hain.

```python
from typing import TypeGuard, TypeVar

T = TypeVar("T")
```

Suppose:

```python
def is_non_empty(
    items: list[T]
) -> TypeGuard[list[T]]:
    return len(items) > 0
```

Yahan `T` preserve ho raha hai.

Agar:

```python
numbers: list[int] = [1, 2, 3]
```

toh:

```text
T = int
```

Aur result conceptually:

```text
TypeGuard[list[int]]
```

---

# 11. Ab `TypeIs`

Modern Python typing mein doosra important tool hai:

```python
TypeIs
```

Import:

```python
from typing import TypeIs
```

Example:

```python
def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

Surface syntax similar hai:

```python
TypeGuard[str]
```

vs

```python
TypeIs[str]
```

Lekin **semantic difference bohat important hai.**

---

# 12. `TypeGuard` vs `TypeIs`

Basic distinction:

### `TypeGuard`

True branch:

```text
input type → specified type
```

False branch ko TypeGuard same tarah narrow nahi karta.

### `TypeIs`

True branch:

```text
input type → intersection with target
```

False branch:

```text
input type → target ko exclude karke remainder
```

Yani `TypeIs` **dono branches ko narrow kar sakta hai**.

---

# 13. Simple example

```python
from typing import TypeIs


def is_string(value: int | str) -> TypeIs[str]:
    return isinstance(value, str)
```

Ab:

```python
def process(value: int | str):

    if is_string(value):
        print(value.upper())
    else:
        print(value + 10)
```

Type checker samajhta hai:

```text
Initial:
int | str

       │
       │ is_string()
       ↓

True:
str

False:
int
```

Ye `TypeIs` ka powerful part hai.

---

# 14. `TypeGuard` mein difference

```python
from typing import TypeGuard


def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

True branch mein:

```text
str
```

milta hai.

Lekin `TypeGuard` ka semantics ye guarantee nahi deta ke false branch mein:

```text
object - str
```

automatically narrow ho kar exact type ban jaye.

---

# 15. TypeIs ko mathematical way mein samjho

Suppose:

```text
Input = int | str
Target = str
```

`TypeIs[str]`:

### True

```text
(int | str) ∩ str
=
str
```

### False

```text
(int | str) - str
=
int
```

Isliye:

```text
True  → str
False → int
```

---

# 16. TypeGuard mein aisa zaroori nahi

`TypeGuard` ka basic contract:

```text
True
 ↓
specified target type
```

Yani:

```text
TypeGuard[T]
```

ka main focus positive branch hai.

---

# 17. Ek important example

```python
from typing import TypeGuard


def is_int(value: object) -> TypeGuard[int]:
    return isinstance(value, int)
```

Use:

```python
def calculate(value: object):

    if is_int(value):
        print(value + 100)
```

True branch:

```text
value: int
```

Ye straightforward hai.

---

# 18. TypeIs ke liye input compatibility

`TypeIs` ka use karte waqt target type aur input type ke darmiyan logical compatibility honi chahiye.

Example:

```python
def is_string(value: int | str) -> TypeIs[str]:
    ...
```

Yahan `str`, input union ka part hai.

Isliye narrowing meaningful hai.

Concept:

```text
Input possibilities:

int
str

Target:

str
```

---

# 19. `TypeGuard` ka ek surprising feature

`TypeGuard` target type input type ka subtype hona **zaroori nahi** hota.

Example conceptual:

```python
def is_str_list(
    value: list[object]
) -> TypeGuard[list[str]]:
    ...
```

Ye allowed pattern hai.

Kyun?

Because:

```text
list[object]
```

aur:

```text
list[str]
```

invariant hain.

Phir bhi custom guard manually guarantee kar raha hai:

```text
"maine actual contents check kiye hain"
```

---

# 20. Isi wajah se TypeGuard powerful hai

Aap runtime validation ko static typing information se connect kar sakte ho.

Example:

```python
def is_valid_equipment_list(
    items: list[object]
) -> TypeGuard[list[Equipment]]:

    return all(
        isinstance(item, Equipment)
        for item in items
    )
```

Ab:

```python
items: list[object]
```

se:

```python
if is_valid_equipment_list(items):
```

ke baad:

```text
items: list[Equipment]
```

---

# 21. `TypeGuard` + Protocol

Ab Lesson 58 se connection.

Suppose:

```python
from typing import Protocol


class Savable(Protocol):
    def save(self) -> None:
        ...
```

Runtime check:

```python
def is_savable(value: object) -> TypeGuard[Savable]:
    return hasattr(value, "save")
```

Ab:

```python
if is_savable(value):
    value.save()
```

Type checker ko:

```text
value: Savable
```

mil sakta hai.

Lekin yahan ek caution hai:

```python
hasattr(value, "save")
```

sirf existence check karta hai; method ka signature correct hai ya nahi, runtime par automatically verify nahi karta.

Agar robust runtime protocol check chahiye, `@runtime_checkable` + `isinstance()` ka appropriate use better ho sakta hai.

---

# 22. `@runtime_checkable`

Example:

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Savable(Protocol):
    def save(self) -> None:
        ...
```

Ab runtime par:

```python
isinstance(obj, Savable)
```

possible ho sakta hai.

Lekin important limitation:

> Runtime protocol checking generally **attribute/method presence** level tak hoti hai; static signature compatibility ki complete verification runtime par nahi hoti.

Ye distinction advanced typing mein important hai.

---

# 23. Type narrowing sirf `if` tak limited nahi

Example:

```python
def process(value: int | str):

    if isinstance(value, int):
        return value + 10

    return value.upper()
```

Narrowing:

```text
if branch:
int

after branch:
str
```

Type checker control flow analyze karta hai.

Isko **flow-sensitive type narrowing** keh sakte hain.

---

# 24. `TypeGuard` with tuples

Example:

```python
from typing import TypeGuard


def is_pair(
    value: tuple[object, ...]
) -> TypeGuard[tuple[str, str]]:

    return (
        len(value) == 2
        and all(isinstance(x, str) for x in value)
    )
```

Then:

```python
value: tuple[object, ...]

if is_pair(value):
    a, b = value

    print(a.upper())
    print(b.upper())
```

Narrowed type:

```text
tuple[str, str]
```

---

# 25. `TypeGuard` with dictionaries

Example:

```python
from typing import TypeGuard


def is_user(data: dict[str, object]) -> TypeGuard[dict[str, str]]:
    return (
        isinstance(data.get("name"), str)
        and isinstance(data.get("email"), str)
    )
```

Then:

```python
data: dict[str, object] = {
    "name": "Ali",
    "email": "ali@example.com"
}
```

After:

```python
if is_user(data):
```

type checker ke perspective se:

```text
data: dict[str, str]
```

ho sakta hai.

**Lekin semantic level par dhyan:** ye guard sirf dictionary ke *saare values* strings prove nahi kar raha; ye function apne declared target ko guarantee karne ke liye strong enough hona chahiye. Real code mein `TypedDict` zyada precise model ho sakta hai.

---

# 26. `TypeIs` aur `TypeGuard` ka direct comparison

| Feature                      | `TypeGuard`                    | `TypeIs`                           |
| ---------------------------- | ------------------------------ | ---------------------------------- |
| True branch narrow           | ✅                              | ✅                                  |
| False branch narrow          | ❌ generally not as TypeIs does | ✅                                  |
| Target subtype hona required | ❌                              | ✅/compatible intersection required |
| Custom narrowing             | ✅                              | ✅                                  |
| Python typing use            | Static type checker            | Static type checker                |
| Runtime magic                | ❌                              | ❌                                  |

Simple memory trick:

```text
TypeGuard
    ↓
"True hai to is type ko maan lo."

TypeIs
    ↓
"True mein ye type,
 False mein is type ko hata do."
```

---

# 27. `TypeIs` ko `isinstance()` ke advanced wrapper ki tarah samjho

Built-in:

```python
isinstance(value, str)
```

type checker already understand karta hai.

Custom logic:

```python
def is_special_string(value):
    ...
```

mein checker ko manually batana pad sakta hai.

`TypeIs`:

```python
def is_special_string(value) -> TypeIs[str]:
    ...
```

type system ko batata hai:

```text
True → value is str
False → value is not str
```

---

# 28. Real-world example: API data validation

Suppose API se:

```python
data: object
```

aata hai.

Aap check karte ho:

```python
def is_valid_equipment(data: object) -> TypeGuard[Equipment]:
    return isinstance(data, Equipment)
```

Then:

```python
if is_valid_equipment(data):
    print(data.equipment_id)
```

Without guard:

```text
data: object
```

With guard:

```text
data: Equipment
```

Yani validation aur static typing connect ho gaye.

---

# 29. `TypeGuard` ko validation function samjho

Aap is pattern ko yaad rakho:

```python
def is_X(value: Input) -> TypeGuard[X]:
    ...
```

Meaning:

```text
Input
  ↓
runtime validation
  ↓
True
  ↓
X
```

Example:

```python
def is_ahu(value: object) -> TypeGuard[AHU]:
    return isinstance(value, AHU)
```

---

# 30. Lekin TypeGuard ko blindly trust nahi karna

Ye bohat important professional point hai.

Aap likh sakte ho:

```python
def fake_guard(value: object) -> TypeGuard[str]:
    return True
```

Ab type checker maan sakta hai:

```text
value: str
```

lekin runtime par value integer ho sakti hai.

Example:

```python
value = 100

if fake_guard(value):
    value.upper()
```

Runtime error:

```text
AttributeError
```

Isliye:

> **TypeGuard ek promise hai jo programmer type checker ko de raha hai.**

Agar guard ki implementation wrong hai, static type safety compromise ho sakti hai.

---

# 31. Ye concept bohat important hai

`TypeGuard`:

```text
"Python ko type convert nahi karta."
```

Instead:

```text
"Type checker ko narrowing information deta hai."
```

Runtime validation:

```python
isinstance()
hasattr()
len()
dictionary checks
custom validation
```

aapko khud karni hoti hai.

---

# 32. Lesson 58 se connection

Humne Lesson 58 mein seekha:

```text
TypeVar
Generic
Protocol
Variance
```

Ab Lesson 62 mein:

```text
TypeGuard
TypeIs
```

in concepts ke saath naturally connect hote hain.

Example architecture:

```text
Generic repository
        │
        ↓
returns unknown/base data
        │
        ↓
runtime validation
        │
        ↓
TypeGuard / TypeIs
        │
        ↓
specific type
        │
        ↓
type-safe processing
```

Example:

```python
equipment: object = repo.get("AHU-001")

if is_ahu(equipment):
    equipment.start()
```

---

# 33. Final mental model

Is lesson ko ye diagram yaad rakh kar revise karo:

```text
             TYPE NARROWING
                   │
          ┌────────┴────────┐
          │                 │
   Built-in checks     Custom checks
          │                 │
    isinstance()      TypeGuard / TypeIs
          │                 │
          └────────┬────────┘
                   ↓
             Specific type
                   ↓
          safer operations
```

Aur sabse important difference:

```text
TypeGuard[T]

True:
    → T

False:
    → TypeIs jaisi complementary narrowing guarantee nahi
```

versus:

```text
TypeIs[T]

True:
    → T ke saath compatible narrowed type

False:
    → T ko exclude karke remainder
```

### Ek practical rule

Agar aap kehna chahte ho:

> **"Meri custom checking true hai to variable ko is type ka samjho."**

→ `TypeGuard`

Agar aap chahte ho:

> **"True mein target type rakho aur false mein target type ko possibilities se remove bhi karo."**

→ `TypeIs`

Aur agar normal:

```python
isinstance()
issubclass()
```

already kaam kar raha hai, to unnecessary `TypeGuard`/`TypeIs` banane ki zaroorat nahi.
Bilkul. Ab **next lesson**:

# Lesson 63 — Python `match` / `case`

## Structural Pattern Matching

Ye Python ka kaafi powerful feature hai. Isko sirf "`switch` ka replacement" samajhna **incomplete** hai.

Python ka `match/case`:

* values compare kar sakta hai
* multiple values destructure kar sakta hai
* lists/tuples match kar sakta hai
* dictionaries match kar sakta hai
* classes/dataclasses match kar sakta hai
* conditions (`if`) ke saath combine ho sakta hai
* nested structures match kar sakta hai
* `|` se OR patterns bana sakta hai
* `_` se wildcard bana sakta hai

---

# 1. Basic `match`

Normal `if/elif`:

```python
def get_status(code):
    if code == 200:
        return "OK"
    elif code == 404:
        return "Not Found"
    elif code == 500:
        return "Server Error"
    else:
        return "Unknown"
```

`match`:

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

Yahan:

```python
case 200:
```

ka matlab:

> Agar `code` ki value `200` hai.

---

# 2. `case _` kya hai?

```python
case _:
```

underscore `_` wildcard hai.

Matlab:

> Jo bhi value ho, match kar jao.

Example:

```python
match value:
    case 10:
        print("Ten")

    case 20:
        print("Twenty")

    case _:
        print("Something else")
```

Agar:

```python
value = 100
```

to:

```text
Something else
```

---

# 3. `match` ko `switch` mat samjho

C/Java style switch normally:

```text
value
 ↓
case value
 ↓
case value
```

Python `match`:

```text
object
 ↓
pattern
 ↓
structure
 ↓
destructuring
 ↓
optional condition
```

Isliye naam hai:

> **Structural Pattern Matching**

---

# 4. Variable capture

Ab interesting part.

```python
value = 100

match value:
    case x:
        print(x)
```

Yahan:

```python
case x:
```

`x` ko compare nahi kar raha.

Ye value ko:

```python
x
```

mein **capture** kar raha hai.

Output:

```text
100
```

Ye beginners ke liye common confusion hai.

---

# 5. `case x` vs `case 100`

```python
case 100:
```

means:

> value exactly `100` honi chahiye.

Lekin:

```python
case x:
```

means:

> jo value hai usko `x` mein capture karo.

Example:

```python
match value:
    case 100:
        print("Exactly 100")

    case x:
        print("Value:", x)
```

---

# 6. Sequence pattern

Ab structural matching ka real power.

```python
data = [10, 20, 30]

match data:
    case [10, 20, 30]:
        print("Exact list")
```

Yahan list ki **structure + values** dono match ho rahe hain.

---

# 7. Capture values from list

```python
data = [10, 20]

match data:
    case [x, y]:
        print(x)
        print(y)
```

Result:

```text
10
20
```

Python ne list ko destructure kar diya.

Conceptually:

```text
[10, 20]

   ↓

[x, y]

x = 10
y = 20
```

---

# 8. Variable number of elements: `*`

Suppose:

```python
data = [10, 20, 30, 40, 50]
```

Aap likh sakte ho:

```python
match data:
    case [first, *rest]:
        print(first)
        print(rest)
```

Result:

```text
10
[20, 30, 40, 50]
```

Yahan:

```python
first
```

first element hai.

Aur:

```python
*rest
```

remaining elements capture karta hai.

---

# 9. Start + middle + end

```python
data = [10, 20, 30, 40, 50]

match data:
    case [first, *middle, last]:
        print(first)
        print(middle)
        print(last)
```

Result:

```text
10
[20, 30, 40]
50
```

Ye normal `if` statements se kaafi cleaner ho sakta hai.

---

# 10. Tuple matching

```python
point = (10, 20)

match point:
    case (x, y):
        print("X =", x)
        print("Y =", y)
```

Output:

```text
X = 10
Y = 20
```

Parentheses optional style mein:

```python
case x, y:
```

bhi likha ja sakta hai.

---

# 11. OR pattern `|`

Suppose:

```python
status = "success"
```

Aur `"success"` aur `"ok"` ko same treat karna hai.

```python
match status:
    case "success" | "ok":
        print("Operation successful")

    case "error":
        print("Operation failed")
```

`|` means:

> Ye **ya** woh.

---

# 12. OR pattern with capture

Important rule:

OR pattern mein alternatives ko compatible captures rakhne hote hain.

Example concept:

```python
case "yes" | "no":
```

simple hai.

Lekin:

```python
case ("yes", x) | ("no", y):
```

problematic design hai because successful alternative different variable names capture kar raha hai.

Better:

```python
case ("yes", value) | ("no", value):
```

Same capture name.

---

# 13. Guard: `if`

`case` ke saath condition laga sakte ho.

```python
value = 15

match value:
    case x if x > 10:
        print("Greater than 10")

    case x:
        print("10 or less")
```

Yahan:

```python
case x if x > 10:
```

do stages hain:

```text
pattern match
      ↓
x capture
      ↓
if x > 10
      ↓
case successful
```

Is extra condition ko **guard** kehte hain.

---

# 14. Guard ka practical example

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

Result:

```text
Warm
```

---

# 15. Dictionary pattern

Ab bohat useful feature.

```python
data = {
    "name": "Ali",
    "age": 30
}
```

Match:

```python
match data:
    case {"name": name, "age": age}:
        print(name)
        print(age)
```

Output:

```text
Ali
30
```

Ye dictionary ko destructure karta hai.

---

# 16. Dictionary pattern mein extra keys

Suppose:

```python
data = {
    "name": "Ali",
    "age": 30,
    "city": "Riyadh"
}
```

Pattern:

```python
case {"name": name, "age": age}:
```

phir bhi match karega.

Kyun?

Pattern ka matlab:

> Dictionary mein ye required keys honi chahiye.

Ye normally ye nahi keh raha:

> Dictionary mein **sirf** ye keys honi chahiye.

---

# 17. Remaining dictionary data

Aap remaining keys capture bhi kar sakte ho:

```python
match data:
    case {
        "name": name,
        **rest
    }:
        print(name)
        print(rest)
```

Conceptually:

```text
name = "Ali"

rest = {
    "age": 30,
    "city": "Riyadh"
}
```

---

# 18. Nested pattern

Ab actual structural matching.

```python
data = {
    "employee": {
        "name": "Ali",
        "department": "HVAC"
    }
}
```

Match:

```python
match data:
    case {
        "employee": {
            "name": name,
            "department": department
        }
    }:
        print(name)
        print(department)
```

Output:

```text
Ali
HVAC
```

Yani nested structures directly match kar sakte ho.

---

# 19. Practical API response example

Suppose API response:

```python
response = {
    "status": "success",
    "data": {
        "id": 100,
        "name": "AHU-001"
    }
}
```

Pattern:

```python
match response:
    case {
        "status": "success",
        "data": {
            "id": equipment_id,
            "name": name
        }
    }:
        print("Equipment:", equipment_id)
        print("Name:", name)

    case {
        "status": "error",
        "message": message
    }:
        print("Error:", message)

    case _:
        print("Unknown response")
```

Ye API response parsing mein bohat readable ho sakta hai.

---

# 20. Class pattern

Ab Lesson 61 ke `dataclass` se connection.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

Object:

```python
point = Point(10, 20)
```

Match:

```python
match point:
    case Point(x, y):
        print(x, y)
```

Output:

```text
10 20
```

Yahan dataclass ka:

```python
__match_args__
```

important role hai.

---

# 21. Keyword class pattern

Aap positional ke bajaye keyword matching bhi kar sakte ho:

```python
match point:
    case Point(x=10, y=20):
        print("Point found")
```

Ya:

```python
match point:
    case Point(x=x, y=y):
        print(x, y)
```

---

# 22. Class pattern + guard

```python
match point:
    case Point(x, y) if x > 0 and y > 0:
        print("First quadrant")

    case Point(x, y):
        print("Other quadrant")
```

Yahan:

```text
Point structure
      ↓
x, y capture
      ↓
guard
      ↓
x > 0 and y > 0
```

---

# 23. Multiple classes

Suppose:

```python
@dataclass
class AHU:
    id: str
    airflow: int


@dataclass
class Refrigerator:
    id: str
    temperature: float
```

Ab:

```python
equipment = AHU("AHU-01", 5000)
```

Match:

```python
match equipment:

    case AHU(id, airflow):
        print("AHU:", id, airflow)

    case Refrigerator(id, temperature):
        print("Refrigerator:", id, temperature)

    case _:
        print("Unknown equipment")
```

Ye facility-management type application mein naturally useful pattern hai.

---

# 24. Nested class patterns

Aur advanced:

```python
@dataclass
class Building:
    name: str
    equipment: object
```

Suppose:

```python
building = Building(
    "Tower A",
    AHU("AHU-01", 5000)
)
```

Match:

```python
match building:
    case Building(
        name,
        AHU(id, airflow)
    ):
        print(name)
        print(id)
        print(airflow)
```

Ek hi pattern mein nested object destructure ho gaya.

---

# 25. Type pattern

Aap type ke basis par bhi match kar sakte ho:

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

Ye conceptually `isinstance()` style type checking jaisa hai.

---

# 26. Capture vs type pattern

Ye difference important hai:

```python
case str():
```

means:

> object `str` type ka hai.

Lekin:

```python
case value:
```

means:

> value ko `value` naam mein capture karo.

Aur:

```python
case str(value):
```

specific pattern context mein string object ko capture/destructure karne ki koshish ka syntax hai; isko simple type check ke liye usually `case str():` hi rakho.

---

# 27. Literal patterns

Ye literal comparison hain:

```python
case 10:
case "hello":
case True:
case None:
```

Example:

```python
match value:
    case None:
        print("No value")

    case True:
        print("Enabled")

    case False:
        print("Disabled")
```

---

# 28. `None` ke saath useful pattern

```python
result = None

match result:
    case None:
        print("No result")

    case value:
        print("Result:", value)
```

Ye readable null handling ho sakti hai.

---

# 29. `_` aur variable mein difference

Ye bohat important hai:

```python
case _:
```

`_`:

> ignore/catch-all

Lekin:

```python
case x:
```

`x`:

> actual value capture

Example:

```python
match 100:
    case _:
        print("Ignored")
```

versus:

```python
match 100:
    case x:
        print(x)
```

Output:

```text
100
```

---

# 30. Case ordering extremely important hai

Patterns top-to-bottom evaluate hote hain.

Example:

```python
match value:
    case x:
        print("Anything")

    case 100:
        print("100")
```

`case x` almost everything capture kar lega.

Isliye:

```python
case 100:
```

kabhi reach nahi hoga.

Correct:

```python
match value:
    case 100:
        print("100")

    case x:
        print("Anything:", x)
```

Rule:

> **Specific patterns pehle, general patterns baad mein.**

---

# 31. `_` usually last hona chahiye

Good:

```python
match status:
    case "running":
        ...

    case "stopped":
        ...

    case _:
        ...
```

Bad design:

```python
match status:
    case _:
        ...

    case "running":
        ...
```

Because wildcard sab kuch consume kar lega.

---

# 32. Sequence matching vs exact length

Example:

```python
data = [1, 2, 3]
```

Pattern:

```python
case [a, b]:
```

match nahi karega because exactly 2 elements expected hain.

Lekin:

```python
case [a, b, *rest]:
```

match karega:

```text
a = 1
b = 2
rest = [3]
```

---

# 33. `*rest` ka special behavior

```python
case [first, *rest]:
```

`rest` always list-style remaining sequence capture karta hai.

Example:

```text
[10]
```

→

```text
first = 10
rest = []
```

Example:

```text
[10, 20, 30]
```

→

```text
first = 10
rest = [20, 30]
```

---

# 34. Mapping pattern vs sequence pattern

Dictionary:

```python
case {"name": name}:
```

Sequence:

```python
case [name]:
```

Tuple:

```python
case (x, y):
```

Class:

```python
case Employee(name, salary):
```

Yani `match` different structures ko directly understand karta hai.

---

# 35. Practical command parser

Ye ek strong practical example hai.

```python
command = ("move", "AHU-01", 10)
```

Match:

```python
match command:

    case ("move", equipment_id, value):
        print(
            "Moving",
            equipment_id,
            value
        )

    case ("stop", equipment_id):
        print(
            "Stopping",
            equipment_id
        )

    case ("status", equipment_id):
        print(
            "Checking",
            equipment_id
        )

    case _:
        print("Unknown command")
```

Ye command-processing architecture mein useful hai.

---

# 36. Pattern + guard together

```python
command = ("set_temperature", "AHU-01", 22)

match command:

    case ("set_temperature", equipment_id, temp) \
            if 18 <= temp <= 26:

        print(
            equipment_id,
            "temperature set to",
            temp
        )

    case ("set_temperature", equipment_id, temp):
        print("Invalid temperature")

    case _:
        print("Unknown command")
```

Yahan pattern:

```text
("set_temperature", equipment_id, temp)
```

aur guard:

```text
18 <= temp <= 26
```

dono use hue.

---

# 37. `match` + Type Narrowing

Lesson 62 se bhi connection hai.

Suppose:

```python
value: int | str
```

Then:

```python
match value:

    case int():
        print(value + 10)

    case str():
        print(value.upper())
```

Each case mein type narrow ho sakta hai:

```text
int | str
    │
    ├── int() → int
    │
    └── str() → str
```

Yani:

> `match/case` bhi type narrowing ka powerful mechanism ho sakta hai.

---

# 38. `match` + `Protocol`

Aap protocols ke saath patterns use karte waqt runtime/static typing details carefully design karte ho, especially because normal class patterns actual class structure aur runtime behavior se related hote hain.

Protocol ko simply:

```python
case SomeProtocol():
```

samajhna `isinstance()` ke runtime behavior ke baghair safe assumption nahi hai.

Practical architecture mein:

```text
Protocol
   ↓
interface / static structural typing

match
   ↓
concrete runtime structure
```

dono ka role alag rakho.

---

# 39. `match` kab use karna chahiye?

Use `match` when:

### 1. Multiple structural cases hain

```python
case [x, y]
case [x, y, z]
```

### 2. Different object types hain

```python
case AHU(...)
case Refrigerator(...)
```

### 3. API/data structures parse karne hain

```python
case {"status": "success", ...}
```

### 4. Commands/events process karne hain

```python
case ("start", id)
case ("stop", id)
```

### 5. Nested data hai

```python
case {"data": {"user": {...}}}
```

---

# 40. Kab simple `if` better hai?

Agar sirf ek simple condition hai:

```python
if temperature > 25:
    ...
```

to `match` unnecessarily complicated hoga.

Similarly:

```python
if user.is_admin:
    ...
```

ke liye `match` ki zaroorat nahi.

Rule:

> **Complex structure → `match`**
>
> **Simple boolean condition → `if`**

---

# 41. `match` ka advanced mental model

Isko yaad rakho:

```text
                     match subject
                           │
                           ↓
                     case patterns
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       Literal          Structure         Class
          │                │                │
       200/"ok"        [x, y]          Employee(...)
                           │
                           ↓
                      Capture values
                           │
                           ↓
                         Guard
                           │
                           ↓
                       case body
```

---

# 42. Sabse important patterns cheat sheet

### Literal

```python
case 200:
```

### Wildcard

```python
case _:
```

### Capture

```python
case x:
```

### OR

```python
case 200 | 201:
```

### List

```python
case [x, y]:
```

### Remaining list

```python
case [x, *rest]:
```

### Dictionary

```python
case {"name": name}:
```

### Class

```python
case Employee(name, salary):
```

### Guard

```python
case x if x > 10:
```

### Nested

```python
case {"employee": {"name": name}}:
```

---

# 43. Final practical example

Ab ek example jisme almost sab concepts combine hain:

```python
from dataclasses import dataclass


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
            print(
                id,
                "AHU has high airflow:",
                airflow
            )

        case AHU(id, airflow):
            print(
                id,
                "AHU airflow:",
                airflow
            )

        case Refrigerator(id, temperature) \
                if temperature > 5:
            print(
                id,
                "temperature high:",
                temperature
            )

        case Refrigerator(id, temperature):
            print(
                id,
                "temperature normal:",
                temperature
            )

        case _:
            print("Unknown equipment")
```

Call:

```python
process_equipment(
    AHU("AHU-01", 6000)
)
```

Result:

```text
AHU-01 AHU has high airflow: 6000
```

Aur:

```python
process_equipment(
    Refrigerator("REF-01", 3)
)
```

Result:

```text
REF-01 temperature normal: 3
```

Yahan ek hi `match` mein:

* class pattern
* destructuring
* variable capture
* guard
* fallback
* dataclass
* type-specific processing

sab combine ho gaye.

---

## Lesson 63 ka core concept

Agar sirf ye 5 cheezen strong ho gayin, to `match/case` ka foundation strong hai:

```text
1. Literal pattern
      case 200

2. Capture pattern
      case x

3. Structural pattern
      case [x, y]
      case {"name": name}

4. Class pattern
      case Employee(name, salary)

5. Guard
      case x if x > 10
```

**Sabse important baat:** Python `match` ko sirf `switch/case` mat samjho. Iski asli power **pattern matching + destructuring + guards + type-aware control flow** mein hai.
# Lesson 64 — `dataclass` Advanced

### Inheritance + `__match_args__` + `InitVar` + `ClassVar`

Ab hum basic `@dataclass` se aage **advanced level** par jayenge. Yeh concepts especially useful hain jab aap **large Python architecture, HVAC/equipment models, configuration objects, API models, ya work-order systems** bana rahe hon.

---

# 1. Sab se pehle: `dataclass` kya karta hai?

Normal class:

```python
class Equipment:
    def __init__(self, equipment_id, name, floor):
        self.equipment_id = equipment_id
        self.name = name
        self.floor = floor
```

Dataclass:

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    name: str
    floor: str
```

Python automatically useful methods generate kar deta hai:

```python
__init__()
__repr__()
__eq__()
```

Example:

```python
equipment = Equipment(
    "MEP-AHU-001",
    "AHU",
    "Thirty Four Floor"
)

print(equipment)
```

Output:

```text
Equipment(equipment_id='MEP-AHU-001', name='AHU', floor='Thirty Four Floor')
```

Lekin advanced dataclass mein 4 important concepts hain:

```text
Inheritance
     ↓
__match_args__
     ↓
InitVar
     ↓
ClassVar
```

---

# 2. Dataclass Inheritance

Ek dataclass doosri dataclass se inherit kar sakti hai.

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    floor: str

@dataclass
class AHU(Equipment):
    airflow: float
```

Ab:

```python
ahu = AHU(
    "MEP-AHU-001",
    "Thirty Four Floor",
    1200
)

print(ahu)
```

Output:

```text
AHU(
    equipment_id='MEP-AHU-001',
    floor='Thirty Four Floor',
    airflow=1200
)
```

Yani child class ko parent ke fields bhi mil gaye.

---

# 3. Iska actual benefit kya hai?

Suppose facility mein different equipment hain:

```text
Equipment
   │
   ├── AHU
   ├── VAV
   ├── Refrigerator
   ├── Pump
   └── FCU
```

Common information:

```python
equipment_id
floor
area
```

Specific information:

AHU:

```python
airflow
```

VAV:

```python
damper_position
```

Refrigerator:

```python
temperature
```

Hum architecture bana sakte hain:

```python
from dataclasses import dataclass


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

Ab:

```python
ahu = AHU(
    "AHU-001",
    "34F",
    1200
)

vav = VAV(
    "VAV-001",
    "34F",
    65
)

ref = Refrigerator(
    "REF-001",
    "41F",
    4.5
)
```

Yeh **domain modeling** ka powerful pattern hai.

---

# 4. Important problem: field ordering

Dataclass inheritance mein ek important rule hai.

Parent fields pehle aate hain.

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str
```

Child:

```python
@dataclass
class AHU(Equipment):
    airflow: float
```

Generated constructor logically:

```python
AHU(
    equipment_id,
    floor,
    airflow
)
```

Isliye:

```python
AHU("AHU-001", "34F", 1200)
```

correct hai.

---

# 5. Default field ka important issue

Yeh common problem hai:

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    floor: str = "Unknown"


@dataclass
class AHU(Equipment):
    airflow: float
```

Yeh problematic ho sakta hai because dataclass constructor ordering effectively ban jati hai:

```python
equipment_id
floor="Unknown"
airflow
```

Aur Python mein non-default parameter default parameter ke baad nahi aa sakta.

Conceptually:

```python
def __init__(
    equipment_id,
    floor="Unknown",
    airflow
):
```

invalid hai.

### Solution

Child field ko bhi default de do:

```python
@dataclass
class AHU(Equipment):
    airflow: float = 0.0
```

Ya architecture ko `kw_only=True` ke saath design karo.

---

# 6. `kw_only=True`

Advanced dataclass mein keyword-only fields bohot useful hain.

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    floor: str

@dataclass(kw_only=True)
class AHU(Equipment):
    airflow: float
```

Ab:

```python
ahu = AHU(
    "AHU-001",
    "34F",
    airflow=1200
)
```

Lekin:

```python
AHU("AHU-001", "34F", 1200)
```

allowed nahi hoga.

### Faida

Large objects mein positional arguments ki mistake kam hoti hai.

```python
AHU(
    equipment_id="AHU-001",
    floor="34F",
    airflow=1200
)
```

Zyada readable hai.

---

# 7. `__match_args__`

Ab dataclass ka ek powerful connection `match/case` ke saath.

Aapne previous lesson mein `match/case` dekha tha.

Example:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

Ab:

```python
point = Point(10, 20)

match point:
    case Point(x, y):
        print(x, y)
```

Output:

```text
10 20
```

Lekin Python ko kaise pata chala ke:

```python
Point(x, y)
```

mein pehla value `x` aur doosra `y` hai?

Yahan `__match_args__` ka role hai.

---

# 8. `__match_args__` kya hai?

Dataclass automatically generally create karta hai:

```python
__match_args__
```

Example:

```python
@dataclass
class Point:
    x: int
    y: int
```

Conceptually:

```python
Point.__match_args__
```

result:

```python
('x', 'y')
```

Yani:

```text
position 0 → x
position 1 → y
```

Isliye:

```python
case Point(x, y):
```

ka matlab:

```text
Point ke x ko x variable mein capture karo
Point ke y ko y variable mein capture karo
```

---

# 9. `__match_args__` manually de sakte hain

Example:

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str

    __match_args__ = (
        "equipment_id",
        "status"
    )
```

Ab:

```python
equipment = Equipment(
    "AHU-001",
    "34F",
    "Running"
)
```

Match:

```python
match equipment:
    case Equipment(equipment_id, status):
        print(equipment_id, status)
```

Output:

```text
AHU-001 Running
```

Notice:

```text
equipment_id → first
status       → second
```

`floor` intentionally positional matching mein include nahi kiya.

---

# 10. `match_args=False`

Aap automatic positional matching disable bhi kar sakte ho.

```python
@dataclass(match_args=False)
class Equipment:
    equipment_id: str
    floor: str
```

Ab:

```python
case Equipment(x, y):
```

positional pattern allowed nahi hoga.

Lekin keyword pattern use kar sakte ho:

```python
match equipment:
    case Equipment(equipment_id="AHU-001"):
        print("Found AHU")
```

### Kab useful?

Jab aap chahte ho ke class ka pattern matching API **stable aur explicit** ho.

---

# 11. `InitVar`

Ab aate hain ek very important advanced feature par.

`InitVar` ka matlab:

> Value constructor mein receive hogi, lekin normal dataclass field ke taur par store nahi hogi.

Example:

```python
from dataclasses import dataclass, InitVar


@dataclass
class Equipment:
    equipment_id: str
    raw_temperature: InitVar[float]

    def __post_init__(self, raw_temperature):
        print(raw_temperature)
```

Create:

```python
equipment = Equipment(
    "AHU-001",
    24.5
)
```

Output:

```text
24.5
```

Lekin:

```python
print(equipment)
```

mein `raw_temperature` normal field nahi hoga.

---

# 12. `InitVar` ka actual purpose

Suppose aapko object create karne ke waqt kuch temporary information chahiye.

Example:

```text
Input:
equipment_id
temperature_celsius

Processing:
temperature_celsius → Fahrenheit

Stored:
equipment_id
temperature_fahrenheit
```

Code:

```python
from dataclasses import dataclass, InitVar


@dataclass
class Equipment:
    equipment_id: str
    temperature_f: float
    temperature_c: InitVar[float]

    def __post_init__(self, temperature_c):
        self.temperature_f = (
            temperature_c * 9 / 5
        ) + 32
```

Use:

```python
equipment = Equipment(
    "REF-001",
    0,
    4
)
```

Result:

```python
equipment.temperature_f
```

is:

```text
39.2
```

`temperature_c` permanently object mein store karna zaroori nahi tha.

---

# 13. `__post_init__`

`InitVar` usually `__post_init__` ke saath use hota hai.

Normal flow:

```text
__init__()
   ↓
fields assign
   ↓
__post_init__()
   ↓
additional processing
```

Example:

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature: float
    raw_temperature: InitVar[str]

    def __post_init__(self, raw_temperature):
        self.temperature = float(raw_temperature)
```

Input:

```python
Equipment(
    "REF-001",
    0,
    "4.5"
)
```

Yahan:

```text
"4.5"
```

temporary initialization value hai.

`__post_init__()` usko process karta hai.

---

# 14. `InitVar` field aur normal field mein difference

### Normal field

```python
@dataclass
class Equipment:
    temperature: float
```

Value:

```python
equipment.temperature
```

object ka permanent data hai.

### `InitVar`

```python
@dataclass
class Equipment:
    raw_temperature: InitVar[str]
```

Value:

```text
constructor ke liye input
```

hai.

Automatically permanent field nahi banti.

Mental model:

```text
Normal field
    ↓
Input → Store


InitVar
    ↓
Input → Process → Discard
```

---

# 15. `InitVar` ka advanced example — database/config

Suppose object create karte waqt config chahiye:

```python
from dataclasses import dataclass, InitVar


@dataclass
class Equipment:
    equipment_id: str
    name: str
    config: InitVar[dict]

    def __post_init__(self, config):
        self.name = config.get(
            "name",
            self.name
        )
```

Use:

```python
config = {
    "name": "AHU Main Lobby"
}

equipment = Equipment(
    "AHU-001",
    "Unknown",
    config
)
```

Object mein:

```python
equipment.equipment_id
equipment.name
```

hain.

Lekin `config` ko object state ka part banana zaroori nahi.

---

# 16. `ClassVar`

Ab fourth important concept.

Normal variable:

```python
@dataclass
class Equipment:
    equipment_id: str
    status: str
```

Har object ka apna:

```text
equipment_id
status
```

hoga.

Lekin kuch data **class-level** hota hai.

Example:

```text
Allowed statuses:

Running
Stopped
Fault
Maintenance
```

Har equipment object ke liye same list hai.

Yahan `ClassVar` useful hai.

```python
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Equipment:
    equipment_id: str
    status: str

    allowed_statuses: ClassVar[set[str]] = {
        "Running",
        "Stopped",
        "Fault",
        "Maintenance"
    }
```

---

# 17. `ClassVar` ka matlab

```python
allowed_statuses: ClassVar[set[str]]
```

ka matlab:

> Yeh dataclass instance field nahi hai; yeh class-level variable hai.

Isliye generated `__init__()` mein:

```python
allowed_statuses
```

nahi aayega.

Yeh:

```python
Equipment(
    "AHU-001",
    "Running"
)
```

hai.

Not:

```python
Equipment(
    "AHU-001",
    "Running",
    {...}
)
```

---

# 18. ClassVar access

Class se:

```python
Equipment.allowed_statuses
```

Instance se bhi technically:

```python
equipment.allowed_statuses
```

access ho sakta hai.

Lekin conceptually yeh:

```text
Equipment class ka data
```

hai, object-specific data nahi.

---

# 19. `ClassVar` kyun important hai?

Dataclass normal annotations ko fields samajhta hai.

Example:

```python
@dataclass
class Equipment:
    equipment_id: str
    counter: int = 0
```

`counter` **instance field** hai.

Har object ka apna:

```python
equipment1.counter
equipment2.counter
```

hoga.

Agar aap class-level counter chahte ho:

```python
from typing import ClassVar

@dataclass
class Equipment:
    equipment_id: str

    total_created: ClassVar[int] = 0
```

Ab:

```text
Equipment.total_created
```

class-level state hai.

---

# 20. Important: `ClassVar` mutable data

Example:

```python
@dataclass
class Equipment:
    equipment_id: str

    types: ClassVar[list[str]] = [
        "AHU",
        "VAV",
        "FCU"
    ]
```

Yeh shared list hai.

Matlab:

```python
Equipment.types.append("Pump")
```

karoge to class ke through sabko same updated list milegi.

Yeh intentional ho to useful hai.

---

# 21. `ClassVar` vs normal field

Yeh distinction yaad rakho:

```python
@dataclass
class Equipment:

    equipment_id: str
```

Meaning:

```text
har object ka apna equipment_id
```

Aur:

```python
types: ClassVar[list[str]]
```

Meaning:

```text
class ka shared data
```

Visual:

```text
Equipment CLASS
│
├── types ─────────────── shared
│
├── Object 1
│    └── equipment_id
│
├── Object 2
│    └── equipment_id
│
└── Object 3
     └── equipment_id
```

---

# 22. Ab sab 4 concepts ek saath

Ab ek realistic HVAC architecture banate hain.

```python
from dataclasses import dataclass, InitVar
from typing import ClassVar


@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str

    allowed_statuses: ClassVar[set[str]] = {
        "Running",
        "Stopped",
        "Fault",
        "Maintenance"
    }


@dataclass
class AHU(Equipment):
    airflow: float
    raw_status: InitVar[str] = ""

    def __post_init__(self, raw_status):
        if raw_status:
            self.status = raw_status.upper()
```

Create:

```python
ahu = AHU(
    equipment_id="AHU-001",
    floor="34F",
    status="unknown",
    airflow=1200,
    raw_status="running"
)
```

Ab:

```python
print(ahu)
```

roughly:

```text
AHU(
    equipment_id='AHU-001',
    floor='34F',
    status='RUNNING',
    airflow=1200
)
```

Notice:

```text
raw_status
```

object ke normal representation ka field nahi hai.

Kyun?

Because:

```python
raw_status: InitVar[str]
```

tha.

Aur:

```python
allowed_statuses
```

bhi instance field nahi hai.

Kyun?

Because:

```python
ClassVar
```

hai.

---

# 23. Ab `match/case` bhi add karo

```python
match ahu:
    case AHU(equipment_id, floor, status, airflow):
        print(
            equipment_id,
            floor,
            status,
            airflow
        )
```

Yahan dataclass ka automatic:

```python
__match_args__
```

kaam kar raha hai.

Conceptually:

```python
AHU.__match_args__
```

roughly fields ke positional names represent karega.

---

# 24. Better: keyword matching

Large architecture mein main keyword matching prefer karunga:

```python
match ahu:
    case AHU(
        equipment_id="AHU-001",
        status="RUNNING"
    ):
        print("AHU running")
```

Iska faida:

Agar kal fields ka order change ho jaye, positional pattern comparatively fragile hota hai.

Keyword pattern:

```python
case AHU(status="RUNNING"):
```

zyada explicit hai.

---

# 25. `__match_args__` + inheritance

Inheritance ke saath yeh aur interesting ho jata hai.

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str


@dataclass
class AHU(Equipment):
    airflow: float
```

AHU ke positional pattern mein inherited fields bhi relevant ho sakte hain:

```python
match ahu:
    case AHU(equipment_id, floor, airflow):
        ...
```

Yani:

```text
AHU
│
├── equipment_id   ← parent
├── floor          ← parent
└── airflow        ← child
```

Pattern matching object ki class hierarchy aur dataclass-generated match metadata ko use kar sakta hai.

---

# 26. Ek aur important concept: `InitVar` inherited class mein

`InitVar` ko inheritance ke saath bhi use kar sakte ho.

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

Yahan dikkat yeh hai ke `__post_init__` inheritance chain mein manually coordinate karni pad sakti hai.

Isliye advanced dataclass architecture mein `__post_init__` ka design carefully karna important hai.

---

# 27. `InitVar` vs `ClassVar` — ek line mein

Yeh bahut important hai:

### `InitVar`

```python
InitVar[T]
```

means:

> **constructor input hai, persistent instance field nahi.**

### `ClassVar`

```python
ClassVar[T]
```

means:

> **class-level data hai, instance field nahi.**

Visual:

```text
InitVar
Input
  ↓
__post_init__
  ↓
Object fields


ClassVar
Class
  ↓
Shared data
  ↓
All instances
```

---

# 28. `dataclass` + inheritance + ClassVar + InitVar + match

Complete example:

```python
from dataclasses import dataclass, InitVar
from typing import ClassVar


@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str

    allowed_statuses: ClassVar[set[str]] = {
        "RUNNING",
        "STOPPED",
        "FAULT",
        "MAINTENANCE"
    }


@dataclass
class AHU(Equipment):
    airflow: float
    raw_status: InitVar[str] = ""

    def __post_init__(self, raw_status):
        if raw_status:
            self.status = raw_status.upper()

        if self.status not in self.allowed_statuses:
            raise ValueError(
                f"Invalid status: {self.status}"
            )
```

Create:

```python
ahu = AHU(
    equipment_id="MEP-AHU-001",
    floor="Thirty Four Floor",
    status="unknown",
    airflow=1200,
    raw_status="running"
)
```

Result:

```python
print(ahu.status)
```

Output:

```text
RUNNING
```

And:

```python
print(ahu.allowed_statuses)
```

works because it comes from the class.

---

# 29. Ab is architecture ko `match/case` ke saath combine karo

```python
match ahu:
    case AHU(
        equipment_id=id,
        status="RUNNING",
        airflow=airflow
    ) if airflow > 1000:

        print(
            f"{id}: High airflow AHU"
        )

    case AHU(status="RUNNING"):
        print("AHU running")

    case AHU(status="FAULT"):
        print("AHU fault")

    case _:
        print("Other equipment")
```

Yahan multiple concepts ek saath kaam kar rahe hain:

```text
dataclass
   ↓
inheritance
   ↓
__match_args__
   ↓
match/case
   ↓
guard
```

---

# 30. Sabse important mental model

Is entire lesson ko is diagram se yaad rakho:

```text
                    DATACLASS
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   Inheritance    InitVar         ClassVar
        │              │              │
 Parent + Child    temporary       shared
 fields            constructor     class data
        │              input
        │
        └──────────────┐
                       ↓
                 __match_args__
                       │
                       ↓
                 match / case
```

### Short definitions

| Concept            | Meaning                                                          |
| ------------------ | ---------------------------------------------------------------- |
| `@dataclass`       | Data-oriented class ko simplify karta hai                        |
| Inheritance        | Parent ke fields/behavior ko child mein reuse karna              |
| `__match_args__`   | Positional `match/case` ke liye attribute order define karta hai |
| `InitVar`          | Constructor-only input                                           |
| `__post_init__`    | Initialization ke baad custom processing                         |
| `ClassVar`         | Class-level/shared variable                                      |
| `match_args=False` | Automatic positional pattern matching disable                    |
| `kw_only=True`     | Fields ko keyword-only banana                                    |

## Practical rule

Agar aapka data model simple hai:

```python
@dataclass
class Equipment:
    id: str
    name: str
```

enough hai.

Agar architecture complex ho:

```text
Base Equipment
      ↓
AHU / VAV / Refrigerator
      ↓
InitVar → input processing
      ↓
ClassVar → shared configuration
      ↓
__match_args__ → match/case integration
```

to advanced dataclass features useful ho jate hain.

**Next logical topic:** `typing.overload` — ek function ke multiple type-safe calling patterns ko static type checker ko samjhana.
# Lesson 65 — `typing.overload` — Function Overloading

Ab hum Python typing ka ek important advanced concept dekhte hain:

```python
typing.overload
```

Iska main purpose hai:

> **Ek hi function ke different input combinations ke corresponding different return types ko type checker ko samjhana.**

Sab se important baat:

**Python runtime par traditional function overloading nahi karta.**
`@overload` primarily **static type checking** ke liye hai.

---

# 1. Problem kya hai?

Suppose hamare paas function hai:

```python
def get_value(value):
    if isinstance(value, int):
        return value * 2

    if isinstance(value, str):
        return value.upper()
```

Ab logically:

```python
get_value(10)
```

return karega:

```text
20
```

Aur:

```python
get_value("hello")
```

return karega:

```text
HELLO
```

Lekin type checker ke liye question hai:

```text
get_value(10) → int
get_value("hello") → str
```

Is relationship ko kaise express karein?

Yahan `@overload` useful hai.

---

# 2. Basic `overload`

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

Ab:

```python
x = get_value(10)
```

Type checker samjhega:

```text
x → int
```

Aur:

```python
y = get_value("hello")
```

Type checker samjhega:

```text
y → str
```

---

# 3. `...` kya hai?

Yeh:

```python
@overload
def get_value(value: int) -> int:
    ...
```

actual implementation nahi hai.

Yeh **type signature declaration** hai.

Aap isko mentally samjho:

```text
Agar input int hai
        ↓
return int
```

Aur:

```python
@overload
def get_value(value: str) -> str:
    ...
```

means:

```text
Agar input str hai
        ↓
return str
```

---

# 4. Actual implementation neeche hoti hai

```python
@overload
def get_value(value: int) -> int:
    ...


@overload
def get_value(value: str) -> str:
    ...


def get_value(value: int | str) -> int | str:
    ...
```

Yahan last function:

```python
def get_value(...)
```

**actual runtime implementation** hai.

Runtime par isi function ko execute kiya jayega.

---

# 5. Bahut important rule

`@overload` functions ko Python runtime par separately implement nahi karta.

Yeh:

```python
@overload
def get_value(value: int) -> int:
    ...
```

aur:

```python
@overload
def get_value(value: str) -> str:
    ...
```

type checker ke liye signatures hain.

Actual function:

```python
def get_value(...):
```

hai.

Mental model:

```text
                    overload
                       │
          ┌────────────┴────────────┐
          ↓                         ↓
       int input                str input
          ↓                         ↓
       int output                str output
          └────────────┬────────────┘
                       ↓
              Actual implementation
```

---

# 6. `overload` ka real faida

Without overload:

```python
def get_value(value: int | str) -> int | str:
    ...
```

Agar:

```python
x = get_value(10)
```

type checker generally dekhega:

```text
x: int | str
```

Even though programmer jaanta hai ke `10` dene par `int` hi return hoga.

Overload ke saath:

```python
x = get_value(10)
```

becomes:

```text
x: int
```

Aur:

```python
y = get_value("hello")
```

becomes:

```text
y: str
```

### Yani:

```text
Union
↓
"input kuch bhi ho sakta hai, output bhi multiple ho sakta hai"

overload
↓
"particular input → particular output"
```

Yehi iska main power hai.

---

# 7. `Union` vs `overload`

### Without overload

```python
def parse(value: int | str) -> int | str:
    ...
```

Type checker:

```text
parse(10) → int | str
```

### With overload

```python
@overload
def parse(value: int) -> int:
    ...


@overload
def parse(value: str) -> str:
    ...


def parse(value: int | str) -> int | str:
    ...
```

Type checker:

```text
parse(10)       → int
parse("hello")  → str
```

### Important distinction

`Union` describes:

> possible types.

`overload` describes:

> **input/output relationship**.

---

# 8. Real practical example — HVAC

Suppose function different input ke according different object return karta hai.

```python
from dataclasses import dataclass


@dataclass
class AHU:
    equipment_id: str


@dataclass
class VAV:
    equipment_id: str
```

Function:

```python
@overload
def get_equipment(equipment_type: str) -> AHU:
    ...


@overload
def get_equipment(equipment_type: int) -> VAV:
    ...


def get_equipment(
    equipment_type: str | int
) -> AHU | VAV:

    if isinstance(equipment_type, str):
        return AHU(equipment_type)

    return VAV(str(equipment_type))
```

Ab:

```python
ahu = get_equipment("AHU-001")
```

Type checker:

```text
ahu → AHU
```

Aur:

```python
vav = get_equipment(100)
```

Type checker:

```text
vav → VAV
```

Runtime implementation ek hi hai.

---

# 9. Multiple overloads

Aap multiple signatures define kar sakte ho.

```python
@overload
def convert(value: int) -> float:
    ...


@overload
def convert(value: float) -> int:
    ...


@overload
def convert(value: str) -> str:
    ...


def convert(value: int | float | str) -> float | int | str:
    if isinstance(value, int):
        return float(value)

    if isinstance(value, float):
        return int(value)

    return value.upper()
```

Ab:

```python
a = convert(10)
```

```text
a → float
```

```python
b = convert(10.5)
```

```text
b → int
```

```python
c = convert("ahu")
```

```text
c → str
```

---

# 10. Overload order important ho sakta hai

Suppose:

```python
@overload
def process(value: object) -> object:
    ...


@overload
def process(value: str) -> str:
    ...
```

Broad signature:

```python
object
```

pehle aa gayi.

Type checker matching mein broad signature pehle capture kar sakti hai, depending on checker and overload rules.

Better:

```python
@overload
def process(value: str) -> str:
    ...


@overload
def process(value: object) -> object:
    ...
```

### Rule:

```text
Specific overload
       ↓
Broad overload
```

Yani narrow → broad.

---

# 11. `bool` aur `int` ka interesting case

Python mein:

```python
bool
```

`int` ka subclass hai.

Conceptually:

```text
int
 ↑
bool
```

Isliye overloads mein hierarchy important ho sakti hai.

```python
@overload
def check(value: bool) -> str:
    ...


@overload
def check(value: int) -> int:
    ...
```

Specific:

```python
bool
```

pehle rakhna safer hai.

---

# 12. `Literal` ke saath overload

Yeh aur powerful pattern hai.

Suppose function ka behavior parameter ke literal value par depend karta hai.

```python
from typing import Literal, overload
```

Example:

```python
@overload
def get_data(
    detailed: Literal[True]
) -> dict:
    ...


@overload
def get_data(
    detailed: Literal[False]
) -> str:
    ...


def get_data(
    detailed: bool
) -> dict | str:

    if detailed:
        return {
            "id": "AHU-001",
            "airflow": 1200
        }

    return "AHU-001"
```

Ab:

```python
data = get_data(True)
```

Type:

```text
dict
```

Aur:

```python
data = get_data(False)
```

Type:

```text
str
```

Yeh APIs mein bohot useful pattern hai.

---

# 13. `Literal` + overload ka mental model

```text
detailed=True
      ↓
dict


detailed=False
      ↓
str
```

Yeh relationship normal union se express karna mushkil hota:

```python
def get_data(
    detailed: bool
) -> dict | str:
```

Ismein type checker ko exact connection nahi pata.

Overload woh connection define karta hai.

---

# 14. `None` ke saath overload

Common real-world example:

```python
@overload
def find_equipment(
    equipment_id: str,
    required: Literal[True]
) -> AHU:
    ...


@overload
def find_equipment(
    equipment_id: str,
    required: Literal[False]
) -> AHU | None:
    ...
```

Implementation:

```python
def find_equipment(
    equipment_id: str,
    required: bool
) -> AHU | None:

    equipment = database_lookup(equipment_id)

    if equipment is None and required:
        raise ValueError("Equipment not found")

    return equipment
```

Ab:

```python
equipment = find_equipment(
    "AHU-001",
    True
)
```

Type:

```text
AHU
```

Lekin:

```python
equipment = find_equipment(
    "AHU-001",
    False
)
```

Type:

```text
AHU | None
```

Yeh static typing mein kaafi powerful hai.

---

# 15. Overload aur runtime dispatch different cheezen hain

Yeh confusion avoid karo.

Python mein:

```python
@overload
def foo(x: int) -> int:
    ...


@overload
def foo(x: str) -> str:
    ...


def foo(x):
    ...
```

Python runtime yeh nahi karta:

```text
int → first function
str → second function
```

Instead:

```text
                foo()
                  │
                  ↓
         ONE implementation
                  │
          ┌───────┴───────┐
          ↓               ↓
        int             str
          ↓               ↓
       branch           branch
```

`@overload` type checker ko information deta hai.

---

# 16. Agar mujhe actual runtime multiple methods chahiye?

Python mein `@overload` uske liye nahi hai.

Aap implementation mein dispatch karoge:

```python
def process(value):
    if isinstance(value, int):
        return process_int(value)

    if isinstance(value, str):
        return process_string(value)

    raise TypeError("Unsupported type")
```

Ya advanced architecture mein:

```text
singledispatch
```

use kiya ja sakta hai.

`functools.singledispatch` runtime dispatch ke liye hai.

Difference:

```text
typing.overload
    ↓
static type checking


singledispatch
    ↓
runtime dispatch
```

---

# 17. `overload` + Generic

Ab advanced level.

Suppose:

```python
from typing import TypeVar, overload

T = TypeVar("T")
```

Function list ka first element return karta hai:

```python
@overload
def first(items: list[T]) -> T:
    ...


def first(items):
    return items[0]
```

Actually simple generic function ke liye overload zaroori nahi:

```python
def first(items: list[T]) -> T:
    return items[0]
```

already enough hai.

Isliye:

> Har generic function ke saath overload use nahi karna.

Overload tab use karo jab **different signatures ka different type behavior** ho.

---

# 18. Overload + sequence

Suppose function tuple return karta hai based on input:

```python
@overload
def get_result(value: int) -> tuple[int, str]:
    ...


@overload
def get_result(value: str) -> tuple[str, int]:
    ...


def get_result(value: int | str):
    if isinstance(value, int):
        return value, "number"

    return value, len(value)
```

Type checker:

```python
a = get_result(10)
```

knows:

```text
tuple[int, str]
```

while:

```python
b = get_result("hello")
```

knows:

```text
tuple[str, int]
```

---

# 19. `@overload` implementation signature

Implementation usually broad honi chahiye.

Example:

```python
@overload
def convert(value: int) -> str:
    ...


@overload
def convert(value: float) -> str:
    ...


def convert(value: int | float) -> str:
    return str(value)
```

Implementation:

```python
int | float
```

dono overloads ko accept kar sakti hai.

---

# 20. Implementation return type bhi compatible honi chahiye

Example:

```python
@overload
def convert(value: int) -> int:
    ...


@overload
def convert(value: str) -> str:
    ...


def convert(value: int | str) -> int | str:
    ...
```

Yeh logical hai.

Implementation:

```text
accepts all overload inputs
        +
can return all overload outputs
```

---

# 21. Ek subtle concept: overload signatures vs implementation

Think of this:

```python
@overload
def foo(x: int) -> str:
    ...


@overload
def foo(x: str) -> int:
    ...


def foo(x: int | str) -> str | int:
    ...
```

Top two:

```text
PUBLIC TYPE API
```

Last:

```text
RUNTIME IMPLEMENTATION
```

Yani overload signatures **API contract** ki tarah kaam karti hain.

---

# 22. Real-world API design

Suppose equipment loader:

```python
@overload
def load_equipment(
    equipment_id: str,
    as_dict: Literal[True]
) -> dict:
    ...


@overload
def load_equipment(
    equipment_id: str,
    as_dict: Literal[False]
) -> Equipment:
    ...


def load_equipment(
    equipment_id: str,
    as_dict: bool
) -> dict | Equipment:

    equipment = database_load(equipment_id)

    if as_dict:
        return {
            "equipment_id": equipment.equipment_id,
            "floor": equipment.floor
        }

    return equipment
```

Ab caller:

```python
data = load_equipment(
    "AHU-001",
    True
)
```

knows:

```text
dict
```

while:

```python
equipment = load_equipment(
    "AHU-001",
    False
)
```

knows:

```text
Equipment
```

Yeh large applications mein excellent type API bana sakta hai.

---

# 23. `overload` ka sabse important use case

Aap isko formula se yaad rakho:

```text
Input A → Output A
Input B → Output B
Input C → Output C
```

Example:

```python
@overload
def parse(x: int) -> float:
    ...


@overload
def parse(x: str) -> datetime:
    ...
```

Meaning:

```text
int
 ↓
float

str
 ↓
datetime
```

Agar sirf:

```python
def parse(x: int | str) -> float | datetime:
```

likho, to relationship weak ho jata hai.

---

# 24. `overload` vs `TypeGuard`

Dono ko confuse mat karna.

### `TypeGuard`

Function **input ko inspect** karke type narrow karta hai:

```python
def is_ahu(value: object) -> TypeGuard[AHU]:
    ...
```

Meaning:

```text
check
 ↓
narrow type
```

### `overload`

Function ke **different input signatures ke return types** describe karta hai:

```python
@overload
def get(x: int) -> AHU:
    ...


@overload
def get(x: str) -> VAV:
    ...
```

Meaning:

```text
input type
   ↓
corresponding output type
```

---

# 25. `overload` vs Generic

### Generic

Relationship usually same type ko preserve karta hai:

```python
T = TypeVar("T")

def identity(value: T) -> T:
    return value
```

```text
int → int
str → str
AHU → AHU
```

### Overload

Different input types ke liye completely different return behavior define kar sakta hai:

```text
int → AHU
str → VAV
```

Yani:

```text
Generic
→ type relationship preserve

overload
→ multiple signatures / relationships describe
```

---

# 26. `overload` vs Union

Isko strongly yaad rakho:

```python
def process(x: int | str) -> int | str:
```

says:

> Input int ya str ho sakta hai, output int ya str ho sakta hai.

Lekin:

```python
@overload
def process(x: int) -> int:
    ...


@overload
def process(x: str) -> str:
    ...
```

says:

> Int doge → int milega.
> Str doge → str milega.

**Overload input-output correlation preserve karta hai.**

---

# 27. Advanced example — work-order system

Aapke work-order architecture ke context mein:

```python
from dataclasses import dataclass
from typing import Literal, overload


@dataclass
class WorkOrder:
    number: str
    description: str


@dataclass
class WorkOrderSummary:
    number: str
```

Function:

```python
@overload
def get_work_order(
    number: str,
    summary: Literal[True]
) -> WorkOrderSummary:
    ...


@overload
def get_work_order(
    number: str,
    summary: Literal[False]
) -> WorkOrder:
    ...


def get_work_order(
    number: str,
    summary: bool
) -> WorkOrderSummary | WorkOrder:

    if summary:
        return WorkOrderSummary(number)

    return WorkOrder(
        number,
        "HVAC Preventive Maintenance"
    )
```

Caller:

```python
wo = get_work_order(
    "WO-1001",
    True
)
```

Type checker:

```text
wo → WorkOrderSummary
```

Aur:

```python
wo = get_work_order(
    "WO-1001",
    False
)
```

Type checker:

```text
wo → WorkOrder
```

---

# 28. Ek dangerous mistake

Overload mein yeh mat karo:

```python
@overload
def get(x: int) -> str:
    ...


@overload
def get(x: int) -> int:
    ...
```

Same input:

```text
int
```

ke liye contradictory return types hain.

Caller:

```python
get(10)
```

par type checker ko clear answer nahi milega.

Overloads ka purpose **unambiguous type relationship** dena hai.

---

# 29. Another mistake — implementation ko overload samajhna

Galat mental model:

```python
@overload
def foo(x: int) -> int:
    return x * 2
```

`@overload` declaration ko runtime implementation ke taur par use nahi karna chahiye.

Correct:

```python
@overload
def foo(x: int) -> int:
    ...


@overload
def foo(x: str) -> str:
    ...


def foo(x: int | str) -> int | str:
    if isinstance(x, int):
        return x * 2

    return x.upper()
```

---

# 30. Final mental model

`typing.overload` ko is tarah visualize karo:

```text
                    ONE FUNCTION
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       Signature 1    Signature 2    Signature 3
          │              │              │
       int → int      str → str      bool → float
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                ONE implementation
```

### Core purpose:

```text
@overload
```

**Python ko runtime par multiple functions nahi deta.**

Yeh **static type checker ko batata hai ke function ke different input forms ke corresponding return types kya hain.**

---

## `overload` kab use karna hai?

Use karo jab:

* same function ke multiple valid calling patterns hon
* input ke according return type change hota ho
* `Literal` ke according return type change hota ho
* API/library ko precise type information deni ho
* static type checker ko input-output relationship samjhana ho

Use na karo jab:

* simple `Union` sufficient ho
* simple `Generic[T]` relationship express kar raha ho
* runtime dispatch chahiye — uske liye `singledispatch`/manual dispatch dekho
* sirf function ke multiple implementations banana hain

### Ek line mein:

> **`Generic` type relationship ko generalize karta hai, `TypeGuard` type ko narrow karta hai, aur `overload` ek function ke multiple input → output type contracts ko precisely describe karta hai.**
# Lesson 66 — `typing.cast()` — Type Casting

Ab hum `typing.cast()` ko **basic se advanced level** tak samjhenge.

Sab se pehle ek important baat:

> **`cast()` runtime par value ka type change nahi karta.**
> Yeh sirf **static type checker ko batata hai: "is value ko is type ke taur par treat karo."**

Yeh distinction bohot important hai.

---

# 1. `cast()` kya hai?

Python mein:

```python
from typing import cast
```

phir:

```python
value = cast(int, something)
```

Iska matlab:

> Type checker, `something` ko `int` samjho.

Lekin runtime par `something` wahi object rehta hai.

---

# 2. Sabse simple example

```python
from typing import cast

value = "100"

number = cast(int, value)

print(number)
```

Output:

```text
100
```

Lekin yahan ek dangerous misconception hai:

```python
number = cast(int, value)
```

**`"100"` ko integer `100` mein convert nahi karta.**

Actual runtime:

```python
type(number)
```

hoga:

```text
<class 'str'>
```

Yani:

```text
cast(int, "100")
        ↓
"100" hi rehta hai
```

---

# 3. `cast()` vs `int()`

Yeh difference strongly yaad rakho.

### `int()`

```python
value = "100"

number = int(value)
```

Runtime conversion hoti hai:

```text
str
 ↓
int
```

Result:

```python
type(number)
```

```text
<class 'int'>
```

### `cast()`

```python
value = "100"

number = cast(int, value)
```

Runtime conversion nahi hoti:

```text
str
 ↓
str
```

Sirf static type checker ke perspective se:

```text
str
 ↓
"treat as int"
```

---

# 4. Ek simple analogy

Socho ek box par label laga hai:

```text
BOX
Actual object: String
```

Aap:

```python
cast(int, box)
```

karte ho.

Aapne **box ke andar object change nahi kiya**.

Sirf type checker ko bola:

```text
"Isko int samajh kar type-check karo."
```

---

# 5. `cast()` ka actual purpose

Question:

> Jab runtime type change nahi hota to phir `cast()` ki zaroorat kyun?

Answer:

**Static type checker kabhi-kabhi woh information nahi samajh pata jo programmer already jaanta hai.**

Example:

```python
def get_value() -> object:
    return 100
```

Ab:

```python
value = get_value()
```

Type checker ke according:

```text
value → object
```

Lekin programmer jaanta hai:

```text
actual value → int
```

Ab:

```python
number = cast(int, value)
```

Type checker ko:

```text
number → int
```

samajh aa jayega.

---

# 6. Runtime aur static world

Yeh entire concept do worlds mein samjho:

```text
             Python program
                   │
          ┌────────┴────────┐
          │                 │
       Runtime          Type checker
          │                 │
      actual object      static type
          │                 │
       unchanged        cast affects this
```

`cast()` mainly right side ko affect karta hai.

```text
Runtime:
object same

Type checker:
type assumption changes
```

---

# 7. Example with `object`

```python
from typing import cast


def get_data() -> object:
    return "AHU-001"


data = get_data()
```

Type checker:

```text
data → object
```

Lekin humein pata hai actual value string hai.

```python
equipment_id = cast(str, data)
```

Ab static type:

```text
equipment_id → str
```

Aur:

```python
equipment_id.upper()
```

type checker ko valid lagega.

---

# 8. Lekin cast verify nahi karta

Yeh sabse important warning hai.

```python
data: object = 100

equipment_id = cast(str, data)
```

Ab type checker maan lega:

```text
equipment_id → str
```

Lekin actual object:

```text
int
```

hai.

Ab:

```python
equipment_id.upper()
```

runtime par:

```text
AttributeError
```

aa sakta hai.

### Isliye:

```text
cast()
≠ validation
```

---

# 9. `cast()` programmer ka promise hai

Isko is tarah yaad karo:

```text
cast()
   ↓
"Type checker, mujh par trust karo."
```

Yani:

> Programmer static analyzer ko ek assertion de raha hai ke value is type ki hai.

Agar programmer galat hai:

```text
cast()
   ↓
false assumption
   ↓
runtime error
```

ho sakta hai.

---

# 10. `cast()` vs `TypeGuard`

Aapne previous lessons mein `TypeGuard` padha hai. Dono ka difference bohot important hai.

### `TypeGuard`

Runtime par **check** karta hai:

```python
def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

Yahan:

```text
actual check
      ↓
True
      ↓
type narrowing
```

### `cast()`

Koi check nahi:

```python
value = cast(str, value)
```

Yahan:

```text
NO CHECK
   ↓
programmer assertion
```

---

# 11. Compare

### Safe narrowing

```python
if isinstance(value, str):
    print(value.upper())
```

Python runtime par verify karta hai.

### `TypeGuard`

```python
if is_string(value):
    print(value.upper())
```

Custom runtime check + static narrowing.

### `cast`

```python
value = cast(str, value)
print(value.upper())
```

Koi runtime verification nahi.

---

# 12. `cast()` ka common use — `dict`

Suppose API data:

```python
data: object = {
    "equipment_id": "AHU-001",
    "airflow": 1200
}
```

Aapko pata hai yeh dictionary hai:

```python
from typing import cast

equipment_data = cast(dict[str, object], data)
```

Ab:

```python
equipment_data["equipment_id"]
```

type checker ko dictionary access samajh aa jayega.

Lekin again:

```python
cast(dict[str, object], data)
```

dictionary **banata nahi hai**.

---

# 13. `cast()` ka powerful use — external data

Real-world programs mein data aksar aata hai:

```text
API
 ↓
JSON
 ↓
database
 ↓
CSV
 ↓
environment variables
 ↓
third-party library
```

Type checker ko har external source ki exact structure nahi pata hoti.

Example:

```python
response: object = api.get_response()
```

Aapko API contract pata hai:

```python
dict[str, object]
```

to:

```python
response_data = cast(
    dict[str, object],
    response
)
```

---

# 14. Lekin structured data mein `cast()` akela enough nahi

Suppose:

```python
data = cast(dict[str, object], response)
```

Ab:

```python
airflow = data["airflow"]
```

Type checker ke liye:

```text
airflow → object
```

Abhi bhi exact type unknown hai.

Aapko further validation karni padegi:

```python
if isinstance(airflow, int | float):
    ...
```

Ya proper model/schema validation use karo.

---

# 15. `cast()` + Protocol

Yeh advanced aur useful example hai.

```python
from typing import Protocol, cast


class EquipmentController(Protocol):
    def start(self) -> None:
        ...
```

Suppose third-party object:

```python
controller = get_controller()
```

Type checker ke paas exact type information nahi:

```text
controller → object
```

Lekin aapko architecture pata hai ke object `start()` provide karta hai.

```python
controller = cast(
    EquipmentController,
    controller
)
```

Ab:

```python
controller.start()
```

static type checker ke liye valid hai.

---

# 16. Lekin Protocol ke saath bhi cast dangerous ho sakta hai

Agar object mein:

```python
start()
```

hai hi nahi:

```python
controller = cast(
    EquipmentController,
    wrong_object
)
```

to `cast()` error nahi dega.

Runtime par:

```python
controller.start()
```

fail karega.

Isliye agar runtime safety chahiye:

```python
isinstance(...)
```

ya proper validation use karo.

---

# 17. `cast()` + `TypeVar`

Ab typing architecture ke context mein.

```python
from typing import TypeVar, cast

T = TypeVar("T")


def get_value(value: object) -> T:
    return cast(T, value)
```

Technically possible hai, lekin yahan **bahut careful** rehna chahiye.

Example:

```python
number = get_value[int](100)
```

Conceptually type checker ko:

```text
number → int
```

bataya gaya.

Lekin function ne runtime par actual verification nahi ki.

Isliye generic `cast()` APIs ko blindly use karna unsafe design ho sakta hai.

---

# 18. `cast()` + `None`

Suppose:

```python
from typing import cast

value: str | None = get_name()
```

Aapko guaranteed pata hai ke is point par `None` nahi ho sakta:

```python
name = cast(str, value)
```

Ab static type:

```text
name → str
```

Lekin agar actual:

```python
value = None
```

hua:

```text
cast(str, None)
```

runtime par `None` hi rahega.

Yani:

```python
name.upper()
```

fail karega.

---

# 19. Better alternative: explicit check

Agar uncertainty real hai:

```python
if value is None:
    raise ValueError("Name missing")

name = value
```

Yeh `cast()` se safer hai.

Rule:

> **Agar runtime par value uncertain hai, pehle validate karo.**

---

# 20. `cast()` ka ek common misconception

Kuch beginners sochte hain:

```python
x = cast(int, "123")
```

same as:

```python
x = int("123")
```

Bilkul nahi.

### `int()`

```text
"123"
 ↓
123
```

### `cast()`

```text
"123"
 ↓
"123"
```

sirf static type checker ke liye assumption change hoti hai.

---

# 21. `cast()` aur `assert`

Dono kabhi similar situation solve kar sakte hain, lekin behavior different hai.

### `assert`

```python
assert isinstance(value, str)

value.upper()
```

Runtime verification karta hai.

### `cast`

```python
value = cast(str, value)

value.upper()
```

Runtime verification nahi karta.

So:

```text
assert
→ check + type narrowing

cast
→ no check + type assertion
```

---

# 22. `cast()` aur `TypeIs`

Previous lesson se connect karo.

### `TypeIs`

```python
def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

Runtime:

```text
actual check
```

Static:

```text
type narrowing
```

### `cast`

```python
value = cast(str, value)
```

Runtime:

```text
nothing
```

Static:

```text
type assumption
```

---

# 23. `cast()` ka use kab genuinely useful hai?

### Case 1 — Type checker ko information missing hai

```python
value: object
```

Lekin architecture guarantee karta hai:

```text
actual → Equipment
```

Then:

```python
equipment = cast(Equipment, value)
```

---

### Case 2 — Third-party library typing incomplete hai

Library actual mein correct object return kar rahi hai, lekin its type hints too broad hain.

```python
result: object = library_function()
```

Aap:

```python
result = cast(MyExpectedType, result)
```

kar sakte ho.

---

### Case 3 — Framework/metaprogramming

Some frameworks dynamically attributes/methods create karte hain.

Static checker ko runtime behavior pata nahi hota.

`cast()` bridge ka kaam kar sakta hai.

---

### Case 4 — Legacy code

Purane untyped code ke saath gradually typing add karte waqt `cast()` useful ho sakta hai.

---

# 24. Kab `cast()` use nahi karna chahiye?

Agar simple type narrowing possible hai:

```python
if isinstance(value, str):
    ...
```

to unnecessary:

```python
cast(str, value)
```

mat karo.

Agar conversion chahiye:

```python
int(value)
float(value)
str(value)
```

use karo.

Agar validation chahiye:

```python
isinstance()
assert
TypeGuard
TypeIs
```

use karo.

---

# 25. `cast()` ko "conversion" mat samajhna

Ek very strong rule:

```text
CAST ≠ CONVERT
```

### Conversion

```python
int("10")
```

actual object change karta hai.

### Cast

```python
cast(int, "10")
```

actual object nahi change karta.

---

# 26. HVAC practical example

Suppose equipment loader ka return type broad hai:

```python
from typing import cast


def load_equipment() -> object:
    return {
        "equipment_id": "AHU-001",
        "airflow": 1200
    }
```

Agar aap simply:

```python
data = load_equipment()
```

karte ho:

```text
data → object
```

Lekin architecture mein aapko pata hai:

```text
data → dict[str, int | str]
```

To:

```python
data = cast(
    dict[str, int | str],
    load_equipment()
)
```

Ab static checker dictionary operations ko samajh sakta hai.

Lekin actual runtime object wahi dictionary hai.

---

# 27. Better architecture — `TypedDict`

Agar dictionary ka exact structure known hai, `cast()` ko `TypedDict` ke saath use karna useful ho sakta hai.

```python
from typing import TypedDict, cast


class AHUData(TypedDict):
    equipment_id: str
    airflow: float
```

External data:

```python
raw_data: object = load_equipment()
```

Cast:

```python
ahu_data = cast(
    AHUData,
    raw_data
)
```

Ab:

```python
ahu_data["equipment_id"]
```

type:

```text
str
```

Aur:

```python
ahu_data["airflow"]
```

type:

```text
float
```

### Lekin:

`TypedDict` bhi runtime validation nahi karta.

Aur `cast()` bhi validation nahi karta.

Dono static typing tools hain.

---

# 28. `cast()` + TypedDict ka danger

Suppose actual API:

```python
{
    "equipment_id": "AHU-001",
    "airflow": "1200"
}
```

lekin TypedDict:

```python
class AHUData(TypedDict):
    equipment_id: str
    airflow: float
```

hai.

Aap:

```python
ahu_data = cast(AHUData, raw_data)
```

kar doge.

Type checker khush.

Runtime actual:

```text
airflow → str
```

hai.

Expected:

```text
airflow → float
```

hai.

Yani `cast()` **bad external data ko correct nahi karta**.

---

# 29. Validation vs cast architecture

Production application mein:

```text
External data
      ↓
Validation
      ↓
Correct model
      ↓
Business logic
```

better architecture hai.

`cast()` ka use:

```text
Static type checker ki missing information
```

ko solve karne ke liye karo.

Not:

```text
Bad/unknown external data
```

ko magically safe banane ke liye.

---

# 30. `cast()` ka syntax

Basic:

```python
cast(Type, expression)
```

Examples:

```python
cast(int, value)

cast(str, value)

cast(Equipment, value)

cast(list[str], value)

cast(dict[str, int], value)

cast(AHUData, value)
```

Important:

```python
cast(...)
```

expression ko evaluate karta hai, lekin usko convert nahi karta.

---

# 31. Runtime mein `cast()` kya return karta hai?

Conceptually `cast()` almost identity operation jaisa hai:

```python
value = "hello"

result = cast(int, value)

print(result is value)
```

Result:

```text
True
```

Yani same object return hota hai.

Conceptually:

```python
cast(int, value)
```

roughly:

```python
value
```

jaisa runtime behavior rakhta hai.

---

# 32. Ek aur important point

`cast()` ka type argument runtime par generally meaningful validation ke liye use nahi hota.

```python
cast(int, value)
```

ka matlab yeh nahi:

```python
if not isinstance(value, int):
    raise TypeError(...)
```

Aisa koi automatic check nahi.

---

# 33. Previous lessons se complete connection

Ab tak humne jo typing tools padhe hain unka relationship dekho:

```text
TypeVar
   ↓
type relationship define


Generic
   ↓
reusable typed architecture


Protocol
   ↓
behavior contract


Variance
   ↓
substitution direction


TypeGuard
   ↓
custom runtime check + narrowing


TypeIs
   ↓
two-way narrowing


overload
   ↓
input → output type relationship


cast
   ↓
type checker ko programmer assertion
```

`cast()` in sab mein sabse zyada **"trust me"** wala mechanism hai.

---

# 34. Golden rule

Isko yaad kar lo:

```text
Type checker confused?
        ↓
cast() MAY help


Runtime value uncertain?
        ↓
cast() DOES NOT help


Runtime conversion required?
        ↓
int(), str(), float(), etc.


Runtime validation required?
        ↓
isinstance(), validation, TypeGuard, TypeIs
```

---

# 35. Final practical example

```python
from typing import TypedDict, cast


class EquipmentData(TypedDict):
    equipment_id: str
    floor: str
    airflow: float


def load_raw_data() -> object:
    return {
        "equipment_id": "MEP-AHU-001",
        "floor": "Thirty Four Floor",
        "airflow": 1200.0
    }


raw = load_raw_data()

equipment = cast(
    EquipmentData,
    raw
)

print(equipment["equipment_id"])
print(equipment["floor"])
print(equipment["airflow"])
```

Static type checker ke perspective se:

```text
raw
 ↓
object

cast(EquipmentData, raw)
 ↓
EquipmentData

equipment["equipment_id"]
 ↓
str

equipment["airflow"]
 ↓
float
```

Lekin runtime par:

```text
raw
 ↓
actual dict

cast(...)
 ↓
same actual dict
```

---

## Sabse important 5 points

1. **`cast()` runtime conversion nahi karta.**
2. **`cast()` static type checker ko type assumption deta hai.**
3. **`cast()` runtime validation nahi karta.**
4. **Galat cast runtime error cause kar sakta hai.**
5. **Jahan `isinstance()`, `TypeGuard`, `TypeIs`, ya actual conversion better solution ho, wahan unnecessary `cast()` avoid karo.**

### One-line definition

> **`typing.cast(T, value)` ka matlab hai: "Runtime par value ko change mat karo, lekin static type checker ke liye is value ko `T` samjho."**
# Lesson 67 — `typing.Annotated` + Metadata

Ab hum Python typing ka ek interesting concept dekhte hain:

```python
typing.Annotated
```

Iska main purpose hai:

> **Kisi type ke saath additional metadata attach karna, bina us type ko change kiye.**

Yeh concept modern Python frameworks mein bohot important hai, especially **validation, API schemas, dependency injection, serialization, configuration aur data models** mein.

---

# 1. Sab se basic example

```python
from typing import Annotated

temperature: Annotated[float, "Celsius"]
```

Yahan actual type:

```text
float
```

hai.

Aur extra metadata:

```text
"Celsius"
```

hai.

Mental model:

```text
Annotated[
    TYPE,
    METADATA
]
```

So:

```python
Annotated[float, "Celsius"]
```

means:

```text
Type:
    float

Metadata:
    "Celsius"
```

---

# 2. Important: Metadata type nahi hai

Yeh:

```python
Annotated[float, "Celsius"]
```

ka matlab yeh nahi:

```text
Celsius ek naya Python type hai
```

Actual underlying type:

```python
float
```

hi hai.

So:

```python
temperature: Annotated[float, "Celsius"]
```

still fundamentally:

```text
float
```

hai.

---

# 3. `Annotated` kyun banaya gaya?

Suppose:

```python
temperature: float
```

Type checker ko pata hai:

```text
temperature → float
```

Lekin usko yeh nahi pata:

```text
Celsius?
Fahrenheit?
Kelvin?
```

Aap metadata attach kar sakte ho:

```python
temperature: Annotated[
    float,
    "Celsius"
]
```

Ab:

```text
Type:
float

Extra information:
Celsius
```

Yeh **type ko replace nahi karta**, balki uske saath information attach karta hai.

---

# 4. Multiple metadata

`Annotated` mein multiple metadata items de sakte ho:

```python
from typing import Annotated

temperature: Annotated[
    float,
    "Celsius",
    "HVAC sensor",
    "validated"
]
```

Structure:

```text
Annotated[
    float,          ← actual type
    "Celsius",      ← metadata 1
    "HVAC sensor",  ← metadata 2
    "validated"     ← metadata 3
]
```

---

# 5. Ek practical HVAC example

Suppose AHU ka airflow:

```python
airflow: float
```

Lekin humein additional information chahiye:

```text
unit = CFM
minimum = 0
maximum = 5000
```

Hum likh sakte hain:

```python
from typing import Annotated

airflow: Annotated[
    float,
    "unit=CFM",
    "min=0",
    "max=5000"
]
```

Actual type:

```text
float
```

Metadata:

```text
unit=CFM
min=0
max=5000
```

---

# 6. Metadata sirf strings hona zaroori nahi

Yeh bohot important hai.

Metadata mein arbitrary Python objects ho sakte hain.

Example:

```python
airflow: Annotated[
    float,
    0,
    5000,
    "CFM"
]
```

Ya custom object:

```python
class Range:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
```

Then:

```python
airflow: Annotated[
    float,
    Range(0, 5000)
]
```

Yahan metadata ek actual `Range` object hai.

---

# 7. Metadata retrieve kaise karein?

Yahan `typing.get_type_hints()` important hai.

Simple:

```python
from typing import Annotated, get_type_hints


def read_sensor(
    temperature: Annotated[
        float,
        "Celsius"
    ]
):
    pass
```

Agar:

```python
print(get_type_hints(read_sensor))
```

normally dekho, metadata preserve karne ke liye:

```python
include_extras=True
```

use karte hain:

```python
print(
    get_type_hints(
        read_sensor,
        include_extras=True
    )
)
```

---

# 8. `include_extras=True` kyun?

By default:

```python
get_type_hints()
```

extra metadata ko strip kar sakta hai.

Example:

```python
get_type_hints(read_sensor)
```

result conceptually:

```python
{
    "temperature": float
}
```

Lekin:

```python
get_type_hints(
    read_sensor,
    include_extras=True
)
```

result:

```python
{
    "temperature": Annotated[
        float,
        "Celsius"
    ]
}
```

Yani:

```text
include_extras=True
        ↓
metadata preserve karo
```

---

# 9. `get_origin()` aur `get_args()`

Advanced inspection ke liye:

```python
from typing import (
    Annotated,
    get_origin,
    get_args
)
```

Example:

```python
from typing import Annotated, get_origin, get_args

Temperature = Annotated[
    float,
    "Celsius"
]

print(get_origin(Temperature))
print(get_args(Temperature))
```

Conceptually output:

```text
<class 'typing.Annotated'>
(float, 'Celsius')
```

So:

```python
get_origin(...)
```

batata hai:

> Yeh typing construct kya hai?

Aur:

```python
get_args(...)
```

batata hai:

> Iske andar kya arguments hain?

---

# 10. `get_args()` ka structure

For:

```python
Annotated[
    float,
    "Celsius",
    "Sensor"
]
```

`get_args()` roughly:

```python
(
    float,
    "Celsius",
    "Sensor"
)
```

First item:

```text
float
```

actual type hai.

Baaki:

```text
"Celsius"
"Sensor"
```

metadata hain.

---

# 11. Custom metadata object

Real architecture mein strings se better custom metadata objects ho sakte hain.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float
```

Ab:

```python
from typing import Annotated

Airflow = Annotated[
    float,
    Range(0, 5000)
]
```

Yahan:

```text
Airflow
  ↓
float
  +
Range metadata
```

---

# 12. Multiple metadata objects

```python
from dataclasses import dataclass
from typing import Annotated


@dataclass(frozen=True)
class Unit:
    name: str


@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float


Airflow = Annotated[
    float,
    Unit("CFM"),
    Range(0, 5000)
]
```

Ab ek type ke saath structured metadata hai:

```text
float
 │
 ├── Unit("CFM")
 │
 └── Range(0, 5000)
```

Yeh large applications mein kaafi powerful architecture bana sakta hai.

---

# 13. `Annotated` ka type alias

Aap reusable type bana sakte ho:

```python
Airflow = Annotated[
    float,
    Unit("CFM"),
    Range(0, 5000)
]
```

Phir:

```python
class AHU:
    airflow: Airflow
```

Aur:

```python
class VAV:
    airflow: Airflow
```

Dono same semantic information use karenge.

---

# 14. `Annotated` type safety ko replace nahi karta

Suppose:

```python
Temperature = Annotated[
    float,
    "Celsius"
]
```

Aap:

```python
temperature: Temperature = "hello"
```

assign karoge to static type checker ko problem hogi.

Kyun?

Because underlying type:

```text
float
```

hai.

Metadata:

```text
"Celsius"
```

sirf extra information hai.

---

# 15. Metadata automatically enforce nahi hota

Yeh extremely important hai.

Aap likho:

```python
Airflow = Annotated[
    float,
    Range(0, 5000)
]
```

iska matlab **automatically** yeh nahi hai ke Python:

```python
airflow = 10000
```

par error throw karega.

`Annotated` khud validation nahi karta.

Yani:

```text
Annotated
    ↓
metadata attach
```

not:

```text
Annotated
    ↓
automatic validation
```

---

# 16. Validation framework ka role

Agar koi framework `Annotated` metadata ko understand karta hai, woh us metadata ko use karke validation kar sakta hai.

Conceptually:

```text
Annotated
    ↓
Metadata
    ↓
Framework reads metadata
    ↓
Validation / schema / dependency injection
```

Lekin plain Python:

```text
Annotated
    ↓
metadata available
```

bas itna hi karta hai.

---

# 17. `Annotated` + custom validator metadata

Suppose:

```python
@dataclass(frozen=True)
class MinValue:
    value: float
```

Then:

```python
Temperature = Annotated[
    float,
    MinValue(-40)
]
```

Aur:

```python
temperature: Temperature
```

Aapka custom framework inspect kar sakta hai:

```text
type = float
minimum = -40
```

phir validation perform kar sakta hai.

---

# 18. Real-world architecture

Imagine HVAC configuration:

```python
from typing import Annotated


Temperature = Annotated[
    float,
    Unit("°C"),
    Range(-40, 80)
]


Airflow = Annotated[
    float,
    Unit("CFM"),
    Range(0, 10000)
]


DamperPosition = Annotated[
    float,
    Unit("%"),
    Range(0, 100)
]
```

Ab:

```python
class AHUConfig:
    temperature: Temperature
    airflow: Airflow
    damper: DamperPosition
```

Aapke model mein:

```text
temperature
    ↓
float + °C + -40..80

airflow
    ↓
float + CFM + 0..10000

damper
    ↓
float + % + 0..100
```

Yeh **semantic typing** ke qareeb architecture hai.

---

# 19. `Annotated` vs `NewType`

Dono ko confuse mat karna.

### `Annotated`

```python
Temperature = Annotated[
    float,
    "Celsius"
]
```

Underlying type:

```text
float
```

Metadata attach hota hai.

### `NewType`

```python
from typing import NewType

Temperature = NewType(
    "Temperature",
    float
)
```

Yeh static typing mein ek **distinct type identity** create karta hai.

Mental model:

```text
Annotated
→ same type + metadata

NewType
→ distinct static type
```

---

# 20. `Annotated` vs TypeAlias

Simple alias:

```python
Temperature = float
```

sirf alias hai.

Annotated:

```python
Temperature = Annotated[
    float,
    "Celsius"
]
```

type ke saath metadata bhi hai.

So:

```text
float
 ↓
simple alias

Annotated[float, metadata]
 ↓
type + extra information
```

---

# 21. `Annotated` + function parameters

Classes ke ilawa functions mein bhi:

```python
def set_temperature(
    temperature: Annotated[
        float,
        "Celsius",
        "Range: -40..80"
    ]
):
    ...
```

Yeh function signature ko semantic information deta hai.

Agar koi framework function annotations inspect karta hai, woh metadata use kar sakta hai.

---

# 22. `Annotated` + return type

Return type par bhi laga sakte ho:

```python
def read_airflow() -> Annotated[
    float,
    "CFM"
]:
    return 1200.0
```

Meaning:

```text
Return:
    float

Metadata:
    CFM
```

---

# 23. `Annotated` nested types ke saath

Aap:

```python
values: Annotated[
    list[int],
    "Sensor readings"
]
```

likh sakte ho.

Underlying type:

```text
list[int]
```

Metadata:

```text
"Sensor readings"
```

---

# 24. Element vs entire list

Yeh distinction important hai.

### Entire list metadata:

```python
values: Annotated[
    list[int],
    "Sensor readings"
]
```

Meaning:

```text
list[int]
    +
metadata
```

### Individual elements metadata:

```python
values: list[
    Annotated[
        int,
        "Sensor value"
    ]
]
```

Ab metadata **elements ke type** par hai.

Visual:

```text
Annotated[list[int], metadata]
        ↓
poori list


list[Annotated[int, metadata]]
        ↓
har element
```

---

# 25. `Annotated` nested example

```python
from typing import Annotated

SensorValue = Annotated[
    float,
    "raw sensor value"
]

values: list[SensorValue]
```

Yahan:

```text
list
 ├── float + metadata
 ├── float + metadata
 └── float + metadata
```

conceptually semantic structure hai.

---

# 26. Metadata ordering

Suppose:

```python
Temperature = Annotated[
    float,
    Unit("C"),
    Range(-40, 80),
    "HVAC"
]
```

Metadata ka order preserve hota hai.

Conceptually:

```python
(
    Unit("C"),
    Range(-40, 80),
    "HVAC"
)
```

important ho sakta hai agar aapka framework metadata ko sequentially process karta hai.

Isliye metadata ko arbitrary mix na karo agar aap custom framework bana rahe ho.

---

# 27. Nested `Annotated`

Suppose:

```python
A = Annotated[int, "A"]

B = Annotated[A, "B"]
```

Typing system metadata ko flatten kar sakta hai, aur practical introspection mein metadata ordering ko samajhna important ho jata hai.

Conceptually aapko resulting metadata ko:

```text
int
+
A
+
B
```

ki tarah think karna chahiye.

Isliye complex annotation systems mein `get_args()` se actual resolved structure inspect karna useful hai.

---

# 28. `Annotated` + decorators/frameworks

Yahan iska real power aata hai.

Imagine:

```python
def create_work_order(
    number: Annotated[str, "Work Order Number"],
    priority: Annotated[int, Range(1, 5)]
):
    ...
```

Aap ek decorator bana sakte ho jo function annotations inspect kare:

```text
function
   ↓
__annotations__
   ↓
Annotated metadata
   ↓
metadata reader
   ↓
validation / documentation / UI
```

Yani annotation **machine-readable metadata** ban sakti hai.

---

# 29. Documentation generation

Suppose:

```python
def set_airflow(
    airflow: Annotated[
        float,
        Unit("CFM"),
        Range(0, 5000)
    ]
):
    ...
```

Aapka documentation generator automatically produce kar sakta hai:

```text
Parameter:
    airflow

Type:
    float

Unit:
    CFM

Allowed range:
    0–5000
```

Python khud yeh documentation generate nahi karta; aapka tooling/framework metadata read karega.

---

# 30. Dependency Injection

Modern frameworks mein `Annotated` dependency information represent karne ke liye bhi use hota hai.

Conceptually:

```python
def endpoint(
    db: Annotated[Database, "inject database"]
):
    ...
```

Framework:

```text
Annotated
   ↓
Database
   +
"inject database"
   ↓
dependency resolver
```

Yahan metadata **framework instruction** ban sakti hai.

---

# 31. Security / permissions metadata

Example:

```python
UserId = Annotated[
    int,
    "requires authenticated user"
]
```

Ya structured:

```python
@dataclass(frozen=True)
class Permission:
    name: str
```

Then:

```python
UserId = Annotated[
    int,
    Permission("equipment.read")
]
```

Framework inspect karke permission enforce kar sakta hai.

Again:

> `Annotated` khud permission enforce nahi karta.

Framework ko karna hoga.

---

# 32. `Annotated` + `Literal`

Dono alag concepts hain.

```python
status: Literal[
    "Running",
    "Stopped",
    "Fault"
]
```

means:

> Allowed values exactly yeh literals hain.

While:

```python
status: Annotated[
    str,
    "Equipment status"
]
```

means:

> Type `str` hai aur extra metadata attached hai.

Can combine:

```python
status: Annotated[
    Literal[
        "Running",
        "Stopped",
        "Fault"
    ],
    "HVAC equipment status"
]
```

Now:

```text
actual type:
Literal["Running", "Stopped", "Fault"]

metadata:
"HVAC equipment status"
```

---

# 33. `Annotated` + `Final`

Aap multiple typing concepts combine bhi kar sakte ho:

```python
from typing import Annotated, Final

MAX_AIRFLOW: Final[
    Annotated[
        float,
        Unit("CFM")
    ]
] = 5000.0
```

Conceptually:

```text
Final
 ↓
reassignment allowed nahi

Annotated
 ↓
metadata = CFM

float
 ↓
actual type
```

---

# 34. `Annotated` + `ClassVar`

Dataclass architecture mein bhi:

```python
from dataclasses import dataclass
from typing import Annotated, ClassVar


@dataclass
class AHU:
    airflow: Annotated[
        float,
        "CFM"
    ]

    default_airflow: ClassVar[
        Annotated[
            float,
            "CFM"
        ]
    ] = 1200.0
```

Yahan:

```text
airflow
→ instance field

default_airflow
→ class variable

Annotated
→ metadata
```

Teen concepts combine ho rahe hain.

---

# 35. `Annotated` vs `cast`

Previous lesson se connect karo.

### `cast`

```python
value = cast(
    Equipment,
    value
)
```

Meaning:

> Type checker, is value ko `Equipment` samjho.

### `Annotated`

```python
value: Annotated[
    Equipment,
    "loaded from database"
]
```

Meaning:

> Type `Equipment` hai, aur additional metadata attached hai.

So:

```text
cast
→ type assertion


Annotated
→ type + metadata
```

---

# 36. `Annotated` vs `TypeGuard`

### TypeGuard

```python
def is_ahu(x: object) -> TypeGuard[AHU]:
    ...
```

Purpose:

```text
runtime check
     ↓
type narrowing
```

### Annotated

```python
x: Annotated[
    AHU,
    "primary HVAC unit"
]
```

Purpose:

```text
type
 +
metadata
```

---

# 37. Ek production-style example

Ab complete architecture banate hain.

```python
from dataclasses import dataclass
from typing import Annotated


@dataclass(frozen=True)
class Unit:
    name: str


@dataclass(frozen=True)
class Range:
    minimum: float
    maximum: float


Airflow = Annotated[
    float,
    Unit("CFM"),
    Range(0, 5000)
]


Temperature = Annotated[
    float,
    Unit("°C"),
    Range(-40, 80)
]


DamperPosition = Annotated[
    float,
    Unit("%"),
    Range(0, 100)
]


@dataclass
class AHU:
    equipment_id: str
    airflow: Airflow
    temperature: Temperature
    damper: DamperPosition
```

Ab class semantically rich hai:

```text
AHU
│
├── equipment_id
│
├── airflow
│    ├── float
│    ├── CFM
│    └── 0..5000
│
├── temperature
│    ├── float
│    ├── °C
│    └── -40..80
│
└── damper
     ├── float
     ├── %
     └── 0..100
```

---

# 38. Lekin ek important limitation

Yeh code:

```python
ahu = AHU(
    "AHU-001",
    airflow=99999,
    temperature=-500,
    damper=250
)
```

automatically fail nahi karega **sirf `Annotated` ki wajah se**.

Kyun?

Because:

```text
Annotated
    ↓
metadata
```

hai.

Validation engine nahi.

Aapko validator banana padega ya aisa framework use karna padega jo metadata understand karta ho.

---

# 39. Agar custom validator banana ho

Conceptually flow:

```text
AHU
 ↓
annotations inspect
 ↓
Annotated identify
 ↓
Range metadata read
 ↓
actual value check
 ↓
valid / invalid
```

Example metadata:

```python
Range(0, 5000)
```

validator:

```text
value < minimum?
value > maximum?
```

Then error.

Yeh `Annotated` ka advanced architectural use hai.

---

# 40. `Annotated` ka deepest concept

Normal annotation:

```python
airflow: float
```

sirf:

```text
WHAT TYPE?
```

batati hai.

`Annotated`:

```python
airflow: Annotated[
    float,
    Unit("CFM"),
    Range(0, 5000)
]
```

do questions ka answer de sakti hai:

```text
WHAT TYPE?
    ↓
float

WHAT EXTRA SEMANTIC INFORMATION?
    ↓
CFM
0..5000
```

Yani:

> **`Annotated` type information ke saath semantic information carry karne ka mechanism hai.**

---

# 41. Complete comparison

| Feature     | Main purpose               |
| ----------- | -------------------------- |
| `TypeVar`   | Type relationship          |
| `Generic`   | Generic architecture       |
| `Protocol`  | Behavior contract          |
| `TypeGuard` | Custom narrowing           |
| `TypeIs`    | Two-way narrowing          |
| `overload`  | Input → output signatures  |
| `cast`      | Static type assertion      |
| `Annotated` | Type + metadata            |
| `Literal`   | Specific allowed values    |
| `Final`     | Reassignment prevent karna |

---

# 42. Golden rule

Isko yaad rakho:

```text
Annotated[T, metadata]
       ↓
       T
       +
extra information
```

Aur:

```text
Annotated
≠ conversion

Annotated
≠ automatic validation

Annotated
≠ new runtime class

Annotated
= type + metadata
```

### One-line definition:

> **`typing.Annotated[T, metadata...]` ka matlab hai: underlying type `T` same rakho, lekin us type ke saath additional machine-readable metadata attach karo.**

Aur advanced Python architecture mein iska real faida tab aata hai jab **framework, validator, serializer, dependency-injection system, documentation generator, ya aapka khud ka tooling** is metadata ko inspect karke meaningful behavior perform kare.
# Lesson 68 — `typing.Self` — Self Type

Python typing mein **`Self`** ek bohat useful concept hai, especially jab hum **class inheritance, method chaining, fluent APIs, builders, aur subclasses** ke saath kaam karte hain.

Simple words mein:

> **`Self` ka matlab hai: "jis class ke context mein method use ho raha hai, usi actual class ka type."**

---

## 1. Sab se pehle problem samjho

Maan lo:

```python
class Equipment:
    def set_status(self, status: str) -> "Equipment":
        self.status = status
        return self
```

Ab subclass:

```python
class AHU(Equipment):
    def set_airflow(self, airflow: float):
        self.airflow = airflow
        return self
```

Hum ye kar sakte hain:

```python
ahu = AHU()

ahu.set_status("Running").set_airflow(1200)
```

Runtime par ye kaam karega.

Lekin typing ke point of view se problem hai.

`set_status()` ka return type humne:

```python
-> Equipment
```

likha hai.

Type checker kahega:

```text
set_status() returns Equipment
```

Isliye:

```python
ahu.set_status("Running").set_airflow(1200)
```

mein `set_airflow()` ko problem ho sakti hai, kyunki `Equipment` ke andar `set_airflow()` exist nahi karta.

---

# 2. Yahan `Self` kaam aata hai

Python mein:

```python
from typing import Self
```

Ab:

```python
class Equipment:
    def set_status(self, status: str) -> Self:
        self.status = status
        return self
```

Ab subclass:

```python
class AHU(Equipment):
    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self
```

Ab:

```python
ahu = AHU()

ahu.set_status("Running").set_airflow(1200)
```

Type checker samajhta hai:

```text
ahu
 ↓
AHU

set_status()
 ↓
AHU

set_airflow()
 ↓
AHU
```

Yani `Self` automatically **actual subclass type preserve karta hai**.

---

# 3. `Self` ka mental model

Isko yaad rakho:

```text
Self
 ↓
"Current class ka actual type"
```

Example:

```python
class Equipment:
    def reset(self) -> Self:
        return self
```

Agar:

```python
equipment = Equipment()
```

to:

```python
equipment.reset()
```

ka type:

```text
Equipment
```

Lekin:

```python
class AHU(Equipment):
    pass
```

aur:

```python
ahu = AHU()
```

to:

```python
ahu.reset()
```

ka type:

```text
AHU
```

**Isi ko Self type kehte hain.**

---

# 4. `Self` aur normal class return type mein difference

### Without `Self`

```python
class Equipment:
    def reset(self) -> "Equipment":
        return self
```

Subclass:

```python
class AHU(Equipment):
    def set_airflow(self, airflow: float):
        self.airflow = airflow
        return self
```

```python
ahu = AHU()

result = ahu.reset()
```

Static typing ke hisaab se:

```text
result -> Equipment
```

---

### With `Self`

```python
from typing import Self

class Equipment:
    def reset(self) -> Self:
        return self
```

Ab:

```python
result = ahu.reset()
```

Type:

```text
AHU
```

Yahi main benefit hai.

---

# 5. `Self` inheritance ko preserve karta hai

Example:

```python
from typing import Self


class Equipment:
    def start(self) -> Self:
        print("Equipment started")
        return self


class AHU(Equipment):
    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self
```

Ab:

```python
ahu = AHU()

ahu.start().set_airflow(1500)
```

Flow:

```text
AHU
 ↓
start()
 ↓
Self = AHU
 ↓
set_airflow()
```

Agar `start()` mein `Equipment` return type hota:

```python
def start(self) -> Equipment:
```

to chaining ka type relationship toot jata.

---

# 6. Fluent API mein `Self` bohat important hai

Fluent API ka matlab hai methods ko chain karna:

```python
object.method1().method2().method3()
```

Example:

```python
from typing import Self


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
```

Use:

```python
query = Query()

query \
    .filter("temperature > 25") \
    .order_by("temperature") \
    .limit(10)
```

Har method:

```python
-> Self
```

return kar raha hai.

Isliye type checker janta hai ke chain mein object ka actual type same rahega.

---

# 7. Subclass mein iska real power

Ab:

```python
class EquipmentQuery(Query):

    def equipment_type(self, name: str) -> Self:
        print("Equipment:", name)
        return self
```

Ab:

```python
query = EquipmentQuery()

query \
    .filter("status = 'Running'") \
    .equipment_type("AHU") \
    .limit(10)
```

`filter()` parent class ka method hai.

Lekin uska return:

```python
Self
```

hai.

Isliye type checker samajhta hai:

```text
EquipmentQuery.filter()
        ↓
EquipmentQuery
```

phir:

```text
EquipmentQuery.equipment_type()
```

available hai.

---

# 8. `Self` sirf return type mein nahi hota

Aksar `Self` return type mein use hota hai, lekin ye class attributes aur parameters mein bhi use ho sakta hai.

Example:

```python
from typing import Self


class Node:
    parent: Self | None
```

Yahan:

```python
parent
```

same class type ko represent karta hai.

Lekin `Self` ka sabse common aur useful use:

```python
-> Self
```

hai.

---

# 9. Classmethod ke saath `Self`

Yahan `Self` aur bhi interesting ho jata hai.

```python
from typing import Self


class Equipment:

    @classmethod
    def create(cls) -> Self:
        return cls()
```

Ab:

```python
class AHU(Equipment):
    pass
```

Aur:

```python
ahu = AHU.create()
```

Type checker samajhta hai:

```text
AHU.create()
    ↓
AHU
```

Na ke:

```text
Equipment
```

---

# 10. Iska reason kya hai?

Dekho:

```python
@classmethod
def create(cls) -> Self:
    return cls()
```

Agar:

```python
Equipment.create()
```

to:

```text
Self = Equipment
```

Agar:

```python
AHU.create()
```

to:

```text
Self = AHU
```

Yani `Self` classmethod ke context mein bhi **actual calling class** ko preserve karta hai.

---

# 11. Factory pattern mein useful

Example:

```python
from typing import Self


class Equipment:

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            data["equipment_id"]
        )
```

Subclass:

```python
class AHU(Equipment):
    pass
```

Ab:

```python
ahu = AHU.from_dict({
    "equipment_id": "AHU-001"
})
```

Type:

```text
AHU
```

Ye factory methods ke liye bohat useful hai.

---

# 12. `Self` vs `TypeVar`

Aapne pehle `TypeVar` padha hai.

Dono ko compare karna important hai.

### TypeVar

```python
T = TypeVar("T")


def identity(value: T) -> T:
    return value
```

Yahan `T` generic relationship represent karta hai.

```text
input T
   ↓
output T
```

---

### Self

```python
class Equipment:

    def reset(self) -> Self:
        return self
```

Yahan relationship specifically:

```text
current class
     ↓
same actual class
```

hai.

### Simple rule:

```text
TypeVar
→ generic type relationship

Self
→ current class/subclass relationship
```

---

# 13. `Self` vs `TypeVar` ka deeper difference

Purane style mein `Self` ke bina hum kuch aisa kar sakte thay:

```python
from typing import TypeVar

T = TypeVar("T", bound="Equipment")


class Equipment:

    def reset(self: T) -> T:
        return self
```

Ye theoretically same idea express kar sakta hai.

Lekin:

```python
Self
```

much clearer hai.

Instead of:

```python
T = TypeVar("T", bound="Equipment")

def reset(self: T) -> T:
```

likhne ke:

```python
def reset(self) -> Self:
```

likho.

---

# 14. `Self` inheritance ko automatically track karta hai

Imagine:

```python
class Equipment:
    def reset(self) -> Self:
        return self
```

Then:

```python
class HVACEquipment(Equipment):
    pass


class AHU(HVACEquipment):
    pass
```

Ab:

```python
ahu = AHU()
result = ahu.reset()
```

Type:

```text
AHU
```

`Self` ne poori inheritance chain preserve kar di:

```text
Equipment
    ↑
HVACEquipment
    ↑
AHU
    ↑
Self
```

---

# 15. Practical HVAC example

Ek builder banate hain:

```python
from typing import Self


class AHUConfig:

    def set_airflow(self, airflow: float) -> Self:
        self.airflow = airflow
        return self

    def set_temperature(self, temperature: float) -> Self:
        self.temperature = temperature
        return self

    def set_pressure(self, pressure: float) -> Self:
        self.pressure = pressure
        return self
```

Use:

```python
config = (
    AHUConfig()
    .set_airflow(2500)
    .set_temperature(22)
    .set_pressure(450)
)
```

Har method:

```text
AHUConfig
   ↓
Self
```

return karta hai.

---

# 16. Subclass add karo

```python
class AdvancedAHUConfig(AHUConfig):

    def set_filter_type(self, filter_type: str) -> Self:
        self.filter_type = filter_type
        return self
```

Ab:

```python
config = (
    AdvancedAHUConfig()
    .set_airflow(2500)
    .set_temperature(22)
    .set_pressure(450)
    .set_filter_type("HEPA")
)
```

Important point:

`set_airflow()` parent class mein defined hai.

Lekin uska return:

```python
Self
```

hai.

Therefore:

```text
AdvancedAHUConfig.set_airflow()
             ↓
AdvancedAHUConfig
             ↓
set_filter_type()
```

Ye fluent APIs ka major benefit hai.

---

# 17. `Self` runtime par kya karta hai?

Yahan important distinction hai.

```python
from typing import Self
```

`Self` primarily **typing system** ka concept hai.

Example:

```python
class Equipment:
    def reset(self) -> Self:
        return self
```

Runtime par:

```python
equipment.reset()
```

simply:

```python
self
```

return karega.

`Self` koi object create nahi karta.

Na hi:

```text
Self()
```

koi special runtime operation hai.

---

# 18. `Self` ≠ `self`

Ye dono confuse mat karna.

### `self`

Runtime object:

```python
class Equipment:

    def reset(self):
        return self
```

`self` actual object hai.

---

### `Self`

Typing concept:

```python
class Equipment:

    def reset(self) -> Self:
        return self
```

`Self` actual object nahi hai.

Ye static type system ko batata hai:

> "Return hone wala object isi actual class ka type hai."

---

# 19. `Self` ka sabse bada faida

### Faida #1 — Method chaining

```python
obj.a().b().c()
```

typing correctly preserve hoti hai.

---

### Faida #2 — Inheritance

Parent method subclass ko return kar sakta hai.

```python
class Parent:
    def method(self) -> Self:
        return self
```

Subclass mein return type automatically subclass hota hai.

---

### Faida #3 — Factory methods

```python
@classmethod
def create(cls) -> Self:
    return cls()
```

`AHU.create()` → `AHU`

---

### Faida #4 — Builder pattern

```python
builder.set_x().set_y().set_z()
```

actual builder subtype preserve hota hai.

---

### Faida #5 — Better static checking

IDE/type checker ko pata hota hai ke chain ke next step par kaunse methods available hain.

---

# 20. `Self` kab use karna chahiye?

Agar method:

```python
return self
```

karta hai aur inheritance important hai:

```python
def method(...) -> Self:
```

bohat suitable hai.

Especially:

```text
Builder
Fluent API
ORM query builder
Configuration objects
Factory methods
Inheritance-heavy models
Method chaining
```

mein.

---

# 21. Ek important warning

Har method jo `self` return karta hai usmein `Self` zaroori nahi.

Agar class inheritance concern hi nahi hai:

```python
class Counter:

    def increment(self):
        self.value += 1
        return self
```

typing ke liye `Self` useful ho sakta hai, lekin agar architecture simple hai aur subclassing nahi hai, to benefit comparatively kam hai.

`Self` ki real power **subclass-preserving typing** mein hai.

---

# 22. Complete architecture example

```python
from typing import Self


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


ahu = (
    AHU.create("AHU-001")
       .start()
       .set_airflow(2500)
       .stop()
)
```

Type flow:

```text
AHU.create()
      ↓
AHU

.start()
      ↓
AHU

.set_airflow()
      ↓
AHU

.stop()
      ↓
AHU
```

Agar `start()` aur `stop()` mein:

```python
-> Equipment
```

hota, to subclass-specific chaining lose ho sakti thi.

`Self` ne poora chain preserve kar diya.

---

# 23. Ek line mein poora concept

```python
def method(self) -> Self:
```

ka matlab hai:

> **"Ye method jis actual class/subclass ke object par call hua hai, usi type ka object return karega."**

### Mental model:

```text
self
 ↓
actual object

Self
 ↓
actual object's class/type
```

Aur sabse important:

```text
TypeVar → generic relationship
Protocol → behavior contract
TypeGuard → type narrowing
Annotated → type + metadata
overload → input/output signatures
cast → static assertion
Self → current class/subclass type
```

Ye concepts mil kar modern Python ki **type-safe architecture** ka strong foundation banate hain.
# `typing.LiteralString` — Deep Explanation

`LiteralString` ko samajhne ke liye pehle ye samjho ke **normal `str` aur `LiteralString` mein kya difference hai**.

```python
from typing import LiteralString
```

Simple definition:

> **`LiteralString` aisi string ko represent karta hai jo source code mein literal string se originate hui ho, ya doosri `LiteralString` values se bani ho.**

Iska main purpose **security-sensitive APIs**, especially **SQL queries, shell commands, format strings**, waghera mein static type checking improve karna hai.

---

## 1. Normal `str`

Normally:

```python
name: str = "Muhammad"
```

Yahan type:

```text
str
```

Hai.

Ye bhi:

```python
name = input("Name: ")
```

type:

```text
str
```

Hai.

Lekin dono strings ka **origin** different hai:

```text
"SELECT * FROM users"
        ↓
source-code literal


input()
   ↓
external/user input
```

Normal `str` typing system ke liye dono bas:

```text
str
```

hain.

---

# 2. `LiteralString` kya additional information deta hai?

Example:

```python
from typing import LiteralString

query: LiteralString = "SELECT * FROM equipment"
```

Yahan:

```text
"SELECT * FROM equipment"
```

ek **literal string** hai.

Isliye:

```text
LiteralString
```

mein assign ho sakti hai.

---

# 3. User input ka kya?

```python
user_query = input("Enter query: ")
```

`user_query` ka type:

```text
str
```

hai.

Ab:

```python
query: LiteralString = user_query
```

Type checker isko reject karega.

Kyun?

Kyunkay `user_query` source-code literal nahi hai.

Yahan security ka concept important hai:

```text
LiteralString
       ↓
trusted/static string origin

str
       ↓
could come from anywhere
```

---

# 4. Sabse important example: SQL

Maan lo hum function banate hain:

```python
from typing import LiteralString


def execute_query(query: LiteralString):
    print(query)
```

Ab:

```python
execute_query("SELECT * FROM equipment")
```

Ye acceptable hai.

Kyun?

```text
"SELECT * FROM equipment"
          ↓
literal
          ↓
LiteralString
```

---

# 5. User input pass karo

```python
user_input = input("Enter SQL: ")

execute_query(user_input)
```

Yahan static type checker warning de sakta hai.

Reason:

```text
user_input
   ↓
str
   ↓
not guaranteed LiteralString
```

Ye **bohat important security concept** hai.

---

# 6. Lekin `LiteralString` SQL injection ko khud prevent nahi karta

Ye point carefully samjho.

`LiteralString`:

```text
SQL injection protection
```

nahi hai.

Ye:

```text
static typing restriction
```

hai.

Example:

```python
def execute_query(query: LiteralString):
    ...
```

Iska purpose hai type checker ko kehna:

> "Is function ko arbitrary string mat do; mujhe statically known string chahiye."

Lekin actual database security ke liye parameterized queries use karni chahiye.

For example conceptual pattern:

```python
cursor.execute(
    "SELECT * FROM equipment WHERE equipment_id = ?",
    (equipment_id,)
)
```

Yahan user data query string ke andar directly concatenate nahi hota.

---

# 7. LiteralString aur `Literal` same nahi hain

Ye dono easily confuse hote hain.

### `Literal`

Specific value represent karta hai:

```python
from typing import Literal

status: Literal["Running", "Stopped"]
```

Matlab:

```text
sirf "Running"
ya
"Stopped"
```

allowed.

---

### `LiteralString`

String ka **origin** represent karta hai:

```python
from typing import LiteralString

query: LiteralString
```

Matlab:

```text
statically known/literal-derived string
```

So:

```text
Literal["Running"]
        ↓
specific value

LiteralString
        ↓
string ka trusted literal origin
```

---

# 8. Example comparison

### `Literal`

```python
def set_status(
    status: Literal["Running", "Stopped"]
):
    ...
```

Allowed:

```python
set_status("Running")
set_status("Stopped")
```

Not allowed:

```python
set_status("Fault")
```

---

### `LiteralString`

```python
def execute_query(
    query: LiteralString
):
    ...
```

Allowed:

```python
execute_query("SELECT * FROM equipment")
execute_query("DELETE FROM equipment")
execute_query("SELECT id FROM users")
```

Yahan exact string value restricted nahi hai.

Restriction **origin** par hai.

---

# 9. Concatenation ka kya hota hai?

Ye interesting part hai.

```python
query: LiteralString = "SELECT "
```

Aur:

```python
table: LiteralString = "equipment"
```

Phir:

```python
full_query = query + table
```

Result ko type checker `LiteralString` ke taur par preserve kar sakta hai.

Mental model:

```text
LiteralString
       +
LiteralString
       ↓
LiteralString
```

Lekin agar arbitrary `str` aa jaye:

```python
query = "SELECT * FROM " + user_input
```

to result safe `LiteralString` nahi mana jata.

Conceptually:

```text
LiteralString + str
       ↓
str
```

Kyunkay ab string mein potentially untrusted data aa gaya.

---

# 10. Function propagation

Ye aur important hai.

```python
from typing import LiteralString


def add_limit(query: LiteralString) -> LiteralString:
    return query + " LIMIT 10"
```

Ab:

```python
query = "SELECT * FROM equipment"

result = add_limit(query)
```

`result` ko literal-derived string maana ja sakta hai.

Flow:

```text
"SELECT * FROM equipment"
          ↓
LiteralString
          ↓
add_limit()
          ↓
LiteralString
```

---

# 11. Dynamic string problem

Suppose:

```python
table_name = input("Table name: ")

query = "SELECT * FROM " + table_name
```

Ab:

```text
"SELECT * FROM "
        ↓
LiteralString

table_name
        ↓
str

combine
        ↓
ordinary str
```

Isliye:

```python
execute_query(query)
```

ko `LiteralString` parameter dene par static checker complain kar sakta hai.

---

# 12. Iska security philosophy kya hai?

Socho function:

```python
def run_command(command: LiteralString):
    ...
```

Developer chahta hai:

```text
Function mein command ka structure
developer-controlled ho.
```

Na ke:

```text
command = user input
```

Example:

```python
run_command("systemctl restart hvac")
```

vs:

```python
command = input("Enter command: ")
run_command(command)
```

Second case mein user arbitrary command provide kar sakta hai.

`LiteralString` static checker ko signal deta hai ke:

> "Is API ko dynamically supplied string mat do."

---

# 13. Format strings ke saath bhi useful

Suppose:

```python
from typing import LiteralString


def safe_format(
    template: LiteralString,
    value: str
):
    return template.format(value)
```

Ab:

```python
safe_format(
    "Equipment ID: {}",
    equipment_id
)
```

Template developer-controlled hai.

Lekin:

```python
template = input("Template: ")

safe_format(template, equipment_id)
```

potentially problematic origin hai.

Yahan `LiteralString` useful signal provide karta hai.

---

# 14. `LiteralString` runtime par check karta hai?

**Nahi.**

Ye bahut important hai.

```python
from typing import LiteralString
```

`LiteralString` runtime validator nahi hai.

Ye:

```text
❌ validation
❌ conversion
❌ sanitization
❌ encryption
❌ SQL protection by itself
```

nahi karta.

Ye primarily:

```text
✅ static type checking
```

ke liye hai.

---

# 15. `cast()` ke saath danger

Aapne `cast()` padha hai.

Ye mat samajhna:

```python
from typing import cast, LiteralString

query = cast(LiteralString, user_input)
```

ab query safe ho gayi.

Nahi.

`cast()` sirf type checker ko keh raha hai:

> "Mujh par trust karo."

Runtime value wahi rahegi.

```text
user_input
    ↓
cast(LiteralString, ...)
    ↓
same runtime string
```

Agar input malicious hai, malicious hi rahega.

So:

```text
LiteralString
+
cast()
```

security validation ka replacement nahi.

---

# 16. `LiteralString` ka deeper mental model

Normal `str`:

```text
"String ki value kya hai?"
```

`LiteralString`:

```text
"String ka origin trusted literal/string composition hai?"
```

Yani typing system sirf value ko nahi dekh raha.

Wo **provenance/origin** ko bhi track karne ki koshish karta hai.

Ye advanced typing ka important concept hai.

---

# 17. `LiteralString` aur `Annotated`

Dono ko compare karo.

### `Annotated`

```python
from typing import Annotated

temperature: Annotated[float, "Celsius"]
```

Meaning:

```text
float
+
metadata
```

---

### `LiteralString`

```python
query: LiteralString
```

Meaning:

```text
string
+
literal-derived origin constraint
```

So:

```text
Annotated
→ semantic metadata

LiteralString
→ string-origin/type-safety constraint
```

---

# 18. HVAC/work-order example

Maan lo API endpoint banaya:

```python
from typing import LiteralString


def build_report_query(
    query: LiteralString
):
    print(query)
```

Developer-controlled query:

```python
build_report_query(
    "SELECT * FROM work_orders WHERE status = 'OPEN'"
)
```

Theek.

Lekin:

```python
status = input("Status: ")

query = (
    "SELECT * FROM work_orders "
    + "WHERE status = '" + status + "'"
)

build_report_query(query)
```

Yahan dynamic user input query ka part ban gaya.

`LiteralString` static analysis level par is design ko flag karne mein help kar sakta hai.

Lekin **real database code mein parameterized query** phir bhi required hai.

---

# 19. `LiteralString` kis problem ko solve karta hai?

Isko table se yaad rakho:

| Type                  | Kya represent karta hai?  |
| --------------------- | ------------------------- |
| `str`                 | koi bhi string            |
| `Literal["A"]`        | exact `"A"`               |
| `Literal["A", "B"]`   | exact allowed values      |
| `LiteralString`       | literal-derived string    |
| `Annotated[str, ...]` | string + metadata         |
| `Final[str]`          | reassignment allowed nahi |
| `Self`                | current class/subclass    |

---

# 20. `LiteralString` ka real faida

Sabse important faide:

### 1. Security-sensitive APIs

SQL, shell commands, query languages, etc. mein static checking improve hoti hai.

### 2. API design

Aap function signature mein explicitly keh sakte ho:

```python
def execute(query: LiteralString):
```

Matlab arbitrary dynamic string accept karna intended nahi.

### 3. Code review

Type signature khud developer ko warning deta hai:

```text
"This function expects a literal-derived string."
```

### 4. Static analysis

Mypy/Pyright jaise type checkers potential unsafe flows identify kar sakte hain.

### 5. Trusted vs dynamic data ka distinction

Normal:

```text
str
```

mein origin ka distinction disappear ho jata hai.

`LiteralString` us distinction ko typing level par preserve karta hai.

---

# 21. Sabse important distinction

Isko memorize karo:

```text
Literal
   ↓
"Kaunsi exact value?"

LiteralString
   ↓
"String ka origin kis type ka hai?"

Annotated
   ↓
"Type ke saath additional metadata kya hai?"

Final
   ↓
"Kya is name ko reassign kar sakte hain?"

Self
   ↓
"Current actual class ka type kya hai?"
```

### `LiteralString` ka one-line formula:

```text
LiteralString
=
string type
+
literal-derived provenance
```

Aur **ye runtime security mechanism nahi**, balki **static typing mechanism** hai.
# Lesson — `typing.TypeAlias` + `type` Statement (Python 3.12+)

Ye topic **type aliases** ke baare mein hai.

Sab se pehle basic idea:

> **Type Alias ka matlab hai kisi existing type ko ek meaningful naam dena.**

For example:

```python
EquipmentID = str
```

Ab `EquipmentID` ko hum `str` ke meaningful naam ke taur par use kar sakte hain.

---

# 1. Type Alias ki zaroorat kyun?

Maan lo HVAC project mein:

```python
def get_equipment(equipment_id: str):
    ...
```

Aur doosri jagah:

```python
def get_work_order(work_order_id: str):
    ...
```

Dono `str` hain, lekin semantically different hain:

```text
equipment_id
     ↓
AHU-001

work_order_id
     ↓
WO-2026-001
```

Python type checker dono ko simply:

```text
str
```

samajhta hai.

Hum readability improve karne ke liye aliases bana sakte hain:

```python
EquipmentID = str
WorkOrderID = str
```

Ab:

```python
def get_equipment(equipment_id: EquipmentID):
    ...

def get_work_order(work_order_id: WorkOrderID):
    ...
```

Code ka meaning much clearer ho gaya.

---

# 2. Simple Type Alias

Old/common style:

```python
EquipmentID = str
```

Phir:

```python
def find_equipment(
    equipment_id: EquipmentID
):
    ...
```

Ye conceptually:

```text
EquipmentID
     ↓
    str
```

hai.

Important:

> Alias koi naya runtime type nahi banata.

`EquipmentID` aur `str` essentially same type ko refer karte hain.

---

# 3. Problem: Python ko kaise pata chale ke ye alias hai?

Ye line:

```python
EquipmentID = str
```

Python ke liye normal assignment bhi ho sakti hai.

Example:

```python
EquipmentID = str
```

ya:

```python
EquipmentID = 100
```

Dono syntactically assignment hain.

Static type checkers ko ambiguity ho sakti hai.

Isi problem ke liye `TypeAlias` introduce hua.

---

# 4. `typing.TypeAlias`

```python
from typing import TypeAlias

EquipmentID: TypeAlias = str
```

Ab explicitly kaha:

> `EquipmentID` ek type alias hai.

Phir:

```python
def get_equipment(
    equipment_id: EquipmentID
):
    ...
```

---

# 5. `TypeAlias` ka mental model

```python
EquipmentID: TypeAlias = str
```

ko aise read karo:

```text
EquipmentID
      ↓
"Ye ek type ka alternative naam hai"
      ↓
str
```

`TypeAlias` khud type nahi hai jisko runtime object banana ho.

Ye **type checker ko declaration deta hai**.

---

# 6. Generic Type Alias

Yahan `TypeAlias` aur interesting ho jata hai.

```python
from typing import TypeAlias

EquipmentList: TypeAlias = list[str]
```

Ab:

```python
equipment_ids: EquipmentList
```

equivalent hai:

```python
equipment_ids: list[str]
```

---

# 7. Generic aliases

Maan lo:

```python
from typing import TypeVar, TypeAlias

T = TypeVar("T")

RepositoryData: TypeAlias = list[T]
```

Conceptually:

```text
RepositoryData[int]
RepositoryData[str]
RepositoryData[AHU]
```

use kiya ja sakta hai, depending on type-checker/context.

Example:

```python
numbers: RepositoryData[int]
names: RepositoryData[str]
```

---

# 8. Lekin Python 3.12 mein better syntax aa gaya

Python 3.12 ne **`type` statement** introduce kiya.

Instead of:

```python
from typing import TypeAlias

EquipmentID: TypeAlias = str
```

likh sakte ho:

```python
type EquipmentID = str
```

Ye modern Python syntax hai.

---

# 9. `type` statement ka basic syntax

```python
type AliasName = ExistingType
```

Example:

```python
type EquipmentID = str
type WorkOrderID = str
type Temperature = float
type EquipmentList = list[str]
```

Ab:

```python
def get_equipment(
    equipment_id: EquipmentID
):
    ...
```

---

# 10. Old vs New

### Old

```python
from typing import TypeAlias

EquipmentID: TypeAlias = str
```

### Python 3.12+

```python
type EquipmentID = str
```

Modern code mein generally `type` statement cleaner hai.

---

# 11. `type` statement ka sabse bada benefit

`type` statement clearly communicate karta hai:

```python
type EquipmentID = str
```

> "Ye normal variable assignment nahi hai. Ye type alias declaration hai."

Yani syntax level par hi distinction clear ho jati hai.

---

# 12. Complex type ko readable banana

Maan lo:

```python
equipment_data: dict[str, list[dict[str, str | float | None]]]
```

Ye difficult read hota hai.

Alias:

```python
type EquipmentData = dict[
    str,
    list[dict[str, str | float | None]]
]
```

Ab:

```python
def load_equipment() -> EquipmentData:
    ...
```

Much cleaner.

---

# 13. HVAC example

Maan lo equipment record:

```python
type EquipmentRecord = dict[str, str | float | None]
```

Ab:

```python
def get_equipment() -> EquipmentRecord:
    return {
        "equipment_id": "AHU-001",
        "floor": "34",
        "temperature": 22.5,
        "status": "Running"
    }
```

Function signature dekhte hi samajh aa raha hai:

```text
EquipmentRecord
```

---

# 14. Type alias vs NewType

Ye **bohat important distinction** hai.

Aapne `EquipmentID = str` dekha.

Lekin:

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
```

ye different hai.

### Type Alias

```python
type EquipmentID = str
```

Matlab:

```text
EquipmentID
    =
str
```

Same underlying type identity.

---

### NewType

```python
EquipmentID = NewType(
    "EquipmentID",
    str
)
```

Matlab static type system mein:

```text
EquipmentID
    ↓
distinct type
    ↓
based on str
```

Yani `NewType` **semantic distinction** create karta hai.

---

# 15. Example

Type Alias:

```python
type EquipmentID = str
type WorkOrderID = str
```

Type checker ke perspective se dono ultimately `str` hain.

So:

```python
equipment_id: EquipmentID
work_order_id: WorkOrderID

work_order_id = equipment_id
```

generally type-compatible ho sakta hai.

---

### `NewType`

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
WorkOrderID = NewType("WorkOrderID", str)
```

Ab:

```python
equipment_id: EquipmentID
work_order_id: WorkOrderID
```

different static types hain.

Ye accidental mixing prevent karne mein useful hai.

---

# 16. Type Alias vs `Annotated`

Ye bhi confuse hota hai.

```python
type Temperature = float
```

sirf alias hai:

```text
Temperature → float
```

Lekin:

```python
from typing import Annotated

Temperature = Annotated[
    float,
    "Celsius"
]
```

mein metadata bhi attached hai.

So:

```text
TypeAlias
→ naam deta hai

Annotated
→ metadata deta hai
```

Dono combine bhi ho sakte hain.

---

# 17. Python 3.12 `type` statement + `Annotated`

Example:

```python
from typing import Annotated

type Temperature = Annotated[
    float,
    "Celsius"
]
```

Ab:

```python
def set_temperature(
    temperature: Temperature
):
    ...
```

Conceptually:

```text
Temperature
   ↓
Annotated[float, "Celsius"]
   ↓
float + metadata
```

---

# 18. Generic type aliases — Python 3.12 style

Python 3.12 ka ek powerful feature hai:

```python
type Result[T] = list[T]
```

Yahan `T` alias ke andar directly define ho raha hai.

Example:

```python
type EquipmentList[T] = list[T]
```

Ab:

```python
ahu_list: EquipmentList[AHU]
```

Aur:

```python
temperature_values: EquipmentList[float]
```

Conceptually:

```text
EquipmentList[AHU]
       ↓
list[AHU]

EquipmentList[float]
       ↓
list[float]
```

Ye modern generic alias syntax hai.

---

# 19. Python 3.12 se pehle generic alias

Purane style mein:

```python
from typing import TypeVar, TypeAlias

T = TypeVar("T")

EquipmentList: TypeAlias = list[T]
```

Python 3.12+:

```python
type EquipmentList[T] = list[T]
```

Naya syntax kaafi clean hai.

---

# 20. Generic alias practical example

Suppose repository response:

```python
type APIResponse[T] = dict[str, T]
```

Ab:

```python
ahu_response: APIResponse[AHU]
```

conceptually:

```python
dict[str, AHU]
```

Aur:

```python
status_response: APIResponse[str]
```

becomes:

```python
dict[str, str]
```

---

# 21. Nested generic aliases

Aur deeper example:

```python
type APIResponse[T] = dict[
    str,
    list[T]
]
```

Ab:

```python
result: APIResponse[AHU]
```

means approximately:

```python
dict[str, list[AHU]]
```

Yani aliases complex type structures ko readable bana dete hain.

---

# 22. Recursive type aliases

`type` statement ka ek powerful use recursive types bhi hain.

Example JSON-like data:

```python
type JSONValue = (
    str
    | int
    | float
    | bool
    | None
    | list["JSONValue"]
    | dict[str, "JSONValue"]
)
```

Ye represent karta hai:

```text
JSONValue
 ├── str
 ├── int
 ├── float
 ├── bool
 ├── None
 ├── list[JSONValue]
 └── dict[str, JSONValue]
```

Yani JSON ke andar:

```text
dictionary
   ↓
list
   ↓
dictionary
   ↓
list
```

jitni nesting ho, alias recursively represent kar sakta hai.

---

# 23. `type` statement runtime par kya banata hai?

Ye important hai.

```python
type EquipmentID = str
```

sirf text substitution nahi hai.

Python 3.12+ mein `type` statement ek **type alias object** create karta hai, specifically `typing.TypeAliasType`.

Conceptually:

```text
type EquipmentID = str
        ↓
TypeAliasType
        ↓
underlying type = str
```

Isliye modern `type` statement old assignment se semantically stronger hai.

---

# 24. `__value__`

Modern type alias object ka underlying value inspect kiya ja sakta hai.

Conceptually:

```python
type EquipmentID = str
```

Aur:

```python
EquipmentID.__value__
```

underlying aliased type ko represent karta hai:

```text
str
```

Ye mostly advanced introspection/tooling ke use cases mein useful hai.

Normal application code mein iski zaroorat rarely hoti hai.

---

# 25. `__type_params__`

Generic aliases ke case mein type parameters bhi associated hote hain.

Example:

```python
type Result[T] = list[T]
```

Yahan alias ke paas `T` type parameter hai.

Ye information typing/introspection systems ke liye relevant hoti hai.

---

# 26. Scope ka important concept

Type aliases module level par commonly define kiye jate hain:

```python
type EquipmentID = str
type Temperature = float
```

Phir poore module/package mein reuse:

```python
def read_temperature() -> Temperature:
    ...
```

Ye architecture ko consistent banata hai.

---

# 27. Type aliases architecture mein kyun useful hain?

Suppose project mein 100 jagah:

```python
dict[str, list[dict[str, str | float | None]]]
```

likha hua hai.

Problem:

* readability poor
* maintenance difficult
* type structure repeat
* change karna mushkil

Alias:

```python
type EquipmentData = dict[
    str,
    list[dict[str, str | float | None]]
]
```

Ab:

```python
def load() -> EquipmentData:
    ...

def save(data: EquipmentData):
    ...

def validate(data: EquipmentData):
    ...
```

Agar underlying structure change ho:

```python
type EquipmentData = ...
```

ek central place change karna easier hai.

---

# 28. Type Alias ≠ Runtime validation

Ye bhi yaad rakho.

```python
type Temperature = float
```

Iska matlab ye **nahi**:

```text
Temperature automatically validates float
```

Agar:

```python
temperature = "hot"
```

runtime par Python automatically TypeAlias ke basis par reject nahi karega.

Typing mostly static analysis ke liye hai.

---

# 29. Type Alias ≠ New class

```python
type EquipmentID = str
```

se new class nahi banti.

Aap ye nahi keh rahe:

```text
class EquipmentID(str):
    ...
```

Alias sirf existing type ko meaningful type name deta hai.

Agar genuinely new static identity chahiye:

```python
NewType
```

consider karo.

Agar runtime behavior chahiye:

```python
class
```

use karo.

---

# 30. Teen concepts ek saath

Isko strongly memorize karo:

```python
type EquipmentID = str
```

### Type Alias

```text
meaningful name
       ↓
existing type
```

---

```python
from typing import NewType

EquipmentID = NewType("EquipmentID", str)
```

### NewType

```text
distinct static type
       ↓
based on str
```

---

```python
class EquipmentID(str):
    ...
```

### Class

```text
actual runtime class
       ↓
can have methods/behavior
```

---

# 31. `TypeAlias` kab use karein?

Agar Python version older hai ya explicit old-style declaration chahiye:

```python
from typing import TypeAlias

type_name: TypeAlias = ...
```

Example:

```python
EquipmentID: TypeAlias = str
```

Lekin Python **3.12+** mein generally:

```python
type EquipmentID = str
```

preferable modern syntax hai.

---

# 32. Practical HVAC architecture

Ek clean type system imagine karo:

```python
from typing import Annotated

type EquipmentID = str
type WorkOrderID = str

type Temperature = Annotated[
    float,
    "Celsius"
]

type Airflow = Annotated[
    float,
    "CFM"
]

type EquipmentList[T] = list[T]
```

Ab:

```python
class AHU:
    def __init__(
        self,
        equipment_id: EquipmentID,
        temperature: Temperature,
        airflow: Airflow
    ):
        self.equipment_id = equipment_id
        self.temperature = temperature
        self.airflow = airflow
```

Aur:

```python
def load_ahus() -> EquipmentList[AHU]:
    ...
```

Yahan different typing concepts combine ho rahe hain:

```text
EquipmentID
     ↓
type alias

Temperature
     ↓
type alias + Annotated metadata

Airflow
     ↓
type alias + Annotated metadata

EquipmentList[T]
     ↓
generic type alias
```

Ye large projects mein type signatures ko kaafi readable bana sakta hai.

---

# 33. `TypeAlias` vs `type` statement — final comparison

| Feature                    | `TypeAlias`                     | `type` statement          |
| -------------------------- | ------------------------------- | ------------------------- |
| Python version             | Older Python versions           | Python 3.12+              |
| Syntax                     | `X: TypeAlias = Y`              | `type X = Y`              |
| Explicit alias declaration | Yes                             | Yes                       |
| Generic aliases            | Older `TypeVar` style           | Cleaner `type X[T] = ...` |
| Recursive aliases          | Possible                        | Cleaner modern syntax     |
| Dedicated alias object     | No same modern syntax semantics | `TypeAliasType`           |
| Recommended for 3.12+      | Legacy/compatibility            | **Yes**                   |

---

# 34. Sab se important mental model

Aapke previous lessons ko connect karo:

```text
TypeVar
   ↓
unknown/generic type relationship

Generic
   ↓
class/type ko parameterized banana

Protocol
   ↓
behavior contract

Self
   ↓
current class/subclass type

Annotated
   ↓
type + metadata

LiteralString
   ↓
literal-derived string constraint

TypeAlias
   ↓
existing type ko meaningful naam

type statement
   ↓
modern Python 3.12+ type-alias declaration
```

### One-line formula:

```text
type EquipmentID = str
```

ka matlab:

> **"Python type system mein `str` ko `EquipmentID` naam se refer karne ke liye ek explicit type alias define karo."**

Aur:

```python
type EquipmentList[T] = list[T]
```

ka matlab:

> **"Ek generic type alias banao jo `EquipmentList[T]` ko `list[T]` ke naam se represent kare."**

**Sabse important distinction:** `type` statement se **new runtime class nahi banti**; ye **type alias** banata hai. Agar aapko `EquipmentID` ko `str` se genuinely alag static type banana hai, to `NewType` relevant concept hai.
# Lesson — `NamedTuple` vs `dataclass` vs `TypedDict`

Ye teenon Python mein **structured data ko type-safe way mein represent** karne ke liye use hote hain, lekin inka purpose bilkul same nahi hai.

Sabse pehle ek simple mental model:

```text
NamedTuple
    ↓
fixed fields + tuple behavior

dataclass
    ↓
actual Python object + fields + methods

TypedDict
    ↓
dictionary ka expected structure
```

---

# 1. Ek hi data ko teen ways mein dekho

Maan lo hamare paas AHU hai:

```text
equipment_id = "AHU-001"
floor        = "34"
airflow      = 2500
```

### `NamedTuple`

```python
from typing import NamedTuple


class AHU(NamedTuple):
    equipment_id: str
    floor: str
    airflow: float
```

Use:

```python
ahu = AHU("AHU-001", "34", 2500)
```

---

### `dataclass`

```python
from dataclasses import dataclass


@dataclass
class AHU:
    equipment_id: str
    floor: str
    airflow: float
```

Use:

```python
ahu = AHU("AHU-001", "34", 2500)
```

---

### `TypedDict`

```python
from typing import TypedDict


class AHU(TypedDict):
    equipment_id: str
    floor: str
    airflow: float
```

Use:

```python
ahu = {
    "equipment_id": "AHU-001",
    "floor": "34",
    "airflow": 2500
}
```

Dekho:

```text
NamedTuple → AHU(...)
dataclass  → AHU(...)
TypedDict  → {...}
```

Yahi sabse basic difference hai.

---

# 2. `NamedTuple` kya hai?

`NamedTuple` basically **tuple + named fields + type hints** hai.

```python
from typing import NamedTuple


class Equipment(NamedTuple):
    equipment_id: str
    floor: str
    status: str
```

Create:

```python
equipment = Equipment(
    "AHU-001",
    "34",
    "Running"
)
```

Access:

```python
equipment.equipment_id
```

Aur tuple ki tarah:

```python
equipment[0]
```

bhi kar sakte ho.

---

# 3. `NamedTuple` ka important feature: immutable

```python
equipment = Equipment(
    "AHU-001",
    "34",
    "Running"
)
```

Ab:

```python
equipment.status = "Stopped"
```

allowed nahi hai.

Kyun?

Kyunkay `NamedTuple` tuple ki tarah **immutable** hota hai.

Mental model:

```text
NamedTuple
   ↓
tuple
   ↓
immutable
```

---

# 4. `dataclass` mutable hota hai

```python
from dataclasses import dataclass


@dataclass
class Equipment:
    equipment_id: str
    floor: str
    status: str
```

Ab:

```python
equipment = Equipment(
    "AHU-001",
    "34",
    "Running"
)
```

Status change:

```python
equipment.status = "Stopped"
```

Allowed hai.

Mental model:

```text
dataclass
   ↓
normal Python object
   ↓
normally mutable
```

---

# 5. `TypedDict` kya hai?

`TypedDict` **dictionary ke expected keys aur value types** define karta hai.

```python
from typing import TypedDict


class EquipmentData(TypedDict):
    equipment_id: str
    floor: str
    status: str
```

Actual object:

```python
equipment = {
    "equipment_id": "AHU-001",
    "floor": "34",
    "status": "Running"
}
```

Ye **dict hi hai**.

Important:

> `TypedDict` runtime par koi special dictionary class nahi banata.

Ye mainly **static type checker ko dictionary ka expected structure batata hai**.

---

# 6. Sabse important difference

Teenon ka underlying concept:

```text
NamedTuple
    → tuple


dataclass
    → class/object


TypedDict
    → dict
```

Isko memorize kar lo.

---

# 7. Access ka difference

### NamedTuple

```python
ahu.equipment_id
```

ya:

```python
ahu[0]
```

---

### dataclass

```python
ahu.equipment_id
```

Normally:

```python
ahu[0]
```

nahi.

---

### TypedDict

```python
ahu["equipment_id"]
```

Normally:

```python
ahu.equipment_id
```

nahi.

---

# 8. Comparison table

| Feature           | `NamedTuple`      | `dataclass`    | `TypedDict`           |
| ----------------- | ----------------- | -------------- | --------------------- |
| Underlying object | `tuple`           | class instance | `dict`                |
| Named fields      | Yes               | Yes            | Yes                   |
| Type hints        | Yes               | Yes            | Yes                   |
| Mutable           | ❌ No              | ✅ Normally     | ✅ Yes                 |
| Attribute access  | ✅                 | ✅              | ❌                     |
| Dictionary access | ❌                 | ❌              | ✅                     |
| Index access      | ✅                 | ❌              | ❌                     |
| Methods           | Limited/possible  | ✅ Excellent    | ❌ Not the purpose     |
| Inheritance       | Limited           | ✅ Strong       | Type-level structure  |
| `__init__`        | Generated         | Generated      | No normal constructor |
| `__repr__`        | Yes               | Yes            | Normal dict repr      |
| Best for          | Immutable records | Domain objects | Dict/API data         |

---

# 9. `dataclass` kab use karna chahiye?

Agar object ke andar **behavior** bhi hai, `dataclass` usually best choice hai.

Example:

```python
from dataclasses import dataclass


@dataclass
class AHU:
    equipment_id: str
    airflow: float
    temperature: float

    def is_overheated(self) -> bool:
        return self.temperature > 30

    def set_airflow(self, airflow: float):
        self.airflow = airflow
```

Ab:

```python
ahu = AHU(
    "AHU-001",
    2500,
    32
)
```

Aur:

```python
ahu.is_overheated()
```

ya:

```python
ahu.set_airflow(3000)
```

Ye **domain object** ban gaya.

---

# 10. `NamedTuple` kab?

Jab data:

* small ho
* fixed ho
* immutable ho
* record ki tarah behave kare
* tuple compatibility chahiye

Example:

```python
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float
```

Use:

```python
point = Point(10, 20)
```

Ye perfect hai.

---

# 11. `TypedDict` kab?

Jab data naturally dictionary/API/JSON format mein aa raha ho.

Example API response:

```python
from typing import TypedDict


class EquipmentResponse(TypedDict):
    equipment_id: str
    status: str
    temperature: float
```

API se:

```python
response = {
    "equipment_id": "AHU-001",
    "status": "Running",
    "temperature": 22.5
}
```

Ab:

```python
def process_equipment(
    data: EquipmentResponse
):
    print(data["equipment_id"])
```

Ye `TypedDict` ka natural use case hai.

---

# 12. API/JSON mein `TypedDict` powerful hai

Suppose API response:

```json
{
    "equipment_id": "AHU-001",
    "floor": "34",
    "temperature": 22.5,
    "status": "Running"
}
```

Python mein naturally:

```python
data = response.json()
```

result:

```text
dict
```

hai.

Isko model karne ke liye:

```python
class EquipmentResponse(TypedDict):
    equipment_id: str
    floor: str
    temperature: float
    status: str
```

useful hai.

Yahan `dataclass` banana unnecessarily object-oriented ho sakta hai agar aapko sirf JSON structure represent karna hai.

---

# 13. `TypedDict` runtime validation nahi karta

Ye bohat important hai.

```python
class EquipmentData(TypedDict):
    equipment_id: str
    temperature: float
```

Ye **automatically validate nahi karega**:

```python
data = {
    "equipment_id": 123,
    "temperature": "hot"
}
```

Python runtime par dictionary bana dega.

`TypedDict` ka purpose:

```text
static typing
```

hai.

Agar external API data ko genuinely validate karna hai, to runtime validation library/schema system alag concern hai.

---

# 14. `NamedTuple` bhi runtime type safety nahi deta

Example:

```python
class Equipment(NamedTuple):
    equipment_id: str
    temperature: float
```

Static checker expected types dekhega.

Lekin Python ki type annotations generally runtime validation enforce nahi kartin.

---

# 15. `dataclass` bhi automatic type validation nahi karta

```python
@dataclass
class Equipment:
    temperature: float
```

Aap technically:

```python
equipment = Equipment("hot")
```

likh sakte ho.

Python automatically:

```text
❌ TypeError because float expected
```

zaroori nahi dega.

Type checker warning de sakta hai, lekin runtime validation separate concept hai.

---

# 16. `dataclass` ka biggest advantage: behavior

Ye dekho:

```python
@dataclass
class VAV:
    equipment_id: str
    temperature: float
    setpoint: float

    def temperature_error(self) -> float:
        return self.temperature - self.setpoint

    def needs_cooling(self) -> bool:
        return self.temperature > self.setpoint
```

Ab object sirf data nahi hai.

Object:

```text
data
+
behavior
```

represent kar raha hai.

Isliye domain models mein `dataclass` bohat useful hai.

---

# 17. `NamedTuple` mein methods possible hain

Ye kehna technically wrong hoga ke NamedTuple mein methods bilkul nahi ho sakte.

Example:

```python
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

Use:

```python
point = Point(3, 4)

print(point.distance_from_origin())
```

Possible hai.

Lekin `NamedTuple` ka primary purpose **immutable tuple-like record** hai.

Complex domain behavior ke liye `dataclass` generally better fit hai.

---

# 18. `dataclass(frozen=True)` se comparison interesting ho jata hai

Agar aapko dataclass ka object chahiye lekin immutable:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Equipment:
    equipment_id: str
    floor: str
```

Ab:

```python
equipment.floor = "35"
```

allowed nahi.

To:

```text
NamedTuple
    → immutable record

dataclass(frozen=True)
    → immutable object
```

Dono immutable hain, lekin design philosophy different hai.

---

# 19. `NamedTuple` vs `dataclass(frozen=True)`

### NamedTuple

Tuple behavior:

```python
ahu[0]
```

available.

Unpacking:

```python
equipment_id, floor = ahu
```

natural.

---

### Frozen dataclass

Object semantics:

```python
ahu.equipment_id
```

No tuple indexing by default.

Isliye agar tuple compatibility important hai:

```text
NamedTuple
```

better.

Agar object/domain semantics important hain:

```text
frozen dataclass
```

better.

---

# 20. Inheritance mein `dataclass` powerful hai

Aapne previous lesson mein dekha tha:

```python
@dataclass
class Equipment:
    equipment_id: str
    floor: str
```

Then:

```python
@dataclass
class AHU(Equipment):
    airflow: float
```

Ab:

```python
ahu = AHU(
    "AHU-001",
    "34",
    2500
)
```

Child automatically parent fields inherit karta hai.

Ye complex domain model ke liye powerful hai.

---

# 21. `TypedDict` mein required/optional keys

`TypedDict` ka ek important feature hai.

```python
from typing import TypedDict


class EquipmentData(TypedDict):
    equipment_id: str
    status: str
    comment: str
```

Normally keys required hain.

Lekin:

```python
from typing import NotRequired


class EquipmentData(TypedDict):
    equipment_id: str
    status: str
    comment: NotRequired[str]
```

Ab:

```python
{
    "equipment_id": "AHU-001",
    "status": "Running"
}
```

valid structure ho sakti hai.

---

# 22. `Required` bhi hai

Aap totality control bhi kar sakte ho:

```python
from typing import TypedDict, NotRequired, Required


class EquipmentData(TypedDict, total=False):
    equipment_id: Required[str]
    status: Required[str]
    comment: str
```

Yahan:

```text
equipment_id → required
status       → required
comment      → optional
```

Ye API payloads ke liye kaafi useful hai.

---

# 23. API request example

Suppose work-order API:

```python
from typing import TypedDict, NotRequired


class WorkOrderPayload(TypedDict):
    work_order_number: str
    equipment_id: str
    description: str
    priority: str
    comment: NotRequired[str]
```

Valid:

```python
payload = {
    "work_order_number": "WO-1001",
    "equipment_id": "AHU-001",
    "description": "AHU inspection",
    "priority": "High"
}
```

`comment` optional hai.

Ye `TypedDict` ka strong practical use case hai.

---

# 24. `NamedTuple` API ke liye kyun less natural?

API JSON:

```json
{
    "equipment_id": "AHU-001",
    "status": "Running"
}
```

Python mein natural representation:

```python
dict
```

Hai.

Agar `NamedTuple` use karo:

```python
Equipment(
    "AHU-001",
    "Running"
)
```

to JSON/dict conversion aur serialization layer mein additional handling aa sakti hai.

Isliye:

```text
JSON/API payload
      ↓
TypedDict
```

usually natural choice hai.

---

# 25. Database row ke liye `NamedTuple`

Agar database query ka result fixed immutable row hai:

```python
class EquipmentRow(NamedTuple):
    equipment_id: str
    floor: str
    temperature: float
```

Database row ko:

```python
row = EquipmentRow(
    "AHU-001",
    "34",
    22.5
)
```

represent karna useful ho sakta hai.

Especially agar tuple-like behavior chahiye.

---

# 26. Business/domain model ke liye `dataclass`

```python
@dataclass
class AHU:
    equipment_id: str
    airflow: float
    temperature: float

    def increase_airflow(self, amount: float):
        self.airflow += amount
```

Ye clearly domain object hai.

```text
AHU
 ├── data
 ├── state
 └── behavior
```

`dataclass` yahan strong choice hai.

---

# 27. JSON/API shape ke liye `TypedDict`

```python
class AHUResponse(TypedDict):
    equipment_id: str
    airflow: float
    temperature: float
```

Ye basically keh raha hai:

```text
"Dictionary ke andar ye keys honi chahiye
aur unki values ye types honi chahiye."
```

Object behavior ki zaroorat nahi.

---

# 28. Fixed lightweight immutable record ke liye `NamedTuple`

```python
class SensorReading(NamedTuple):
    timestamp: str
    temperature: float
    humidity: float
```

Use:

```python
reading = SensorReading(
    "2026-10-04 19:00",
    22.5,
    45.0
)
```

Agar reading immutable snapshot hai, `NamedTuple` natural fit hai.

---

# 29. Ek real architecture

Aap facility/HVAC project mein teenon ko ek saath use kar sakte ho.

### API layer

```python
class EquipmentResponse(TypedDict):
    equipment_id: str
    airflow: float
    temperature: float
```

### Internal domain model

```python
@dataclass
class AHU:
    equipment_id: str
    airflow: float
    temperature: float

    def needs_cooling(self) -> bool:
        return self.temperature > 24
```

### Immutable sensor reading

```python
class SensorReading(NamedTuple):
    timestamp: str
    temperature: float
```

Flow:

```text
External API
     ↓
TypedDict
     ↓
convert/validate
     ↓
dataclass domain object
     ↓
business logic
     ↓
NamedTuple immutable snapshot
```

Ye architecture mein bohat sensible separation ho sakti hai.

---

# 30. Performance ke baare mein

Sirf ye assume mat karo:

```text
NamedTuple = always faster
dataclass = slow
TypedDict = fastest
```

Aisi simplistic ranking useful nahi hai.

Teenon ka purpose different hai.

Generally:

```text
NamedTuple
→ compact tuple semantics

dataclass
→ normal object semantics

TypedDict
→ normal dict semantics
```

Actual performance ko workload ke context mein benchmark karna chahiye.

---

# 31. `NamedTuple` vs `dataclass` — simple decision

Khud se ye question karo:

### "Mujhe tuple behavior chahiye?"

Yes:

```text
NamedTuple
```

### "Mujhe object + methods + inheritance + mutable state chahiye?"

Yes:

```text
dataclass
```

### "Mujhe dictionary/JSON ka structure type karna hai?"

Yes:

```text
TypedDict
```

---

# 32. `TypedDict` vs `dataclass` — sabse important difference

Ye yaad rakho:

```text
TypedDict
     ↓
data ka SHAPE

dataclass
     ↓
data ka OBJECT
```

Example:

```python
class EquipmentData(TypedDict):
    id: str
    temperature: float
```

Meaning:

> Dictionary mein `id` aur `temperature` honge.

Whereas:

```python
@dataclass
class Equipment:
    id: str
    temperature: float
```

Meaning:

> `Equipment` naam ka actual Python object hai.

---

# 33. `NamedTuple` vs `dataclass` — sabse important difference

```text
NamedTuple
     ↓
"immutable tuple-like record"

dataclass
     ↓
"object-oriented data model"
```

Example:

```python
point = Point(10, 20)

x = point[0]
```

NamedTuple ke liye natural.

Dataclass:

```python
point.x
```

natural.

---

# 34. Decision tree

```text
                    Structured data?
                           |
             +-------------+-------------+
             |             |             |
           dict           object        tuple
             |             |             |
        TypedDict       dataclass    NamedTuple
             |             |             |
        API/JSON       behavior       immutable
        payload        methods        record
        response       inheritance    indexing
```

Isko practical shortcut samjho.

---

# 35. Final master comparison

| Requirement                  | Best choice              |
| ---------------------------- | ------------------------ |
| API JSON response            | `TypedDict`              |
| API request payload          | `TypedDict`              |
| Dictionary structure         | `TypedDict`              |
| Business/domain object       | `dataclass`              |
| Methods + state              | `dataclass`              |
| Inheritance-heavy model      | `dataclass`              |
| Mutable object               | `dataclass`              |
| Immutable object             | `dataclass(frozen=True)` |
| Tuple behavior               | `NamedTuple`             |
| Index access                 | `NamedTuple`             |
| Immutable lightweight record | `NamedTuple`             |
| Fixed sensor snapshot        | `NamedTuple`             |
| Static dict shape only       | `TypedDict`              |

---

## 36. Sab concepts ko ek line mein yaad karo

```text
NamedTuple
    = Tuple + names + types + immutable

dataclass
    = Class/Object + fields + generated methods

TypedDict
    = Dict + expected keys + expected value types
```

Aur sabse important:

> **`NamedTuple` tab jab data ko immutable tuple-like record banana ho.**

> **`dataclass` tab jab data ko actual domain object banana ho jisme state, methods, inheritance ya behavior ho.**

> **`TypedDict` tab jab aapke paas dictionary/JSON/API data ho aur aap sirf uska expected structure type-check karna chahte ho.**
Bilkul. Ab **Lesson 69 — `typing.TYPE_CHECKING` — Circular Import Avoid** start karte hain.

# Lesson 69: `typing.TYPE_CHECKING` — Circular Import Avoid

Sab se pehle ek important baat:

> `TYPE_CHECKING` ka main purpose **type hints ke liye imports ko runtime par execute hone se rokna** hai.

Iska sab se common use **circular imports** avoid karna hai.

---

## 1. Circular Import kya hota hai?

Maan lo hamare paas 2 files hain:

```text
equipment.py
ahu.py
```

`equipment.py` mein:

```python
from ahu import AHU

class Equipment:
    def get_ahu(self) -> AHU:
        ...
```

Aur `ahu.py` mein:

```python
from equipment import Equipment

class AHU(Equipment):
    ...
```

Ab dependency dekho:

```text
equipment.py
     ↓
   ahu.py
     ↓
equipment.py
```

Yani:

```text
Equipment → AHU → Equipment
```

Isko **circular import** kehte hain.

---

# 2. Problem kyun hoti hai?

Python jab:

```python
import equipment
```

karta hai, to `equipment.py` execute hoti hai.

Wahan:

```python
from ahu import AHU
```

milta hai.

Python `ahu.py` open karta hai.

Wahan:

```python
from equipment import Equipment
```

milta hai.

Lekin `equipment.py` abhi complete execute nahi hui.

Is wajah se Python ko incomplete module mil sakta hai.

Example error:

```text
ImportError: cannot import name 'Equipment'
```

---

# 3. Lekin kabhi import sirf type hint ke liye hota hai

Yahan important point hai.

Suppose:

```python
equipment.py
```

mein:

```python
from ahu import AHU

class Equipment:
    def get_ahu(self) -> AHU:
        ...
```

Humein `AHU` ki zarurat **runtime logic** mein nahi hai.

Humein sirf type checker ko batana hai:

```text
get_ahu() AHU return karega
```

To phir runtime par:

```python
from ahu import AHU
```

karne ki zarurat nahi.

Yahan `TYPE_CHECKING` useful hota hai.

---

# 4. `TYPE_CHECKING` kya hai?

Python mein:

```python
from typing import TYPE_CHECKING
```

phir:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

Complete example:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU


class Equipment:
    def get_ahu(self) -> "AHU":
        ...
```

Ab kya hua?

Type checker ko:

```python
AHU
```

ka import nazar aa raha hai.

Lekin normal Python runtime mein:

```python
TYPE_CHECKING
```

ki value:

```python
False
```

hoti hai.

Isliye:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

runtime par execute nahi hota.

---

# 5. Sab se important concept

Isko yaad rakho:

```text
TYPE_CHECKING
      ↓
False at runtime
      ↓
import execute nahi hota
      ↓
circular dependency avoid ho sakti hai
```

Lekin static type checker ke liye:

```text
TYPE_CHECKING
      ↓
True maana jata hai
      ↓
type checker import ko analyze karta hai
```

Yani ek hi code ke do perspectives hain:

```text
Runtime Python
       ↓
TYPE_CHECKING = False


Static Type Checker
       ↓
TYPE_CHECKING = True
```

---

# 6. `TYPE_CHECKING` practically kaise use hota hai?

Example:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU


class Equipment:

    def get_ahu(self) -> "AHU":
        return self.ahu
```

Yahan `"AHU"` string mein hai.

Isko **forward reference** kehte hain.

Python runtime ko immediately `AHU` class resolve karne ki zarurat nahi padti.

---

# 7. Python 3.11 aur earlier style

Common style:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU


class Equipment:
    def get_ahu(self) -> "AHU":
        ...
```

Quotes important hain:

```python
"AHU"
```

instead of:

```python
AHU
```

---

# 8. `from __future__ import annotations`

Modern Python mein ek aur option hai:

```python
from __future__ import annotations
```

Example:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU


class Equipment:
    def get_ahu(self) -> AHU:
        ...
```

Ab quotes ki zarurat nahi:

```python
-> AHU
```

Python annotations ko immediately evaluate nahi karta.

Isliye modern code mein yeh pattern common hai:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU
```

---

# 9. HVAC example

Suppose architecture:

```text
equipment.py
ahu.py
vav.py
```

`equipment.py`:

```python
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
```

Aur:

```python
ahu.py
```

```python
from equipment import Equipment


class AHU(Equipment):

    def start(self):
        print("AHU started")
```

Ab `equipment.py` ko runtime par `AHU` import karne ki zarurat nahi.

Lekin type checker samajhta hai:

```python
connected_ahu() -> AHU
```

---

# 10. Important: `TYPE_CHECKING` koi magic circular-import solution nahi

Ye bahut important hai.

Agar aapko runtime mein actual class ki zarurat hai:

```python
if isinstance(obj, AHU):
    ...
```

to sirf:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

kaafi nahi hoga.

Kyun?

Runtime par:

```python
AHU
```

exist hi nahi karega.

Example:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU


def check(obj):
    if isinstance(obj, AHU):
        return True
```

Runtime:

```text
NameError: name 'AHU' is not defined
```

Kyunke `AHU` import hi nahi hua.

---

# 11. `TYPE_CHECKING` kab use karein?

Jab import **sirf type hints** ke liye required ho:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

Good.

Example:

```python
def get_ahu() -> AHU:
    ...
```

---

# 12. Kab use nahi karein?

Agar runtime code ko class/function actually chahiye:

```python
from ahu import AHU
```

to normal import hi karein.

Example:

```python
ahu = AHU()
```

Yahan runtime par `AHU` required hai.

`TYPE_CHECKING` use karoge to:

```python
AHU()
```

fail ho sakta hai.

---

# 13. Ek aur common example: Models

Suppose:

```text
models/
    equipment.py
    location.py
```

`equipment.py`:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from location import Location


class Equipment:

    location: Location

    def __init__(self, location: Location):
        self.location = location
```

Yahan `Location` sirf annotation mein use ho raha hai.

Isliye:

```python
if TYPE_CHECKING:
    from location import Location
```

use kar sakte hain.

---

# 14. TYPE_CHECKING ka real architectural benefit

Large projects mein classes ek doosre ko reference karti hain.

Example:

```text
API
 ↓
Service
 ↓
Repository
 ↓
Model
```

Aur kabhi models ek doosre ko reference karte hain:

```text
Equipment ↔ Location
Equipment ↔ WorkOrder
WorkOrder ↔ Technician
```

Agar har file runtime imports kare:

```python
from equipment import Equipment
from work_order import WorkOrder
from technician import Technician
from location import Location
```

to dependency graph complicated ho sakta hai.

`TYPE_CHECKING` se **type-only dependencies** runtime dependency graph se hata sakte ho.

---

# 15. Runtime dependency vs type dependency

Ye distinction bohot important hai.

### Runtime dependency

Code ko actual object/class chahiye:

```python
from ahu import AHU

ahu = AHU()
```

Dependency:

```text
equipment.py
      ↓
    ahu.py
```

### Type dependency

Sirf type annotation ke liye:

```python
if TYPE_CHECKING:
    from ahu import AHU

def get_ahu() -> AHU:
    ...
```

Runtime dependency:

```text
equipment.py
      X
    ahu.py
```

Type-checking dependency:

```text
equipment.py
      ↓
    ahu.py
```

Sirf static analysis ke waqt.

---

# 16. `TYPE_CHECKING` ka mental model

Isko yaad rakho:

```text
Normal import
    ↓
Runtime + Type Checker


TYPE_CHECKING import
    ↓
Type Checker only
```

Yani:

```python
from ahu import AHU
```

means:

> Mujhe AHU runtime mein bhi chahiye.

Aur:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

means:

> Mujhe AHU sirf type checking ke liye chahiye.

---

# 17. `TYPE_CHECKING` + Generic

Advanced example:

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

Agar kisi specific module mein:

```python
Repository[Equipment]
```

use ho raha hai, type checker relationship samajh sakta hai without necessarily creating runtime import cycles.

---

# 18. `TYPE_CHECKING` + Protocol

Architecture mein yeh aur powerful ho jata hai.

```python
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from equipment import Equipment


class EquipmentRepository(Protocol):

    def get(self, equipment_id: str) -> Equipment:
        ...
```

Yahan `Equipment` runtime par required nahi.

Sirf type contract define karne ke liye chahiye.

---

# 19. Sabse important difference

### `TYPE_CHECKING`

```python
if TYPE_CHECKING:
    from ahu import AHU
```

**Import ko runtime se hide karta hai.**

### `cast()`

```python
cast(AHU, obj)
```

**Existing object ko static type batata hai.**

### `TypeGuard`

```python
def is_ahu(obj: object) -> TypeGuard[AHU]:
    ...
```

**Runtime check ke basis par type narrow karta hai.**

### `Protocol`

```python
class AHUProtocol(Protocol):
    ...
```

**Behavior-based interface define karta hai.**

Ye chaar concepts alag purposes ke hain.

---

# 20. Production rule

Agar aapke code mein circular import aa raha hai, pehla sawal yeh hona chahiye:

> **Kya mujhe yeh import runtime mein actually chahiye, ya sirf type hint ke liye?**

Agar sirf type hint ke liye:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from other_module import SomeClass
```

Aur modern Python mein preferably:

```python
from __future__ import annotations
```

ke saath.

Agar runtime mein bhi required hai, to `TYPE_CHECKING` se problem ko hide mat karo. Architecture/dependency ko properly refactor karo.

---

## Short summary

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ahu import AHU
```

ka matlab:

> **AHU ko static type checker ke liye import karo, lekin normal Python runtime mein import mat karo.**

Iska major use:

```text
TYPE_CHECKING
      ↓
type-only imports
      ↓
circular imports reduce
      ↓
cleaner module dependencies
```

**Lesson 69 ka core concept:**
`TYPE_CHECKING` runtime behavior ko change karne ke liye nahi, **type-checking dependencies ko runtime imports se separate karne ke liye** hai.
Bilkul. Ab next topic:

# Lesson 70 — `typing.reveal_type()` — Debugging Types

`reveal_type()` ka purpose **Python program ko debug karna nahi**, balki **static type checker ko debug karna** hai.

Yani jab aapko doubt ho:

> "Type checker is variable ko kis type ka samajh raha hai?"

to `reveal_type()` use karte hain.

---

## 1. Basic concept

```python
from typing import reveal_type

x = 100

reveal_type(x)
```

Type checker generally batayega:

```text
Revealed type is "int"
```

Yahan `x` runtime par:

```python
100
```

hi hai.

`reveal_type()` ka main kaam hai **type checker se poochna**:

```text
"Is waqt tum x ko kis type ka samajh rahe ho?"
```

---

# 2. Ye `print()` jaisa nahi hai

Important difference:

```python
print(x)
```

runtime value dekhta hai:

```text
100
```

Lekin:

```python
reveal_type(x)
```

static type dekhta hai:

```text
int
```

Mental model:

```text
print()
   ↓
Runtime value

reveal_type()
   ↓
Static type
```

---

# 3. Simple example

```python
from typing import reveal_type

name = "Muhammad"

reveal_type(name)
```

Type checker:

```text
Revealed type is "str"
```

Aur:

```python
temperature = 22.5

reveal_type(temperature)
```

Result:

```text
Revealed type is "float"
```

---

# 4. Type inference samajhne ke liye

Python mein hum har jagah type explicitly nahi likhte.

```python
equipment_id = "AHU-001"
```

Type checker automatically infer kar leta hai:

```text
equipment_id → str
```

Agar doubt ho:

```python
reveal_type(equipment_id)
```

Type checker confirm karega:

```text
str
```

---

# 5. Union ke saath

Ab interesting example:

```python
from typing import reveal_type

value: int | str

reveal_type(value)
```

Type checker:

```text
int | str
```

Kyun?

Kyunkay `value` dono mein se koi bhi ho sakta hai.

---

# 6. Type narrowing ke saath

Yahan `reveal_type()` bohot useful hai.

```python
from typing import reveal_type

value: int | str

if isinstance(value, str):
    reveal_type(value)
else:
    reveal_type(value)
```

Type checker logically dekhta hai:

```text
if branch
    ↓
str

else branch
    ↓
int
```

Yani:

```text
if isinstance(value, str):
    value → str

else:
    value → int
```

Ye exactly **type narrowing** hai.

---

# 7. `TypeGuard` ke saath

Humne previous lessons mein `TypeGuard` padha tha.

Example:

```python
from typing import TypeGuard, reveal_type


def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

Ab:

```python
value: object

if is_string(value):
    reveal_type(value)
```

Type checker:

```text
str
```

Yani `reveal_type()` se hum verify kar sakte hain ke hamara custom type guard actually expected narrowing kar raha hai ya nahi.

---

# 8. `TypeIs` ke saath

```python
from typing import TypeIs, reveal_type


def is_string(value: int | str) -> TypeIs[str]:
    return isinstance(value, str)
```

Phir:

```python
value: int | str

if is_string(value):
    reveal_type(value)
else:
    reveal_type(value)
```

Expected:

```text
True branch  → str
False branch → int
```

Is tarah `reveal_type()` type narrowing ko inspect karne ka excellent tool hai.

---

# 9. Generic ke saath

Ye aur important hai.

```python
from typing import TypeVar, reveal_type

T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]
```

Ab:

```python
number = first([10, 20, 30])

reveal_type(number)
```

Type checker:

```text
int
```

Aur:

```python
name = first(["Ali", "Ahmed"])

reveal_type(name)
```

Type:

```text
str
```

Yahan `reveal_type()` verify kar raha hai ke **Generic inference correctly kaam kar rahi hai**.

---

# 10. Generic architecture mein iska faida

Maan lo:

```python
T = TypeVar("T")


class Repository(Generic[T]):

    def get(self) -> T:
        ...
```

Ab:

```python
ahu_repo: Repository[AHU]
```

Agar:

```python
ahu = ahu_repo.get()

reveal_type(ahu)
```

Type checker:

```text
AHU
```

Agar kahin unexpectedly:

```text
Equipment
```

ya:

```text
object
```

aa raha ho, to `reveal_type()` se immediately pata chal sakta hai.

---

# 11. `Self` ke saath

Previous lesson mein humne `Self` padha tha.

```python
from typing import Self, reveal_type


class Equipment:

    def reset(self) -> Self:
        return self


class AHU(Equipment):

    def start(self) -> Self:
        return self
```

Ab:

```python
ahu = AHU()

result = ahu.reset()

reveal_type(result)
```

Type checker ideally:

```text
AHU
```

Na ke:

```text
Equipment
```

Ye `Self` ka benefit verify karne ka achha example hai.

---

# 12. `Literal` ke saath

Suppose:

```python
from typing import Literal, reveal_type

status: Literal["ON", "OFF"]
```

Agar:

```python
status = "ON"

reveal_type(status)
```

Type checker context ke mutabiq literal ya `str` infer kar sakta hai.

Yahan `reveal_type()` useful hai jab aapko samajhna ho:

> "Kya checker exact literal value track kar raha hai ya sirf `str`?"

---

# 13. `overload` ke saath

Ye `reveal_type()` ka **bohot practical use** hai.

Previous lesson mein:

```python
from typing import overload, Literal


@overload
def get_data(detailed: Literal[True]) -> dict:
    ...


@overload
def get_data(detailed: Literal[False]) -> str:
    ...


def get_data(detailed: bool) -> dict | str:
    if detailed:
        return {"status": "OK"}

    return "OK"
```

Ab:

```python
data = get_data(True)

reveal_type(data)
```

Type checker:

```text
dict
```

Aur:

```python
data = get_data(False)

reveal_type(data)
```

Type:

```text
str
```

Ye prove karta hai ke overload signatures correctly input/output relationship de rahe hain.

---

# 14. `TypedDict` ke saath

Suppose:

```python
from typing import TypedDict, reveal_type


class EquipmentData(TypedDict):
    equipment_id: str
    floor: str
    airflow: float
```

Then:

```python
equipment: EquipmentData = {
    "equipment_id": "AHU-001",
    "floor": "34",
    "airflow": 2500.0,
}
```

Agar:

```python
reveal_type(equipment)
```

Type checker:

```text
EquipmentData
```

Aur:

```python
reveal_type(equipment["airflow"])
```

Type:

```text
float
```

---

# 15. `Annotated` ke saath

Humne `Annotated` bhi padha tha.

```python
from typing import Annotated, reveal_type

Temperature = Annotated[float, "Celsius"]

temperature: Temperature = 22.5

reveal_type(temperature)
```

Type checker generally underlying type ko:

```text
float
```

samjhega.

Important:

> `Annotated` ka metadata normal type identity nahi banata.

---

# 16. `cast()` ke saath

Previous lesson:

```python
from typing import cast, reveal_type

value = cast(str, some_value)

reveal_type(value)
```

Type checker:

```text
str
```

Lekin yaad rakho:

```python
cast(str, value)
```

runtime par value ko convert nahi karta.

`reveal_type()` sirf static checker ka view confirm karta hai.

---

# 17. `TYPE_CHECKING` se difference

Abhi jo Lesson 69 padha:

```python
if TYPE_CHECKING:
    from ahu import AHU
```

Aur Lesson 70:

```python
reveal_type(ahu)
```

Dono ka purpose different hai.

### `TYPE_CHECKING`

Type-only imports:

```text
runtime import dependency ko control karo
```

### `reveal_type`

Type inference inspect karo:

```text
type checker variable ko kis type ka samajh raha hai?
```

Mental model:

```text
TYPE_CHECKING
     ↓
"Ye import kab chahiye?"

reveal_type()
     ↓
"Ye variable kis type ka hai?"
```

---

# 18. Real debugging example

Suppose aapka code:

```python
def get_equipment():
    return {
        "id": "AHU-001",
        "airflow": 2500
    }
```

Aap assume kar rahe ho:

```python
equipment: dict[str, str]
```

Lekin actually:

```python
airflow = 2500
```

integer hai.

Aap:

```python
equipment = get_equipment()

reveal_type(equipment)
```

kar sakte ho.

Type checker jo infer karta hai, woh saamne aa jayega.

Phir:

```python
reveal_type(equipment["id"])
reveal_type(equipment["airflow"])
```

se individual values ka type bhi check kar sakte ho.

---

# 19. Large code mein iska asli faida

Suppose function kaafi complex hai:

```python
def process_equipment(data):
    if isinstance(data, dict):
        ...
    elif isinstance(data, list):
        ...
```

Aapko pata nahi:

```python
data
```

kis branch mein checker ke nazdeek kis type ka hai.

Temporary debugging:

```python
reveal_type(data)
```

ya:

```python
if isinstance(data, dict):
    reveal_type(data)
```

Isse aap type checker's reasoning dekh sakte ho.

---

# 20. `reveal_type()` actual runtime mein kya karta hai?

Yahan ek subtle point hai.

Modern Python mein:

```python
from typing import reveal_type
```

ke saath `reveal_type()` runtime par bhi available hai.

Example:

```python
from typing import reveal_type

x = 100

result = reveal_type(x)

print(result)
```

Runtime par `reveal_type()` value ko return kar sakta hai, aur implementation diagnostic message bhi emit kar sakti hai.

Lekin **iska primary purpose static type checking hai**.

Isliye:

```python
reveal_type(x)
```

ko normal application logging ka replacement mat samjho.

Runtime value dekhni ho:

```python
print(x)
```

Static type dekhna ho:

```python
reveal_type(x)
```

---

# 21. Type checker difference

Ek important practical point:

`reveal_type()` ka exact diagnostic output type checker par depend karta hai.

For example different tools:

```text
mypy
pyright
basedpyright
```

apna diagnostic format use kar sakte hain.

Isliye:

```text
Revealed type is ...
```

ko Python ka normal `print()` output mat samjho.

Ye **type checker diagnostic** hai.

---

# 22. `reveal_type()` vs `type()`

Ye confusion bohot common hai.

### `type()`

```python
x = 100

print(type(x))
```

Runtime:

```text
<class 'int'>
```

Python actual object ko inspect karta hai.

### `reveal_type()`

```python
reveal_type(x)
```

Static type checker:

```text
int
```

Difference:

```text
type()
   ↓
actual runtime object

reveal_type()
   ↓
static type checker ka understanding
```

---

# 23. Sabse powerful use: "Checker mujhe kya samajh raha hai?"

Ye iska best mental model hai:

```python
reveal_type(variable)
```

ko mentally read karo:

> **"Type checker, mujhe batao tum is variable ko kis type ka samajh rahe ho."**

Example:

```python
value: int | str

if isinstance(value, str):
    reveal_type(value)
```

Answer:

```text
str
```

Yani narrowing successful.

---

# 24. Practical HVAC example

```python
from typing import reveal_type


def get_airflow(value: int | float) -> int | float:
    return value
```

Ab:

```python
airflow = get_airflow(2500)

reveal_type(airflow)
```

Type:

```text
int
```

Agar:

```python
airflow = get_airflow(2500.5)

reveal_type(airflow)
```

Type:

```text
float
```

Agar function ka return annotation sirf:

```python
def get_airflow(value: int | float) -> int | float:
```

ho aur inference lose ho jaye, `reveal_type()` aapko bata dega ke caller side par exact type preserve ho rahi hai ya nahi.

---

# 25. Generic HVAC repository example

```python
from typing import Generic, TypeVar, reveal_type

T = TypeVar("T")


class Repository(Generic[T]):

    def __init__(self, item: T):
        self.item = item

    def get(self) -> T:
        return self.item
```

AHU:

```python
class AHU:
    pass
```

Use:

```python
repo = Repository(AHU())

ahu = repo.get()

reveal_type(ahu)
```

Type checker infer karega:

```text
AHU
```

Yani Generic type inference correctly preserve ho rahi hai.

---

# 26. Agar unexpected type aaye?

Suppose expected:

```text
AHU
```

lekin:

```python
reveal_type(ahu)
```

shows:

```text
Equipment
```

ya:

```text
object
```

To ye signal hai ke kahin type information lose ho rahi hai.

Possible reasons:

```text
1. Wrong annotation
2. Generic parameter missing
3. Union too broad
4. Function return type too broad
5. Overload missing
6. TypeGuard narrowing missing
7. cast required ho sakta hai
8. Library typing incomplete
```

Yani `reveal_type()` **type-debugging microscope** ki tarah kaam karta hai.

---

# 27. Ek complete debugging flow

Maan lo:

```python
value: int | str | None
```

Aur code:

```python
if value is not None:

    reveal_type(value)

    if isinstance(value, str):
        reveal_type(value)
```

Type narrowing:

```text
Start:
int | str | None

is not None:
int | str

isinstance(..., str):
str
```

Aap har stage par `reveal_type()` laga kar checker ki reasoning observe kar sakte ho.

---

# 28. Golden rule

`reveal_type()` ko production logic ka part mat samjho.

Iska main use:

```text
Development
     ↓
Static typing debugging
     ↓
Type inference inspect
     ↓
Narrowing verify
     ↓
Generic/overload behavior verify
```

---

## Short summary

| Tool             | Purpose                              |
| ---------------- | ------------------------------------ |
| `type(x)`        | Runtime actual type                  |
| `print(x)`       | Runtime value                        |
| `reveal_type(x)` | Static type checker ka inferred type |
| `cast(T, x)`     | Checker ko type assertion            |
| `TypeGuard`      | Custom narrowing                     |
| `TypeIs`         | True + false branch narrowing        |
| `TYPE_CHECKING`  | Type-only imports                    |

### Sab se important line:

```python
reveal_type(x)
```

ka matlab samjho:

> **"Type checker, tumhare according `x` kis type ka hai?"**

Aur `reveal_type()` especially **Generics, TypeGuard/TypeIs, overloads, `Self`, unions aur complex type inference** debug karne mein bohot powerful hai.
