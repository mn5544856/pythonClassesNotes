# Python OOP — Advanced Lessons 11-20 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 11: Composition vs Inheritance

## 1. Inheritance — "is-a"

```python
class Equipment:
    pass

class AHU(Equipment):
    pass
```

**Explanation:**
- `class Equipment:` → parent class
- `class AHU(Equipment):` → child class, `Equipment` se inherit
- `AHU` **IS-A** `Equipment` (AHU ek equipment hai)
- `isinstance(AHU(), Equipment)` → `True`

## 2. Composition — "has-a"

```python
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self):
        self.engine = Engine()
```

**Explanation:**
- `self.engine = Engine()` → Car ke andar Engine ka object
- `Car` **HAS-A** `Engine` (Car ke paas Engine hai)
- Car khud Engine nahi hai

**Use:**
```python
car = Car()
car.engine.start()
```

**Output:**
```
Engine started
```

## 3. HVAC Real Example

```python
class Fan:
    def start(self):
        print("Fan started")

class Damper:
    def open(self):
        print("Damper opened")

class TemperatureSensor:
    def read(self):
        return 22

class AHU:
    def __init__(self):
        self.fan = Fan()
        self.damper = Damper()
        self.sensor = TemperatureSensor()
```

**Explanation:**
- `self.fan = Fan()` → AHU ke andar Fan ka object
- `self.damper = Damper()` → AHU ke andar Damper ka object
- `self.sensor = TemperatureSensor()` → AHU ke andar Sensor ka object
- AHU **HAS-A** Fan, Damper, Sensor (composition)

**Use:**
```python
ahu = AHU()
ahu.fan.start()
ahu.damper.open()
print(ahu.sensor.read())
```

**Output:**
```
Fan started
Damper opened
22
```

## 4. Composition + Inheritance Together

```python
class Equipment:
    def start(self):
        print("Equipment started")

class AHU(Equipment):
    def __init__(self):
        self.fan = Fan()
        self.sensor = TemperatureSensor()
```

**Explanation:**
- `class AHU(Equipment):` → inheritance (AHU IS-A Equipment)
- `self.fan = Fan()` → composition (AHU HAS-A Fan)
- `self.sensor = TemperatureSensor()` → composition (AHU HAS-A Sensor)

## 5. Dependency Injection

```python
class AHU:
    def __init__(self, fan):
        self.fan = fan
```

**Explanation:**
- `def __init__(self, fan):` → fan bahar se provide hota hai
- AHU khud decide nahi karta kaunsa Fan use karna hai
- User provide karta hai: `ahu = AHU(Fan())`

**Benefit:**
```python
class NormalFan:
    def start(self):
        print("Normal fan")

class HighSpeedFan:
    def start(self):
        print("High speed fan")

ahu1 = AHU(NormalFan())
ahu2 = AHU(HighSpeedFan())

ahu1.start()   # Normal fan
ahu2.start()   # High speed fan
```

**Explanation:**
- Same `AHU` class, different Fan types
- Composition + Polymorphism dono use ho rahe hain

## 6. Comparison Table

| Inheritance | Composition |
|-------------|-------------|
| IS-A | HAS-A |
| `class AHU(Equipment)` | `self.fan = Fan()` |
| Code reuse | Components combine |
| Tight relationship | Flexible |
| Override possible | Replace easy |

## 7. "Favor Composition Over Inheritance"

Jab genuine **IS-A** relationship ho to inheritance use karo. Warna composition zyada flexible hoti hai.

---

# Lesson 12: `@property` — Deep Understanding

## 1. Normal Attribute

```python
class Employee:
    def __init__(self, name):
        self.name = name

emp = Employee("Ali")
print(emp.name)
```

**Output:**
```
Ali
```

**Explanation:**
- `self.name = name` → normal instance attribute
- `emp.name` → direct access

## 2. `@property` Kya Change Karta Hai?

```python
class Employee:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

emp = Employee("Ali")
print(emp.name)
```

**Output:**
```
Ali
```

**Explanation:**
- `@property` → `name()` method ko attribute ki tarah access karne deta hai
- `emp.name` → getter call hua, `_name` return hua
- Parentheses nahi lagte: `emp.name` (na ke `emp.name()`)

## 3. Method vs Property

**Method:**
```python
emp.get_name()
```

**Property:**
```python
emp.name
```

## 4. Property Ka Real Faida

```python
class Employee:
    def __init__(self, salary):
        self._salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary negative nahi ho sakti")
        self._salary = value
```

