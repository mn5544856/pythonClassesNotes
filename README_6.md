


# Lesson 51: Python `logging` — `print()` se Production Logging tak

Ab hum samjhenge ke real Python application mein errors aur program activity ko properly record kaise karte hain.

Tumhare **work-order script, Google Sheets, file creation, API aur data-processing** projects mein logging bohat useful hogi.

---

# 1. `print()` vs `logging`

Beginner code mein:

```python
print("Work order created")
```

use karte hain.

Lekin production application mein:

```python
import logging

logging.info("Work order created")
```

zyada useful hai.

### Difference

```text
print()
↓
sirf message display

logging
↓
message
+ severity
+ timestamp
+ source
+ destination
+ filtering
```

---

# 2. Logging kya hai?

Logging ka matlab:

> Application ke important events aur errors ko structured form mein record karna.

Example:

```text
2026-09-29 10:15:32 INFO Work order WO-1001 created
```

Is message mein:

```text
timestamp
   ↓
2026-09-29 10:15:32

level
   ↓
INFO

message
   ↓
Work order WO-1001 created
```

---

# 3. Python ka built-in `logging`

Python mein external package ki zaroorat nahi:

```python
import logging
```

Basic:

```python
logging.warning("Temperature high hai")
```

---

# 4. Logging levels

Python ke standard levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Inki severity roughly:

```text
DEBUG       10
INFO        20
WARNING     30
ERROR       40
CRITICAL    50
```

Number manually yaad rakhna zaroori nahi, concept samjho:

```text
DEBUG
  ↓
INFO
  ↓
WARNING
  ↓
ERROR
  ↓
CRITICAL
```

Neeche se upar severity increase hoti hai.

---

# 5. `DEBUG`

Detailed diagnostic information:

```python
logging.debug("Processing row 25")
```

Useful during development/troubleshooting.

Example:

```text
DEBUG Processing WO-1001
DEBUG Reading column Equipment ID
DEBUG Equipment ID = AHU-01
```

Production mein DEBUG logs aksar disable ya filter kiye ja sakte hain.

---

# 6. `INFO`

Normal important application events:

```python
logging.info("Work order created")
```

Example:

```text
INFO Work order WO-1001 created
INFO Google Sheet loaded
INFO 250 rows processed
```

---

# 7. `WARNING`

Potential problem, lekin application necessarily fail nahi hui.

```python
logging.warning("Equipment ID missing")
```

Example:

```text
WARNING Temperature value missing for AHU-01
```

Program continue kar sakta hai.

---

# 8. `ERROR`

Operation fail hui:

```python
logging.error("Folder creation failed")
```

Example:

```text
ERROR Failed to create folder for WO-1005
```

Application ka kuch portion fail hua hai.

---

# 9. `CRITICAL`

Serious application/system failure:

```python
logging.critical("Database unavailable")
```

Example:

```text
CRITICAL Configuration file missing
```

Aisi situation mein application continue karna unsafe ho sakta hai, depending on architecture.

---

# 10. Basic example

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.debug("Debug message")
logging.info("Application started")
logging.warning("Warning")
logging.error("Something failed")
logging.critical("Critical failure")
```

Typical output:

```text
INFO:root:Application started
WARNING:root:Warning
ERROR:root:Something failed
CRITICAL:root:Critical failure
```

`DEBUG` nahi dikhega because level `INFO` hai.

---

# 11. Level filtering

Agar:

```python
logging.basicConfig(level=logging.WARNING)
```

to normally:

```text
DEBUG   ❌
INFO    ❌
WARNING ✅
ERROR   ✅
CRITICAL ✅
```

Yani configured level se kam severity wale records filter ho jate hain.

---

# 12. `basicConfig()`

Simple scripts ke liye:

```python
logging.basicConfig(
    level=logging.INFO
)
```

common starting point hai.

Lekin larger applications mein directly root logger configure karne ke bajaye named loggers, handlers aur formatters use karna better architecture hota hai.

---

# 13. Log format customize karna

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

Output:

```text
2026-09-29 10:20:15,123 - INFO - Application started
```

---

# 14. Useful format fields

Common fields:

```text
%(asctime)s
%(levelname)s
%(name)s
%(message)s
%(filename)s
%(lineno)d
%(funcName)s
```

Example:

```python
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
```

Output:

```text
2026-09-29 10:20:15 | INFO | root | Application started
```

---

# 15. Logger object

Production-style code mein:

```python
logger = logging.getLogger(__name__)
```

use karna common hai.

Example:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Work order processing started")
```

---

# 16. `__name__` kyun?

Agar file:

```text
work_orders.py
```

hai aur usmein:

```python
logger = logging.getLogger(__name__)
```

to logger ka naam module ke naam se related hoga.

Conceptually:

```text
work_orders
    ↓
logger
```

Isse large project mein pata chal sakta hai ke log kis module se aya.

---

# 17. Project structure

Suppose:

```text
project/
│
├── main.py
├── work_orders.py
├── google_sheets.py
└── folders.py
```

Har module:

```python
logger = logging.getLogger(__name__)
```

use kar sakta hai.

Then logs identify kar sakte hain:

```text
work_orders
folders
google_sheets
```

Ye `print()` se significantly better observability provide karta hai.

---

# 18. File mein logging

Suppose:

```python
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
```

Ab logs:

```text
app.log
```

mein write honge.

Example:

```text
2026-09-29 10:25:01 | INFO | Application started
2026-09-29 10:25:03 | INFO | 100 rows loaded
2026-09-29 10:25:04 | ERROR | Folder creation failed
```

---

# 19. Console + File dono

Real application mein tum aksar chahte ho:

```text
console
+
log file
```

Dono jagah logs aayein.

Iske liye:

```text
Logger
   ↓
Handlers
   ├── Console
   └── File
```

---

# 20. Handler kya hai?

**Handler** decide karta hai:

> Log record ko kahan bhejna hai?

Examples:

```text
StreamHandler
→ console

FileHandler
→ file

RotatingFileHandler
→ rotating log files
```

Mental model:

```text
logger
  ↓
handler
  ↓
destination
```

---

# 21. Formatter kya hai?

Formatter decide karta hai:

> Log message kis format mein appear hoga?

Architecture:

```text
Logger
   ↓
LogRecord
   ↓
Handler
   ↓
Formatter
   ↓
Output
```

---

# 22. Complete logger example

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logger.info("Application started")
```

Output:

```text
2026-09-29 10:30:00 | INFO | my_module | Application started
```

---

# 23. Logger vs Handler vs Formatter

Ye teen confuse mat karna:

```text
Logger
→ log record create/process karta hai

Handler
→ log kahan jayega?

Formatter
→ log ka appearance kya hoga?
```

Example:

```text
Logger
   │
   ↓
Handler → console
   │
   ↓
Formatter → "time | level | message"
```

---

# 24. Multiple handlers

```python
logger
   │
   ├── ConsoleHandler
   │       ↓
   │    terminal
   │
   └── FileHandler
           ↓
        app.log
```

Iska faida:

```text
developer → console dekhta hai
history    → file mein save hoti hai
```

---

# 25. Exception logging

Ye bohat important hai.

Instead of:

```python
except Exception as e:
    print(e)
```

use:

```python
except Exception:
    logger.exception("Work order processing failed")
```

---

# 26. `logger.exception()`

`logger.exception()` normally `except` block ke andar use hota hai.

Example:

```python
try:
    result = 10 / 0

except Exception:
    logger.exception("Calculation failed")
```

Ye message ke saath traceback bhi log karta hai.

Example conceptually:

```text
ERROR Calculation failed
Traceback:
  ...
ZeroDivisionError: division by zero
```

Debugging ke liye extremely useful.

---

# 27. `logger.error()` vs `logger.exception()`

```python
logger.error("Something failed")
```

sirf error message log karta hai.

```python
logger.exception("Something failed")
```

`except` context mein current exception ka traceback bhi include karta hai.

So:

```text
error()
→ message

exception()
→ message + traceback
```

---

# 28. `exc_info=True`

Equivalent style:

```python
logger.error(
    "Something failed",
    exc_info=True
)
```

Traceback information include karne ke liye.

Lekin inside `except`, readable/common pattern:

```python
logger.exception("Something failed")
```

---

# 29. Work-order example

```python
import logging

logger = logging.getLogger(__name__)

def create_work_order_folder(work_order_number):

    logger.info(
        "Creating folder for %s",
        work_order_number
    )

    try:
        # folder creation
        ...

    except PermissionError:
        logger.exception(
            "Permission denied for %s",
            work_order_number
        )
        raise
```

Important:

```python
logger.info(
    "Creating folder for %s",
    work_order_number
)
```

ko prefer kiya jata hai over:

```python
logger.info(
    f"Creating folder for {work_order_number}"
)
```

especially logging APIs mein, kyunki logging framework message formatting ko later perform kar sakta hai.

---

# 30. `%s` logging style

```python
logger.info(
    "Equipment %s temperature is %s",
    equipment_id,
    temperature
)
```

Output:

```text
Equipment AHU-01 temperature is 22.5
```

Logging arguments separately dena standard pattern hai.

---

# 31. Logging levels ka practical use

Tumhare work-order project mein:

### DEBUG

```python
logger.debug("Row data: %s", row)
```

### INFO

```python
logger.info("Created folder: %s", folder)
```

### WARNING

```python
logger.warning(
    "Comment missing for %s",
    work_order
)
```

### ERROR

```python
logger.error(
    "Folder creation failed for %s",
    work_order
)
```

### CRITICAL

```python
logger.critical(
    "Work-order source unavailable"
)
```

---

# 32. `print()` completely useless nahi hai

`print()` still useful hai:

```text
quick debugging
small scripts
interactive experiments
simple CLI output
```

Lekin production monitoring/auditing ke liye logging much more capable hai.

---

# 33. Logging architecture

Ab tak:

```text
print()
```

se:

```text
logging
```

tak aaye.

Full architecture:

```text
Application
    │
    ↓
  Logger
    │
    ↓
 LogRecord
    │
    ├──────────────┐
    ↓              ↓
Console Handler   File Handler
    │              │
    ↓              ↓
Formatter        Formatter
    │              │
    ↓              ↓
Terminal         app.log
```

---

# 34. Log levels ko filter karna

Har handler ka apna level ho sakta hai.

Example concept:

```text
Logger → DEBUG

Console Handler → INFO
File Handler    → DEBUG
```

Then:

```text
DEBUG
→ file only

INFO
→ console + file

WARNING
→ console + file

ERROR
→ console + file
```

Ye production systems mein useful configuration hai.

---

# 35. Log propagation

Python logging mein logger hierarchy hoti hai.

Example:

```text
root
│
├── app
│   ├── app.workorders
│   └── app.folders
```

Child logger records normally parent/root handlers tak propagate kar sakta hai.

Example:

```python
logger = logging.getLogger("app.workorders")
```

Parent:

```text
app
```

aur root hierarchy ka part hai.

---

# 36. `propagate`

Agar:

```python
logger.propagate = False
```

set karo, record parent logger ko propagate nahi karega.

Ye advanced configuration mein duplicate logs prevent karne ke liye useful ho sakta hai.

---

# 37. Duplicate logging ka common problem

Agar accidentally same handler repeatedly add karo:

```python
logger.addHandler(handler)
```

multiple times, same message multiple times appear ho sakta hai.

Example:

```text
INFO Started
INFO Started
INFO Started
```

jab tumne ek hi event ek baar log kiya ho.

Isliye logger configuration ko centralized rakhna generally better hai.

---

# 38. Production log rotation

Agar:

```text
app.log
```

har din continuously grow karta rahe, file huge ho sakti hai.

Python provides:

```python
from logging.handlers import RotatingFileHandler
```

Conceptually:

```text
app.log
app.log.1
app.log.2
app.log.3
```

Size limit ke basis par rotation.

Time-based rotation ke liye:

```python
from logging.handlers import TimedRotatingFileHandler
```

use kiya ja sakta hai.

---

# 39. Work-order application ka recommended basic architecture

```text
project/
│
├── main.py
├── logging_config.py
│
├── work_orders.py
├── folders.py
└── sheets.py
```

`logging_config.py`:

```python
import logging

def get_logger(name):
    return logging.getLogger(name)
```

Other modules:

```python
from logging_config import get_logger

logger = get_logger(__name__)
```

Phir:

```python
logger.info(...)
logger.warning(...)
logger.error(...)
logger.exception(...)
```

---

# 40. Logging + Exception = powerful combination

Exception handling:

```python
try:
    process_work_order(row)

except WorkOrderError:
    logger.exception(
        "Work order processing failed"
    )
    raise
```

Yahan:

```text
Exception
   ↓
Logger
   ↓
Traceback
   ↓
Log file
   ↓
raise
   ↓
caller can handle
```

Error silently disappear nahi hota.

---

# 41. Final mental model

```text
print()
↓
quick output


logging
↓
structured application events
↓
levels
↓
logger
↓
handlers
↓
formatters
↓
console/file/etc.
```

### Golden rules

```text
1. DEBUG → detailed diagnostics

2. INFO → normal important events

3. WARNING → potential problem

4. ERROR → operation failed

5. CRITICAL → severe application/system problem

6. logger = logging.getLogger(__name__)

7. Handler → destination

8. Formatter → appearance

9. logger.exception()
   → exception + traceback

10. Production code mein logging generally
    print() se zyada suitable hai.
```

## Next Lesson 52

Ab hum **Python `inspect` + introspection + reflection** dekhenge:

```text
inspect
dir()
type()
id()
vars()
__dict__
__annotations__
signature()
getmembers()
```

Aur samjhenge ke Python program **runtime par apne objects/classes/functions ke baare mein information kaise discover karta hai**.

# Lesson 52: Python Introspection + Reflection + `inspect`

Ab hum ek powerful Python concept par aate hain:

> **Program runtime par khud objects, classes aur functions ke baare mein information kaise discover karta hai?**

Isko broadly **introspection** kehte hain.

Tumne pehle `__dict__`, `type()`, `dir()`, `__annotations__` waghera use kiye hain. Ab in sab ko ek system ki tarah samjhenge.

---

# 1. Introspection kya hai?

Simple definition:

> **Runtime par object ke baare mein information inspect karna = introspection.**

Example:

```python
class Equipment:
    def start(self):
        print("Started")

ahu = Equipment()
```

Ab hum Python se pooch sakte hain:

```python
type(ahu)
```

```text
<class '__main__.Equipment'>
```

Yani:

> `ahu` kis class ka object hai?

---

# 2. `type()`

```python
x = 100

print(type(x))
```

Output:

```text
<class 'int'>
```

String:

```python
name = "AHU-01"

print(type(name))
```

Output:

```text
<class 'str'>
```

List:

```python
items = [1, 2, 3]

print(type(items))
```

Output:

```text
<class 'list'>
```

---

# 3. `type()` aur `__class__`

Ye:

```python
type(ahu)
```

aur:

```python
ahu.__class__
```

dono object ki class ko represent karte hain.

Example:

```python
print(type(ahu))
print(ahu.__class__)
```

Dono:

```text
<class '__main__.Equipment'>
```

---

# 4. `id()`

Previous memory lesson se:

```python
x = []

print(id(x))
```

`id()` object ki identity deta hai.

Example:

```python
a = []
b = a

print(id(a))
print(id(b))
```

Dono same honge:

```text
123456789
123456789
```

because:

```python
a is b
```

→ `True`.

---

# 5. `dir()`

`dir()` object/class ke available attributes aur methods ke names discover karne mein useful hai.

```python
name = "AHU"

print(dir(name))
```

Tumhein bohat saare names milenge:

```text
['__add__',
 '__class__',
 '__contains__',
 '__len__',
 'capitalize',
 'lower',
 'upper',
 ...]
```

---

# 6. `dir()` kya nahi karta?

`dir()` normally names ki list deta hai.

Ye directly:

```text
method ka source code
method ki complete implementation
```

nahi deta.

Example:

```python
dir(name)
```

se:

```text
upper
lower
split
```

mil sakte hain.

Lekin `upper()` internally kaise implement hua, ye `dir()` nahi batata.

---

# 7. `hasattr()`

Check karna ho ke object mein attribute/method available hai ya nahi:

```python
hasattr(ahu, "start")
```

Output:

```text
True
```

Aur:

```python
hasattr(ahu, "stop")
```

agar method nahi hai:

```text
False
```

---

# 8. `getattr()`

Dynamic attribute access:

```python
method = getattr(ahu, "start")
```

Ab:

```python
method()
```

execute kar sakte ho.

Ye equivalent idea hai:

```python
ahu.start()
```

Lekin difference ye hai ke name string se runtime par aa sakta hai.

---

# 9. `getattr()` ka default

Agar attribute exist nahi karta:

```python
value = getattr(ahu, "temperature", None)
```

Agar `temperature` nahi hai:

```text
None
```

milega.

Ye:

```python
getattr(obj, "name", default)
```

dynamic programming mein bohat useful hai.

---

# 10. `setattr()`

Runtime par attribute set kar sakte ho:

```python
setattr(ahu, "temperature", 22.5)
```

Ab:

```python
print(ahu.temperature)
```

Output:

```text
22.5
```

Conceptually:

```python
ahu.temperature = 22.5
```

jaisa.

---

# 11. `delattr()`

Runtime par attribute delete:

```python
delattr(ahu, "temperature")
```

Conceptually:

```python
del ahu.temperature
```

jaisa.

---

# 12. `getattr`, `setattr`, `delattr`

Ye teen ek important family hain:

```text
getattr()
    ↓
attribute read

setattr()
    ↓
attribute write

delattr()
    ↓
attribute delete
```

Example:

```python
name = "temperature"

setattr(ahu, name, 22.5)

value = getattr(ahu, name)

delattr(ahu, name)
```

Yahan attribute ka naam variable se aa raha hai.

---

# 13. `vars()`

`vars(obj)` bohat useful hai.

Example:

```python
class Equipment:
    def __init__(self):
        self.equipment_id = "AHU-01"
        self.status = "ON"

ahu = Equipment()

print(vars(ahu))
```

Output:

```text
{
    'equipment_id': 'AHU-01',
    'status': 'ON'
}
```

For normal objects, ye usually instance namespace/dictionary ko expose karta hai.

---

# 14. `__dict__`

Same concept:

```python
print(ahu.__dict__)
```

Output:

```text
{
    'equipment_id': 'AHU-01',
    'status': 'ON'
}
```

So:

```python
vars(ahu)
```

often effectively:

```python
ahu.__dict__
```

ke equivalent information deta hai.

---

# 15. `vars()` vs `dir()`

Important difference:

### `vars(obj)`

Actual instance namespace/data:

```text
equipment_id
status
```

### `dir(obj)`

Available names:

```text
equipment_id
status
start
__class__
__dict__
...
```

Mental model:

```text
vars()
→ "Object ke namespace mein kya stored hai?"

dir()
→ "Object ke saath kaun se names accessible hain?"
```

---

# 16. Class ka `__dict__`

```python
class Equipment:

    category = "HVAC"

    def start(self):
        print("Started")
```

Then:

```python
print(Equipment.__dict__)
```

Ismein class namespace ke entries hongi:

```text
category
start
__module__
__dict__
__weakref__
...
```

Methods bhi class namespace mein objects ke form mein stored/referenced hote hain.

---

# 17. Instance vs class namespace

```python
class Equipment:
    category = "HVAC"

    def __init__(self):
        self.equipment_id = "AHU-01"
```

Then:

```python
ahu = Equipment()
```

Conceptually:

```text
Equipment.__dict__
│
├── category
└── __init__
```

while:

```text
ahu.__dict__
│
└── equipment_id
```

---

# 18. Attribute lookup connection

Previous lessons mein humne attribute lookup padha tha.

When:

```python
ahu.category
```

Python class hierarchy/attribute lookup se `category` find kar sakta hai.

When:

```python
ahu.equipment_id
```

instance namespace mein mil sakta hai.

Isliye `__dict__` introspection attribute lookup samajhne mein bohat useful hai.

---

# 19. `__annotations__`

Python type annotations runtime par class/function/module mein metadata ke form mein accessible ho sakti hain.

Example:

```python
class Equipment:
    equipment_id: str
    temperature: float
```

Then:

```python
print(Equipment.__annotations__)
```

Output:

```text
{
    'equipment_id': <class 'str'>,
    'temperature': <class 'float'>
}
```

---

# 20. Function annotations

```python
def add(a: int, b: int) -> int:
    return a + b
```

Then:

```python
print(add.__annotations__)
```

Output:

```text
{
    'a': <class 'int'>,
    'b': <class 'int'>,
    'return': <class 'int'>
}
```

Yani function ki type annotation metadata runtime par inspect ki ja sakti hai.

---

# 21. Important: annotations automatically validation nahi karti

Agar:

```python
def add(a: int, b: int) -> int:
    return a + b
```

tum:

```python
add("10", "20")
```

call kar do, Python automatically type error sirf annotation ki wajah se nahi deta.

Annotations primarily:

```text
type checkers
IDE
documentation
frameworks
runtime introspection
```

ke liye useful hain.

---

# 22. `inspect` module

Python standard library mein:

```python
import inspect
```

hai.

Ye advanced introspection ke liye powerful toolkit hai.

---

# 23. `inspect.isfunction()`

```python
import inspect

def start():
    pass

print(inspect.isfunction(start))
```

Output:

```text
True
```

Agar:

```python
x = 10

print(inspect.isfunction(x))
```

→

```text
False
```

---

# 24. `inspect.ismethod()`

Object ke bound method ko inspect kar sakte ho:

```python
class Equipment:
    def start(self):
        pass

ahu = Equipment()

print(inspect.ismethod(ahu.start))
```

Output:

```text
True
```

---

# 25. `inspect.isclass()`

```python
class Equipment:
    pass

