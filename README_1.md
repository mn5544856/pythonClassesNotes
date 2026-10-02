


# Python Classes — Complete Guide in Roman Urdu

Python mein Class OOP (Object-Oriented Programming) ka basic concept hai. Class ki madad se hum apna data aur us data par kaam karne wale functions aik jagah organize kar sakte hain.

Python mein classes seekhne ke liye humein kuch important concepts samajhne honge:

1. Class aur Object

2. Attributes aur Methods

3. `__init__()` constructor

4. `self` keyword

5. Instance Variables aur Class Variables

6. Instance Methods, Class Methods aur Static Methods

7. Encapsulation

8. Inheritance

9. Polymorphism

10. Abstraction

11. Properties (`@property`)

12. Special (Magic/Dunder) Methods

13. Composition aur Aggregation

14. Class ke andar doosri class

15. Method Overriding aur `super()`

Chalo in sab ko examples ke sath step by step samajhte hain.

# 1. Class kya hoti hai?

Class aik blueprint ya template hoti hai, jis ki madad se hum objects create karte hain.

Misal ke taur par, agar hum `Car` ki class banate hain, to us mein car ka color, model aur speed define kar sakte hain.

## Class aur Objects

Car Class

Blueprint

color

model

speed

drive()

Class se objects create hote hain

Car 1

Toyota

Car 2

Honda

Car 3

BMW

Example:

Python

Run

```
class Car:
    pass

car1 = Car()
car2 = Car()
```

Explanation:

* `class Car:` aik class define karti hai.

* `pass` ka matlab hai ke filhal class ke andar koi code nahi hai.

* `car1 = Car()` aik object create karta hai.

* `car2 = Car()` doosra object create karta hai.

Yahan `Car` class hai aur `car1`, `car2` objects hain.

# 2. Attributes aur Methods

Class ke andar do important cheezein hoti hain.

* Attributes: Object ka data ya properties.

* Methods: Class ke andar define kiye gaye functions.

Python

Run

```
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

Output:

```
Toyota
White
Car started
```

Is example mein:

|
Code

|

Meaning

|
| --- | --- |
|

`brand`

|

Attribute ka input

|
|

`color`

|

Attribute ka input

|
|

`self.brand`

|

Object ka brand attribute

|
|

`self.color`

|

Object ka color attribute

|
|

`start()`

|

Method

|
|

`car1`

|

Object

|

Jab hum `car1.start()` likhte hain to `start()` method execute hota hai.

# 3. `__init__()` constructor

`__init__()` aik special method hai jo object create hone ke baad automatically call hota hai.

Iska aam istemal object ke attributes initialize karne ke liye hota hai.

Python

Run

```
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp1 = Employee("Nouman", 5000)
emp2 = Employee("Ali", 6000)

print(emp1.name)
print(emp2.name)
```

Output:

```
Nouman
Ali
```

Jab hum `Employee("Nouman", 5000)` likhte hain, Python object create karta hai aur `__init__()` ko automatically call karta hai.

`__init__()` technically object initialize karta hai, jabke object create karne ka kaam aam tor par `__new__()` karta hai.

# 4. `self` keyword

`self` current object ko represent karta hai. Iski madad se hum current object ke attributes aur methods access karte hain.

Python

Run

```
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

Output:

```
Nouman
Ali
```

Jab `emp1.show()` call hota hai, to `self` mein `emp1` object aata hai. Jab `emp2.show()` call hota hai, to `self` mein `emp2` aata hai.

`self` Python ka reserved keyword nahi hai, lekin convention ke mutabiq isi naam ko use kiya jata hai.

# 5. Instance Variables aur Class Variables

Python classes mein variables ki do common types hain.

Instance Variable

Har object ka apna data hota hai.

Python

Run

```
class Employee:
    def __init__(self, name):
        self.name = name

e1 = Employee("Ali")
e2 = Employee("Ahmed")
```

`e1.name` aur `e2.name` alag hain.

Class Variable

Class ke sab objects ke liye shared hota hai, jab tak object apna alag attribute na bana le.

Python

Run

```
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

e1 = Employee("Ali")
e2 = Employee("Ahmed")

print(e1.company)
print(e2.company)
```

Dono ka result `ABC` hoga.

Class variable ko class ke naam se bhi access kar sakte hain:

Python

Run

```
print(Employee.company)
```

Agar class variable ko class ke naam se change karte hain, to woh shared value change hoti hai.

Python

Run

```
Employee.company = "XYZ"
```

Lekin agar `e1.company = "PQR"` likhen, to `e1` par aik naya instance attribute ban jayega. Class variable apni purani value par rahega.

# 6. Methods ki 3 types

Python mein classes ke andar methods ki teen common types hoti hain.

1. Instance Method

`self` leta hai aur object ke data ke sath kaam karta hai.

Python

Run

```
class Employee:
    def show(self):
        print("Employee")

e = Employee()
e.show()
```

2. Class Method

`@classmethod` decorator aur `cls` parameter use karta hai. Class-level data ya alternative constructors ke liye useful hai.

Python

Run

```
class Employee:
    company = "ABC"

    @classmethod
    def show_company(cls):
        print(cls.company)

Employee.show_company()
```

3. Static Method

`@staticmethod` use karta hai. Is mein na `self` zaroori hai, na `cls`. Aisa function jo class se logically related ho, us ke liye useful hai.

Python

Run

```
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

print(Calculator.add(5, 3))
```

Output: `8`

In teenon mein farq: Instance method object ke data ke liye, class method class ke data ya class-level construction ke liye aur static method independent utility operation ke liye hota hai.


# 7. Encapsulation

Encapsulation ka matlab hai data aur us par kaam karne wale methods ko aik class ke andar organize karna. Is ke zariye hum data ko controlled access de sakte hain.

Python mein access ke liye naming conventions hain:

|
Syntax

|

Meaning

|
| --- | --- |
|

`name`

|

Public attribute

|
|

`_name`

|

Protected-style attribute; convention ke mutabiq internal use

|
|

`__name`

|

Name-mangled attribute

|

Example:

Python

Run

```
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)

account.deposit(500)
print(account.get_balance())
```

Output:

```
1500
```

Yahan `__balance` ko class ke bahar `account.__balance` se directly access nahi kar sakte. Python name mangling use karta hai.

Lekin yaad rakho: double underscore complete security nahi hai. Iska maqsad accidental access aur naming conflicts se bachana hai.

# 8. Inheritance

Inheritance ka matlab hai aik class doosri class ke attributes aur methods inherit kar sakti hai.

Is mein do important classes hoti hain:

* Parent class: Jis se inherit kiya jata hai.

* Child class: Jo parent se inherit karti hai.

Animal

Parent class

eat()

Cat

Child class

meow()

Dog

Child class

bark()

Example:

Python

Run

```
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

Output:

```
Eating
Barking
```

`Dog` ne `Animal` se `eat()` method inherit kiya hai. Is liye `Dog` ka object dono methods use kar sakta hai.

## Inheritance ki types

1. Single Inheritance

Aik child class aik parent class se inherit karti hai.

Parent

Child

2. Multiple Inheritance

Aik child class aik se zyada parent classes se inherit karti hai.

Parent A

Parent B

Child

3. Multilevel Inheritance

Aik class doosri se aur teesri class us doosri se inherit karti hai.

Grandparent

Parent

Child

4. Hierarchical Inheritance

Aik parent class se multiple child classes inherit karti hain.

Parent

Child A

Child B

Child C

5. Hybrid Inheritance

Jab inheritance ki multiple types combine hoti hain, use hybrid inheritance kehte hain.

Multiple inheritance mein agar parent classes mein same method ho, to Python ka Method Resolution Order (MRO) decide karta hai ke kaunsa method use hoga.

# 9. `super()` function

`super()` ka use parent class ke methods ko child class se call karne ke liye hota hai.

Python

Run

```
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

Output:

```
Tommy
German Shepherd
```

`super().__init__(name)` parent class ka constructor call karta hai. Is se `name` initialize ho jata hai aur child class apna `breed` attribute bhi add kar sakti hai.

# 10. Polymorphism

Polymorphism ka matlab hai aik hi interface ya method ka different objects ke liye different behavior hona.

Example:

Python

Run

```
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

Output:

```
Bark
Meow
```

Dono classes mein `sound()` method hai, lekin dono ka behavior different hai.

Python mein polymorphism duck typing ke zariye bhi hota hai. Matlab object ki actual class se zyada important ye hai ke us mein required method available hai ya nahi.

# 11. Method Overriding

Jab child class parent class ke method ko apne tareeqe se dobara define karti hai, to isay method overriding kehte hain.

Python

Run

```
class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

dog = Dog()
dog.sound()
```

Output:

```
Bark
```

Yahan `Dog` ne parent ka `sound()` method override kar diya hai.

Agar parent ka method bhi execute karna ho, to `super()` use kar sakte hain.

Python

Run

```
class Dog(Animal):
    def sound(self):
        super().sound()
        print("Bark")