**Explanation:**
- `@property` → getter define kiya
- `@salary.setter` → setter define kiya
- `if value < 0:` → validation laga di

**Use:**
```python
emp = Employee(5000)
print(emp.salary)      # 5000
emp.salary = 6000      # setter call hua
print(emp.salary)      # 6000
emp.salary = -100      # ValueError
```

## 5. Read-Only Property

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary

    @property
    def annual_salary(self):
        return self._salary * 12
```

**Explanation:**
- `annual_salary` → sirf getter hai, setter nahi
- `emp.annual_salary` → read kar sakte hain
- `emp.annual_salary = 100000` → error (setter nahi)

**Use:**
```python
emp = Employee("Ali", 5000)
print(emp.annual_salary)   # 60000
```

## 6. Calculated Property — HVAC Example

```python
class AHU:
    def __init__(self, supply_temp, return_temp):
        self.supply_temp = supply_temp
        self.return_temp = return_temp

    @property
    def delta_t(self):
        return self.return_temp - self.supply_temp
```

**Explanation:**
- `delta_t` → stored nahi hai, calculate hota hai
- `return self.return_temp - self.supply_temp` → 24 - 18 = 6

**Use:**
```python
ahu = AHU(18, 24)
print(ahu.delta_t)   # 6
```

## 7. `self._salary` Kyun?

```python
@property
def salary(self):
    return self._salary
```

**Explanation:**
- `self.salary` nahi likhte (recursion ho jayegi)
- `self._salary` → internal storage
- Getter khud ko call nahi karta

## 8. Mental Model

```
emp.salary        →  @property  →  getter  →  _salary
emp.salary = 6000 →  @setter    →  validation  →  _salary
```

## 9. Kab Property Use Karein?

- Validation chahiye
- Calculated value chahiye
- Read-only attribute banana ho
- Internal implementation hide karni ho

Simple data ke liye normal attribute theek hai.

---

# Lesson 13: Attribute Lookup — `__getattribute__`, `__getattr__`, `__setattr__`

## 1. Normal Attribute Access

```python
class Employee:
    def __init__(self):
        self.name = "Ali"

emp = Employee()
print(emp.name)
```

**Output:**
```
Ali
```

**Explanation:**
- `emp.name` → Python internally `__getattribute__("name")` call karta hai
- Attribute search hoti hai, `"Ali"` return hota hai

## 2. `__getattribute__`

```python
class Employee:
    def __init__(self):
        self.name = "Ali"

    def __getattribute__(self, name):
        print("Accessing:", name)
        return super().__getattribute__(name)

emp = Employee()
print(emp.name)
```

**Output:**
```
Accessing: name
Ali
```

**Explanation:**
- `def __getattribute__(self, name):` → har attribute access par call
- `print("Accessing:", name)` → print kiya
- `super().__getattribute__(name)` → actual lookup continue kiya
- `emp.name` → `__getattribute__` involve hua

## 3. `__getattr__`

```python
class Employee:
    def __init__(self):
        self.name = "Ali"

    def __getattr__(self, name):
        return "Attribute nahi mila"

emp = Employee()
print(emp.name)      # Ali (exist karta hai)
print(emp.salary)    # Attribute nahi mila (nahi mila)
```

**Output:**
```
Ali
Attribute nahi mila
```

**Explanation:**
- `__getattr__` → sirf tab call hota hai jab normal lookup fail ho
- `emp.name` → exist karta hai, `__getattr__` nahi chala
- `emp.salary` → nahi mila, `__getattr__` chala

## 4. Difference

| Method | Kab run hota hai |
|--------|------------------|
| `__getattribute__` | Har attribute read par |
| `__getattr__` | Attribute normal lookup mein na mile |

## 5. `__setattr__`

```python
class Employee:
    def __setattr__(self, name, value):
        print("Setting:", name, value)
        super().__setattr__(name, value)

emp = Employee()
emp.name = "Ali"
emp.salary = 5000
```

**Output:**
```
Setting: name Ali
Setting: salary 5000
```

**Explanation:**
- `def __setattr__(self, name, value):` → har attribute assignment par call
- `print("Setting:", name, value)` → print kiya
- `super().__setattr__(name, value)` → actual set kiya

## 6. `__setattr__` with Validation

```python
class Temperature:
    def __setattr__(self, name, value):
        if name == "value" and value < -273.15:
            raise ValueError("Invalid temperature")
        super().__setattr__(name, value)

