# Python OOP — Lessons 31-40 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 31: `global` aur `nonlocal` Deeply

## 1. Normal Assignment → Local

```python
x = 10

def test():
    x = 20
    print(x)

test()
print(x)
```

**Output:**
```
20
10
```

**Explanation:**
- `x = 10` → global variable
- `x = 20` → function ke andar **naya local** variable
- `print(x)` (andar) → local `20`
- `print(x)` (bahar) → global `10`

## 2. `global` — Global Modify

```python
x = 10

def test():
    global x
    x = 20

test()
print(x)
```

**Output:**
```
20
```

**Explanation:**
- `global x` → Python ko bataya: "`x` global hai, local mat banao"
- `x = 20` → global `x` update
- `print(x)` → `20`

## 3. `nonlocal` — Enclosing Modify

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

**Output:**
```
20
```

**Explanation:**
- `x = 10` → `outer()` ka local
- `nonlocal x` → `inner()` ko bataya: "`x` enclosing function ka hai"
- `x = 20` → `outer()` ka `x` update
- `print(x)` → `20`

## 4. `global` vs `nonlocal`

```python
x = "GLOBAL"

def outer():
    x = "OUTER"

    def inner():
        nonlocal x
        x = "CHANGED"

    inner()
    print(x)

outer()
print(x)
```

**Output:**
```
CHANGED
GLOBAL
```

**Explanation:**
- `nonlocal x` → `outer()` ka `x` change
- Global `x` unchanged

## 5. `nonlocal` Nearest Enclosing

```python
def outer():
    x = "outer"

    def middle():
        x = "middle"

        def inner():
            nonlocal x
            x = "changed"

        inner()
        print(x)

    middle()
    print(x)

outer()
```

**Output:**
```
changed
outer
```

**Explanation:**
- `inner()` ka `nonlocal x` → nearest enclosing `x` (middle ka) change
- `outer()` ka `x` unchanged

## 6. `nonlocal` Bina Enclosing Variable

```python
def outer():
    def inner():
        nonlocal x
        x = 10

    inner()
```

**Error:**
```
SyntaxError: no binding for nonlocal 'x' found
```

**Explanation:**
- `x` kahin enclosing function mein exist nahi karta
- `nonlocal` fail

## 7. Mutable Object — No `nonlocal` Needed

```python
def outer():
    data = []

    def inner():
        data.append(10)

    inner()
    print(data)

outer()
```

**Output:**
```
[10]
```

**Explanation:**
- `data.append(10)` → mutation (existing object change)
- `nonlocal` ki zaroorat nahi

## 8. Mutation vs Rebinding

```python
# Mutation — no nonlocal
data.append(10)

# Rebinding — nonlocal needed
nonlocal data
data = [10]
```

**Explanation:**
- Mutation → same object change
- Rebinding → variable ko naye object se bind

## 9. Closure + `nonlocal`

```python
def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

c = counter()
print(c())   # 1
print(c())   # 2
print(c())   # 3
```

**Explanation:**
- `count = 0` → enclosing variable
- `nonlocal count` → modify
- `count` → calls ke darmiyan preserve

## 10. Closure vs Class

```python
# Closure
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

# Class
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
        return self.count
```

**Explanation:**
- Class → state = `self.count`
- Closure → state = enclosing variable

## 11. Decorator mein `nonlocal`

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

**Explanation:**
- `count = 0` → enclosing
- `nonlocal count` → modify
- Calls ke darmiyan preserve

## 12. LEGB + Modification

```
Local      → normal assignment
Enclosing  → nonlocal
Global     → global
```

## 13. Interview Example 1

```python
x = 10

def outer():
    x = 20
    def inner():
        print(x)
    inner()

outer()
```

**Output:**
```
20
```

**Explanation:**
- `inner()` → Local nahi → Enclosing `x = 20`

## 14. Interview Example 2

```python
x = 10

def outer():
    x = 20
    def inner():
        global x
        x = 30
    inner()
    print(x)

outer()
print(x)
```

**Output:**
```
20
30
```

**Explanation:**
- `global x` → global `x` target
- `outer()` ka `x` unchanged → `20`
- Global `x` → `30`

## 15. Final Mental Model

```
x = value    → Local
global x     → Global
nonlocal x   → Nearest enclosing
```

---

# Lesson 32: Namespace aur `__dict__`

## 1. Namespace Kya Hai?

```python
name = "Ali"
age = 25
```

**Explanation:**
- Python conceptually mapping rakhta hai:

```
name → "Ali"
age  → 25
```

- Namespace = names → objects

## 2. Global Namespace

```python
name = "Ali"
age = 25
print(globals())
```

**Output (conceptually):**
```
{'name': 'Ali', 'age': 25, ...}
```

**Explanation:**
- `globals()` → module ka global namespace dictionary
- `globals()["name"]` → `"Ali"`

## 3. `locals()`

```python
def test():
    name = "Ali"
    age = 25
    print(locals())

test()
```

**Output:**
```
{'name': 'Ali', 'age': 25}
```

**Explanation:**
- `locals()` → current local namespace