print(inspect.isclass(Equipment))
```

→

```text
True
```

---

# 26. `inspect.isbuiltin()`

Built-in functions detect karne ke liye:

```python
print(inspect.isbuiltin(len))
```

Output generally:

```text
True
```

---

# 27. `inspect.signature()`

Ye extremely useful hai.

Suppose:

```python
def create_equipment(
    equipment_id: str,
    temperature: float = 22.0,
    active: bool = True
):
    pass
```

Then:

```python
print(inspect.signature(create_equipment))
```

Output:

```text
(equipment_id: str, temperature: float = 22.0, active: bool = True)
```

Yani runtime par function ka parameter structure discover kar sakte ho.

---

# 28. Signature ko inspect karna

```python
signature = inspect.signature(create_equipment)

print(signature.parameters)
```

Ye parameters ka mapping provide karega.

Conceptually:

```text
equipment_id
temperature
active
```

---

# 29. Individual parameter

```python
param = signature.parameters["temperature"]

print(param.name)
print(param.annotation)
print(param.default)
```

Conceptually:

```text
name      → temperature
annotation → float
default   → 22.0
```

Ye frameworks mein bohat useful technique hai.

---

# 30. `inspect.getmembers()`

Object ke members retrieve kar sakte ho:

```python
members = inspect.getmembers(Equipment)

for name, value in members:
    print(name, value)
```

Ye `(name, value)` pairs ki list provide karta hai.

---

# 31. Specific members filter karna

Suppose sirf methods chahiye:

```python
methods = inspect.getmembers(
    Equipment,
    inspect.isfunction
)
```

Then:

```text
__init__
start
...
```

type ke matching members mil sakte hain.

---

# 32. `inspect.getsource()`

Python-defined function ka source code retrieve karne ki koshish:

```python
def add(a, b):
    return a + b
```

Then:

```python
print(inspect.getsource(add))
```

Output:

```python
def add(a, b):
    return a + b
```

Lekin important limitation:

> Har callable ka source available nahi hota.

Built-in functions, dynamically generated objects, interactive environments etc. mein `getsource()` fail kar sakta hai.

---

# 33. `inspect.getfile()`

Function/class kis file mein defined hai:

```python
print(inspect.getfile(add))
```

Example:

```text
C:\project\math_utils.py
```

Useful when debugging large projects.

---

# 34. `inspect.getmodule()`

```python
module = inspect.getmodule(add)

print(module)
```

Function kis module se related hai, ye discover kar sakte ho.

---

# 35. `inspect.iscoroutinefunction()`

Tumne async programming padhi hai.

Example:

```python
async def fetch_data():
    pass
```

Check:

```python
inspect.iscoroutinefunction(fetch_data)
```

→

```text
True
```

---

# 36. Generator function detect karna

```python
def numbers():
    yield 1
    yield 2
```

Then:

```python
inspect.isgeneratorfunction(numbers)
```

→

```text
True
```

Ye tumhari generators wali lesson se directly connect hota hai.

---

# 37. Callable detection

Python mein:

```python
callable(obj)
```

check karta hai ke object ko:

```python
obj()
```

call kiya ja sakta hai ya nahi.

Example:

```python
def hello():
    pass

print(callable(hello))
```

→ `True`

---

# 38. Class with `__call__`

Previous lesson:

```python
class Logger:
    def __call__(self):
        print("Called")
```

Then:

```python
logger = Logger()

print(callable(logger))
```

→

```text
True
```

Yani `callable()` introspection ka simple runtime tool hai.

---

# 39. `isinstance()`

```python
ahu = Equipment()

print(isinstance(ahu, Equipment))
```

→

```text
True
```

Inheritance ke saath:

```python
class AHU(Equipment):
    pass

ahu = AHU()

print(isinstance(ahu, Equipment))
```

→

```text
True
```

Because AHU is an Equipment.

---

# 40. `issubclass()`

Classes ke relationship ko inspect karna:

```python
print(issubclass(AHU, Equipment))
```

→

```text
True
```

Lekin:

```python
print(issubclass(Equipment, AHU))
```

→

```text
False
```

---

# 41. `isinstance()` vs `issubclass()`

```text
isinstance()
→ object kis class/type ka hai?

issubclass()
→ class kis class se inherit karti hai?
```

Example:

```python
isinstance(ahu, Equipment)
```

Object involved.

```python
issubclass(AHU, Equipment)
```

Classes involved.

---

# 42. `__mro__`

Previous MRO lesson:

```python
print(AHU.__mro__)
```

Example:

```text
(
    <class 'AHU'>,
    <class 'Equipment'>,
    <class 'object'>
)
```

Runtime par inheritance resolution order inspect kar sakte ho.

---

# 43. `__bases__`

Direct base classes:

```python
print(AHU.__bases__)
```

Output conceptually:

```text
(<class 'Equipment'>,)
```

Difference:

```text
__bases__
→ direct parents

__mro__
→ complete method resolution order
```

---

# 44. Introspection ka practical use

Suppose tumhare paas equipment objects hain:

```python
equipment = [AHU(...), VAV(...), Sensor(...)]
```

Tum runtime par discover kar sakte ho:

```python
for item in equipment:
    print(type(item))
```

Output:

```text
AHU
VAV
Sensor
```

Aur:

```python
print(dir(item))
```

se capabilities inspect kar sakte ho.

---

# 45. Dynamic plugin architecture

Suppose plugin classes hain:

```text
plugins/
├── hvac.py
├── electrical.py
└── plumbing.py
```

Application runtime par inspect karke classes/functions discover kar sakti hai.

Conceptually:

```text
load module
    ↓
inspect members
    ↓
find classes
    ↓
check interface
    ↓
register plugin
```

Ye frameworks aur plugin systems mein common pattern hai.

---

# 46. Protocol se connection

Previous lesson mein:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...
```

tha.

Runtime introspection:

```python
hasattr(obj, "start")
```

se basic capability check kar sakte ho.

Lekin:

> `Protocol` static type-checking contract hai; `inspect`/`hasattr` runtime introspection tools hain.

Dono ko same cheez mat samjho.

---

# 47. Descriptor se connection

Tumne descriptors bhi padhe hain.

Suppose:

```python
class PositiveNumber:
    def __get__(self, instance, owner):
        ...
```

Runtime par:

```python
inspect.getmembers(MyClass)
```

class members discover kar sakta hai.

Aur:

```python
MyClass.__dict__
```

se descriptor object ko inspect kar sakte ho.

---

# 48. Dataclass se connection

Previous lesson:

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    temperature: float
```

Runtime:

```python
print(Equipment.__annotations__)
```

aur dataclass-specific:

```python
from dataclasses import fields

print(fields(Equipment))
```

`fields()` dataclass fields ko structured metadata ke form mein deta hai.

Yani introspection frameworks ka foundation ban sakti hai.

---

# 49. TypedDict se connection

`TypedDict` mein bhi metadata inspect kar sakte ho:

```python
class WorkOrder(TypedDict):
    work_order: str
    equipment_id: str
```

Then type metadata:

```python
WorkOrder.__annotations__
```

Aur required/optional key metadata bhi available ho sakta hai.

Ye JSON/CSV/Google Sheets data validation frameworks mein useful hai.

---

# 50. Reflection vs Introspection

Ye terms related hain lekin distinction useful hai.

### Introspection

> Object ke baare mein information discover karna.

Examples:

```python
type()
dir()
vars()
inspect.signature()
```

### Reflection

> Runtime par object/program structure ko inspect **aur manipulate** karna.

Examples:

```python
getattr()
setattr()
delattr()
```

Simple mental model:

```text
Introspection
→ "Mujhe batao tum kya ho?"

Reflection
→ "Mujhe runtime par tumhare structure ke saath kaam karne do."
```

Python mein dono concepts overlap karte hain.

---

# 51. Complete example

```python
import inspect

class Equipment:

    def __init__(
        self,
        equipment_id: str,
        temperature: float = 22.0
    ):
        self.equipment_id = equipment_id
        self.temperature = temperature

    def start(self) -> None:
        print("Started")


ahu = Equipment("AHU-01")
```

Ab:

```python
print(type(ahu))
```

→ class.

```python
print(vars(ahu))
```

→ instance data.

```python
print(dir(ahu))
```

→ available names.

```python
print(hasattr(ahu, "start"))
```

→ capability check.

```python
print(inspect.signature(Equipment))
```

→ constructor signature.

```python
print(Equipment.__annotations__)
```

→ class annotations.

```python
print(Equipment.__dict__)
```

→ class namespace.

---

# 52. Most important tools

Is lesson ke liye ye table yaad rakho:

| Tool                            | Purpose                        |
| ------------------------------- | ------------------------------ |
| `type()`                        | object ka type/class           |
| `id()`                          | object identity                |
| `dir()`                         | available names                |
| `vars()`                        | namespace/data                 |
| `__dict__`                      | namespace dictionary           |
| `hasattr()`                     | attribute exists?              |
| `getattr()`                     | dynamic read                   |
| `setattr()`                     | dynamic write                  |
| `delattr()`                     | dynamic delete                 |
| `isinstance()`                  | object/type relationship       |
| `issubclass()`                  | class inheritance              |
| `callable()`                    | callable hai?                  |
| `inspect.signature()`           | function parameters            |
| `inspect.getmembers()`          | members discover               |
| `inspect.getsource()`           | source retrieve where possible |
| `inspect.isclass()`             | class check                    |
| `inspect.isfunction()`          | function check                 |
| `inspect.iscoroutinefunction()` | async function check           |

---

# 53. Final mental model

```text
                 Python Object
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
      type()        dir()        vars()
        │             │             │
      "Kya ho?"    "Kya hai?"   "Kya stored?"
        │
        ↓
     inspect
        │
   ┌────┼──────────────┐
   ↓    ↓              ↓
signature members    source
```

Aur dynamic access:

```text
getattr()
setattr()
delattr()
```

---

## Golden Rules

```text
1. type() → object ki class.

2. dir() → available names discover.

3. vars()/__dict__ → namespace inspect.

4. getattr/setattr/delattr
   → dynamic attribute manipulation.

5. inspect.signature()
   → function ka parameter contract runtime par inspect.

6. isinstance()
   → object relationship.

7. issubclass()
   → class relationship.

8. Introspection
   → runtime information discover.

9. Reflection
   → runtime par structure ko access/manipulate.

10. Annotations runtime par available ho sakti hain,
    lekin automatically validation nahi karti.
```

### Next Lesson 53

Ab hum **Python Modules + Packages + Import System** deeply samjhenge:

```text
module
package
__init__.py
__name__
__main__
sys.path
import
from ... import ...
relative import .
absolute import
```

Aur specifically tumhare pehle wale:

```python
from .cell import Cell
```

ko **actual Python import mechanism** ke context mein samjhenge.

# Lesson 53: Python Modules, Packages aur Import System

Ab hum Python ke **import system** ko deeply samjhenge. Ye tumhare is question se directly connected hai:

```python
from .cell import Cell
```

Yahan `.` kyun aata hai, package kya hota hai, `__init__.py` kya karta hai, aur Python actually module ko find kaise karta hai — sab clear karte hain.

---

# 1. Module kya hota hai?

Simple:

> **Python ki ek `.py` file ko module keh sakte hain.**

Suppose:

```text
project/
│
├── main.py
└── cell.py
```

`cell.py` ek module hai.

Agar `cell.py` mein:

```python
class Cell:
    pass
```

hai, to `main.py` mein:

```python
from cell import Cell
```

kar sakte ho.

---

# 2. Module ka faida kya hai?

Agar sari Python code ek hi file mein likho:

```text
main.py
```

to file bohat badi ho sakti hai.

Instead:

```text
project/
│
├── main.py
├── cell.py
├── employee.py
├── work_order.py
└── google_sheet.py
```

Har file ek specific responsibility rakh sakti hai.

```text
cell.py
→ Cell

employee.py
→ Employee

work_order.py
→ WorkOrder

google_sheet.py
→ Google Sheets logic
```

---

# 3. Import

Suppose:

```python
# cell.py

class Cell:
    def read(self):
        return "data"
```

Then:

```python
# main.py

from cell import Cell

cell = Cell()
print(cell.read())
```

Flow:

```text
main.py
   ↓
import cell
   ↓
Python cell.py ko locate karta hai
   ↓
module load karta hai
   ↓
Cell available
```

---

# 4. `import module`

Do styles dekho.

### Style 1

```python
import cell
```

Then:

```python
c = cell.Cell()
```

### Style 2

```python
from cell import Cell
```

Then:

```python
c = Cell()
```

Difference:

```text
import cell
→ module namespace available

from cell import Cell
→ specific name directly available
```

---

# 5. `import cell` ke baad kya hota hai?

Suppose:

```python
import cell
```

Python variable/name:

```python
cell
```

provide karta hai.

Then:

```python
cell.Cell
cell.some_function
cell.some_variable
```

access kar sakte ho.

Mental model:

```text
cell
 ↓
module object
 ↓
Cell
some_function
some_variable
```

---

# 6. `from cell import Cell`

Ye:

```python
from cell import Cell
```

ka matlab:

> `cell` module se `Cell` naam import karo.

Then:

```python
Cell()
```

directly use kar sakte ho.

---

# 7. Package kya hota hai?

Suppose project grow ho gaya:

```text
project/
│
├── main.py
│
└── equipment/
    ├── __init__.py
    ├── cell.py
    ├── sensor.py
    └── controller.py
```

`equipment` ek **package** hai.

Conceptually:

```text
package
   │
   ├── cell.py
   ├── sensor.py
   └── controller.py
```

Package modules ko organize karta hai.

---

# 8. `__init__.py`

Historically Python package ko identify karne ke liye:

```text
equipment/
└── __init__.py
```

use hota tha.

Modern Python mein **namespace packages** ki wajah se har directory ko `__init__.py` ki zaroorat nahi hoti, lekin normal application/package design mein `__init__.py` ab bhi commonly useful hai.

---

# 9. `__init__.py` mein kya likhte hain?

Empty bhi ho sakti hai:

```python
# __init__.py
```

Ya package-level imports:

```python
from .cell import Cell
from .sensor import Sensor
```

Then outside:

```python
from equipment import Cell
```

use kar sakte ho.

---

# 10. Tumhara important example: `from .cell import Cell`

Suppose:

```text
project/
│
└── equipment/
    ├── __init__.py
    ├── manager.py
    └── cell.py
```

`manager.py` mein:

```python
from .cell import Cell
```

Yahan:

```text
.
```

ka matlab:

> **Current package.**

So:

```python
from .cell import Cell
```

roughly means:

> Current package ke `cell.py` module se `Cell` import karo.

---

# 11. `.` ka matlab current directory nahi samjho

Ye important distinction hai.

```python
from .cell import Cell
```

mein `.` ka conceptual meaning:

> **current package**

hai, simple filesystem current directory nahi.

Python import system package context use karta hai.

---

# 12. `..`

Suppose:

```text
project/
│
├── common/
│   └── utils.py
│
└── equipment/
    ├── __init__.py
    └── controller.py
```

Agar package hierarchy deeper ho:

```text
project/
└── equipment/
    └── hvac/
        └── controller.py
```

To:

```python
from ..common import something
```

conceptually ek package level upar jaata hai.

General idea:

```text
.
→ current package

..
→ parent package

...
→ us se upar
```

Lekin relative imports package context ke andar meaningful hote hain.

---

# 13. Absolute import vs relative import

### Absolute

```python
from equipment.cell import Cell
```

### Relative

```python
from .cell import Cell
```

Difference:

```text
Absolute
→ package/module ka full import path

Relative
→ current package ko reference point banao
```

---

# 14. Relative import ka faida

Suppose package:

```text
myapp/
└── equipment/
    ├── cell.py
    └── controller.py
```

`controller.py`:

```python
from .cell import Cell
```

Agar `equipment` package ka naam/project location change ho, internal relationship:

```text
controller
   ↓
same package
   ↓
cell
```

clear rehti hai.

---

# 15. Lekin relative import directly file run karne par problem kyun de sakta hai?

Suppose:

```text
equipment/
├── __init__.py
├── controller.py
└── cell.py
```

`controller.py`:

```python
from .cell import Cell
```

Agar tum:

```bash
python controller.py
```

run karte ho, Python us file ko top-level script ki tarah execute kar raha hota hai.

Us waqt package context available nahi ho sakta.

Result:

```text
ImportError:
attempted relative import with no known parent package
```

---

# 16. Correct package execution

Project root se:

```bash
python -m equipment.controller
```

`-m` ka matlab roughly:

> Module ko package/module context mein execute karo.

Ab Python jaanta hai:

```text
equipment
   ↓
controller
```

isliye:

```python
from .cell import Cell
```

resolve ho sakta hai.

---

# 17. `__name__`

Har Python module ke paas:

```python
__name__
```

hota hai.

Agar directly script run karo:

```python
print(__name__)
```

usually:

```text
__main__
```

Agar module import hua:

```python
import cell
```

to:

```python
cell.__name__
```

usually:

```text
cell
```

---

# 18. `if __name__ == "__main__"`

Very important pattern:

```python
if __name__ == "__main__":
    main()
```

Iska matlab:

> Ye code tab run karo jab file directly execute ho, import hone par nahi.

Example:

```python
def main():
    print("Application started")


if __name__ == "__main__":
    main()
```

---

# 19. Ye pattern kyun useful hai?

Suppose:

```text
app.py
```

mein:

```python
print("Running application")
```

hai.

Agar doosri file:

```python
import app
```

karegi, import ke waqt top-level code execute ho sakta hai.

Lekin:

```python
if __name__ == "__main__":
    print("Running application")
```

ho to ye part direct execution par chalega, normal import par nahi.

---

# 20. `__main__` ko simple example se samjho

`app.py`:

```python
print("Module loaded")


if __name__ == "__main__":
    print("Program started")
```

### Direct:

```bash
python app.py
```

Output:

```text
Module loaded
Program started
```

### Import:

```python
import app
```

Output:

```text
Module loaded
```

`Program started` nahi chalega.

---

# 21. `sys.path`

Ab important question:

> Python ko kaise pata chalta hai ke `cell.py` kahan hai?

Python import search path use karta hai:

```python
import sys

print(sys.path)
```

Ye paths ki list hoti hai.

Python imported module ko locate karne ke liye import machinery mein in search locations ka use karta hai.

---

# 22. `sys.path` mein kya ho sakta hai?

Typical environment mein entries ho sakti hain:

```text
current/script-related location
standard library
site-packages
virtual environment packages
other configured paths
```

Exact order/environment vary kar sakta hai.

---

# 23. `sys.path` ka practical importance

Agar:

```python
import mymodule
```

fail ho:

```text
ModuleNotFoundError
```

to ek question:

> Python `mymodule` ko search kahan kar raha tha?

Check:

```python
import sys

for path in sys.path:
    print(path)
```

Ye import debugging mein useful hai.

---

# 24. `sys.modules`

Python imported modules ko runtime mein cache karta hai.

Check:

```python
import sys

print("math" in sys.modules)
```

Agar math already imported hai:

```text
True
```

`sys.modules` basically loaded module objects ka registry/cache hai.

---

# 25. Import caching

Suppose:

```python
import mymodule
import mymodule
```

Python har baar file ko completely fresh load nahi karta.

Loaded module `sys.modules` mein available ho sakta hai.

Conceptually:

```text
first import
    ↓
find module
    ↓
load
    ↓
sys.modules mein store

second import
    ↓
sys.modules check
    ↓
existing module use
```

---

# 26. `importlib`

Python ka module import system programmatically control/inspect karne ke liye:

```python
import importlib
```

Example:

```python
module = importlib.import_module("math")

print(module.sqrt(16))
```

Output:

```text
4.0
```

Yani module name string ke form mein ho sakta hai.

---

# 27. Dynamic import

Normal:

```python
import math
```

Dynamic:

```python
import importlib

name = "math"

math_module = importlib.import_module(name)
```

Ye plugin systems mein useful hai.

Example:

```text
plugin_name = "hvac_plugin"
        ↓
importlib.import_module(plugin_name)
```

---

# 28. Package architecture

Tumhare Python project ko aise organize kiya ja sakta hai:

```text
workorder_app/
│
├── pyproject.toml
│
└── workorder/
    ├── __init__.py
    ├── models.py
    ├── validation.py
    ├── folders.py
    ├── sheets.py
    └── main.py
```

Relationships:

```text
models.py
→ data classes

validation.py
→ validation logic

folders.py
→ folder creation

sheets.py
→ Google Sheets

main.py
→ application entry point
```

---

# 29. Internal imports

`validation.py`:

```python
from .models import WorkOrder
```

`folders.py`:

```python
from .models import WorkOrder
```

`sheets.py`:

```python
from .models import WorkOrder
```

Yahan `.` ka matlab:

```text
workorder package
```

---

# 30. Import architecture

Overall:

```text
workorder
│
├── models
│      ↑
│      │
├── validation
│      │
├── folders
│      │
└── sheets
```

Modules ek doosre ke components import karte hain.

Good architecture mein dependencies ideally understandable honi chahiye.

---

# 31. Circular import

Important problem:

```text
A imports B
B imports A
```

Example:

```python
# a.py
from b import B
```

and:

```python
# b.py
from a import A
```

Isse circular import problems aa sakti hain.

Conceptually:

```text
a.py
 ↓
b.py
 ↓
a.py
 ↓
b.py
...
```

Python partially initialized modules ke state mein errors de sakta hai.

---

# 32. Circular import ko avoid kaise karein?

Usually architecture improve karo.

Bad:

```text
models
 ↕
services
```

Better:

```text
models
  ↑
services
  ↑
main
```

Yani lower-level module ko upper-level application module par unnecessary dependency na do.

Kabhi shared functionality ko third module mein move karna useful hota hai:

```text
a.py ───→ common.py ←─── b.py
```

instead of:

```text
a.py ↔ b.py
```

---

# 33. `__init__.py` as package API

Suppose:

```text
equipment/
├── __init__.py
├── ahu.py
└── vav.py
```

`ahu.py`:

```python
class AHU:
    pass
```

`vav.py`:

```python
class VAV:
    pass