t = Temperature()
t.value = 25      # OK
t.value = -300    # ValueError
```

**Explanation:**
- `if name == "value" and value < -273.15:` → validation
- `t.value = -300` → error raise hua

## 7. `__delattr__`

```python
class Employee:
    def __delattr__(self, name):
        print("Deleting:", name)
        super().__delattr__(name)

emp = Employee()
emp.name = "Ali"
del emp.name
```

**Output:**
```
Deleting: name
```

**Explanation:**
- `def __delattr__(self, name):` → `del obj.name` par call
- `del emp.name` → `__delattr__` chala

## 8. Complete Flow

```
Read:   obj.x         → __getattribute__ → (fail) → __getattr__
Write:  obj.x = value → __setattr__
Delete: del obj.x     → __delattr__
```

## 9. `__setattr__` vs `@property`

| `@property` | `__setattr__` |
|-------------|---------------|
| Specific attribute | All attribute assignments |
| `value` control | General mechanism |

---

# Lesson 14: Descriptors — `__get__`, `__set__`, `__delete__`

## 1. Basic Descriptor

```python
class Descriptor:
    def __get__(self, instance, owner):
        print("GET")

    def __set__(self, instance, value):
        print("SET", value)

class Employee:
    salary = Descriptor()

emp = Employee()
emp.salary          # GET
emp.salary = 5000   # SET 5000
```

**Output:**
```
GET
SET 5000
```

**Explanation:**
- `class Descriptor:` → descriptor class
- `def __get__(self, instance, owner):` → read par call
- `def __set__(self, instance, value):` → write par call
- `salary = Descriptor()` → class attribute descriptor hai
- `emp.salary` → `__get__` chala
- `emp.salary = 5000` → `__set__` chala

## 2. `instance` aur `owner`

```python
def __get__(self, instance, owner):
```

**Explanation:**
- `self` → descriptor object
- `instance` → jis object par access hua (`emp`)
- `owner` → jis class mein descriptor hai (`Employee`)

## 3. Practical Descriptor — Validation

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Value negative nahi ho sakti")
        instance.__dict__[self.name] = value

class Employee:
    salary = PositiveNumber()
```

**Explanation:**
- `__set_name__` → Python batata hai descriptor kis naam se assign hua
- `self.name = name` → `"salary"` store kiya
- `__get__` → `instance.__dict__[self.name]` se value return ki
- `__set__` → validation ke baad `instance.__dict__[self.name]` mein store kiya

**Use:**
```python
emp = Employee()
emp.salary = 5000    # OK
print(emp.salary)    # 5000
emp.salary = -100    # ValueError
```

## 4. Multiple Fields

```python
class Employee:
    salary = PositiveNumber()
    bonus = PositiveNumber()
```

**Explanation:**
- Ek hi descriptor class dono fields ke liye use ho rahi hai
- `__set_name__` se pata chalta hai kaunsa field hai

## 5. Property vs Descriptor

**Property:**
```python
@property
def salary(self):
    return self._salary
```

**Descriptor:**
```python
class PositiveNumber:
    def __get__(self, instance, owner):
        ...
```

**Explanation:**
- Property specific attribute ke liye
- Descriptor reusable, multiple classes/attributes ke liye

## 6. Property Khud Descriptor Hai

```
@property → property object → Descriptor behavior → __get__/__set__
```

## 7. Data vs Non-Data Descriptor

| Type | Methods | Priority |
|------|---------|----------|
| Data | `__get__` + `__set__` | Higher |
| Non-Data | sirf `__get__` | Lower |

## 8. HVAC Example

```python
class RangeValue:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not self.minimum <= value <= self.maximum:
            raise ValueError(f"{self.name} range se bahar hai")
        instance.__dict__[self.name] = value

class AHU:
    temperature = RangeValue(-20, 60)
    humidity = RangeValue(0, 100)
```

**Explanation:**
- `RangeValue` → reusable descriptor
- `temperature = RangeValue(-20, 60)` → range define ki
- `humidity = RangeValue(0, 100)` → range define ki
- `ahu.temperature = 22` → OK
- `ahu.humidity = 150` → ValueError

## 9. Mental Model

```
obj.temperature        → descriptor → __get__ → value
obj.temperature = 25   → descriptor → __set__ → validation → storage
```

---

# Lesson 15: Context Managers — `with`, `__enter__`, `__exit__`

## 1. Problem

```python
file = open("data.txt")
data = file.read()
some_function_that_fails()
file.close()
```

**Explanation:**
- Agar `some_function_that_fails()` error de, `file.close()` nahi chalega
- Resource properly close nahi hoga

## 2. `with` Solution

```python
with open("data.txt") as file:
    data = file.read()
```

