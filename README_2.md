# Lesson 11: Composition vs Inheritance

Ab hum OOP ke ek **bohat important design concept** par hain:

> **Inheritance = "is-a" relationship**
> **Composition = "has-a" relationship**

Ye distinction real-world Python projects mein bohat useful hai.

---

# 1. Inheritance — "is-a"

Agar hum keh sakte hain:

> **AHU is an Equipment**

to inheritance logical hai.

```python
class Equipment:
    pass


class AHU(Equipment):
    pass
```

Relationship:

```text
AHU
 ↓
is an
 ↓
Equipment
```

Yani:

```python
isinstance(AHU(), Equipment)
```

`True` hoga.

---

# 2. Composition — "has-a"

Composition mein aik class ke andar doosri class ka object hota hai.

Example:

> **Car has an Engine**

Car khud Engine nahi hai.

```text
Car
 ↓
has an
 ↓
Engine
```

Code:

```python
class Engine:

    def start(self):
        print("Engine started")


class Car:

    def __init__(self):
        self.engine = Engine()
```

Ab:

```python
car = Car()

car.engine.start()
```

Output:

```text
Engine started
```

Yahan:

```python
self.engine = Engine()
```

**Composition** hai.

---

# 3. Difference simple example

### Inheritance

```python
class Dog(Animal):
```

Matlab:

```text
Dog IS-A Animal
```

### Composition

```python
class Dog:

    def __init__(self):
        self.brain = Brain()
```

Matlab:

```text
Dog HAS-A Brain
```

---

# 4. Real HVAC Example

Suppose AHU ke andar multiple components hain:

```text
AHU
 ├── Fan
 ├── Filter
 ├── Damper
 └── Sensor
```

AHU **fan nahi hai**.

AHU ke paas fan hai.

So:

```text
AHU HAS-A Fan
AHU HAS-A Filter
AHU HAS-A Damper
AHU HAS-A Sensor
```

Composition suitable hai.

---

# 5. Code

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
```

Ab AHU:

```python
class AHU:

    def __init__(self):
        self.fan = Fan()
        self.damper = Damper()
        self.sensor = TemperatureSensor()
```

Ab:

```python
ahu = AHU()

ahu.fan.start()
ahu.damper.open()

print(ahu.sensor.read())
```

Output:

```text
Fan started
Damper opened
22
```

Ye **composition** hai.

---

# 6. Composition ka visual model

```text
             AHU
              |
      ┌───────┼────────┐
      ↓       ↓        ↓
     Fan    Damper   Sensor
```

AHU ke paas ye objects hain.

Code:

```python
self.fan
self.damper
self.sensor
```

---

# 7. Inheritance ka visual model

```text
          Equipment
              |
       ┌──────┼──────┐
       ↓      ↓      ↓
      AHU    VAV    Pump
```

Yahan:

```text
AHU IS-A Equipment
VAV IS-A Equipment
Pump IS-A Equipment
```

---

# 8. Composition + Inheritance together

Real projects mein dono ek saath use ho sakte hain.

Example:

```python
class Equipment:

    def start(self):
        print("Equipment started")
```

AHU inherits:

```python
class AHU(Equipment):

    def __init__(self):
        self.fan = Fan()
        self.sensor = TemperatureSensor()
```

Yahan AHU:

**Inheritance:**

```text
AHU IS-A Equipment
```

**Composition:**

```text
AHU HAS-A Fan
AHU HAS-A Sensor
```

Ye bohat common OOP design hai.

---

# 9. Composition ka major benefit

Suppose:

```python
class AHU:
    ...
```

ke andar direct fan implementation kar di.

Baad mein tum different fan use karna chaho.

Better design:

```python
class Fan:

    def start(self):
        print("Standard fan")
```

AHU:

```python
class AHU:

    def __init__(self, fan):
        self.fan = fan
```

Ab fan bahar se provide kar sakte ho.

```python
fan = Fan()

ahu = AHU(fan)
```

Isay **dependency injection** kehte hain.

---

# 10. Dependency Injection

Naam thora advanced hai, concept simple hai.

Instead of:

```python
class AHU:

    def __init__(self):
        self.fan = Fan()
```

hum likh sakte hain:

```python
class AHU:

    def __init__(self, fan):
        self.fan = fan
```

Ab AHU khud decide nahi kar raha ke kaunsa Fan use karna hai.

User provide karta hai:

```python
fan = Fan()

ahu = AHU(fan)
```

---

# 11. Iska benefit

Suppose two fans hain:

```python
class NormalFan:

    def start(self):
        print("Normal fan")


class HighSpeedFan:

    def start(self):
        print("High speed fan")
```

AHU:

```python
class AHU:

    def __init__(self, fan):
        self.fan = fan

    def start(self):
        self.fan.start()
```

Ab:

```python
ahu1 = AHU(NormalFan())
ahu2 = AHU(HighSpeedFan())
```

Dono same `AHU` class use kar rahe hain.

Lekin behavior different:

```python
ahu1.start()
ahu2.start()
```

Output:

```text
Normal fan
High speed fan
```

Yahan **Composition + Polymorphism** dono use ho rahe hain.

---

# 12. Composition vs Inheritance

| Inheritance               | Composition                    |
| ------------------------- | ------------------------------ |
| IS-A                      | HAS-A                          |
| Parent/child relationship | Object contains another object |
| `class AHU(Equipment)`    | `self.fan = Fan()`             |
| Code reuse                | Components combine karna       |
| Tight relationship        | Usually more flexible          |
| Override possible         | Component replace karna easy   |

---

# 13. Kab inheritance use karein?

Jab genuine **IS-A** relationship ho.

Example:

```text
Dog is an Animal
AHU is Equipment
Manager is Employee
```

Code:

```python
class Dog(Animal):
```

---

# 14. Kab composition use karein?

Jab **HAS-A** relationship ho.

Example:

```text
Car has an Engine
AHU has a Fan
Computer has a CPU
House has Rooms
```

Code:

```python
class Car:

    def __init__(self):
        self.engine = Engine()
```

---

# 15. Ek common mistake

Ye design questionable ho sakta hai:

```python
class Car(Engine):
    pass
```

Kyun?

Car **Engine nahi hai**.

Car ke paas Engine hai.

Better:

```python
class Car:

    def __init__(self):
        self.engine = Engine()
```

Yani:

```text
Car HAS-A Engine
```

---

# 16. Composition aur Encapsulation

Composition mein internal components ko hide bhi kar sakte hain.

```python
class AHU:

    def __init__(self):
        self.__fan = Fan()

    def start(self):
        self.__fan.start()
```

Ab user simply:

```python
ahu = AHU()

ahu.start()
```

User ko ye detail jaanne ki zaroorat nahi:

```text
AHU
 ↓
internal fan
 ↓
Fan.start()
```

Yahan:

**Composition + Encapsulation** dono hain.

---

# 17. Composition aur Polymorphism

Aur agar:

```python
class NormalFan:

    def start(self):
        print("Normal fan")


class VariableSpeedFan:

    def start(self):
        print("Variable speed fan")
```

AHU:

```python
class AHU:

    def __init__(self, fan):
        self.fan = fan

    def start(self):
        self.fan.start()
```

Ab:

```python
ahu1 = AHU(NormalFan())
ahu2 = AHU(VariableSpeedFan())
```

Aur:

```python
ahu1.start()
ahu2.start()
```

Same:

```python
self.fan.start()
```

Lekin different behavior.

Ye **polymorphism through composition** hai.

---

# 18. Important concept: "Favor Composition Over Inheritance"

Software engineering mein aik common design principle hai:

> Jab inheritance ki zaroorat genuinely na ho, composition aksar zyada flexible design de sakti hai.

Lekin iska matlab ye nahi:

> "Inheritance kabhi use nahi karni."

Inheritance useful hai jab actual **IS-A** relationship aur shared abstraction ho.

Composition useful hai jab tum components ko combine aur replace karna chahte ho.

---

# 19. Complete Example

```python
class Sensor:

    def read(self):
        return 22


class Fan:

    def start(self):
        print("Fan started")


class Equipment:

    def status(self):
        print("Equipment running")


class AHU(Equipment):

    def __init__(self, fan, sensor):
        self.fan = fan
        self.sensor = sensor

    def start(self):
        self.fan.start()

    def temperature(self):
        return self.sensor.read()
```

Use:

```python
fan = Fan()
sensor = Sensor()

ahu = AHU(fan, sensor)
```

Ab:

```python
ahu.status()
ahu.start()

print(ahu.temperature())
```

Output:

```text
Equipment running
Fan started
22
```

Is aik example mein:

### Inheritance

```python
class AHU(Equipment):
```

AHU **IS-A Equipment**.

### Composition

```python
self.fan = fan
self.sensor = sensor
```

AHU **HAS-A Fan** aur **HAS-A Sensor**.

### Encapsulation

AHU internal components ko apne methods ke through expose kar sakta hai.

### Polymorphism

Different `Fan` implementations `start()` provide kar sakti hain.

---

# 20. Ab tak OOP ka complete map

```text
                         OOP
                          |
       ┌──────────────────┼──────────────────┐
       ↓                  ↓                  ↓
  Encapsulation       Inheritance       Polymorphism
       |                  |                  |
  Data control         IS-A             Same interface
                                            |
                                            ↓
                                     Different behavior

                    Abstraction
                         |
                         ↓
                  Interface hide
                  implementation
```

Aur design relationships:

```text
Inheritance
    ↓
  IS-A

Composition
    ↓
 HAS-A
```

### Ek line mein:

```text
AHU IS-A Equipment
AHU HAS-A Fan
```

Ye distinction strong ho jaye to OOP design samajhna kaafi easy ho jata hai.

**Next Lesson 12:** **`@property`, descriptors aur attribute access ka deeper concept** — `obj.x` ke peeche Python actually kya karta hai, aur `property` internally kaise kaam karti hai.

# Lesson 12: `@property` aur Attribute Access — Deep Understanding

Ab hum `@property` ko sirf getter/setter ke tor par nahi, balkay **Python ke attribute access mechanism** ke perspective se samjhenge.

---

## 1. Normal attribute kya hota hai?

```python
class Employee:

    def __init__(self, name):
        self.name = name
```

Object:

```python
emp = Employee("Ali")
```

Ab:

```python
print(emp.name)
```

Output:

```text
Ali
```

Yahan `emp.name` ek normal **instance attribute** hai.

---

# 2. `@property` kya change karta hai?

Ab:

```python
class Employee:

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
```

Use:

```python
emp = Employee("Ali")

print(emp.name)
```

Output:

```text
Ali
```

Interesting baat:

Humne likha:

```python
emp.name
```

Lekin internally Python `name()` property ka getter execute karta hai.

Conceptually:

```text
emp.name
   ↓
property getter
   ↓
return self._name
```

Isliye property ko **method ko attribute ki tarah access karne ka mechanism** samajh sakte ho.

---

# 3. Method aur property ka difference

Normal method:

```python
class Employee:

    def get_name(self):
        return self._name
```

Call:

```python
emp.get_name()
```

Lekin property:

```python
@property
def name(self):
    return self._name
```

Call:

```python
emp.name
```

### Difference:

```text
Method:
emp.get_name()

Property:
emp.name
```

Parentheses nahi lagte.

---

# 4. Property ka real faida

Suppose pehle tumhara code ye tha:

```python
class Employee:

    def __init__(self, salary):
        self.salary = salary
```

Log use kar rahe hain:

```python
emp.salary
```

Baad mein tum decide karte ho salary ko validate karna hai.

Agar direct attribute hai:

```python
emp.salary = -500
```

ye allow ho sakta hai.

Property use karo:

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

Ab:

```python
emp = Employee(5000)

print(emp.salary)
```

Output:

```text
5000
```

Aur:

```python
emp.salary = -100
```

Error:

```text
ValueError
```

---

# 5. Sabse important benefit

User code same reh sakta hai:

```python
emp.salary
```

Pehle:

```text
simple attribute
```

Baad mein:

```text
property + validation
```

Lekin bahar se interface same:

```python
emp.salary
```

Ye **encapsulation** ka powerful example hai.

---

# 6. Getter

```python
@property
def salary(self):
    return self._salary
```

Ye **getter** hai.

Jab:

```python
emp.salary
```

likhte ho, getter execute hota hai.

---

# 7. Setter

```python
@salary.setter
def salary(self, value):
    self._salary = value
```

Jab:

```python
emp.salary = 6000
```

likhte ho, setter execute hota hai.

Conceptually:

```text
emp.salary
     ↓
   getter
```

Aur:

```text
emp.salary = 6000
     ↓
   setter
```

---

# 8. Getter + Setter complete example

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
            raise ValueError("Invalid salary")

        self._salary = value
```

Use:

```python
emp = Employee(5000)

print(emp.salary)

emp.salary = 7000

print(emp.salary)
```

Output:

```text
5000
7000
```

---

# 9. Setter kyun useful hai?

Setter mein business rules laga sakte ho.

Example:

```python
@salary.setter
def salary(self, value):

    if not isinstance(value, (int, float)):
        raise TypeError("Salary number honi chahiye")

    if value < 0:
        raise ValueError("Salary negative nahi ho sakti")

    self._salary = value
```

