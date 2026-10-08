# Python Classes — Detailed Guide with Code Explanation (Roman Urdu)

Har concept ke sath **code** aur uski **line-by-line explanation** di gayi hai.

---

# 1. Class aur Object

```python
class Car:
    pass

car1 = Car()
car2 = Car()
```

**Explanation:**
- `class Car:` → `Car` naam ki class define ki
- `pass` → filhal class khali hai (koi code nahi)
- `car1 = Car()` → `Car` class se pehla object banaya
- `car2 = Car()` → `Car` class se doosra object banaya

Yahan `Car` **class** hai aur `car1`, `car2` **objects** hain.

---

# 2. Attributes aur Methods

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def start(self):
        print("Car started")

car1 = Car("Toyota", "White")
print(car1.brand)
print(car1.color)
car1.start()
```

**Output:**
```
Toyota
White
Car started
```

**Explanation:**
- `def __init__(self, brand, color):` → constructor, object banate waqt chalta hai
- `self.brand = brand` → `brand` value object ke andar store ki
- `self.color = color` → `color` value object ke andar store ki
- `def start(self):` → method jo car start hone par print karta hai
- `car1 = Car("Toyota", "White")` → object banaya aur values di
- `print(car1.brand)` → object ka `brand` attribute print kiya
- `car1.start()` → method call kiya

---

# 3. `__init__()` Constructor

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp1 = Employee("Nouman", 5000)
emp2 = Employee("Ali", 6000)

print(emp1.name)
print(emp2.name)
```

**Output:**
```
Nouman
Ali
```

**Explanation:**
- `def __init__(self, name, salary):` → constructor jo object banate waqt automatically call hota hai
- `self.name = name` → `name` ko object ke attribute mein save kiya
- `self.salary = salary` → `salary` ko object ke attribute mein save kiya
- `emp1 = Employee("Nouman", 5000)` → object banaya, `__init__` automatically chala
- `print(emp1.name)` → `emp1` ka name print kiya

---

# 4. `self` Keyword

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

emp1 = Employee("Nouman")
emp2 = Employee("Ali")

emp1.show()
emp2.show()
```

**Output:**
```
Nouman
Ali
```

**Explanation:**
- `self` → current object ko represent karta hai
- `def show(self):` → method jo current object ka name print karta hai
- `emp1.show()` → `self` mein `emp1` chala gaya, `Nouman` print hua
- `emp2.show()` → `self` mein `emp2` chala gaya, `Ali` print hua

> `self` reserved keyword nahi hai, lekin convention ke mutabiq use hota hai.

---

# 5. Instance Variables aur Class Variables

## Instance Variable

```python
class Employee:
    def __init__(self, name):
        self.name = name

e1 = Employee("Ali")
e2 = Employee("Ahmed")

print(e1.name)
print(e2.name)
```

**Output:**
```
Ali
Ahmed
```

**Explanation:**
- `self.name = name` → har object ka apna `name` banata hai
- `e1.name` → `Ali` (e1 ka apna data)
- `e2.name` → `Ahmed` (e2 ka apna data)

## Class Variable

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

e1 = Employee("Ali")
e2 = Employee("Ahmed")

print(e1.company)
print(e2.company)
print(Employee.company)
```

**Output:**
```
ABC
ABC
ABC
```

**Explanation:**
- `company = "ABC"` → class variable, sab objects ke liye shared
- `e1.company` → `ABC` (class se aaya)
- `e2.company` → `ABC` (class se aaya)
- `Employee.company` → `ABC` (class se direct)

### Class variable change karna:

```python
Employee.company = "XYZ"
print(e1.company)
```

**Output:**
```
XYZ
```

**Explanation:**
- `Employee.company = "XYZ"` → class variable change hua
- `e1.company` → ab `XYZ` (kyunkay sab shared hai)

### Object se change karna:

```python
e1.company = "PQR"
print(e1.company)
print(e2.company)
```

**Output:**
```
PQR
XYZ
```

**Explanation:**
- `e1.company = "PQR"` → `e1` par **naya instance attribute** ban gaya
- `e1.company` → `PQR` (apna naya attribute)
- `e2.company` → `XYZ` (class variable wahi hai)

---

# 6. Methods ki 3 Types

## 1. Instance Method

```python
class Employee:
    def show(self):
        print("Employee")

e = Employee()
e.show()
```

**Output:**
```
Employee
```