**Explanation:**
- `with` ensure karta hai cleanup ho
- Exception aaye ya na aaye, cleanup hoga

## 3. Context Manager

```python
class Demo:
    def __enter__(self):
        print("Enter")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exit")

with Demo() as obj:
    print("Inside")
```

**Output:**
```
Enter
Inside
Exit
```

**Explanation:**
- `__enter__` → `with` block start par call
- `return self` → `obj` ko `self` mila
- `__exit__` → `with` block end par call
- `with Demo() as obj:` → `obj = __enter__()` ka return

## 4. `__exit__` ke 3 Parameters

```python
def __exit__(self, exc_type, exc_value, traceback):
```

**Explanation:**
- `exc_type` → exception ki class (e.g., `ValueError`)
- `exc_value` → exception ka message
- `traceback` → error kahan hua

## 5. Exception ke Saath

```python
class Demo:
    def __enter__(self):
        print("Start")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cleanup")
        print(exc_type)
        print(exc_value)

with Demo():
    print("Work")
    raise ValueError("Something wrong")
```

**Output:**
```
Start
Work
Cleanup
<class 'ValueError'>
Something wrong
```

**Explanation:**
- Exception ke bawajood `__exit__` chala
- `exc_type` = `ValueError`
- `exc_value` = `Something wrong`

## 6. Exception Suppress Karna

```python
class Demo:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exception handled")
        return True

with Demo():
    raise ValueError("Error")
```

**Output:**
```
Exception handled
```

**Explanation:**
- `return True` → exception suppress ho gayi
- `return False` ya `None` → exception propagate hogi

## 7. HVAC Example

```python
class HVACConnection:
    def __enter__(self):
        print("HVAC connection opened")
        return self

    def read_point(self, point):
        print("Reading:", point)

    def __exit__(self, exc_type, exc_value, traceback):
        print("HVAC connection closed")

with HVACConnection() as connection:
    connection.read_point("AHU-01.Temperature")
    connection.read_point("AHU-01.Damper")
```

**Output:**
```
HVAC connection opened
Reading: AHU-01.Temperature
Reading: AHU-01.Damper
HVAC connection closed
```

**Explanation:**
- `__enter__` → connection open
- `read_point()` → connection use
- `__exit__` → connection close (automatically)

## 8. Mental Model

```
with
  ↓
__enter__()
  ↓
Resource ready
  ↓
Your code
  ↓
__exit__()
  ↓
Cleanup
```

---

# Lesson 16: `__new__()` vs `__init__()`

## 1. Basic Difference

```
__new__()   → Object CREATE karta hai
__init__()  → Object INITIALIZE karta hai
```

## 2. `__new__` Example

```python
class Employee:
    def __new__(cls, name):
        print("__new__ called")
        return super().__new__(cls)

    def __init__(self, name):
        print("__init__ called")
        self.name = name

emp = Employee("Ali")
```

**Output:**
```
__new__ called
__init__ called
```

**Explanation:**
- `def __new__(cls, name):` → object create se pehle call
- `super().__new__(cls)` → actual object create kiya
- `def __init__(self, name):` → object create hone ke baad call
- `self.name = name` → initialize kiya

## 3. `cls` vs `self`

| Method | Parameter | Kab |
|--------|-----------|-----|
| `__new__` | `cls` | Object create se pehle |
| `__init__` | `self` | Object create ke baad |

## 4. `__new__` Return Na Kare

```python
class Employee:
    def __new__(cls):
        print("Creating")
        return None

    def __init__(self):
        print("Initializing")

emp = Employee()
```

**Output:**
```
Creating
```

**Explanation:**
- `return None` → object create nahi hua
- `__init__` skip ho gaya

## 5. Immutable Types — `PositiveInt`

```python
class PositiveInt(int):
    def __new__(cls, value):
        if value < 0:
            raise ValueError("Negative value allowed nahi")
        return super().__new__(cls, value)

x = PositiveInt(10)    # OK
x = PositiveInt(-5)    # ValueError
```

**Explanation:**
- `class PositiveInt(int):` → int se inherit
- `__new__` mein validation (kyunki int immutable hai)
- `super().__new__(cls, value)` → int object create kiya

## 6. Singleton Pattern

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)
```

**Output:**
```
True
```

**Explanation:**
- `_instance = None` → class variable
- `if cls._instance is None:` → pehli baar check
- `cls._instance = super().__new__(cls)` → object create kiya
- `return cls._instance` → same object return kiya
- `a is b` → `True` (same object)

## 7. Singleton with `__init__` Issue

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating object")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("Initializing")

a = Singleton()
b = Singleton()
```