```

`__init__.py`:

```python
from .ahu import AHU
from .vav import VAV
```

Now users can write:

```python
from equipment import AHU, VAV
```

instead of:

```python
from equipment.ahu import AHU
from equipment.vav import VAV
```

So `__init__.py` can define a convenient public package interface.

---

# 34. `__all__`

Package/module mein:

```python
__all__ = ["AHU", "VAV"]
```

define kar sakte ho.

Then:

```python
from equipment import *
```

ke behavior ko `__all__` influence kar sakta hai.

Lekin:

> `from module import *` generally normal application code mein avoid karna better hai, kyunki namespace unclear ho jata hai.

Explicit imports better:

```python
from equipment import AHU, VAV
```

---

# 35. `__name__`, `__package__`, `__spec__`

Import system mein aur metadata bhi hota hai.

```python
print(__name__)
print(__package__)
print(__spec__)
```

### `__name__`

Module ka name.

### `__package__`

Package context.

### `__spec__`

Module ki import specification/metadata.

Tumhare:

```python
from .cell import Cell
```

jaise relative imports ko samajhne mein `__package__` especially relevant hai.

---

# 36. Absolute vs relative — final comparison

| Syntax                            | Meaning                 |
| --------------------------------- | ----------------------- |
| `import cell`                     | module import           |
| `from cell import Cell`           | module se specific name |
| `from equipment.cell import Cell` | absolute package path   |
| `from .cell import Cell`          | current package se      |
| `from ..cell import Cell`         | parent package level se |

---

# 37. Tumhare `.cell` wale question ka exact answer

Agar file structure hai:

```text
package/
│
├── __init__.py
├── cell.py
└── manager.py
```

aur `manager.py` mein:

```python
from .cell import Cell
```

to:

```text
.
↓
current package = package

cell
↓
cell.py

Cell
↓
cell.py ke andar class/name
```

So full conceptual path:

```text
package
   ↓
cell.py
   ↓
Cell
```

---

# 38. Most important mental model

```text
.py file
   ↓
Module

folder/package structure
   ↓
Package

import
   ↓
Python import machinery

sys.path
   ↓
Search locations

sys.modules
   ↓
Loaded module cache

__name__
   ↓
Module identity/context

__package__
   ↓
Package context

.
   ↓
Current package

..
   ↓
Parent package
```

---

# 39. Ek complete example

Structure:

```text
project/
│
├── main.py
│
└── equipment/
    ├── __init__.py
    ├── cell.py
    └── manager.py
```

### `cell.py`

```python
class Cell:

    def read(self):
        return "Temperature = 22.5"
```

### `manager.py`

```python
from .cell import Cell


class Manager:

    def read_cell(self):
        cell = Cell()
        return cell.read()
```

### `main.py`

```python
from equipment.manager import Manager


def main():
    manager = Manager()
    print(manager.read_cell())


if __name__ == "__main__":
    main()
```

Run from project root:

```bash
python main.py
```

Output:

```text
Temperature = 22.5
```

Flow:

```text
main.py
   ↓
equipment.manager
   ↓
manager.py
   ↓
.cell
   ↓
cell.py
   ↓
Cell
```

---

# 40. Golden Rules

```text
1. `.py` file → module.

2. Package → modules ko organize karne ka namespace.

3. `import x`
   → module import.

4. `from x import Y`
   → x se Y import.

5. `.`
   → current package.

6. `..`
   → parent package.

7. `__name__`
   → module ka runtime name/context.

8. `__main__`
   → direct execution context.

9. `sys.path`
   → import search locations.

10. `sys.modules`
    → loaded module cache/registry.

11. `importlib`
    → programmatic/dynamic imports.

12. `__init__.py`
    → package initialization/public API ke liye useful.

13. Relative import ko package context chahiye.

14. Circular imports ko architecture se avoid karna generally better hai.
```

## Next Lesson 54

Ab hum **Python import system ka aur deeper level** karenge:

```text
import machinery
     ↓
Finder
     ↓
Loader
     ↓
ModuleSpec
     ↓
sys.meta_path
     ↓
__pycache__
     ↓
.pyc
```

Isse tum samjhoge ke Python internally:

> **`import` likhne ke baad module ko find, load aur execute actually kaise karta hai.**

# Lesson 54: Python Import Machinery — Finder, Loader, `ModuleSpec`, `sys.meta_path`

Ab hum `import` ko **andar se** samjhenge.

Pichli lesson mein humne dekha:

```python
from .cell import Cell
```

Lekin ab sawal hai:

> Python ko actually kaise pata chalta hai ke `cell` module kahan hai aur usko load kaise karna hai?

Iske liye Python ke import system mein kuch important components hain:

```text
import
  ↓
sys.meta_path
  ↓
Finder
  ↓
ModuleSpec
  ↓
Loader
  ↓
Module object
  ↓
execute module code
  ↓
sys.modules
```

---

# 1. Sabse pehle `import` ka basic concept

Agar tum likho:

```python
import math
```

Python roughly ye process karta hai:

```text
1. Kya math already loaded hai?
        ↓
2. Agar nahi → module find karo
        ↓
3. Module ki specification banao
        ↓
4. Module object create karo
        ↓
5. Module ka code execute karo
        ↓
6. sys.modules mein register karo
```

Ye exact internal implementation is simplified flow se zyada complex hai, lekin learning ke liye ye correct mental model hai.

---

# 2. `sys.modules`

Pehle:

```python
import sys
```

Ab:

```python
print("math" in sys.modules)
```

Agar `math` loaded hai:

```text
True
```

`sys.modules` mein module name → module object mapping hoti hai.

Conceptually:

```text
sys.modules
│
├── "math"       → math module object
├── "sys"        → sys module object
├── "os"         → os module object
└── ...
```

---

# 3. Import caching

Suppose:

```python
import math
import math
import math
```

Python normally har baar `math.py` ko fresh execute nahi karta.

Conceptually:

```text
First import
    ↓
find + load + execute
    ↓
sys.modules["math"]

Second import
    ↓
sys.modules mein math mil gaya
    ↓
existing module use
```

Isliye `sys.modules` import system ka bohat important part hai.

---

# 4. Finder kya hai?

Finder ka kaam:

> **Module ko locate karna aur batana ke is module ko kaise load kiya ja sakta hai.**

Example:

```python
import mymodule
```

Python ko pata karna hai:

```text
mymodule kahan hai?
```

Finder is process mein help karta hai.

---

# 5. Loader kya hai?

Finder module ko locate/specify karta hai.

Loader ka kaam roughly:

> **Module ko create/load karna aur uska code execute karna.**

Simple distinction:

```text
Finder
→ "Module kahan hai?"

Loader
→ "Module ko load/execute kaise karna hai?"
```

---

# 6. `ModuleSpec`

Finder normally module ke liye ek:

```python
ModuleSpec
```

provide karta hai.

Ismein module ke import-related metadata hoti hai.

Example:

```python
import math

print(math.__spec__)
```

Tumhein ek `ModuleSpec` representation mil sakti hai.

Conceptually:

```text
ModuleSpec
│
├── name
├── loader
├── origin
├── submodule_search_locations
└── ...
```

---

# 7. `__spec__`

Har properly imported module ke paas aksar:

```python
module.__spec__
```

available hota hai.

Example:

```python
import math

print(math.__spec__)
```

Ye tumhein batata hai ke module import machinery ke perspective se kis specification ke saath load hua.

---

# 8. `__spec__.name`

```python
import math

print(math.__spec__.name)
```

Output:

```text
math
```

---

# 9. `__spec__.loader`

```python
print(math.__spec__.loader)
```

Ye loader object/reference ke baare mein information de sakta hai.

Conceptually:

```text
ModuleSpec
   │
   └── loader
         ↓
       Loader
```

---

# 10. `__spec__.origin`

```python
print(math.__spec__.origin)
```

Module ki origin information mil sakti hai.

Built-in/extension modules ke liye normal `.py` file path zaroori nahi hota.

Example output environment ke mutabiq kuch is type ka ho sakta hai:

```text
built-in
```

Ya file-based module ke liye:

```text
C:\project\mymodule.py
```

---

# 11. `sys.meta_path`

Ab sabse important part:

```python
import sys

print(sys.meta_path)
```

Ye **meta path finders** ki list hoti hai.

Python import karte waqt in finders ko use karta hai.

Conceptually:

```text
import mymodule
       ↓
sys.meta_path
       ↓
Finder 1
       ↓
Finder 2
       ↓
Finder 3
       ↓
matching finder
```

---

# 12. Finder sequence

Suppose:

```python
import xyz
```

Conceptually:

```text
Python
  ↓
Finder #1
  ↓
"xyz? nahi"
  ↓
Finder #2
  ↓
"xyz? nahi"
  ↓
Finder #3
  ↓
"xyz mil gaya"
```

Matching finder `ModuleSpec` return kar sakta hai.

Agar koi finder module nahi find karta, next finder try hota hai.

---

# 13. `sys.path` vs `sys.meta_path`

Ye dono confuse nahi karna.

### `sys.path`

Search locations ka data:

```text
folders/directories
```

### `sys.meta_path`

Import finders:

```text
finder mechanisms
```

Mental model:

```text
sys.meta_path
→ "Kis mechanism se module find karna hai?"

sys.path
→ "File-system based finder ko kin locations mein search karna hai?"
```

---

# 14. `PathFinder`

Python standard import system mein ek important finder:

```python
import importlib.machinery
```

Aur:

```python
importlib.machinery.PathFinder
```

Path-based modules ko locate karne mein important hai.

Conceptually:

```text
sys.meta_path
      ↓
PathFinder
      ↓
sys.path
      ↓
module file/package
```

---

# 15. `FileFinder`

File-based imports mein `FileFinder` bhi important mechanism hai.

Ye filesystem locations par module/package files discover karne mein use hota hai.

Conceptually:

```text
sys.path
   ↓
FileFinder
   ↓
.py
package
extension module
...
```

---

# 16. Module ke possible forms

Python module sirf `.py` file nahi hota.

Module different sources se aa sakta hai:

```text
.py source module
built-in module
extension module
package
namespace package
```

Example:

```python
import math
```

`math` normal Python source file jaisa zaroori nahi.

---

# 17. Built-in module

Example:

```python
import sys
```

`sys` Python interpreter ke saath built-in module hai.

Isliye iska origin normal:

```text
C:\something\sys.py
```

jaisa nahi hota.

---

# 18. Source module

Tumhari file:

```text
cell.py
```

is a source module.

Example:

```python
class Cell:
    pass
```

Import:

```python
from cell import Cell
```

---

# 19. Package import

Suppose:

```text
equipment/
├── __init__.py
└── cell.py
```

Tum:

```python
import equipment
```

kar sakte ho.

Yahan `equipment` package hai.

Package ka apna module object hota hai.

---

# 20. Submodule import

```python
import equipment.cell
```

Yahan:

```text
equipment
   ↓
cell
```

dono import system mein relevant modules/package objects ho sakte hain.

After import:

```python
equipment.cell
```

access karna possible hota hai.

---

# 21. `__path__`

Packages mein ek interesting attribute hota hai:

```python
equipment.__path__
```

Ye package ke submodules ko search karne ke relevant locations represent karta hai.

Normal module:

```text
cell.py
```

aur package:

```text
equipment/
```

mein important difference ye hai ke package submodules rakh sakta hai.

---

# 22. `__file__`

File-backed module ke liye:

```python
import mymodule

print(mymodule.__file__)
```

Example:

```text
C:\project\mymodule.py
```

Ye module file ki location discover karne ke liye useful hai.

Lekin:

> Har module ke paas meaningful `__file__` hona zaroori nahi, especially built-in/extension/special modules.

---

# 23. `__cached__`

Python source module ke saath:

```python
print(mymodule.__cached__)
```

cache file location ke baare mein information de sakta hai, agar applicable ho.

Usually ye `.pyc` file se related hota hai.

---

# 24. `__pycache__`

Suppose:

```text
project/
├── main.py
└── cell.py
```

Python source module import karne ke baad directory mein:

```text
__pycache__/
```

directory appear ho sakti hai.

Example:

```text
project/
│
├── main.py
├── cell.py
│
└── __pycache__/
    └── cell.cpython-3xx.pyc
```

---

# 25. `.pyc` kya hai?

`.pyc` = Python bytecode cache.

Python source:

```text
cell.py
```

ko interpreter internally bytecode mein compile karta hai.

Conceptually:

```text
cell.py
   ↓
bytecode
   ↓
.pyc
```

Python bytecode interpreter/virtual machine ke liye intermediate representation hai.

---

# 26. Kya `.pyc` machine code hai?

Nahi.

Important:

```text
.py
→ source code

.pyc
→ Python bytecode

machine code
→ CPU-specific native instructions
```

`.pyc` CPU ka direct machine code nahi hota.

---

# 27. `__pycache__` ka purpose

Repeated imports/startups mein cached bytecode compilation cost ko reduce kar sakta hai.

Conceptually:

```text
First time
.py
 ↓
compile
 ↓
bytecode
 ↓
cache

Later
.py + valid cache
 ↓
cached bytecode use ho sakta hai
```

Python validity/version/timestamp/hash details ke basis par cache use karta hai.

---

# 28. `.pyc` manually edit nahi karna

Normally:

```text
__pycache__
.pyc
```

ko manually manage karne ki zaroorat nahi.

Python khud generate/update karta hai.

---

# 29. `importlib.util.find_spec()`

Ab practical introspection.

```python
import importlib.util

spec = importlib.util.find_spec("math")

print(spec)
```

Ye module ke liye `ModuleSpec` discover karne mein useful hai.

---

# 30. Example: `find_spec()`

```python
import importlib.util

spec = importlib.util.find_spec("json")

print(spec.name)
print(spec.loader)
print(spec.origin)
```

Tum module ko actually import kiye baghair uski import specification ke baare mein information obtain kar sakte ho.

Lekin package/import side effects aur parent-package behavior jaise nuances ho sakte hain, isliye `find_spec()` ko simply "zero-effect" guarantee na samjho.

---

# 31. `importlib.import_module()`

Dynamic import:

```python
import importlib

module = importlib.import_module("math")

print(module.sqrt(25))
```

Output:

```text
5.0
```

Difference:

```text
import math
```

vs:

```python
importlib.import_module("math")
```

Second case mein module name runtime string se aa sakta hai.

---

# 32. Plugin system example

Suppose:

```text
plugins/
├── hvac.py
├── electrical.py
└── plumbing.py
```

Application ke paas:

```python
plugin_name = "plugins.hvac"
```

Then:

```python
import importlib

plugin = importlib.import_module(plugin_name)
```

Ab runtime par plugin load ho sakta hai.

Flow:

```text
plugin name
     ↓
importlib
     ↓
Finder
     ↓
ModuleSpec
     ↓
Loader
     ↓
Module
```

---

# 33. Custom Finder/Loader

Python theoretically tumhein custom import mechanism banane deta hai.

For example:

```text
import mydata
```

aur custom finder decide kare:

> `mydata` ko database/API/custom storage se load karo.

Ye advanced framework/plugin systems mein possible hai.

Iske liye `importlib.abc` ke finder/loader interfaces relevant hain.

---

# 34. Custom finder ka conceptual idea

```text
Python:
"mujhe myplugin chahiye"

        ↓

Custom Finder:
"haan, mujhe pata hai myplugin kahan hai"

        ↓

ModuleSpec

        ↓

Custom Loader:
"main iska module object load karunga"

        ↓

Python module
```

Yani import system extensible hai.

---

# 35. `MetaPathFinder`

Custom finder generally:

```python
import importlib.abc
```

se related ABCs use kar sakta hai.

Conceptually:

```python
class MyFinder(importlib.abc.MetaPathFinder):
    ...
```

Phir:

```python
sys.meta_path
```

mein finder register kiya ja sakta hai.

**Lekin production code mein custom import hooks carefully use karne chahiye**, kyunki import behavior complex ho sakta hai.

---

# 36. `Loader`

Loader ka conceptual interface:

```text
create module
     ↓
execute module
```

Modern import machinery mein `exec_module()` particularly important hai.

Conceptually:

```python
class MyLoader(...):
    def create_module(self, spec):
        ...

    def exec_module(self, module):
        ...
```

---

# 37. Finder + Loader relationship

```text
                 import
                   │
                   ↓
              Meta Path
                   │
                   ↓
                Finder
                   │
                   ↓
             ModuleSpec
              /       \
             /         \
        loader       metadata
           │
           ↓
        execute
           │
           ↓
        module
```

---

# 38. `ModuleSpec` ko simple language mein

`ModuleSpec` ko tum **import blueprint/recipe** samajh sakte ho.

Ismein information hoti hai:

```text
Module ka naam kya hai?
Loader kaun hai?
Origin kya hai?
Package hai?
Submodules kahan search honge?
```

Ye actual module nahi hai.

```text
ModuleSpec ≠ Module
```

Spec module ke import-related metadata/instructions ka object hai.

---

# 39. Module vs ModuleSpec

```text
ModuleSpec
→ module ko import karne ki information

Module
→ actual loaded Python module object
```

Example:

```python
import math

print(type(math))
```

→ module object.

```python
print(type(math.__spec__))
```

→ `ModuleSpec` object.

---

# 40. Import process ka deeper flow

Ab poora process:

```text
import equipment.cell
        │
        ↓
Check sys.modules
        │
        ├── already loaded → reuse
        │
        ↓
Find module
        │
        ↓
sys.meta_path
        │
        ↓
Finder
        │
        ↓
ModuleSpec
        │
        ↓
Loader
        │
        ↓
Create module
        │
        ↓
sys.modules mein register
        │
        ↓
Execute module code
        │
        ↓
Loaded module
```

Implementation details mein exact sequencing kuch cases mein nuanced hai, lekin ye strong conceptual model hai.

---

# 41. Module code execute kyun hota hai?

Suppose `cell.py`:

```python
print("Cell module loaded")

class Cell:
    pass
```

Aur:

```python
import cell
```

Output:

```text
Cell module loaded
```

Kyun?

Because import process module ke top-level code ko execute karta hai.

---

# 42. Isliye top-level side effects dangerous ho sakte hain

Bad design:

```python
# database.py

connect_to_production_database()
delete_old_records()
```

Ab:

```python
import database
```

karte hi side effects ho jayenge.

Better:

```python
def connect():
    ...

if __name__ == "__main__":
    connect()
```

Ya functions/classes ko expose karo aur explicit call karo.

---

# 43. Import aur execution ka relation

Important distinction:

```text
import
→ module load + top-level module execution

function call
→ function body execution

class definition
→ class creation process
```

Isliye import itself completely "passive file reading" nahi hai.

---

# 44. `reload()`

`importlib.reload()` exist karta hai:

```python
import importlib

import mymodule

importlib.reload(mymodule)
```

Ye module ko re-execute/reload karne ki koshish karta hai.

Useful ho sakta hai development/interactively, lekin production application state ke saath careful rehna chahiye.

---

# 45. `reload()` aur object references

Suppose:

```python
from mymodule import MyClass
```

phir:

```python
importlib.reload(mymodule)
```

Purane imported references aur newly defined objects ke beech identity/state differences aa sakte hain.

Isliye reload ko simply:

> "Sab kuch magically fresh ho gaya"

nahi samajhna.

---

# 46. Tumhare work-order project se connection

Suppose tumhara project:

```text
workorder/
│
├── models.py
├── validation.py
├── folders.py
├── sheets.py
└── main.py
```

`main.py`:

```python
from workorder.models import WorkOrder
from workorder.validation import validate
from workorder.folders import create_work_order_folders
```

Import system roughly:

```text
main
 ↓
workorder.models
 ↓
Finder
 ↓
Spec
 ↓
Loader
 ↓
models module
 ↓
WorkOrder available
```

Phir:

```text
workorder.validation
workorder.folders
```

same architecture follow karte hain.

---

# 47. Relative import yahan kaise fit hota hai?

`validation.py`:

```python
from .models import WorkOrder
```

Yahan:

```text
.
↓
workorder package
```

Python package context + import machinery ke through `models` ko resolve karta hai.

So tumhara pehle wala:

```python
from .cell import Cell
```

actually Python ke complete import system ka part hai.

---

# 48. Most important comparison

| Concept         | Simple meaning                     |
| --------------- | ---------------------------------- |
| `sys.path`      | Search locations                   |
| `sys.meta_path` | Finder mechanisms                  |
| Finder          | Module locate/specify karta hai    |
| `ModuleSpec`    | Import metadata/recipe             |
| Loader          | Module load/execute karta hai      |
| `sys.modules`   | Loaded module registry/cache       |
| `__file__`      | File location, if applicable       |
| `__path__`      | Package submodule search locations |
| `__pycache__`   | Bytecode cache directory           |
| `.pyc`          | Cached Python bytecode             |
| `importlib`     | Import machinery APIs              |

---

# 49. Ek powerful debugging example

Agar:

```python
import equipment
```

unexpected module load kar raha hai, inspect:

```python
import equipment

print(equipment)
print(equipment.__name__)
print(equipment.__file__)
print(equipment.__package__)
print(equipment.__spec__)
print(equipment.__path__)
```

Isse tumhein module ke import context ka bohat detailed view mil sakta hai.

---

# 50. Golden Mental Model

Isko yaad rakho:

```text
                IMPORT
                   │
                   ↓
            sys.modules?
             /         \
           yes          no
            │            │
          reuse      sys.meta_path
                         │
                         ↓
                      Finder
                         │
                         ↓
                   ModuleSpec
                         │
                         ↓
                      Loader
                         │
                         ↓
                   Module Object
                         │
                         ↓
                  Execute module
                         │
                         ↓
                    sys.modules
```

Aur filesystem-based normal imports mein:

```text
sys.meta_path
     ↓
PathFinder
     ↓
sys.path
     ↓
FileFinder
     ↓
.py / package / extension
```

---

## Lesson 54 ka core

Sabse important 5 cheezen:

```text
Finder
→ module ko locate karta hai

Loader
→ module ko load/execute karta hai

ModuleSpec
→ module ki import information