**Explanation:**
- `def show(self):` → instance method, `self` leta hai
- `e.show()` → object se call kiya

## 2. Class Method

```python
class Employee:
    company = "ABC"

    @classmethod
    def show_company(cls):
        print(cls.company)

Employee.show_company()
```

**Output:**
```
ABC
```

**Explanation:**
- `@classmethod` → decorator jo class method banata hai
- `def show_company(cls):` → `cls` current class ko represent karta hai
- `cls.company` → class ka `company` attribute access kiya
- `Employee.show_company()` → class se call kiya (object ki zaroorat nahi)

## 3. Static Method

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

print(Calculator.add(5, 3))
```

**Output:**
```
8
```

**Explanation:**
- `@staticmethod` → decorator jo static method banata hai
- `def add(a, b):` → na `self`, na `cls`
- `Calculator.add(5, 3)` → sirf calculation, object/class ki zaroorat nahi

## Teenon ka Difference

```python
class Employee:
    company = "ABC"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def show_employee(self):          # Instance Method
        print(self.name)
        print(self.salary)

    @classmethod
    def show_company(cls):            # Class Method
        print(cls.company)

    @staticmethod
    def calculate_bonus(salary):      # Static Method
        return salary * 0.10

emp = Employee("Nouman", 5000)
emp.show_employee()                   # object ka data
Employee.show_company()               # class ka data
print(Employee.calculate_bonus(5000)) # sirf calculation
```

**Output:**
```
Nouman
5000
ABC
500.0
```

**Explanation:**
- `emp.show_employee()` → `self` mein `emp` gaya, object ka data print hua
- `Employee.show_company()` → `cls` mein `Employee` gayi, class ka data print hua
- `Employee.calculate_bonus(5000)` → sirf `5000` par calculation hui

## Class Method ka Practical Use — Alternative Constructor

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @classmethod
    def from_string(cls, data):
        name, salary = data.split(",")
        return cls(name, int(salary))

emp = Employee.from_string("Nouman,5000")
print(emp.name)
print(emp.salary)
```

**Output:**
```
Nouman
5000
```

**Explanation:**
- `data.split(",")` → `"Nouman,5000"` ko `["Nouman", "5000"]` banaya
- `name, salary = ...` → unpacking, `name="Nouman"`, `salary="5000"`
- `return cls(name, int(salary))` → `cls` current class ka object banata hai
- `Employee.from_string("Nouman,5000")` → string se object banaya

---

# 7. Encapsulation

## Public Attribute

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp = Employee("Ali", 5000)
print(emp.name)
print(emp.salary)
emp.salary = 7000
print(emp.salary)
```

**Output:**
```
Ali
5000
7000
```

**Explanation:**
- `self.name`, `self.salary` → public attributes, direct access
- `emp.salary = 7000` → directly change kar sakte hain

## `_protected`

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary

emp = Employee("Ali", 5000)
print(emp._salary)
```

**Output:**
```
5000
```

**Explanation:**
- `self._salary` → single underscore, convention "internal use"
- `emp._salary` → technically access ho jata hai, lekin signal milta hai ke bahar use mat karo

## `__private` — Name Mangling

```python
class Employee:
    def __init__(self, salary):
        self.__salary = salary

emp = Employee(5000)
print(emp.__salary)
```

**Output:**
```
AttributeError: 'Employee' object has no attribute '__salary'
```

**Explanation:**
- `self.__salary` → double underscore, Python naam badal deta hai
- `__salary` → andar se `_Employee__salary` ban jata hai
- `emp.__salary` → direct access nahi hota, error aata hai

### Name mangled access:

```python
print(emp._Employee__salary)
```

**Output:**
```
5000
```

**Explanation:**
- `_Employee__salary` → name mangling ke baad ka actual naam

## Getter aur Setter

```python
class Employee:
    def __init__(self, salary):
        self.__salary = salary

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        if salary >= 0:
            self.__salary = salary
        else:
            print("Salary cannot be negative")

emp = Employee(5000)
print(emp.get_salary())
emp.set_salary(7000)
print(emp.get_salary())
emp.set_salary(-1000)
```

**Output:**
```
5000
7000
Salary cannot be negative
```

**Explanation:**
- `get_salary()` → private data return karta hai (getter)
- `set_salary()` → validation ke sath data set karta hai (setter)
- `emp.set_salary(-1000)` → negative hai, is liye print hua error message