```

Output:

```
Animal sound
Bark
```

# 12. Abstraction

Abstraction ka matlab hai implementation ki unnecessary details chhupa kar user ko sirf zaroori interface dena.

Python mein `abc` module ke zariye abstract classes banayi ja sakti hain.

Python

Run

```
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

Output:

```
50
```

`Shape` aik abstract class hai. Is ka `area()` abstract method hai. Child class `Rectangle` ko `area()` implement karna zaroori hai, warna uska object create nahi ho sakta.

Abstract class ka direct object bhi create nahi kar sakte.

# 13. Properties — `@property`

`@property` ki madad se hum method ko attribute ki tarah access kar sakte hain. Iska use data ko validate ya controlled access dene ke liye hota hai.

Python

Run

```
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

Output:

```
5000
6000
```

Yahan `salary` method ko hum `emp.salary` ki tarah access kar rahe hain.

* `@property` getter define karta hai.

* `@salary.setter` value set karne ka tareeqa define karta hai.

* Setter mein validation bhi kar sakte hain.


# 14. Special Methods (Dunder Methods)

Python mein kuch methods ke naam ke start aur end mein double underscores hote hain. Inhein dunder methods kehte hain.

Ye Python ke built-in operations ke sath classes ko kaam karne ke qabil banate hain.

|
Method

|

Kaam

|
| --- | --- |
|

`__init__()`

|

Object initialize karta hai

|
|

`__str__()`

|

Object ki readable string deta hai

|
|

`__repr__()`

|

Object ki developer-friendly representation deta hai

|
|

`__len__()`

|

`len()` ka behavior define karta hai

|
|

`__eq__()`

|

`==` ka behavior define karta hai

|
|

`__lt__()`

|

`<` ka behavior define karta hai

|
|

`__add__()`

|

`+` ka behavior define karta hai

|
|

`__del__()`

|

Object destroy hone par call ho sakta hai

|

Example:

Python

Run

```
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __str__(self):
        return f"{self.name}: {self.salary}"

emp = Employee("Ali", 5000)

print(emp)
```

Output:

```
Ali: 5000
```

Agar `__str__()` define na ho, to `print(emp)` aam tor par object ki default representation dikhata hai.

Ek aur example `__add__()` ka:

Python

Run

```
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value

a = Number(10)
b = Number(20)

print(a + b)
```

Output:

```
30
```

Yahan `a + b` internally `a.__add__(b)` ko call karta hai.

# 15. Composition aur Aggregation

Ye dono OOP mein objects ke darmiyan relationships define karte hain.

Composition

Aik object doosre object ka essential part hota hai. Dono ki lifecycle aksar closely linked hoti hai.

Example: Car aur uska Engine.

Python

Run

```
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

Car apna Engine object khud create karti hai.

Aggregation

Aik object doosre object ko use karta hai, lekin dono independently exist kar sakte hain.

Example: Department aur Employee.

Python

Run

```
class Employee:
    def __init__(self, name):
        self.name = name

class Department:
    def __init__(self, employee):
        self.employee = employee

emp = Employee("Ali")
dept = Department(emp)
```

Employee pehle se independently exist karta hai aur Department uska reference rakhta hai.

Python mein composition aur aggregation ko language enforce nahi karti. Ye object relationships ko design karne ke concepts hain.

# 16. Nested Classes

Jab aik class ke andar doosri class define ki jati hai, to usay nested class kehte hain.

Python

Run

```
class Computer:
    class CPU:
        def process(self):
            print("CPU processing")

computer = Computer()
cpu = Computer.CPU()

cpu.process()
```

Output:

```
CPU processing
```

Nested class apne aap outer class ke object se connected nahi hoti. Isay tab use karna chahiye jab inner class logically outer class se closely related ho.

# 17. Class Attributes aur `__dict__`

Python objects aur classes ke attributes ko inspect karne ke liye `__dict__` use kar sakte hain.

Python

Run

```
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

emp = Employee("Ali")

print(emp.__dict__)
print(Employee.__dict__["company"])
```

Output:

```
{'name': 'Ali'}
ABC
```

`emp.__dict__` instance ke attributes dikhata hai. `Employee.__dict__` class ke attributes aur methods ka mapping deta hai.

# 18. Class mein methods ko call karna

Aik method doosre method ko bhi call kar sakta hai.

Python

Run

```
class Calculator:
    def add(self, a, b):
        return a + b

    def calculate(self):
        result = self.add(10, 20)
        print(result)

calc = Calculator()
calc.calculate()
```

Output:

```
30
```

`self.add()` current object ka `add()` method call karta hai.

# 19. Practical example: Employee Management System

Ab in concepts ko aik chhote practical example mein combine karte hain.

Python

Run

```
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

Output:

```
Name: Nouman
Salary: 8000
Company: ABC
Department: HVAC
```

Is example mein:

* `Employee` parent class hai.

* `Manager` child class hai.

* `__init__()` object initialize karta hai.

* `self` current object ko represent karta hai.

* `company` class variable hai.

* `salary` property hai.

* `super()` parent class ke constructor aur method ko call karta hai.

* `show_details()` child class mein override hua hai.

# 20. Python Classes ka complete revision

|
Concept

|

Purpose

|
| --- | --- |
|

Class

|

Object banane ka blueprint

|
|

Object

|

Class ka instance

|
|

Attribute

|

Object ya class ka data

|
|

Method

|

Class ke andar function

|
|

`self`

|

Current instance

|
|

`__init__`

|

Object initialization

|
|

Instance variable

|

Har object ka apna data

|
|

Class variable

|

Class-level shared data

|
|

`@classmethod`

|

Class ko `cls` ke zariye access karna

|
|

`@staticmethod`

|

Class se related utility method

|
|

Encapsulation

|

Data aur methods ko organize karna, controlled access dena

|
|

Inheritance

|

Parent class se functionality lena

|
|

Polymorphism

|

Aik interface, mukhtalif behavior

|
|

Abstraction

|

Interface define karna, implementation details chhupana

|
|

Overriding

|

Parent method ka child mein naya implementation

|
|

`super()`

|

Parent class ke methods tak access

|
|

`@property`

|

Method ko attribute ki tarah access karna

|
|

Dunder methods

|

Built-in Python operations customize karna

|
|

Composition

|

Objects ko doosre objects ke parts ke taur par use karna

|
|

Aggregation

|

Independently existing objects ko associate karna

|
|

MRO

|

Multiple inheritance mein method lookup order

|

# Practice: Apni understanding check karein

1. Class ka main purpose kya hai?

Sirf variables store karna

Objects banane ka blueprint dena

Sirf loops chalana

2. `self` kya represent karta hai?

Parent class

Current object

Python interpreter

3. `@classmethod` mein aam tor par kaunsa parameter hota hai?

self

cls

this

4. Inheritance ka kya faida hai?

Code reuse

Variables delete karna

Loop rokna

5. `@property` ka kya faida hai?

Method ko attribute ki tarah access karna

Object delete karna

Class inherit karna

Check Answers

Learning order: Pehle Class, Object, `self`, `__init__` aur variables par practice karein. Us ke baad methods, inheritance, encapsulation, polymorphism aur abstraction par projects banayein. Is tarah Python OOP ki foundation mazboot hogi.

# Lesson 5: Instance Method, Class Method aur Static Method

Ab hum classes ke **3 important method types** detail mein samjhenge:

1. **Instance Method** → `self`
2. **Class Method** → `@classmethod` + `cls`
3. **Static Method** → `@staticmethod`

Sab se pehle basic difference:

| Method          | Pehla parameter                     | Kis cheez ke sath kaam? |
| --------------- | ----------------------------------- | ----------------------- |
| Instance Method | `self`                              | Object                  |
| Class Method    | `cls`                               | Class                   |
| Static Method   | koi required special parameter nahi | Independent logic       |

---

# 1. Instance Method

Instance method woh normal method hai jo **object ke data** ke sath kaam karta hai.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def show_details(self):
        print(self.name)
        print(self.salary)


emp1 = Employee("Ali", 5000)

emp1.show_details()
```

Output:

```text
Ali
5000
```

Yahan:

```python
def show_details(self):
```

mein `self` current object ko represent karta hai.

Jab hum:

```python
emp1.show_details()
```

likhte hain, to conceptually Python isay:

```python
Employee.show_details(emp1)
```

ki tarah treat karta hai.

Is liye `self` ke andar `emp1` aa jata hai.

---

# 2. Instance Method object ka data change kar sakta hai

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def increase_salary(self, amount):
        self.salary += amount


emp1 = Employee("Ali", 5000)

emp1.increase_salary(1000)