## 4. `globals()` vs `locals()`

```python
name = "Global"

def test():
    name = "Local"
    print("locals:", locals())
    print("globals:", globals()["name"])

test()
```

**Output:**
```
locals: {'name': 'Local'}
globals: Global
```

**Explanation:**
- Dono mein `name` hai, lekin different namespaces

## 5. Class ka `__dict__`

```python
class Employee:
    company = "ABC"

print(Employee.__dict__)
```

**Output (conceptually):**
```
{'company': 'ABC', ...}
```

**Explanation:**
- `__dict__` → class namespace

## 6. Object ka `__dict__`

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp = Employee("Ali", 5000)
print(emp.__dict__)
```

**Output:**
```
{'name': 'Ali', 'salary': 5000}
```

**Explanation:**
- `self.name = "Ali"` → object namespace mein store
- `emp.__dict__` → instance attributes

## 7. `__dict__` Dictionary Ki Tarah

```python
print(emp.name)              # Ali
print(emp.__dict__["name"])  # Ali
```

**Explanation:**
- Dono same value
- `emp.__dict__` → instance namespace

## 8. `__dict__` Modify

```python
emp.__dict__["salary"] = 7000
print(emp.salary)   # 7000
```

**Explanation:**
- Namespace mein direct value change
- `emp.salary` → `7000`

## 9. Naya Attribute Manually

```python
emp.__dict__["department"] = "HVAC"
print(emp.department)   # HVAC
```

**Explanation:**
- Namespace mein entry add
- Attribute accessible

## 10. `vars()`

```python
class Employee:
    def __init__(self, name):
        self.name = name

emp = Employee("Ali")
print(vars(emp))
```

**Output:**
```
{'name': 'Ali'}
```

**Explanation:**
- `vars(emp)` ≈ `emp.__dict__`

## 11. `vars()` aur `__dict__`

```
vars(emp)
    ↓
emp.__dict__
    ↓
instance namespace
```

## 12. Class ka `__dict__` (Methods)

```python
class Equipment:
    category = "HVAC"

    def start(self):
        print("Starting")

print(Equipment.__dict__)
```

**Output (conceptually):**
```
{'category': 'HVAC', 'start': <function ...>, ...}
```

**Explanation:**
- Class namespace mein methods bhi store

## 13. Instance vs Class Namespace

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

emp = Employee("Ali")
```

**Explanation:**
- `Employee.__dict__` → `company`, `__init__`, etc.
- `emp.__dict__` → `name`

## 14. Attribute Lookup

```
emp.name
   ↓
data descriptor?
   ↓
emp.__dict__
   ↓
class / MRO
```

**Explanation:**
- `emp.__dict__["name"]` → instance value

## 15. Class Variable Example

```python
class Employee:
    company = "ABC"

emp = Employee()
print(emp.__dict__)   # {}
print(emp.company)    # ABC
```

**Explanation:**
- `company` instance namespace mein nahi
- Python class mein search karta hai

## 16. Instance Variable Add

```python
emp.company = "XYZ"
print(emp.__dict__)   # {'company': 'XYZ'}
```

**Explanation:**
- Instance ka apna `company` ban gaya
- `Employee.company` → `ABC`
- `emp.company` → `XYZ`

## 17. Scope vs Namespace

```
Scope     → Name kahan accessible?
Namespace → Name → object mapping kahan?
```

## 18. Closure mein Namespace

```python
def outer():
    x = 10

    def inner():
        return x

    return inner

f = outer()
print(f.__code__.co_freevars)   # ('x',)
print(f.__closure__)             # (<cell ...>,)
```

**Explanation:**
- `co_freevars` → free variable names
- `__closure__` → captured value

## 19. `globals()` Practical

```python
x = 100
print(globals()["x"])   # 100

globals()["y"] = 200
print(y)                # 200
```

**Explanation:**
- Global namespace access/modify

## 20. `locals()` Practical

```python
def calculate(a, b):
    total = a + b
    result = total * 2
    print(locals())

calculate(10, 20)
```

**Output:**
```
{'a': 10, 'b': 20, 'total': 30, 'result': 60}
```

**Explanation:**
- Debugging ke liye useful

## 21. `dir()` vs `__dict__`

```python
print(dir(emp))      # Zyada names (inherited bhi)
print(emp.__dict__)  # Directly stored attributes
```

## 22. HVAC Example

```python
class AHU:
    system_type = "HVAC"

    def __init__(self, equipment_id, temperature):
        self.equipment_id = equipment_id
        self.temperature = temperature

ahu = AHU("AHU-01", 22)
print(ahu.__dict__)
```

**Output:**
```
{'equipment_id': 'AHU-01', 'temperature': 22}
```

**Explanation:**
- Instance namespace → `equipment_id`, `temperature`

## 23. Complete Connection

```
Scope → Name kahan search?
LEGB  → L → E → G → B
Namespace → Name → Object mapping
globals() → Global namespace
locals()  → Current local namespace
__dict__  → Object/Class namespace
```

---

# Lesson 33: `__slots__`