## `@property` — Modern Tareeqa

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

emp = Employee(5000)
print(emp.salary)
emp.salary = 6000
print(emp.salary)
```

**Output:**
```
5000
6000
```

**Explanation:**
- `@property` → `salary()` method ko attribute ki tarah access karne deta hai
- `emp.salary` → getter call hua, `5000` return hua
- `@salary.setter` → setter define kiya
- `emp.salary = 6000` → setter call hua, validation pass, value set hui

## HVAC Example

```python
class AHU:
    def __init__(self, temperature):
        self.__temperature = temperature

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        if 15 <= value <= 30:
            self.__temperature = value
        else:
            print("Temperature must be between 15 and 30°C")

ahu = AHU(22)
print(ahu.temperature)
ahu.temperature = 24
print(ahu.temperature)
ahu.temperature = 50
```

**Output:**
```
22
24
Temperature must be between 15 and 30°C
```

**Explanation:**
- `ahu.temperature` → getter, `22` return
- `ahu.temperature = 24` → setter, valid, value set
- `ahu.temperature = 50` → setter, invalid, error message

---

# 8. Inheritance

## Basic

```python
class Animal:
    def eat(self):
        print("Eating")

class Dog(Animal):
    def bark(self):
        print("Barking")

dog = Dog()
dog.eat()
dog.bark()
```

**Output:**
```
Eating
Barking
```

**Explanation:**
- `class Animal:` → parent class
- `class Dog(Animal):` → child class, `Animal` se inherit kiya
- `dog.eat()` → parent ka method (inherit hua)
- `dog.bark()` → child ka apna method

## Parent ka `__init__()` Inherit

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    pass

dog = Dog("Tommy")
print(dog.name)
```

**Output:**
```
Tommy
```

**Explanation:**
- `Dog` ne apna `__init__` nahi banaya
- Is liye parent ka `__init__` use hua
- `dog.name` → `Tommy` set ho gaya

## Child ka apna `__init__()` + `super()`

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

dog = Dog("Tommy", "German Shepherd")
print(dog.name)
print(dog.breed)
```

**Output:**
```
Tommy
German Shepherd
```

**Explanation:**
- `super().__init__(name)` → parent ka `__init__` call kiya, `name` set hua
- `self.breed = breed` → child ne apna attribute add kiya
- `dog.name` → `Tommy` (parent se)
- `dog.breed` → `German Shepherd` (child ka apna)

## Method Overriding

```python
class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

dog = Dog()
dog.sound()
```

**Output:**
```
Bark
```

**Explanation:**
- `Dog` ne `sound()` method override kar diya
- `dog.sound()` → child ka method chala, parent ka nahi

## `super()` with Overriding

```python
class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        super().sound()
        print("Bark")

dog = Dog()
dog.sound()
```

**Output:**
```
Animal sound
Bark
```

**Explanation:**
- `super().sound()` → parent ka `sound()` call kiya
- `print("Bark")` → child ka additional behavior

## Multilevel Inheritance

```python
class Animal:
    def eat(self):
        print("Eating")

class Mammal(Animal):
    def walk(self):
        print("Walking")

class Dog(Mammal):
    def bark(self):
        print("Barking")

dog = Dog()
dog.eat()
dog.walk()
dog.bark()
```

**Output:**
```
Eating
Walking
Barking
```

**Explanation:**
- `Dog` → `Mammal` → `Animal` chain
- `dog.eat()` → `Animal` se aaya
- `dog.walk()` → `Mammal` se aaya
- `dog.bark()` → `Dog` ka apna

## Multiple Inheritance

```python
class Camera:
    def take_photo(self):
        print("Photo")

class Phone:
    def make_call(self):
        print("Calling")

class Smartphone(Camera, Phone):
    pass

phone = Smartphone()
phone.take_photo()
phone.make_call()
```

**Output:**
```
Photo
Calling
```

**Explanation:**
- `Smartphone(Camera, Phone)` → dono se inherit kiya
- `phone.take_photo()` → `Camera` se aaya
- `phone.make_call()` → `Phone` se aaya

## MRO

```python
class A:
    def show(self):
        print("A")

class B:
    def show(self):
        print("B")

class C(A, B):
    pass

