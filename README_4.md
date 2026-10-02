## Lesson 31: `global` aur `nonlocal` ko Deeply Samjho

Ab LEGB ke baad next important concept ye hai ke **scope ko sirf read nahi, modify kaise karte hain**.

### 1. Normal assignment → Local

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

Function ke andar `x = 20` ne **new local `x`** bana diya.

---

### 2. `global` → Global variable modify

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

`global x` ka matlab:

> "Is function mein `x` ko local mat samjho; module/global scope wala `x` use karo."

---

### 3. `nonlocal` → Enclosing variable modify

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

Yahan `x` global nahi hai.

`x` `outer()` ke andar hai, isliye `inner()` mein:

```python
nonlocal x
```

use hua.

---

## 4. `global` vs `nonlocal`

```text
global
   ↓
Global scope

nonlocal
   ↓
Nearest enclosing function scope
```

Example:

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

Output:

```text
CHANGED
GLOBAL
```

`nonlocal` ne `outer()` ka `x` change kiya, global ka nahi.

---

## 5. `nonlocal` nearest enclosing scope ko target karta hai

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

Output:

```text
changed
outer
```

`inner()` ka `nonlocal x` **middle() wala x** change karta hai, kyun ke woh nearest enclosing `x` hai.

---

## 6. `nonlocal` ke liye enclosing variable hona zaroori hai

Ye invalid hai:

```python
def outer():

    def inner():
        nonlocal x
        x = 10

    inner()
```

Error:

```text
SyntaxError: no binding for nonlocal 'x' found
```

Kyun?

`inner()` ke bahar kisi enclosing function mein `x` exist hi nahi karta.

---

## 7. Mutable object ka interesting case

Ye dekho:

```python
def outer():
    data = []

    def inner():
        data.append(10)

    inner()
    print(data)

outer()
```

Output:

```text
[10]
```

Yahan `nonlocal` ki zaroorat nahi.

Kyun?

Hum `data` ko **reassign** nahi kar rahe:

```python
data = [...]
```

Hum existing list ko mutate kar rahe hain:

```python
data.append(10)
```

Lekin:

```python
def inner():
    data = [10]
```

alag local `data` bana dega.

Aur:

```python
def inner():
    nonlocal data
    data = [10]
```

enclosing `data` ko replace karega.

---

## 8. Ye distinction bohat important hai

```text
Mutation:
data.append(10)
```

→ existing object change

```text
Rebinding:
data = [10]
```

→ variable ko new object se bind

`nonlocal`/`global` ki zaroorat **rebinding** mein hoti hai.

---

## 9. Closure + `nonlocal`

Pichli lesson ka counter ab samjho:

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
c = counter()

print(c())
print(c())
print(c())
```

Output:

```text
1
2
3
```

Yahan:

```text
counter()
   ↓
count = 0
   ↓
increment()
   ↓
nonlocal count
   ↓
count = 1
   ↓
count = 2
   ↓
count = 3
```

`count` function ke bahar directly accessible nahi, lekin closure usko remember karta hai.

---

# 10. Closure vs Class

Same counter class se:

```python
class Counter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count
```

Closure se:

```python
def counter():

    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
```

Dono state maintain kar sakte hain.

```text
Class
→ state = self.count

Closure
→ state = enclosing variable
```

---

# 11. Decorator mein `nonlocal`

Ye especially important hai kyun ke tum decorators already padh chuke ho.

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

Yahan:

```python
count = 0
```

enclosing scope mein hai.

`wrapper()`:

```python
nonlocal count
```

use karke usko update karta hai.

---

# 12. `global` aur `nonlocal` ko LEGB se connect karo

Ab complete picture:

```text
             LEGB

L → Local
E → Enclosing
G → Global
B → Built-in
```

Aur modification ke liye:

```text
Local
  ↑
normal assignment

Enclosing
  ↑
nonlocal

Global
  ↑
global
```

---

# 13. Ek important interview-style example

Iska output predict karo:

```python
x = 10

def outer():
    x = 20

    def inner():
        print(x)

    inner()

outer()
```

Answer:

```text
20
```

Reason:

```text
inner()
 ↓
Local → x nahi
 ↓
Enclosing → x = 20
```

---

Ab ye:

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

Output:

```text
20
30
```

Kyun?

`global x` ne `outer()` ke `x` ko target nahi kiya.

Usne directly:

```text
Global x
```

ko target kiya.

---

## Final mental model

```text
x = value
→ normally current function ka Local x

global x
→ Global x

nonlocal x
→ nearest enclosing function ka x
```

Aur LEGB:

```text
Local
  ↓
Enclosing
  ↓
Global
  ↓
Built-in
```

**Next Lesson 32:** `namespace` aur `__dict__` — Python mein variables actually **kahan store hote hain**, aur `globals()`, `locals()`, `vars()`, `obj.__dict__` kaise kaam karte hain.

# Lesson 32: Namespace aur `__dict__`

Ab hum **Scope ke baad next level** par ja rahe hain:

> Variable ka naam Python **kahan store karta hai**, aur `globals()`, `locals()`, `vars()` aur `__dict__` kya karte hain?

Scope batata hai **name kahan search hoga**.
Namespace batata hai **name → value mapping kahan rakhi hui hai**.

---

## 1. Namespace kya hota hai?

Simple example:

```python
name = "Ali"
age = 25
```

Python conceptually ek mapping rakhta hai:

```text
name → "Ali"
age  → 25
```

Yani:

```text
Namespace = names → objects
```

Python mein namespace ko roughly dictionary ki tarah samajh sakte ho.

---

## 2. Global Namespace

```python
name = "Ali"
age = 25

print(globals())
```

`globals()` current module ka global namespace dictionary return karta hai.

Conceptually:

```python
{
    "name": "Ali",
    "age": 25,
    ...
}
```

Isliye:

```python
globals()["name"]
```

result:

```text
Ali
```

Aur theoretically:

```python
globals()["age"] = 30
```

ke baad:

```python
print(age)
```

output:

```text
30
```

---

# 3. `locals()`

Function ke andar:

```python
def test():
    name = "Ali"
    age = 25

    print(locals())

test()
```

Conceptually output:

```python
{
    "name": "Ali",
    "age": 25
}
```

Yani:

```text
globals()
→ global namespace

locals()
→ current local namespace
```

---

# 4. `globals()` vs `locals()`

```python
name = "Global"

def test():
    name = "Local"

    print("locals:", locals())
    print("globals:", globals()["name"])

test()
```

Output conceptually:

```text
locals: {'name': 'Local'}
globals: Global
```

Dono mein `name` hai, lekin dono **different namespaces** hain.

```text
Global Namespace
┌─────────────────┐
│ name → Global   │
└─────────────────┘

Local Namespace
┌─────────────────┐
│ name → Local    │
└─────────────────┘
```

---

# 5. `__dict__`

Ab OOP se connect karo.

Class:

```python
class Employee:
    company = "ABC"
```

Class ke paas namespace hota hai.

Usko dekh sakte ho:

```python
print(Employee.__dict__)
```

Ismein roughly:

```python
{
    "company": "ABC",
    ...
}
```

mil jayega.

---

# 6. Object ka `__dict__`

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp = Employee("Ali", 5000)

print(emp.__dict__)
```

Output:

```python
{
    'name': 'Ali',
    'salary': 5000
}
```

Yahan bohat important connection hai:

```text
self.name = "Ali"
       ↓
object ke namespace mein
       ↓
"name" → "Ali"
```

---

# 7. `__dict__` ko dictionary ki tarah samjho

```python
emp.__dict__
```

roughly:

```python
{
    "name": "Ali",
    "salary": 5000
}
```

Isliye:

```python
emp.name
```

conceptually attribute lookup karta hai.

Aur:

```python
emp.__dict__["name"]
```

directly instance namespace se value dekh raha hai.

Example:

```python
print(emp.name)
print(emp.__dict__["name"])
```

Dono:

```text
Ali
Ali
```

---

# 8. `__dict__` modify bhi kar sakte ho

```python
emp.__dict__["salary"] = 7000

print(emp.salary)
```

Output:

```text
7000
```

Kyun?

Object namespace mein:

```text
salary → 7000
```

ho gaya.

---

# 9. Naya attribute manually add

```python
emp.__dict__["department"] = "HVAC"

print(emp.department)
```

Output:

```text
HVAC
```

Humne directly:

```python
emp.department = "HVAC"
```

nahi likha, lekin namespace mein entry add kar di.

---

# 10. `vars()`

Python mein:

```python
vars(obj)
```

bohat commonly `obj.__dict__` ke equivalent hota hai, jab object ka `__dict__` available ho.

Example:

```python
class Employee:
    def __init__(self, name):
        self.name = name

emp = Employee("Ali")

print(vars(emp))
```

Output:

```python
{'name': 'Ali'}
```

So:

```python
vars(emp)
```

≈

```python
emp.__dict__
```

---

# 11. `vars()` aur `__dict__`

Simple mental model:

```text
vars(emp)
    ↓
emp.__dict__
    ↓
instance namespace
```

Lekin yaad rakho: **har object ke paas `__dict__` zaroori nahi hota**. `__slots__` jaisi techniques se objects ke paas normal instance dictionary nahi bhi ho sakti.

---

# 12. Class ka `__dict__`

```python
class Equipment:

    category = "HVAC"

    def start(self):
        print("Starting")
```

Ab:

```python
print(Equipment.__dict__)
```

mein roughly:

```text
category → "HVAC"
start    → function object
```

Yani class namespace mein methods bhi stored hote hain.

---

# 13. Instance aur Class namespace different hain

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

emp = Employee("Ali")
```

Ab:

```python
print(Employee.__dict__)
```

mein:

```text
company
__init__
...
```

Aur:

```python
print(emp.__dict__)
```

mein:

```text
name
```

So:

```text
Class namespace
┌────────────────────┐
│ company → ABC      │
│ __init__ → method  │
└────────────────────┘

Instance namespace
┌────────────────────┐
│ name → Ali         │
└────────────────────┘
```

---

# 14. Attribute lookup se connection

Ab Lesson 13 aur 14 connect karo.

```python
emp.name
```

Python roughly instance attribute ko search karta hai.

Simplified view:

```text
emp.name
   ↓
data descriptor?
   ↓
emp.__dict__
   ↓
class / MRO
```

Isliye:

```python
emp.__dict__["name"]
```

instance ka actual stored value de sakta hai.

---

# 15. Class variable example

```python
class Employee:
    company = "ABC"

emp = Employee()
```

Ab:

```python
print(emp.__dict__)
```

Output:

```python
{}
```

Lekin:

```python
print(emp.company)
```

Output:

```text
ABC
```

Kyun?

`company` instance namespace mein nahi hai.

Python class mein search karta hai:

```text
emp.company
    ↓
emp.__dict__
    ↓
company nahi
    ↓
Employee.__dict__
    ↓
company = "ABC"
```

---

# 16. Instance variable add karo

```python
emp.company = "XYZ"
```

Ab:

```python
print(emp.__dict__)
```

Output:

```python
{'company': 'XYZ'}
```

Ab instance ka apna `company` ban gaya.

```text
Employee.company
→ ABC

emp.company
→ XYZ
```

Ye wahi **shadowing** concept hai jo humne LEGB mein dekha tha, lekin yahan attribute lookup ke context mein.

---

# 17. Namespace aur Scope same cheez nahi

Ye distinction important hai.

### Scope

Batata hai:

> Name **kahan accessible / resolved** hai?

### Namespace

Batata hai:

> Names aur objects ki **mapping kahan maintained** hai?

Example:

```python
x = 10

def test():
    x = 20
```

Yahan:

```text
Global namespace
x → 10