## 1. Normal Class

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp = Employee("Ali", 5000)
print(emp.__dict__)
```

**Output:**
```
{'name': 'Ali', 'salary': 5000}
```

**Explanation:**
- Object ke paas `__dict__` hai

## 2. `__slots__`

```python
class Employee:
    __slots__ = ("name", "salary")

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp = Employee("Ali", 5000)
print(emp.__dict__)
```

**Output:**
```
AttributeError
```

**Explanation:**
- `__slots__` → normal `__dict__` nahi
- Allowed attributes: `name`, `salary`

## 3. Extra Attribute Add

```python
class Employee:
    __slots__ = ("name",)

    def __init__(self):
        self.name = "Ali"

emp = Employee()
emp.department = "HVAC"
```

**Error:**
```
AttributeError
```

**Explanation:**
- `department` slots mein nahi
- Extra attributes allowed nahi

## 4. Benefit

```
10 objects → chhota difference
100,000 objects → memory overhead important
```

**Explanation:**
- `__slots__` → per-instance memory reduce

## 5. Normal vs Slots

**Normal:**
```
Object → __dict__ → equipment_id, temperature
```

**Slots:**
```
Object → fixed slots → equipment_id, temperature
```

## 6. `__slots__` Private Nahi

```python
class Employee:
    __slots__ = ("salary",)

emp = Employee()
emp.salary = 5000    # OK
print(emp.salary)    # 5000
```

**Explanation:**
- `__slots__` → private nahi
- Purpose: allowed attributes, memory

## 7. `__slots__` Security Nahi

```
__slots__ → security boundary nahi
Encapsulation → separate concept
```

## 8. `__slots__` + Inheritance

```python
class Employee:
    __slots__ = ("name",)

class Manager(Employee):
    __slots__ = ("department",)
```

**Explanation:**
- `Manager` ke paas `name` + `department` dono

## 9. Child mein `__slots__` Na Ho

```python
class Employee:
    __slots__ = ("name",)

class Manager(Employee):
    pass
```

**Explanation:**
- `Manager` instances ko normal `__dict__` mil sakta hai
- Consistent slots ke liye child mein bhi define karo

## 10. Empty `__slots__`

```python
class Base:
    __slots__ = ()

obj = Base()
obj.x = 10   # Error
```

**Explanation:**
- Koi additional slot nahi
- Extra attributes allowed nahi

## 11. `__slots__` + `__dict__`

```python
class Employee:
    __slots__ = ("name", "salary", "__dict__")

emp = Employee()
emp.name = "Ali"
emp.department = "HVAC"   # OK
```

**Explanation:**
- `__dict__` explicitly add
- Dynamic attributes possible
- Lekin memory benefit reduce

## 12. `__weakref__`

```python
class Employee:
    __slots__ = ("name", "__weakref__")
```

**Explanation:**
- Weak references support
- Advanced topic

## 13. HVAC Example

```python
class Sensor:
    __slots__ = ("point_id", "temperature")

    def __init__(self, point_id, temperature):
        self.point_id = point_id
        self.temperature = temperature
```

**Explanation:**
- 100,000 sensors → memory overhead reduce

## 14. `__slots__` + `@property`

```python
class Temperature:
    __slots__ = ("_value",)

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < -273.15:
            raise ValueError("Invalid temperature")
        self._value = value
```

**Explanation:**
- `__slots__` → storage control
- `@property` → access/validation control

## 15. `__slots__` + Descriptor

```
__slots__
    ↓
slot descriptors
    ↓
attribute access/storage
```

## 16. `__dict__` vs `__slots__`

| Feature | Normal | `__slots__` |
|---------|--------|-------------|
| Instance `__dict__` | Yes | No |
| Arbitrary attributes | Yes | No |
| Memory | Higher | Lower |
| Fixed layout | No | Yes |

## 17. Faster Nahi Automatically

```
__slots__ → primarily memory optimization
```

## 18. Mental Model

**Normal:**
```
emp → __dict__ → name, salary
```

**Slots:**
```
emp → name slot, salary slot
```

## 19. Scope → Namespace → `__dict__` → `__slots__`

```
Scope → accessible?
LEGB → search order
Namespace → name → object
__dict__ → dynamic namespace
__slots__ → fixed storage
```

---

# Lesson 34: MRO + `super()` Deeply

## 1. MRO

```python
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    pass

dog = Dog()
dog.speak()
```

**Output:**
```
Animal
```

**Explanation:**
- MRO: `Dog → Animal → object`
- `Dog` mein nahi mila → `Animal` mein mila

## 2. MRO Dekho

```python
print(Dog.mro())
```

**Output:**
```
[<class 'Dog'>, <class 'Animal'>, <class 'object'>]
```

## 3. `object`

```python
class Animal:
    pass
```

**Conceptually:**
```python
class Animal(object):
    pass
```

**Explanation:**
- Python 3 mein sab classes `object` se derive

## 4. Method Overriding + MRO

```python
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    def speak(self):
        print("Dog")

dog = Dog()
dog.speak()
```

**Output:**
```
Dog
```

**Explanation:**
- MRO: `Dog → Animal → object`
- `Dog.speak()` mil gaya → stop

## 5. `super()`

```python
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    def speak(self):
        print("Dog")
        super().speak()