sys.meta_path
→ finders ki list

sys.modules
→ already loaded modules
```

Aur:

```text
.py
 ↓
source

.pyc
 ↓
Python bytecode cache

machine code
 ↓
CPU instructions
```

Ye teen alag concepts hain.

### Next Lesson 55

Ab hum **Python `property` → descriptor → `__getattribute__` → `__getattr__` → `__setattr__`** ko ek hi complete chain mein connect karenge.

Yani jab tum likhte ho:

```python
obj.temperature
```

Python internally **exactly kis order mein** decide karta hai ke value kahan se leni hai — ye deeply samjhenge.


# Lesson 55: Python Attribute Access — `property`, Descriptor aur `__getattribute__` ka Complete Connection

Ab hum Python ke **attribute access mechanism** ko deeply connect karenge.

Tum jab simple likhte ho:

```python
obj.temperature
```

to Python ke andar sirf "dictionary se value nikaalo" nahi hota. Iske peeche:

```text
__getattribute__
      ↓
Descriptor?
      ↓
instance __dict__?
      ↓
class attribute?
      ↓
__getattr__?
```

jaisi machinery involved ho sakti hai.

---

# 1. Sabse simple example

```python
class Equipment:
    def __init__(self):
        self.temperature = 22.5

ahu = Equipment()

print(ahu.temperature)
```

Output:

```text
22.5
```

Tum naturally soch sakte ho:

> `ahu.__dict__` mein temperature hai, isliye Python ne value de di.

Partially correct hai.

```python
print(ahu.__dict__)
```

Output:

```text
{'temperature': 22.5}
```

Lekin actual attribute access mechanism isse zyada general hai.

---

# 2. `__getattribute__`

Har normal attribute read:

```python
ahu.temperature
```

conceptually `__getattribute__()` ke through process hoti hai.

Example:

```python
class Equipment:

    def __init__(self):
        self.temperature = 22.5

    def __getattribute__(self, name):
        print("GET:", name)
        return super().__getattribute__(name)
```

Ab:

```python
ahu = Equipment()

print(ahu.temperature)
```

Output roughly:

```text
GET: temperature
22.5
```

---

# 3. `__getattribute__` har attribute par chalega

Agar:

```python
print(ahu.temperature)
```

to:

```text
GET: temperature
```

Agar:

```python
print(ahu.__dict__)
```

to `__dict__` access bhi `__getattribute__` se guzarta hai.

Yani:

> `__getattribute__` extremely broad hook hai.

---

# 4. Isliye recursion ka danger

Ye galat:

```python
class Equipment:

    def __getattribute__(self, name):
        print(self.__dict__)
        return self.__dict__[name]
```

Kyun?

Tum:

```python
self.__dict__
```

access kar rahe ho.

Lekin `__dict__` access bhi:

```python
__getattribute__
```

ko trigger karega.

Phir:

```text
__getattribute__
    ↓
self.__dict__
    ↓
__getattribute__
    ↓
self.__dict__
    ↓
...
```

Infinite recursion.

---

# 5. Correct technique

Isliye:

```python
super().__getattribute__(name)
```

use karna safe/common approach hai.

Example:

```python
class Equipment:

    def __init__(self):
        self.temperature = 22.5

    def __getattribute__(self, name):
        print("GET:", name)
        return super().__getattribute__(name)
```

Yahan actual normal lookup parent implementation ko delegate ho jata hai.

---

# 6. `__getattr__`

Ab doosra hook:

```python
__getattr__()
```

Ye **har access par nahi** chalta.

Ye tab chalta hai jab normal attribute lookup fail ho jaye.

Example:

```python
class Equipment:

    def __init__(self):
        self.temperature = 22.5

    def __getattr__(self, name):
        return f"{name} available nahi hai"
```

Then:

```python
ahu = Equipment()

print(ahu.temperature)
```

→

```text
22.5
```

But:

```python
print(ahu.pressure)
```

→

```text
pressure available nahi hai
```

---

# 7. `__getattribute__` vs `__getattr__`

Ye difference bohat important hai:

```text
__getattribute__
→ har attribute access ke liye

__getattr__
→ sirf jab normal lookup fail ho
```

Flow:

```text
obj.x
 ↓
__getattribute__("x")
 ↓
normal lookup successful?
 ├── yes → value
 └── no
       ↓
   __getattr__("x")
       ↓
     fallback
```

---

# 8. Ab descriptor enter hota hai

Descriptor:

```python
class Temperature:

    def __get__(self, instance, owner):
        return 22.5
```

Use:

```python
class Equipment:
    temperature = Temperature()
```

Then:

```python
ahu = Equipment()

print(ahu.temperature)
```

Output:

```text
22.5
```

Yahan `temperature` normal instance dictionary se zaroori nahi aa raha.

Descriptor intervene kar raha hai.

---

# 9. Descriptor ka core idea

Descriptor wo object hai jo:

```python
__get__()
__set__()
__delete__()
```

mein se methods provide karke attribute access control karta hai.

Example:

```python
class Temperature:

    def __get__(self, instance, owner):
        print("Descriptor GET")
        return 22.5
```

Then:

```python
class Equipment:
    temperature = Temperature()
```

---

# 10. `property` khud descriptor hai

Ye extremely important connection hai.

Jab tum likhte ho:

```python
class Equipment:

    @property
    def temperature(self):
        return self._temperature
```

to `property` internally descriptor mechanism use karta hai.

Yani:

```text
@property
    ↓
property object
    ↓
descriptor protocol
    ↓
attribute access
```

Isliye hum pehle jo:

```python
@property
```

seekh chuke hain, wo descriptor lesson se directly connected hai.

---

# 11. Property getter

Example:

```python
class Equipment:

    def __init__(self):
        self._temperature = 22.5

    @property
    def temperature(self):
        return self._temperature
```

Then:

```python
ahu.temperature
```

method call jaisa likha nahi:

```python
ahu.temperature()
```

balki:

```python
ahu.temperature
```

Lekin internally property descriptor getter ko invoke kar raha hota hai.

---

# 12. Property setter

```python
class Equipment:

    def __init__(self):
        self._temperature = 22.5

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("Invalid temperature")

        self._temperature = value
```

Now:

```python
ahu.temperature = 24
```

setter invoke hota hai.

Conceptually:

```text
ahu.temperature
       ↓
property.__get__()

ahu.temperature = 24
       ↓
property.__set__()
```

---

# 13. Data descriptor

Descriptor agar:

```python
__set__()
```

ya:

```python
__delete__()
```

provide karta hai, to wo **data descriptor** ho sakta hai.

Example:

```python
class PositiveNumber:

    def __get__(self, instance, owner):
        ...

    def __set__(self, instance, value):
        ...
```

Ye data descriptor hai.

`property` bhi data descriptor ho sakta hai jab setter/deleter present ho.

---

# 14. Non-data descriptor

Agar descriptor sirf:

```python
__get__()
```

provide kare:

```python
class Descriptor:

    def __get__(self, instance, owner):
        ...
```

to ye **non-data descriptor** hai.

Important difference:

```text
Data descriptor
→ __get__ + __set__ / __delete__

Non-data descriptor
→ only __get__
```

---

# 15. Attribute lookup priority

Ab main important part.

Simplified model for:

```python
obj.x
```

Python roughly ye priority follow karta hai:

```text
1. Data descriptor
       ↓
2. Instance __dict__
       ↓
3. Non-data descriptor
       ↓
4. Class attribute
       ↓
5. __getattr__ fallback
```

Ye sequence bohat important hai.

---

# 16. Data descriptor instance dictionary ko override kar sakta hai

Example:

```python
class Descriptor:

    def __get__(self, instance, owner):
        return "descriptor value"

    def __set__(self, instance, value):
        print("SET:", value)


class Equipment:
    temperature = Descriptor()
```

Agar:

```python
ahu = Equipment()
```

aur manually:

```python
ahu.__dict__["temperature"] = 100
```

kar do.

Phir:

```python
print(ahu.temperature)
```

data descriptor ki wajah se:

```text
descriptor value
```

mil sakta hai.

---

# 17. Instance `__dict__` ka role

Normal class:

```python
class Equipment:
    pass
```

Then:

```python
ahu = Equipment()
ahu.temperature = 22.5
```

Normally:

```python
ahu.__dict__
```

mein:

```python
{
    "temperature": 22.5
}
```

store ho sakta hai.

Isliye normal attributes dynamic hote hain.

---

# 18. Class attribute

Example:

```python
class Equipment:
    category = "HVAC"
```

Then:

```python
ahu = Equipment()

print(ahu.category)
```

`category` instance `__dict__` mein zaroori nahi hai.

Python class se value find kar sakta hai.

```python
print(Equipment.category)
```

→

```text
HVAC
```

---

# 19. Instance attribute class attribute ko shadow kar sakta hai

```python
class Equipment:
    category = "HVAC"

ahu = Equipment()

ahu.category = "Electrical"
```

Ab:

```python
print(ahu.category)
```

→

```text
Electrical
```

Aur:

```python
print(Equipment.category)
```

→

```text
HVAC
```

Kyun?

Instance namespace mein:

```python
ahu.__dict__
```

ab:

```python
{
    "category": "Electrical"
}
```

hai.

---

# 20. Lekin data descriptor ka behavior different hai

Agar class attribute data descriptor ho:

```text
data descriptor
```

to wo instance dictionary se priority le sakta hai.

Isliye descriptors powerful hain.

---

# 21. Methods bhi descriptor mechanism use karte hain

Ye bohat interesting connection hai.

Class:

```python
class Equipment:

    def start(self):
        print("Started")
```

Then:

```python
ahu = Equipment()
ahu.start
```

actually bound method produce karta hai.

Function class ke andar descriptor behavior ke through instance se bind hota hai.

Conceptually:

```text
Equipment.start
      ↓
function object

ahu.start
      ↓
bound method
      ↓
self = ahu
```

---

# 22. Isi liye `ahu.start()` kaam karta hai

Class mein:

```python
def start(self):
    ...
```

Tum:

```python
ahu.start()
```

likhte ho.

Python method ko object ke saath bind karta hai:

```text
ahu
 ↓
start
 ↓
bound method
 ↓
self = ahu
```

Ye descriptor protocol ka important practical example hai.

---

# 23. `classmethod` bhi descriptor hai

Tumne pehle:

```python
@classmethod
```

seekha.

Example:

```python
class Equipment:

    @classmethod
    def create(cls):
        return cls()
```

`classmethod` bhi descriptor machinery use karta hai.

Difference:

```text
instance method
→ self se bind

classmethod
→ class se bind
```

---

# 24. `staticmethod` bhi descriptor machinery se related hai

```python
class Equipment:

    @staticmethod
    def convert(value):
        return value * 2
```

Then:

```python
Equipment.convert(10)
```

No automatic:

```text
self
```

or:

```text
cls
```

pass hota.

`staticmethod` bhi class namespace mein descriptor object ke through behavior provide karta hai.

---

# 25. Ek single picture mein

Python ke ye concepts connected hain:

```text
                 Attribute Access
                       │
                       ↓
                __getattribute__
                       │
                       ↓
              Descriptor lookup
                 /          \
                /            \
       Data descriptor    Other lookup
            │                   │
            ↓                   ↓
        __get__              __dict__
        __set__                  │
        __delete__               ↓
                             Class attr
                                 │
                                 ↓
                            __getattr__
```

Aur:

```text
@property
classmethod
staticmethod
function methods
```

sab descriptor machinery se connected hain.

---

# 26. `__setattr__`

Ab write operation:

```python
ahu.temperature = 25
```

ke liye:

```python
__setattr__
```

hook relevant hai.

Example:

```python
class Equipment:

    def __setattr__(self, name, value):
        print("SET:", name, value)
        super().__setattr__(name, value)
```

Then:

```python
ahu = Equipment()

ahu.temperature = 25
```

Output:

```text
SET: temperature 25
```

---

# 27. `__setattr__` bhi recursion create kar sakta hai

Wrong:

```python
class Equipment:

    def __setattr__(self, name, value):
        self.name = name
```

Kyun?

```text
self.name = ...
 ↓
__setattr__
 ↓
self.name = ...
 ↓
__setattr__
 ↓
...
```

Infinite recursion.

Normal behavior delegate karo:

```python
super().__setattr__(name, value)
```

---

# 28. `__delattr__`

Deletion:

```python
del ahu.temperature
```

ke liye:

```python
__delattr__
```

hook relevant hai.

Example:

```python
class Equipment:

    def __delattr__(self, name):
        print("DELETE:", name)
        super().__delattr__(name)
```

---

# 29. Read/write/delete complete picture

```text
Read
obj.x
 ↓
__getattribute__
 ↓
descriptor / namespace / class
 ↓
__getattr__ if missing


Write
obj.x = value
 ↓
__setattr__
 ↓
descriptor __set__ if applicable
 ↓
storage


Delete
del obj.x
 ↓
__delattr__
 ↓
descriptor __delete__ if applicable
 ↓
remove
```

---

# 30. `__getattr__` ka practical HVAC use

Suppose BMS equipment object:

```python
class Equipment:

    def __init__(self):
        self.temperature = 22.5

    def __getattr__(self, name):
        return "Point not available"
```

Then:

```python
ahu.temperature
```

→ `22.5`

But:

```python
ahu.damper_position
```

→

```text
Point not available
```

Ye dynamic systems mein useful pattern ho sakta hai.

---

# 31. Dynamic points example

Aur advanced:

```python
class Equipment:

    def __init__(self):
        self.points = {
            "temperature": 22.5,
            "humidity": 45,
            "damper": 60
        }

    def __getattr__(self, name):
        if name in self.points:
            return self.points[name]

        raise AttributeError(name)
```

Now:

```python
ahu = Equipment()

print(ahu.temperature)
print(ahu.humidity)
print(ahu.damper)
```

Output:

```text
22.5
45
60
```

Yahan actual attributes nahi, dictionary data dynamic attribute access ke through expose ho raha hai.

---

# 32. Lekin `__getattr__` mein `None` return karna hamesha good idea nahi

Agar:

```python
def __getattr__(self, name):
    return None
```

to typo bhi silently hide ho sakta hai:

```python
ahu.temprature
```

instead of:

```python
ahu.temperature
```

Result:

```text
None
```

Bug detect karna difficult ho sakta hai.

Often better:

```python
raise AttributeError(name)
```

jab genuinely attribute available nahi ho.

---

# 33. `__getattribute__` kab use karna chahiye?

Ye very powerful hook hai.

Use cases:

```text
logging
access control
proxy objects
lazy loading
dynamic object systems
instrumentation
```

Lekin:

> Normal application code mein `__getattribute__` ko unnecessarily override nahi karna chahiye.

Kyunki har attribute access affect hota hai.

---

# 34. `__getattr__` kab better hai?

Agar sirf missing attributes ka fallback chahiye:

```python
def __getattr__(self, name):
    ...
```

usually simpler hai.

Comparison:

```text
__getattribute__
→ every access

__getattr__
→ missing access only
```

---

# 35. Property vs `__getattr__`

Agar specific known attribute:

```python
temperature
```

ko validate/control karna hai:

```python
@property
```

better choice ho sakta hai.

Agar arbitrary unknown names dynamically resolve karne hain:

```python
__getattr__
```

useful hai.

---

# 36. Descriptor vs property

`property`:

```python
@property
def temperature(self):
    ...
```

is a **specific built-in descriptor abstraction**.

Custom descriptor:

```python
class PositiveNumber:
    def __get__(...):
        ...
    def __set__(...):
        ...
```

reusable behavior multiple fields ke liye use kar sakta hai.

Example:

```python
class Equipment:
    temperature = PositiveNumber()
    humidity = PositiveNumber()
    pressure = PositiveNumber()
```

Ek descriptor teen attributes control kar sakta hai.

---

# 37. Descriptor ka reusable advantage

Without descriptor:

```python
class Equipment:

    @property
    def temperature(self):
        ...

    @temperature.setter
    def temperature(self, value):
        ...

    @property
    def humidity(self):
        ...

    @humidity.setter
    def humidity(self, value):
        ...
```

Code repetitive ho sakta hai.

Descriptor:

```python
class PositiveNumber:
    ...
```

Then:

```python
class Equipment:
    temperature = PositiveNumber()
    humidity = PositiveNumber()
    pressure = PositiveNumber()
```

Same validation logic reuse.

---

# 38. `__set_name__`

Custom descriptor mein:

```python
class PositiveNumber:

    def __set_name__(self, owner, name):
        self.name = name
```

Then:

```python
class Equipment:
    temperature = PositiveNumber()
    humidity = PositiveNumber()
```

Python descriptor ko names de sakta hai:

```text
temperature
humidity
```

Ye reusable descriptor design ko easy banata hai.

---

# 39. Complete descriptor example

```python
class PositiveNumber:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(
                f"{self.name} cannot be negative"
            )

        instance.__dict__[self.name] = value
```

Use:

```python
class Equipment:

    temperature = PositiveNumber()
    humidity = PositiveNumber()
```

Then:

```python
ahu = Equipment()

ahu.temperature = 22
ahu.humidity = 45
```

Works.

But:

```python
ahu.temperature = -5
```

raises:

```text
ValueError
```

---

# 40. Full attribute-access chain

Ab isko carefully dekho:

```python
ahu.temperature
```

Possible conceptual flow:

```text
ahu.temperature
      ↓
ahu.__getattribute__("temperature")
      ↓
Equipment class mein lookup
      ↓
temperature descriptor hai?
      ↓
YES
      ↓
descriptor.__get__(ahu, Equipment)
      ↓
value
```

Agar descriptor nahi:

```text
instance __dict__
      ↓
value found?
      ↓
YES → value
```

Agar nahi:

```text
class attribute
      ↓
found?
      ↓
YES → value
```

Agar still nahi:

```text
__getattr__("temperature")
      ↓
fallback / AttributeError
```

---

# 41. Sab concepts ko connect karo

Ab tumhare previous lessons ka connection:

```text
@property
   ↓
Descriptor

Instance methods
   ↓
Function descriptor behavior

classmethod
   ↓
Descriptor

staticmethod
   ↓
Descriptor

__getattribute__
   ↓
Central attribute-read hook

__getattr__
   ↓
Missing-attribute fallback

__setattr__
   ↓
Attribute-write hook

__delattr__
   ↓
Attribute-delete hook

__dict__
   ↓
Instance/class namespace
```

Ye Python object model ka core part hai.

---

# 42. `__slots__` ka connection

Tumne `__slots__` bhi padha tha.

Normal object:

```text
obj
 ↓
__dict__
 ↓
attributes
```

Slots:

```text
obj
 ↓
slots
 ↓
fixed attribute storage
```

Isliye slots use karne wale objects mein normal:

```python
obj.__dict__
```

available na bhi ho sakta hai.

Ye attribute storage model ko change karta hai.

---

# 43. Metaclass ka connection

Aur ek level upar:

```text
Instance attribute access
        ↓
object/type machinery

Class creation
        ↓
metaclass
```

Yani:

```text
object level
→ descriptors, __getattribute__, __dict__

class level
→ metaclass
```

Ye Python object model ki layered architecture hai.

---

# 44. Exam/interview mental model

Agar tumse poocha jaye:

> `obj.x` kaise resolve hota hai?

Short answer:

```text
__getattribute__()
      ↓
data descriptor
      ↓
instance __dict__
      ↓
non-data descriptor/class attribute
      ↓
__getattr__ fallback
```

Aur:

> `obj.x = value`?

```text
__setattr__()
      ↓
data descriptor __set__()
      ↓
normal storage
```

---

# 45. Final summary

```text
                 obj.x
                   │
                   ↓
           __getattribute__
                   │
                   ↓
          ┌────────────────┐
          │ Data Descriptor│
          └───────┬────────┘
                  │
                  ↓
              instance
              __dict__
                  │
                  ↓
        non-data descriptor
                  │
                  ↓
           class attribute
                  │
                  ↓
             __getattr__
```

### Golden rules:

```text
__getattribute__
→ har attribute read

__getattr__
→ missing attribute ka fallback

__setattr__
→ attribute assignment

__delattr__
→ attribute deletion

Descriptor
→ attribute access ka behavior control

property
→ built-in descriptor

__dict__
→ namespace/storage for normal instances

Data descriptor
→ instance __dict__ se priority

Method
→ function descriptor behavior ke through bind hota hai
```

### Next Lesson 56

Ab next hum **Python Object Model: `object`, `type`, metaclass aur instance — ye 4 levels actually kaise connected hain** deeply samjhenge:

```text
object
  ↑
instance
  ↑
class
  ↑
metaclass
```

Aur ye question solve karenge:

> **`type` khud kis type ka object hai, aur `object` aur `type` ka relationship exactly kya hai?**

# Lesson 56: Python Object Model — `object`, `type`, Class, Instance aur Metaclass

Ab hum Python ke object model ke **sabse fundamental concepts** mein ja rahe hain.

Pichli lessons mein humne:

* class
* object
* inheritance
* `type()`
* metaclass
* descriptors
* attribute lookup

sab alag-alag padhe.

Ab in sab ko **ek single model** mein connect karenge.

---

# 1. Sabse pehle: Python mein almost everything object hai

Python mein:

```python
x = 10
```

to `10` object hai.

```python
name = "AHU"
```

`"AHU"` object hai.

```python
items = [1, 2, 3]
```

list bhi object hai.

Aur interesting part:

```python
class Equipment:
    pass
```

`Equipment` bhi **object** hai.

Yani:

```text
10             → object
"AHU"          → object
[1, 2, 3]      → object
Equipment      → object
Equipment()    → object
```

---

# 2. Instance kya hai?

```python
class Equipment:
    pass

ahu = Equipment()
```

Yahan:

```text
Equipment
    ↓
class

ahu
    ↓