Local namespace
x → 20
```

Scope rules decide karte hain ke `x` ko access karte waqt kaunsa namespace check hoga.

---

# 18. Closure mein namespace

Ab closure:

```python
def outer():

    x = 10

    def inner():
        return x

    return inner
```

`inner` ke paas `x` ka reference capture ho jata hai.

Isko inspect karne ke liye:

```python
f = outer()

print(f.__code__.co_freevars)
print(f.__closure__)
```

Conceptually:

```text
co_freevars
→ ('x',)

closure
→ captured value
```

Ye wahi closure concept hai jo humne Lesson 29 mein padha tha.

---

# 19. `globals()` practical use

Kabhi-kabhi dynamic code/frameworks mein global namespace inspect kiya jata hai:

```python
x = 100

print(globals()["x"])
```

Output:

```text
100
```

Aur:

```python
globals()["y"] = 200

print(y)
```

Output:

```text
200
```

Lekin normal application code mein variables ko is tarah dynamically manipulate karna usually unnecessary hota hai.

---

# 20. `locals()` practical use

Debugging ke liye:

```python
def calculate(a, b):

    total = a + b
    result = total * 2

    print(locals())

calculate(10, 20)
```

Conceptually:

```python
{
    'a': 10,
    'b': 20,
    'total': 30,
    'result': 60
}
```

Ye debugging mein useful ho sakta hai.

---

# 21. `dir()` vs `__dict__`

Ye dono confuse mat karna.

```python
dir(emp)
```

available/relevant attribute names ki list deta hai.

```python
emp.__dict__
```

instance namespace mein actually stored attributes deta hai.

Example:

```python
print(dir(emp))
print(emp.__dict__)
```

`dir()` bohat zyada names dikha sakta hai, including inherited attributes.

`__dict__` normally instance ke directly stored attributes dikhata hai.

---

# 22. HVAC example

```python
class AHU:

    system_type = "HVAC"

    def __init__(self, equipment_id, temperature):
        self.equipment_id = equipment_id
        self.temperature = temperature

ahu = AHU("AHU-01", 22)
```

Instance namespace:

```python
print(ahu.__dict__)
```

Output:

```python
{
    'equipment_id': 'AHU-01',
    'temperature': 22
}
```

Class namespace:

```python
print(AHU.__dict__)
```

mein:

```text
system_type
__init__
...
```

---

# 23. Complete connection

Ab tak ke lessons ko connect karo:

```text
Scope
  ↓
Name kahan search hoga?

LEGB
  ↓
Local → Enclosing → Global → Built-in

Namespace
  ↓
Name → Object mapping

globals()
  ↓
Global namespace

locals()
  ↓
Current local namespace

__dict__
  ↓
Object/Class namespace

Attribute lookup
  ↓
descriptor → instance → class/MRO
```

### Golden mental model

```text
VARIABLE NAME
     │
     ▼
NAMESPACE
(name → object)
     │
     ▼
SCOPE RULES
     │
     ▼
Python decides
kaunsa name/value use karna hai
```

**Next Lesson 33:** `__slots__` — `__dict__` ke saath iska relation, memory optimization, fixed attributes, aur kyun kuch Python objects ke paas `__dict__` nahi hota.

# Lesson 33: `__slots__`

Ab hum `__dict__` ke opposite concept ko samjhte hain:

> **`__slots__` object ke allowed attributes ko define karta hai aur normal instance `__dict__` ko hata sakta hai.**

Ye especially useful hai jab **bohat saare objects** create karne hon aur memory optimize karni ho.

---

## 1. Normal class mein kya hota hai?

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp = Employee("Ali", 5000)
```

Normally:

```python
print(emp.__dict__)
```

Output:

```python
{'name': 'Ali', 'salary': 5000}
```

Yani object ke paas apna `__dict__` hota hai.

---

# 2. `__slots__`

Ab:

```python
class Employee:
    __slots__ = ("name", "salary")

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
```

Object:

```python
emp = Employee("Ali", 5000)
```

Ab normally:

```python
print(emp.__dict__)
```

par:

```text
AttributeError
```

kyun ke is class ke instances ke paas normal `__dict__` nahi hota.

---

# 3. `__slots__` mein kya define kiya?

```python
__slots__ = ("name", "salary")
```

Matlab:

> Is class ke normal instances ke liye ye attributes allowed hain.

```text
Employee
   │
   ├── name
   └── salary
```

---

# 4. Extra attribute add karne ki koshish

Normal class:

```python
class Employee:
    def __init__(self):
        self.name = "Ali"

emp = Employee()

emp.department = "HVAC"
```

Ye normally kaam karega.

Lekin slots:

```python
class Employee:
    __slots__ = ("name",)

    def __init__(self):
        self.name = "Ali"

emp = Employee()

emp.department = "HVAC"
```

Error:

```text
AttributeError
```

Kyun?

`department` slots mein defined nahi hai.

---

# 5. Iska main benefit

Agar tumhare paas:

```text
10 objects
```

hain, difference chhota ho sakta hai.

Lekin agar:

```text
100,000
1,000,000
```

objects hain, to per-instance memory overhead important ho sakta hai.

`__slots__` normal instance dictionary ko avoid karke memory overhead reduce kar sakta hai.

---

# 6. Normal vs slots

### Normal

```python
class Equipment:
    def __init__(self, equipment_id, temperature):
        self.equipment_id = equipment_id
        self.temperature = temperature
```

Conceptually:

```text
Object
  ↓
__dict__
  ├── equipment_id
  └── temperature
```

### `__slots__`

```python
class Equipment:
    __slots__ = ("equipment_id", "temperature")

    def __init__(self, equipment_id, temperature):
        self.equipment_id = equipment_id
        self.temperature = temperature
```

Conceptually:

```text
Object
  ↓
fixed slot storage
  ├── equipment_id
  └── temperature
```

---

# 7. `__slots__` = private nahi

Ye bohat important hai.

```python
class Employee:
    __slots__ = ("salary",)
```

Iska matlab ye nahi:

> salary private hai.

Tum phir bhi:

```python
emp.salary
```

access kar sakte ho.

`__slots__` ka purpose mainly:

* allowed attributes define karna
* instance `__dict__` avoid karna
* memory overhead reduce karna
* accidental arbitrary attributes ko prevent karna

---

# 8. `__slots__` security mechanism nahi

Example:

```python
class Employee:
    __slots__ = ("salary",)
```

Iska matlab **security boundary** nahi hai.

Ye encapsulation ka replacement bhi nahi.

Agar sensitive data protect karna ho to `__slots__` us purpose ke liye nahi bana.

---

# 9. `__slots__` + inheritance

Ye thora important hai.

```python
class Employee:
    __slots__ = ("name",)

class Manager(Employee):
    __slots__ = ("department",)
```

Ab Manager ke paas:

```text
Employee
 └── name

Manager
 └── department
```

dono slots available hain.

```python
manager = Manager()

manager.name = "Ali"
manager.department = "HVAC"
```

---

# 10. Agar child mein `__slots__` na ho?

```python
class Employee:
    __slots__ = ("name",)

class Manager(Employee):
    pass
```

Yahan child class ka behavior important hai: `Manager` instances ko normal `__dict__` mil sakta hai.

Isliye agar slots ko inheritance hierarchy mein consistently use karna hai, child classes mein bhi appropriate `__slots__` define karna chahiye.

---

# 11. Empty `__slots__`

Kabhi:

```python
class Base:
    __slots__ = ()
```

use kiya jata hai.

Iska matlab:

> Is class ke direct instances ke liye additional instance attributes ke slots define nahi kiye gaye.

Example:

```python
class Base:
    __slots__ = ()

obj = Base()
```

Ab:

```python
obj.x = 10
```

allowed nahi hoga.

---

# 12. `__slots__` mein `__dict__` explicitly add kar sakte ho

Agar tum chahte ho ke slots bhi hon aur arbitrary attributes bhi allowed hon:

```python
class Employee:
    __slots__ = ("name", "salary", "__dict__")
```

Ab:

```python
emp = Employee()

emp.name = "Ali"
emp.salary = 5000
emp.department = "HVAC"
```

`department` possible hai kyun ke `__dict__` available hai.

So:

```text
__slots__
+
__dict__
=
fixed slots + dynamic attributes
```

Lekin phir `__dict__` ka memory-saving benefit partly reduce ho jata hai.

---

# 13. `__weakref__`

Advanced point:

Kuch classes ko weak references support karne ke liye `__weakref__` slot ki zaroorat hoti hai, depending on inheritance/design.

Example:

```python
class Employee:
    __slots__ = ("name", "__weakref__")
```

Ab object weak-referenceable ho sakta hai.

Abhi ke liye isko sirf itna yaad rakho:

```text
__weakref__
→ weak reference support
```

Weak references ko baad mein separately detail mein samajhna better hai.

---

# 14. HVAC example

Normal:

```python
class Sensor:
    def __init__(self, point_id, temperature):
        self.point_id = point_id
        self.temperature = temperature
```

Agar tumhare paas:

```text
100,000 sensors
```

ke objects hain, unnecessary per-object dictionary overhead memory consume kar sakta hai.

Slots:

```python
class Sensor:
    __slots__ = ("point_id", "temperature")

    def __init__(self, point_id, temperature):
        self.point_id = point_id
        self.temperature = temperature
```

Ye high-volume object models mein useful ho sakta hai.

---

# 15. `__slots__` aur `@property`

Dono ek saath use ho sakte hain.

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

Yahan:

```text
__slots__
→ storage control

@property
→ access/validation control
```

Dono ka purpose different hai.

---

# 16. `__slots__` aur Descriptor ka connection

Ye tumhare Lesson 14 se connect hota hai.

`__slots__` internally descriptor-based machinery use karta hai for slot attributes.

Conceptually:

```text
__slots__
    ↓
slot descriptors
    ↓
attribute access/storage
```

Isliye `__slots__` samajhne ke baad descriptors ka concept aur clear hota hai.

---

# 17. `__dict__` vs `__slots__`

| Feature                   | Normal class   | `__slots__`              |
| ------------------------- | -------------- | ------------------------ |
| Instance `__dict__`       | Usually yes    | Usually no               |
| Arbitrary new attributes  | Yes            | No                       |
| Memory overhead           | Usually higher | Often lower              |
| Fixed attribute layout    | No             | Yes                      |
| Attribute typo protection | No             | Often yes                |
| `@property`               | Yes            | Yes                      |
| Inheritance               | Yes            | Yes, with considerations |

---

# 18. Important: `__slots__` automatically faster nahi

Common misconception:

> "`__slots__` use karunga to Python har case mein faster ho jayega."

Aisa guarantee nahi hai.

Primary reason:

```text
memory overhead reduce karna
```

Attribute access bhi kuch situations mein beneficial ho sakta hai, lekin `__slots__` ko primarily **memory/layout optimization** samjho.

---

# 19. Normal object vs slots mental model

### Normal

```text
emp
 │
 └── __dict__
       │
       ├── name → "Ali"
       └── salary → 5000
```

### Slots

```text
emp
 │
 ├── name slot → "Ali"
 └── salary slot → 5000
```

Isliye:

```python
emp.__dict__
```

normal class mein mil sakta hai,

lekin slots-only class mein nahi.

---

# 20. Scope → Namespace → `__dict__` → `__slots__`

Ab hamari lessons ka connection:

```text
Scope
  ↓
name kahan accessible?

LEGB
  ↓
name kahan search hoga?

Namespace
  ↓
name → object mapping

__dict__
  ↓
object/class ka dynamic namespace

__slots__
  ↓
instance storage ko fixed slots ki taraf le jata hai
```