dog = Dog()
dog.speak()
```

**Output:**
```
Dog
Animal
```

**Explanation:**
- `super().speak()` → MRO mein next `speak()`

## 6. `super()` = Parent Nahi

```
super() → MRO mein current class ke baad next implementation
```

## 7. Simple Inheritance

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()
```

**MRO:**
```
B → A → object
```

**Explanation:**
- `super()` from B → A

## 8. `super()` + `__init__`

```python
class Employee:
    def __init__(self, name):
        self.name = name

class Manager(Employee):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department

manager = Manager("Ali", "HVAC")
print(manager.name)        # Ali
print(manager.department)  # HVAC
```

**Flow:**
```
Manager.__init__()
    ↓
super().__init__()
    ↓
Employee.__init__()
    ↓
self.name = "Ali"
    ↓
self.department = "HVAC"
```

## 9. `super()` ka Fayda

- Parent initialization reuse
- Code duplication avoid
- Future changes automatically

## 10. Multiple Inheritance

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()

class C(A):
    def show(self):
        print("C")
        super().show()

class D(B, C):
    def show(self):
        print("D")
        super().show()

d = D()
d.show()
```

**Output:**
```
D
B
C
A
```

**Explanation:**
- MRO: `D → B → C → A → object`
- `super()` chain follow

## 11. `D` ka MRO

```python
print(D.mro())
```

**Output:**
```
[D, B, C, A, object]
```

## 12. Diamond Inheritance

```
       A
      / \
     B   C
      \ /
       D
```

**MRO:**
```
D → B → C → A → object
```

## 13. MRO Manually

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
```

**MRO:**
```
D → B → C → A → object
```

## 14. `super()` Multiple Inheritance

```python
class B(A):
    def show(self):
        print("B")
        super().show()
```

**Explanation:**
- `super()` B se direct A par jump nahi karta
- MRO-relative next → `C`

## 15. Key Line

```
super() → MRO mein current class ke baad next
```

## 16. `super()` Object

```python
s = super()
```

**Explanation:**
- Super object MRO-based lookup

## 17. `super()` with Arguments

```python
super(CurrentClass, self)
```

**Modern:**
```python
super()
```

## 18. `super()` Attributes

```python
class A:
    value = 10

class B(A):
    value = 20

    def show(self):
        print(super().value)   # 10
```

## 19. HVAC Example

```python
class Equipment:
    def start(self):
        print("Equipment starting")

class AHU(Equipment):
    def start(self):
        super().start()
        print("AHU fan starting")

ahu = AHU()
ahu.start()
```

**Output:**
```
Equipment starting
AHU fan starting
```

## 20. Multiple HVAC

```python
class Equipment:
    def start(self):
        print("Equipment")

class Fan(Equipment):
    def start(self):
        super().start()
        print("Fan")

class AHU(Fan):
    def start(self):
        super().start()
        print("AHU")

AHU().start()
```

**Output:**
```
Equipment
Fan
AHU
```

## 21. Cooperative Inheritance

```python
super().method()  # Best practice
```

**Explanation:**
- MRO chain follow

## 22. `super()` vs Direct

```python
Employee.__init__(self, name)  # Specific
super().__init__(name)         # MRO follow
```

## 23. Final Architecture

```
Inheritance → MRO → super()
```

## 24. Golden Rules

```
1. MRO = Method Resolution Order
2. Class.mro() → exact order
3. super() → MRO next
4. Multiple inheritance → super() important
5. Cooperative inheritance → super() chain
```

---

# Lesson 35: MRO aur C3 Linearization

## 1. Simple Inheritance

```python
class A: pass
class B(A): pass
```

**MRO:**
```
B → A → object
```

## 2. Multiple Inheritance

```python
class A: pass
class B: pass
class C(B, A): pass
```

**MRO:**
```
C → B → A → object
```

**Explanation:**
- Parent order important

## 3. Diamond

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
```

**MRO:**
```
D → B → C → A → object
```

## 4. `A` B aur C ke Baad Kyun?

**Explanation:**
- `D → B → A` aur `D → C → A` maintain
- C3 consistent order banata hai

## 5. C3 Basic Idea

```
Inheritance graph → C3 → MRO list
```

## 6. C3 Rules

1. Child pehle
2. Parent order preserve
3. Existing inheritance order preserve

## 7. C3 Practical

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
```

**MRO:**
```
D → B → C → A → object
```

## 8. `A` Pehle Kyun Nahi?

**Explanation:**
- B ka MRO: `B → A`
- A pehle rakhne se B ki relationship break

## 9. Parent Order

```python
class C(A, B): pass
```

**MRO:**
```
C → A → B → object
```

```python
class C(B, A): pass
```

**MRO:**
```
C → B → A → object
```

## 10. MRO Conflict

```python
class A: pass
class B(A): pass
class C(A): pass
class X(B, C): pass
class Y(C, B): pass
class Z(X, Y): pass
```

**Error:**
```
TypeError: Cannot create a consistent MRO
```