Ab:

```python
emp.salary = "hello"
```

allowed nahi hoga.

Aur:

```python
emp.salary = -500
```

bhi allowed nahi hoga.

---

# 10. Read-only property

Kabhi hum chahte hain user value **read** kar sake lekin directly change na kar sake.

Example:

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self._salary = salary

    @property
    def annual_salary(self):
        return self._salary * 12
```

Ab:

```python
emp = Employee("Ali", 5000)

print(emp.annual_salary)
```

Output:

```text
60000
```

Lekin:

```python
emp.annual_salary = 100000
```

setter define nahi hai, isliye assignment allowed nahi hogi.

---

# 11. Property calculated value bhi ho sakti hai

Ye important hai.

Property zaroori nahi ke kisi variable ko simply return kare.

Example:

```python
class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height
```

Use:

```python
r = Rectangle(10, 5)

print(r.area)
```

Output:

```text
50
```

Yahan `area` actual stored variable nahi hai.

Python calculate kar raha hai:

```python
self.width * self.height
```

Lekin user ko ye attribute jaisa nazar aa raha hai:

```python
r.area
```

---

# 12. Method ki jagah property kyun?

Agar value object ki **natural attribute/property** lagti hai, property convenient hai.

Compare:

```python
r.get_area()
```

versus:

```python
r.area
```

`area` ko property banana zyada natural hai kyunki area object ki state se derived value hai.

---

# 13. HVAC example

Suppose AHU ke paas:

```text
Supply Air Temperature = 18°C
Return Air Temperature = 24°C
```

Temperature difference:

```text
24 - 18 = 6°C
```

Code:

```python
class AHU:

    def __init__(self, supply_temp, return_temp):
        self.supply_temp = supply_temp
        self.return_temp = return_temp

    @property
    def delta_t(self):
        return self.return_temp - self.supply_temp
```

Use:

```python
ahu = AHU(18, 24)

print(ahu.delta_t)
```

Output:

```text
6
```

`delta_t` stored nahi hai.

Ye **calculated property** hai.

---

# 14. `@property` actually kya return karta hai?

Ye thora advanced point hai.

Jab tum likhte ho:

```python
@property
def salary(self):
    return self._salary
```

Python `salary` ko normal function ki tarah class mein store nahi karta.

`@property` decorator function ko ek **property object** mein convert karta hai.

Conceptually:

```text
function
   ↓
@property
   ↓
property object
```

Is property object ke paas getter/setter/deleter mechanism hota hai.

---

# 15. Ye line

```python
@property
def salary(self):
```

roughly conceptually:

```python
salary = property(salary)
```

jaisa samjhi ja sakti hai.

Aur setter:

```python
@salary.setter
def salary(self, value):
```

property ke setter ko configure karta hai.

---

# 16. `obj.x` ke peeche kya hota hai?

Jab tum likhte ho:

```python
emp.salary
```

Python attribute lookup perform karta hai.

Simplified mental model:

```text
emp.salary
    ↓
Python attribute lookup
    ↓
class mein salary property?
    ↓
YES
    ↓
property getter
    ↓
return value
```

Isliye `@property` Python ke **attribute access protocol** ka part hai.

---

# 17. `self._salary` kyun?

Tumne dekha:

```python
@property
def salary(self):
    return self._salary
```

Aur:

```python
@salary.setter
def salary(self, value):
    self._salary = value
```

Hum `salary` ke andar `self.salary` nahi likhte.

Galat:

```python
@property
def salary(self):
    return self.salary
```

Kyun?

Ye getter khud ko dobara call karega:

```text
salary
 ↓
salary
 ↓
salary
 ↓
salary
...
```

Eventually recursion error.

Isliye internal storage ke liye different name use karte hain:

```python
self._salary
```

---

# 18. Mental model

Is pattern ko yaad rakho:

```python
class Employee:

    def __init__(self, salary):
        self._salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = value
```

External interface:

```text
emp.salary
```

Internal storage:

```text
emp._salary
```

Beech mein:

```text
        salary
          ↓
     ┌──────────┐
     │ property │
     └──────────┘
       ↓      ↓
    getter   setter
       ↓      ↓
    _salary _salary
```

---

# 19. Property ka use kab karna chahiye?

Useful when:

* validation chahiye
* calculated value chahiye
* read-only attribute banana ho
* existing attribute interface ko preserve karna ho
* internal implementation hide karni ho

Har variable ko property banana zaroori nahi.

Simple data ho:

```python
self.name = "Ali"
```

to normal attribute bilkul theek hai.

---

# Practice

Ye class complete karo:

```python
class Temperature:

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        # getter

    @value.setter
    def value(self, new_value):
        # setter
        # temperature -273.15 se kam nahi honi chahiye
```

Goal:

```python
t = Temperature(25)

print(t.value)

t.value = 30

print(t.value)
```

Expected:

```text
25
30
```

Aur:

```python
t.value = -300
```

par `ValueError` aana chahiye.

**Next Lesson 13:** Python mein **`__getattr__`, `__getattribute__`, `__setattr__` aur attribute lookup** — yani Python jab `obj.name` dekhta hai to internally kaise decide karta hai ke value kahan se leni hai.

# Lesson 13: Python Attribute Lookup — `__getattribute__`, `__getattr__`, `__setattr__`

Ab hum Python ke **attribute access mechanism** ko deep level par samjhenge.

Jab tum likhte ho:

```python
obj.name
```

Python simply variable nahi dhoond raha hota. Iske peeche **attribute lookup protocol** hota hai.

---

## 1. Normal attribute access

Example:

```python
class Employee:

    def __init__(self):
        self.name = "Ali"


emp = Employee()

print(emp.name)
```

Output:

```text
Ali
```

Tumhe simple lagta hai:

```text
emp.name
```

Lekin Python internally attribute ko lookup karta hai.

Simplified:

```text
emp.name
   ↓
__getattribute__("name")
   ↓
attribute search
   ↓
"Ali"
```

---

# 2. `__getattribute__`

`__getattribute__` **har attribute access** par call hota hai.

Example:

```python
class Employee:

    def __init__(self):
        self.name = "Ali"

    def __getattribute__(self, name):
        print("Accessing:", name)
        return super().__getattribute__(name)
```

Ab:

```python
emp = Employee()

print(emp.name)
```

Output approximately:

```text
Accessing: name
Ali
```

Jab tum:

```python
emp.name
```

karte ho, Python `__getattribute__()` ko involve karta hai.

---

# 3. `super().__getattribute__()` kyun?

Ye bohat important hai.

Humne:

```python
def __getattribute__(self, name):
    print("Accessing:", name)
    return super().__getattribute__(name)
```

likha.

`super().__getattribute__(name)` actual/default attribute lookup ko continue karta hai.

Agar hum simply:

```python
def __getattribute__(self, name):
    return self.name
```

likh dein, problem ho jayegi.

Kyun?

```text
self.name
   ↓
__getattribute__
   ↓
self.name
   ↓
__getattribute__
   ↓
self.name
   ↓
...
```

Ye **infinite recursion** create karega.

---

# 4. `__getattr__`

Ab doosra method:

```python
__getattr__
```

Ye `__getattribute__` se different hai.

`__getattr__` tab call hota hai jab **normal attribute lookup fail ho jaye**.

Example:

```python
class Employee:

    def __init__(self):
        self.name = "Ali"

    def __getattr__(self, name):
        return "Attribute nahi mila"
```

Ab:

```python
emp = Employee()

print(emp.name)
```

Output:

```text
Ali
```

Kyunki `name` exist karta hai.

Lekin:

```python
print(emp.salary)
```

Output:

```text
Attribute nahi mila
```

Kyunki `salary` nahi mila, isliye `__getattr__` run hua.

---

# 5. Sabse important difference

### `__getattribute__`

**Har attribute access** par run hota hai.

```text
emp.name
emp.salary
emp.department
```

sab par.

### `__getattr__`

Sirf tab run hota hai jab attribute **normally nahi mila**.

```text
emp.unknown
       ↓
not found
       ↓
__getattr__
```

---

# 6. Visual comparison

```text
             obj.name
                 |
                 ↓
       __getattribute__()
                 |
          ┌──────┴──────┐
          ↓             ↓
       Found         Not Found
          |             |
          ↓             ↓
       return      __getattr__()
                      |
                      ↓
                   return
```

---

# 7. Practical example — default value

Suppose equipment ke optional attributes ho sakte hain.

```python
class Equipment:

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    def __getattr__(self, name):
        return "N/A"
```

Use:

```python
ahu = Equipment("AHU-001")

print(ahu.equipment_id)
print(ahu.location)
print(ahu.status)
```

Output:

```text
AHU-001
N/A
N/A
```

Yahan `location` aur `status` exist nahi karte, isliye `__getattr__` default value provide karta hai.

---

# 8. Lekin `__getattr__` dangerous bhi ho sakta hai

Agar har missing attribute ke liye:

```python
return "N/A"
```

kar diya, spelling mistake bhi hide ho sakti hai.

Example:

```python
print(ahu.equipmnt_id)
```

Tumne `equipment_id` ki spelling galat likhi.

Normal Python:

```text
AttributeError
```

dega.

Lekin custom `__getattr__`:

```python
N/A
```

de sakta hai.

Isliye production code mein isko carefully use karna chahiye.

---

# 9. `__setattr__`

Ab attribute **set** karne ki baat.

Jab tum:

```python
emp.name = "Ali"
```

karte ho, Python attribute assignment perform karta hai.

Is process ko customize karne ke liye:

```python
__setattr__
```

use hota hai.

Example:

```python
class Employee:

    def __setattr__(self, name, value):
        print("Setting:", name, value)
        super().__setattr__(name, value)
```

Ab:

```python
emp = Employee()

emp.name = "Ali"
emp.salary = 5000
```

Output:

```text
Setting: name Ali
Setting: salary 5000
```

---

# 10. `__setattr__` mein validation

Ye practical use hai.

```python
class Temperature:

    def __setattr__(self, name, value):

        if name == "value" and value < -273.15:
            raise ValueError("Invalid temperature")

        super().__setattr__(name, value)
```

Ab:

```python
t = Temperature()

t.value = 25
```

allowed.

Lekin:

```python
t.value = -300
```

par:

```text
ValueError: Invalid temperature
```

---

# 11. `__setattr__` aur `@property` mein difference

Dono validation ke liye use ho sakte hain.

### Property

```python
class Temperature:

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < -273.15:
            raise ValueError("Invalid")
        self._value = value
```

Ye **specific attribute** `value` ko control kar raha hai.

### `__setattr__`

```python
def __setattr__(self, name, value):
```

Ye **general attribute assignment mechanism** ko intercept karta hai.

So:

```text
@property
    ↓
specific attribute

__setattr__
    ↓
all attribute assignments
```

---

# 12. `__getattribute__` vs `__getattr__` vs `__setattr__`

| Method             | Kab run hota hai?                    |
| ------------------ | ------------------------------------ |
| `__getattribute__` | Har attribute read par               |
| `__getattr__`      | Attribute normal lookup mein na mile |
| `__setattr__`      | Attribute assign karte waqt          |

Examples:

```python
obj.name
```

→ `__getattribute__`

```python
obj.unknown
```

→ `__getattribute__` → fail → `__getattr__`

```python
obj.name = "Ali"
```

→ `__setattr__`

---

# 13. `__delattr__`

Ek aur related dunder method:

```python
__delattr__
```

Jab:

```python
del obj.name
```

karte ho.

Example:

```python
class Employee:

    def __delattr__(self, name):
        print("Deleting:", name)
        super().__delattr__(name)
```

Use:

```python
emp = Employee()
emp.name = "Ali"

del emp.name
```

Output:

```text
Deleting: name
```

---

# 14. Ab complete attribute system

Basic level par:

```text
Read:
obj.x
  ↓
__getattribute__
  ↓
if missing → __getattr__

Write:
obj.x = value
  ↓
__setattr__

Delete:
del obj.x
  ↓
__delattr__
```

Ye Python ke object model ka important part hai.

---

# 15. Ek complete example

```python
class Equipment:

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    def __getattribute__(self, name):
        print("READ:", name)
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return "N/A"

    def __setattr__(self, name, value):
        print("WRITE:", name, value)
        super().__setattr__(name, value)
```

Use:

```python
equipment = Equipment("AHU-001")
```

Initialization ke waqt:

```text
WRITE: equipment_id AHU-001
```

Phir:

```python
print(equipment.equipment_id)
```

roughly:

```text
READ: equipment_id
AHU-001
```

Aur:

```python
print(equipment.location)
```

roughly:

```text
READ: location
N/A
```

---

# 16. Ye advanced OOP kyun hai?

Normal Python development mein tum aksar sirf:

```python
obj.name
obj.name = value
```

use karoge.

Lekin framework/library development mein:

```python
__getattribute__
__getattr__
__setattr__
__delattr__
```

bohat powerful ho sakte hain.

Examples:

* lazy loading
* proxy objects
* validation
* dynamic attributes
* ORM frameworks
* configuration systems
* logging
* API wrappers

---

# 17. Important warning

`__getattribute__` powerful hai lekin unnecessarily use nahi karna chahiye.

Agar tum sirf:

```python
salary
```

validate karna chahte ho to:

```python
@property
```

zyada readable hai.

Agar tum **har attribute access** control karna chahte ho, tab:

```python
__getattribute__
```

relevant ho sakta hai.

---

# 18. Connection with previous lesson

Previous lesson mein humne:

```python
@property
```

dekha tha.

Ab tum samajh sakte ho ke property sirf syntactic convenience nahi hai.

Python ka object model attribute access ko customize karne ki facilities deta hai:

```text
                Attribute Access
                       |
          ┌────────────┼────────────┐
          ↓            ↓            ↓
   __getattribute__ __setattr__ __delattr__
          |
          ↓
     __getattr__