### Ek line mein:

> **`__dict__` dynamic attribute storage deta hai, jab ke `__slots__` predefined attributes ke liye fixed storage structure provide karta hai aur normal instance `__dict__` ko avoid kar sakta hai.**

**Next Lesson 34:** Python ka **MRO + `super()` deeply** — multiple inheritance mein Python parent methods ko kis order mein search karta hai, `super()` actually kya karta hai, aur diamond inheritance kaise solve hoti hai.

# Lesson 34: MRO + `super()` Deeply

Ab hum **Inheritance ka advanced part** start karte hain.

Do concepts bohat important hain:

```text
MRO
↓
Method Resolution Order

super()
↓
MRO ke according next class ko call karta hai
```

---

## 1. MRO kya hai?

MRO ka full form:

> **Method Resolution Order**

Jab Python ko kisi method ya attribute ko find karna hota hai, especially inheritance mein, Python ek specific order follow karta hai.

Example:

```python
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    pass

dog = Dog()
dog.speak()
```

Python search karega:

```text
Dog
 ↓
Animal
 ↓
object
```

`Dog` mein `speak()` nahi mila.

`Animal` mein mil gaya.

Output:

```text
Animal
```

---

# 2. MRO directly dekho

Python mein:

```python
print(Dog.mro())
```

Conceptually:

```text
[
    Dog,
    Animal,
    object
]
```

Ya:

```python
print(Dog.__mro__)
```

same inheritance resolution chain deta hai.

---

# 3. `object` kya hai?

Python 3 mein normal classes ultimately `object` se derive hoti hain.

```python
class Animal:
    pass
```

Conceptually:

```python
class Animal(object):
    pass
```

Isliye:

```text
Dog
 ↓
Animal
 ↓
object
```

MRO ka end normally:

```text
object
```

hota hai.

---

# 4. Method overriding + MRO

```python
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    def speak(self):
        print("Dog")
```

Ab:

```python
dog = Dog()
dog.speak()
```

Output:

```text
Dog
```

MRO:

```text
Dog
 ↓
Animal
 ↓
object
```

Python pehle `Dog` check karta hai.

`Dog.speak()` mil gaya.

Search stop.

---

# 5. `super()` ka basic concept

```python
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    def speak(self):
        print("Dog")
        super().speak()
```

Ab:

```python
dog = Dog()
dog.speak()
```

Output:

```text
Dog
Animal
```

Yahan:

```python
super().speak()
```

ka matlab simply:

> "Mujhe MRO ke according **next appropriate implementation** ka `speak()` do."

---

# 6. Important: `super()` ka matlab "parent" exactly nahi

Beginners usually samajhte hain:

```python
super()
```

=

```text
parent class
```

Ye **simple single inheritance mein aksar aisa lagta hai**, lekin technically:

> `super()` MRO mein current class ke baad wali class ko search karta hai.

Ye difference multiple inheritance mein bohat important hai.

---

# 7. Simple inheritance mein

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()
```

MRO:

```text
B
↓
A
↓
object
```

`super()` from `B`:

```text
B ke baad MRO mein
↓
A
```

Isliye `A.show()` execute hota hai.

---

# 8. `super()` with `__init__`

Ye bohat common pattern hai:

```python
class Employee:
    def __init__(self, name):
        self.name = name

class Manager(Employee):
    def __init__(self, name, department):
        super().__init__(name)
        self.department = department
```

Create:

```python
manager = Manager("Ali", "HVAC")
```

Ab:

```python
print(manager.name)
print(manager.department)
```

Output:

```text
Ali
HVAC
```

Flow:

```text
Manager.__init__()
       ↓
super().__init__()
       ↓
Employee.__init__()
       ↓
self.name = "Ali"
       ↓
back to Manager
       ↓
self.department = "HVAC"
```

---

# 9. `super()` ka fayda

Agar `super()` use na karo:

```python
class Manager(Employee):
    def __init__(self, name, department):
        self.name = name
        self.department = department
```

Ye bhi kaam kar sakta hai.

Lekin parent initialization ki logic duplicate ho jayegi.

Agar parent mein future mein:

```python
self.employee_id = ...
self.name = ...
self.status = ...
```

add hua, child manually update karna padega.

`super()` code reuse karta hai.

---

# 10. Multiple inheritance

Ab interesting part.

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
```

Ab:

```python
d = D()
d.show()
```

Output:

```text
D
B
C
A
```

Ye beginners ke liye surprising hota hai.

Kyun?

MRO.

---

# 11. `D` ka MRO

```python
print(D.mro())
```

Conceptually:

```text
D
B
C
A
object
```

Isliye:

```python
D.show()
```

→ D

`super()`:

```text
D ke baad → B
```

B ka `super()`:

```text
B ke baad → C
```

C ka `super()`:

```text
C ke baad → A
```

A ka `super()`:

```text
A ke baad → object
```

Result:

```text
D
↓
B
↓
C
↓
A
```

---

# 12. Diamond inheritance

Ye structure:

```text
       A
      / \
     B   C
      \ /
       D
```

kehlata hai:

> **Diamond inheritance**

Code:

```python
class A:
    def show(self):
        print("A")

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

MRO:

```text
D
↓
B
↓
C
↓
A
↓
object
```

Python C ko A se pehle consider karta hai.

---

# 13. MRO manually calculate karna

Is example mein:

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

Python ko multiple inheritance mein ek **consistent order** chahiye.

Python C3 linearization algorithm use karta hai.

Result:

```text
D → B → C → A → object
```

Abhi C3 algorithm ka mathematical detail zaroori nahi; practical level par `Class.mro()` use karke exact order inspect kar sakte ho.

---

# 14. `super()` multiple inheritance mein powerful kyun hai?

Imagine:

```python
class B(A):
    def show(self):
        print("B")
        super().show()
```

Aur:

```python
class C(A):
    def show(self):
        print("C")
        super().show()
```

Agar `D(B, C)` hai:

```python
super()
```

B se direct A par jump nahi karta.

B ka MRO-relative next:

```text
C
```

hai.

Isliye:

```text
B
↓
C
↓
A
```

---

# 15. Ye line yaad rakho

> **`super()` parent ko nahi, MRO mein current class ke baad next implementation ko call karta hai.**

Ye MRO + `super()` ka sabse important concept hai.

---

# 16. `super()` ka object kya hota hai?

Technically:

```python
super()
```

ek **super object** return karta hai.

Example:

```python
s = super()
```

Ye object MRO-based attribute lookup ko facilitate karta hai.

Isliye:

```python
super().show()
```

ka matlab:

```text
super object se show lookup karo
```

---

# 17. `super()` mein arguments

Normally modern Python mein:

```python
super()
```

enough hai.

Lekin technically:

```python
super(CurrentClass, self)
```

bhi likh sakte ho.

Example:

```python
class Dog(Animal):

    def speak(self):
        super(Dog, self).speak()
```

Modern Python mein preferred:

```python
super().speak()
```

---

# 18. `super()` sirf methods ke liye nahi

Attributes ke liye bhi use ho sakta hai.

```python
class A:
    value = 10

class B(A):
    value = 20

    def show(self):
        print(super().value)
```

Output:

```text
10
```

Yahan `super()` MRO ke next class mein `value` search karta hai.

---

# 19. HVAC example

```python
class Equipment:

    def start(self):
        print("Equipment starting")

class AHU(Equipment):

    def start(self):
        super().start()
        print("AHU fan starting")
```

Run:

```python
ahu = AHU()
ahu.start()
```

Output:

```text
Equipment starting
AHU fan starting
```

Flow:

```text
AHU.start()
    ↓
super().start()
    ↓
Equipment.start()
```

---

# 20. Multiple HVAC components

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
```

Output:

```text
Equipment
Fan
AHU
```

MRO:

```text
AHU
 ↓
Fan
 ↓
Equipment
 ↓
object
```

---

# 21. `super()` aur cooperative inheritance

Multiple inheritance mein best practice hoti hai ke participating classes:

```python
super().method()
```

use karein instead of directly parent ko call karna.

Good:

```python
super().start()
```

Potentially problematic:

```python
Parent.start(self)
```

Kyun?

Direct parent call MRO chain ko bypass kar sakta hai.

---

# 22. `super()` vs direct parent call

### Direct:

```python
Employee.__init__(self, name)
```

Ye specifically `Employee` ko call karta hai.

### `super()`:

```python
super().__init__(name)
```

Ye MRO follow karta hai.

Simple inheritance mein dono similar result de sakte hain.

Multiple inheritance mein difference critical ho sakta hai.

---

# 23. Final architecture

```text
Inheritance
     ↓
MRO
     ↓
Python classes ka search order
     ↓
super()
     ↓
MRO ke according next implementation
```

Example:

```text
       Equipment
       /       \
     HVAC     Electrical
       \       /
        BuildingSystem
```

Aise complex hierarchy mein direct parent calls ke bajaye cooperative `super()` chain MRO ko follow kar sakti hai.

---

# 24. Golden rules

```text
1. MRO = Method Resolution Order

2. Class.mro() se exact order dekh sakte ho.

3. super() ka matlab simply "parent" nahi hai.

4. super() MRO mein current class ke baad next implementation
   ko search karta hai.

5. Multiple inheritance mein super() bohat important hai.

6. Direct Parent.method(self) MRO ko bypass kar sakta hai.

7. Cooperative inheritance mein classes super() chain continue karti hain.
```

### Mental model

```text
class D(B, C)

MRO:

D
↓
B
↓
C
↓
A
↓
object

D.super() → B
B.super() → C
C.super() → A
A.super() → object
```

**Next Lesson 35:** Python ka **Method Resolution Order (C3 Linearization) deeply** — `D(B, C)` ka MRO Python mathematically kaise calculate karta hai, aur **MRO conflict** kab aur kyun hota hai.

# Lesson 35: MRO aur C3 Linearization

Ab hum previous lesson ke **MRO** ko deeper level par samjhenge.

Sab se pehle simple rule:

> **MRO woh order hai jisme Python classes ko search karta hai.**

Multiple inheritance mein Python **C3 Linearization** use karta hai taake ek consistent MRO ban sake.

---

## 1. Simple inheritance

```python
class A:
    pass

class B(A):
    pass
```

MRO:

```text
B
↓
A
↓
object
```

```python
print(B.mro())
```

Conceptually:

```text
[B, A, object]
```

Simple case easy hai.

---

# 2. Multiple inheritance

```python
class A:
    pass

class B:
    pass

class C(B, A):
    pass
```

MRO:

```text
C
↓
B
↓
A
↓
object
```

Yahan parent order:

```python
class C(B, A)
```

important hai.

Python normally `B` ko `A` se pehle rakhega.

---

# 3. Diamond inheritance

Ab famous example:

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

Structure:

```text
       A
      / \
     B   C
      \ /
       D
```

MRO:

```text
D
B
C
A
object
```

Yani:

```python
print(D.mro())
```

conceptually:

```text
[D, B, C, A, object]
```

---

# 4. Sawal: `A` ko B aur C ke baad kyun rakha?

Kyunkay Python ko ye dono relationships maintain karne hain:

```text
D → B → A
```

aur:

```text
D → C → A
```

Saath hi:

```text
B → C
```

ya

```text
C → B
```

jaisi arbitrary ordering nahi banani.

C3 ek **consistent linear order** produce karta hai.

---

# 5. C3 ka basic idea

C3 ko abhi mathematical formula ke baghair samjho.

Python inheritance tree ko ek single ordered list mein convert karta hai:

```text
Inheritance graph
       ↓
C3 Linearization
       ↓
MRO list
```

Example:

```text
       A
      / \
     B   C
      \ /
       D
```