print(emp1.salary)
```

Output:

```text
6000
```

`self.salary` current object ki salary hai.

Is liye:

```python
self.salary += amount
```

current object ki salary change karta hai.

---

# 3. Class Method

Class method object ke bajaye **class ke sath kaam karta hai**.

Iske liye:

```python
@classmethod
```

decorator use hota hai.

Aur first parameter aam tor par:

```python
cls
```

hota hai.

Example:

```python
class Employee:
    company = "ABC"

    @classmethod
    def show_company(cls):
        print(cls.company)


Employee.show_company()
```

Output:

```text
ABC
```

Yahan:

```python
cls.company
```

ka matlab hai:

**current class ka `company` attribute**.

---

# 4. `self` vs `cls`

Ye difference bohat important hai.

### `self`

```python
self.name
```

Matlab:

> Current **object** ka `name`

### `cls`

```python
cls.company
```

Matlab:

> Current **class** ka `company`

Example:

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name

    def show_employee(self):
        print(self.name)

    @classmethod
    def show_company(cls):
        print(cls.company)
```

Yahan:

```python
self.name
```

object-specific hai.

Aur:

```python
cls.company
```

class-level hai.

---

# 5. Class Method ka practical use

Class method ka aik bohat important use **alternative constructor** banana hai.

Suppose data is format mein aa raha hai:

```text
"Nouman,5000"
```

Hum is string se Employee object banana chahte hain.

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

Output:

```text
Nouman
5000
```

Yahan:

```python
Employee.from_string(...)
```

class method hai.

Aur:

```python
return cls(name, int(salary))
```

current class ka object create kar raha hai.

Ye **alternative constructor** kehlata hai.

---

# 6. `cls` kyun use karte hain?

Agar hum directly:

```python
Employee(...)
```

likh dein to method specifically `Employee` class ke sath tied ho jayega.

Lekin:

```python
cls(...)
```

use karne se method inherited classes ke sath bhi zyada flexible rehta hai.

Example:

```python
class Employee:
    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name):
        return cls(name)


class Manager(Employee):
    pass


manager = Manager.create("Ali")

print(type(manager))
```

Output:

```text
<class '__main__.Manager'>
```

`cls` ki wajah se `Manager.create()` ne `Manager` ka object create kiya.

---

# 7. Static Method

Ab third type:

```python
@staticmethod
```

Static method mein automatically `self` ya `cls` pass nahi hota.

Example:

```python
class Calculator:

    @staticmethod
    def add(a, b):
        return a + b


result = Calculator.add(10, 20)

print(result)
```

Output:

```text
30
```

Yahan:

```python
add(a, b)
```

ko na object ki zaroorat hai aur na class data ki.

Ye sirf calculation kar raha hai.

---

# 8. Static Method kab use karein?

Jab koi function logically class se related ho, lekin usay:

* object ka data nahi chahiye
* class ka data nahi chahiye

to static method useful ho sakta hai.

Example:

```python
class Temperature:

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return (celsius * 9 / 5) + 32


print(Temperature.celsius_to_fahrenheit(25))
```

Output:

```text
77.0
```

`celsius_to_fahrenheit()` ko kisi Employee ya Temperature object ki zaroorat nahi.

---

# 9. Teenon ko aik hi class mein dekho

```python
class Employee:

    company = "ABC"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # Instance Method
    def show_employee(self):
        print(self.name)
        print(self.salary)

    # Class Method
    @classmethod
    def show_company(cls):
        print(cls.company)

    # Static Method
    @staticmethod
    def calculate_bonus(salary):
        return salary * 0.10
```

Ab use karte hain:

```python
emp = Employee("Nouman", 5000)
```

### Instance Method

```python
emp.show_employee()
```

Object ka data use karega.

### Class Method

```python
Employee.show_company()
```

Class ka data use karega.

### Static Method

```python
bonus = Employee.calculate_bonus(5000)
print(bonus)
```

Sirf calculation karega.

---

# 10. Simple mental model

Isko yaad rakhne ka easiest tareeqa:

### `self` → "Mera object"

```python
self.name
self.salary
```

Matlab:

> Is particular object ka data.

### `cls` → "Meri class"

```python
cls.company
cls(...)
```

Matlab:

> Current class ka data ya current class ka object.

### `staticmethod` → "Mujhe object/class ki zaroorat nahi"

```python
@staticmethod
def add(a, b):
```

Sirf given inputs par kaam karega.

---

# 11. Important comparison

```text
                    METHOD
                      |
          ┌───────────┼───────────┐
          ↓           ↓           ↓
      Instance      Class       Static
       Method       Method       Method
          |           |           |
        self         cls         none
          |           |           |
       Object       Class      Independent
        data         data        logic
```

## Example

```python
class Test:

    x = 100

    def instance_method(self):
        print(self)

    @classmethod
    def class_method(cls):
        print(cls)

    @staticmethod
    def static_method():
        print("Hello")
```

---

# 12. Ek common mistake

Ye ghalat hai:

```python
class Employee:

    def show(self):
        print("Hello")


Employee.show()
```

Kyun?

Kyunkay `show()` instance method hai aur usay `self` chahiye.

Correct:

```python
emp = Employee()

emp.show()
```

Ya technically:

```python
Employee.show(emp)
```

---

# 13. Class method mein bhi same concept

```python
class Employee:

    @classmethod
    def show(cls):
        print(cls)


Employee.show()
```

Yahan object ki zaroorat nahi kyun ke `cls` automatically class ko represent karta hai.

---

# 14. Final rule

**Instance Method:**

```python
def method(self):
```

Use when **object ka data** chahiye.

**Class Method:**

```python
@classmethod
def method(cls):
```

Use when **class ka data / class-level construction** chahiye.

**Static Method:**

```python
@staticmethod
def method():
```

Use when **neither object nor class state** ki zaroorat ho.

---

### Practice

Is code ka output khud predict karo:

```python
class Employee:

    company = "ABC"

    def __init__(self, name):
        self.name = name

    def show_name(self):
        print(self.name)

    @classmethod
    def show_company(cls):
        print(cls.company)

    @staticmethod
    def add(a, b):
        return a + b


emp = Employee("Nouman")

emp.show_name()
Employee.show_company()
print(Employee.add(10, 20))
```

Expected output kya hoga?

**Next lesson:** **Encapsulation** — public, `_protected`, `__private`, name mangling, getters/setters aur `@property` ko detail mein samjhenge.

# Lesson 6: Encapsulation in Python

Ab hum **Encapsulation** samjhenge. Ye OOP ka important concept hai.

Simple words mein:

> **Encapsulation ka matlab hai data aur us data par kaam karne wale methods ko aik class ke andar organize karna, aur zaroorat ke mutabiq data ki access ko control karna.**

Python mein encapsulation samajhne ke liye 4 cheezen important hain:

1. Public
2. `_protected` convention
3. `__private`
4. `@property` — getter/setter

---

## 1. Public Attribute

Python mein normal attribute **public** hota hai.

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
```

Ab:

```python
emp = Employee("Ali", 5000)

print(emp.name)
print(emp.salary)
```

Output:

```text
Ali
5000
```

Aur hum directly change bhi kar sakte hain:

```python
emp.salary = 7000
```

Yani:

```python
self.salary
```

public hai.

---

# 2. `_protected`

Agar attribute ke start mein **single underscore** lagao:

```python
self._salary
```

to Python convention kehta hai:

> Ye internal/protected type ka data hai; normally class ke bahar directly access nahi karna chahiye.

Example:

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self._salary = salary
```

Technically Python phir bhi access allow karta hai:

```python
emp = Employee("Ali", 5000)

print(emp._salary)
```

Output:

```text
5000
```

Important:

**`_salary` actually private nahi hai.**

Python sirf developer ko signal de raha hai:

> "Is attribute ko internal samjho."

---

# 3. `__private`

Ab double underscore:

```python
self.__salary
```

Ye Python mein **name mangling** trigger karta hai.

Example:

```python
class Employee:

    def __init__(self, salary):
        self.__salary = salary
```

Ab:

```python
emp = Employee(5000)

print(emp.__salary)
```

normally error aayega:

```text
AttributeError
```

Kyun?

Kyunkay Python internally naam ko modify kar deta hai.

Conceptually:

```text
__salary
```

becomes something like:

```text
_Employee__salary
```

Isay **name mangling** kehte hain.

---

# 4. Name Mangling

Example:

```python
class Employee:

    def __init__(self, salary):
        self.__salary = salary


emp = Employee(5000)

print(emp._Employee__salary)
```

Output:

```text
5000
```

Is se aik important baat samjho:

> Python ka `__private` C++/Java jaisa absolute private nahi hai.

Python actually name ko mangle karta hai taake accidental access/name collision se protection mile.

---

# 5. Private Data ko Method ke through access karna

Suppose:

```python
class Employee:

    def __init__(self, salary):
        self.__salary = salary

    def get_salary(self):
        return self.__salary
```