**Output:**
```
Creating object
Initializing
Initializing
```

**Explanation:**
- Object sirf **ek baar** create hua
- Lekin `__init__` **do baar** chala

## 8. Complete Flow

```
Employee("Ali")
      ↓
__new__()
      ↓
Object create
      ↓
__init__()
      ↓
self.name = "Ali"
      ↓
emp
```

## 9. Kab `__new__` Use Karein?

- Immutable types subclass karte waqt
- Object creation control karna ho
- Singleton/Flyweight patterns
- Metaprogramming
- Advanced framework development

Normal classes mein `__init__` kaafi hai.

---

# Lesson 17: Metaclasses — `type`, Class Bhi Object Hai

## 1. Class Bhi Object Hai

```python
class Employee:
    pass

emp = Employee()

print(type(emp))        # <class '__main__.Employee'>
print(type(Employee))   # <class 'type'>
```

**Output:**
```
<class '__main__.Employee'>
<class 'type'>
```

**Explanation:**
- `type(emp)` → `emp` kis class ka object hai? → `Employee`
- `type(Employee)` → `Employee` kis class ka object hai? → `type`
- Yani `Employee` bhi ek object hai, `type` ka

## 2. Relationship

```
emp
 ↓
Employee
 ↓
type
```

- `emp` is instance of `Employee`
- `Employee` is instance of `type`

## 3. `type()` se Class Banana

```python
Employee = type(
    "Employee",
    (),
    {}
)

emp = Employee()
print(type(emp))
```

**Output:**
```
<class '__main__.Employee'>
```

**Explanation:**
- `type(name, bases, namespace)` → 3 arguments
- `"Employee"` → class ka naam
- `()` → base classes (khali)
- `{}` → class namespace (attributes/methods)

## 4. Class with Attribute

```python
Employee = type(
    "Employee",
    (),
    {"company": "ABC"}
)

emp = Employee()
print(emp.company)
```

**Output:**
```
ABC
```

**Explanation:**
- `{"company": "ABC"}` → class attribute add kiya
- `emp.company` → `ABC`

## 5. Class with Method

```python
def show(self):
    print("Employee:", self.name)

Employee = type(
    "Employee",
    (),
    {"name": "Ali", "show": show}
)

emp = Employee()
emp.show()
```

**Output:**
```
Employee: Ali
```

**Explanation:**
- `"show": show` → method add kiya
- `emp.show()` → method call hua

## 6. Metaclass

```python
class MyMeta(type):
    def __new__(cls, name, bases, namespace):
        print("Class create ho rahi hai:", name)
        return super().__new__(cls, name, bases, namespace)

class Employee(metaclass=MyMeta):
    pass
```

**Output:**
```
Class create ho rahi hai: Employee
```

**Explanation:**
- `class MyMeta(type):` → metaclass, `type` se inherit
- `def __new__(cls, name, bases, namespace):` → class creation par call
- `class Employee(metaclass=MyMeta):` → metaclass use kiya
- `Employee` class create hote hi print hua

## 7. Metaclass vs Normal Class

| Normal Class | Metaclass |
|--------------|-----------|
| `__new__` → Employee objects | `__new__` → Employee classes |
| Instance creation | Class creation |

## 8. Automatic Registration

```python
registry = {}

class EquipmentMeta(type):
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        registry[name] = new_class
        return new_class

class AHU(metaclass=EquipmentMeta):
    pass

class VAV(metaclass=EquipmentMeta):
    pass

print(registry)
```

**Output:**
```
{'AHU': <class '__main__.AHU'>, 'VAV': <class '__main__.VAV'>}
```

**Explanation:**
- `registry = {}` → global dictionary
- `registry[name] = new_class` → class create hote hi register kiya
- `AHU`, `VAV` dono automatically register ho gaye

## 9. Complete Picture

```
                type
                 │ creates
                 ▼
             Employee
                 │ creates
                 ▼
                emp
```

## 10. Kab Metaclass Use Karein?

Normal code mein:
- ❌ Har problem ke liye metaclass nahi
- ✅ Pehle class, composition, inheritance, decorator, descriptor consider karo
- ✅ Metaclass tab jab class creation itself customize karni ho

---

# Lesson 18: ABC vs Protocol

## 1. ABC

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
- `class Equipment(ABC):` → abstract base class
- `@abstractmethod` → child ko implement karna hoga
- `class AHU(Equipment):` → inherit karna zaroori
- `def start(self):` → implement kiya

## 2. Protocol