```

Aur `property` isi broader attribute-access system ke andar kaam karti hai.

---

## Practice

Is class ko dekho:

```python
class Equipment:

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    def __getattr__(self, name):
        return "Point not available"
```

Ab predict karo:

```python
equipment = Equipment("AHU-01")

print(equipment.equipment_id)
print(equipment.temperature)
print(equipment.damper_position)
```

Output kya hoga?

---

**Next Lesson 14:** **Descriptors — `__get__`, `__set__`, `__delete__`**. Ye `@property` ke peeche ka aur deeper mechanism hai, aur isi concept se Python ke advanced frameworks samajhne ka foundation banta hai.

# Lesson 14: Descriptors — `__get__`, `__set__`, `__delete__`

Ab hum Python OOP ke **advanced object model** mein enter kar rahe hain.

Tumne previous lesson mein dekha:

```python
@property
def salary(self):
    return self._salary
```

Ab sawal:

> **`@property` internally kis mechanism se kaam karti hai?**

Iska jawab hai: **Descriptor Protocol**.

---

## 1. Descriptor kya hota hai?

Simple definition:

> **Descriptor aik object hota hai jo attribute access ko control karta hai.**

Yani:

```python
obj.x
```

par Python ko tum control kar sakte ho ke `x` ko **read**, **write**, ya **delete** kaise kiya jaye.

Descriptor ke main methods:

```python
__get__()
__set__()
__delete__()
```

---

# 2. Sabse basic descriptor

```python
class Descriptor:

    def __get__(self, instance, owner):
        print("GET")

    def __set__(self, instance, value):
        print("SET", value)
```

Ab:

```python
class Employee:

    salary = Descriptor()
```

Object:

```python
emp = Employee()
```

Jab:

```python
emp.salary
```

likhoge:

```text
GET
```

Aur:

```python
emp.salary = 5000
```

likhoge:

```text
SET 5000
```

Yani `salary` normal variable ki tarah behave nahi kar raha.

---

# 3. Descriptor ke 3 main methods

### `__get__`

Jab attribute **read** ho:

```python
emp.salary
```

to:

```python
__get__()
```

### `__set__`

Jab attribute **assign** ho:

```python
emp.salary = 5000
```

to:

```python
__set__()
```

### `__delete__`

Jab attribute delete ho:

```python
del emp.salary
```

to:

```python
__delete__()
```

Visual:

```text
          Descriptor
               |
       ┌───────┼────────┐
       ↓       ↓        ↓
     __get__  __set__  __delete__
       ↓       ↓        ↓
      READ    WRITE    DELETE
```

---

# 4. `instance` aur `owner` kya hain?

Ye important hai.

```python
def __get__(self, instance, owner):
```

Teen concepts:

```text
self      → descriptor object
instance  → jis object par access hua
owner     → jis class mein descriptor hai
```

Example:

```python
class Employee:
    salary = Descriptor()
```

Aur:

```python
emp = Employee()
```

Jab:

```python
emp.salary
```

hota hai:

```text
instance = emp
owner    = Employee
```

---

# 5. `owner` ko samjho

Agar:

```python
Employee.salary
```

access karo, to instance nahi hota.

Conceptually:

```python
instance = None
owner = Employee
```

Isliye descriptor mein aksar:

```python
if instance is None:
    return self
```

likha jata hai.

---

# 6. Practical descriptor — validation

Ab actual useful example.

Hum chahte hain salary:

* number ho
* negative na ho

Descriptor:

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
```

Employee:

```python
class Employee:

    salary = PositiveNumber()
```

Use:

```python
emp = Employee()

emp.salary = 5000

print(emp.salary)
```

Output:

```text
5000
```

Lekin:

```python
emp.salary = -100
```

par:

```text
ValueError
```

---

# 7. `__set_name__` kya hai?

Ye Python ka useful descriptor hook hai.

```python
def __set_name__(self, owner, name):
    self.name = name
```

Jab class create hoti hai, Python descriptor ko automatically batata hai:

> Tum kis naam se class mein assign hue ho?

Example:

```python
class Employee:

    salary = PositiveNumber()
```

Python descriptor ko bata sakta hai:

```text
owner = Employee
name = "salary"
```

Isliye:

```python
self.name = "salary"
```

ho jata hai.

---

# 8. Multiple fields

Ye descriptor ka real benefit hai.

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
            raise ValueError(
                f"{self.name} negative nahi ho sakta"
            )

        instance.__dict__[self.name] = value
```

Ab:

```python
class Employee:

    salary = PositiveNumber()
    bonus = PositiveNumber()
```

Use:

```python
emp = Employee()

emp.salary = 5000
emp.bonus = 1000

print(emp.salary)
print(emp.bonus)
```

Output:

```text
5000
1000
```

Ek hi descriptor class dono fields ke liye use ho rahi hai.

---

# 9. `instance.__dict__` kya hai?

Ye bhi important concept hai.

Normally object ka data roughly:

```python
emp.__dict__
```

mein hota hai.

Example:

```python
class Employee:

    def __init__(self):
        self.name = "Ali"
        self.salary = 5000
```

Then:

```python
print(emp.__dict__)
```

roughly:

```python
{
    "name": "Ali",
    "salary": 5000
}
```

Descriptor example mein hum manually:

```python
instance.__dict__[self.name] = value
```

use kar rahe hain.

Yani actual value object ke dictionary mein store kar rahe hain.

---

# 10. Descriptor vs `@property`

Ab important comparison.

### Property:

```python
class Employee:

    def __init__(self, salary):
        self._salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = value
```

### Descriptor:

```python
class PositiveNumber:

    def __get__(self, instance, owner):
        ...

    def __set__(self, instance, value):
        ...
```

Phir:

```python
class Employee:

    salary = PositiveNumber()
```

Dono attribute access control karte hain.

Lekin descriptor ko **multiple classes aur multiple attributes** ke liye reusable banaya ja sakta hai.

---

# 11. `property` khud descriptor hai

Ye sabse important connection hai.

Jab tum:

```python
@property
def salary(self):
    ...
```

likhte ho, Python `property` object create karta hai.

`property` descriptor protocol implement karta hai.

Conceptually:

```text
@property
   ↓
property object
   ↓
Descriptor behavior
   ↓
__get__ / __set__
```

Isliye previous lesson aur current lesson directly connected hain.

---

# 12. Data Descriptor vs Non-Data Descriptor

Ye thora advanced point hai.

### Data descriptor

Agar descriptor mein:

```python
__set__
```

ya:

```python
__delete__
```

ho, to woh **data descriptor** hota hai.

Example:

```python
class Descriptor:

    def __get__(self, instance, owner):
        ...

    def __set__(self, instance, value):
        ...
```

### Non-data descriptor

Agar sirf:

```python
__get__
```

ho:

```python
class Descriptor:

    def __get__(self, instance, owner):
        ...
```

to ye **non-data descriptor** hota hai.

---

# 13. Ye distinction kyun important hai?

Python attribute lookup mein priority hoti hai.

Simplified model:

```text
obj.attribute
      ↓
Data Descriptor?
      ↓
Yes → descriptor
      ↓
No
      ↓
instance.__dict__?
      ↓
Yes → instance value
      ↓
No
      ↓
Non-data descriptor?
      ↓
Yes → descriptor
      ↓
No
      ↓
Class attribute
```

Ye Python ke attribute lookup ka important part hai.

---

# 14. Simple example

Data descriptor:

```python
class D:

    def __get__(self, instance, owner):
        return "descriptor value"

    def __set__(self, instance, value):
        pass
```

Class:

```python
class Employee:

    salary = D()
```

Agar:

```python
emp.__dict__["salary"] = 9999
```

bhi manually kar do, data descriptor ki wajah se:

```python
emp.salary
```

descriptor ko priority mil sakti hai.

Ye reason hai ke data descriptors attribute access par strong control dete hain.

---

# 15. Descriptor ka practical use

Descriptors Python ke advanced systems mein use hote hain, jaise:

* `property`
* ORM fields
* validation frameworks
* lazy loading
* configuration systems
* type checking
* framework APIs

For example, ORM mein tum kuch aisa dekh sakte ho:

```python
class User:

    name = StringField()
    age = IntegerField()
```

Yahan:

```python
StringField()
IntegerField()
```

descriptor-based systems ho sakte hain.

---

# 16. HVAC example

Suppose equipment ka:

```text
Temperature
Pressure
Humidity
```

validate karna hai.

Descriptor:

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
            raise ValueError(
                f"{self.name} range se bahar hai"
            )

        instance.__dict__[self.name] = value
```

AHU:

```python
class AHU:

    temperature = RangeValue(-20, 60)
    humidity = RangeValue(0, 100)
```

Ab:

```python
ahu = AHU()

ahu.temperature = 22
ahu.humidity = 50
```

Valid.

Lekin:

```python
ahu.humidity = 150
```

Invalid.

Yahan descriptor ne common validation logic provide ki.

---

# 17. Is example ka main benefit

Agar 100 classes hain:

```text
AHU
VAV
FCU
Pump
Chiller
Boiler
```

aur sab mein range validation chahiye, tum same descriptor reuse kar sakte ho.

Instead of:

```python
@property
...
```

har class mein manually likhne ke.

Ye **code reuse through behavior** hai.

---

# 18. Descriptor ko mental model se samjho

Normal variable:

```text
obj.temperature
      ↓
stored value
```

Property:

```text
obj.temperature
      ↓
property
      ↓
getter
      ↓
value
```

Descriptor:

```text
obj.temperature
      ↓
descriptor
      ↓
__get__
      ↓
value
```

Aur:

```text
obj.temperature = 25
      ↓
descriptor
      ↓
__set__
      ↓
validation
      ↓
storage
```

---

# 19. OOP journey mein hum kahan hain?

Ab tak:

```text
Class/Object
    ↓
Attributes/Methods
    ↓
self / __init__
    ↓
Class variables
    ↓
classmethod / staticmethod
    ↓
Encapsulation
    ↓
Inheritance
    ↓
Polymorphism
    ↓
Abstraction
    ↓
Dunder methods
    ↓
Composition
    ↓
@property
    ↓
Attribute access
    ↓
Descriptors  ← Ab yahan
```

Ye ab **advanced Python OOP** territory hai.

---

## Practice

Is code ko samjho:

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
            raise ValueError("Negative allowed nahi")

        instance.__dict__[self.name] = value


class Employee:

    salary = PositiveNumber()
    bonus = PositiveNumber()
```

Ab:

```python
emp = Employee()

emp.salary = 5000
emp.bonus = 1000

print(emp.salary)
print(emp.bonus)
```

Expected:

```text
5000
1000
```

Aur:

```python
emp.salary = -500
```

par error aayega.

**Next Lesson 15:** **Context Managers — `with`, `__enter__`, `__exit__`**. Ye Python mein files, database connections, locks aur resources ko safely manage karne ke liye bohat important OOP concept hai.

# Lesson 15: Context Managers — `with`, `__enter__`, `__exit__`

Ab hum Python ke ek bohat practical OOP concept par hain:

> **Context Manager = resource ko safely open/use/close karna.**

Tumne Python mein ye syntax zaroor dekha hoga:

```python
with open("data.txt") as file:
    data = file.read()
```

Sawal ye hai:

**`with` actually karta kya hai?**

Iske peeche `__enter__()` aur `__exit__()` ka mechanism hota hai.

---

## 1. Problem samjho

Normally file:

```python
file = open("data.txt")

data = file.read()

file.close()
```

Yahan problem ye hai ke agar beech mein error aa jaye:

```python
file = open("data.txt")

data = file.read()

some_function_that_fails()

file.close()
```

Agar `some_function_that_fails()` exception throw kare, to `file.close()` execute nahi hoga.

Resource properly close nahi hua.

---

# 2. `with` is problem ko solve karta hai

```python
with open("data.txt") as file:
    data = file.read()
```

Python ensure karta hai ke context se bahar nikalte waqt cleanup mechanism execute ho.

Conceptually:

```text
with
 ↓
resource acquire
 ↓
code execute
 ↓
cleanup
```

Chahe code successfully complete ho ya exception aaye.

---

# 3. Context Manager kya hai?

Aisa object jo context-management protocol implement karta hai:

```python
__enter__()
__exit__()
```

Basic structure:

```python
class MyContext:

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_value, traceback):
        ...
```

Phir:

```python
with MyContext() as obj:
    ...