instance/object
```

`ahu` ko `Equipment` ka instance kehte hain.

Check:

```python id="3j8k0h"
print(type(ahu))
```

Output:

```text
<class '__main__.Equipment'>
```

---

# 3. `type(ahu)`

```python id="1l2t8m"
type(ahu)
```

ka matlab:

> `ahu` kis class ka instance hai?

Answer:

```text
Equipment
```

So:

```python id="0k0qxl"
ahu.__class__
```

bhi conceptually:

```text
Equipment
```

---

# 4. Lekin `Equipment` khud kya hai?

Ye interesting question hai:

```python id="xj5v9a"
type(Equipment)
```

Output:

```text
<class 'type'>
```

Yani:

```text
ahu
 ↓
Equipment ka instance

Equipment
 ↓
type ka instance
```

So:

```text id="6v4nq7"
ahu → Equipment
Equipment → type
```

---

# 5. `type` kya hai?

`type` Python ki built-in metaclass hai.

Simple mental model:

> **`type` classes ko create karne wali default metaclass hai.**

Normal class:

```python id="3t5hqa"
class Equipment:
    pass
```

roughly conceptual level par:

```text
Python class statement
        ↓
metaclass machinery
        ↓
type
        ↓
Equipment class object
```

---

# 6. `type()` ka double role

`type` interesting hai kyunki ye do major roles play karta hai.

### Role 1: object ka type discover karna

```python id="k4n3ve"
type(ahu)
```

→ `Equipment`

### Role 2: dynamically class create karna

```python id="m1q5td"
Employee = type(
    "Employee",
    (),
    {}
)
```

Ab:

```python id="w0v2ch"
Employee()
```

possible hai.

---

# 7. Dynamic class creation

Example:

```python id="7yq8z2"
Employee = type(
    "Employee",
    (),
    {
        "company": "ABC"
    }
)
```

Ye approximately equivalent hai:

```python id="8m5u4q"
class Employee:
    company = "ABC"
```

Then:

```python id="o2j6bq"
e = Employee()

print(e.company)
```

Output:

```text
ABC
```

---

# 8. `type(name, bases, namespace)`

Dynamic class creation ka basic formula:

```python id="2g9f4x"
type(
    class_name,
    base_classes,
    namespace
)
```

Example:

```python id="k1x4r7"
Animal = type(
    "Animal",
    (),
    {}
)
```

Three parts:

```text
"Animal"
   ↓
class name

()
   ↓
base classes

{}
   ↓
class namespace
```

---

# 9. Inheritance dynamically

Suppose:

```python id="f3f3f4"
class Equipment:
    def start(self):
        print("Started")
```

Dynamic child:

```python id="cz4v2d"
AHU = type(
    "AHU",
    (Equipment,),
    {}
)
```

Now:

```python id="8f8qpu"
ahu = AHU()

ahu.start()
```

Output:

```text
Started
```

Because:

```text
AHU
 ↓
Equipment
 ↓
object
```

---

# 10. `object` kya hai?

Python ka fundamental base class:

```python id="75xqkc"
object
```

Almost all normal Python classes ultimately `object` se inherit karti hain.

Example:

```python id="xj0qg4"
class Equipment:
    pass
```

Conceptually:

```text
Equipment
    ↓
object
```

Check:

```python id="l4z0o1"
Equipment.__bases__
```

Output:

```text
(<class 'object'>,)
```

---

# 11. `object` ka MRO

```python id="e8q0v1"
print(Equipment.__mro__)
```

Output:

```text
(
    <class '__main__.Equipment'>,
    <class 'object'>
)
```

Yani:

```text
Equipment
   ↓
object
```

---

# 12. `object` khud kya hai?

Ab:

```python id="z7r7z9"
type(object)
```

Output:

```text
<class 'type'>
```

So:

```text
object
   ↓
is an instance of
   ↓
type
```

Yani:

```text
type(object) == type
```

---

# 13. `type` khud kya hai?

Ab interesting:

```python id="4wz9g4"
type(type)
```

Output:

```text
<class 'type'>
```

Yani:

```text
type
 ↓
type
```

Conceptually `type` apni hi metaclass `type` ka instance hai.

Ye Python ke object model ka special self-referential part hai.

---

# 14. `object` aur `type` ko confuse mat karo

Important:

```text id="0fs5ck"
object
→ fundamental base class

type
→ default metaclass / class-creation machinery
```

Aur:

```python id="w6wz7q"
issubclass(Equipment, object)
```

→ `True`

Lekin:

```python id="d7z6pj"
isinstance(Equipment, type)
```

→ `True`

Ye different relationships hain.

---

# 15. Four important relationships

Ye table bohat important hai:

| Expression                      | Meaning                                        |
| ------------------------------- | ---------------------------------------------- |
| `isinstance(ahu, Equipment)`    | `ahu` is an instance of `Equipment`            |
| `issubclass(Equipment, object)` | `Equipment` inherits from `object`             |
| `isinstance(Equipment, type)`   | `Equipment` is an instance of metaclass `type` |
| `isinstance(type, type)`        | `type` is an instance of itself                |

---

# 16. Ek diagram

```text
                 type
               ↗  ↑  ↖
              /   │   \
             /    │    \
       Equipment object  type
          ↑        ↑
          │        │
         ahu      ...
```

Lekin is diagram ko carefully interpret karo.

Inheritance aur instance relationship **same arrow nahi** hain.

Better:

```text
INSTANCE RELATIONSHIP:

ahu ─────────→ Equipment
Equipment ───→ type
object ──────→ type
type ────────→ type
```

Aur:

```text
INHERITANCE:

Equipment
    ↓
  object
```

---

# 17. `isinstance()` vs `issubclass()` again

Example:

```python id="m6r6wt"
class Equipment:
    pass

class AHU(Equipment):
    pass

ahu = AHU()
```

Now:

```python id="fd8q3v"
isinstance(ahu, AHU)
```

→ `True`

```python id="8qkq8j"
isinstance(ahu, Equipment)
```

→ `True`

Because AHU inherits Equipment.

---

But:

```python id="8w0e8x"
issubclass(AHU, Equipment)
```

→ `True`

And:

```python id="9m9v77"
issubclass(ahu, Equipment)
```

error hoga, because `issubclass()` classes expect karta hai.

---

# 18. Class bhi object kyun hai?

Python mein class definition:

```python id="9d3q9v"
class Equipment:
    pass
```

sirf source-code template nahi.

Python runtime par **Equipment class object create karta hai**.

That class object has:

```text
attributes
methods
__dict__
__mro__
__bases__
__name__
__module__
__annotations__
```

etc.

Isliye:

```python id="r4l8h2"
Equipment.__dict__
```

possible hai.

---

# 19. Class creation ka flow

Normal:

```python id="w5d3l9"
class Equipment:
    pass
```

Conceptually:

```text
class statement
      ↓
class namespace prepare
      ↓
body execute
      ↓
metaclass selected
      ↓
metaclass creates class
      ↓
Equipment class object
```

Default case mein metaclass:

```text
type
```

hoti hai.

---

# 20. Custom metaclass

Agar:

```python id="2l8x6r"
class MyMeta(type):
    pass
```

aur:

```python id="q3j9m0"
class Equipment(metaclass=MyMeta):
    pass
```

to:

```python id="q7m8m1"
type(Equipment)
```

→

```text
MyMeta
```

Not ordinary `type`.

---

# 21. Metaclass ka role

Normal object:

```text
ahu
 ↓
Equipment
```

Class object:

```text
Equipment
 ↓
MyMeta
```

So:

```text
Instance
→ class

Class
→ metaclass
```

Metaclass class creation/control ke liye hoti hai.

---

# 22. Metaclass hierarchy

Suppose:

```python id="2l2h1s"
class MyMeta(type):
    pass
```

Then:

```python id="5wzj4b"
type(MyMeta)
```

likely:

```text
<class 'type'>
```

because `MyMeta` itself is a class whose metaclass is `type`.

So:

```text
MyMeta
   ↓
type
```

where arrow here means "instance of".

---

# 23. `type` ka inheritance

Check:

```python id="9q6e5q"
type.__bases__
```

Output:

```text
(<class 'object'>,)
```

So `type` itself is a subclass of `object`.

Interesting:

```text
type
 ↓
object
```

while:

```text
object
```

is an instance of:

```text
type
```

So inheritance aur instance relationships cross-connect karte hain.

---

# 24. Very important distinction

```text
"X is instance of Y"
```

means:

```python id="zv6xgv"
isinstance(X, Y)
```

While:

```text
"X inherits from Y"
```

means:

```python id="8e8q8m"
issubclass(X, Y)
```

Ye same cheez nahi hain.

---

# 25. `type` ka self-reference

```python id="w1m5o8"
type(type)
```

→ `type`

Isko beginner level par bas itna samjho:

> Python ne `type` ko special tarike se define kiya hai jahan `type` ki metaclass bhi `type` hi hai.

Ye circularity Python ke object model ko bootstrap karne ke liye designed hai.

---

# 26. `object` aur `type` ka relationship

Sabse important diagram:

```text
INSTANCE-OF:

ahu
 ↓
Equipment
 ↓
type

object
 ↓
type

type
 ↓
type
```

Aur inheritance:

```text
Equipment
    ↓
  object

type
    ↓
  object
```

Yahan dono arrows ka meaning different hai.

---

# 27. Isko table mein dekho

| Entity      | `type(entity)` | Parent   |
| ----------- | -------------- | -------- |
| `ahu`       | `Equipment`    | —        |
| `Equipment` | `type`         | `object` |
| `object`    | `type`         | —        |
| `type`      | `type`         | `object` |

`Parent` yahan inheritance relationship hai.

---

# 28. `__class__`

Har normal object mein:

```python id="g9h8wi"
obj.__class__
```

object ki class ko refer karta hai.

Example:

```python id="j9k3nw"
ahu.__class__
```

→ `Equipment`

And:

```python id="q3g2y4"
Equipment.__class__
```

→ `type`

And:

```python id="6g4h0v"
object.__class__
```

→ `type`

---

# 29. `__class__` aur `type()`

Generally:

```python id="g7m4m7"
type(obj)
```

aur:

```python id="f5e8d2"
obj.__class__
```

same class relationship ko expose karte hain.

Example:

```python id="x5w7j9"
type(ahu) is ahu.__class__
```

→ `True`

---

# 30. `__bases__`

Class ke direct parent classes:

```python id="p7t0cz"
Equipment.__bases__
```

Example:

```text
(object,)
```

AHU:

```python id="r1g6c8"
AHU.__bases__
```

→

```text
(Equipment,)
```

---

# 31. `__mro__`

Complete lookup order:

```python id="v4s8q6"
AHU.__mro__
```

Example:

```text
AHU
Equipment
object
```

So:

```text
__bases__
→ direct parents

__mro__
→ complete resolution order
```

---

# 32. Class object ka `__dict__`

```python id="6f9d1v"
Equipment.__dict__
```

class ka namespace deta hai.

Ismein ho sakta hai:

```text
__module__
__init__
start
temperature
__dict__
__weakref__
...
```

Ye isliye possible hai kyunki class khud object hai.

---

# 33. Class object ke attributes kaun control karta hai?

Class object ka type:

```python id="u0z1hz"
type(Equipment)
```

→ `type`.

Isliye class-level behavior mein metaclass important ho sakti hai.

Example:

```python id="j7k3u5"
class MyMeta(type):

    def __new__(mcls, name, bases, namespace):
        print("Creating:", name)
        return super().__new__(
            mcls,
            name,
            bases,
            namespace
        )
```

Then:

```python id="v4h8sj"
class Equipment(metaclass=MyMeta):
    pass
```

Output:

```text
Creating: Equipment
```

---

# 34. Instance creation vs class creation

Ye difference yaad rakho.

### Instance creation

```python id="z8d1ry"
ahu = Equipment()
```

roughly:

```text
Equipment.__new__()
      ↓
Equipment.__init__()
```

### Class creation

```python id="n3f2v7"
class Equipment:
    pass
```

roughly:

```text
type.__new__()
      ↓
class object
```

Agar custom metaclass hai:

```text
MyMeta.__new__()
      ↓
Equipment class
```

---

# 35. Previous lessons ka connection

Ab Lesson 16:

```text
__new__
```

instance creation se related tha.

Lesson 17:

```text
metaclass
```

class creation se related tha.

Ab distinction clear:

```text
Instance level:
Equipment()
   ↓
__new__
   ↓
__init__

Class level:
class Equipment:
   ↓
metaclass
   ↓
__new__
   ↓
class object
```

---

# 36. Descriptor bhi isi object model ka part hai

Suppose:

```python id="6m8o9y"
class Equipment:
    @property
    def temperature(self):
        return 22.5
```

`temperature` class namespace mein ek object hai.

```python id="1z4qg3"
Equipment.__dict__["temperature"]
```

property object mil sakta hai.

Aur:

```python id="8o4q7d"
type(Equipment.__dict__["temperature"])
```

→ `property`.

Yani:

```text
property
→ object

Equipment
→ class object

type(Equipment)
→ metaclass
```

---

# 37. Python object model ki layers

Ab ek useful layered model:

```text
LEVEL 1 — Instance
ahu
│
├── temperature
├── equipment_id
└── status
│
↓ type
│
LEVEL 2 — Class
Equipment
│
├── methods
├── descriptors
├── class attributes
└── __dict__
│
↓ type
│
LEVEL 3 — Metaclass
type / MyMeta
│
├── class creation
├── class-level behavior
└── metaclass attributes
│
↓
LEVEL 4 — object/type bootstrap relationship
```

---

# 38. Simple HVAC example

```python id="l5p9e4"
class Equipment:
    category = "HVAC"

    def start(self):
        print("Equipment started")


class AHU(Equipment):
    pass


ahu = AHU()
```

Relationships:

```text
ahu
 │
 │ instance of
 ↓
AHU
 │
 │ subclass of
 ↓
Equipment
 │
 │ subclass of
 ↓
object
```

Aur:

```text
AHU
 │
 │ instance of
 ↓
type
```

---

# 39. `isinstance()` ka deeper meaning

```python id="n5o6w8"
isinstance(ahu, Equipment)
```

Python inheritance hierarchy ko consider karta hai.

Because:

```text
ahu
 ↓
AHU
 ↓
Equipment
```

So `True`.

Similarly:

```python id="m4l0d7"
isinstance(ahu, object)
```

→ `True`.

Because all normal class instances ultimately object hierarchy mein hain.

---

# 40. `isinstance(Equipment, object)`

Ye bhi:

```python id="i8q5qk"
isinstance(Equipment, object)
```

→ `True`

Kyun?

Because `Equipment` khud ek object hai.

Ye beginners ke liye usually surprising hota hai.

---

# 41. `issubclass(type, object)`

```python id="f9j2c4"
issubclass(type, object)
```

→ `True`

Because:

```text
type
 ↓
object
```

inheritance relationship hai.

---

# 42. `isinstance(object, type)`

```python id="6u4j8w"
isinstance(object, type)
```

→ `True`

Because:

```text
object
 ↓
type
```

instance-of relationship hai.

---

# 43. Four expressions jo yaad karne hain

```python id="0xq1al"
isinstance(Equipment(), Equipment)
```

→ `True`

```python id="e9k3s1"
isinstance(Equipment, type)
```

→ `True`

```python id="k6q4pv"
isinstance(object, type)
```

→ `True`

```python id="1m9t3r"
isinstance(type, type)
```

→ `True`

---

# 44. `object` ko "root class" samjho

Beginner-friendly mental model:

```text
object
```

Python classes ke inheritance tree ka fundamental root hai.

Example:

```text
object
 ↑
Equipment
 ↑
AHU
```

Actually inheritance direction normally:

```text
AHU
 ↓
Equipment
 ↓
object
```

---

# 45. `type` ko "class factory/metaclass" samjho

Beginner-friendly:

```text
type
→ classes ka default metaclass
→ class objects create/manage karta hai
```

Example:

```python id="2kq4q4"
Equipment = type(
    "Equipment",
    (),
    {}
)
```

Yahan `type` class object create kar raha hai.

---

# 46. Lekin `type` ordinary factory nahi hai

Important nuance:

`type` ko sirf "factory function" samajhna incomplete hai.

Ye simultaneously:

```text
type()
→ runtime type inspection

type(name, bases, namespace)
→ dynamic class creation

type
→ metaclass
```

teen roles se related hai.

---

# 47. Object model ka final diagram

Is diagram ko save kar lo:

```text
                         ┌─────────────┐
                         │    type     │
                         └──────┬──────┘
                                │
                       instance-of
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
        Equipment            object             type
              │                 │
       instance-of        instance-of
              │                 │
              ▼                 ▼
             ahu              ...
```

Inheritance separately:

```text
AHU
 ↓
Equipment
 ↓
object
```

And metaclass:

```text
Equipment
 ↓ instance-of
type
```

---

# 48. Sabse important distinction

Ye 3 concepts kabhi mix mat karna:

### Instance

```text
ahu
```

### Class

```text
Equipment
```

### Metaclass

```text
type
```

Relationship:

```text
ahu
 ↓
Equipment
 ↓
type
```

Yahan har arrow **same meaning nahi** rakhta.

More precisely:

```text
ahu
 --instance of--> Equipment

Equipment
 --instance of--> type

Equipment
 --inherits from--> object

type
 --inherits from--> object

type
 --instance of--> type
```

---

# 49. One-line mental model

> **Object batata hai "main kis class ka hoon"; class batati hai "main kis metaclass se bana hoon"; aur inheritance batati hai "main kis parent class se behavior leta hoon."**

Example:

```text
ahu
→ AHU

AHU
→ type

AHU
→ Equipment
→ object
```

---

# 50. Golden Rules

```text
1. Python mein classes bhi objects hain.

2. Normal object:
   type(obj) → uski class.

3. Normal class:
   type(Class) → usually type.

4. object:
   fundamental base class.

5. type:
   default metaclass.

6. Equipment inherits object.

7. Equipment is an instance of type.

8. type itself is an instance of type.

9. __bases__
   → direct parent classes.

10. __mro__
    → complete inheritance lookup order.

11. __class__
    → object's class.

12. __new__/__init__
    → instance creation.

13. metaclass
    → class creation/control.
```

---

## Next Lesson 57

Ab hum **`abc.ABC` vs `Protocol` vs Duck Typing vs `collections.abc`** ko ek hi architecture mein compare karenge.

Especially:

```text
ABC
Protocol
Duck Typing
Structural Typing
Nominal Typing
collections.abc
```

Aur ye practical question solve karenge:

> **Agar mujhe `start()` method wala AHU/VAV/Sensor accept karna hai, to `ABC`, `Protocol`, ya simple Duck Typing mein se architecture ke hisaab se kya difference hota hai?**

# Lesson 57: ABC vs Protocol vs Duck Typing vs `collections.abc`

Ab hum Python mein **interface/contract design** ko properly samjhenge.

Tumne ye concepts pehle separately padhe hain:

```text
ABC
Protocol
Duck Typing
Structural Typing
Nominal Typing
collections.abc
```

Ab inko ek hi picture mein connect karte hain.

---

# 1. Problem kya hai?

Suppose hamare paas different equipment hain:

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
```

Ab function:

```python
def start_equipment(equipment):
    equipment.start()
```

Tum:

```python
start_equipment(AHU())
start_equipment(VAV())
start_equipment(Pump())
```

kar sakte ho.

Question:

> Python ko kaise pata hai ke ye objects acceptable hain?

Yahan se **Duck Typing** aati hai.

---

# 2. Duck Typing

Simple rule:

> Agar object required operation kar sakta hai, to use kar lo.

```python
def start_equipment(equipment):
    equipment.start()
```

Function ye nahi pooch raha:

```python
isinstance(equipment, AHU)
```

ya:

```python
isinstance(equipment, VAV)
```

Bas:

```python
equipment.start()
```

kar raha hai.

Agar `start()` hai → kaam karega.

---

# 3. Duck Typing ka famous mental model

Python ka philosophy:

> "Object ka naam/type kya hai" se zyada important hai "object kya kar sakta hai."

Example:

```python
class Remote:
    def start(self):
        print("Remote command")


class Motor:
    def start(self):
        print("Motor started")
```

Dono:

```python
start_equipment(Remote())
start_equipment(Motor())
```

accept kar sakte hain.

Chahe `Remote` equipment hierarchy mein ho hi na.

---

# 4. Lekin Duck Typing ka problem

Suppose:

```python
class BrokenEquipment:
    pass
```

Then:

```python
start_equipment(BrokenEquipment())
```

Runtime par:

```text
AttributeError:
'BrokenEquipment' object has no attribute 'start'
```

Yani contract explicitly documented/type-checked nahi tha.

---

# 5. ABC solution

ABC = **Abstract Base Class**.

```python
from abc import ABC, abstractmethod

class Startable(ABC):

    @abstractmethod
    def start(self):
        pass
```

Ab:

```python
class AHU(Startable):

    def start(self):
        print("AHU started")
```

AHU explicitly kehta hai:

> Main `Startable` interface/contract implement karta hoon.

---

# 6. ABC mein explicit inheritance hoti hai

```python
class AHU(Startable):
```

Ye **nominal typing** ka example hai.

Nominal ka matlab:

> Type relationship naam/declaration/inheritance ke through establish hota hai.

```text
AHU
 ↓
Startable
```

Python ko explicitly bataya gaya:

```python
AHU is a Startable
```

---

# 7. ABC ka benefit

Agar class:

```python
class AHU(Startable):
    pass
```

aur `start()` implement nahi karti, to:

```python
AHU()
```

normally instantiate nahi ho sakta.

Error:

```text
TypeError:
Can't instantiate abstract class AHU
```

Yani ABC runtime par contract enforce kar sakta hai.

---

# 8. Protocol ka approach

Ab:

```python
from typing import Protocol

class Startable(Protocol):

    def start(self) -> None:
        ...
```

Ab AHU ko explicitly inherit karna zaroori nahi:

```python
class AHU:

    def start(self):
        print("AHU started")
```

Phir static type checker ke perspective se:

```text
AHU
 ↓
has required structure
 ↓
compatible with Startable
```

---

# 9. Protocol = structural typing