Ab:

```python
emp = Employee(5000)

print(emp.get_salary())
```

Output:

```text
5000
```

Yahan:

```python
self.__salary
```

private attribute hai.

Aur:

```python
get_salary()
```

uski value provide kar raha hai.

Is concept ko **getter** kehte hain.

---

# 6. Setter

Agar salary change karni ho:

```python
class Employee:

    def __init__(self, salary):
        self.__salary = salary

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        self.__salary = salary
```

Use:

```python
emp = Employee(5000)

print(emp.get_salary())

emp.set_salary(7000)

print(emp.get_salary())
```

Output:

```text
5000
7000
```

Yahan:

```python
get_salary()
```

= getter

```python
set_salary()
```

= setter

---

# 7. Setter ka actual faida

Setter ka sab se important faida hai ke hum **validation** laga sakte hain.

Example:

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
```

Ab:

```python
emp = Employee(5000)

emp.set_salary(-1000)
```

Output:

```text
Salary cannot be negative
```

Yani direct data modification ke bajaye hum **rules enforce** kar sakte hain.

---

# 8. `@property`

Python mein getter/setter ko aur clean banane ke liye:

```python
@property
```

use hota hai.

Example:

```python
class Employee:

    def __init__(self, salary):
        self.__salary = salary

    @property
    def salary(self):
        return self.__salary
```

Ab:

```python
emp = Employee(5000)

print(emp.salary)
```

Notice karo:

Humne ye nahi likha:

```python
emp.salary()
```

Balkay:

```python
emp.salary
```

Likha.

`@property` method ko **attribute ki tarah access** karne deta hai.

---

# 9. `@property` + Setter

Ab salary ko set bhi karna hai.

```python
class Employee:

    def __init__(self, salary):
        self.__salary = salary

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):

        if value >= 0:
            self.__salary = value
        else:
            print("Salary cannot be negative")
```

Ab:

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

Lekin:

```python
emp.salary = -2000
```

Output:

```text
Salary cannot be negative
```

---

# 10. Yahan magic kya ho raha hai?

Jab hum:

```python
emp.salary
```

likhte hain, Python internally property getter call karta hai:

```python
salary()
```

Aur jab:

```python
emp.salary = 7000
```

likhte hain, Python setter call karta hai.

Yani:

```text
emp.salary
      ↓
@property
      ↓
getter
```

Aur:

```text
emp.salary = 7000
      ↓
@salary.setter
      ↓
validation
      ↓
__salary update
```

---

# 11. Real Example — HVAC Temperature

Tumhare HVAC context mein ye example useful hai:

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
```

Object:

```python
ahu = AHU(22)
```

Temperature read:

```python
print(ahu.temperature)
```

Output:

```text
22
```

Temperature change:

```python
ahu.temperature = 24
```

Valid hai.

Lekin:

```python
ahu.temperature = 50
```

Output:

```text
Temperature must be between 15 and 30°C
```

Ye encapsulation ka practical benefit hai.

---

# 12. Public vs Protected vs Private

| Syntax      | Meaning              | Python behavior                  |
| ----------- | -------------------- | -------------------------------- |
| `name`      | Public               | Direct access                    |
| `_name`     | Protected convention | Direct access possible           |
| `__name`    | Private/name-mangled | Direct normal access nahi        |
| `@property` | Controlled access    | Getter/setter ke through control |

---

# 13. Important point

Python mein:

```python
_name
```

**actual protection mechanism nahi** hai.

Aur:

```python
__name
```

bhi absolute security mechanism nahi hai.

Encapsulation ka main purpose hai:

> **Class ke internal implementation ko controlled interface ke through expose karna.**

Example:

```python
emp.salary = -5000
```

allow karne ke bajaye:

```python
if salary >= 0:
    ...
```

jaisi validation laga sakte hain.

---

# 14. Ek complete example

```python
class BankAccount:

    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):

        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):

        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Invalid withdrawal")
```

Use:

```python
account = BankAccount(1000)

print(account.balance)

account.deposit(500)

print(account.balance)

account.withdraw(300)

print(account.balance)
```

Output:

```text
1000
1500
1200
```

Yahan user directly:

```python
account.__balance
```

se balance manipulate nahi kar raha.

Instead:

```python
deposit()
withdraw()
```

ke through balance change ho raha hai.

**Ye encapsulation ka core idea hai.**

---

### Yaad rakhne ka shortcut

```text
Public
   ↓
Direct access

_protected
   ↓
"Please internal use karo"

__private
   ↓
Name mangling

@property
   ↓
Controlled access

@property + @setter
   ↓
Read + validation ke sath write
```

**Next Lesson 7:** **Inheritance** — parent class, child class, code reuse, `super()`, method overriding, single/multiple/multilevel/hierarchical inheritance.

# Lesson 7: Inheritance in Python

Ab hum **Inheritance** samjhenge.

Inheritance ka basic idea:

> **Ek class doosri class ke attributes aur methods ko reuse kar sakti hai.**

Is se code repeat karne ki zaroorat kam hoti hai.

---

## 1. Parent Class aur Child Class

Example:

```python
class Animal:

    def eat(self):
        print("Animal is eating")


class Dog(Animal):
    pass
```

Yahan:

```python
Animal
```

**Parent class** hai.

Aur:

```python
Dog
```

**Child class** hai.

`Dog` ne `Animal` se inheritance li:

```python
class Dog(Animal):
```

Ab:

```python
dog = Dog()

dog.eat()
```

Output:

```text
Animal is eating
```

Dog class mein `eat()` method likha hi nahi tha, phir bhi available hai.

Kyun?

**Dog ne Animal se inherit kiya hai.**

---

# 2. Inheritance ka main purpose

Suppose:

```python
class Dog:
    def eat(self):
        print("Eating")

    def sleep(self):
        print("Sleeping")
```

Aur phir:

```python
class Cat:
    def eat(self):
        print("Eating")

    def sleep(self):
        print("Sleeping")
```

Yahan same code repeat ho raha hai.

Inheritance se:

```python
class Animal:

    def eat(self):
        print("Eating")

    def sleep(self):
        print("Sleeping")


class Dog(Animal):
    pass


class Cat(Animal):
    pass
```

Ab `Dog` aur `Cat` dono `Animal` ke methods reuse kar sakte hain.

---

# 3. Child apna method bhi add kar sakta hai

```python
class Animal:

    def eat(self):
        print("Eating")


class Dog(Animal):

    def bark(self):
        print("Barking")
```

Ab:

```python
dog = Dog()

dog.eat()
dog.bark()
```

Output:

```text
Eating
Barking
```

Yani child class ke paas:

* Parent ke methods
* Apne khud ke methods

dono ho sakte hain.

---

# 4. Parent ka `__init__()`

Ab important concept.

```python
class Animal:

    def __init__(self, name):
        self.name = name


class Dog(Animal):
    pass
```

Ab:

```python
dog = Dog("Tommy")

print(dog.name)
```

Output:

```text
Tommy
```

Dog ne apna `__init__()` define nahi kiya.

Is liye inherited initialization use ho gayi.

---

# 5. Child ka apna `__init__()`

Agar child apna `__init__()` bana de:

```python
class Animal:

    def __init__(self, name):
        self.name = name


class Dog(Animal):

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
```

Ab:

```python
dog = Dog("Tommy", "German Shepherd")

print(dog.name)
print(dog.breed)
```

Output:

```text
Tommy
German Shepherd
```

Lekin yahan parent ka initialization code manually repeat ho gaya:

```python
self.name = name
```

Isko avoid karne ke liye `super()` use karte hain.

---

# 6. `super()`

`super()` parent class ke methods ko call karne ke liye use hota hai.

Example:

```python
class Animal:

    def __init__(self, name):
        self.name = name


class Dog(Animal):

    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
```

Ab:

```python
dog = Dog("Tommy", "German Shepherd")

print(dog.name)
print(dog.breed)
```

Output:

```text
Tommy
German Shepherd
```

Yahan:

```python
super().__init__(name)
```

ka matlab:

> Parent class ka `__init__()` call karo.

---

# 7. `super()` ka practical example

Tumhare HVAC context se:

```python
class Equipment:

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id


class AHU(Equipment):

    def __init__(self, equipment_id, airflow):
        super().__init__(equipment_id)
        self.airflow = airflow
```

Object:

```python
ahu = AHU("AHU-01", 5000)
```

Ab:

```python
print(ahu.equipment_id)
print(ahu.airflow)
```

Output:

```text
AHU-01
5000
```

Parent:

```text
Equipment
   |
   └── equipment_id
```

Child:

```text
AHU
   |
   ├── equipment_id  ← parent se
   └── airflow       ← khud ka
```

---

# 8. Method Overriding

Ab inheritance ka bohat important concept:

**Method Overriding**

Parent mein method hai:

```python
class Animal:

    def sound(self):
        print("Animal sound")
```

Child same naam ka method bana deta hai:

```python
class Dog(Animal):

    def sound(self):
        print("Bark")
```

Ab:

```python
dog = Dog()

dog.sound()
```

Output:

```text
Bark
```

Parent ka `sound()` nahi chala.

Child ne parent method ko **override** kar diya.

---

# 9. `super()` with method overriding

Kabhi child parent ka method bhi chalana chahta hai aur apna additional behavior bhi.

```python
class Animal:

    def sound(self):
        print("Animal sound")


class Dog(Animal):

    def sound(self):
        super().sound()
        print("Bark")
```

Ab:

```python
dog = Dog()

dog.sound()
```

Output:

```text
Animal sound
Bark
```

Yahan:

```python
super().sound()
```

parent ka method call karta hai.

---

# 10. Single Inheritance

Ek parent → ek child.

```text
Animal
   ↓
 Dog
```

Python:

```python
class Animal:
    pass


class Dog(Animal):
    pass
```

Isay **Single Inheritance** kehte hain.

---

# 11. Multilevel Inheritance

Chain ki tarah inheritance.

```text
Animal
   ↓
 Mammal
   ↓
 Dog
```

Example:

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
```

Ab Dog ke paas teenon levels ke methods hain:

```python
dog = Dog()

dog.eat()
dog.walk()
dog.bark()
```

Output:

```text
Eating
Walking
Barking
```

---

# 12. Hierarchical Inheritance

Ek parent ke multiple children.

```text
        Animal
       /      \
     Dog      Cat
```

Example:

```python
class Animal:

    def eat(self):
        print("Eating")


class Dog(Animal):

    def bark(self):
        print("Bark")


class Cat(Animal):

    def meow(self):
        print("Meow")
```

`Dog` aur `Cat` dono `Animal` se inherit kar rahe hain.

---

# 13. Multiple Inheritance

Ek child ke multiple parents.

```text
Parent A ──┐
           ├── Child
Parent B ──┘
```

Example:

```python
class Camera:

    def take_photo(self):
        print("Photo")


class Phone:

    def make_call(self):
        print("Calling")


class Smartphone(Camera, Phone):
    pass
```

Ab:

```python
phone = Smartphone()

phone.take_photo()
phone.make_call()
```

Output:

```text
Photo
Calling
```

`Smartphone` ne dono classes se inherit kiya.

---

# 14. Multiple Inheritance mein MRO

Multiple inheritance mein Python ko decide karna hota hai:

> Agar same method dono parents mein ho to pehle kis ka method use karna hai?

Iske liye Python **MRO — Method Resolution Order** use karta hai.

Example:

```python
class A:

    def show(self):
        print("A")


class B:

    def show(self):
        print("B")


class C(A, B):
    pass
```

Ab:

```python
c = C()

c.show()
```

Output:

```text
A
```

Kyun?

Kyunkay:

```python
class C(A, B):
```

mein `A` pehle hai.

MRO dekhne ke liye:

```python
print(C.mro())
```

Python inheritance chain show karega.

---

# 15. `isinstance()`

Ye check karta hai ke object kisi class ka instance hai ya nahi.

```python
class Animal:
    pass


class Dog(Animal):
    pass


dog = Dog()
```

Ab:

```python
print(isinstance(dog, Dog))
```

Output:

```text
True
```

Aur:

```python
print(isinstance(dog, Animal))
```

Output:

```text
True
```

Kyun ke `Dog`, `Animal` se inherit karta hai.

---

# 16. `issubclass()`

Ye classes ke beech inheritance check karta hai.

```python
print(issubclass(Dog, Animal))
```

Output:

```text
True
```

Lekin:

```python
print(issubclass(Animal, Dog))
```

Output:

```text
False
```

---

# 17. Inheritance ka complete HVAC example

```python
class Equipment:

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    def status(self):
        print("Equipment is running")


class AHU(Equipment):

    def __init__(self, equipment_id, airflow):
        super().__init__(equipment_id)
        self.airflow = airflow

    def show_airflow(self):
        print(f"Airflow: {self.airflow} CFM")

    def status(self):
        print("AHU is running")
```

Object:

```python
ahu = AHU("AHU-01", 5000)
```

Parent ka attribute:

```python
print(ahu.equipment_id)
```

Output:

```text
AHU-01
```

Child ka attribute:

```python
ahu.show_airflow()
```

Output:

```text
Airflow: 5000 CFM
```

Overridden method:

```python
ahu.status()
```

Output:

```text
AHU is running
```

Yahan:

```text
Equipment
    |
    ├── equipment_id
    └── status()
          ↑
          │ override
          │
AHU
    |
    ├── airflow
    └── show_airflow()
```

---

# 18. Inheritance ko ek line mein yaad rakho

```text
Parent Class
     ↓
Child Class
     ↓
Reuse + Extend + Override
```

### `super()`

```python
super().__init__()
```

→ Parent ka constructor.

```python
super().method()
```

→ Parent ka method.

### Override

Child same method name banaye:

```python
def status(self):
```

→ Parent ka behavior replace/customize kar sakta hai.

### `isinstance()`

```python
isinstance(object, Class)
```

→ Object ka class relationship check.

### `issubclass()`

```python
issubclass(Child, Parent)
```

→ Inheritance relationship check.

---

## Practice

Is code ka output predict karo:

```python
class Equipment:

    def start(self):
        print("Equipment started")


class AHU(Equipment):

    def start(self):
        print("AHU started")


class VAV(AHU):

    def start(self):
        super().start()
        print("VAV started")


vav = VAV()

vav.start()
```

Socho:

1. `VAV.start()` mein pehle kya chalega?
2. `super().start()` kis class ka method call karega?
3. Final output ki 2 lines kya hongi?

**Next lesson:** **Polymorphism** — same method/interface different objects ke liye different behavior kaise deta hai, duck typing, method overriding aur practical Python examples.

# Lesson 8: Polymorphism in Python

Ab hum OOP ke ek bohat important concept par hain:

> **Polymorphism = same interface/method, different objects, different behavior.**

Simple example:

```python
dog.sound()
cat.sound()
```

Dono mein method ka naam same hai:

```python
sound()
```

Lekin Dog ka behavior alag aur Cat ka behavior alag ho sakta hai.

---

## 1. Basic Example

```python
class Dog:

    def sound(self):
        print("Bark")


class Cat:

    def sound(self):
        print("Meow")
```

Ab:

```python
dog = Dog()
cat = Cat()

dog.sound()
cat.sound()
```

Output:

```text
Bark
Meow
```

Method dono classes mein:

```python
sound()
```

same hai.

Lekin behavior different hai.

**Ye polymorphism hai.**

---

# 2. Sab se important point

Polymorphism ka focus ye nahi hai ke classes same hon.

Focus ye hai:

> **Hum same operation/interface ko different objects par apply kar saken.**

Example:

```python
def make_sound(animal):
    animal.sound()
```

Ab:

```python
make_sound(dog)
make_sound(cat)
```

Output:

```text
Bark
Meow
```

Function ko ye jaanne ki zaroorat nahi ke object `Dog` hai ya `Cat`.

Usko sirf itna pata hai:

```python
animal.sound()
```

available hona chahiye.

---

# 3. Duck Typing

Python mein polymorphism ka bohat famous concept hai:

**Duck Typing**

Python ka philosophy roughly ye hai:

> Agar object required behavior provide karta hai, to uski exact class kya hai ye zaroori nahi.

Example:

```python
class Dog:

    def sound(self):
        print("Bark")


class Robot:

    def sound(self):
        print("Beep")
```

Ab:

```python
def make_sound(obj):
    obj.sound()
```

Dono kaam karenge:

```python
make_sound(Dog())
make_sound(Robot())
```

Output:

```text
Bark
Beep
```

Function ne ye check nahi kiya:

```python
if isinstance(obj, Dog):
```

Usne simply kaha:

```python
obj.sound()
```

Agar `sound()` hai → kaam karo.

---

# 4. Real-world example

Tumhare HVAC context mein:

```python
class AHU:

    def start(self):
        print("AHU fan started")


class VAV:

    def start(self):
        print("VAV damper/control started")


class Pump:

    def start(self):
        print("Pump started")
```

Ab common function:

```python
def start_equipment(equipment):
    equipment.start()
```

Ab:

```python
start_equipment(AHU())
start_equipment(VAV())
start_equipment(Pump())
```

Output:

```text
AHU fan started
VAV damper/control started
Pump started
```

Function:

```python
start_equipment()
```

same hai.

Lekin object ke according behavior change ho gaya.

---

# 5. Method Overriding bhi Polymorphism ka example hai

Inheritance mein humne dekha:

```python
class Equipment:

    def start(self):
        print("Equipment started")


class AHU(Equipment):

    def start(self):
        print("AHU started")