```

---

# 4. `__enter__()`

`with` block start hone par:

```python
__enter__()
```

execute hota hai.

Example:

```python
class Demo:

    def __enter__(self):
        print("Enter")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exit")
```

Use:

```python
with Demo() as obj:
    print("Inside")
```

Output:

```text
Enter
Inside
Exit
```

---

# 5. Flow samjho

```text
with Demo() as obj:
        ↓
Demo object create
        ↓
__enter__()
        ↓
obj ko value milti hai
        ↓
with block
        ↓
__exit__()
```

Yani:

```python
with Demo() as obj:
```

mein `obj` ko `__enter__()` ka return value milta hai.

---

# 6. `return self` kyun?

```python
def __enter__(self):
    print("Enter")
    return self
```

Is wajah se:

```python
with Demo() as obj:
```

mein:

```python
obj
```

actual `Demo` object hota hai.

Example:

```python
class Demo:

    def __enter__(self):
        return self

    def hello(self):
        print("Hello")

    def __exit__(self, exc_type, exc_value, traceback):
        pass
```

Ab:

```python
with Demo() as obj:
    obj.hello()
```

Output:

```text
Hello
```

---

# 7. `__exit__()` ke 3 parameters

Ye important hain:

```python
def __exit__(self, exc_type, exc_value, traceback):
```

### `exc_type`

Exception ki class/type.

Example:

```text
ValueError
TypeError
FileNotFoundError
```

### `exc_value`

Actual exception object/message.

Example:

```text
"Invalid temperature"
```

### `traceback`

Exception ka traceback information.

Mental model:

```text
exc_type
   ↓
Exception kis type ki hai?

exc_value
   ↓
Exception mein kya information hai?

traceback
   ↓
Error kahan/kaise hua?
```

---

# 8. Exception ke baghair

```python
class Demo:

    def __enter__(self):
        print("Start")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cleanup")
```

Use:

```python
with Demo():
    print("Work")
```

Output:

```text
Start
Work
Cleanup
```

`__exit__()` mein:

```python
exc_type
exc_value
traceback
```

normally `None` honge.

---

# 9. Exception ke saath

```python
class Demo:

    def __enter__(self):
        print("Start")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cleanup")
        print(exc_type)
        print(exc_value)
```

Use:

```python
with Demo():
    print("Work")
    raise ValueError("Something wrong")
```

Output roughly:

```text
Start
Work
Cleanup
<class 'ValueError'>
Something wrong
```

Notice:

**Exception ke bawajood `__exit__()` execute hua.**

Yahi context manager ka major purpose hai.

---

# 10. `__exit__()` exception ko suppress bhi kar sakta hai

Ye advanced aur important behavior hai.

Agar:

```python
__exit__()
```

`True` return kare:

```python
def __exit__(self, exc_type, exc_value, traceback):
    return True
```

to exception suppress ho sakti hai.

Example:

```python
class Demo:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exception handled")
        return True
```

Ab:

```python
with Demo():
    raise ValueError("Error")
```

Exception bahar propagate nahi hogi.

---

# 11. Agar `False` return karein?

```python
def __exit__(self, exc_type, exc_value, traceback):
    return False
```

to exception normally propagate hogi.

Normally cleanup karte hue exception ko suppress nahi karna ho to:

```python
return False
```

ya simply:

```python
return None
```

rakha ja sakta hai.

---

# 12. `with open()` ka connection

Ab famous example:

```python
with open("data.txt") as file:
    data = file.read()
```

`file` object context-management protocol support karta hai.

Conceptually:

```text
with open(...)
       ↓
__enter__()
       ↓
file object
       ↓
read/write
       ↓
__exit__()
       ↓
file cleanup/close
```

Isi wajah se `with` files ke liye itna useful hai.

---

# 13. Apna file-like context manager

Simple demonstration:

```python
class MyFile:

    def __enter__(self):
        print("File opened")
        return self

    def write(self, text):
        print("Writing:", text)

    def __exit__(self, exc_type, exc_value, traceback):
        print("File closed")
```

Use:

```python
with MyFile() as file:
    file.write("Hello")
```

Output:

```text
File opened
Writing: Hello
File closed
```

---

# 14. Real-world HVAC example

Context manager ka concept equipment/resource handling mein bhi samajh sakte ho.

Suppose kisi system ka connection open karna hai:

```python
class HVACConnection:

    def __enter__(self):
        print("HVAC connection opened")
        return self

    def read_point(self, point):
        print("Reading:", point)

    def __exit__(self, exc_type, exc_value, traceback):
        print("HVAC connection closed")
```

Use:

```python
with HVACConnection() as connection:

    connection.read_point("AHU-01.Temperature")
    connection.read_point("AHU-01.Damper")
```

Output:

```text
HVAC connection opened
Reading: AHU-01.Temperature
Reading: AHU-01.Damper
HVAC connection closed
```

Yahan:

```text
open connection
      ↓
use connection
      ↓
close connection
```

automatically managed hai.

---

# 15. Context managers kahan use hote hain?

Common examples:

### Files

```python
with open(...) as file:
```

### Database

```python
with database_connection:
    ...
```

### Locks / threading

```python
with lock:
    ...
```

### Network resources

```python
with connection:
    ...
```

### Temporary resources

```python
with temporary_resource:
    ...
```

Core idea same:

> **Acquire → Use → Release**

---

# 16. Context Manager ka mental model

Isko yaad rakho:

```text
             with
              |
              ↓
        __enter__()
              |
              ↓
        Resource ready
              |
              ↓
         Your code
              |
              ↓
        __exit__()
              |
              ↓
          Cleanup
```

---

# 17. `as obj` kya karta hai?

Ye line:

```python
with Demo() as obj:
```

ka matlab roughly:

```text
Demo()
   ↓
__enter__()
   ↓
return value
   ↓
obj
```

Agar:

```python
def __enter__(self):
    return 123
```

to:

```python
with Demo() as obj:
    print(obj)
```

Output:

```text
123
```

`obj` zaroori nahi ke `self` ho.

---

# 18. Context manager ka simplified equivalent

Conceptually `with` ko kuch is tarah imagine kar sakte ho:

```python
manager = Demo()

obj = manager.__enter__()

try:
    # with block
    print("Work")

finally:
    manager.__exit__(None, None, None)
```

Exception ho to `__exit__()` ko exception information di jati hai.

Ye exact language-level implementation nahi, balkay **mental model** hai.

---

# 19. `try/finally` se relation

Context managers ka major benefit:

```python
try:
    resource = acquire()
    use(resource)
finally:
    release(resource)
```

ko reusable object protocol mein convert karna.

Instead of har jagah:

```python
try:
    ...
finally:
    ...
```

tum:

```python
with Resource() as resource:
    ...
```

likh sakte ho.

---

# 20. Context manager + OOP

Yahan tumhari OOP learning connect hoti hai:

```text
Class
  ↓
Object
  ↓
Methods
  ↓
Dunder methods
  ↓
__enter__
__exit__
  ↓
Context Manager
```

`__enter__` aur `__exit__` **dunder methods** hain.

---

# 21. Practice

Is class ko complete karo:

```python
class Database:

    def __enter__(self):
        print("Database connected")
        return self

    def query(self, sql):
        print("Running:", sql)

    def __exit__(self, exc_type, exc_value, traceback):
        print("Database disconnected")
```

Phir:

```python
with Database() as db:
    db.query("SELECT * FROM equipment")
```

Expected:

```text
Database connected
Running: SELECT * FROM equipment
Database disconnected
```

### Practice question

Agar `query()` ke andar:

```python
raise ValueError("Query failed")
```

aa jaye, to kya:

```text
Database disconnected
```

phir bhi print hoga?

**Haan.** `__exit__()` cleanup ke liye execute hota hai, exception ho ya na ho.

---

### Next Lesson 16

**`__new__()` vs `__init__()` — object actually create kaise hota hai?**

Is lesson mein hum dekhenge:

```text
Class()
  ↓
__new__()
  ↓
object create
  ↓
__init__()
  ↓
object initialize
```

Aur phir **Singleton, immutable objects, aur object creation control** ka concept samjhenge.

# Lesson 16: `__new__()` vs `__init__()`

Ab hum Python mein **object creation** ka actual process samjhenge.

Ab tak hum `__init__()` jaante hain:

```python
class Employee:

    def __init__(self, name):
        self.name = name
```

Lekin important question:

> `self` object aaya kahan se?

Yahan `__new__()` ka role aata hai.

---

## 1. Basic difference

Yaad rakho:

```text
__new__()
   ↓
Object CREATE karta hai

__init__()
   ↓
Object INITIALIZE karta hai
```

Yani:

> `__new__` = object banana
> `__init__` = bane hue object ko configure karna

---

# 2. Normal object creation

Jab tum likhte ho:

```python
emp = Employee("Ali")
```

simplified flow:

```text
Employee("Ali")
      ↓
__new__()
      ↓
Object create
      ↓
__init__()
      ↓
name = "Ali"
      ↓
emp
```

---

# 3. `__new__()` example

```python
class Employee:

    def __new__(cls, name):
        print("__new__ called")
        return super().__new__(cls)

    def __init__(self, name):
        print("__init__ called")
        self.name = name
```

Ab:

```python
emp = Employee("Ali")
```

Output:

```text
__new__ called
__init__ called
```

Notice:

**`__new__()` pehle execute hua.**

---

# 4. `cls` kyun hai?

`__new__()` normally:

```python
def __new__(cls, ...):
```

leta hai.

Yahan:

```text
self → object
cls  → class
```

Lekin `__new__()` object create hone se **pehle** execute hota hai.

Isliye uske paas `self` nahi hota.

Uske paas class hoti hai:

```python
cls
```

---

# 5. `__init__()` mein `self`

`__new__()` object create kar deta hai.

Uske baad Python us object ko `__init__()` mein deta hai:

```python
def __init__(self, name):
```

Yahan:

```text
self = newly created object
```

So:

```text
__new__
  ↓
new object
  ↓
self
  ↓
__init__
```

---

# 6. `__new__()` ka return value

Ye bohat important hai.

`__new__()` ko normally **object return karna hota hai**.

Example:

```python
class Employee:

    def __new__(cls):
        obj = super().__new__(cls)
        return obj
```

`super().__new__(cls)` actual object create karta hai.

---

# 7. Agar `__new__()` object return na kare?

Example:

```python
class Employee:

    def __new__(cls):
        print("Creating")
        return None

    def __init__(self):
        print("Initializing")
```

Ab:

```python
emp = Employee()
```

`__new__()`:

```python
return None
```

karta hai.

Isliye normal `__init__()` call nahi hota.

Yani:

```text
__new__
  ↓
None
  ↓
__init__ skipped
```

Ye demonstrate karta hai ke `__new__()` object creation ko control karta hai.

---

# 8. `__new__()` aur immutable types

`__new__()` ka important real-world use **immutable objects** ke saath hai.

Python ke kuch objects immutable hain:

```text
int
float
str
tuple
```

Example:

```python
x = 10
```

Tum existing integer object ko internally modify nahi karte.

New value ke liye new object create hota hai.

Isi liye immutable subclasses mein `__new__()` useful hota hai.

---

# 9. Example: custom integer

```python
class PositiveInt(int):

    def __new__(cls, value):
        if value < 0:
            raise ValueError("Negative value allowed nahi")

        return super().__new__(cls, value)
```

Ab:

```python
x = PositiveInt(10)

print(x)
```

Output:

```text
10
```

Lekin:

```python
x = PositiveInt(-5)
```

par:

```text
ValueError
```

Yahan validation object creation ke stage par ho rahi hai.

---

# 10. `__init__()` kyun nahi?

Kyuki `int` immutable hai.

Agar object banne ke baad uski underlying value modify nahi kar sakte, to validation/value creation ka kaam `__new__()` mein karna logical hai.

Mental model:

```text
Immutable object

value
 ↓
__new__()
 ↓
object created with that value
```

---

# 11. String example

```python
class MyString(str):

    def __new__(cls, value):
        print("Creating string")
        return super().__new__(cls, value)
```

Use:

```python
text = MyString("Hello")

print(text)
```

Output:

```text
Creating string
Hello
```

Yahan bhi `str` immutable hai.

---

# 12. `__new__()` ka ek famous use: Singleton

Ab ek advanced concept.

**Singleton** ka idea:

> Class se multiple calls hon, lekin same object return ho.

Example:

```python
class Singleton:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
```

Ab:

```python
a = Singleton()
b = Singleton()
```

Check:

```python
print(a is b)
```

Output:

```text
True
```

Dono variables **same object** ko reference kar rahe hain.

---

# 13. Normal class mein kya hota?

Normally:

```python
class Employee:
    pass

a = Employee()
b = Employee()

print(a is b)
```

Output:

```text
False
```

Har call par new object.

```text
a → Employee object #1

b → Employee object #2
```

Singleton:

```text
a ─┐
   ├──→ same Employee/Singleton object