**Explanation:**
- `X` require: B → C
- `Y` require: C → B
- Contradiction

## 11. Diagram

```
       B       C
       ↓       ↓
       X       Y
      /         \
   B before C   C before B
        \       /
           Z
```

## 12. Error Kab?

```python
class Z(X, Y): pass  # Class creation par error
```

**Explanation:**
- Runtime nahi, class definition par

## 13. MRO Tools

```python
D.mro()       # List
D.__mro__     # Tuple
```

## 14. `super()` + C3

```python
class D(B, C):
    def show(self):
        print("D")
        super().show()
```

**MRO:**
```
D → B → C → A → object
```

**Flow:**
```
D → B → C → A
```

## 15. `super()` Real Meaning

```
B super() → MRO mein B ke baad → C
```

## 16. Direct Parent Call

```python
A.show(self)   # C bypass
```

**Explanation:**
- Cooperative inheritance break

## 17. `super()` + `__init__`

```python
class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()
```

**Output:**
```
D
B
C
A
```

## 18. Cooperative Inheritance

```python
# Har class super().__init__() call
```

## 19. HVAC Example

```python
class SmartAHU(HVAC, NetworkDevice):
    def start(self):
        print("Smart AHU")
        super().start()
```

**MRO:**
```
SmartAHU → HVAC → NetworkDevice → Equipment → object
```

## 20. C3 Mental Model

```
C3 → consistent MRO
   ↓
child first
parent order preserve
existing order preserve
conflict → error
```

## 21. Distinction

```
MRO     → search order
super() → MRO next
C3      → MRO calculate
```

---

# Lesson 36: `Protocol` aur Structural Typing

## 1. Traditional Interface

```python
from abc import ABC, abstractmethod

class Equipment(ABC):
    @abstractmethod
    def start(self):
        pass

class AHU(Equipment):
    def start(self):
        print("AHU started")
```

**Explanation:**
- `AHU` explicitly `Equipment` se inherit

## 2. `Protocol`

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
- Structure match → compatible

## 3. Structural Typing

```
Nominal:    AHU → Equipment (explicit)
Structural: AHU → has start() → matches
```

## 4. Duck Typing

```python
def start_equipment(equipment):
    equipment.start()

start_equipment(AHU())
start_equipment(Pump())
```

**Explanation:**
- `start()` available → kaam karega

## 5. `Protocol` = Duck Typing Static

```python
class Startable(Protocol):
    def start(self) -> None:
        ...
```

**Explanation:**
- Type checker ko bata rahe ho

## 6. Practical

```python
def start_equipment(equipment: Startable) -> None:
    equipment.start()
```

**Explanation:**
- `AHU`, `Pump` dono compatible

## 7. `AHU` Inherit Nahi

```python
class AHU:  # Not AHU(Startable)
```

**Explanation:**
- Structural compatibility

## 8. ABC vs Protocol

| Feature | ABC | Protocol |
|---------|-----|----------|
| Inheritance | Yes | No |
| Style | Nominal | Structural |
| Runtime | Possible | Static |

## 9. ABC Example

```python
class AHU(Startable):
    def start(self):
        print("AHU")
```

## 10. Protocol Example

```python
class AHU:
    def start(self):
        print("AHU")
```

## 11. `...` Ka Matlab

```python
def start(self) -> None:
    ...
```

**Explanation:**
- Implementation nahi
- Specification

## 12. Multiple Methods

```python
class EquipmentProtocol(Protocol):
    equipment_id: str

    def start(self) -> None: ...
    def stop(self) -> None: ...
    def status(self) -> str: ...
```

## 13. Protocol Attributes

```python
class Sensor(Protocol):
    temperature: float
    def read(self) -> float: ...
```

## 14. Read-Only Property

```python
class TemperatureSensor(Protocol):
    @property
    def temperature(self) -> float: ...
```

## 15. Protocol Inheritance

```python
class Controllable(Startable, Stoppable, Protocol):
    def reset(self) -> None: ...
```

## 16. Real-World Advantage

```python
class ExternalDevice:
    def start(self):
        print("Started")
```

**Explanation:**
- External class modify nahi kar sakte
- Protocol use kar sakte ho

## 17. Loose Coupling

```
Function → required interface → start()
```

## 18. Protocol + Polymorphism

```python
def start(device: Startable):
    device.start()

start(AHU())
start(Pump())
start(Chiller())
```

## 19. `@runtime_checkable`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):
    def start(self) -> None: ...

isinstance(AHU(), Startable)   # True
```

## 20. Limitation

```
@runtime_checkable → basic structure check
Full static validation nahi
```

## 21. ABC vs Protocol Kab

**ABC:**
```
Strong hierarchy, shared implementation
```

**Protocol:**
```
Different classes, same capability, loose coupling
```

## 22. `typing` Connection

```
Any → kuch bhi
Union → multiple types
Optional → T ya None
TypeVar → generic
Protocol → required structure
TypedDict → dictionary structure
```

## 23. Final Mental Model

```
ABC → "Meri hierarchy ka member bano"
Protocol → "Required interface do"
Duck Typing → "Behavior do, use kar lo"
Structural Typing → "Structure match → compatible"
```

---

# Lesson 37: `Generic` + `TypeVar` + `Protocol`

## 1. `TypeVar`

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]
```