Protocol ka core idea:

> Agar object required structure provide karta hai, to wo compatible hai.

AHU:

```python
class AHU:
    def start(self):
        ...
```

VAV:

```python
class VAV:
    def start(self):
        ...
```

Dono `Startable` protocol ke compatible ho sakte hain.

Explicit:

```python
class AHU(Startable):
```

likhna zaroori nahi.

---

# 10. Nominal vs Structural

Ye distinction bohat important hai.

### Nominal

```python
class AHU(Startable):
    ...
```

Relationship:

```text
AHU
 ↓
explicitly declared
 ↓
Startable
```

### Structural

```python
class AHU:
    def start(self):
        ...
```

Relationship:

```text
AHU
 ↓
has required structure
 ↓
Startable-compatible
```

---

# 11. ABC vs Protocol

| Feature                             | ABC                                    | Protocol                       |
| ----------------------------------- | -------------------------------------- | ------------------------------ |
| Explicit inheritance                | Usually yes                            | Usually no                     |
| Typing style                        | Nominal                                | Structural                     |
| Abstract methods                    | Yes                                    | Interface declarations         |
| Runtime enforcement                 | Stronger                               | Limited/default static focus   |
| Loose coupling                      | Less                                   | More                           |
| Existing unrelated class compatible | Usually needs inheritance/registration | Can be compatible structurally |
| Main purpose                        | Runtime class hierarchy/contract       | Static structural interface    |

---

# 12. Existing third-party class example

Suppose external library ka class hai:

```python
class ExternalMotor:
    def start(self):
        print("Motor started")
```

Tum usko modify nahi kar sakte.

ABC:

```python
class Startable(ABC):
    @abstractmethod
    def start(self):
        pass
```

ExternalMotor automatically subclass nahi hai.

Protocol:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...
```

ExternalMotor ke paas required `start()` hai.

So structural compatibility possible hai.

Yahan Protocol ka loose coupling advantage samajh aata hai.

---

# 13. Duck Typing vs Protocol

Dono similar lagte hain, lekin important difference hai.

### Duck Typing

Runtime philosophy:

```python
def start(obj):
    obj.start()
```

Python runtime bas call karta hai.

### Protocol

Type-checking contract:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...
```

Static type checker ko bata rahe ho:

> Function ko aisa object chahiye jisme `start()` available ho.

---

# 14. Same example

Duck typing:

```python
def start_equipment(equipment):
    equipment.start()
```

Protocol ke saath:

```python
from typing import Protocol

class Startable(Protocol):

    def start(self) -> None:
        ...


def start_equipment(equipment: Startable):
    equipment.start()
```

Runtime operation same hai:

```python
equipment.start()
```

Lekin type information much clearer ho gayi.

---

# 15. Protocol ka major advantage

Function signature:

```python
def start_equipment(equipment: Startable):
```

reader ko immediately pata hai:

> Mujhe koi bhi object do jo `Startable` interface satisfy karta ho.

Ye architecture ko document bhi karta hai.

---

# 16. `@runtime_checkable`

Protocol ko runtime `isinstance()` ke saath use karna ho to:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Then:

```python
class AHU:

    def start(self):
        print("Started")
```

Now:

```python
ahu = AHU()

print(isinstance(ahu, Startable))
```

Structural runtime check possible ho sakta hai.

---

# 17. Lekin `runtime_checkable` ki limitation

Important:

```python
isinstance(ahu, Startable)
```

runtime par mainly required members ki presence check karta hai.

Ye complete static type validation nahi karta.

For example annotations:

```python
def start(self) -> int:
```

vs:

```python
def start(self) -> str:
```

runtime structural check automatically full signature/type correctness prove nahi karta.

Static type checker is area mein much more useful hai.

---

# 18. `collections.abc` kya hai?

Python standard library mein:

```python
collections.abc
```

standard collection interfaces/ABCs provide karta hai.

Examples:

```python
from collections.abc import (
    Iterable,
    Iterator,
    Sequence,
    Mapping,
    MutableMapping,
    Callable
)
```

Ye tum Lesson 43 mein padh chuke ho.

---

# 19. `Iterable`

Agar function ko sirf iteration chahiye:

```python
from collections.abc import Iterable

def process(items: Iterable[str]):
    for item in items:
        print(item)
```

Ab function ko specifically `list` nahi chahiye.

Ye accept kar sakta hai:

```python
list
tuple
set
generator
```

agar appropriate iterable hain.

---

# 20. `Sequence`

Agar tumhe:

* iteration
* indexing
* ordered sequence

chahiye:

```python
from collections.abc import Sequence

def first(items: Sequence[str]):
    return items[0]
```

Ab:

```python
first(["AHU", "VAV"])
first(("AHU", "VAV"))
```

dono reasonable hain.

Lekin arbitrary `Iterable` ko index nahi kar sakte.

---

# 21. `Mapping`

Agar function ko dictionary-like read access chahiye:

```python
from collections.abc import Mapping

def show_equipment(data: Mapping[str, str]):
    print(data["equipment_id"])
```

Tum function ko actual `dict` tak restrict nahi kar rahe.

Requirement hai:

> Mujhe mapping behavior chahiye.

---

# 22. `MutableMapping`

Agar function ko mapping modify bhi karni hai:

```python
from collections.abc import MutableMapping

def update_status(data: MutableMapping[str, str]):
    data["status"] = "ON"
```

Difference:

```text
Mapping
→ read mapping

MutableMapping
→ read + modify mapping
```

---

# 23. `Callable`

Agar function ko callable object chahiye:

```python
from collections.abc import Callable

def execute(action: Callable[[], None]):
    action()
```

Accept:

```python
def start():
    print("Started")

execute(start)
```

Aur callable class:

```python
class Command:

    def __call__(self):
        print("Command executed")
```

```python
execute(Command())
```

Dono callable hain.

---

# 24. Ye sab Protocol jaisa kyun lagta hai?

Because conceptually ye bhi **capabilities/interfaces** describe karte hain.

Example:

```text
Iterable
→ iterate kar sakta hai

Sequence
→ index kar sakta hai

Mapping
→ key/value access

Callable
→ () ke saath call ho sakta hai
```

Yani:

> Type ke naam se zyada required behavior important hai.

---

# 25. `collections.abc` aur Protocol same nahi

Ye important distinction hai.

`collections.abc`:

```python
Iterable
Sequence
Mapping
```

standardized Python collection abstractions hain.

Protocol:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...
```

tum **apna structural interface** define kar sakte ho.

So:

```text
collections.abc
→ Python ke standard collection interfaces

Protocol
→ apna/custom structural interface
```

---

# 26. ABC + `collections.abc`

`collections.abc` mein bohat se types ABC machinery use karte hain.

Example:

```python
from collections.abc import Sequence
```

`Sequence` ek standard abstraction hai.

Tum apna class design karte waqt relevant ABC ko implement/inherit bhi kar sakte ho, depending on the behavior you want.

---

# 27. `Iterable` ka practical example

Suppose work-order data:

```python
work_orders = [
    "WO-1001",
    "WO-1002",
    "WO-1003"
]
```

Function:

```python
def create_folders(work_orders: Iterable[str]):
    for wo in work_orders:
        print("Creating:", wo)
```

Ye sirf list ke liye nahi hai.

Generator bhi:

```python
def work_orders():
    yield "WO-1001"
    yield "WO-1002"
```

Then:

```python
create_folders(work_orders())
```

kaam kar sakta hai.

Ye **interface-based design** hai.

---

# 28. `Sequence` kab use karna hai?

Agar tum likh rahe ho:

```python
items[0]
items[1]
```

to:

```python
Sequence
```

zyada appropriate hai.

Example:

```python
def get_first_work_order(
    work_orders: Sequence[str]
) -> str:
    return work_orders[0]
```

Agar tum sirf:

```python
for wo in work_orders:
```

karte ho:

```python
Iterable
```

better abstraction hai.

---

# 29. Important design principle

Function ko unnecessarily concrete type mat do.

Instead of:

```python
def process(data: list[str]):
```

agar function ko sirf iteration chahiye:

```python
def process(data: Iterable[str]):
```

Better abstraction.

Agar sirf mapping read karni hai:

```python
Mapping
```

Agar modification bhi chahiye:

```python
MutableMapping
```

Agar callable chahiye:

```python
Callable
```

---

# 30. "Program to an interface"

Software engineering ka important principle:

> Concrete implementation ke bajaye required interface/capability par depend karo.

Example:

Badly restrictive:

```python
def process(data: list[dict]):
    ...
```

Agar actual requirement sirf iteration hai:

```python
def process(data: Iterable[Mapping[str, str]]):
    ...
```

Ab function zyada flexible hai.

---

# 31. HVAC architecture example

Suppose:

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
```

Custom Protocol:

```python
from typing import Protocol

class Startable(Protocol):

    def start(self) -> None:
        ...
```

Function:

```python
def start_system(
    equipment: Startable
) -> None:
    equipment.start()
```

Now:

```python
start_system(AHU())
start_system(VAV())
start_system(Pump())
```

Same interface.

Different implementation.

This is polymorphism + structural typing.

---

# 32. ABC version

```python
from abc import ABC, abstractmethod

class Startable(ABC):

    @abstractmethod
    def start(self) -> None:
        pass
```

Then:

```python
class AHU(Startable):

    def start(self):
        print("AHU started")
```

And:

```python
class VAV(Startable):

    def start(self):
        print("VAV started")
```

Yahan hierarchy explicitly defined hai.

---

# 33. Duck typing version

No ABC:

```python
def start_system(equipment):
    equipment.start()
```

That's it.

No formal interface.

Maximum simplicity, minimum explicit contract.

---

# 34. Teen approaches ka comparison

```text
DUCK TYPING

"start() call kar ke dekho."

        ↓

PROTOCOL

"Type checker, mujhe aisa object chahiye
jisme start() capability ho."

        ↓

ABC

"Is class hierarchy ka member bano
aur required methods implement karo."
```

---

# 35. Kab kya choose karna hai?

### Simple internal code

Duck typing often enough:

```python
def run(obj):
    obj.start()
```

### Public/library/API design

Protocol useful:

```python
class Startable(Protocol):
    def start(self) -> None: ...
```

Especially jab unrelated implementations ko support karna ho.

### Strong runtime hierarchy/contract

ABC useful:

```python
class Equipment(ABC):
    @abstractmethod
    def start(self):
        ...
```

Especially jab shared base implementation/state bhi ho.

### Standard collection behavior

`collections.abc`:

```python
Iterable
Sequence
Mapping
MutableMapping
Callable
```

---

# 36. ABC mein shared implementation bhi ho sakti hai

Ye Protocol se important difference ho sakta hai.

```python
from abc import ABC, abstractmethod

class Equipment(ABC):

    def log_start(self):
        print("Starting equipment...")

    @abstractmethod
    def start(self):
        pass
```

Child:

```python
class AHU(Equipment):

    def start(self):
        self.log_start()
        print("AHU started")
```

ABC shared code + contract dono provide kar sakti hai.

---

# 37. Protocol ka focus capability hai

```python
class Startable(Protocol):

    def start(self) -> None:
        ...
```

Iska focus:

```text
"start() capability"
```

hai, na ke:

```text
"tum Equipment hierarchy mein ho"
```

Isi liye Protocol loose coupling provide karta hai.

---

# 38. Protocol multiple capabilities combine kar sakta hai

Example:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...


class Stoppable(Protocol):
    def stop(self) -> None:
        ...
```

Phir:

```python
class Controllable(Startable, Stoppable, Protocol):
    pass
```

Conceptually:

```text
Controllable
 ├── start()
 └── stop()
```

Ab koi class jo dono capabilities provide kare, compatible ho sakti hai.

---

# 39. Interface segregation ka connection

Ye software design principle se connected hai.

Instead of giant interface:

```text
Equipment
 ├── start
 ├── stop
 ├── cool
 ├── heat
 ├── open_valve
 ├── close_valve
 └── calibrate
```

small capability interfaces:

```text
Startable
→ start()

Stoppable
→ stop()

Calibratable
→ calibrate()

ValveControllable
→ open()
→ close()
```

Zyada focused contracts ban sakte hain.

---

# 40. Final architecture

```text
                    Required Behavior
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
        Duck Typing    Protocol    collections.abc
             │            │            │
       runtime call   structural    standard
                       typing       interfaces
                          │
                          │
                          ▼
                     Type Checker


                ABC
                 │
                 ▼
          explicit hierarchy
          + runtime contract
          + shared behavior
```

---

# 41. Golden mental model

```text
Duck Typing
→ "Can you do it?"

Protocol
→ "Your structure says you can do it."

ABC
→ "You explicitly belong to this contract hierarchy."

collections.abc
→ "This is a standard Python collection capability."
```

### Aur typing style:

```text
ABC
→ Nominal typing

Protocol
→ Structural typing

Duck typing
→ Runtime behavioral approach
```

---

# 42. Practical rule

Agar tumhara function:

```python
for x in data:
```

karta hai:

```python
Iterable
```

Agar:

```python
data[0]
```

chahiye:

```python
Sequence
```

Agar:

```python
data["key"]
```

chahiye:

```python
Mapping
```

Agar:

```python
data["key"] = value
```

chahiye:

```python
MutableMapping
```

Agar:

```python
action()
```

chahiye:

```python
Callable
```

Agar custom capability:

```python
equipment.start()
```

chahiye:

```python
Protocol
```

Agar explicit class hierarchy + abstract contract:

```python
ABC
```

---

## Next Lesson 58

Ab hum **Python typing ka advanced part: `Generic`, `TypeVar`, variance aur Protocol ko ek practical architecture mein combine** karenge.

Example:

```python
Sensor[T]
Repository[T]
Handler[T]
```

aur samjhenge:

```text
T
T_co
T_contra
Generic[T]
Protocol[T]
Callable[P, R]
```

ek real application mein **ek doosre ke saath kaise kaam karte hain**.

# Lesson 58: `Generic[T]` + `TypeVar` + `Protocol` + Variance — Practical Architecture

Ab hum typing ke un concepts ko ek saath connect karenge jo pehle separately padhe:

```text
TypeVar
Generic
Protocol
covariance
contravariance
invariance
Callable
```

Is lesson ka main goal hai:

> **Ek generic system kaise design hota hai jahan same code different data types ke saath safely kaam kare?**

---

# 1. Pehle `TypeVar` ko yaad karo

```python
from typing import TypeVar

T = TypeVar("T")
```

`T` koi actual type nahi hai.

Ye ek **placeholder** hai.

Socho:

```text
T
↓
"Jo type caller provide karega"
```

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

Aur:

```python
identity("AHU")
```

to:

```text
T = str
```

Important:

```text
input T
   ↓
same T
   ↓
output
```

---

# 2. Generic class

Ab function ke bajaye class:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Storage(Generic[T]):

    def __init__(self):
        self.value: T | None = None

    def set(self, value: T):
        self.value = value

    def get(self) -> T | None:
        return self.value
```

Ab:

```python
numbers = Storage[int]()
```

Yahan:

```text
T = int
```

Aur:

```python
names = Storage[str]()
```

Yahan:

```text
T = str
```

---

# 3. Generic ka actual purpose

Without generic:

```python
class Storage:
    def set(self, value):
        ...
```

Type relationship clear nahi.

Generic:

```python
class Storage(Generic[T]):
    def set(self, value: T):
        ...
```

Ab relationship clear:

```text
Storage[int]
    ↓
set() expects int
    ↓
get() returns int
```

Aur:

```text
Storage[str]
    ↓
set() expects str
    ↓
get() returns str
```

---

# 4. HVAC example

Suppose temperature sensor:

```python
class TemperatureSensor:
    def read(self) -> float:
        return 22.5
```

Status sensor:

```python
class StatusSensor:
    def read(self) -> str:
        return "ON"
```

Ab generic sensor interface bana sakte hain.

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Sensor(Protocol[T]):

    def read(self) -> T:
        ...
```

Conceptually:

```text
Sensor[float]
→ read() returns float

Sensor[str]
→ read() returns str
```

---

# 5. Generic Protocol

Ye powerful combination hai:

```python
class Sensor(Protocol[T]):

    def read(self) -> T:
        ...
```

Ab:

```python
class TemperatureSensor:

    def read(self) -> float:
        return 22.5
```

aur:

```python
class StatusSensor:

    def read(self) -> str:
        return "ON"
```

Dono same protocol ke different type versions satisfy karte hain.

---

# 6. Generic function

Ab function:

```python
def read_sensor(sensor: Sensor[T]) -> T:
    return sensor.read()
```

Agar:

```python
temperature = read_sensor(TemperatureSensor())
```

to type relationship:

```text
Sensor[float]
     ↓
T = float
     ↓
temperature: float
```

Aur:

```python
status = read_sensor(StatusSensor())
```

to:

```text
Sensor[str]
     ↓
T = str
     ↓
status: str
```

---

# 7. Ye `Any` se better kyun hai?

Agar:

```python
def read_sensor(sensor: Any) -> Any:
    return sensor.read()
```

to type relationship lost ho gayi.

Static type checker ko nahi pata:

```text
input kya hai?
output kya hai?
```

Generic:

```python
def read_sensor(sensor: Sensor[T]) -> T:
```

clearly kehta hai:

> Sensor jis type ka value return karega, function bhi wahi type return karega.

---

# 8. `T` ko "connection" samjho

Ye bohat useful mental model hai:

```text
Sensor[T]
   │
   │ same T
   ▼
read() → T
   │
   ▼
function returns T
```

`T` input aur output ke darmiyan **type connection** bana raha hai.

---

# 9. Ab covariance

Ab question:

> Kya `Sensor[Dog]` ko `Sensor[Animal]` ki jagah use kar sakte hain?

Pehle hierarchy:

```python
class Animal:
    pass

class Dog(Animal):
    pass
```

Relationship:

```text
Dog
 ↓
Animal
```

Dog is an Animal.

---

# 10. Producer concept

Sensor:

```python
class Sensor(Protocol[T]):
    def read(self) -> T:
        ...
```

Sensor value **produce** kar raha hai.

```text
Sensor
   ↓
produces
   ↓
T
```

Producer/output types mein covariance relevant hoti hai.

---

# 11. Covariant TypeVar

```python
T_co = TypeVar("T_co", covariant=True)
```

Then:

```python
class Producer(Protocol[T_co]):

    def get(self) -> T_co:
        ...
```

Relationship:

```text
Dog <: Animal

Producer[Dog] <: Producer[Animal]
```

Conceptually:

> Jo system Dog produce kar sakta hai, wo Animal produce karne wali requirement ko satisfy kar sakta hai.

Kyun?

Because har Dog ek Animal bhi hai.

---

# 12. Simple real-world example

```python
class Animal:
    def speak(self):
        print("Animal sound")


class Dog(Animal):
    def speak(self):
        print("Woof")
```

Producer:

```python
class AnimalProducer(Protocol[T_co]):

    def get(self) -> T_co:
        ...
```

Dog producer:

```python
class DogProducer:

    def get(self) -> Dog:
        return Dog()
```

Dog produce karne wala producer Animal produce karne ki requirement ke liye useful ho sakta hai.

---

# 13. Covariance ka mental shortcut

```text
T_co
 ↓
CO = OUT
 ↓
Producer
 ↓
returns T
```

So:

```text
Covariance
→ output/producer side
```

---

# 14. Contravariance

Ab opposite situation.

Suppose handler:

```python
class Handler(Protocol[T]):
    def handle(self, value: T) -> None:
        ...
```

Yahan T **input** hai.

```text
Handler
   ↓
consumes
   ↓
T
```

Ye consumer hai.

---

# 15. Contravariant TypeVar

```python
T_contra = TypeVar(
    "T_contra",
    contravariant=True
)
```

Then:

```python
class Handler(Protocol[T_contra]):

    def handle(
        self,
        value: T_contra
    ) -> None:
        ...
```

Ab:

```text
CONTRA
   ↓
input
   ↓
consumer
```

---

# 16. Ye direction ulat kyun hoti hai?

Hierarchy:

```text
Animal
  ↑
Dog
```

Suppose:

```text
Handler[Animal]
```

Animal handler:

```python
def handle(animal: Animal):
    ...
```

Ye Dog bhi handle kar sakta hai.

Because:

```text
Dog is an Animal
```

So:

```text
Handler[Animal]
```

Dog handling requirement ke liye use ho sakta hai.

Isliye direction reverse hoti hai.

---

# 17. Simple mental model

```text
COVARIANCE
→ output
→ producer
→ same direction

CONTRAVARIANCE
→ input
→ consumer
→ opposite direction

INVARIANCE
→ input + output
→ read + write
→ no substitution relationship
```

---

# 18. Invariance

Ab:

```python
T = TypeVar("T")
```

default behavior invariant hai.

Suppose:

```python
class Storage(Generic[T]):

    def get(self) -> T:
        ...

    def set(self, value: T):
        ...
```

Yahan T:

```text
output bhi
input bhi
```

So:

```text
read + write
```

Aise generic containers generally invariant hote hain.

---

# 19. `list` invariant kyun hai?

Suppose theoretically:

```text
list[Dog]
```

ko:

```text
list[Animal]
```

maan lete.

Phir:

```python
dogs: list[Dog] = []
```

Aur kisi function ko:

```python
animals: list[Animal]
```

mil gayi.

Wo kar sakta hai:

```python
animals.append(Cat())
```

Ab original `dogs` list mein:

```text
Dog
Dog
Cat   ← problem
```

Aa gaya.

Isliye mutable `list` ko safely covariant nahi bana sakte.

---

# 20. `Sequence` covariant kyun ho sakti hai?

Sequence mostly read-oriented interface hai.

```python
from collections.abc import Sequence
```

Conceptually:

```text
Sequence[Dog]
```

ko:

```text
Sequence[Animal]
```

ke context mein use karna safer hai.

Kyun?

Consumer normally sequence mein arbitrary Animal insert nahi kar raha.

```text
read-only-ish
→ covariance possible
```

---

# 21. `MutableSequence` ka kya?

Mutable:

```text
read
+
write
```

Isliye covariance unsafe ho sakti hai.

Same reason:

```text
list
```

invariance se related hai.

---

# 22. `Mapping` ka interesting case

Mapping:

```text
key → value
```

mein variance more nuanced hoti hai.

For example:

```python
Mapping[str, Animal]
```

value side read-only hoti hai, isliye value covariance relevant ho sakti hai.

Lekin key side input/lookup semantics ki wajah se variance different ho sakti hai.

Beginner level par important point:

> Variance har generic parameter ke **use position** par depend karti hai.

---

# 23. Callable mein variance

Ab:

```python
Callable[[Input], Output]
```

ko dekho.

Example:

```python
Callable[[Animal], Dog]
```

Ismein:

```text
Animal
 ↓