b ─┘
```

---

# 14. `is` vs `==`

Yahan ye distinction important hai.

### `==`

Values compare karta hai.

```python
a == b
```

### `is`

Identity compare karta hai.

```python
a is b
```

Singleton mein:

```python
a is b
```

`True` ka matlab:

> dono same object hain.

---

# 15. `__new__()` + `__init__()` Singleton issue

Ek subtle point:

```python
a = Singleton()
b = Singleton()
```

Har call par:

```text
__new__()
```

run hoga.

Aur agar object return hua:

```text
__init__()
```

bhi run ho sakta hai.

Yani same object hone ke bawajood initialization multiple times ho sakti hai.

Isliye real Singleton implementation mein `__init__` ko carefully handle karna padta hai.

---

# 16. Example

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
```

Ab:

```python
a = Singleton()
b = Singleton()
```

Output roughly:

```text
Creating object
Initializing
Initializing
```

Notice:

Object sirf **ek baar create** hua.

Lekin `__init__()` do baar run hua.

Ye distinction bohat important hai.

---

# 17. Object creation vs initialization

Isko strongly yaad rakho:

### `__new__`

```text
"Object mujhe banana hai."
```

### `__init__`

```text
"Object ban chuka hai, ab uski values set karni hain."
```

Example:

```python
class Employee:

    def __new__(cls, name):
        print("Object create ho raha hai")
        return super().__new__(cls)

    def __init__(self, name):
        print("Object initialize ho raha hai")
        self.name = name
```

---

# 18. Complete flow

Jab:

```python
emp = Employee("Ali")
```

execute hota hai:

```text
Employee("Ali")
      │
      ▼
   __new__
      │
      ▼
Object allocated
      │
      ▼
   __init__
      │
      ▼
self.name = "Ali"
      │
      ▼
      emp
```

---

# 19. Ek important misconception

Ye mat samajhna:

```text
__new__ = constructor
__init__ = constructor
```

Strictly speaking Python terminology mein:

* `__new__()` object **create/construct** karta hai.
* `__init__()` existing object ko **initialize** karta hai.

Isi liye `__init__()` ko technically object creation method kehna accurate nahi hai.

---

# 20. `__new__()` kab use karna chahiye?

Normal classes mein aksar tumhein `__new__()` ki zaroorat **nahi** hoti.

Mostly:

```python
class Employee:

    def __init__(self, name):
        self.name = name
```

enough hai.

`__new__()` useful ho sakta hai:

* immutable types subclass karte waqt
* object creation control karna ho
* Singleton/flyweight patterns
* metaprogramming
* advanced framework/library development
* special object allocation behavior

---

# 21. `__new__()` aur `classmethod` ka relation

Dono mein `cls` dekh kar confusion ho sakti hai.

### `classmethod`

```python
@classmethod
def create(cls, ...):
```

Existing class ko use karke object create karne ka **alternative interface** de sakta hai.

### `__new__`

```python
def __new__(cls, ...):
```

Actual object creation process ko customize karta hai.

Yani:

```text
classmethod
    ↓
alternative constructor/interface

__new__
    ↓
actual object creation mechanism
```

---

# 22. Ek practical comparison

| Method         | Role                                         |
| -------------- | -------------------------------------------- |
| `__new__()`    | Object create karta hai                      |
| `__init__()`   | Object initialize karta hai                  |
| `@classmethod` | Class-based method / alternative constructor |
| `__str__()`    | Human-readable representation                |
| `__repr__()`   | Developer-oriented representation            |
| `__enter__()`  | Context start                                |
| `__exit__()`   | Context cleanup                              |

Ab tumhare dunder methods ka ecosystem connect hona start ho raha hai.

---

# 23. Practice

Is code ka output predict karo:

```python
class Test:

    def __new__(cls):
        print("NEW")
        return super().__new__(cls)

    def __init__(self):
        print("INIT")


obj = Test()
```

Output:

```text
NEW
INIT
```

Kyun?

```text
Test()
 ↓
__new__()
 ↓
object create
 ↓
__init__()
 ↓
object initialize
```

---

## Ek aur practice

```python
class Test:

    def __new__(cls):
        print("NEW")
        return None

    def __init__(self):
        print("INIT")


obj = Test()
```

Output:

```text
NEW
```

`INIT` nahi chalega, kyunki `__new__()` ne actual `Test` instance return nahi kiya.

---

# OOP journey update

Ab tak hum:

```text
Class / Object
      ↓
Attributes / Methods
      ↓
self / __init__
      ↓
classmethod / staticmethod
      ↓
Encapsulation
      ↓
Inheritance
      ↓
Polymorphism
      ↓
Abstraction
      ↓
Dunder Methods
      ↓
Composition
      ↓
@property
      ↓
Attribute Lookup
      ↓
Descriptors
      ↓
Context Managers
      ↓
__new__ vs __init__  ← Yahan
```

**Next Lesson 17:** **Metaclasses — `type`, class bhi object hai, aur Python class ko create kaise karta hai.** Ye OOP ka advanced level hai aur `type`, `__class__`, aur custom class creation ko connect karega.

# Lesson 17: Metaclasses — `type`, Class bhi Object Hai

Ab hum Python OOP ke **advanced level** mein enter kar rahe hain.

Pehle ek important concept:

> Python mein **class khud bhi ek object hoti hai**.

Ye samajh aa gaya to metaclass ka concept kaafi easy ho jata hai.

---

## 1. Ab tak hum class ko kya samajhte thay?

Example:

```python
class Employee:
    pass
```

Phir:

```python
emp = Employee()
```

Hum kehte hain:

```text
Employee = class
emp      = object
```

Lekin Python mein picture thori deeper hai:

```text
Employee
   ↓
class ka object
```

Yani `Employee` khud bhi kisi class ka instance hai.

---

# 2. `type()` se check karo

```python
class Employee:
    pass

emp = Employee()

print(type(emp))
print(type(Employee))
```

Output:

```text
<class '__main__.Employee'>
<class 'type'>
```

Pehli line:

```python
type(emp)
```

batati hai:

> `emp` kis class ka object hai?

Answer:

```text
Employee
```

Dusri:

```python
type(Employee)
```

batati hai:

> `Employee` khud kis class ka object hai?

Answer:

```text
type
```

---

# 3. Ye important relationship hai

```text
emp
 ↓
Employee
 ↓
type
```

Yani:

```text
emp is instance of Employee

Employee is instance of type
```

Code:

```python
isinstance(emp, Employee)
```

→ `True`

Aur:

```python
isinstance(Employee, type)
```

→ `True`

---

# 4. `type` kya hai?

`type` Python ki built-in class hai.

Hum normally:

```python
type(10)
```

karte hain.

Output:

```text
<class 'int'>
```

Lekin `type` sirf type check karne ke liye nahi hai.

**`type` classes create bhi kar sakta hai.**

Ye bohat important hai.

---

# 5. Class manually `type()` se banana

Normally:

```python
class Employee:
    pass
```

Lekin isi tarah ka class object `type()` se dynamically bana sakte ho:

```python
Employee = type(
    "Employee",
    (),
    {}
)
```

Ab:

```python
emp = Employee()

print(type(emp))
```

Output:

```text
<class '__main__.Employee'>
```

Yani class dynamically create ho gayi.

---

# 6. `type()` ke 3 arguments

Ye:

```python
type(
    "Employee",
    (),
    {}
)
```

mein:

### First

```python
"Employee"
```

Class ka naam.

### Second

```python
()
```

Base classes.

### Third

```python
{}
```

Class namespace/dictionary.

So:

```text
type(name, bases, namespace)
```

---

# 7. Simple example with attribute

```python
Employee = type(
    "Employee",
    (),
    {
        "company": "ABC"
    }
)
```

Ab:

```python
emp = Employee()

print(emp.company)
```

Output:

```text
ABC
```

Yani `type()` se class create karte waqt class ke attributes bhi provide kar sakte ho.

---

# 8. Method bhi add kar sakte ho

```python
def show(self):
    print("Employee:", self.name)


Employee = type(
    "Employee",
    (),
    {
        "name": "Ali",
        "show": show
    }
)
```

Ab:

```python
emp = Employee()

print(emp.name)
emp.show()
```

Output:

```text
Ali
Employee: Ali
```

---

# 9. Lekin normally aisa kyun nahi karte?

Tum soch sakte ho:

> Agar `type()` se class bana sakte hain to `class` keyword kyun use karte hain?

Normal development mein:

```python
class Employee:
    ...
```

zyada readable aur maintainable hai.

`type()` dynamic class creation ke special cases mein useful hota hai.

---

# 10. Ab Metaclass

Ab main definition:

> **Metaclass wo class hoti hai jo classes ko create/control karti hai.**

Normal relationship:

```text
Object
   ↓
Class
   ↓
Metaclass
```

Python mein normally:

```text
object → Employee → type
```

Yahan:

```text
Employee
    ↓
instance of
    ↓
type
```

So:

> **`type` Python ki default metaclass hai.**

---

# 11. Simple mental model

Normal class:

```text
Employee
   ↓ creates
emp
```

Metaclass:

```text
type
   ↓ creates
Employee
```

So:

```text
type → Employee → emp
```

Isko yaad rakho:

> **Class objects banati hai. Metaclass classes banati hai.**

---

# 12. Custom metaclass

Ab simple example:

```python
class MyMeta(type):

    def __new__(cls, name, bases, namespace):
        print("Class create ho rahi hai:", name)

        return super().__new__(
            cls,
            name,
            bases,
            namespace
        )
```

Ab:

```python
class Employee(metaclass=MyMeta):
    pass
```

Output:

```text
Class create ho rahi hai: Employee
```

Interesting baat:

`Employee` ka instance abhi bana bhi nahi.

Sirf **class create** hui hai.

---

# 13. Flow

Jab tum:

```python
class Employee(metaclass=MyMeta):
    pass
```

likhte ho:

```text
Python class body
      ↓
MyMeta
      ↓
__new__()
      ↓
Employee class object
```

Phir:

```python
emp = Employee()
```

alag process hai:

```text
Employee
   ↓
instance creation
   ↓
emp
```

---

# 14. Metaclass `__new__()`

Tumne previous lesson mein normal class ka:

```python
__new__()
```

dekha tha.

Yahan bhi `__new__()` hai, lekin level different hai.

Normal class:

```python
class Employee:

    def __new__(cls):
        ...
```

Ye **Employee ke instances** ke creation ko control karta hai.

Metaclass:

```python
class MyMeta(type):

    def __new__(cls, name, bases, namespace):
        ...
```

Ye **classes** ke creation ko control karta hai.

---

# 15. Compare karo

```text
Normal __new__
    ↓
Employee object create

Metaclass __new__
    ↓
Employee class create
```

Ye distinction bohat important hai.

---

# 16. Metaclass mein `name`, `bases`, `namespace`

Ye:

```python
def __new__(cls, name, bases, namespace):
```

mein:

### `name`

Class ka naam:

```text
Employee
```

### `bases`

Parent classes:

```python
(Equipment,)
```

### `namespace`

Class ke andar defined attributes/methods:

```python
{
    "__module__": ...,
    "__qualname__": ...,
    "salary": ...,
    "show": ...
}
```

---

# 17. Example

```python
class MyMeta(type):

    def __new__(cls, name, bases, namespace):

        print("Name:", name)
        print("Bases:", bases)
        print("Attributes:", list(namespace.keys()))

        return super().__new__(
            cls,
            name,
            bases,
            namespace
        )
```

Ab:

```python
class Employee(metaclass=MyMeta):

    company = "ABC"

    def show(self):
        print("Hello")
```

Conceptually output mein kuch aisa milega:

```text
Name: Employee
Bases: ()
Attributes: ['__module__', '__qualname__', 'company', 'show']
```

---

# 18. Metaclass ka practical use

Metaclasses powerful hain, lekin normal application code mein har jagah use nahi karni chahiye.

Examples jahan metaclasses useful ho sakti hain:

* ORM frameworks
* validation frameworks
* plugin systems
* automatic class registration
* API/framework design
* declarative configuration
* class-level constraints

---

# 19. Automatic registration example

Suppose hum chahte hain ke jitni bhi equipment classes banengi, woh automatically registry mein add ho jayein.

```python
registry = {}
```

Metaclass:

```python
class EquipmentMeta(type):

    def __new__(cls, name, bases, namespace):

        new_class = super().__new__(
            cls,
            name,
            bases,
            namespace
        )

        registry[name] = new_class

        return new_class
```

Ab:

```python
class AHU(metaclass=EquipmentMeta):
    pass


class VAV(metaclass=EquipmentMeta):
    pass
```

Registry:

```python
print(registry)
```

mein `AHU` aur `VAV` classes register ho sakti hain.

Yani class create hote hi automatic action perform ho gaya.

---

# 20. Metaclass vs Decorator

Ye dono confuse ho sakte hain.

Class decorator:

```python
@my_decorator
class Employee:
    pass
```

Class create hone ke baad class ko modify/wrap kar sakta hai.

Metaclass:

```python
class Employee(metaclass=MyMeta):
    pass
```

Class creation process ko deeper level par control karti hai.

Simple mental model:

```text
Decorator
    ↓
Class ko modify/wrap

Metaclass
    ↓
Class creation control
```

---

# 21. Metaclass vs inheritance

Ye bhi different concepts hain.

Inheritance:

```python
class AHU(Equipment):
```

Relationship:

```text
AHU IS-A Equipment
```

Metaclass:

```python
class AHU(metaclass=EquipmentMeta):
```