**Explanation:**
- `T` → type placeholder

## 2. Problem: Reusable Class

```python
class Storage:
    def __init__(self):
        self.data = None

    def set(self, value):
        self.data = value

    def get(self):
        return self.data
```

**Explanation:**
- `get()` type unclear

## 3. Generic Class

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Storage(Generic[T]):
    def __init__(self):
        self.data: T | None = None

    def set(self, value: T):
        self.data = value

    def get(self) -> T | None:
        return self.data
```

**Explanation:**
- `Storage[str]`, `Storage[int]` possible

## 4. `Storage[str]`

```python
name_storage = Storage[str]()
name_storage.set("Muhammad")
```

**Explanation:**
- `T = str`

## 5. `Storage[int]`

```python
salary_storage = Storage[int]()
salary_storage.set(5000)
```

**Explanation:**
- `T = int`

## 6. `Generic[T]`

```
Storage[T]
    ├── Storage[str]
    ├── Storage[int]
    └── Storage[AHU]
```

## 7. Protocol + Generic

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Repository(Protocol[T]):
    def get(self) -> T: ...
    def set(self, value: T) -> None: ...
```

**Explanation:**
- Generic protocol

## 8. Repository Types

```
Repository[str]
Repository[int]
Repository[Employee]
```

## 9. No Inheritance Needed

```python
class MemoryRepository:
    def get(self): ...
    def set(self, value): ...
```

**Explanation:**
- Structural typing

## 10. HVAC Sensor

```python
T = TypeVar("T")

class Sensor(Protocol[T]):
    def read(self) -> T: ...
```

```python
class TemperatureSensor:
    def read(self) -> float:
        return 22.5

class StatusSensor:
    def read(self) -> str:
        return "Running"
```

## 11. Generic Function

```python
def read_sensor(sensor: Sensor[T]) -> T:
    return sensor.read()
```

**Explanation:**
- `T` automatic

## 12. Flow

```
TemperatureSensor → float → T = float
StatusSensor → str → T = str
```

## 13. `Generic` vs `Protocol`

```
Generic → reusable with types
Protocol → required capabilities
```

## 14. Dono Combine

```python
class Repository(Protocol[T]):
    def get(self) -> T: ...
```

```
Protocol → required behavior
T → required data type
```

## 15. Generic Repository

```python
class EmployeeRepository:
    def get(self, id: int) -> Employee: ...
    def save(self, item: Employee) -> None: ...
```

## 16. Large Projects

```
Application → Repository[T] ← MySQL/API/Sheets
```

## 17. `T` Mental Model

```
T = "jo type baad mein decide karoge"
```

## 18. `Generic[T]`

```
Box → T placeholder → Box[str], Box[int]
```

## 19. `Protocol[T]`

```
Reader[T] → read() returns T
Reader[float] → float
Reader[str] → str
```

## 20. HVAC Point Readers

```python
class PointReader(Protocol[T]):
    def read(self, point_name: str) -> T: ...
```

## 21. Protocol Runtime Nahi

```python
reader = PointReader()  # Nahi
```

**Explanation:**
- Contract define karna

## 22. Mental Model

```
TypeVar → T placeholder
Generic → reusable type-aware
Protocol → required structure
Generic + Protocol → reusable + structural + type-safe
```

---

# Lesson 38: `Callable` + `ParamSpec` + Generic Functions

## 1. `Callable`

```python
from collections.abc import Callable

def add(a: int, b: int) -> int:
    return a + b
```

**Type:**
```
Callable[[int, int], int]
```

## 2. Basic Example

```python
def execute(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return func(a, b)

execute(add, 10, 20)   # 30
```

## 3. `Callable` Box

```
Callable → inputs → output
```

## 4. Different Examples

```python
Callable[[], str]           # No args
Callable[[str], int]        # One arg
Callable[[str, int], bool]  # Multiple
```

## 5. Decorator Problem

```python
def logger(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

**Explanation:**
- Type checker ko `*args` types unclear

## 6. `ParamSpec`

```python
from typing import ParamSpec

P = ParamSpec("P")
```

**Explanation:**
- Function ke parameters capture

## 7. `TypeVar` vs `ParamSpec`

```
TypeVar → type
ParamSpec → parameters
```

## 8. Decorator Typing

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def logger(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper
```

## 9. Line by Line

```python
func: Callable[P, R]  # Parameters P, return R
*args: P.args         # Positional preserve
**kwargs: P.kwargs    # Keyword preserve
-> R                  # Return preserve
```

## 10. Example

```python
@logger
def add(a: int, b: int) -> int:
    return a + b
```

**Type:**
```
(int, int) → int (preserved)
```

## 11. Another Example

```python
@logger
def greet(name: str, age: int) -> str:
    return f"{name}: {age}"
```

**Type:**
```
(str, int) → str
```

## 12. `P.args` / `P.kwargs`

```
P.args → positional
P.kwargs → keyword
```