```

Aur:

```python
class VAV(Equipment):

    def start(self):
        print("VAV started")
```

Ab:

```python
equipment_list = [
    AHU(),
    VAV()
]
```

Loop:

```python
for equipment in equipment_list:
    equipment.start()
```

Output:

```text
AHU started
VAV started
```

Same:

```python
equipment.start()
```

different objects ke liye different behavior.

**Ye polymorphism hai.**

---

# 6. Polymorphism + Inheritance

Common structure:

```text
             Equipment
                 |
        ┌────────┼────────┐
        ↓        ↓        ↓
       AHU      VAV      Pump
        |        |        |
      start()  start()  start()
```

Parent define karta hai common interface:

```python
start()
```

Child classes apna behavior provide karti hain.

---

# 7. Python mein formal interface zaroori nahi

Kuch languages mein interface explicitly define karna common hai.

Python mein duck typing ki wajah se zaroori nahi.

Example:

```python
class AHU:

    def start(self):
        print("AHU started")


class VAV:

    def start(self):
        print("VAV started")
```

Dono ka parent hona bhi zaroori nahi.

Phir bhi:

```python
def start_equipment(equipment):
    equipment.start()
```

dono ke sath kaam karega.

Ye Python ki flexibility hai.

---

# 8. Operator Polymorphism

Polymorphism sirf methods mein nahi hota.

Operators bhi different types ke liye different behavior dete hain.

Example:

```python
print(10 + 20)
```

Output:

```text
30
```

Lekin:

```python
print("Hello " + "World")
```

Output:

```text
Hello World
```

`+` ka behavior data type ke according change ho gaya.

Numbers:

```text
10 + 20 → addition
```

Strings:

```text
"Hello" + "World" → concatenation
```

Ye bhi polymorphic behavior ka example hai.

---

# 9. Built-in `len()` bhi polymorphism

Dekho:

```python
print(len("Python"))
```

Output:

```text
6
```

List:

```python
print(len([10, 20, 30]))
```

Output:

```text
3
```

Dictionary:

```python
print(len({"a": 1, "b": 2}))
```

Output:

```text
2
```

Same function:

```python
len()
```

Different objects ke sath kaam kar raha hai.

Ye Python ke polymorphic design ka acha example hai.

---

# 10. Abstract Base Class ke sath Polymorphism

Ab thora advanced concept.

Python mein `abc` module use karke hum abstract interface define kar sakte hain.

```python
from abc import ABC, abstractmethod


class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass
```

Ab child class ko `start()` implement karna hoga:

```python
class AHU(Equipment):

    def start(self):
        print("AHU started")
```

Aur:

```python
class VAV(Equipment):

    def start(self):
        print("VAV started")
```

Ab:

```python
def start_equipment(equipment):
    equipment.start()
```

Use:

```python
start_equipment(AHU())
start_equipment(VAV())
```

Output:

```text
AHU started
VAV started
```

Yahan `Equipment` ek common contract/interface jaisa role play kar raha hai.

---

# 11. Polymorphism ka benefit

Suppose tumhare paas 100 equipment hain:

```python
equipment_list = [
    AHU(),
    VAV(),
    Pump(),
    AHU(),
    VAV()
]
```

Tumhe alag-alag:

```python
if equipment is AHU:
    ...

elif equipment is VAV:
    ...

elif equipment is Pump:
    ...
```

likhne ki zaroorat nahi.

Simply:

```python
for equipment in equipment_list:
    equipment.start()
```

Ye **clean aur extensible code** banata hai.

Agar kal:

```python
Chiller
```

add kar do:

```python
class Chiller(Equipment):

    def start(self):
        print("Chiller started")
```

To existing loop change karne ki zaroorat nahi:

```python
for equipment in equipment_list:
    equipment.start()
```

---

# 12. Polymorphism vs Inheritance

Dono related hain lekin same cheez nahi.

### Inheritance

Question:

> "Ye class kis class se properties/methods inherit karti hai?"

Example:

```python
class AHU(Equipment):
```

### Polymorphism

Question:

> "Same interface/method different objects par kaise different behavior de raha hai?"

Example:

```python
ahu.start()
vav.start()
pump.start()
```

---

# 13. Polymorphism vs Method Overriding

**Method overriding** ek technique hai.

```python
class Parent:

    def show(self):
        print("Parent")


class Child(Parent):

    def show(self):
        print("Child")
```

**Polymorphism** broader concept hai:

```python
for obj in objects:
    obj.show()
```

Har object apne `show()` implementation ke according behavior karega.

---

# 14. Four OOP pillars ab tak

Ab tumne Python OOP ke major pillars cover kar liye:

```text
             OOP
              |
    ┌─────────┼─────────┐
    ↓         ↓         ↓
Encapsulation Inheritance Polymorphism
              |
          Abstraction
```

Aur basic foundation:

```text
Class
Object
Attributes
Methods
```

### Encapsulation

Data ko controlled way mein manage karna.

### Inheritance

Existing class ka code reuse/extend karna.

### Polymorphism

Same interface, different behavior.

### Abstraction

Complex implementation ko hide karke sirf required interface expose karna.

---

## Practice

Is code ka output predict karo:

```python
class AHU:

    def start(self):
        print("AHU started")


class VAV:

    def start(self):
        print("VAV started")


class Pump:

    def start(self):
        print("Pump started")


def run_equipment(equipment):
    equipment.start()


equipment = [
    AHU(),
    VAV(),
    Pump()
]

for item in equipment:
    run_equipment(item)
```

Output:

```text
?
?
?
```

Yahan important question ye hai:

**`run_equipment()` ko kaise pata chalta hai ke `item` AHU hai, VAV hai ya Pump?**

Answer: **Usay pata hona zaroori hi nahi.** Wo sirf required behavior `start()` ko call karta hai. یہی Python ka **duck typing / polymorphism** concept hai.

**Next Lesson 9: Abstraction** — `ABC`, `@abstractmethod`, abstract class, interface-like design, aur `Protocol` se iska connection.

# Lesson 9: Abstraction in Python

Abstraction OOP ka **4th major pillar** hai.

Ab tak:

1. **Encapsulation** → data ko control karna
2. **Inheritance** → code reuse karna
3. **Polymorphism** → same interface, different behavior
4. **Abstraction** → unnecessary implementation details hide karna

Simple definition:

> **Abstraction ka matlab hai user ko "kya karna hai" batana, lekin "andar kaise ho raha hai" ki detail zaroori na banana.**

---

# 1. Real-life example

Socho tum **AC thermostat** use karte ho.

Tum temperature set karte ho:

```text
Set Temperature → 22°C
```

Lekin tumhe ye nahi karna padta:

```text
compressor kaise operate hua?
refrigerant kaise circulate hua?
fan motor kaise control hui?
valve kitna open hua?
```

Ye internal implementation hai.

Tumhe sirf interface milta hai:

```text
set_temperature(22)
```

Ye abstraction ka basic idea hai.

---

# 2. Python mein abstraction kaise?

Python mein commonly:

```python
from abc import ABC, abstractmethod
```

use karte hain.

Example:

```python id="5x6p8c"
from abc import ABC, abstractmethod


class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass
```

Yahan `Equipment` **abstract class** hai.

Aur:

```python
@abstractmethod
def start(self):
```

ek **abstract method** hai.

---

# 3. Abstract class ka purpose

Ab:

```python id="6t6x8m"
class AHU(Equipment):

    def start(self):
        print("AHU started")
```

Aur:

```python id="9h6x2w"
class VAV(Equipment):

    def start(self):
        print("VAV started")
```

Dono `Equipment` se inherit kar rahe hain.

`Equipment` basically keh raha hai:

> Har equipment ke paas `start()` method hona chahiye.

Lekin `Equipment` ye decide nahi kar raha ke:

> AHU kaise start hoga?

Ye child class decide karegi.

---

# 4. Abstract class ka object nahi bana sakte

Ye:

```python id="4xq8qf"
equipment = Equipment()
```

error dega.

Kyun?

Kyunkay `Equipment` mein abstract method hai:

```python id="8c9b4s"
start()
```

Aur uski actual implementation nahi hai.

Abstract class ka purpose normally **base design/contract** provide karna hai, direct object banana nahi.

---

# 5. Child class implementation provide karti hai

```python id="1cz7m9"
from abc import ABC, abstractmethod


class Equipment(ABC):

    @abstractmethod
    def start(self):
        pass


class AHU(Equipment):

    def start(self):
        print("AHU started")
```

Ab:

```python id="d4h7nf"
ahu = AHU()

ahu.start()
```

Output:

```text
AHU started
```

Kyun?

Kyunkay `AHU` ne required abstract method:

```python
start()
```

implement kar diya.

---

# 6. Agar child method implement na kare?

```python id="q7m0a1"
class VAV(Equipment):
    pass