becomes:

```text
D → B → C → A → object
```

---

# 6. Sabse important C3 rules

C3 MRO ko banate waqt generally ye properties maintain karta hai:

### Rule 1 — Child pehle

```text
D
↓
parents
```

Isliye `D` apne parents se pehle aata hai.

---

### Rule 2 — Parent order preserve karo

Agar likha:

```python
class D(B, C):
```

to:

```text
B → C
```

order preserve hona chahiye.

Python normally ise reverse nahi karega:

```text
C → B
```

---

### Rule 3 — Existing inheritance order preserve karo

Agar:

```python
class B(A):
```

to B ke MRO mein:

```text
B → A
```

hona chahiye.

Python kisi derived class ka established parent order randomly break nahi karta.

---

# 7. C3 ko ek practical example se samjho

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

Pehle:

```text
B ka MRO:
B → A → object
```

Aur:

```text
C ka MRO:
C → A → object
```

Ab D:

```text
D(B, C)
```

ko dono inheritance chains ko combine karna hai.

Result:

```text
D → B → C → A → object
```

---

# 8. `A` ko pehle kyun nahi rakh sakte?

Agar Python ye karta:

```text
D → A → B → C
```

to B ki inheritance relationship:

```text
B → A
```

ka expected order break ho jata.

B ke MRO mein B ko A se pehle hona chahiye.

Isliye:

```text
B → A
```

preserve hota hai.

---

# 9. Parent order ka example

```python
class A:
    pass

class B:
    pass

class C(A, B):
    pass
```

MRO:

```text
C
↓
A
↓
B
↓
object
```

Agar:

```python
class C(B, A):
    pass
```

to MRO generally:

```text
C
↓
B
↓
A
↓
object
```

Parent declaration order matter karta hai.

---

# 10. MRO conflict

Ab important part.

Har multiple inheritance hierarchy ka valid MRO zaroori nahi hota.

Example:

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

Valid:

```text
D → B → C → A → object
```

Lekin agar inheritance constraints contradictory ho jayein, Python class creation par error de sakta hai.

---

# 11. Classic MRO conflict

Example:

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class X(B, C):
    pass

class Y(C, B):
    pass

class Z(X, Y):
    pass
```

Yahan problem:

`X` require karta hai:

```text
B → C
```

Lekin `Y` require karta hai:

```text
C → B
```

Ab `Z` ko dono conditions simultaneously satisfy karni hain:

```text
B before C
```

aur:

```text
C before B
```

Impossible.

Python class create karte waqt MRO conflict report karega.

---

# 12. Isko diagram se dekho

```text
       B       C
       ↓       ↓
       X       Y
      /         \
   B before C   C before B
        \       /
           Z
```

`Z` ke liye requirements:

```text
B < C
```

aur:

```text
C < B
```

Dono simultaneously true nahi ho sakte.

Isliye valid MRO nahi ban sakta.

---

# 13. Error kab aata hai?

Important:

Ye runtime method call ka error nahi.

Class definition ke waqt hi:

```python
class Z(X, Y):
    pass
```

Python MRO calculate karega.

Agar consistent MRO nahi ban sakta:

```text
TypeError
Cannot create a consistent method resolution order
```

type ka error mil sakta hai.

---

# 14. MRO inspect karne ke tools

Sabse useful:

```python
Class.mro()
```

Example:

```python
print(D.mro())
```

Ya:

```python
print(D.__mro__)
```

### `mro()`

List deta hai.

### `__mro__`

Tuple deta hai.

Conceptually:

```python
D.mro()
```

```text
[D, B, C, A, object]
```

aur:

```python
D.__mro__
```

```text
(D, B, C, A, object)
```

---

# 15. `super()` ka connection

Ab previous lesson ka `super()` aur C3 connect karo.

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
```

MRO:

```text
D
↓
B
↓
C
↓
A
↓
object
```

Call:

```python
D().show()
```

Flow:

```text
D.show()
   ↓
super()
   ↓
B.show()
   ↓
super()
   ↓
C.show()
   ↓
super()
   ↓
A.show()
```

Output:

```text
D
B
C
A
```

---

# 16. Yahan `super()` ka real meaning

B ke andar:

```python
super().show()
```

ka matlab:

> "B ke parent ko directly call karo"

**nahi.**

Actual idea:

> "MRO mein B ke baad `show()` ki next implementation find karo."

B ke MRO context mein next:

```text
C
```

hai.

Isliye B se:

```text
B → C
```

hota hai.

---

# 17. Direct parent call kyun dangerous ho sakta hai?

Agar B mein:

```python
A.show(self)
```

likh diya:

```python
class B(A):
    def show(self):
        print("B")
        A.show(self)
```

to B direct A par jump karega.

Multiple inheritance mein C bypass ho sakta hai.

```text
D
↓
B
↓
A
```

instead of cooperative:

```text
D
↓
B
↓
C
↓
A
```

Isliye cooperative multiple inheritance mein:

```python
super()
```

important hai.

---

# 18. `super()` + `__init__`

Multiple inheritance mein ye pattern common hai:

```python
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()
```

MRO:

```text
D → B → C → A → object
```

So:

```python
D()
```

Output:

```text
D
B
C
A
```

---

# 19. Is pattern ko cooperative inheritance kehte hain

Har class:

```python
super().__init__()
```

call karti hai.

Result:

```text
D
 ↓
B
 ↓
C
 ↓
A
```

Har class apni responsibility perform karti hai aur chain ko continue karti hai.

---

# 20. Practical HVAC example

Suppose:

```text
Equipment
   ↑
   ├── HVAC
   │
   └── NetworkDevice
```

Aur ek device dono categories ka hai:

```python
class Equipment:
    def start(self):
        print("Equipment started")

class HVAC(Equipment):
    def start(self):
        print("HVAC system")
        super().start()

class NetworkDevice(Equipment):
    def start(self):
        print("Network connection")
        super().start()

class SmartAHU(HVAC, NetworkDevice):
    def start(self):
        print("Smart AHU")
        super().start()
```

MRO:

```text
SmartAHU
↓
HVAC
↓
NetworkDevice
↓
Equipment
↓
object
```

`SmartAHU().start()`:

```text
Smart AHU
HVAC system
Network connection
Equipment started
```

Ye cooperative multiple inheritance ka practical pattern hai.

---

# 21. C3 ko abhi kitna yaad rakhna hai?

Tumhe abhi mathematical implementation memorize karne ki zaroorat nahi.

Ye mental model enough hai:

```text
C3 Linearization
        ↓
consistent MRO banata hai
        ↓
child first
        ↓
parent declaration order preserve
        ↓
existing inheritance order preserve
        ↓
conflict ho to class creation fail
```

---

# 22. Most important distinction

### MRO

```text
Python classes ko kis order mein search karega?
```

### `super()`

```text
MRO ke according next implementation ko kaise access karna hai?
```

### C3 Linearization

```text
MRO ko calculate karne ka algorithm.
```

---

## Final mental model

```text
Multiple Inheritance
        ↓
   C3 Linearization
        ↓
       MRO
        ↓
D → B → C → A → object
        ↓
     super()
        ↓
MRO mein next implementation
```

### Ek line mein:

> **C3 Linearization inheritance hierarchy ko ek consistent MRO mein convert karta hai; `super()` us MRO ko follow karte hue next implementation tak pohanchta hai.**

**Next Lesson 36:** **Protocols & Structural Typing (`typing.Protocol`)** — Python mein inheritance ke baghair “interface” kaise define hota hai, `Protocol` aur ABC mein kya difference hai, aur ye tumhare pehle wale `Protocol` wale question se kaise connect hota hai.

# Lesson 36: `Protocol` aur Structural Typing

Ab hum Python typing ka ek important advanced concept samjhenge:

> **`Protocol` inheritance ke baghair interface-like behavior define karta hai.**

Ye tumhare pehle wale question **“Protocol as interface kaam karta hai?”** ka deeper answer hai.

---

## 1. Traditional inheritance interface

Suppose hum kehte hain har equipment ke paas `start()` hona chahiye:

```python
from abc import ABC, abstractmethod

class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass
```

Ab:

```python
class AHU(Equipment):

    def start(self):
        print("AHU started")
```

`AHU` explicitly `Equipment` se inherit kar raha hai.

```text
AHU
 ↓
Equipment
```

Ye **nominal typing** style hai:

> Relationship explicitly declare ki gayi hai.

---

# 2. `Protocol` mein inheritance zaroori nahi

Ab:

```python
from typing import Protocol

class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab koi class:

```python
class AHU:

    def start(self) -> None:
        print("AHU started")
```

Notice:

```python
class AHU:
```

ne:

```python
Startable
```

se inherit nahi kiya.

Phir bhi static type checker ke liye `AHU` `Startable` protocol satisfy kar sakta hai, kyun ke uske paas required:

```python
start()
```

method hai.

---

# 3. Ye Structural Typing hai

Is concept ka naam:

> **Structural Typing**

Meaning:

> Object ki identity/parentage se zyada uski **structure/capabilities** dekhi jati hain.

Simple mental model:

```text
Nominal typing:

AHU → Equipment
      ↓
explicit relationship


Structural typing:

AHU
 ↓
has start()
 ↓
matches Startable
```

---

# 4. Duck typing se connection

Python mein famous idea:

> **If it walks like a duck and quacks like a duck, treat it like a duck.**

Example:

```python
class AHU:

    def start(self):
        print("AHU started")


class Pump:

    def start(self):
        print("Pump started")
```

Function:

```python
def start_equipment(equipment):
    equipment.start()
```

Dono work karenge:

```python
start_equipment(AHU())
start_equipment(Pump())
```

Kyun?

Function ko ye matter nahi karta ke object kis class se bana hai.

Usko sirf chahiye:

```text
start()
```

---

# 5. `Protocol` duck typing ko static typing deta hai

Without Protocol:

```python
def start_equipment(equipment):
    equipment.start()
```

Runtime par Python simply method call karega.

Protocol ke saath:

```python
from typing import Protocol

class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab type checker ko explicitly bata rahe ho:

> Jo object `start()` provide karta hai, woh `Startable` interface ko satisfy karta hai.

---

# 6. Practical example

```python
from typing import Protocol


class Startable(Protocol):

    def start(self) -> None:
        ...


class AHU:

    def start(self) -> None:
        print("AHU started")


class Pump:

    def start(self) -> None:
        print("Pump started")


def start_equipment(equipment: Startable) -> None:
    equipment.start()
```

Use:

```python
start_equipment(AHU())
start_equipment(Pump())
```

Output:

```text
AHU started
Pump started
```

---

# 7. AHU ne Protocol inherit nahi kiya

Ye important hai:

```python
class AHU:
```

not:

```python
class AHU(Startable):
```

Phir bhi static type checker structural compatibility recognize kar sakta hai.

Yahi `Protocol` ki major power hai.

---

# 8. ABC vs Protocol

| Feature                                     | ABC                                 | Protocol                  |
| ------------------------------------------- | ----------------------------------- | ------------------------- |
| Explicit inheritance                        | Usually yes                         | Zaroori nahi              |
| Main idea                                   | Nominal abstraction                 | Structural abstraction    |
| Runtime enforcement                         | Possible                            | Primarily static typing   |
| Duck typing style                           | Less direct                         | Very natural              |
| Existing unrelated class adapt ho sakti hai | Usually explicit inheritance needed | Yes, if structure matches |
| Interface-like design                       | Yes                                 | Yes                       |

---

# 9. ABC example

```python
from abc import ABC, abstractmethod

class Startable(ABC):

    @abstractmethod
    def start(self):
        pass
```

Class:

```python
class AHU(Startable):

    def start(self):
        print("AHU")
```

Explicit relationship:

```text
AHU
 ↓
Startable
```

---

# 10. Protocol example

```python
from typing import Protocol

class Startable(Protocol):

    def start(self) -> None:
        ...
```

Class:

```python
class AHU:

    def start(self):
        print("AHU")
```

Relationship:

```text
AHU
 │
 ├── start()
 │
 └── structurally matches Startable
```

No inheritance required.

---

# 11. `...` ka kya matlab hai?

Protocol mein:

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

`...` yani Ellipsis yahan implementation provide nahi kar raha.

Ye basically specification/interface batata hai:

```text
Required:
start() → None
```

Protocol ka focus:

> **What should be available?**

not:

> **How should it be implemented?**

---

# 12. Multiple methods

Protocol sirf ek method ke liye nahi.

```python
from typing import Protocol

class EquipmentProtocol(Protocol):

    equipment_id: str

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def status(self) -> str:
        ...
```

Ab compatible class mein ye sab hona chahiye:

```python
class AHU:

    def __init__(self):
        self.equipment_id = "AHU-01"

    def start(self):
        print("Starting")

    def stop(self):
        print("Stopping")

    def status(self):
        return "Running"
```

Structure match ho raha hai.

---

# 13. Protocol attribute bhi define kar sakta hai

Example:

```python
class Sensor(Protocol):

    temperature: float

    def read(self) -> float:
        ...
```

Ab compatible object ke paas:

```text
temperature
read()
```

hona chahiye.

---

# 14. Read-only property Protocol mein

Agar interface property expect karta hai:

```python
from typing import Protocol

class TemperatureSensor(Protocol):

    @property
    def temperature(self) -> float:
        ...
```

Ab class:

```python
class AHUSensor:

    @property
    def temperature(self) -> float:
        return 22.5
```

structurally compatible ho sakti hai.

---

# 15. Protocol inheritance

Protocols ek doosre se inherit bhi kar sakte hain.

```python
class Startable(Protocol):

    def start(self) -> None:
        ...


class Stoppable(Protocol):

    def stop(self) -> None:
        ...


class Controllable(Startable, Stoppable, Protocol):

    def reset(self) -> None:
        ...
```

Ab `Controllable` require karta hai:

```text
start()
stop()
reset()
```

---

# 16. Protocol ka real-world advantage

Suppose tumhare paas external library ki class hai:

```python
class ExternalDevice:

    def start(self):
        print("Started")
```

Tum us class ko modify nahi kar sakte.

Aur na hi:

```python
class ExternalDevice(Startable):
```

kar sakte ho.

Protocol ke saath:

```python
class Startable(Protocol):

    def start(self):
        ...
```

Function:

```python
def run(device: Startable):
    device.start()
```

ExternalDevice ko directly use kar sakte ho, provided uska structure compatible ho.

---

# 17. Isi liye Protocol loose coupling deta hai

Traditional:

```text
Function
   ↓
specific parent class
   ↓
Equipment
```

Protocol:

```text
Function
   ↓
required interface
   ↓
start()
```

Function ko concrete class ki dependency kam ho jati hai.

Isko software architecture mein **loose coupling** ke context mein use kiya jata hai.

---

# 18. Protocol + polymorphism

Ye dono naturally connect hote hain.

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Multiple classes:

```python
class AHU:

    def start(self):
        print("AHU")


class Pump:

    def start(self):
        print("Pump")


class Chiller:

    def start(self):
        print("Chiller")
```

Function:

```python
def start(device: Startable):
    device.start()
```

Ab:

```python
start(AHU())
start(Pump())
start(Chiller())
```

Same interface:

```text
start()
```

Different behavior:

```text
AHU
Pump
Chiller
```

Ye **polymorphism** hai.

---

# 19. Runtime `isinstance()` ka special case

Normally:

```python
class Startable(Protocol):
    def start(self):
        ...
```

ke saath:

```python
isinstance(AHU(), Startable)
```

directly runtime structural check ke liye generally allowed nahi hota.

Agar runtime check chahiye:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab:

```python
print(isinstance(AHU(), Startable))
```

`True` ho sakta hai agar required runtime structure satisfy ho.

---

# 20. Important limitation

`@runtime_checkable` ko full static type validation samajhna galat hoga.

Runtime check primarily ye dekh sakta hai ke required attributes/method names available hain.

Ye static type checker ki tarah har detail verify nahi karta.

For example, method ke exact type annotations ka complete static compatibility check runtime `isinstance()` ka kaam nahi hai.

---

# 21. `Protocol` vs `ABC` kab?

### ABC

Use karna natural hai jab:

```text
strong conceptual hierarchy
shared implementation
controlled inheritance
```

Example:

```text
Equipment
├── AHU
├── VAV
└── Chiller
```

### Protocol

Use karna natural hai jab:

```text
different/unrelated classes
same capability
loose coupling
external classes
structural typing
```

Example:

```text
AHU      → start()
Pump     → start()
Chiller  → start()
```

Inka inheritance relationship hona zaroori nahi.

---

# 22. Tumhare `typing` wale concepts se connection

Tumne pehle poocha tha:

```python
from typing import (
    Any,
    Dict,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Union
)
```

Ab `Protocol` ko complete context mein dekho:

```text
Any
→ kuch bhi

Union
→ multiple possible types

Optional
→ T ya None

TypeVar
→ generic type placeholder

Protocol
→ required structure / interface

TypedDict
→ dictionary ki expected structure
```

Protocol ka core idea:

```text
"Object kis class ka hai?"
        ↓
kam important

"Object kya methods/attributes provide karta hai?"
        ↓
important
```

---

# 23. Final mental model

```text
ABC
↓
"Is class ko meri hierarchy ka member bano."

Protocol
↓
"Bas required interface provide karo."

Duck Typing
↓
"Jo required behavior provide karta hai, use kar lo."

Structural Typing
↓
"Structure/capability match ho to type compatible."
```

### Ek line mein:

> **`Protocol` Python mein interface-like contract define karta hai jise classes bina explicit inheritance ke bhi satisfy kar sakti hain; isi ko structural typing kehte hain.**

**Next Lesson 37:** `Generic`, `TypeVar` aur `Protocol` ko combine karna — yani reusable **type-safe generic interfaces**, jaise `Repository[T]`, `Storage[T]`, aur HVAC equipment ke generic providers.

# Lesson 37: `Generic` + `TypeVar` + `Protocol`

Ab hum 3 concepts ko **ek saath** samjhenge:

```text
TypeVar
   ↓
Generic
   ↓
Protocol
   ↓
Reusable type-safe design
```

Ye Python typing ka kaafi important advanced part hai.

---

## 1. Pehle `TypeVar` yaad karo

Tumne pehle padha tha:

```python
from typing import TypeVar

T = TypeVar("T")
```

`T` ka matlab:

> "Yahan koi bhi type aa sakti hai, lekin jo type aayegi usko preserve karo."

Example:

```python
def first(items: list[T]) -> T:
    return items[0]
```

Agar:

```python
names = ["Ali", "Ahmed", "Usman"]

result = first(names)
```

to type:

```text
list[str]
   ↓
T = str
   ↓
result = str
```

Agar:

```python
numbers = [10, 20, 30]

result = first(numbers)
```

to:

```text
T = int
```

---

# 2. Problem: reusable class

Suppose humein storage banana hai.

```python
class Storage:
    def __init__(self):
        self.data = None

    def set(self, value):
        self.data = value

    def get(self):
        return self.data
```

Problem:

`get()` se kya type return hoga?

```text
str?
int?
AHU?
Sensor?
Employee?
```

Python ko clearly pata nahi.

---

# 3. Generic class

Ab:

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

Ab hum specify kar sakte hain:

```python
Storage[str]
```

ya:

```python
Storage[int]
```

---

# 4. `Storage[str]`

```python
name_storage = Storage[str]()
```

Conceptually:

```text
Storage[T]

T = str

Storage[str]
```

Ab:

```python
name_storage.set("Muhammad")
```

valid.

Aur:

```python
name = name_storage.get()
```

type checker samjhega:

```text
name → str | None
```

---

# 5. `Storage[int]`

```python
salary_storage = Storage[int]()
```

Ab:

```python
salary_storage.set(5000)
```

valid.

Lekin:

```python
salary_storage.set("5000")
```

static type checker isko incorrect report kar sakta hai.

---

# 6. `Generic[T]` ka actual role

Ye:

```python
class Storage(Generic[T]):
```

ka matlab:

> Storage class khud generic hai aur `T` ko carry karegi.

Diagram:

```text
Storage[T]
    │
    ├── Storage[str]
    │
    ├── Storage[int]
    │
    └── Storage[AHU]
```

Same class.

Different type.

---

# 7. Ab `Protocol` add karte hain

Suppose hum kehte hain:

> Humein aisa object chahiye jisme `get()` aur `set()` ho.

```python
from typing import Protocol, TypeVar

T = TypeVar("T")


class Repository(Protocol[T]):

    def get(self) -> T:
        ...

    def set(self, value: T) -> None:
        ...
```

Ab `Repository` ek **generic protocol** hai.

---

# 8. Generic Protocol ka matlab

```python
Repository[T]
```

mein `T` change ho sakta hai:

```text
Repository[str]
Repository[int]
Repository[Employee]
Repository[AHU]
```

Aur interface same rahega:

```text
get()
set()
```

---

# 9. Concrete class ko inherit karna zaroori nahi

```python
class MemoryRepository:

    def __init__(self):
        self.data = None

    def get(self):
        return self.data

    def set(self, value):
        self.data = value
```

Notice:

```python
class MemoryRepository:
```

ne:

```python
Repository
```

se inherit nahi kiya.

Phir bhi structure match karta hai:

```text
MemoryRepository
│
├── get()
└── set()

Repository
│
├── get()
└── set()
```

Ye **structural typing** hai.

---

# 10. Real example: HVAC

Ab ek useful example.

Humein ek generic sensor reader banana hai.

```python
from typing import Protocol, TypeVar

T = TypeVar("T")


class Sensor(Protocol[T]):

    def read(self) -> T:
        ...
```

Ab temperature sensor:

```python
class TemperatureSensor:

    def read(self) -> float:
        return 22.5
```

Aur status sensor:

```python
class StatusSensor:

    def read(self) -> str:
        return "Running"
```

Dono same protocol ko structurally satisfy kar sakte hain.

---

# 11. Generic function

```python
def read_sensor(sensor: Sensor[T]) -> T:
    return sensor.read()
```

Ab:

```python
temperature = read_sensor(TemperatureSensor())
```

Type:

```text
float
```

Aur:

```python
status = read_sensor(StatusSensor())
```

Type:

```text
str
```

Yahan `T` automatically different ho gaya.

---

# 12. Flow dekho

Temperature:

```text
TemperatureSensor
       ↓
read() → float
       ↓
T = float
       ↓
read_sensor()
       ↓
float
```

Status:

```text
StatusSensor
       ↓
read() → str
       ↓
T = str
       ↓
read_sensor()
       ↓
str
```

Yahi generic typing ki power hai.

---

# 13. `Generic` vs `Protocol`

Dono same cheez nahi hain.

### `Generic`

Batata hai:

> Class/function kis type ke saath reusable hai?

Example:

```python
class Box(Generic[T]):
```

### `Protocol`

Batata hai:

> Object mein kya capabilities honi chahiye?

Example:

```python
class Readable(Protocol):
    def read(self):
        ...
```

---

# 14. Dono combine karne ka reason

Suppose:

```python
class Repository(Protocol[T]):

    def get(self) -> T:
        ...

    def save(self, value: T) -> None:
        ...
```