## 13. `ParamSpec` Zaroorat

```python
Callable[..., R]     # Parameters unknown
Callable[P, R]       # Parameters preserved
```

## 14. HVAC Example

```python
@logger
def set_temperature(
    equipment_id: str,
    temperature: float
) -> bool:
    ...
```

**Type:**
```
P = (str, float)
R = bool
```

## 15. `TypeVar` + `ParamSpec`

```
T → type
P → parameters
R → return
```

## 16. Mental Model

```
Original:  P → function → R
Decorator: P → wrapper → R
```

## 17. `Callable` Objects

```python
class Calculator:
    def __call__(self, a: int, b: int) -> int:
        return a + b

calc = Calculator()
calc(10, 20)
```

## 18. Protocol + Callable

```python
class Command(Protocol):
    def __call__(self, equipment_id: str) -> bool: ...
```

## 19. Three Together

```
Protocol → capability
Callable → shape
ParamSpec → parameters
TypeVar → types
```

## 20. Comparison

| Concept | Kya |
|---------|-----|
| `TypeVar` | Generic type |
| `ParamSpec` | Parameters |
| `Callable` | Input/output shape |
| `Protocol` | Required structure |
| `Generic` | Type-aware reusable |

## 21. Decorator Yaad

```python
def logger(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        ...
    return wrapper
```

## 22. Final Mental Model

```
TypeVar → "T kya type?"
ParamSpec → "Parameters kya?"
Callable → "Input/output?"
Protocol → "Capability?"
Generic → "Reusable?"
```

---

# Lesson 39: `TypeVar` — `bound` vs `constraints`

## 1. Simple `TypeVar`

```python
T = TypeVar("T")
```

**Explanation:**
- Unrestricted

## 2. `bound`

```python
T = TypeVar("T", bound=SomeType)
```

**Explanation:**
- `SomeType` ya subclass

## 3. `Animal` Example

```python
class Animal:
    def speak(self):
        print("Animal sound")

T = TypeVar("T", bound=Animal)
```

**Explanation:**
- `T` → Animal ya subclass

## 4. Bound Benefit

```python
def make_sound(animal: T) -> T:
    animal.speak()
    return animal
```

**Explanation:**
- `T <: Animal` → `speak()` allowed

## 5. Subclass Preserve

```python
dog = Dog()
result = identity(dog)
```

**Explanation:**
- `result` → `Dog` (not just `Animal`)

## 6. Constraints

```python
T = TypeVar("T", int, float)
```

**Explanation:**
- Sirf `int` ya `float`

## 7. Bound vs Constraints

**Bound:**
```
Animal → Dog, Cat, Horse...
```

**Constraints:**
```
int, float (fixed)
```

## 8. Visual

**Bound:**
```
Animal
/      \
Dog      Cat
```

**Constraints:**
```
T
├── int
└── float
```

## 9. Subclass Difference

```python
T = TypeVar("T", bound=Animal)   # Dog, Cat OK
T = TypeVar("T", Dog, Cat)       # Only Dog, Cat
```

## 10. Constraint Inference

```python
T = TypeVar("T", int, float)

def get_value(value: T) -> T:
    return value

get_value(10)     # int
get_value(10.5)   # float
```

## 11. Bound + Protocol

```python
class HasID(Protocol):
    id: int

T = TypeVar("T", bound=HasID)
```

## 12. HVAC Example

```python
class Equipment:
    def start(self):
        print("Started")

T = TypeVar("T", bound=Equipment)

def start_equipment(equipment: T) -> T:
    equipment.start()
    return equipment

ahu = start_equipment(AHU())   # AHU
vav = start_equipment(VAV())   # VAV
```

## 13. Simple vs Generic

```python
# Simple
def start_equipment(equipment: Equipment) -> Equipment:
    ...

# Generic
def start_equipment(equipment: T) -> T:
    ...
```

**Explanation:**
- Generic → subtype preserve

## 14. Bound Mental Model

```
T → Equipment boundary
   ├── AHU
   ├── VAV
   └── Chiller
```

## 15. Constraints Mental Model

```
T → int, float (fixed)
```

## 16. Bound vs Union

```python
# Union
def process(value: int | float): ...

# TypeVar
T = TypeVar("T", int, float)

def process(value: T) -> T:
    return value
```

**Explanation:**
- Union → possibilities
- TypeVar → relationship preserve

## 17. Example

```python
T = TypeVar("T", int, float)

def same(value: T) -> T:
    return value
```

```
same(10)   # int → int
same(2.5)  # float → float
```

## 18. Comparison

| Concept | Meaning |
|---------|---------|
| `TypeVar("T")` | Any type |
| `bound=Animal` | Animal ya subclass |
| `TypeVar("T", int, float)` | Fixed choices |
| `int \| float` | Value possibilities |

## 19. Practical Rule

```
"Koi bhi type"         → T = TypeVar("T")
"Subclass of X"        → T = TypeVar("T", bound=X)
"Sirf ye types"        → T = TypeVar("T", int, float)
"Value int/float"      → int | float
```

## 20. Complete Example