```python
from typing import Protocol

class Equipment(Protocol):
    def start(self) -> None:
        ...

class AHU:
    def start(self):
        print("AHU ON")
```

**Explanation:**
- `class Equipment(Protocol):` → protocol define kiya
- `def start(self) -> None: ...` → method signature
- `class AHU:` → inherit **nahi** kiya
- `def start(self):` → same structure
- Protocol ke perspective se `AHU` compatible hai

## 3. Nominal vs Structural

**ABC — Nominal:**
```
AHU IS-A Equipment
```
Explicit inheritance zaroori.

**Protocol — Structural:**
```
AHU HAS-A start()
```
Structure match karta hai, inheritance zaroori nahi.

## 4. Duck Typing Connection

```python
def start(obj):
    obj.start()
```

**Explanation:**
- Python ko class ki detail nahi chahiye
- Sirf `start()` chahiye
- Ye runtime duck typing hai
- Protocol isi idea ko static typing mein formalize karta hai

## 5. `@runtime_checkable`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):
    def start(self) -> None:
        ...

class AHU:
    def start(self):
        print("AHU ON")

ahu = AHU()
print(isinstance(ahu, Startable))
```

**Output:**
```
True
```

**Explanation:**
- `@runtime_checkable` → runtime par check allow kiya
- `isinstance(ahu, Startable)` → `True` (structure match)
- Ye ABC jaisa complete validation nahi, sirf structural check

## 6. ABC vs Protocol Table

| Feature | ABC | Protocol |
|---------|-----|----------|
| Inheritance | Required | Nahi |
| Typing | Nominal | Structural |
| Idea | "Meri hierarchy ka part" | "Required behavior do" |
| Shared implementation | Possible | Usually interface only |
| Runtime enforcement | Abstract instantiate nahi hoti | Static checking mainly |

## 7. Mental Model

**ABC:**
```
"Come into my family."
        Equipment
             ↑
            AHU
```

**Protocol:**
```
"I don't care which family.
Just provide these capabilities."
AHU  ──┐
VAV  ──┼──> start()
Pump ──┘
```

## 8. Kab Kya Use Karein?

| Situation | Use |
|-----------|-----|
| Inheritance hierarchy + shared code | ABC |
| Behavior/interface, no inheritance | Protocol |
| Runtime par simple method call | Duck typing |

---

# Lesson 19: `Generic`, `TypeVar`, `Generic[T]`

## 1. `TypeVar`

```python
from typing import TypeVar

T = TypeVar("T")
```

**Explanation:**
- `T` → type variable
- Runtime data variable nahi hai
- Type system ke liye placeholder: "koi bhi ek type"

## 2. Generic Function

```python
from typing import TypeVar

T = TypeVar("T")

def first_item(items: list[T]) -> T:
    return items[0]
```

**Explanation:**
- `items: list[T]` → input list, elements type `T`
- `-> T` → output bhi type `T`
- `T` input aur output ko connect karta hai

**Use:**
```python
numbers = first_item([10, 20, 30])   # T = int
names = first_item(["Ali", "Ahmed"]) # T = str
```

## 3. Without `TypeVar`

```python
def first_item(items: list) -> object:
    return items[0]
```

**Explanation:**
- Type checker ko sirf pata: return `object`
- `list[int] → int` relationship lost
- `TypeVar` ye relationship preserve karta hai

## 4. Generic Class

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

**Explanation:**
- `class Box(Generic[T]):` → generic class
- `def __init__(self, value: T):` → value type `T`
- `def get(self) -> T:` → return type `T`

**Use:**
```python
number_box = Box[int](100)   # T = int
name_box = Box[str]("Ali")   # T = str
```

## 5. Multiple TypeVars

```python
T = TypeVar("T")
U = TypeVar("U")

def pair(first: T, second: U) -> tuple[T, U]:
    return first, second

result = pair(10, "Ali")   # tuple[int, str]
```

**Explanation:**
- `T` → pehla type
- `U` → doosra type
- `tuple[T, U]` → return type

## 6. HVAC Example

```python
T = TypeVar("T")