Ye nahi keh raha:

```text
AHU IS-A EquipmentMeta
```

Balkay:

```text
AHU is an instance of EquipmentMeta
```

Ye class-level relationship hai.

---

# 22. `type` ka interesting point

Hum likhte hain:

```python
class Employee:
    pass
```

Python internally class object create karta hai.

Default case mein roughly:

```text
metaclass = type
```

So conceptually:

```python
Employee = type(
    "Employee",
    (),
    {...}
)
```

Actual class statement ka process is se zyada detailed hai, lekin learning ke liye ye useful mental model hai.

---

# 23. `__class__`

Har instance ke paas apni class ka reference hota hai:

```python
emp.__class__
```

Example:

```python
class Employee:
    pass

emp = Employee()

print(emp.__class__)
```

Output:

```text
<class '__main__.Employee'>
```

Ye roughly:

```python
type(emp)
```

ke equivalent result deta hai.

---

# 24. Class ka class

Ab:

```python
print(Employee.__class__)
```

Output:

```text
<class 'type'>
```

Yani:

```text
emp.__class__
    ↓
Employee

Employee.__class__
    ↓
type
```

Aur:

```python
type(Employee)
```

bhi:

```text
type
```

---

# 25. Complete picture

Is diagram ko yaad karo:

```text
                type
                 │
                 │ creates
                 ▼
             Employee
                 │
                 │ creates
                 ▼
                emp
```

Aur relationships:

```text
emp
 ↓ is instance of
Employee
 ↓ is instance of
type
```

Ye Python object model ka fundamental concept hai.

---

# 26. Important: `type` khud kis ka instance hai?

Interesting question:

```python
type(type)
```

Output:

```text
<class 'type'>
```

Yani `type` khud ka instance bhi `type` hai.

Isko initially strange lag sakta hai.

Is level par Python ka object model deliberately self-referential structure rakhta hai.

Tumhein abhi isko memorize karne ki zaroorat nahi. Bas relationship samjho:

```text
object → class → metaclass
```

aur default metaclass:

```text
type
```

---

# 27. Kab metaclass use karni hai?

Beginner/normal application code mein:

```text
❌ Har problem ke liye metaclass nahi
```

Pehle:

```text
1. Normal class
2. Composition
3. Inheritance
4. Decorator
5. Descriptor
```

consider karo.

Metaclass tab use karo jab **class creation itself** ko customize karna genuinely required ho.

---

# 28. OOP journey

Ab hum yahan tak aa gaye:

```text
Class / Object
      ↓
Attributes / Methods
      ↓
self / __init__
      ↓
classmethod / staticmethod
      ↓
Encapsulation
      ↓
Inheritance
      ↓
Polymorphism
      ↓
Abstraction
      ↓
Dunder Methods
      ↓
Composition
      ↓
@property
      ↓
Attribute Lookup
      ↓
Descriptors
      ↓
Context Managers
      ↓
__new__ / __init__
      ↓
Metaclasses ← Yahan
```

### Core idea

```text
Object
  ↓
created by
  ↓
Class
  ↓
created by
  ↓
Metaclass
```

Aur Python ka default metaclass:

```python
type
```

**Next Lesson 18:** **Abstract Base Classes vs Protocols — `ABC` aur `Protocol` mein actual difference**, including structural typing, duck typing, `@runtime_checkable`, aur tumhare pehle wale `Protocol` wale question se direct connection.

# Lesson 18: ABC vs Protocol — `ABC` aur `Protocol` mein kya difference hai?

Ye lesson tumhare pehle wale question **“Protocol interface ki tarah kaam karta hai?”** ka deeper answer hai.

Python mein do important approaches hain:

1. **ABC — Abstract Base Class**
2. **Protocol — Structural Typing**

Dono ka purpose similar lag sakta hai, lekin approach different hai.

---

## 1. ABC kya tha?

Humne pehle dekha:

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

Yahan `AHU` ko explicitly:

```python
Equipment
```

se inherit karna padega.

```text
Equipment
    ↑
    |
   AHU
```

---

# 2. ABC ka main concept

ABC kehta hai:

> "Agar tum mere type/category ke member banna chahte ho, to mujh se inherit karo aur required methods implement karo."

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

Ab:

```python
class AHU(Equipment):

    def start(self):
        print("AHU ON")

    def stop(self):
        print("AHU OFF")
```

AHU properly `Equipment` hierarchy ka part hai.

---

# 3. Protocol ka approach different hai

Protocol kehta hai:

> "Tum mujh se inherit karo ya na karo, agar tum required structure/behavior provide karte ho to tum is interface ko satisfy karte ho."

Example:

```python
from typing import Protocol

class Equipment(Protocol):

    def start(self) -> None:
        ...
```

Ab ek class:

```python
class AHU:

    def start(self):
        print("AHU ON")
```

Notice:

```python
class AHU:
```

ne `Equipment` se inherit nahi kiya.

Phir bhi type checker ke perspective se:

```text
AHU
 ↓
has start()
 ↓
Equipment Protocol ko satisfy karta hai
```

---

# 4. Isko structural typing kehte hain

Protocol ka core concept:

> **Structural typing**

Matlab:

```text
"What you ARE"
```

se zyada:

```text
"What you CAN DO"
```

important hai.

Example:

```python
class AHU:
    def start(self):
        print("AHU ON")


class VAV:
    def start(self):
        print("VAV ON")
```

Dono ke paas:

```python
start()
```

hai.

To ek function:

```python
def start_equipment(equipment: Equipment):
    equipment.start()
```

ko dono objects diye ja sakte hain.

```python
start_equipment(AHU())
start_equipment(VAV())
```

---

# 5. ABC vs Protocol

| Feature                    | ABC                                  | Protocol                                 |
| -------------------------- | ------------------------------------ | ---------------------------------------- |
| Inheritance                | Usually required                     | Required nahi                            |
| Typing style               | Nominal                              | Structural                               |
| Main idea                  | "Tum meri hierarchy ka part ho"      | "Tum required behavior provide karte ho" |
| Shared implementation      | Easily possible                      | Usually interface-focused                |
| Abstract methods           | Yes                                  | Method signatures define kar sakta hai   |
| Runtime enforcement        | Abstract class instantiate nahi hoti | Mainly static type checking              |
| Existing unrelated classes | Adapt karna pad sakta hai            | Directly compatible ho sakti hain        |

---

# 6. Nominal typing vs Structural typing

Ye sabse important difference hai.

### ABC → Nominal

```python
class Animal(ABC):
    ...
```

Aur:

```python
class Dog(Animal):
    ...
```

Relationship explicitly declared hai.

```text
Dog IS-A Animal
```

---

### Protocol → Structural

```python
class Flyable(Protocol):

    def fly(self) -> None:
        ...
```

Ab:

```python
class Bird:

    def fly(self):
        print("Flying")
```

Bird ne:

```python
Flyable
```

se inherit nahi kiya.

Lekin structure match karta hai.

```text
Bird
 ↓
has fly()
 ↓
satisfies Flyable
```

---

# 7. Ye duck typing se related hai

Python mein famous concept hai:

> **If it walks like a duck and quacks like a duck, treat it like a duck.**

Example:

```python
def start(obj):
    obj.start()
```

Python ko zaroori nahi ke:

```python
obj
```

exactly kisi particular class ka ho.

Bas uske paas:

```python
start()
```

hona chahiye.

Ye runtime duck typing hai.

Protocol isi idea ko **static type checking** ke saath formalize karta hai.

---

# 8. Protocol ka practical example

```python
from typing import Protocol


class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab:

```python
class AHU:

    def start(self) -> None:
        print("AHU started")
```

Aur:

```python
class Pump:

    def start(self) -> None:
        print("Pump started")
```

Function:

```python
def run_equipment(equipment: Startable):
    equipment.start()
```

Ab:

```python
run_equipment(AHU())
run_equipment(Pump())
```

Dono compatible hain.

---

# 9. `...` ka kya matlab?

Protocol mein tum dekhoge:

```python
def start(self) -> None:
    ...
```

Ye implementation nahi hai.

Yahan:

```python
...
```

ellipsis hai.

Conceptually:

> "Is interface mein `start()` method required hai."

Implementation actual class mein hogi.

---

# 10. Protocol ko interface samajh sakte ho?

**Haan, practical learning ke liye Protocol ko Python ka interface-like mechanism samajh sakte ho.**

Lekin technically:

```text
Protocol ≠ traditional Java/C# interface
```

Python ka type system structural typing use kar sakta hai through Protocol.

---

# 11. `@runtime_checkable`

Normally Protocol ka main purpose static type checking hai.

Lekin kuch protocols ko runtime par check bhi kar sakte ho.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab:

```python
class AHU:

    def start(self):
        print("AHU ON")
```

Check:

```python
ahu = AHU()

print(isinstance(ahu, Startable))
```

Ye `True` ho sakta hai.

---

# 12. Lekin runtime check limited hai

Important:

```python
isinstance(ahu, Startable)
```

mainly check karta hai ke required members available hain.

Ye ABC jaisa complete behavioral validation system nahi hai.

Example:

```python
class AHU:

    def start(self):
        return "wrong behavior"
```

Protocol runtime check ye guarantee nahi karta ke method logically sahi kaam kar raha hai.

Sirf structural requirement important hai.

---

# 13. Protocol mein attributes bhi define kar sakte ho

Example:

```python
from typing import Protocol


class Equipment(Protocol):

    equipment_id: str
    temperature: float

    def start(self) -> None:
        ...
```

Ab koi class:

```python
class AHU:

    equipment_id = "AHU-01"
    temperature = 22.5

    def start(self):
        print("AHU started")
```

Structure satisfy karti hai.

---

# 14. Read-only property bhi

Protocol:

```python
class Sensor(Protocol):

    @property
    def temperature(self) -> float:
        ...
```

Ab koi object agar:

```python
@property
def temperature(self):
    return 22.5
```

provide karta hai, to structure compatible ho sakta hai.

---

# 15. ABC ka strong point

ABC tab useful hai jab tum **common implementation** bhi dena chahte ho.

Example:

```python
from abc import ABC, abstractmethod


class Equipment(ABC):

    def log(self):
        print("Equipment log created")

    @abstractmethod
    def start(self):
        pass
```

Child:

```python
class AHU(Equipment):

    def start(self):
        print("AHU started")
```

AHU ko automatically:

```python
log()
```

mil gaya.

Yani ABC:

```text
Interface
+
Common behavior
+
Inheritance hierarchy
```

provide kar sakta hai.

---

# 16. Protocol ka strong point

Protocol particularly useful hai jab tumhare paas **existing unrelated classes** hon.

Suppose:

```python
class HoneywellAHU:
    def start(self):
        print("Honeywell AHU")


class SiemensAHU:
    def start(self):
        print("Siemens AHU")
```

Dono classes tumhari control mein nahi bhi ho sakti.

Tum unko force nahi karna chahte:

```python
class HoneywellAHU(Equipment):
```

Protocol mein requirement simple hai:

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Agar classes `start()` provide karti hain, typing perspective se compatible ho sakti hain.

---

# 17. Python mein Protocol kyun powerful hai?

Suppose tumhari function ko actually ye nahi chahiye:

```text
Employee
AHU
VAV
Pump
Motor
```

Usko sirf chahiye:

```text
start()
```

To tum function ko unnecessarily kisi concrete class se tie nahi karte.

Instead:

```python
def start_equipment(obj: Startable):
    obj.start()
```

Ye **loose coupling** create karta hai.

---

# 18. ABC vs Protocol — mental model

### ABC

```text
"Come into my family."

        Equipment
             ↑
             |
            AHU
```

### Protocol

```text
"I don't care which family you belong to.
Just provide these capabilities."

AHU  ──┐
VAV  ──┼──> start()
Pump ──┘
```

---

# 19. Tumhare Python project mein iska use

Agar tumhare code mein:

```python
class Cell:
    ...
```

aur different objects ko kisi common behavior ki requirement hai, for example:

```python
read()
write()
validate()
```

to Protocol useful ho sakta hai.

Example:

```python
from typing import Protocol


class Readable(Protocol):

    def read(self) -> str:
        ...
```

Ab:

```python
class Cell:

    def read(self) -> str:
        return "data"
```

Function:

```python
def process(obj: Readable):
    value = obj.read()
    print(value)
```

`Cell` ko `Readable` se explicitly inherit karna zaroori nahi.

---

# 20. ABC kab aur Protocol kab?

Simple rule:

```text
ABC
↓
Jab inheritance hierarchy + shared implementation chahiye
```

```text
Protocol
↓
Jab behavior/interface define karna hai
aur inheritance force nahi karni
```

Aur:

```text
Duck typing
↓
Runtime par simply method call karna hai
```

---

## Final mental model

```text
ABC
│
├── Nominal typing
├── Explicit inheritance
├── Abstract methods
└── Shared implementation possible


Protocol
│
├── Structural typing
├── Inheritance required nahi
├── Behavior/interface define
└── Static type checking ke liye powerful


Duck Typing
│
└── "Object ke paas required method hai?
    To use kar lo."