```python
T = TypeVar("T", bound=Equipment)

def start_equipment(equipment: T) -> T:
    equipment.start()
    return equipment

ahu = start_equipment(AHU())   # T = AHU
vav = start_equipment(VAV())   # T = VAV
start_equipment("hello")       # Error
```

## 21. Final Mental Model

```
TypeVar → generic placeholder
bound → upper boundary
constraints → fixed choices
T + input/output → relationship preserve
```

---

# Lesson 40: `TypedDict` — Deep Understanding

## 1. `TypedDict` Kya Hai?

```python
from typing import TypedDict

class EmployeeData(TypedDict):
    name: str
    salary: float
    department: str
```

**Explanation:**
- Dictionary structure define

## 2. Normal `dict` vs `TypedDict`

```python
# Normal
employee: dict = {"name": "Ali", "salary": 5000}

# TypedDict
employee: EmployeeData = {
    "name": "Ali",
    "salary": 5000.0,
    "department": "HVAC"
}
```

## 3. Runtime Par

```python
employee = EmployeeData(name="Ali", salary=5000.0, department="HVAC")
print(type(employee))
```

**Output:**
```
<class 'dict'>
```

**Explanation:**
- Runtime → normal dict

## 4. Validation Nahi

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": "5000",   # Wrong type
    "department": "HVAC"
}
```

**Explanation:**
- Static type checker error
- Runtime automatically reject nahi

## 5. Work Order Example

```python
class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: str
```

## 6. Key Typing

```python
data["salary"]   # float
data["name"]     # str
```

## 7. Missing Key

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": 5000
    # department missing
}
```

**Explanation:**
- Static checker error

## 8. Extra Key

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": 5000,
    "department": "HVAC",
    "age": 30   # Extra
}
```

**Explanation:**
- Flag kar sakta hai

## 9. `total=False`

```python
class EmployeeData(TypedDict, total=False):
    name: str
    salary: float
    department: str

employee: EmployeeData = {"name": "Ali"}   # OK
```

## 10. `Required` / `NotRequired`

```python
from typing import TypedDict, NotRequired

class EmployeeData(TypedDict):
    name: str
    salary: float
    comment: NotRequired[str]
```

## 11. Mix

```python
class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: NotRequired[str]
```

## 12. `Required`

```python
class WorkOrder(TypedDict, total=False):
    work_order_number: Required[str]
    description: Required[str]
    comment: str
```

## 13. Combination

```python
class EquipmentData(TypedDict, total=False):
    equipment_id: Required[str]
    equipment_type: Required[str]
    temperature: float
    humidity: float
    comment: str
```

## 14. Nested `TypedDict`

```python
class Location(TypedDict):
    floor: str
    area: str

class Equipment(TypedDict):
    equipment_id: str
    equipment_type: str
    location: Location
```

## 15. API JSON

```python
class EquipmentResponse(TypedDict):
    equipment_id: str
    status: str
    temperature: float
```

## 16. `TypedDict` vs `dataclass`

```python
# TypedDict
employee = {"name": "Ali", "salary": 5000}

# Dataclass
@dataclass
class Employee:
    name: str
    salary: float

employee = Employee("Ali", 5000)
```

**Rule:**
- Dictionary → TypedDict
- Behavior → dataclass

## 17. Visual

```
TypedDict → {"name": "Ali", ...}
Dataclass → Employee(name="Ali", ...)
```

## 18. `TypedDict` vs `dict`

```python
# dict
data: dict[str, object]

# TypedDict
class EmployeeData(TypedDict):
    name: str
    salary: float
```

## 19. `TypedDict` vs `Protocol`

```
TypedDict → dictionary structure
Protocol → object behavior
```

## 20. `TypedDict` vs Normal Class

```
Normal class → data + behavior
TypedDict → data structure
```

## 21. Work Order Example

```python
def create_folder(work_order: WorkOrder) -> str:
    return work_order["work_order_number"]
```

**Explanation:**
- Type checker knows structure

## 22. Limitation

```python
employee.show()   # Methods nahi
```

## 23. Runtime Inspection

```python
EmployeeData.__annotations__
EmployeeData.__required_keys__
EmployeeData.__optional_keys__
```

## 24. JSON → TypedDict

```
JSON → dict → TypedDict annotation → static info
```

## 25. Complete Example

```python
class Location(TypedDict):
    floor: str
    area: str

class EquipmentData(TypedDict):
    equipment_id: str
    equipment_type: str
    location: Location
    temperature: NotRequired[float]
    comment: NotRequired[str]

equipment: EquipmentData = {
    "equipment_id": "AHU-01",
    "equipment_type": "AHU",
    "location": {
        "floor": "34",
        "area": "Mechanical Room"
    },
    "temperature": 22.5
}
```

## 26. Mental Model

```
dict → normal
TypedDict → structure
Required → lazmi
NotRequired → optional
total=False → all optional
Nested → structured dict
```

**Comparison:**
```
TypedDict → data structure
dataclass → data + behavior
Protocol → behavior/interface
class → data + behavior + OOP
```

---

**Ab ye guide complete hai (Lessons 31-40).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