input

Dog
 ↓
output
```

So:

```text
Input
→ contravariant

Output
→ covariant
```

Ye Python typing ka important rule hai.

---

# 24. `Callable[P, R]`

Previous lesson mein:

```python
P = ParamSpec("P")
R = TypeVar("R")
```

Then:

```python
Callable[P, R]
```

means:

```text
P
→ parameters

R
→ return value
```

Decorator:

```python
def logger(
    func: Callable[P, R]
) -> Callable[P, R]:
    ...
```

Meaning:

> Function ke parameters aur return type preserve karo.

---

# 25. Generic Repository

Ab ek real architecture banate hain.

```python
T = TypeVar("T")

class Repository(Protocol[T]):

    def get(self, item_id: str) -> T | None:
        ...

    def save(self, item: T) -> None:
        ...
```

Example model:

```python
class Equipment:
    def __init__(self, equipment_id: str):
        self.equipment_id = equipment_id
```

Repository:

```python
class EquipmentRepository:

    def get(self, item_id: str) -> Equipment | None:
        ...

    def save(self, item: Equipment) -> None:
        ...
```

Conceptually:

```text
Repository[Equipment]
```

---

# 26. Generic repository ka benefit

Same architecture:

```text
Repository[Equipment]
Repository[WorkOrder]
Repository[Employee]
Repository[Sensor]
```

Ek generic concept:

```text
Repository[T]
```

T ko actual model decide karta hai.

---

# 27. Generic Handler

Suppose work order handler:

```python
T = TypeVar("T")

class Handler(Protocol[T]):

    def handle(self, item: T) -> None:
        ...
```

Then:

```python
class WorkOrderHandler:

    def handle(self, item: WorkOrder) -> None:
        ...
```

And:

```python
class EquipmentHandler:

    def handle(self, item: Equipment) -> None:
        ...
```

Same generic interface.

---

# 28. Producer + Consumer architecture

Ab complete picture:

```text
Sensor[T]
   ↓
PRODUCER
   ↓
T

Repository[T]
   ↓
STORAGE
   ↓
T

Handler[T]
   ↓
CONSUMER
   ↓
T
```

Ye generic architecture ka basic pattern hai.

---

# 29. HVAC pipeline

Imagine:

```text
Temperature Sensor
       ↓
   float value
       ↓
Repository
       ↓
Temperature data
       ↓
Handler
       ↓
Alarm / Dashboard
```

Typing:

```text
Sensor[float]
Repository[TemperatureReading]
Handler[TemperatureReading]
```

Har layer ka contract clear.

---

# 30. `Protocol` + `Generic` ka real benefit

Without Protocol:

```python
class EquipmentSensor:
    ...
```

Function concrete implementation par depend karega.

With Protocol:

```python
class Sensor(Protocol[T]):
    def read(self) -> T:
        ...
```

Ab function capability par depend karta hai.

With Generic:

```text
Sensor[float]
Sensor[str]
Sensor[bool]
```

same interface different data types ke liye reusable ho gaya.

---

# 31. `TypeVar` with bound

Previous lesson ka concept:

```python
T = TypeVar("T", bound=Equipment)
```

Meaning:

```text
T
↓
Equipment ya uski subclass
```

Example:

```python
def start_equipment(equipment: T) -> T:
    equipment.start()
    return equipment
```

If:

```python
ahu = AHU()
result = start_equipment(ahu)
```

type relationship preserve hoti hai:

```text
AHU
 ↓
result
AHU
```

---

# 32. Generic + bound

```python
T = TypeVar("T", bound=Equipment)

class Repository(Generic[T]):
    ...
```

Ab:

```text
Repository[AHU]
Repository[VAV]
```

allowed conceptual types hain.

Lekin:

```text
Repository[str]
```

nahi, because:

```text
str
```

Equipment subclass nahi.

---

# 33. Generic + Protocol + bound

Advanced architecture mein TypeVar ko Protocol se bound bhi kiya ja sakta hai.

Example:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...


T = TypeVar("T", bound=Startable)
```

Ab:

```python
def start_and_return(item: T) -> T:
    item.start()
    return item
```

Function ko concrete `AHU` ya `VAV` ki knowledge nahi.

Usko sirf:

```text
start()
```

capability chahiye.

---

# 34. Ye bohat powerful pattern hai

```text
Concrete class
      ↓
required capability
      ↓
Protocol
      ↓
TypeVar bound
      ↓
generic function
```

Example:

```python
class Startable(Protocol):
    def start(self) -> None:
        ...


T = TypeVar("T", bound=Startable)


def start_and_return(item: T) -> T:
    item.start()
    return item
```

Input ka exact subtype output mein preserve hota hai.

---

# 35. `Any` vs `T`

Compare:

```python
def process(value: Any) -> Any:
    return value
```

vs:

```python
T = TypeVar("T")

def process(value: T) -> T:
    return value
```

`Any`:

```text
"Type checking ko zyada concern mat karo."
```

`T`:

```text
"Input aur output ka type relationship preserve karo."
```

Isliye generic code mein `T` often much more informative hota hai.

---

# 36. `object` vs `Any` vs `T`

Ye bhi important:

### `Any`

```python
value: Any
```

Almost kuch bhi allow karta hai aur static checking ko weaken karta hai.

### `object`

```python
value: object
```

Har Python object accept kar sakta hai, lekin operations ke liye narrowing/type knowledge chahiye.

### `T`

```python
value: T
```

Specific type relationship preserve karta hai.

Mental model:

```text
Any
→ "anything, don't check much"

object
→ "anything, but type-safe operations only"

T
→ "some specific type, preserve its identity"
```

---

# 37. Real work-order example

Suppose:

```python
from dataclasses import dataclass

@dataclass
class WorkOrder:
    number: str
    description: str
```

Generic repository:

```python
T = TypeVar("T")

class Repository(Protocol[T]):

    def save(self, item: T) -> None:
        ...

    def get(self, item_id: str) -> T | None:
        ...
```

Then implementation:

```python
class WorkOrderRepository:

    def save(self, item: WorkOrder) -> None:
        print("Saving:", item.number)

    def get(self, item_id: str) -> WorkOrder | None:
        return None
```

Conceptually:

```text
Repository[WorkOrder]
```

---

# 38. Equipment version

```python
@dataclass
class Equipment:
    equipment_id: str
```

Repository:

```python
class EquipmentRepository:

    def save(self, item: Equipment) -> None:
        print("Saving:", item.equipment_id)

    def get(self, item_id: str) -> Equipment | None:
        return None
```

Same architecture:

```text
Repository[T]

T = WorkOrder
T = Equipment
T = Employee
T = SensorReading
```

---

# 39. Full architecture picture

```text
                    Generic Architecture

                         T
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Sensor[T]      Repository[T]    Handler[T]
          │              │              │
       produces        stores         consumes
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                    Actual Type
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           float       WorkOrder   Equipment
```

---

# 40. Variance ka final visual

```text
COVARIANCE

Producer[T]
    ↑
 output
    ↑
T_co

Dog → Animal
Producer[Dog] → Producer[Animal]


CONTRAVARIANCE

Consumer[T]
    ↓
 input
    ↓
T_contra

Dog → Animal
Consumer[Animal] → Consumer[Dog]


INVARIANCE

Storage[T]
    ↕
 input + output

Storage[Dog] ≠ Storage[Animal]
```

Direction ko carefully yaad rakho.

---

# 41. Ek important correction

Variance **actual runtime conversion** nahi hai.

Ye mainly **static type compatibility relationship** hai.

Python runtime:

```python
list[Dog]
```

ko magically kisi different runtime object mein convert nahi karta.

Variance ka discussion mostly:

```text
type checker
type compatibility
generic substitution
```

ke context mein hota hai.

---

# 42. Kab variance manually specify karni hai?

```python
T = TypeVar("T")
```

normally enough hai.

Agar tum generic abstraction design kar rahe ho aur clearly:

```text
producer only
```

hai:

```python
T_co = TypeVar("T_co", covariant=True)
```

Agar:

```text
consumer only
```

hai:

```python
T_contra = TypeVar(
    "T_contra",
    contravariant=True
)
```

Mixed input/output:

```python
T = TypeVar("T")
```

invariant.

---

# 43. Common mistake

Ye mat sochna:

```text
covariant = better
contravariant = better
invariant = bad
```

Aisa nahi.

Variance **design requirement** hai.

```text
Producer
→ covariance

Consumer
→ contravariance

Read + Write
→ invariance
```

---

# 44. Golden rules

```text
TypeVar
→ generic placeholder

Generic[T]
→ class/function ko type-parameterized banana

Protocol[T]
→ structural generic interface

T_co
→ covariant / output

T_contra
→ contravariant / input

T
→ usually invariant

Callable[P, R]
→ P = parameters
→ R = return

bound=Base
→ T must be Base/subclass

Any
→ type checking ko weaken karta hai

object
→ universal base type

T
→ specific type relationship preserve karta hai
```

---

## Next Lesson 59

Ab hum **Python typing ke `TypeGuard` / type narrowing** par jayenge.

Ismein ye samjhenge:

```python
isinstance()
issubclass()
TypeGuard
TypeIs
Union
Optional
```

aur especially ye question:

> Agar Python ko runtime par sirf `object` ya `Union[...]` pata ho, to static type checker ko kaise batate hain ke **"is point ke baad ye value actually `AHU` hai"**?

# Lesson 59: `TypeGuard` + `TypeIs` + Type Narrowing

Ab hum ek important problem solve karte hain:

> Python mein runtime par hum check karte hain ke object kis type ka hai, lekin **static type checker ko kaise samjhayein ke check ke baad value ka exact type kya hai?**

Is concept ko **type narrowing** kehte hain.

---

# 1. Type narrowing kya hai?

Suppose:

```python
def process(value: int | str):
    ...
```

Yahan `value` ke do possible types hain:

```text
value
├── int
└── str
```

Agar hum:

```python
if isinstance(value, int):
    print(value + 10)
```

likhen, to `if` ke andar Python/type checker samajh sakta hai:

```text
value → int
```

Ye **type narrowing** hai.

---

# 2. `Union` type

Modern Python mein:

```python
int | str
```

ka matlab:

```text
int OR str
```

Example:

```python
def show(value: int | str):
    print(value)
```

Call:

```python
show(10)
show("AHU")
```

dono valid hain.

---

# 3. Problem kahan aati hai?

Suppose:

```python
def process(value: int | str):

    if isinstance(value, int):
        print(value + 10)
```

`isinstance()` runtime check karta hai.

Type checker bhi generally samajhta hai:

```text
if branch:
    value = int
```

Aur:

```python
else:
```

mein:

```text
value = str
```

So:

```python
def process(value: int | str):

    if isinstance(value, int):
        print(value + 10)
    else:
        print(value.upper())
```

Yahan narrowing automatically ho rahi hai.

---

# 4. `isinstance()` ka role

Basic pattern:

```python
if isinstance(value, SomeType):
```

Example:

```python
value: object = "AHU"

if isinstance(value, str):
    print(value.upper())
```

Initially:

```text
value: object
```

check ke baad:

```text
value: str
```

---

# 5. `object` se narrowing

Suppose:

```python
def process(value: object):

    if isinstance(value, str):
        print(value.upper())

    elif isinstance(value, int):
        print(value + 10)
```

Initially:

```text
object
```

First branch:

```text
str
```

Second branch:

```text
int
```

Ye type narrowing ka simple example hai.

---

# 6. Lekin custom function ho to?

Suppose tum helper function banate ho:

```python
def is_string(value: object) -> bool:
    return isinstance(value, str)
```

Ab:

```python
value: object

if is_string(value):
    value.upper()
```

Runtime par ye correct hai.

Lekin static type checker ko necessarily ye automatically pata nahi hota ke:

```text
is_string(value) == True
```

means:

```text
value is str
```

Yahan **TypeGuard** ka role aata hai.

---

# 7. `TypeGuard`

Python typing mein:

```python
from typing import TypeGuard
```

Example:

```python
def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

Ab:

```python
value: object

if is_string(value):
    print(value.upper())
```

Type checker samajhta hai:

```text
is_string(value) == True
        ↓
value is str
```

---

# 8. `TypeGuard[T]` ka meaning

```python
TypeGuard[str]
```

ka simple meaning:

> Agar function `True` return kare, to type checker value ko `str` treat kar sakta hai.

Example:

```python
def is_int(value: object) -> TypeGuard[int]:
    return isinstance(value, int)
```

Then:

```python
value: object

if is_int(value):
    print(value + 10)
```

Inside branch:

```text
value → int
```

---

# 9. TypeGuard function ka structure

General pattern:

```python
def is_something(
    value: SomeBroadType
) -> TypeGuard[SpecificType]:
    ...
```

Example:

```python
def is_ahu(value: object) -> TypeGuard[AHU]:
    return isinstance(value, AHU)
```

Then:

```python
equipment: object = AHU()

if is_ahu(equipment):
    equipment.start()
```

Type checker ke liye:

```text
equipment
object
 ↓
is_ahu() == True
 ↓
AHU
```

---

# 10. HVAC example

```python
class Equipment:
    pass


class AHU(Equipment):

    def start(self):
        print("AHU started")


class VAV(Equipment):

    def adjust_damper(self):
        print("Damper adjusted")
```

Ab:

```python
from typing import TypeGuard

def is_ahu(
    equipment: Equipment
) -> TypeGuard[AHU]:

    return isinstance(equipment, AHU)
```

Then:

```python
equipment: Equipment = AHU()

if is_ahu(equipment):
    equipment.start()
```

Narrowing:

```text
Equipment
    ↓
is_ahu()
    ↓
AHU
```

---

# 11. TypeGuard sirf bool nahi hai

Return annotation:

```python
-> TypeGuard[AHU]
```

runtime mein actual returned value still:

```python
True
```

ya:

```python
False
```

hoti hai.

`TypeGuard` runtime object nahi hai jo magic karta hai.

Ye mainly **static type checker ko information deta hai**.

---

# 12. Important: TypeGuard runtime validation nahi karta

Ye:

```python
def is_ahu(
    equipment: Equipment
) -> TypeGuard[AHU]:
    return isinstance(equipment, AHU)
```

safe hai because actual runtime check hai.

Lekin agar tum likho:

```python
def is_ahu(
    equipment: Equipment
) -> TypeGuard[AHU]:
    return True
```

to type checker assume kar sakta hai:

```text
True
↓
AHU
```

lekin runtime par object AHU hona guaranteed nahi.

So:

> `TypeGuard` khud validation nahi karta. Function implementation ki responsibility hai ke returned condition actually correct ho.

---

# 13. TypeGuard ka main purpose

TypeGuard especially useful hai jab normal `isinstance()` enough nahi.

Example custom condition:

```python
def is_valid_work_order(
    data: dict
) -> TypeGuard[dict[str, str]]:
    ...
```

Function complex validation kar sakta hai.

Agar:

```python
if is_valid_work_order(data):
```

to static type checker ko specific type information mil sakti hai.

---

# 14. `TypeGuard` aur generic types

TypeGuard generic structures ke saath bhi useful hai.

Suppose:

```python
from typing import TypeGuard

def is_str_list(
    value: list[object]
) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in value)
```

Then:

```python
items: list[object] = ["AHU", "VAV"]

if is_str_list(items):
    for item in items:
        print(item.upper())
```

Type narrowing:

```text
list[object]
     ↓
TypeGuard
     ↓
list[str]
```

---

# 15. Ye important kyun hai?

Python mein generic containers ki variance restrictions hain.

Yaad karo:

```text
list[Dog]
≠
list[Animal]
```

generally.

So agar tumhare paas:

```python
list[object]
```

hai aur tum runtime par verify karte ho ke **har element string hai**, TypeGuard static checker ko batata hai:

```text
list[object]
      ↓
verified
      ↓
list[str]
```

---

# 16. TypeGuard vs `isinstance()`

### Direct `isinstance`

```python
if isinstance(value, AHU):
    value.start()
```

Python/type checker naturally samajh sakta hai.

### Custom condition

```python
if is_ahu(value):
    value.start()
```

Type checker ko explicit information dene ke liye:

```python
def is_ahu(value) -> TypeGuard[AHU]:
```

useful hai.

---

# 17. `TypeIs`

Ab modern typing ka related concept:

```python
from typing import TypeIs
```

Python 3.13 mein `TypeIs` introduce hua.

Basic:

```python
def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

Ye bhi type narrowing ke liye hai.

Lekin `TypeGuard` aur `TypeIs` exactly same nahi hain.

---

# 18. `TypeGuard` vs `TypeIs`

Basic difference:

```text
TypeGuard[T]
→ True branch ko T ke taur par narrow karta hai.

TypeIs[T]
→ True branch mein T
→ False branch mein bhi complementary narrowing provide kar sakta hai.
```

Ye difference important hai.

---

# 19. Example with `TypeIs`

Suppose:

```python
def is_str(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

Then:

```python
value: str | int
```

and:

```python
if is_str(value):
    ...
else:
    ...
```

Conceptually:

```text
if:
    str

else:
    int
```

TypeIs negative branch mein bhi narrowing information de sakta hai.

---

# 20. TypeGuard mein false branch

TypeGuard ka important difference:

```python
def is_str(value: object) -> TypeGuard[str]:
    ...
```

True branch:

```text
value → str
```

Lekin false branch ke liye type checker ko generally ye assume nahi karna chahiye:

```text
value → definitely not str
```

kyunki TypeGuard ki semantics arbitrary type predicates ko support karti hain.

---

# 21. TypeIs more restrictive hai

`TypeIs[T]` predicate ko logically compatible hona chahiye.

Simple example:

```python
def is_str(value: str | int) -> TypeIs[str]:
    return isinstance(value, str)
```

Then:

```text
True
→ str

False
→ int
```

Yahan negative narrowing meaningful hai.

---

# 22. Mental model

```text
TypeGuard
   ↓
"agar True hai,
 value ko T samjho"

TypeIs
   ↓
"agar True hai,
 value T hai

agar False hai,
 value T nahi hai"
```

---

# 23. `TypeGuard` ka generic example

Suppose:

```python
from typing import TypeGuard, TypeVar

T = TypeVar("T")
```

Specific predicates complex generic code mein useful ho sakte hain.

Lekin beginner level par sabse important pattern:

```python
def is_x(value: BroadType) -> TypeGuard[SpecificType]:
    ...
```

hai.

---

# 24. `Optional` ke saath narrowing

Suppose:

```python
temperature: float | None = None
```

Agar:

```python
if temperature is not None:
    print(temperature + 1)
```

to narrowing:

```text
float | None
      ↓
float
```

Ye TypeGuard ki zaroorat ke baghair built-in narrowing hai.

---

# 25. `Union` ke saath narrowing

Example:

```python
def process(value: int | str):

    if isinstance(value, int):
        print(value + 1)
    else:
        print(value.upper())
```

Narrowing:

```text
int | str
   │
   ├── isinstance(int) → int
   │
   └── else → str
```

---

# 26. `Literal` ke saath narrowing

Suppose:

```python
from typing import Literal

Mode = Literal["auto", "manual"]
```

Then:

```python
def set_mode(mode: Mode):
    if mode == "auto":
        ...
    else:
        ...
```

Static analyzer exact literal values ko reason kar sakta hai.

---

# 27. `Enum` ke saath narrowing

```python
from enum import Enum

class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

Then:

```python
def configure(mode: Mode):

    if mode is Mode.AUTO:
        print("Automatic")
    else:
        print("Manual")
```

Yahan condition ke basis par type/value reasoning ho sakti hai.

---

# 28. `issubclass()` aur narrowing

`issubclass()` classes ke liye hai.

Example:

```python
class Equipment:
    pass

class AHU(Equipment):
    pass

class VAV(Equipment):
    pass
```

Function:

```python
def inspect_class(cls: type[Equipment]):

    if issubclass(cls, AHU):
        print("This is an AHU class")
```

Yahan:

```text
cls
↓
class object
```

yaad rakho.

`isinstance()`:

```text
object check
```

`issubclass()`:

```text
class check
```

---

# 29. `type[...]`

Ye bhi important syntax hai:

```python
type[Equipment]
```

ka matlab:

> Equipment ka **class object**.

Ye:

```python
Equipment()
```

nahi hai.

Difference:

```text
Equipment()
→ instance

Equipment
→ class object

type[Equipment]
→ Equipment-type class object
```

---

# 30. Example

```python
def create_equipment(
    cls: type[Equipment]
) -> Equipment:

    return cls()
```

Call:

```python
ahu = create_equipment(AHU)
```

Yahan function ko:

```text
AHU
```

class object mila.

Function ke andar:

```python
cls()
```

se instance create hua.

---

# 31. `isinstance` + `issubclass` mental model

```text
isinstance()
↓
"Ye object kis class ka instance hai?"

issubclass()
↓
"Ye class kis class ki subclass hai?"
```

Example:

```python
ahu = AHU()

isinstance(ahu, Equipment)
```

vs:

```python
issubclass(AHU, Equipment)
```

---

# 32. Type narrowing ka complete flow

```text
Broad type
    ↓
runtime condition
    ↓
type checker
    ↓
narrower type
```

Example:

```text
object
  ↓
isinstance(value, AHU)
  ↓
AHU
```