c = C()
c.show()
print(C.mro())
```

**Output:**
```
A
[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
```

**Explanation:**
- `class C(A, B):` → `A` pehle hai
- `c.show()` → `A` ka method chala
- `C.mro()` → Method Resolution Order dikhata hai

---

# 9. `super()` Function

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

dog = Dog("Tommy", "German Shepherd")
dog.show()
print(dog.breed)
```

**Output:**
```
Tommy
German Shepherd
```

**Explanation:**
- `super().__init__(name)` → parent ka constructor call, `name` set hua
- `dog.show()` → parent ka method chala, `Tommy` print hua
- `print(dog.breed)` → child ka attribute, `German Shepherd`

---

# 10. Polymorphism

```python
class Dog:
    def sound(self):
        print("Bark")

class Cat:
    def sound(self):
        print("Meow")

animals = [Dog(), Cat()]
for animal in animals:
    animal.sound()
```

**Output:**
```
Bark
Meow
```

**Explanation:**
- Dono classes mein `sound()` method hai
- `for` loop mein har object ka `sound()` call hua
- Har object ne apna behavior dikhaya

## Duck Typing

```python
class Dog:
    def sound(self):
        print("Bark")

class Robot:
    def sound(self):
        print("Beep")

def make_sound(obj):
    obj.sound()

make_sound(Dog())
make_sound(Robot())
```

**Output:**
```
Bark
Beep
```

**Explanation:**
- `make_sound()` function ko object ki class nahi pata
- Sirf `obj.sound()` call karta hai
- Jis mein `sound()` hai, wo kaam karta hai

## HVAC Example

```python
class AHU:
    def start(self):
        print("AHU fan started")

class VAV:
    def start(self):
        print("VAV damper started")

class Pump:
    def start(self):
        print("Pump started")

def start_equipment(equipment):
    equipment.start()

start_equipment(AHU())
start_equipment(VAV())
start_equipment(Pump())
```

**Output:**
```
AHU fan started
VAV damper started
Pump started
```

**Explanation:**
- `start_equipment()` same function hai
- Har object ka apna `start()` method chala
- Function ko class ki detail nahi chahiye

## Operator Polymorphism

```python
print(10 + 20)
print("Hello " + "World")
```

**Output:**
```
30
Hello World
```

**Explanation:**
- `+` ka behavior data type ke according badalta hai
- Numbers → addition
- Strings → concatenation

---

# 11. Method Overriding

```python
class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

dog = Dog()
dog.sound()
```

**Output:**
```
Bark
```

**Explanation:**
- `Dog` ne `sound()` ko override kiya
- `dog.sound()` → child ka method chala

### `super()` ke sath:

```python
class Dog(Animal):
    def sound(self):
        super().sound()
        print("Bark")

dog = Dog()
dog.sound()
```

**Output:**
```
Animal sound
Bark
```

**Explanation:**
- `super().sound()` → parent ka method chala
- `print("Bark")` → child ka additional behavior

---

# 12. Abstraction

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

r = Rectangle(10, 5)
print(r.area())
```

**Output:**
```
50
```

**Explanation:**
- `from abc import ABC, abstractmethod` → abstraction ke liye modules import kiye
- `class Shape(ABC):` → abstract class banayi
- `@abstractmethod` → `area()` ko abstract method banaya
- `class Rectangle(Shape):` → child class
- `def area(self):` → abstract method implement kiya
- `r.area()` → `10 * 5 = 50` return hua

### Abstract class ka object nahi bana sakte:

```python
s = Shape()
```

**Output:**
```
TypeError: Can't instantiate abstract class Shape with abstract method area
```

**Explanation:**
- `Shape` abstract hai, direct object nahi bana sakte

### Child method implement na kare:

```python
class Circle(Shape):
    pass

c = Circle()
```

**Output:**
```
TypeError: Can't instantiate abstract class Circle with abstract method area
```

**Explanation:**
- `Circle` ne `area()` implement nahi kiya
- Is liye object nahi bana

## HVAC Example

```python
from abc import ABC, abstractmethod

class HVACEquipment(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class AHU(HVACEquipment):
    def start(self):
        print("AHU fan started")

    def stop(self):
        print("AHU fan stopped")

ahu = AHU()
ahu.start()
ahu.stop()
```

**Output:**
```
AHU fan started
AHU fan stopped
```

**Explanation:**
- `HVACEquipment` → abstract class, `start()` aur `stop()` required
- `AHU` ne dono implement kiye
- `ahu.start()` → `AHU` ka method chala
- `ahu.stop()` → `AHU` ka method chala

---

# 13. Properties — `@property`

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

emp = Employee(5000)
print(emp.salary)
emp.salary = 6000
print(emp.salary)
```

**Output:**
```
5000
6000
```

**Explanation:**
- `@property` → `salary()` method ko attribute ki tarah access
- `emp.salary` → getter call, `5000` return
- `@salary.setter` → setter define
- `emp.salary = 6000` → setter call, validation pass, value set

---

# 14. Special Methods (Dunder Methods)

## `__str__`

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __str__(self):
        return f"{self.name}: {self.salary}"

emp = Employee("Ali", 5000)
print(emp)
```

**Output:**
```
Ali: 5000
```

**Explanation:**
- `__str__` → human-readable string return karta hai
- `print(emp)` → `__str__` call hua, `Ali: 5000` print hua

## `__add__`

```python
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value

a = Number(10)
b = Number(20)
print(a + b)
```

**Output:**
```
30
```

**Explanation:**
- `__add__` → `+` operator ka behavior define kiya
- `a + b` → `a.__add__(b)` call hua
- `10 + 20 = 30` return hua

## `__eq__`

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

emp1 = Employee("Ali")
emp2 = Employee("Ali")
print(emp1 == emp2)
```

**Output:**
```
True
```

**Explanation:**
- `__eq__` → `==` operator ka behavior define kiya
- `emp1 == emp2` → `emp1.__eq__(emp2)` call hua
- `self.name == other.name` → `"Ali" == "Ali"` → `True`

## `__len__`

```python
class Team:
    def __init__(self, members):
        self.members = members

    def __len__(self):
        return len(self.members)

team = Team(["Ali", "Ahmed", "Usman"])
print(len(team))
```

**Output:**
```
3
```

**Explanation:**
- `__len__` → `len()` ka behavior define kiya
- `len(team)` → `team.__len__()` call hua
- `len(self.members)` → `3` return hua

## `__getitem__`

```python
class Team:
    def __init__(self, members):
        self.members = members

    def __getitem__(self, index):
        return self.members[index]

team = Team(["Ali", "Ahmed", "Usman"])
print(team[0])
print(team[1])
```

**Output:**
```
Ali
Ahmed
```

**Explanation:**
- `__getitem__` → indexing ka behavior define kiya
- `team[0]` → `team.__getitem__(0)` call hua
- `self.members[0]` → `Ali` return hua

## `__contains__`

```python
class Team:
    def __init__(self, members):
        self.members = members

    def __contains__(self, name):
        return name in self.members

team = Team(["Ali", "Ahmed", "Usman"])
print("Ali" in team)
print("John" in team)
```

**Output:**
```
True
False
```

**Explanation:**
- `__contains__` → `in` operator ka behavior define kiya
- `"Ali" in team` → `team.__contains__("Ali")` call hua
- `"Ali" in self.members` → `True` return hua

## `__call__`

```python
class Greeter:
    def __call__(self, name):
        print(f"Hello {name}")

greet = Greeter()
greet("Ali")
```

**Output:**
```
Hello Ali
```

**Explanation:**
- `__call__` → object ko function ki tarah call karne deta hai
- `greet("Ali")` → `greet.__call__("Ali")` call hua
- `Hello Ali` print hua

---

# 15. Composition aur Aggregation

## Composition

```python
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        self.engine.start()

car = Car()
car.start()
```

**Output:**
```
Engine started
```

**Explanation:**
- `Car` apna `Engine` object khud banati hai (`self.engine = Engine()`)
- `car.start()` → `self.engine.start()` call hua
- Dono ki lifecycle linked hai

## Aggregation

```python
class Employee:
    def __init__(self, name):
        self.name = name

class Department:
    def __init__(self, employee):
        self.employee = employee

emp = Employee("Ali")
dept = Department(emp)
print(dept.employee.name)
```

**Output:**
```
Ali
```

**Explanation:**
- `emp` pehle se exist karta hai
- `Department` ko `emp` ka reference diya
- `dept.employee.name` → `Ali` print hua
- Dono independently exist kar sakte hain

---

# 16. Nested Classes

```python
class Computer:
    class CPU:
        def process(self):
            print("CPU processing")

computer = Computer()
cpu = Computer.CPU()
cpu.process()
```

**Output:**
```
CPU processing
```

**Explanation:**
- `class CPU:` → `Computer` ke andar nested class
- `Computer.CPU()` → nested class ka object banaya
- `cpu.process()` → nested class ka method chala

---

# 17. `__dict__`

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

emp = Employee("Ali")
print(emp.__dict__)
print(Employee.__dict__["company"])
```

**Output:**
```
{'name': 'Ali'}
ABC
```

**Explanation:**
- `emp.__dict__` → instance ke attributes dikhata hai
- `Employee.__dict__["company"]` → class ka `company` attribute

---

# 18. Practical Example — Employee Management System

```python
class Employee:
    company = "ABC"

    def __init__(self, name, salary):
        self.name = name
        self._salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Invalid salary")
        self._salary = value

    def show_details(self):
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")
        print(f"Company: {self.company}")

class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department

    def show_details(self):
        super().show_details()
        print(f"Department: {self.department}")

manager = Manager("Nouman", 8000, "HVAC")
manager.show_details()
```

**Output:**
```
Name: Nouman
Salary: 8000
Company: ABC
Department: HVAC
```

**Explanation:**
- `company = "ABC"` → class variable
- `self._salary = salary` → protected attribute
- `@property` → getter define kiya
- `@salary.setter` → setter with validation
- `show_details()` → instance method
- `class Manager(Employee):` → inheritance
- `super().__init__(name, salary)` → parent constructor call
- `super().show_details()` → parent method call
- `manager.show_details()` → child ka overridden method chala

---

# 19. Complete Revision Table

| Concept | Purpose | Example |
|---------|---------|---------|
| Class | Object banane ka blueprint | `class Car:` |
| Object | Class ka instance | `car1 = Car()` |
| Attribute | Object ya class ka data | `self.name` |
| Method | Class ke andar function | `def start(self):` |
| `self` | Current instance | `self.name` |
| `__init__` | Object initialization | `def __init__(self):` |
| Instance variable | Har object ka apna data | `self.name` |
| Class variable | Class-level shared data | `company = "ABC"` |
| `@classmethod` | Class ko `cls` ke zariye access | `@classmethod` |
| `@staticmethod` | Class se related utility method | `@staticmethod` |
| Encapsulation | Data access control | `__salary`, `@property` |
| Inheritance | Parent se functionality lena | `class Dog(Animal):` |
| Polymorphism | Aik interface, mukhtalif behavior | `animal.sound()` |
| Abstraction | Interface define, implementation hide | `ABC`, `@abstractmethod` |
| Overriding | Parent method ka naya implementation | `def sound(self):` |
| `super()` | Parent class ke methods tak access | `super().__init__()` |
| `@property` | Method ko attribute ki tarah access | `@property` |
| Dunder methods | Built-in operations customize | `__str__`, `__eq__` |
| Composition | Objects ko parts ke taur par use | `self.engine = Engine()` |
| Aggregation | Independently existing objects associate | `Department(emp)` |
| MRO | Multiple inheritance mein method lookup order | `C.mro()` |

---

# 20. OOP ke 4 Pillars

```
                 OOP
                  │
      ┌───────────┼───────────┐
      ↓           ↓           ↓
Encapsulation  Inheritance  Polymorphism
                  │
                  ↓
              Abstraction
```

| Pillar | Matlab | Example |
|--------|--------|---------|
| **Encapsulation** | Data ko control karna | `__salary`, `@property` |
| **Inheritance** | Code reuse karna | `class Manager(Employee)` |
| **Polymorphism** | Same interface, different behavior | `ahu.start()`, `vav.start()` |
| **Abstraction** | Complexity hide karna | `ABC`, `@abstractmethod` |

---

# 21. Learning Order

```
Step 1: Class, Object, self, __init__
        ↓
Step 2: Instance vs Class variables
        ↓
Step 3: Methods (Instance, Class, Static)
        ↓
Step 4: Encapsulation + @property
        ↓
Step 5: Inheritance + super()
        ↓
Step 6: Polymorphism + Overriding
        ↓
Step 7: Abstraction (ABC)
        ↓
Step 8: Dunder Methods
        ↓
Step 9: Composition vs Aggregation
        ↓
Step 10: Real Projects
```

---

**Ab ye guide bilkul detailed hai.** Har code ke sath:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation

Agar kisi **specific concept** ko aur detail mein samjhana ho, ya **advanced topics** (metaclass, dataclass, descriptors) add karne ho, to batao! 🚀