Yahan:

```text
Protocol
↓
required behavior

T
↓
required data type
```

Isliye:

```text
Repository[str]
Repository[int]
Repository[AHU]
```

sab possible hain.

---

# 15. Generic Repository example

```python
from typing import Protocol, TypeVar

T = TypeVar("T")


class Repository(Protocol[T]):

    def get(self, id: int) -> T:
        ...

    def save(self, item: T) -> None:
        ...
```

Ab:

```python
class Employee:
    def __init__(self, name):
        self.name = name
```

Aur:

```python
class EmployeeRepository:

    def get(self, id: int) -> Employee:
        return Employee("Ali")

    def save(self, item: Employee) -> None:
        print("Employee saved")
```

Conceptually:

```text
EmployeeRepository
        ↓
Repository[Employee]
```

without explicit inheritance.

---

# 16. Ye large projects mein useful kyun hai?

Suppose tumhara application database use karta hai.

Aaj:

```text
MySQLRepository
```

kal:

```text
GoogleSheetsRepository
```

parson:

```text
APIRepository
```

Agar sab mein same interface hai:

```text
get()
save()
delete()
```

to application ko implementation ki details se kam concern hoga.

```text
Application
     ↓
Repository[T]
     ↑
     │
 ┌───┼───────────────┐
 │   │               │
SQL Google Sheets   API
```

Ye **loose coupling** hai.

---

# 17. `T` ko simple tareeqe se yaad rakho

```python
T = TypeVar("T")
```

ko initially is tarah socho:

> **T = jo type tum baad mein decide karoge.**

Example:

```python
Box[str]
```

means:

```text
T = str
```

Aur:

```python
Box[int]
```

means:

```text
T = int
```

---

# 18. `Generic[T]` ka mental model

```python
class Box(Generic[T]):
```

matlab:

```text
Box ek template hai
       ↓
T placeholder hai
       ↓
Box[str]
Box[int]
Box[float]
```

Ye C++/Java ke generics ke concept se related hai.

---

# 19. `Protocol[T]` ka mental model

```python
class Reader(Protocol[T]):
    def read(self) -> T:
        ...
```

matlab:

```text
Reader[T]
   │
   ├── required behavior: read()
   │
   └── output type: T
```

So:

```text
Reader[float]
→ read() returns float

Reader[str]
→ read() returns str
```

---

# 20. Tumhare HVAC project mein iska use

Imagine BMS mein multiple point readers:

```python
class PointReader(Protocol[T]):

    def read(self, point_name: str) -> T:
        ...
```

Temperature:

```python
class TemperatureReader:

    def read(self, point_name: str) -> float:
        return 22.4
```

Status:

```python
class StatusReader:

    def read(self, point_name: str) -> str:
        return "ON"
```

Boolean:

```python
class AlarmReader:

    def read(self, point_name: str) -> bool:
        return False
```

Same conceptual interface:

```text
read(point_name)
```

Different data:

```text
float
str
bool
```

---

# 21. Ek important distinction

Ye:

```python
class PointReader(Protocol[T]):
```

**runtime object create karne ke liye normal class nahi hai.**

Usually tum:

```python
reader = PointReader()
```

nahi karoge.

Protocol ka purpose contract/type interface define karna hai.

Actual implementation:

```python
class TemperatureReader:
    ...
```

provide karegi.

---

# 22. Aaj ka complete mental model

```text
TypeVar
   ↓
T = type placeholder

Generic
   ↓
class/function ko reusable type-aware banata hai

Protocol
   ↓
required structure/interface define karta hai

Generic + Protocol
   ↓
reusable + structural + type-safe interface
```

Example:

```python
T = TypeVar("T")

class Reader(Protocol[T]):

    def read(self) -> T:
        ...
```

Iska matlab:

> **"Mujhe aisa object do jo `read()` provide karta ho, aur jo type read karega woh T hoga."**

---

### Next: Lesson 38

Agla important topic hoga:

**`Callable` + generic types + `ParamSpec`**

Ismein hum dekhenge ke Python mein **function ko bhi type ke taur par kaise describe karte hain**, aur decorators mein `*args/**kwargs` ki exact typing kaise hoti hai.

# Lesson 38: `Callable` + `ParamSpec` + Generic Functions

Ab hum Python typing ka ek important advanced topic karte hain:

```text
Callable
   ↓
function ka type describe karta hai

ParamSpec
   ↓
function ke parameters ko preserve karta hai

TypeVar
   ↓
input/output types ko preserve karta hai
```

Ye specially **decorators** aur higher-order functions mein bohat useful hai.

---

## 1. `Callable` kya hai?

Tumne pehle `Callable` ka naam dekha tha.

Simple meaning:

> **`Callable` kisi callable object/function ka type describe karta hai.**

Example:

```python
from collections.abc import Callable
```

Ab:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Is function ka conceptual type:

```text
Callable[[int, int], int]
```

Meaning:

```text
Callable[
    [input types],
    output type
]
```

So:

```python
Callable[[int, int], int]
```

ka matlab:

> Aisa callable jo 2 `int` inputs leta hai aur `int` return karta hai.

---

# 2. Basic example

```python
from collections.abc import Callable

def execute(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return func(a, b)
```

Function:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Use:

```python
result = execute(add, 10, 20)
```

Output:

```text
30
```

Yahan:

```text
add
 ↓
(int, int) → int
```

isliye `Callable[[int, int], int]` match karta hai.

---

# 3. `Callable` ko function ke box ki tarah samjho

```text
Callable
   │
   ├── inputs
   │     ├── int
   │     └── int
   │
   └── output
         ↓
        int
```

Example:

```python
Callable[[str], int]
```

means:

```text
str input
   ↓
function
   ↓
int output
```

---

# 4. Different examples

### No arguments

```python
Callable[[], str]
```

Meaning:

```text
()
 ↓
str
```

Example:

```python
def get_status() -> str:
    return "Running"
```

---

### One argument

```python
Callable[[str], int]
```

Example:

```python
def get_length(text: str) -> int:
    return len(text)
```

---

### Multiple arguments

```python
Callable[[str, int], bool]
```

Example:

```python
def check_name(name: str, minimum: int) -> bool:
    return len(name) >= minimum
```

---

# 5. Problem with decorators

Ab decorator ka example dekho:

```python
def logger(func):

    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result

    return wrapper
```

Runtime par ye perfectly kaam karta hai.

Lekin type checker ke liye problem hai:

```python
*args
**kwargs
```

ki exact types kya hain?

Agar original function:

```python
def add(a: int, b: int) -> int:
```

hai to wrapper ko ideally ye information preserve karni chahiye:

```text
(int, int) → int
```

Yahan **ParamSpec** ka role aata hai.

---

# 6. `ParamSpec`

```python
from typing import ParamSpec
```

Phir:

```python
P = ParamSpec("P")
```

`P` ka matlab:

> **Function ke complete parameter specification ko capture karo.**

Ye `TypeVar` se different hai.

---

# 7. `TypeVar` vs `ParamSpec`

### `TypeVar`

Type represent karta hai:

```python
T = TypeVar("T")
```

Example:

```python
def identity(value: T) -> T:
    return value
```

Yahan:

```text
T = input/output type
```

---

### `ParamSpec`

Function ke **parameters ka complete signature** represent karta hai:

```python
P = ParamSpec("P")
```

Yani:

```text
P = (a: int, b: int)
```

ya:

```text
P = (name: str, age: int)
```

ya:

```text
P = (*args, **kwargs)
```

ka type-level representation.

---

# 8. Decorator ko properly type karna

Modern Python mein:

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")
```

Decorator:

```python
def logger(
    func: Callable[P, R]
) -> Callable[P, R]:

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Before")

        result = func(*args, **kwargs)

        print("After")

        return result

    return wrapper
```

Ye advanced decorator typing hai.

---

# 9. Isko line by line samjho

Sabse important line:

```python
func: Callable[P, R]
```

Meaning:

> `func` koi bhi callable hai jiske parameters `P` hain aur return type `R` hai.

Then:

```python
wrapper(
    *args: P.args,
    **kwargs: P.kwargs
)
```

Meaning:

> Original function ke parameters exactly preserve karo.

And:

```python
-> R
```

Meaning:

> Wrapper bhi wahi return type preserve karega.

---

# 10. Example

Original:

```python
@logger
def add(a: int, b: int) -> int:
    return a + b
```

Type information:

```text
Original:

(int, int) → int
```

Decorator ke baad:

```text
wrapper:

(int, int) → int
```

So decorator ne function ke signature ko conceptually preserve kiya.

---

# 11. Another example

```python
@logger
def greet(name: str, age: int) -> str:
    return f"{name}: {age}"
```

Original:

```text
(str, int) → str
```

Decorator ke baad bhi:

```text
(str, int) → str
```

`P` capture karta hai:

```text
P = (str, int)
```

Aur:

```text
R = str
```

---

# 12. `P.args` aur `P.kwargs`

Ye bohat important hai.

```python
*args: P.args
```

means:

> Original positional parameters preserve karo.

Aur:

```python
**kwargs: P.kwargs
```

means:

> Original keyword parameters preserve karo.

Example original:

```python
def equipment(
    equipment_id: str,
    temperature: float,
    mode: str
):
    ...
```

Decorator ke andar:

```python
*args: P.args
**kwargs: P.kwargs
```

original function ka parameter structure represent karega.

---

# 13. `ParamSpec` ki zaroorat kyun?

Without `ParamSpec`, tum kuch aisa likh sakte ho:

```python
def logger(func: Callable[..., R]) -> Callable[..., R]:
    ...
```

`...` ka matlab roughly:

> parameters ke exact types specify nahi kiye.

Ye less precise hai.

```python
Callable[..., R]
```

versus:

```python
Callable[P, R]
```

Difference:

```text
... 
↓
parameters unknown / unspecified

P
↓
parameters preserve karo
```

---

# 14. HVAC example

Suppose:

```python
def set_temperature(
    equipment_id: str,
    temperature: float
) -> bool:
    print(equipment_id, temperature)
    return True
```

Decorator:

```python
@logger
def set_temperature(
    equipment_id: str,
    temperature: float
) -> bool:
    ...
```

Conceptually:

```text
P
↓
(str, float)

R
↓
bool
```

Therefore:

```text
Callable[P, R]
```

becomes:

```text
Callable[[str, float], bool]
```

---

# 15. `TypeVar` + `ParamSpec`

Dono ka difference ek example se:

```python
T = TypeVar("T")
P = ParamSpec("P")
```

### `T`

```text
"What type?"
```

### `P`

```text
"What parameters?"
```

### `R`

```text
"What return type?"
```

Together:

```text
P → parameters
R → return
```

Decorator:

```python
Callable[P, R]
```

---

# 16. Function transformation ka mental model

Decorator ko is tarah dekho:

```text
Original function

P → function → R
        │
        │ decorator
        ↓
Wrapper

P → wrapper → R
```

Decorator original parameters aur return type ko preserve kar raha hai.

---

# 17. `Callable` sirf normal functions ke liye nahi

Ye callable objects ke liye bhi ho sakta hai.

Example:

```python
class Calculator:

    def __call__(self, a: int, b: int) -> int:
        return a + b
```

Object:

```python
calc = Calculator()
```

Ab:

```python
calc(10, 20)
```

callable hai.

So:

```python
callable(calc)
```

returns:

```text
True
```

`Callable` concept functions + callable objects dono cover kar sakta hai.

---

# 18. `Protocol` + `Callable`

Ab tumhare previous lesson ka connection dekho.

Agar tumhe callable object ka interface define karna ho:

```python
from typing import Protocol