Custom:

```text
Equipment
  ↓
is_ahu(equipment)
  ↓
TypeGuard[AHU]
  ↓
AHU
```

---

# 33. Work-order practical example

Suppose raw Google Sheets data:

```python
row: object
```

Tum verify karna chahte ho:

```text
work_order_number
code
description
area
floor
comment
```

sab strings hain.

Custom type:

```python
from typing import TypedDict, TypeGuard

class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: str
```

Validation function:

```python
def is_work_order(
    data: dict
) -> TypeGuard[WorkOrder]:

    required = [
        "work_order_number",
        "code",
        "description",
        "area",
        "floor",
        "comment",
    ]

    return all(
        key in data and isinstance(data[key], str)
        for key in required
    )
```

Then:

```python
if is_work_order(row):
    print(row["work_order_number"])
```

Conceptually:

```text
dict
 ↓
validation
 ↓
WorkOrder
```

---

# 34. Lekin ek important warning

`TypeGuard` likhne se runtime data automatically safe nahi ho jata.

Agar validator incomplete hai:

```python
def is_work_order(data) -> TypeGuard[WorkOrder]:
    return True
```

to static type checker ko wrong information mil sakti hai.

Therefore:

> TypeGuard function ki implementation ko actual predicate correctly establish karna chahiye.

---

# 35. TypeGuard + Protocol

Ye bhi combine ho sakte hain.

```python
from typing import Protocol, TypeGuard

class Startable(Protocol):

    def start(self) -> None:
        ...
```

Predicate:

```python
def is_startable(
    value: object
) -> TypeGuard[Startable]:

    return callable(getattr(value, "start", None))
```

Then:

```python
equipment: object = AHU()

if is_startable(equipment):
    equipment.start()
```

Conceptually:

```text
object
 ↓
has start()
 ↓
Startable Protocol
```

---

# 36. Lekin runtime Protocol checking ka difference

Agar:

```python
@runtime_checkable
class Startable(Protocol):
    def start(self) -> None:
        ...
```

to:

```python
isinstance(obj, Startable)
```

possible hai.

Lekin runtime structural checking static typing jitni detailed nahi hoti.

So:

```text
Static type checker
→ detailed type analysis

Runtime isinstance
→ actual runtime check
```

dono separate concerns hain.

---

# 37. `TypeIs` kab useful hai?

Jab predicate genuinely partition karta ho:

```text
A | B
```

into:

```text
True  → A
False → B
```

Example:

```python
def is_string(
    value: str | int
) -> TypeIs[str]:
    return isinstance(value, str)
```

Then:

```python
def process(value: str | int):

    if is_string(value):
        value.upper()
    else:
        value + 10
```

Conceptually:

```text
before:
str | int

True:
str

False:
int
```

---

# 38. `TypeGuard` kab useful hai?

Jab predicate kisi broad type ko **specific type** mein establish karta hai, especially complex/custom validation.

Examples:

```text
dict
→ validated TypedDict

list[object]
→ list[str]

Equipment
→ AHU

object
→ custom Protocol-compatible type
```

---

# 39. Type narrowing hierarchy

```text
                  Type Narrowing
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
     isinstance    issubclass    custom predicate
          │            │            │
          │            │       ┌────┴────┐
          │            │       ▼         ▼
          │            │  TypeGuard    TypeIs
          │            │
          └────────────┴───────────────┘
                       ↓
                narrower type
```

---

# 40. Golden rules

```text
Union
→ multiple possible types

isinstance()
→ runtime instance check + normal narrowing

issubclass()
→ class inheritance check

TypeGuard[T]
→ True branch ko T ke taur par narrow karne ki
  static typing information

TypeIs[T]
→ True branch T
→ False branch mein T ko exclude karne ki
  narrowing information

object
→ broad universal object type

type[Equipment]
→ Equipment ka class object

Optional[T]
→ T | None
```

---

# 41. Sabse important example

Isko carefully dekho:

```python
from typing import TypeGuard

class Equipment:
    pass


class AHU(Equipment):

    def start(self):
        print("AHU started")


def is_ahu(
    equipment: Equipment
) -> TypeGuard[AHU]:

    return isinstance(equipment, AHU)


equipment: Equipment = AHU()

if is_ahu(equipment):
    equipment.start()
```

Flow:

```text
equipment
   │
   ▼
Equipment
   │
   │ is_ahu()
   ▼
TypeGuard[AHU]
   │
   ▼
AHU
   │
   ▼
start()
```

Yahi **type narrowing** ka core concept hai.

---

## Next Lesson 60

Ab hum **Python `match` / `case` pattern matching + type narrowing** dekhenge.

Ismein hum cover karenge:

```text
match / case
case _
case int()
case str()
case Class(...)
case [a, b]
case {"key": value}
guards: if ...
```

Aur dekhenge ke Python pattern matching sirf `if/elif` ka replacement nahi, balki **structural pattern matching** hai.

# Lesson 60: Python `match` / `case` — Structural Pattern Matching

Ab hum Python ke **structural pattern matching** ko detail mein samjhenge.

Ye sirf:

```python
if / elif / else
```

ka replacement nahi hai.

`match` object ki **shape, type, values, sequence, mapping aur class structure** ke basis par pattern match kar sakta hai.

---

# 1. Basic `match`

Example:

```python
status = "ON"

match status:
    case "ON":
        print("Equipment running")

    case "OFF":
        print("Equipment stopped")

    case _:
        print("Unknown status")
```

Output:

```text
Equipment running
```

---

# 2. `case _` kya hai?

```python
case _:
```

`_` yahan:

> koi bhi remaining value

ko match karta hai.

Ye roughly `else` jaisa fallback hai.

```text
match
 ├── case "ON"
 ├── case "OFF"
 └── case _
```

---

# 3. `match` ka basic flow

```text
value
  ↓
match
  ↓
case 1
  ↓ no match
case 2
  ↓ no match
case 3
  ↓
matched case
```

**First matching case** execute hota hai.

---

# 4. Multiple values ek case mein

Suppose:

```python
day = "Saturday"
```

Tum likh sakte ho:

```python
match day:
    case "Saturday" | "Sunday":
        print("Weekend")

    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("Working day")
```

`|` ka matlab:

> OR pattern

---

# 5. Important: `|` aur `or` same nahi

Pattern matching mein:

```python
case "ON" | "AUTO":
```

likhte hain.

Normal boolean condition mein:

```python
if mode == "ON" or mode == "AUTO":
```

So:

```text
case pattern | pattern
```

pattern alternatives hain.

---

# 6. Variable capture

Ye important hai:

```python
value = 10

match value:
    case x:
        print(x)
```

`x` **capture pattern** hai.

Ye almost har value ko match karega aur value ko `x` mein store karega.

So:

```text
value = 10
↓
case x
↓
x = 10
```

Isliye:

```python
case x:
```

ko blindly `case variable` mat samajhna.

---

# 7. `_` aur variable mein difference

```python
case _:
```

value ko ignore karta hai.

```python
case x:
```

value ko capture karta hai.

Example:

```python
match 100:
    case _:
        print("ignored")
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

# 8. Literal patterns

Simple values:

```python
match value:
    case 10:
        print("Ten")

    case "AHU":
        print("AHU")

    case True:
        print("True")
```

Literal exact value ko match karte hain.

---

# 9. Type patterns

Ab interesting part:

```python
value = 100

match value:
    case int():
        print("Integer")

    case str():
        print("String")
```

Output:

```text
Integer
```

Yahan:

```python
case int():
```

ka matlab:

> value `int` ka instance hai.

---

# 10. `int()` pattern

Suppose:

```python
value = 42
```

Then:

```python
match value:
    case int():
        print("integer")
```

match karega.

Similarly:

```python
case str():
```

string.

```python
case list():
```

list.

```python
case dict():
```

dictionary.

---

# 11. Type + capture

Tum type check aur value capture dono kar sakte ho:

```python
value = 42

match value:
    case int(x):
        print(x)
```

Conceptually:

```text
value
 ↓
is int?
 ↓ yes
x = value
```

---

# 12. HVAC example

```python
equipment = AHU()
```

Suppose:

```python
class Equipment:
    pass


class AHU(Equipment):
    pass


class VAV(Equipment):
    pass
```

Then:

```python
match equipment:
    case AHU():
        print("AHU")

    case VAV():
        print("VAV")

    case Equipment():
        print("Other equipment")
```

Output:

```text
AHU
```

---

# 13. Case order matters

Ye:

```python
match equipment:
    case Equipment():
        print("Equipment")

    case AHU():
        print("AHU")
```

problem create karega logically, kyunki `AHU` bhi `Equipment` hai.

First case:

```python
case Equipment():
```

AHU ko bhi match kar sakta hai.

So more specific patterns pehle:

```text
AHU
VAV
Equipment
_
```

---

# 14. Sequence patterns

List:

```python
data = [10, 20]
```

Match:

```python
match data:
    case [10, 20]:
        print("Exact list")
```

---

# 15. Capture sequence values

```python
data = [10, 20]

match data:
    case [a, b]:
        print(a)
        print(b)
```

Output:

```text
10
20
```

Pattern:

```text
[a, b]
```

means:

> two-element sequence, first value `a`, second `b`.

---

# 16. Three elements

```python
data = [10, 20, 30]

match data:
    case [a, b, c]:
        print(a, b, c)
```

Output:

```text
10 20 30
```

---

# 17. `*rest`

Variable-length sequence:

```python
data = [10, 20, 30, 40]
```

```python
match data:
    case [first, *rest]:
        print(first)
        print(rest)
```

Output:

```text
10
[20, 30, 40]
```

So:

```text
[first, *rest]
```

means:

```text
first → first element
rest  → remaining elements
```

---

# 18. Exact vs flexible sequence

```python
case [a, b]:
```

requires two elements.

```python
case [a, *rest]:
```

allows variable number of remaining elements.

Example:

```python
[10, 20, 30, 40]
```

matches:

```python
[a, *rest]
```

but not:

```python
[a, b]
```

---

# 19. Nested sequence pattern

```python
data = [10, [20, 30]]
```

You can:

```python
match data:
    case [a, [b, c]]:
        print(a, b, c)
```

Output:

```text
10 20 30
```

Ye structural matching hai.

Object ki **shape** match ho rahi hai.

---

# 20. Mapping patterns

Dictionary:

```python
equipment = {
    "type": "AHU",
    "status": "ON"
}
```

Pattern:

```python
match equipment:
    case {"type": "AHU", "status": "ON"}:
        print("Running AHU")
```

---

# 21. Dictionary values capture karna

```python
equipment = {
    "type": "AHU",
    "status": "ON"
}
```

```python
match equipment:
    case {"type": equipment_type, "status": status}:
        print(equipment_type)
        print(status)
```

Output:

```text
AHU
ON
```

---

# 22. Mapping pattern mein extra keys

Ye important hai.

Suppose:

```python
equipment = {
    "type": "AHU",
    "status": "ON",
    "temperature": 22.5
}
```

Pattern:

```python
case {"type": "AHU"}:
```

phir bhi match kar sakta hai.

Kyun?

Mapping pattern normally specified keys ko check karta hai; dictionary mein additional keys hona automatically failure nahi banata.

---

# 23. `**rest` mapping

Tum remaining mapping data capture kar sakte ho:

```python
match equipment:
    case {"type": "AHU", **rest}:
        print(rest)
```

Possible:

```text
{
    "status": "ON",
    "temperature": 22.5
}
```

---

# 24. Class patterns

Ab custom class:

```python
class Equipment:

    def __init__(self, equipment_id, status):
        self.equipment_id = equipment_id
        self.status = status
```

Object:

```python
ahu = Equipment("AHU-01", "ON")
```

Pattern matching:

```python
match ahu:
    case Equipment("AHU-01", "ON"):
        print("Running AHU-01")
```

Yahan class structure/attributes ke basis par matching ho rahi hai.

---

# 25. `__match_args__`

Positional class pattern:

```python
case Equipment("AHU-01", "ON"):
```

class ke `__match_args__` se related hai.

Dataclass automatically useful `__match_args__` provide kar sakti hai in normal configurations.

Example:

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    status: str
```

Then:

```python
equipment = Equipment("AHU-01", "ON")

match equipment:
    case Equipment("AHU-01", "ON"):
        print("Match")
```

---

# 26. Keyword class pattern

Positional matching ke bajaye:

```python
match equipment:
    case Equipment(
        equipment_id="AHU-01",
        status="ON"
    ):
        print("Match")
```

Ye often clearer hota hai.

---

# 27. Dataclass + pattern matching

Ye practical combination hai.

```python
from dataclasses import dataclass

@dataclass
class WorkOrder:
    number: str
    status: str
    floor: str
```

Then:

```python
wo = WorkOrder(
    "WO-1001",
    "OPEN",
    "34"
)
```

Pattern:

```python
match wo:
    case WorkOrder(
        number="WO-1001",
        status="OPEN"
    ):
        print("Open work order")
```

---

# 28. Guards — `if`

Pattern match ke saath condition:

```python
temperature = 28

match temperature:
    case int() as temp if temp > 25:
        print("High temperature")

    case int() as temp:
        print("Normal temperature")
```

Yahan:

```python
if temp > 25
```

**guard** hai.

---

# 29. Guard ka flow

```text
value
 ↓
pattern match?
 ↓ yes
capture variables
 ↓
guard condition
 ↓
True?
 ↓
case execute
```

Agar pattern match ho gaya lekin guard false:

```text
next case
```

try hota hai.

---

# 30. `as` pattern

Example:

```python
match value:
    case int() as number:
        print(number)
```

Yahan:

```text
int()
 ↓
type match
 ↓
as number
 ↓
number mein original value
```

---

# 31. Type + condition

HVAC example:

```python
temperature = 28.5

match temperature:
    case float() as temp if temp >= 30:
        print("Critical")

    case float() as temp if temp >= 25:
        print("High")

    case float() as temp:
        print("Normal")
```

Output:

```text
High
```

---

# 32. OR pattern + capture

Suppose:

```python
mode = "AUTO"
```

You can:

```python
match mode:
    case "AUTO" | "MANUAL":
        print("Control mode")
```

Lekin OR patterns mein captured variables consistent hone chahiye.

Conceptually Python ko ensure karna hota hai ke successful alternatives same bindings provide karein.

---

# 33. Nested pattern

Real work-order data:

```python
row = {
    "equipment": {
        "type": "AHU",
        "status": "ON"
    },
    "floor": 34
}
```

Match:

```python
match row:
    case {
        "equipment": {
            "type": "AHU",
            "status": "ON"
        },
        "floor": floor
    }:
        print("AHU running on floor", floor)
```

Output:

```text
AHU running on floor 34
```

Ye `if` ke multiple nested checks se kaafi expressive ho sakta hai.

---

# 34. Work-order example

```python
row = {
    "work_order": "WO-1001",
    "status": "OPEN",
    "priority": "HIGH"
}
```

Pattern:

```python
match row:
    case {
        "work_order": wo,
        "status": "OPEN",
        "priority": "HIGH"
    }:
        print("High priority:", wo)

    case {
        "work_order": wo,
        "status": "OPEN"
    }:
        print("Open:", wo)

    case _:
        print("Other")
```

---

# 35. Pattern order again

Specific:

```text
HIGH + OPEN
```

pehle.

General:

```text
OPEN
```

baad mein.

Fallback:

```text
_
```

last.

Mental rule:

> **Specific → general → fallback**

---

# 36. `match` vs `if/elif`

Simple value comparison:

```python
if status == "ON":
    ...
elif status == "OFF":
    ...
```

`match`:

```python
match status:
    case "ON":
        ...
    case "OFF":
        ...
```

Simple cases mein dono readable ho sakte hain.

Lekin nested structures mein:

```python
match row:
    case {
        "equipment": {
            "type": "AHU",
            "status": "ON"
        }
    }:
        ...
```

`match` zyada expressive ho sakta hai.

---

# 37. Pattern matching ka real power

`match` simultaneously check kar sakta hai:

```text
type
value
sequence structure
mapping structure
class structure
nested structure
conditions
```

Example:

```python
match data:
    case {"type": "AHU", "temperature": temp} if temp > 25:
        print("High AHU temperature")
```

Ek hi pattern mein:

```text
dict?
 ↓
type == AHU?
 ↓
temperature available?
 ↓
temperature > 25?
```

---

# 38. `match` aur `Protocol`

Important distinction:

`Protocol`:

```text
"What operations/capabilities does this object provide?"
```

`match`:

```text
"What structure/value does this object have?"
```

So:

```text
Protocol
→ interface/capability

match
→ structural pattern/value matching
```

---

# 39. `match` aur `TypeGuard`

Ye bhi related hain but different.

`TypeGuard`:

```python
if is_ahu(equipment):
    ...
```

custom predicate se type narrowing.

`match`:

```python
match equipment:
    case AHU():
        ...
```

pattern ke through matching/narrowing.

---

# 40. `match` + `TypeGuard` architecture

Tum helper predicate bhi use kar sakte ho:

```python
match equipment:
    case AHU():
        print("AHU")

    case VAV():
        print("VAV")

    case _:
        print("Unknown")
```

Aur complex validation ke liye:

```python
if is_valid_work_order(row):
    ...
```

Dono ka purpose same nahi.

---

# 41. `match` mein wildcard `_`

Last fallback:

```python
case _:
    print("Unknown")
```

Ye generally default case hai.

Agar koi case match nahi karta aur `_` nahi hai:

```text
kuch execute nahi hota
```

`match` khud exception nahi throw karta sirf is wajah se ke no case matched.

---

# 42. Match statement vs switch

Many languages mein `switch` hota hai.

Python ka:

```python
match
```

naam switch jaisa lagta hai, lekin functionality broader hai.

Traditional switch:

```text
value
↓
case value
```

Python pattern matching:

```text
value
↓
pattern
↓
structure
↓
bindings
↓
guard
```

---

# 43. Ek complete HVAC example

```python
from dataclasses import dataclass


@dataclass
class Equipment:
    equipment_id: str
    status: str
    temperature: float


equipment = Equipment(
    "AHU-01",
    "ON",
    27.5
)


match equipment:

    case Equipment(
        equipment_id="AHU-01",
        status="ON",
        temperature=temp
    ) if temp >= 25:
        print("AHU-01 running with high temperature")

    case Equipment(
        equipment_id="AHU-01",
        status="ON",
        temperature=temp
    ):
        print("AHU-01 normal")

    case Equipment(status="OFF"):
        print("Equipment OFF")

    case _:
        print("Unknown equipment")
```

Given:

```text
temperature = 27.5
```

first case match karega.

---

# 44. Is example ka flow

```text
Equipment object
       ↓
case Equipment(...)
       ↓
ID == AHU-01?
       ↓
status == ON?
       ↓
temperature capture → temp
       ↓
temp >= 25?
       ↓
YES
       ↓
High temperature
```

---

# 45. Work-order data ke liye powerful

Tumhare work-order script mein row roughly:

```text
Work Order Number
Code
Description
Area
Floor
Comment
```

ho sakti hai.

Agar tum dictionary bana lo:

```python
row = {
    "work_order": "WO-1001",
    "code": "HVAC",
    "floor": "34",
    "status": "OPEN"
}
```

to:

```python
match row:
    case {
        "work_order": wo,
        "code": "HVAC",
        "status": "OPEN"
    }:
        print("HVAC WO:", wo)

    case {
        "work_order": wo,
        "status": "CLOSED"
    }:
        print("Closed:", wo)

    case _:
        print("Other")
```

Ye tumhare work-order processing architecture mein useful ho sakta hai.

---

# 46. `match` ko kab use karein?

Use it when:

* multiple structured cases hain
* nested dictionaries/lists hain
* different classes ke according behavior change hota hai
* patterns readable ban rahe hain
* parsing/dispatch logic hai
* AST/data structures process karne hain

Simple condition:

```python
if temperature > 25:
```

ke liye `match` zaroori nahi.

---

# 47. `match` ko kab avoid karein?

Agar:

```python
if x > 10 and y < 20:
```

jaisi simple boolean logic hai, normal `if` often clearer hai.

Similarly:

```python
if user.is_admin:
```

ke liye `match` unnecessarily complex ho sakta hai.

Rule:

> Pattern structure complex ho to `match`; simple boolean condition ho to `if`.

---

# 48. Important mental model

```text
if
→ condition-based logic

match
→ pattern-based logic
```

More detailed:

```text
if:
    "Kya condition True hai?"

match:
    "Object/value ki structure kis pattern se match karti hai?"
```

---

# 49. Golden rules

```text
match value:
    case pattern:
        ...

case _:
    → fallback

case A | B:
    → OR pattern

case [a, b]:
    → sequence structure

case [first, *rest]:
    → variable-length sequence

case {"key": value}:
    → mapping pattern

case Class(...):
    → class pattern

case ... if condition:
    → guard

case Type() as value:
    → type pattern + capture
```

---

# 50. Final picture

```text
                     match
                       │
         ┌─────────────┼──────────────┐
         │             │              │
         ▼             ▼              ▼
      Literal       Sequence       Mapping
         │             │              │
         ▼             ▼              ▼
      "ON"          [a, b]       {"status": x}
                       
                       │
                       ▼
                     Class
                       │
                       ▼
                  Equipment(...)
                       │
                       ▼
                    Guard
                       │
                    if temp > 25
```

Aur typing ke perspective se:

```text
isinstance()
     ↓
normal narrowing

TypeGuard
     ↓
custom predicate narrowing

TypeIs
     ↓
positive + negative narrowing

match/case
     ↓
pattern-based structural narrowing
```

---

## Next Lesson 61

Ab hum Python ke **`dataclass` ko advanced level par** dekhenge:

```text
@dataclass
field()
default_factory
__post_init__
frozen
slots
kw_only
ClassVar
InitVar
inheritance
__match_args__
```

Aur especially ye samjhenge ke `dataclass` internally **normal class + generated methods + descriptors/fields + object initialization** ko kaise combine karta hai.