```

### Ek line mein:

> **ABC kehta hai: "Tum meri hierarchy ka member ho."**
> **Protocol kehta hai: "Tumhare paas required behavior hai, mujhe inheritance ki parwah nahi."**

**Next Lesson 19:** `Generic`, `TypeVar` aur `Generic[T]` — yani ek hi class/function ko **different data types ke saath reusable** kaise banate hain.


# Lesson 19: `Generic`, `TypeVar` aur `Generic[T]`

Ab hum **Python type system** ke advanced part mein aa rahe hain. Tumne pehle `TypeVar` ke baare mein poocha tha—ab usko properly samajhte hain.

---

## 1. Problem: reusable code, different types

Maan lo humare paas function hai:

```python
def first_item(items):
    return items[0]
```

Ye multiple types ke saath kaam karega:

```python
print(first_item([10, 20, 30]))
print(first_item(["Ali", "Ahmed", "Usman"]))
```

Output:

```text
10
Ali
```

Lekin type checker ko ye samjhana ho ke:

> jo type input mein aayegi, wahi type output mein return hogi

to `TypeVar` useful hai.

---

# 2. `TypeVar` kya hai?

```python
from typing import TypeVar

T = TypeVar("T")
```

`T` ek **type variable** hai.

Isko normal variable mat samajhna:

```python
T = 10
```

jaisa runtime data variable nahi.

Ye type system ke liye placeholder hai.

Mental model:

```text
T = "koi bhi ek type"
```

---

# 3. Simple example

```python
from typing import TypeVar

T = TypeVar("T")


def first_item(items: list[T]) -> T:
    return items[0]
```

Ab:

```python
numbers = first_item([10, 20, 30])
```

Type checker samjhega:

```text
T = int
```

Isliye:

```text
numbers → int
```

Aur:

```python
names = first_item(["Ali", "Ahmed"])
```

mein:

```text
T = str
```

So:

```text
names → str
```

---

# 4. Ye generic kyun hai?

Ek hi function:

```python
first_item()
```

different types ke saath reusable hai.

```text
list[int]   → T = int
list[str]   → T = str
list[float] → T = float
```

Is concept ko **generic programming** kehte hain.

---

# 5. `T` input aur output ko connect karta hai

Ye important hai.

```python
def first_item(items: list[T]) -> T:
```

Yahan `T` do jagah hai:

```text
list[T]
   ↓
input type

T
↓
output type
```

Matlab:

```text
Input: list[int]
Output: int
```

aur:

```text
Input: list[str]
Output: str
```

---

# 6. Agar `TypeVar` na use karein?

Tum likh sakte ho:

```python
def first_item(items: list) -> object:
    return items[0]
```

Lekin information lose ho jati hai.

Type checker ko sirf pata hai:

```text
return → object
```

Usko ye relationship clearly nahi pata:

```text
list[int] → int
list[str] → str
```

`TypeVar` ye relationship preserve karta hai.

---

# 7. Generic class

Ab function se class par aate hain.

Python mein:

```python
from typing import Generic, TypeVar

T = TypeVar("T")
```

Phir:

```python
class Box(Generic[T]):

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

Ab `Box` generic class hai.

---

# 8. `Box[int]`

```python
number_box = Box[int](100)
```

Yahan:

```text
T = int
```

So:

```python
number_box.value
```

ka type:

```text
int
```

Aur:

```python
number_box.get()
```

ka type:

```text
int
```

---

# 9. `Box[str]`

```python
name_box = Box[str]("Ali")
```

Yahan:

```text
T = str
```

So:

```python
name_box.get()
```

ka type:

```text
str
```

---

# 10. Ek class, multiple types

```text
             Box[T]
                │
        ┌───────┴───────┐
        ↓               ↓
    Box[int]         Box[str]
        ↓               ↓
      100              "Ali"
```

Isi wajah se `Generic[T]` powerful hai.

---

# 11. `Generic[T]` ka actual meaning

```python
class Box(Generic[T]):
```

ka matlab roughly:

> "Box ek generic class hai jo kisi type `T` ke saath kaam karegi."

Phir:

```python
Box[int]
```

means:

> Box jahan `T = int`

Aur:

```python
Box[str]
```

means:

> Box jahan `T = str`

---

# 12. Multiple TypeVars

Sirf `T` hi nahi hota.

```python
T = TypeVar("T")
U = TypeVar("U")
```

Example:

```python
def pair(first: T, second: U) -> tuple[T, U]:
    return first, second
```

Ab:

```python
result = pair(10, "Ali")
```

Type:

```text
tuple[int, str]
```

Yahan:

```text
T = int
U = str
```

---

# 13. Example

```python
result = pair("Temperature", 22.5)
```

Type:

```text
tuple[str, float]
```

Yani:

```text
T = str
U = float
```

---

# 14. HVAC example

Maan lo hum ek generic sensor value container banana chahte hain.

```python
from typing import Generic, TypeVar

T = TypeVar("T")


class SensorValue(Generic[T]):

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

Temperature:

```python
temperature = SensorValue[float](22.5)
```

Pressure:

```python
pressure = SensorValue[int](250)
```

Status:

```python
status = SensorValue[str]("RUNNING")
```

Ek hi class:

```text
SensorValue[T]
     │
     ├── float
     ├── int
     └── str
```

---

# 15. `TypeVar` ko constraint de sakte hain

Example:

```python
T = TypeVar("T", int, float)
```

Ab `T` normally:

```text
int
```

ya:

```text
float
```

ho sakta hai.

Example:

```python
def square(value: T) -> T:
    return value * value
```

Conceptually allowed:

```python
square(5)
square(2.5)
```

Lekin arbitrary `str` ke liye type checker is generic definition ko acceptable nahi samjhega.

---

# 16. Bound `TypeVar`

Ek aur concept:

```python
T = TypeVar("T", bound=Employee)
```

Matlab:

> `T` ko `Employee` ya `Employee` ki subclass hona chahiye.

Example:

```python
class Employee:
    pass


class Manager(Employee):
    pass


T = TypeVar("T", bound=Employee)


def process(employee: T) -> T:
    return employee
```

Ab:

```python
manager = process(Manager())
```

Type relationship preserve ho sakta hai:

```text
T = Manager
```

---

# 17. Constraint vs Bound

Ye difference important hai.

### Constraints

```python
T = TypeVar("T", int, float)
```

Matlab specific listed types:

```text
int OR float
```

### Bound

```python
T = TypeVar("T", bound=Employee)
```

Matlab:

```text
Employee
ya Employee ki subclass
```

Mental model:

```text
Constraints
→ limited choices

Bound
→ ek type family / hierarchy ke andar
```

---

# 18. `Generic` aur `Protocol` ka connection

Ab tumhare previous lesson ka concept connect karte hain.

`Protocol`:

```python
class Repository(Protocol[T]):

    def get(self, id: int) -> T:
        ...
```

Ye generic Protocol ho sakta hai.

Example:

```text
Repository[Employee]
Repository[Equipment]
Repository[Customer]
```

Yani:

```text
Protocol
+
Generic
=
Reusable structural interface
```

---

# 19. `TypeVar` vs `Any`

Ye bhi bohat important difference hai.

### `Any`

```python
def get_value() -> Any:
    ...
```

Matlab:

> Type checker ko practically keh rahe ho: "is value ko kisi bhi type ki tarah treat karo."

### `TypeVar`

```python
T = TypeVar("T")

def get_value(value: T) -> T:
    return value
```

Matlab:

> Input aur output ke darmiyan type relationship preserve karo.

So:

```text
Any
→ type information loose

TypeVar
→ type relationship preserve
```

---

# 20. `TypeVar` runtime par kya karta hai?

Ye bohat important:

```python
T = TypeVar("T")
```

Python runtime par koi actual `T` value create nahi karta.

`T` mainly **static typing / type checking** ke liye hai.

Yani:

```text
TypeVar
     ↓
type checker ko information
     ↓
developer ko safer code
```

Ye Java/C++ ke runtime generic mechanism jaisa exactly nahi hai.

---

# 21. `Generic` ka purpose

Suppose:

```python
class Box:
    def __init__(self, value):
        self.value = value
```

Ye runtime par perfectly kaam karega.

Lekin:

```python
class Box(Generic[T]):
```

type checker ko additional information deta hai:

```text
Box[int]
Box[str]
Box[Employee]
```

Yani generic type relationship formally express hota hai.

---

# 22. Real-world mental model

Ek **container** imagine karo:

```text
Box[T]
```

Box khud same hai.

Lekin andar kya hai?

```text
Box[int]       → 100
Box[str]       → "Ali"
Box[float]     → 22.5
Box[Employee]  → Employee object
```

`T` ka matlab:

> "Box ke andar jo type hai, woh T hai."

---

# 23. Python ki built-in generics

Tum already generics use kar rahe ho:

```python
list[int]
```

```python
dict[str, int]
```

```python
tuple[str, float]
```

```python
set[int]
```

Example:

```python
employees: list[str]
```

means:

> `employees` ek list hai jiske elements `str` hain.

Aur:

```python
prices: dict[str, float]
```

means:

```text
key   → str
value → float
```

Ye bhi generic type concept hai.

---

# 24. `T` ko `list[T]` mein samjho

```python
T = TypeVar("T")
```

Function:

```python
def first_item(items: list[T]) -> T:
    return items[0]
```

Agar:

```python
first_item([1, 2, 3])
```

to:

```text
T = int
```

Agar:

```python
first_item(["A", "B"])
```

to:

```text
T = str
```

Yehi **generic type inference** ka basic idea hai.

---

# 25. Complete example

```python
from typing import Generic, TypeVar

T = TypeVar("T")


class Storage(Generic[T]):

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    def set(self, value: T) -> None:
        self.value = value
```

Use:

```python
storage = Storage[int](100)

storage.set(200)

print(storage.get())
```

Output:

```text
200
```

Lekin type checker ke perspective se:

```python
storage.set("Hello")
```

wrong type hai, kyun ke:

```text
Storage[int]
```

mein:

```text
T = int
```

---

# 26. Sab concepts ko connect karo

Ab tumne Python ke type-system ke multiple pieces dekhe:

```text
Any
│
├── kisi bhi type ko allow
│
TypeVar
│
├── type relationship preserve
│
Generic
│
├── reusable typed classes
│
Protocol
│
├── structural interface
│
TypedDict
│
└── dictionary ki expected structure
```

Ye sab **static typing ecosystem** ke concepts hain.

---

## Sabse important 5 lines

```python
T = TypeVar("T")
```

→ type variable.

```python
def get(x: T) -> T:
```

→ input aur output same generic type relationship.

```python
class Box(Generic[T]):
```

→ generic class.

```python
Box[int]
```

→ `T = int`.

```python
Box[str]
```

→ `T = str`.

---

### Next Lesson 20

**`TypedDict`, `Mapping`, `MutableMapping`, `Sequence`, `Iterable`, `Iterator`, aur `Callable`** — ye tumhare pehle wale `typing` wale question ka next major part hoga, aur hum specifically samjhenge ke:

```python
list
Sequence
Iterable
Iterator
```

mein actual difference kya hai, aur **`Mapping` vs `MutableMapping`** kya hota hai.

# Lesson 20: `TypedDict`, `Mapping`, `MutableMapping`, `Sequence`, `Iterable`, `Iterator`, `Callable`

Ab hum Python ke `typing` module ke important types ko properly differentiate karenge.

Tumne pehle ye import dekha tha:

```python
from typing import (
    TypedDict,
    MutableMapping,
    Sequence,
    Iterable,
    Iterator,
    Callable
)
```

Aaj iska actual meaning clear karte hain.

---

# 1. `TypedDict`

Sabse pehle `TypedDict`.

Normally Python dictionary:

```python
employee = {
    "name": "Ali",
    "age": 30,
    "salary": 5000
}
```

Python runtime ke liye ye simply:

```text
dict
```

hai.

Lekin type checker ko hum bata sakte hain ke dictionary mein **kaun se keys honi chahiye aur unki values kis type ki honi chahiye**.

```python
from typing import TypedDict


class Employee(TypedDict):
    name: str
    age: int
    salary: float
```

Ab:

```python
employee: Employee = {
    "name": "Ali",
    "age": 30,
    "salary": 5000.0
}
```

---

# 2. `TypedDict` class normal class nahi hai

Ye important hai.

```python
class Employee(TypedDict):
    name: str
    age: int
```

Iska matlab ye nahi:

```text
Employee → normal Python object/class
```

Balkay:

```text
Employee
   ↓
dictionary ki expected structure
```

Ye mainly **static type checking** ke liye hai.

---

# 3. Wrong key/value

Suppose:

```python
employee: Employee = {
    "name": "Ali",
    "age": "thirty",
    "salary": 5000.0
}
```

`age` expected:

```python
int
```

Lekin diya:

```python
str
```

Type checker warning de sakta hai.

Isi tarah:

```python
employee: Employee = {
    "name": "Ali",
    "age": 30
}
```

mein `salary` required hone ki wajah se type checker issue report kar sakta hai.

---

# 4. `TypedDict` kab useful hai?

Jab tumhara data dictionary form mein ho:

```python
{
    "work_order": "WO-1001",
    "floor": "34",
    "area": "Kitchen"
}
```

Tum define kar sakte ho:

```python
class WorkOrder(TypedDict):
    work_order: str
    floor: str
    area: str