```

Ab:

```python id="b0p2j7"
vav = VAV()
```

error aayega.

Kyun?

`VAV` ne:

```python
start()
```

implement nahi kiya.

Yani abstract class child class ko **required interface** enforce kar rahi hai.

---

# 7. `pass` ka kya matlab?

Ye:

```python id="y4z8xq"
def start(self):
    pass
```

ka matlab ye nahi ke actual equipment start ho raha hai.

Yahan `pass` sirf placeholder hai.

Matlab:

> "Method required hai, actual implementation child class provide karegi."

---

# 8. HVAC example

Ye abstraction ka bohat practical example hai:

```python id="3z7q5d"
from abc import ABC, abstractmethod


class HVACEquipment(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
```

Ab AHU:

```python id="d7v3k9"
class AHU(HVACEquipment):

    def start(self):
        print("AHU fan started")

    def stop(self):
        print("AHU fan stopped")
```

VAV:

```python id="j8n1x4"
class VAV(HVACEquipment):

    def start(self):
        print("VAV control started")

    def stop(self):
        print("VAV control stopped")
```

Ab user simply:

```python id="4m6tq2"
ahu = AHU()

ahu.start()
ahu.stop()
```

Output:

```text
AHU fan started
AHU fan stopped
```

User ko internal implementation ki detail nahi chahiye.

---

# 9. Abstraction + Polymorphism

Dono concepts bohat closely related hain.

```python id="h2v5s9"
equipment_list = [
    AHU(),
    VAV()
]

for equipment in equipment_list:
    equipment.start()
```

Output:

```text
AHU fan started
VAV control started
```

Yahan:

### Abstraction

`HVACEquipment` kehta hai:

```python
start()
stop()
```

available hone chahiye.

### Polymorphism

Actual object decide karta hai:

```text
AHU → AHU fan started
VAV → VAV control started
```

---

# 10. Abstract class mein normal methods bhi ho sakte hain

Abstract class ka matlab ye nahi ke **har method abstract** hona chahiye.

Example:

```python id="3m5v7c"
from abc import ABC, abstractmethod


class Equipment(ABC):

    def show_id(self):
        print("Equipment ID")

    @abstractmethod
    def start(self):
        pass
```

Ab:

```python id="k6s2p8"
class AHU(Equipment):

    def start(self):
        print("AHU started")
```

`AHU` ko `start()` implement karna padega.

Lekin:

```python
show_id()
```

already parent mein implemented hai.

---

# 11. Abstract property

Ab thora advanced concept.

`@abstractmethod` sirf methods ke liye nahi, property ke sath bhi use ho sakta hai.

```python id="8v3m1r"
from abc import ABC, abstractmethod


class Equipment(ABC):

    @property
    @abstractmethod
    def equipment_id(self):
        pass
```

Child:

```python id="k4d7p1"
class AHU(Equipment):

    def __init__(self, equipment_id):
        self._equipment_id = equipment_id

    @property
    def equipment_id(self):
        return self._equipment_id
```

Ab:

```python id="n9c4x2"
ahu = AHU("AHU-001")

print(ahu.equipment_id)
```

Output:

```text
AHU-001
```

Yani abstraction properties par bhi apply ho sakti hai.

---

# 12. `ABC` kya hai?

```python
from abc import ABC
```

`ABC` ka matlab:

**Abstract Base Class**

Jab class:

```python
class Equipment(ABC):
```

likhte ho, tum indicate kar rahe ho ke ye class abstract base class ke taur par use ho sakti hai.

---

# 13. `@abstractmethod` kya karta hai?

```python
@abstractmethod
def start(self):
    pass
```

Ye child classes ke liye requirement define karta hai.

Matlab:

> Jo concrete class `Equipment` se inherit karegi, usay `start()` implement karna hoga.

---

# 14. Abstraction aur Encapsulation ka difference

Ye dono aksar confuse hote hain.

### Encapsulation

Focus:

> **Data ko kaise control/protect/manage karna hai?**

Example:

```python id="x6p3q8"
self.__salary
```

aur:

```python id="p4k7s1"
@property
```

### Abstraction

Focus:

> **User ko kya interface dena hai aur implementation details ko kaise hide karna hai?**

Example:

```python id="u8m2z5"
start()
stop()
```

Simple comparison:

```text
Encapsulation
→ Data access control

Abstraction
→ Complexity hide + required interface define
```

---

# 15. Abstraction vs Inheritance

Inheritance:

```python id="f1x8n3"
class AHU(Equipment):
```

ka matlab:

> AHU, Equipment se inherit kar raha hai.

Abstraction:

```python id="w5r2k7"
@abstractmethod
def start(self):
```

ka matlab:

> Equipment require karta hai ke child `start()` provide kare.

Dono ek sath use ho sakte hain.

---

# 16. Abstraction ka real software benefit

Suppose tumhara program 100 different equipment handle karta hai:

```text
AHU
VAV
Chiller
Pump
Fan
FCU
...
```

Tum common interface define kar sakte ho:

```python
start()
stop()
```

Phir application ko sirf interface se deal karna hai:

```python
equipment.start()
```

Har equipment apni internal implementation rakhega.

Is se code:

* modular
* maintainable
* extensible

ban sakta hai.

---

# 17. Complete Example

```python id="q1v6s8"
from abc import ABC, abstractmethod


class Equipment(ABC):

    def __init__(self, equipment_id):
        self.equipment_id = equipment_id

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def show_id(self):
        print(f"Equipment ID: {self.equipment_id}")


class AHU(Equipment):

    def start(self):
        print("AHU started")

    def stop(self):
        print("AHU stopped")


class VAV(Equipment):

    def start(self):
        print("VAV started")

    def stop(self):
        print("VAV stopped")
```

Use:

```python id="x8n2c4"
ahu = AHU("AHU-001")
vav = VAV("VAV-001")

ahu.show_id()
ahu.start()
ahu.stop()

vav.show_id()
vav.start()
vav.stop()
```

Output:

```text
Equipment ID: AHU-001
AHU started
AHU stopped

Equipment ID: VAV-001
VAV started
VAV stopped
```

Yahan:

```text
Equipment
    │
    ├── common data
    │     equipment_id
    │
    ├── abstract interface
    │     start()
    │     stop()
    │
    └── common implementation
          show_id()
```

Aur:

```text
       Equipment
       /       \
      ↓         ↓
     AHU       VAV
      |         |
   start()   start()
   stop()    stop()
```

---

# 18. Abstraction ko yaad rakhne ka shortcut

```text
ABC
 ↓
Abstract Base Class
 ↓
Common design/interface

@abstractmethod
 ↓
Child ko ye method implement karna hoga
```

Aur:

```text
Encapsulation → "Data ko control kaise karna hai?"

Inheritance   → "Code reuse kaise karna hai?"

Polymorphism  → "Same interface par different behavior kaise?"

Abstraction   → "Required interface kya hai, implementation details hide kaise?"
```

## OOP ke 4 pillars complete

Ab tumhare paas Python OOP ka core structure hai:

```text
                 OOP
                  │
      ┌───────────┼───────────┐
      ↓           ↓           ↓
Encapsulation  Inheritance  Polymorphism
                  │
                  ↓
              Abstraction
```

**Next Lesson 10:** `__str__`, `__repr__`, `__eq__`, `__len__`, `__add__` jaise **Magic/Dunder Methods** — yani Python mein `__name__` wale methods kaise kaam karte hain aur operator overloading kaise hoti hai.

# Lesson 10: Magic / Dunder Methods in Python

Ab hum Python classes ke ek bohat important concept par hain:

> **Dunder methods** woh special methods hain jin ka naam `__` se start aur `__` par end hota hai.

Example:

```python
__init__
__str__
__repr__
__eq__
__len__
__add__
```

`dunder` = **double underscore**.

Ye methods Python ko batate hain ke tumhari custom class ke objects built-in Python operations ke sath kaise behave karein.

---

# 1. `__init__` — already seen

Sab se pehle:

```python
class Employee:

    def __init__(self, name):
        self.name = name
```

Jab:

```python
emp = Employee("Ali")
```

likhte ho, Python object initialization ke process mein `__init__()` call karta hai.

---

# 2. `__str__`

Ye bohat important hai.

Suppose:

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
```

Ab:

```python
emp = Employee("Ali", 5000)

print(emp)
```

Output kuch is type ka ho sakta hai:

```text
<__main__.Employee object at 0x...>
```

Ye human-friendly nahi hai.

Hum `__str__()` define kar sakte hain:

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __str__(self):
        return f"{self.name} - {self.salary}"
```

Ab:

```python
emp = Employee("Ali", 5000)

print(emp)
```

Output:

```text
Ali - 5000
```

### Simple rule:

```python
__str__
```

→ object ka **human-readable representation**.

---

# 3. `__str__` kab call hota hai?

Jab:

```python
print(emp)
```

likhte ho, Python `__str__()` ko use kar sakta hai.

Aur:

```python
str(emp)
```

bhi `__str__()` ko use karta hai.

Example:

```python
print(str(emp))
```

---

# 4. `__repr__`

Ab `__repr__()`.

Ye object ka **developer-oriented representation** provide karta hai.

Example:

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __repr__(self):
        return f"Employee({self.name!r}, {self.salary!r})"
```

Ab:

```python
emp = Employee("Ali", 5000)

print(repr(emp))
```

Output:

```text
Employee('Ali', 5000)
```

`repr()` ka focus debugging/development representation par hota hai.

---

# 5. `__str__` vs `__repr__`

Ye difference yaad rakho:

### `__str__`

Human ke liye:

```text
Ali - 5000
```

### `__repr__`

Developer/debugging ke liye:

```text
Employee('Ali', 5000)
```

Example:

```python
class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __str__(self):
        return f"{self.name} - {self.salary}"

    def __repr__(self):
        return f"Employee({self.name!r}, {self.salary!r})"
```

---

# 6. `__eq__` — `==` operator

Ab operator overloading samjho.

Suppose:

```python
class Employee:

    def __init__(self, name):
        self.name = name
```

Do objects:

```python
emp1 = Employee("Ali")
emp2 = Employee("Ali")
```

Ab:

```python
print(emp1 == emp2)
```

Normally:

```text
False
```

Kyun?

Dono separate objects hain.

Agar hum chahte hain ke same name wale employees equal consider hon:

```python
class Employee:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name
```

Ab:

```python
emp1 = Employee("Ali")
emp2 = Employee("Ali")

print(emp1 == emp2)
```

Output:

```text
True
```

Yahan:

```python
==
```

internally `__eq__()` se related hai.

---

# 7. `__eq__` mein `other`

```python
def __eq__(self, other):
```

Yahan:

```python
self
```

left-side object hai.

Aur:

```python
other
```

right-side object.

For:

```python
emp1 == emp2
```

conceptually:

```python
emp1.__eq__(emp2)
```

---

# 8. `__lt__`, `__gt__`

Comparison operators bhi customize kar sakte ho.

### `<`

```python
__lt__
```

### `>`

```python
__gt__
```

Example:

```python
class Employee:

    def __init__(self, salary):
        self.salary = salary

    def __lt__(self, other):
        return self.salary < other.salary
```

Ab:

```python
emp1 = Employee(5000)
emp2 = Employee(7000)

print(emp1 < emp2)
```

Output:

```text
True
```

---

# 9. `__add__` — `+` operator

Ye bohat interesting hai.

Suppose tumhare paas:

```python
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

Do points:

```python
p1 = Point(10, 20)
p2 = Point(5, 7)
```

Agar:

```python
p3 = p1 + p2
```

likho to Python ko pata nahi hoga ke custom objects ko `+` kaise karna hai.

Hum `__add__()` define kar sakte hain:

```python
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y
        )