class SensorValue(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

temperature = SensorValue[float](22.5)
pressure = SensorValue[int](250)
status = SensorValue[str]("RUNNING")
```

**Explanation:**
- Ek class, different types
- `SensorValue[float]` → T = float
- `SensorValue[int]` → T = int
- `SensorValue[str]` → T = str

## 7. Constrained `TypeVar`

```python
T = TypeVar("T", int, float)

def square(value: T) -> T:
    return value * value
```

**Explanation:**
- `T` sirf `int` ya `float` ho sakta hai
- `square(5)` → OK
- `square(2.5)` → OK
- `square("hi")` → type checker warning

## 8. Bound `TypeVar`

```python
T = TypeVar("T", bound=Employee)

def process(employee: T) -> T:
    return employee
```

**Explanation:**
- `T` ko `Employee` ya subclass hona chahiye
- `process(Manager())` → T = Manager

## 9. `TypeVar` vs `Any`

| `Any` | `TypeVar` |
|-------|-----------|
| Type info loose | Type relationship preserve |
| Koi bhi type | Input-output connection |

## 10. Mental Model

```
Box[T]
  ↓
Box[int]       → 100
Box[str]       → "Ali"
Box[float]     → 22.5
Box[Employee]  → Employee object
```

---

# Lesson 20: `TypedDict`, `Mapping`, `Sequence`, `Iterable`, `Iterator`, `Callable`

## 1. `TypedDict`

`TypedDict` Python mein dictionary ke keys aur unki values ke expected data types define karne ke liye use hota hai. Is se type checkers ko pata chalta hai ke dictionary mein kaun se keys aur values honi chahiye.

```python
from typing import TypedDict

class Employee(TypedDict):
    name: str
    age: int
    salary: float

employee: Employee = {
    "name": "Ali",
    "age": 30,
    "salary": 5000.0
}

print(employee)
print(employee["name"])
print(employee["age"])
print(employee["salary"])
```

**Output:**

```text
{'name': 'Ali', 'age': 30, 'salary': 5000.0}
Ali
30
5000.0
```

**Important points:**

* `name: str` ka matlab name ki value string honi chahiye.
* `age: int` ka matlab age ki value integer honi chahiye.
* `salary: float` ka matlab salary ki value float honi chahiye.
* `TypedDict` runtime par automatically type validation nahi karta. Is ka primary purpose static type checking hai.

## 2. `Mapping`

`Mapping` ek read-only interface represent karta hai jo key-value pairs ko access karne deta hai. Isay tab use karte hain jab function ko dictionary ka data read karna ho, lekin dictionary ko modify karna zaroori na ho.

```python
from typing import Mapping

def show_employee(employee: Mapping[str, object]) -> None:
    print(employee["name"])
    print(employee["age"])

data = {
    "name": "Ali",
    "age": 30
}

show_employee(data)
```

**Output:**

```text
Ali
30
```

**Important points:**

* `Mapping[str, object]` ka matlab string keys aur kisi bhi type ki values wali mapping.
* `Mapping` ke through items read kiye ja sakte hain.
* Mapping interface ke through items add, update ya delete nahi kiye ja sakte.
* Normal `dict` object ko `Mapping` parameter ke taur par pass kiya ja sakta hai.

## 3. `Sequence`

`Sequence` ordered collection ko represent karta hai jiske elements ko index se access kiya ja sakta hai. Examples mein `list`, `tuple` aur `str` shamil hain.

```python
from typing import Sequence

def show_items(items: Sequence[str]) -> None:
    print("First item:", items[0])
    print("All items:", items)

fruits = ["Apple", "Banana", "Mango"]

show_items(fruits)
```

**Output:**

```text
First item: Apple
All items: ['Apple', 'Banana', 'Mango']
```

**Important points:**

* `Sequence[str]` string elements wali sequence ko represent karta hai.
* Indexing, slicing aur iteration supported hain.
* Sequence interface ke through collection ko modify karna supported nahi hota.
* `list` mutable hoti hai, lekin `tuple` immutable hota hai.

## 4. `Iterable`

`Iterable` aise object ko represent karta hai jiske elements par loop chalaya ja sakta hai, jaise `list`, `tuple`, `str` aur `set`.

```python
from typing import Iterable

def print_items(items: Iterable[str]) -> None:
    for item in items:
        print(item)

fruits = ["Apple", "Banana", "Mango"]

print_items(fruits)
```

**Output:**

```text
Apple
Banana
Mango
```

**Important points:**

* `Iterable` ko `for` loop mein use kiya ja sakta hai.
* Har iterable index-based access support nahi karta.
* Lists, tuples, sets aur generators iterable hote hain.
* Iterable se iterator hasil karne ke liye `iter()` use hota hai.

## 5. `Iterator`

`Iterator` aisa object hai jo elements ko ek-ek karke provide karta hai. Is mein `next()` ke zariye agla element hasil kiya ja sakta hai.

```python
from typing import Iterator

def count_numbers() -> Iterator[int]:
    yield 1
    yield 2
    yield 3

numbers = count_numbers()

print(next(numbers))
print(next(numbers))
print(next(numbers))
```

**Output:**

```text
1
2
3
```

**Important points:**

* `Iterator[int]` integers provide karne wale iterator ko represent karta hai.
* `next()` agla element return karta hai.
* Jab tamam elements khatam ho jate hain, `next()` `StopIteration` raise karta hai.
* `yield` function ko generator banata hai, jo values ek-ek karke produce karta hai.

**Example: Iterator with a loop**

```python
numbers = iter([10, 20, 30])

for number in numbers:
    print(number)
```

**Output:**

```text
10
20
30
```

## 6. `Callable`

`Callable` aise object ko represent karta hai jise function ki tarah call kiya ja sakta hai. Is se function ke expected arguments aur return type specify kiye ja sakte hain.

```python
from typing import Callable

def add(a: int, b: int) -> int:
    return a + b

def calculate(
    operation: Callable[[int, int], int],
    x: int,
    y: int
) -> int:
    return operation(x, y)

result = calculate(add, 10, 20)

print(result)
```

**Output:**

```text
30
```

**Important points:**

* `Callable[[int, int], int]` ka matlab aisa callable jo do integers accept kare aur integer return kare.
* Functions ko doosre functions ke arguments ke taur par pass kiya ja sakta hai.
* `Callable[..., int]` kisi bhi argument signature wale callable ko represent karta hai jo integer return karta hai; `...` argument types ko specify nahi karta.

### Additional Example: `Callable` with Lambda

```python
from typing import Callable

def apply_operation(
    operation: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return operation(a, b)

result = apply_operation(lambda x, y: x * y, 4, 5)

print(result)
```

**Output:**

```text
20
```

---

## 7. Quick Comparison

| Type        | Purpose                                         | Example                |
| ----------- | ----------------------------------------------- | ---------------------- |
| `TypedDict` | Dictionary ke keys aur value types define karna | Employee record        |
| `Mapping`   | Key-value data ko read karna                    | Dictionary reader      |
| `Sequence`  | Ordered, indexable collection                   | List, tuple, string    |
| `Iterable`  | Elements par loop chalana                       | List, set, generator   |
| `Iterator`  | Elements ek-ek karke provide karna              | `next()` aur generator |
| `Callable`  | Function-like object ka type define karna       | Function argument      |

## 8. Complete Practice Example

Is example mein `TypedDict`, `Mapping`, `Sequence`, `Iterable`, `Iterator` aur `Callable` ko alag-alag functions mein use kiya gaya hai.

```python
from typing import (
    TypedDict,
    Mapping,
    Sequence,
    Iterable,
    Iterator,
    Callable
)

class Employee(TypedDict):
    name: str
    age: int
    salary: float


def show_employee(employee: Mapping[str, object]) -> None:
    print("Employee:", employee["name"])


def show_names(names: Sequence[str]) -> None:
    print("First name:", names[0])


def print_names(names: Iterable[str]) -> None:
    for name in names:
        print(name)


def get_numbers() -> Iterator[int]:
    yield 1
    yield 2
    yield 3


def calculate(
    operation: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return operation(a, b)


employee: Employee = {
    "name": "Ali",
    "age": 30,
    "salary": 5000.0
}

show_employee(employee)

names = ["Ali", "Ahmed", "Sara"]
show_names(names)
print_names(names)

numbers = get_numbers()
print(next(numbers))
print(next(numbers))

result = calculate(lambda x, y: x + y, 10, 20)
print("Result:", result)
```

**Output:**

```text
Employee: Ali
First name: Ali
Ali
Ahmed
Sara
1
2
Result: 30
```

## 9. Practice Questions

1. `TypedDict` aur normal `dict` mein kya difference hai?
2. `Mapping` aur `Sequence` mein kya difference hai?
3. Kya har `Iterable` ek `Iterator` hota hai?
4. `next()` ka kya purpose hai?
5. `Callable[[int, int], int]` ka kya matlab hai?
6. Ek `Product` naam ka `TypedDict` banayein jisme `name`, `price` aur `quantity` hon.
7. Ek function banayein jo `Iterable[int]` accept kare aur tamam numbers ka sum return kare.
8. Ek function banayein jo `Callable[[int, int], int]` accept kare aur do numbers par operation perform kare.

**Lesson Summary:** In six typing tools ki madad se Python code ke expected data structures, iteration behavior aur function signatures ko clearly describe kiya ja sakta hai. Ye static type checking aur maintainable code likhne mein madad karte hain.