```

Ab code ko clear pata hai ke expected dictionary structure kya hai.

---

# 5. `TypedDict` vs normal class

### Normal class

```python
class Employee:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

Object:

```python
emp = Employee("Ali", 30)
```

### TypedDict

```python
class EmployeeData(TypedDict):
    name: str
    age: int
```

Data:

```python
emp = {
    "name": "Ali",
    "age": 30
}
```

Mental model:

```text
class
→ object ka structure + behavior

TypedDict
→ dictionary ka structure
```

---

# 6. Ab `Mapping`

`Mapping` ko simple words mein samjho:

> **key-value data ko read/access karne wala interface.**

Example:

```python
from typing import Mapping

data: Mapping[str, int] = {
    "AHU": 10,
    "VAV": 20
}
```

Yahan:

```text
key   → str
value → int
```

---

# 7. `Mapping` read-oriented hai

Suppose:

```python
data: Mapping[str, int] = {
    "AHU": 10
}
```

Tum read kar sakte ho:

```python
print(data["AHU"])
```

Lekin type ke conceptually:

```python
data["AHU"] = 20
```

allowed nahi maana jata, kyun ke `Mapping` mutable hone ki guarantee nahi deta.

Yani:

```text
Mapping
   ↓
read/access
```

---

# 8. `MutableMapping`

Ab:

```python
from typing import MutableMapping
```

`MutableMapping` ka matlab:

> Mapping jisme values/entries modify ki ja sakti hain.

Example:

```python
data: MutableMapping[str, int] = {
    "AHU": 10
}
```

Ab:

```python
data["AHU"] = 20
```

valid hai.

Aur:

```python
data["VAV"] = 30
```

bhi.

---

# 9. `dict` aur `Mapping`

Important relationship:

```text
dict
  ↓
Mapping
```

`dict` ek concrete mutable dictionary implementation hai.

Function ko agar sirf read karna hai:

```python
def show(data: Mapping[str, int]):
    print(data["AHU"])
```

to function ko specifically `dict` demand karne ki zaroorat nahi.

---

# 10. Ye better design kyun hai?

Instead of:

```python
def show(data: dict[str, int]):
    ...
```

agar function sirf data read karta hai:

```python
def show(data: Mapping[str, int]):
    ...
```

to function broader types accept kar sakta hai jo Mapping behavior provide karti hain.

Ye **programming to an interface/abstraction** ka concept hai.

---

# 11. `Mapping` vs `MutableMapping`

| Type             | Read | Modify |
| ---------------- | ---: | -----: |
| `Mapping`        |    ✅ |      ❌ |
| `MutableMapping` |    ✅ |      ✅ |
| `dict`           |    ✅ |      ✅ |

Mental model:

```text
Mapping
   ↓
"I need key-value access."

MutableMapping
   ↓
"I need key-value access + modification."
```

---

# 12. Ab `Sequence`

`Sequence` ordered collection ka interface hai.

Examples:

```python
list
tuple
str
```

Ye sequence behavior provide karte hain.

Example:

```python
from typing import Sequence

numbers: Sequence[int] = [10, 20, 30]
```

Tum indexing kar sakte ho:

```python
print(numbers[0])
```

Output:

```text
10
```

Aur:

```python
len(numbers)
```

---

# 13. Sequence ki important properties

Sequence generally:

```text
ordered
indexable
iterable
length available
```

Example:

```python
numbers = [10, 20, 30]
```

Tum:

```python
numbers[0]
numbers[1]
len(numbers)
```

kar sakte ho.

---

# 14. `Sequence` vs `list`

Agar function ko specifically list ki zaroorat nahi:

```python
def total(numbers: Sequence[int]):
    return sum(numbers)
```

Ab tum:

```python
total([1, 2, 3])
```

aur:

```python
total((1, 2, 3))
```

dono de sakte ho.

Kyun?

Kyunkay:

```text
list
tuple
```

dono sequence behavior provide karte hain.

---

# 15. Sequence ka matlab mutable nahi

Ye important hai.

```python
numbers: Sequence[int]
```

ka matlab ye nahi ke list hi hogi.

Aur na hi ye guarantee hai ke modify kar sakte ho.

For example:

```python
numbers[0] = 100
```

`Sequence` interface ke against allowed nahi maana jata.

Agar modification chahiye to `MutableSequence` bhi available hai.

---

# 16. `MutableSequence`

Example:

```python
from typing import MutableSequence

numbers: MutableSequence[int] = [10, 20, 30]

numbers[0] = 100
```

Ab modification allowed hai.

Common concrete example:

```text
list → MutableSequence
```

---

# 17. `Sequence` vs `MutableSequence`

```text
Sequence
   ↓
read/index/access

MutableSequence
   ↓
read + modify
```

Similar relationship:

```text
Mapping
   ↓
read key/value

MutableMapping
   ↓
read + modify
```

---

# 18. Ab `Iterable`

Ye bohat important hai.

`Iterable` ka matlab:

> Jis object ko `for` loop mein iterate kiya ja sakta hai.

Example:

```python
from typing import Iterable

def show(items: Iterable[int]):
    for item in items:
        print(item)
```

Ab:

```python
show([1, 2, 3])
```

Aur:

```python
show((1, 2, 3))
```

Aur:

```python
show({1, 2, 3})
```

sab possible hain.

---

# 19. `Iterable` ka core idea

Agar tum:

```python
for x in object:
    ...
```

kar sakte ho, to object iterable hai.

Examples:

```text
list       → Iterable
tuple      → Iterable
set        → Iterable
dict       → Iterable
string     → Iterable
generator  → Iterable
```

---

# 20. `Sequence` vs `Iterable`

Ye bohat important difference hai.

```text
Sequence
   ↓
ordered + indexable + iterable

Iterable
   ↓
bas iterate kar sakte ho
```

Example:

```python
numbers = [10, 20, 30]
```

Ye:

```python
numbers[0]
```

kar sakta hai.

Isliye Sequence behavior.

Lekin generic Iterable ko assume nahi kar sakte ke:

```python
items[0]
```

available hoga.

---

# 21. Example

Function:

```python
def process(items: Iterable[int]):
    for item in items:
        print(item)
```

Is function ko index ki zaroorat nahi.

Isliye `Iterable` use karna better abstraction hai.

Agar function mein:

```python
items[0]
```

chahiye, to `Sequence` more appropriate hai.

---

# 22. `Iterator`

Ab `Iterable` aur `Iterator` ko differentiate karo.

### Iterable

```text
"Main tumhein iterator de sakta hoon."
```

### Iterator

```text
"Main next item de sakta hoon."
```

Iterator mein:

```python
next()
```

ka concept hota hai.

Example:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)
```

Ab:

```python
print(next(iterator))
```

Output:

```text
10
```

Phir:

```python
print(next(iterator))
```

Output:

```text
20
```

Phir:

```python
print(next(iterator))
```

Output:

```text
30
```

---

# 23. Fourth `next()`?

Ab:

```python
next(iterator)
```

karoge to:

```text
StopIteration
```

raise hoga.

Kyun?

Kyun ke iterator ke paas aur items nahi hain.

---

# 24. Iterable → Iterator

Basic flow:

```text
list
 ↓
iter()
 ↓
iterator
 ↓
next()
 ↓
item
```

Example:

```python
numbers = [10, 20, 30]

it = iter(numbers)

print(next(it))
print(next(it))
```

---

# 25. `for` loop internally iterator use karta hai

Jab tum:

```python
for x in numbers:
    print(x)
```

likhte ho, conceptually Python iterator protocol use karta hai.

Simplified idea:

```text
iter(numbers)
      ↓
next()
      ↓
next()
      ↓
next()
      ↓
StopIteration
```

Isliye `Iterator` samajhna `for` loop ke internals samajhne mein useful hai.

---

# 26. Iterable vs Iterator

| Feature                  |                 Iterable |       Iterator |
| ------------------------ | -----------------------: | -------------: |
| `for` loop               |                        ✅ |              ✅ |
| `iter()`                 | Usually returns iterator | Usually itself |
| `next()`                 |             Zaroori nahi |              ✅ |
| State maintain karta hai |          Not necessarily |              ✅ |

Simple:

```text
Iterable
→ iterate kar sakte ho

Iterator
→ next item provide karta hai
```

---

# 27. Generator kya hai?

Generator iterator ka common example hai.

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

```python
g = numbers()
```

`g` ko iterate kar sakte ho:

```python
for x in g:
    print(x)
```

Generator ek iterator behavior provide karta hai.

---

# 28. `Callable`

Ab last important type:

```python
Callable
```

`Callable` ka matlab:

> Jo object function ki tarah call kiya ja sakta ho.

Example:

```python
def add(a, b):
    return a + b
```

`add` callable hai.

```python
add(10, 20)
```

---

# 29. Callable type annotation

```python
from typing import Callable
```

Example:

```python
def execute(
    operation: Callable[[int, int], int],
    a: int,
    b: int
) -> int:

    return operation(a, b)
```

Yahan:

```python
Callable[[int, int], int]
```

ka matlab:

```text
arguments:
    int
    int

return:
    int
```

---

# 30. Example

```python
def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b
```

Function:

```python
def execute(
    operation: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return operation(a, b)
```

Use:

```python
print(execute(add, 10, 20))
```

Output:

```text
30
```

Aur:

```python
print(execute(multiply, 10, 20))
```

Output:

```text
200
```

---

# 31. Callable ka mental model

```text
Callable[[InputTypes], ReturnType]
```

Example:

```python
Callable[[str, int], bool]
```

means:

```text
input 1 → str
input 2 → int
return  → bool
```

---

# 32. Sab concepts ek saath

Ab ye diagram dekho:

```text
                    Collections / Objects
                           │
             ┌─────────────┼─────────────┐
             │             │             │
          Mapping       Sequence       Iterable
             │             │             │
             ↓             ↓             ↓
      key/value data     ordered      for-loop
             │             │
             ↓             ↓
     MutableMapping  MutableSequence
             │             │
             ↓             ↓
       modify data    modify sequence


Iterable
   ↓
iter()
   ↓
Iterator
   ↓
next()
```

Aur:

```text
Callable
   ↓
function ki tarah call ho sakta hai
```

---

# 33. Practical function design

Suppose tumhare paas:

```python
def process(data):
    ...
```

Ab question ye hai ke `data` kis type ka hona chahiye?

### Agar sirf loop chahiye:

```python
def process(data: Iterable[str]):
    ...
```

### Agar indexing chahiye:

```python
def process(data: Sequence[str]):
    ...
```

### Agar key-value read karna hai:

```python
def process(data: Mapping[str, int]):
    ...
```

### Agar key-value modify bhi karna hai:

```python
def process(data: MutableMapping[str, int]):
    ...
```

### Agar function receive karna hai:

```python
def process(fn: Callable[[int], str]):
    ...
```

Ye **good API/type design** hai.

---

# 34. Sabse important comparison

```text
dict
  ↓
Mapping
  ↓
MutableMapping
```

Actually conceptually `MutableMapping` Mapping behavior ko extend karta hai.

Similarly:

```text
list
  ↓
Sequence
  ↓
MutableSequence
```

Aur:

```text
list
tuple
set
dict
string
generator
      ↓
   Iterable
```

Lekin har Iterable Sequence nahi hota.

---

# 35. Ek important example

```python
data = {
    "AHU-01": 22.5,
    "AHU-02": 23.0
}
```

Dictionary:

```python
data
```

Iterable hai.

Lekin jab tum:

```python
for x in data:
    print(x)
```

karte ho, normally keys milengi:

```text
AHU-01
AHU-02
```

Agar values chahiye:

```python
for value in data.values():
    print(value)
```

Agar key/value pairs:

```python
for key, value in data.items():
    print(key, value)
```

Isliye `Iterable` ka matlab sirf:

> "Main is object ko iterate kar sakta hoon."

Ye automatically ye nahi batata ke iteration mein **kya** milega.

---

## Final cheat sheet

| Type              | Simple meaning                            |
| ----------------- | ----------------------------------------- |
| `TypedDict`       | Dictionary ki expected keys + value types |
| `Mapping`         | Key-value data ko read/access karna       |
| `MutableMapping`  | Key-value data read + modify              |
| `Sequence`        | Ordered/indexable collection              |
| `MutableSequence` | Ordered collection + modify               |
| `Iterable`        | `for` loop se iterate ho sakta hai        |
| `Iterator`        | `next()` se next item deta hai            |
| `Callable`        | Function ki tarah call ho sakta hai       |

### Sabse important distinction:

```text
Iterable
   ↓
for x in data

Iterator
   ↓
next(data)

Sequence
   ↓
data[0]

Mapping
   ↓
data["key"]

MutableMapping
   ↓
data["key"] = value

Callable
   ↓
data(...)
```

**Next Lesson 21:** `Optional`, `Union`, `Literal`, `Final`, `ClassVar`, `Any`, `Never`, aur `NoReturn` — yani type annotations mein **"value ho sakti hai ya nahi", "multiple types", "fixed values", aur "class variable"** kaise define karte hain.