```

Ab:

```python
p3 = p1 + p2

print(p3.x)
print(p3.y)
```

Output:

```text
15
27
```

Yahan:

```python
p1 + p2
```

conceptually:

```python
p1.__add__(p2)
```

---

# 10. Operator Overloading

Is concept ko kehte hain:

> **Operator Overloading**

Hum existing operators ko apni class ke objects ke liye define karte hain.

Examples:

```text
+    → __add__
-    → __sub__
*    → __mul__
/    → __truediv__
==   → __eq__
<    → __lt__
>    → __gt__
```

---

# 11. `__len__`

Agar tum chahte ho ke:

```python
len(object)
```

kaam kare, to `__len__()` define kar sakte ho.

Example:

```python
class Team:

    def __init__(self, members):
        self.members = members

    def __len__(self):
        return len(self.members)
```

Ab:

```python
team = Team(["Ali", "Ahmed", "Usman"])

print(len(team))
```

Output:

```text
3
```

Yahan:

```python
len(team)
```

`__len__()` ko use karta hai.

---

# 12. `__getitem__`

Ye indexing ko customize karta hai.

Example:

```python
class Team:

    def __init__(self, members):
        self.members = members

    def __getitem__(self, index):
        return self.members[index]
```

Ab:

```python
team = Team(["Ali", "Ahmed", "Usman"])

print(team[0])
print(team[1])
```

Output:

```text
Ali
Ahmed
```

Yahan:

```python
team[0]
```

conceptually:

```python
team.__getitem__(0)
```

---

# 13. `__contains__`

Ye `in` operator ke behavior ko customize kar sakta hai.

```python
class Team:

    def __init__(self, members):
        self.members = members

    def __contains__(self, name):
        return name in self.members
```

Ab:

```python
team = Team(["Ali", "Ahmed", "Usman"])

print("Ali" in team)
```

Output:

```text
True
```

Aur:

```python
print("John" in team)
```

Output:

```text
False
```

---

# 14. `__call__`

Ye thora interesting hai.

Python mein normally:

```python
object()
```

function-call jaisa syntax hota hai.

Lekin agar class mein:

```python
__call__
```

define ho, to object ko function ki tarah call kar sakte ho.

Example:

```python
class Greeter:

    def __call__(self, name):
        print(f"Hello {name}")
```

Ab:

```python
greet = Greeter()

greet("Ali")
```

Output:

```text
Hello Ali
```

Yani:

```python
greet("Ali")
```

possible ho gaya.

---

# 15. Important Dunder Methods

Ab common methods ki list dekho:

| Operation             | Dunder Method  |
| --------------------- | -------------- |
| Object initialization | `__init__`     |
| `print(obj)`          | `__str__`      |
| `repr(obj)`           | `__repr__`     |
| `obj1 == obj2`        | `__eq__`       |
| `obj1 < obj2`         | `__lt__`       |
| `obj1 > obj2`         | `__gt__`       |
| `obj1 + obj2`         | `__add__`      |
| `obj1 - obj2`         | `__sub__`      |
| `obj1 * obj2`         | `__mul__`      |
| `len(obj)`            | `__len__`      |
| `obj[index]`          | `__getitem__`  |
| `x in obj`            | `__contains__` |
| `obj()`               | `__call__`     |

---

# 16. Real HVAC example

Ab sab concepts ko equipment class mein combine karte hain:

```python
class Equipment:

    def __init__(self, equipment_id, name):
        self.equipment_id = equipment_id
        self.name = name

    def __str__(self):
        return f"{self.equipment_id} - {self.name}"

    def __eq__(self, other):
        return self.equipment_id == other.equipment_id
```

Ab:

```python
ahu1 = Equipment("AHU-001", "Main AHU")
ahu2 = Equipment("AHU-001", "Main AHU")

print(ahu1)
print(ahu1 == ahu2)
```

Output:

```text
AHU-001 - Main AHU
True
```

`__str__()` ki wajah se:

```python
print(ahu1)
```

human-readable bana.

`__eq__()` ki wajah se same equipment ID wale objects equal consider hue.

---

# 17. Dunder methods ka real concept

Important baat:

Tum normally ye nahi karte:

```python
obj.__add__(other)
```

Balkay:

```python
obj + other
```

likhte ho.

Tum:

```python
obj.__len__()
```

ke bajaye:

```python
len(obj)
```

likhte ho.

Tum:

```python
obj.__getitem__(0)
```

ke bajaye:

```python
obj[0]
```

likhte ho.

Yani **Python syntax ko custom objects ke behavior ke sath connect karne ka mechanism** dunder methods provide karte hain.

---

# 18. Ek important mental model

```text
Python syntax
     ↓
Special method
     ↓
Object ka custom behavior
```

Examples:

```text
obj + obj
   ↓
__add__()

obj == obj
   ↓
__eq__()

len(obj)
   ↓
__len__()

obj[0]
   ↓
__getitem__()

obj()
   ↓
__call__()
```

---

# 19. Sabse important 5 pehle yaad karo

Beginner ke liye pehle ye strong karo:

```python
__init__
__str__
__repr__
__eq__
__len__
```

Phir:

```python
__add__
__getitem__
__contains__
__call__
```

---

## Practice

Is class ko complete karo:

```python
class Equipment:

    def __init__(self, equipment_id, name):
        self.equipment_id = equipment_id
        self.name = name

    # print(obj) ke liye
    def __str__(self):
        pass

    # obj1 == obj2 ke liye
    def __eq__(self, other):
        pass
```

Goal:

```python
ahu1 = Equipment("AHU-01", "Main AHU")
ahu2 = Equipment("AHU-01", "Main AHU")

print(ahu1)
print(ahu1 == ahu2)
```

Expected:

```text
AHU-01 - Main AHU
True
```

**Next Lesson 11:** Python OOP mein **Composition vs Inheritance** — `has-a` vs `is-a`, aur kyun real projects mein aksar composition use ki jati hai.