class Command(Protocol):

    def __call__(self, equipment_id: str) -> bool:
        ...
```

Ab koi callable object jo:

```text
__call__(str) → bool
```

provide karta hai, structurally compatible ho sakta hai.

---

# 19. Three concepts together

Ab architecture:

```text
Protocol
   ↓
Required capability

Callable
   ↓
Function/callable ka shape

ParamSpec
   ↓
Parameters preserve

TypeVar
   ↓
Types preserve
```

---

# 20. Sabse important comparison

| Concept     | Kya represent karta hai?           |
| ----------- | ---------------------------------- |
| `TypeVar`   | Ek generic type                    |
| `ParamSpec` | Function ke parameters             |
| `Callable`  | Callable ka input/output shape     |
| `Protocol`  | Required structure/interface       |
| `Generic`   | Type-aware reusable class/function |

---

# 21. Ek practical decorator yaad rakho

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

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

Isko abhi memorize karne ki zaroorat nahi.

Bas ye architecture samjho:

```text
func
 ↓
Callable[P, R]
 ↓
P = parameters
R = return type
 ↓
wrapper
 ↓
Callable[P, R]
```

---

## Final mental model

```text
TypeVar
"T kya type hai?"

ParamSpec
"Function ke parameters kya hain?"

Callable
"Ye function kya inputs leta hai aur kya output deta hai?"

Protocol
"Object ko kaunsi capability provide karni hai?"

Generic
"Is design ko different types ke saath reusable banao."
```

### Next Lesson 39

**`TypeVar` ke bounds aur constraints**:

```python
T = TypeVar("T", bound=...)
```

vs

```python
T = TypeVar("T", int, float, str)
```

Aur hum dekhenge:

**`bound` vs `constraints` exactly kya difference hai, aur static type checker kis situation mein kya infer karta hai.**

# Lesson 39: `TypeVar` — `bound` vs `constraints`

Ab hum `TypeVar` ko deeper level par samjhenge. Ye important hai kyun ke:

```python
T = TypeVar("T")
```

ke ilawa tum ye bhi likh sakte ho:

```python
T = TypeVar("T", bound=...)
```

ya:

```python
T = TypeVar("T", int, float)
```

Dono ka purpose different hai.

---

## 1. Simple `TypeVar`

Pehle:

```python
from typing import TypeVar

T = TypeVar("T")
```

Yahan `T` basically unrestricted hai.

Example:

```python
def identity(value: T) -> T:
    return value
```

Agar:

```python
identity(10)
```

to:

```text
T = int
```

Agar:

```python
identity("Ali")
```

to:

```text
T = str
```

Yani:

```text
T = jo type input mein aayi
```

---

# 2. `bound` kya karta hai?

Syntax:

```python
T = TypeVar("T", bound=SomeType)
```

Meaning:

> `T` koi bhi type ho sakti hai, **lekin `SomeType` ya uski subclass honi chahiye.**

Important word:

> **upper bound**

---

# 3. Example: `Animal`

```python
class Animal:

    def speak(self):
        print("Animal sound")
```

Ab:

```python
T = TypeVar("T", bound=Animal)
```

Matlab:

```text
T
↓
Animal ya Animal ki subclass
```

Example:

```python
class Dog(Animal):
    pass


class Cat(Animal):
    pass
```

Ab:

```python
def get_animal(animal: T) -> T:
    return animal
```

Ye valid conceptually hai:

```python
dog = get_animal(Dog())
```

Type:

```text
Dog
```

Aur:

```python
cat = get_animal(Cat())
```

Type:

```text
Cat
```

---

# 4. Bound ka important benefit

Dekho:

```python
class Animal:

    def speak(self):
        print("Animal")


T = TypeVar("T", bound=Animal)


def make_sound(animal: T) -> T:
    animal.speak()
    return animal
```

Type checker ko pata hai:

```text
T <: Animal
```

Isliye:

```python
animal.speak()
```

allowed hai.

Kyun?

Kyun ke har valid `T` ke paas `Animal` ka interface available hona chahiye.

---

# 5. `T` exact subclass preserve karta hai

Ye important point hai.

```python
def identity(value: T) -> T:
    return value
```

Aur:

```python
dog = Dog()
result = identity(dog)
```

`result` ko type checker `Dog` ke taur par preserve kar sakta hai.

Bound ke saath bhi:

```python
T = TypeVar("T", bound=Animal)
```

to:

```text
Dog → T = Dog
Cat → T = Cat
```

Na ke har cheez ko simply `Animal` bana de.

---

# 6. Ab `constraints`

Syntax:

```python
T = TypeVar("T", int, float)
```

Iska meaning:

> `T` sirf specified types mein se ek ho sakti hai.

Yahan:

```text
T ∈ {int, float}
```

Example:

```python
T = TypeVar("T", int, float)

def double(value: T) -> T:
    return value * 2
```

Valid:

```python
double(10)
double(2.5)
```

Lekin:

```python
double("Ali")
```

type checker reject karega.

---

# 7. `bound` vs `constraints`

Sabse important comparison:

### Bound

```python
T = TypeVar("T", bound=Animal)
```

Meaning:

```text
Animal
├── Dog
├── Cat
├── Horse
└── ...
```

**Animal ya koi subclass.**

---

### Constraints

```python
T = TypeVar("T", int, float)
```

Meaning:

```text
sirf int
ya
float
```

Fixed choices.

---

# 8. Visual difference

### Bound

```text
          Animal
         /      \
       Dog      Cat
        \
       Puppy

T = Animal ya Dog ya Cat ya Puppy...
```

### Constraints

```text
T
├── int
└── float
```

No arbitrary subclasses outside the listed choices.

---

# 9. Real difference with subclasses

Ye subtle point important hai.

Suppose:

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass
```

With bound:

```python
T = TypeVar("T", bound=Animal)
```

`Dog`, `Cat`, etc. acceptable hain.

But constraints:

```python
T = TypeVar("T", Dog, Cat)
```

means:

```text
Dog
or
Cat
```

specifically constrained choices.

---

# 10. Constraint type inference

Suppose:

```python
T = TypeVar("T", int, float)

def get_value(value: T) -> T:
    return value
```

Agar:

```python
result = get_value(10)
```

then `int`.

Agar:

```python
result = get_value(10.5)
```

then `float`.

Lekin constraints ka behavior bound se different ho sakta hai jab subclasses involve hon.

Isliye constraints ko:

> **fixed allowed type categories**

samajhna useful hai.

---

# 11. Bound ka powerful example: `Comparable`

Suppose:

```python
from typing import TypeVar

T = TypeVar("T", bound="Comparable")
```

Conceptually hum keh rahe hain:

```text
T ko Comparable capability/type hierarchy ke andar hona chahiye.
```

Lekin Python typing mein interface-like behavior ke liye `Protocol` aksar zyada suitable hota hai.

Example:

```python
from typing import Protocol, TypeVar


class Comparable(Protocol):

    def __lt__(self, other) -> bool:
        ...
```

Then generic design can require that capability.

Ye `Protocol` ke saath `TypeVar` ka connection hai.

---

# 12. Bound + Protocol

Ab advanced combination:

```python
from typing import Protocol, TypeVar


class HasID(Protocol):

    id: int


T = TypeVar("T", bound=HasID)
```

Meaning:

> `T` aisa type hona chahiye jo `HasID` structure satisfy kare.

Example:

```python
class Employee:

    def __init__(self, id: int):
        self.id = id
```

Employee compatible ho sakta hai.

---

# 13. HVAC example

Suppose:

```python
class Equipment:

    def start(self):
        print("Started")
```

Subclasses:

```python
class AHU(Equipment):
    pass


class VAV(Equipment):
    pass
```

Generic function:

```python
T = TypeVar("T", bound=Equipment)


def start_equipment(equipment: T) -> T:
    equipment.start()
    return equipment
```

Ab:

```python
ahu = start_equipment(AHU())
```

Type:

```text
AHU
```

Aur:

```python
vav = start_equipment(VAV())
```

Type:

```text
VAV
```

Yahan `bound=Equipment` ensure karta hai ke `T` ke paas `Equipment` ka behavior available ho.

---

# 14. Ye simple `Equipment` annotation se different hai

Tum ye bhi kar sakte ho:

```python
def start_equipment(equipment: Equipment) -> Equipment:
    equipment.start()
    return equipment
```

Lekin phir return type generic subclass ko preserve nahi karta in the same way.

Generic version:

```python
def start_equipment(equipment: T) -> T:
```

means:

```text
Input:
AHU

Output:
AHU
```

not merely:

```text
Equipment
```

Ye **type preservation** hai.

---

# 15. `bound` ka mental model

```text
T = TypeVar("T", bound=Equipment)
```

ko read karo:

> "`T` koi bhi type ho sakti hai, bas `Equipment` ki boundary ke andar honi chahiye."

Diagram:

```text
T
↓
Equipment
├── AHU
├── VAV
├── Chiller
└── Pump
```

---

# 16. Constraints ka mental model

```python
T = TypeVar("T", int, float)
```

ko read karo:

> "`T` sirf in listed types mein se ek ho."

Diagram:

```text
T
├── int
└── float
```

---

# 17. `bound` vs `Union`

Ye bhi important comparison hai.

### Union

```python
def process(value: int | float):
    ...
```

Meaning:

> Function ko `int` ya `float` mil sakta hai.

### TypeVar

```python
T = TypeVar("T", int, float)

def process(value: T) -> T:
    return value
```

Meaning:

> Input type ko preserve karne ki generic relationship hai.

---

# 18. Example

```python
T = TypeVar("T", int, float)

def same(value: T) -> T:
    return value
```

Conceptually:

```text
same(10)
↓
int → int

same(2.5)
↓
float → float
```

Ye generic relationship hai.

---

# 19. `bound` vs `constraints` vs `Union`

| Concept                    | Meaning                         |
| -------------------------- | ------------------------------- |
| `T = TypeVar("T")`         | Any type, relationship preserve |
| `bound=Animal`             | Animal ya subclass              |
| `TypeVar("T", int, float)` | Listed type choices             |
| `int \| float`             | Value can be int or float       |

Sabse important difference:

```text
Union
→ allowed possibilities

TypeVar
→ type relationship

bound
→ TypeVar ki upper boundary

constraints
→ TypeVar ki fixed choices
```

---

# 20. Practical rule

Jab tumhare mind mein ye ho:

### "Koi bhi type"

```python
T = TypeVar("T")
```

### "Koi bhi subclass of X"

```python
T = TypeVar("T", bound=X)
```

### "Sirf ye specific types"

```python
T = TypeVar("T", int, float)
```

### "Value sirf in types mein se ho sakti hai"

```python
int | float
```

---

# 21. One complete example

```python
from typing import TypeVar


class Equipment:

    def start(self):
        print("Equipment started")


class AHU(Equipment):
    pass


class VAV(Equipment):
    pass


T = TypeVar("T", bound=Equipment)


def start_equipment(equipment: T) -> T:
    equipment.start()
    return equipment
```

Use:

```python
ahu = start_equipment(AHU())
vav = start_equipment(VAV())
```

Conceptually:

```text
AHU
 ↓
T = AHU
 ↓
AHU return


VAV
 ↓
T = VAV
 ↓
VAV return
```

Aur:

```python
start_equipment("hello")
```

type checker ke perspective se incorrect hai, kyun ke:

```text
str
 ↓
Equipment ki subclass nahi
```

---

## Final mental model

```text
TypeVar
   ↓
generic placeholder

TypeVar + bound
   ↓
placeholder with upper boundary

TypeVar + constraints
   ↓
placeholder with fixed allowed types

T + input/output
   ↓
type relationship preserve
```

### Ek line mein:

> **`bound` inheritance/capability ki boundary deta hai, jab ke `constraints` fixed allowed types ki list dete hain.**

### Next Lesson 40

Ab hum **`TypedDict` deeply** karenge:

```python
class EmployeeData(TypedDict):
    name: str
    salary: float
    department: str
```

Aur samjhenge **`TypedDict` vs `dict` vs `dataclass` vs normal class**, `Required`, `NotRequired`, `total=False`, aur nested `TypedDict`.

# Lesson 40: `TypedDict` — Deep Understanding

Ab hum `TypedDict` ko properly samjhenge, kyun ke ye tumhare **CSV, Google Sheets, API JSON aur work-order data** ke liye bohat useful hai.

---

## 1. `TypedDict` kya hai?

Simple definition:

> **`TypedDict` ek dictionary ki expected structure/type define karta hai.**

Example:

```python
from typing import TypedDict


class EmployeeData(TypedDict):
    name: str
    salary: float
    department: str
```

Ab expected dictionary:

```python
employee = {
    "name": "Ali",
    "salary": 5000.0,
    "department": "HVAC"
}
```

Conceptually:

```text
EmployeeData
│
├── name       → str
├── salary     → float
└── department → str
```

---

# 2. Ye normal `dict` se different kyun?

Normal:

```python
employee: dict = {
    "name": "Ali",
    "salary": 5000
}
```

Type checker ko exact structure ka pata nahi.

`TypedDict`:

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": 5000.0,
    "department": "HVAC"
}
```

Ab type checker ko pata hai:

```text
name       → str
salary     → float
department → str
```

---

# 3. Sabse important: Runtime par kya hai?

Ye point bohat important hai.

`TypedDict` **normal runtime dictionary ko special object nahi banata**.

Example:

```python
employee = EmployeeData(
    name="Ali",
    salary=5000.0,
    department="HVAC"
)
```

Runtime par ye basically dictionary hi hoti hai.

```python
print(type(employee))
```

conceptually:

```text
<class 'dict'>
```

Yani:

```text
TypedDict
   ↓
mainly static type checking
   ↓
runtime par normal dict
```

---

# 4. `TypedDict` actual validation nahi karta

Suppose:

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": "5000",
    "department": "HVAC"
}
```

`salary` ko `float` hona chahiye.

Static type checker error report kar sakta hai.

Lekin normal Python runtime automatically:

```text
"5000"
↓
reject
```

nahi karega.

Isliye:

> `TypedDict` runtime validation library nahi hai.

---

# 5. `TypedDict` kyun useful hai?

Tumhare work-order data ko dekho:

```text
Work Order Number
Code
Description
Area
Floor
Comment
```

Hum define kar sakte hain:

```python
from typing import TypedDict


class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: str
```

Ab:

```python
row: WorkOrder = {
    "work_order_number": "WO-1001",
    "code": "HVAC",
    "description": "AHU inspection",
    "area": "Mechanical Room",
    "floor": "34",
    "comment": "Normal"
}
```

Type checker ko complete structure pata hai.

---

# 6. Dictionary ki key typing

Normal:

```python
data["salary"]
```

`TypedDict` ke saath:

```python
data["salary"]
```

type checker samajhta hai:

```text
salary → float
```

Aur:

```python
data["name"]
```

means:

```text
name → str
```

---

# 7. Missing key

Agar:

```python
class EmployeeData(TypedDict):
    name: str
    salary: float
    department: str
```

Aur:

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": 5000
}
```

`department` missing hai.

Static type checker isko error report karega because default `TypedDict` fields required hote hain.

---

# 8. Extra key

Suppose:

```python
employee: EmployeeData = {
    "name": "Ali",
    "salary": 5000,
    "department": "HVAC",
    "age": 30
}
```

`age` defined structure mein nahi hai.

Type checker context ke mutabiq isko unexpected key ke taur par flag kar sakta hai.

---

# 9. `total=False`

Ab maan lo kuch fields optional hon:

```python
class EmployeeData(TypedDict, total=False):
    name: str
    salary: float
    department: str
```

Ab fields required nahi rahengi.

Example:

```python
employee: EmployeeData = {
    "name": "Ali"
}
```

valid type-wise ho sakta hai.

Mental model:

```text
total=True
↓
keys required by default

total=False
↓
keys optional by default
```

Default:

```python
class EmployeeData(TypedDict):
```

roughly:

```python
total=True
```

---

# 10. `Required` aur `NotRequired`

Modern typing mein tum individual fields ka behavior control kar sakte ho.

```python
from typing import TypedDict, NotRequired


class EmployeeData(TypedDict):
    name: str
    salary: float
    comment: NotRequired[str]
```

Ab:

```python
employee = {
    "name": "Ali",
    "salary": 5000
}
```

valid structure hai.

`comment` optional hai.

---

# 11. Required + optional mix

Example:

```python
from typing import TypedDict, NotRequired


class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: NotRequired[str]
```

Yahan:

```text
Required:
├── work_order_number
├── code
├── description
├── area
└── floor

Optional:
└── comment
```

---

# 12. `Required`

Agar overall `total=False` ho:

```python
from typing import TypedDict, Required


class WorkOrder(TypedDict, total=False):
    work_order_number: Required[str]
    description: Required[str]
    comment: str
```

Ab:

```text
Required:
├── work_order_number
└── description

Optional:
└── comment
```

---

# 13. `total=False` + `Required` / `NotRequired`

Ye combination large API/data structures mein useful hai.

```python
class EquipmentData(TypedDict, total=False):

    equipment_id: Required[str]
    equipment_type: Required[str]

    temperature: float
    humidity: float
    comment: str
```

Meaning:

```text
equipment_id     → required
equipment_type   → required

temperature      → optional
humidity         → optional
comment          → optional
```

---

# 14. Nested `TypedDict`

Real JSON/API data usually nested hota hai.

Example:

```python
class Location(TypedDict):
    floor: str
    area: str


class Equipment(TypedDict):
    equipment_id: str
    equipment_type: str
    location: Location
```

Data:

```python
equipment: Equipment = {
    "equipment_id": "AHU-01",
    "equipment_type": "AHU",
    "location": {
        "floor": "34",
        "area": "Mechanical Room"
    }
}
```

Ab:

```python
equipment["location"]["floor"]
```

type checker ko pata hai:

```text
str
```

---

# 15. API JSON example

Suppose API response:

```json
{
    "equipment_id": "AHU-01",
    "status": "Running",
    "temperature": 22.5
}
```

Define:

```python
class EquipmentResponse(TypedDict):
    equipment_id: str
    status: str
    temperature: float
```

Then:

```python
response: EquipmentResponse
```

Type information clear ho jati hai.

---

# 16. `TypedDict` vs `dataclass`

Ye important comparison hai.

### TypedDict

Data dictionary form mein:

```python
employee = {
    "name": "Ali",
    "salary": 5000
}
```

Best when:

* JSON
* API response
* CSV converted rows
* Google Sheets records
* dictionary-based data

---

### Dataclass

Object form:

```python
from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    salary: float
```

Then:

```python
employee = Employee("Ali", 5000)
```

Best when:

* actual Python objects
* methods
* behavior
* object-oriented design

---

# 17. Visual difference

```text
TypedDict

{
    "name": "Ali",
    "salary": 5000
}
```

versus:

```text
Dataclass

Employee(
    name="Ali",
    salary=5000
)
```

Simple rule:

> **Data dictionary hai → TypedDict**

> **Behavior wala object hai → dataclass/class**

---

# 18. `TypedDict` vs normal `dict`

Normal:

```python
data: dict[str, object]
```

Generic dictionary hai.

`TypedDict`:

```python
class EmployeeData(TypedDict):
    name: str
    salary: float
```

Specific structure hai.

```text
dict
↓
generic structure

TypedDict
↓
known keys + known value types
```

---

# 19. `TypedDict` vs `Protocol`

Ye bhi tumhare previous lessons se connect hota hai.

### TypedDict

Dictionary ki **data structure** define karta hai.

```python
class EmployeeData(TypedDict):
    name: str
    salary: float
```

### Protocol

Object ki **behavior/interface** define karta hai.

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Mental model:

```text
TypedDict
→ "Dictionary mein kya data hai?"

Protocol
→ "Object kya kar sakta hai?"
```

---

# 20. `TypedDict` vs normal class

Normal class:

```python
class Employee:

    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)
```

Yahan:

```text
data + behavior
```

TypedDict:

```python
class EmployeeData(TypedDict):
    name: str
```

Yahan primarily:

```text
data structure
```

---

# 21. Work-order example

Tumhare actual data structure ko imagine karo:

```python
class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: str
```

Ab function:

```python
def create_folder(work_order: WorkOrder) -> str:
    return work_order["work_order_number"]
```

Type checker knows:

```text
work_order
   ↓
WorkOrder
   ↓
["work_order_number"]
   ↓
str
```

Isse large scripts mein typo detection better hoti hai.

Example typo:

```python
work_order["workorder_number"]
```

Expected key defined nahi hai.

---

# 22. `TypedDict` ka ek important limitation

Ye:

```python
class EmployeeData(TypedDict):
    name: str
```

tumhe ye methods automatically nahi deta:

```python
employee.show()
employee.calculate_salary()
employee.save()
```

Kyun ke ye object-oriented class nahi.

Dictionary hi hai.

---

# 23. Runtime inspection

Tum:

```python
EmployeeData.__annotations__
```

se type annotations dekh sakte ho.

Aur modern Python mein:

```python
EmployeeData.__required_keys__
EmployeeData.__optional_keys__
```

se required/optional keys inspect ki ja sakti hain.

Example conceptual output:

```text
__required_keys__
{'name', 'salary'}

__optional_keys__
{'comment'}
```

---

# 24. JSON → TypedDict mental model

API/JSON:

```text
JSON
 ↓
dict
 ↓
TypedDict annotation
 ↓
static structure information
```

Important:

> `TypedDict` khud JSON ko validate/convert nahi karta.

Agar external data unreliable hai, runtime validation ke liye separate validation approach chahiye.

---

# 25. Complete example

```python
from typing import TypedDict, NotRequired


class Location(TypedDict):
    floor: str
    area: str


class EquipmentData(TypedDict):
    equipment_id: str
    equipment_type: str
    location: Location
    temperature: NotRequired[float]
    comment: NotRequired[str]
```

Data:

```python
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

Structure:

```text
EquipmentData
│
├── equipment_id → str
├── equipment_type → str
│
├── location → Location
│   ├── floor → str
│   └── area → str
│
├── temperature → float      optional
└── comment → str            optional
```

---

# 26. Aaj ka complete mental model

```text
dict
↓
normal dictionary

TypedDict
↓
dictionary ki expected structure

Required
↓
key lazmi

NotRequired
↓
key optional

total=False
↓
normally all fields optional

Nested TypedDict
↓
dictionary ke andar structured dictionary
```

Aur comparison:

```text
TypedDict
→ data structure

dataclass
→ data + object behavior

Protocol
→ object behavior/interface

normal class
→ data + behavior + OOP
```

### Ek line mein:

> **`TypedDict` runtime par normal `dict` hi hota hai, lekin static type checker ko batata hai ke dictionary mein kaunsi keys honi chahiye aur unki values kis type ki honi chahiye.**

### Next Lesson 41

Ab hum **`dataclass` deeply** karenge:

```python
@dataclass
class Equipment:
    equipment_id: str
    temperature: float
```

Phir dekhenge:

* `field()`
* `default`
* `default_factory`
* `frozen=True`
* `slots=True`
* `kw_only=True`
* `__post_init__()`
* `dataclass` vs normal class vs `TypedDict`
