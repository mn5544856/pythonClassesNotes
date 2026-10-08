# Python OOP — Lessons 51-60 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 51: Python `logging`

## 1. `print()` vs `logging`

```python
# Beginner
print("Work order created")

# Production
import logging
logging.info("Work order created")
```

**Explanation:**
- `print()` → sirf message
- `logging` → message + severity + timestamp + source + filtering

## 2. Logging Kya Hai

```
2026-09-29 10:15:32 INFO Work order WO-1001 created
```

**Explanation:**
- `timestamp` → `2026-09-29 10:15:32`
- `level` → `INFO`
- `message` → `Work order WO-1001 created`

## 3. Basic Logging

```python
import logging
logging.warning("Temperature high hai")
```

## 4. Logging Levels

```
DEBUG       10
INFO        20
WARNING     30
ERROR       40
CRITICAL    50
```

**Explanation:**
- Neeche se upar severity increase

## 5. `DEBUG`

```python
logging.debug("Processing row 25")
```

**Explanation:**
- Detailed diagnostic info
- Development/troubleshooting

## 6. `INFO`

```python
logging.info("Work order created")
```

**Explanation:**
- Normal important events

## 7. `WARNING`

```python
logging.warning("Equipment ID missing")
```

**Explanation:**
- Potential problem
- Application continue

## 8. `ERROR`

```python
logging.error("Folder creation failed")
```

**Explanation:**
- Operation fail hui

## 9. `CRITICAL`

```python
logging.critical("Database unavailable")
```

**Explanation:**
- Serious failure

## 10. Basic Example

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.debug("Debug message")
logging.info("Application started")
logging.warning("Warning")
logging.error("Something failed")
logging.critical("Critical failure")
```

**Output:**
```
INFO:root:Application started
WARNING:root:Warning
ERROR:root:Something failed
CRITICAL:root:Critical failure
```

**Explanation:**
- `DEBUG` nahi dikha (level `INFO` hai)

## 11. Level Filtering

```python
logging.basicConfig(level=logging.WARNING)
```

**Explanation:**
- `DEBUG` ❌
- `INFO` ❌
- `WARNING` ✅
- `ERROR` ✅
- `CRITICAL` ✅

## 12. `basicConfig()`

```python
logging.basicConfig(level=logging.INFO)
```

**Explanation:**
- Simple scripts ke liye

## 13. Log Format

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

**Output:**
```
2026-09-29 10:20:15,123 - INFO - Application started
```

## 14. Useful Format Fields

```python
%(asctime)s     # Timestamp
%(levelname)s   # Level name
%(name)s        # Logger name
%(message)s     # Message
%(filename)s    # File name
%(lineno)d      # Line number
%(funcName)s    # Function name
```

## 15. Logger Object

```python
logger = logging.getLogger(__name__)
logger.info("Work order processing started")
```

**Explanation:**
- Production-style code
- Logger module name se related

## 16. `__name__` Kyun

```python
# work_orders.py
logger = logging.getLogger(__name__)
```

**Explanation:**
- Logger ka naam module ke naam se
- Large project mein pata chalta hai kis module se aya

## 17. Project Structure

```
project/
├── main.py
├── work_orders.py
├── google_sheets.py
└── folders.py
```

**Explanation:**
- Har module:
```python
logger = logging.getLogger(__name__)
```

## 18. File Mein Logging

```python
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
```

**Explanation:**
- Logs `app.log` mein write honge

## 19. Console + File Dono

```
Logger
   ↓
Handlers
   ├── Console
   └── File
```

## 20. Handler

```python
StreamHandler      # Console
FileHandler        # File
RotatingFileHandler # Rotation
```

**Explanation:**
- Handler → log kahan jayega

## 21. Formatter

```
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

**Explanation:**
- Formatter → log ka appearance

## 22. Complete Logger Example

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

**Output:**
```
2026-09-29 10:30:00 | INFO | my_module | Application started
```

## 23. Logger vs Handler vs Formatter

```
Logger    → log record create
Handler   → kahan jayega?
Formatter → kaise dikhega?
```

## 24. Multiple Handlers

```
logger
   ├── ConsoleHandler → terminal
   └── FileHandler    → app.log
```

**Explanation:**
- Developer → console
- History → file

## 25. Exception Logging

```python
# Bad
except Exception as e:
    print(e)

# Good
except Exception:
    logger.exception("Work order processing failed")
```

## 26. `logger.exception()`

```python
try:
    result = 10 / 0
except Exception:
    logger.exception("Calculation failed")
```

**Output (conceptually):**
```
ERROR Calculation failed
Traceback:
  ...
ZeroDivisionError: division by zero
```

**Explanation:**
- Message + traceback

## 27. `logger.error()` vs `logger.exception()`

```
error()     → message
exception() → message + traceback
```

## 28. `exc_info=True`

```python
logger.error("Something failed", exc_info=True)
```

**Explanation:**
- Traceback include

## 29. Work-Order Example

```python
logger = logging.getLogger(__name__)

def create_work_order_folder(work_order_number):
    logger.info("Creating folder for %s", work_order_number)
    try:
        ...
    except PermissionError:
        logger.exception("Permission denied for %s", work_order_number)
        raise
```

**Explanation:**
- `%s` style preferred over f-string

## 30. `%s` Logging Style

```python
logger.info(
    "Equipment %s temperature is %s",
    equipment_id,
    temperature
)
```

**Output:**
```
Equipment AHU-01 temperature is 22.5
```

## 31. Practical Use

```python
logger.debug("Row data: %s", row)
logger.info("Created folder: %s", folder)
logger.warning("Comment missing for %s", work_order)
logger.error("Folder creation failed for %s", work_order)
logger.critical("Work-order source unavailable")
```

## 32. `print()` Useless Nahi

```
print() → quick debugging, small scripts
logging → production monitoring/auditing
```

## 33. Architecture

```
Application → Logger → LogRecord
                ├── Console Handler → Formatter → Terminal
                └── File Handler    → Formatter → app.log
```

## 34. Level Filter

```
Logger → DEBUG
Console Handler → INFO
File Handler    → DEBUG

DEBUG   → file only
INFO    → console + file
WARNING → console + file
```

## 35. Log Propagation

```
root
├── app
│   ├── app.workorders
│   └── app.folders
```

**Explanation:**
- Child logger parent/root tak propagate

## 36. `propagate`

```python
logger.propagate = False
```

**Explanation:**
- Parent ko propagate nahi

## 37. Duplicate Logging

```python
# Same handler multiple times add
logger.addHandler(handler)
# Output: INFO Started
#         INFO Started
#         INFO Started
```

## 38. Log Rotation

```python
from logging.handlers import RotatingFileHandler
```

```
app.log
app.log.1
app.log.2
app.log.3
```

**Explanation:**
- Size limit par rotation

## 39. Recommended Architecture

```python
# logging_config.py
def get_logger(name):
    return logging.getLogger(name)

# Other modules
from logging_config import get_logger
logger = get_logger(__name__)
```

## 40. Logging + Exception

```python
try:
    process_work_order(row)
except WorkOrderError:
    logger.exception("Work order processing failed")
    raise
```

**Explanation:**
- Error silently disappear nahi hota

## 41. Final Model

```
print() → quick output
logging → structured events → levels → logger → handlers → formatters
```

## 42. Golden Rules

```
DEBUG → detailed diagnostics
INFO → normal events
WARNING → potential problem
ERROR → operation failed
CRITICAL → severe problem
logger = logging.getLogger(__name__)
Handler → destination
Formatter → appearance
logger.exception() → message + traceback
```

---

# Lesson 52: Python Introspection + Reflection + `inspect`

## 1. Introspection

```python
class Equipment:
    def start(self):
        print("Started")

ahu = Equipment()
print(type(ahu))
```

**Output:**
```
<class '__main__.Equipment'>
```

**Explanation:**
- Runtime par object ke baare mein information

## 2. `type()`

```python
x = 100
print(type(x))      # <class 'int'>

name = "AHU-01"
print(type(name))   # <class 'str'>

items = [1, 2, 3]
print(type(items))  # <class 'list'>
```

## 3. `type()` aur `__class__`

```python
print(type(ahu))       # <class 'Equipment'>
print(ahu.__class__)   # <class 'Equipment'>
```

**Explanation:**
- Dono same class

## 4. `id()`

```python
x = []
print(id(x))
```

**Explanation:**
- Object identity

## 5. `dir()`

```python
name = "AHU"
print(dir(name))
```

**Output:**
```
['__add__', '__class__', 'capitalize', 'lower', 'upper', ...]
```

**Explanation:**
- Available names list

## 6. `dir()` Kya Nahi Karta

```
dir() → names list
dir() → implementation nahi
```

## 7. `hasattr()`

```python
hasattr(ahu, "start")   # True
hasattr(ahu, "stop")    # False
```

**Explanation:**
- Attribute/method exists?

## 8. `getattr()`

```python
method = getattr(ahu, "start")
method()
```

**Explanation:**
- Dynamic attribute access

## 9. `getattr()` Default

```python
value = getattr(ahu, "temperature", None)
```

**Explanation:**
- Attribute nahi mila → `None`

## 10. `setattr()`

```python
setattr(ahu, "temperature", 22.5)
print(ahu.temperature)   # 22.5
```

## 11. `delattr()`

```python
delattr(ahu, "temperature")
```

## 12. Family

```
getattr() → attribute read
setattr() → attribute write
delattr() → attribute delete
```

## 13. `vars()`

```python
class Equipment:
    def __init__(self):
        self.equipment_id = "AHU-01"
        self.status = "ON"

ahu = Equipment()
print(vars(ahu))
```

**Output:**
```
{'equipment_id': 'AHU-01', 'status': 'ON'}
```

## 14. `__dict__`

```python
print(ahu.__dict__)
```

**Output:**
```
{'equipment_id': 'AHU-01', 'status': 'ON'}
```

## 15. `vars()` vs `dir()`

```
vars() → actual data
dir() → available names
```

## 16. Class ka `__dict__`

```python
class Equipment:
    category = "HVAC"
    def start(self):
        print("Started")

print(Equipment.__dict__)
```

**Output:**
```
{'category': 'HVAC', 'start': <function ...>, ...}
```

## 17. Instance vs Class Namespace

```python
class Equipment:
    category = "HVAC"
    def __init__(self):
        self.equipment_id = "AHU-01"

ahu = Equipment()
# Equipment.__dict__ → category, __init__
# ahu.__dict__ → equipment_id
```

## 18. Attribute Lookup

```python
ahu.category       # Class se
ahu.equipment_id   # Instance se
```

## 19. `__annotations__`

```python
class Equipment:
    equipment_id: str
    temperature: float

print(Equipment.__annotations__)
```

**Output:**
```
{'equipment_id': <class 'str'>, 'temperature': <class 'float'>}
```

## 20. Function Annotations

```python
def add(a: int, b: int) -> int:
    return a + b

print(add.__annotations__)
```

**Output:**
```
{'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

## 21. Annotations Validation Nahi

```python
add("10", "20")   # Error nahi
```

**Explanation:**
- Annotations → type checkers, IDE, documentation

## 22. `inspect` Module

```python
import inspect
```

## 23. `inspect.isfunction()`

```python
def start():
    pass

print(inspect.isfunction(start))   # True
x = 10
print(inspect.isfunction(x))       # False
```

## 24. `inspect.ismethod()`

```python
class Equipment:
    def start(self):
        pass

ahu = Equipment()
print(inspect.ismethod(ahu.start))   # True
```

## 25. `inspect.isclass()`

```python
print(inspect.isclass(Equipment))   # True
```

## 26. `inspect.isbuiltin()`

```python
print(inspect.isbuiltin(len))   # True
```

## 27. `inspect.signature()`

```python
def create_equipment(equipment_id: str, temperature: float = 22.0, active: bool = True):
    pass

print(inspect.signature(create_equipment))
```

**Output:**
```
(equipment_id: str, temperature: float = 22.0, active: bool = True)
```

## 28. Signature Parameters

```python
signature = inspect.signature(create_equipment)
print(signature.parameters)
```

## 29. Individual Parameter

```python
param = signature.parameters["temperature"]
print(param.name)         # temperature
print(param.annotation)   # float
print(param.default)      # 22.0
```

## 30. `inspect.getmembers()`

```python
members = inspect.getmembers(Equipment)
for name, value in members:
    print(name, value)
```

## 31. Specific Members

```python
methods = inspect.getmembers(Equipment, inspect.isfunction)
```

## 32. `inspect.getsource()`

```python
def add(a, b):
    return a + b

print(inspect.getsource(add))
```

**Output:**
```
def add(a, b):
    return a + b
```

**Explanation:**
- Har callable ka source available nahi

## 33. `inspect.getfile()`

```python
print(inspect.getfile(add))
```

**Output:**
```
C:\project\math_utils.py
```

## 34. `inspect.getmodule()`

```python
module = inspect.getmodule(add)
print(module)
```

## 35. `inspect.iscoroutinefunction()`

```python
async def fetch_data():
    pass

inspect.iscoroutinefunction(fetch_data)   # True
```

## 36. Generator Function

```python
def numbers():
    yield 1

inspect.isgeneratorfunction(numbers)   # True
```

## 37. Callable Detection

```python
def hello():
    pass

callable(hello)   # True
```

## 38. Class with `__call__`

```python
class Logger:
    def __call__(self):
        print("Called")

logger = Logger()
callable(logger)   # True
```

## 39. `isinstance()`

```python
ahu = Equipment()
isinstance(ahu, Equipment)   # True

class AHU(Equipment):
    pass

ahu = AHU()
isinstance(ahu, Equipment)   # True
```

## 40. `issubclass()`

```python
issubclass(AHU, Equipment)   # True
issubclass(Equipment, AHU)   # False
```

## 41. `isinstance` vs `issubclass`

```
isinstance → object
issubclass → classes
```

## 42. `__mro__`

```python
print(AHU.__mro__)
# (AHU, Equipment, object)
```

## 43. `__bases__`

```python
print(AHU.__bases__)
# (<class 'Equipment'>,)
```

**Explanation:**
- `__bases__` → direct parents
- `__mro__` → complete order

## 44. Practical Use

```python
equipment = [AHU(...), VAV(...), Sensor(...)]

for item in equipment:
    print(type(item))
```

## 45. Plugin Architecture

```
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

## 46. Protocol Connection

```python
hasattr(obj, "start")   # Runtime check
```

**Explanation:**
- Protocol → static typing
- `inspect`/`hasattr` → runtime introspection

## 47. Descriptor Connection

```python
MyClass.__dict__   # Descriptor objects
```

## 48. Dataclass Connection

```python
print(Equipment.__annotations__)
from dataclasses import fields
print(fields(Equipment))
```

## 49. TypedDict Connection

```python
WorkOrder.__annotations__
```

## 50. Reflection vs Introspection

```
Introspection → information discover
Reflection → structure access/manipulate
```

## 51. Complete Example

```python
import inspect

class Equipment:
    def __init__(self, equipment_id: str, temperature: float = 22.0):
        self.equipment_id = equipment_id
        self.temperature = temperature

    def start(self) -> None:
        print("Started")

ahu = Equipment("AHU-01")
print(type(ahu))
print(vars(ahu))
print(dir(ahu))
print(hasattr(ahu, "start"))
print(inspect.signature(Equipment))
print(Equipment.__annotations__)
print(Equipment.__dict__)
```

## 52. Tools Table

| Tool | Purpose |
|------|---------|
| `type()` | Type/class |
| `id()` | Identity |
| `dir()` | Available names |
| `vars()` | Namespace |
| `__dict__` | Namespace dict |
| `hasattr()` | Exists? |
| `getattr()` | Dynamic read |
| `setattr()` | Dynamic write |
| `delattr()` | Dynamic delete |
| `isinstance()` | Object relationship |
| `issubclass()` | Class relationship |
| `callable()` | Callable? |
| `inspect.signature()` | Parameters |
| `inspect.getmembers()` | Members |
| `inspect.getsource()` | Source |
| `inspect.isclass()` | Class check |

## 53. Golden Rules

```
type() → class
dir() → names
vars()/__dict__ → namespace
getattr/setattr/delattr → dynamic access
inspect.signature() → parameter contract
isinstance() → object relationship
issubclass() → class relationship
Annotations → runtime available, validation nahi
```

---

# Lesson 53: Modules, Packages aur Import System

## 1. Module

```
project/
├── main.py
└── cell.py
```

**Explanation:**
- `.py` file → module

## 2. Module Faida

```
main.py → Cell
employee.py → Employee
work_order.py → WorkOrder
```

## 3. Import

```python
# cell.py
class Cell:
    def read(self):
        return "data"

# main.py
from cell import Cell
cell = Cell()
print(cell.read())   # data
```

## 4. `import module`

```python
import cell
c = cell.Cell()
```

## 5. `from module import Name`

```python
from cell import Cell
c = Cell()
```

## 6. Package

```
project/
├── main.py
└── equipment/
    ├── __init__.py
    ├── cell.py
    ├── sensor.py
    └── controller.py
```

**Explanation:**
- `equipment` → package

## 7. `__init__.py`

```
equipment/
└── __init__.py
```

**Explanation:**
- Package initialize

## 8. `__init__.py` Content

```python
# __init__.py
from .cell import Cell
from .sensor import Sensor
```

**Explanation:**
- Public interface

## 9. `from .cell import Cell`

```
.
↓
current package
```

**Explanation:**
- `cell.py` se `Cell`

## 10. `.` Current Package

```
. → current package
.. → parent package
```

## 11. Absolute vs Relative

```python
# Absolute
from equipment.cell import Cell

# Relative
from .cell import Cell
```

## 12. Relative Import Faida

```
controller → same package → cell
```

## 13. Relative Import Problem

```bash
python controller.py   # Error
```

**Error:**
```
ImportError: attempted relative import with no known parent package
```

## 14. Correct Execution

```bash
python -m equipment.controller
```

**Explanation:**
- `-m` → module context

## 15. `__name__`

```python
print(__name__)   # __main__ (direct)
```

```python
import cell
cell.__name__     # cell
```

## 16. `if __name__ == "__main__"`

```python
if __name__ == "__main__":
    main()
```

**Explanation:**
- Direct execute par chale

## 17. Pattern Use

```python
def main():
    print("Application started")

if __name__ == "__main__":
    main()
```

## 18. `__main__` Example

```python
# app.py
print("Module loaded")

if __name__ == "__main__":
    print("Program started")

# Direct: Module loaded, Program started
# Import: Module loaded
```

## 19. `sys.path`

```python
import sys
print(sys.path)
```

**Explanation:**
- Import search locations

## 20. `sys.path` Entries

```
current/script-related
standard library
site-packages
venv packages
```

## 21. `sys.path` Practical

```python
import sys
for path in sys.path:
    print(path)
```

## 22. `sys.modules`

```python
import sys
print("math" in sys.modules)
```

**Explanation:**
- Loaded modules cache

## 23. Import Caching

```
First import → find + load + sys.modules
Second import → sys.modules use
```

## 24. `importlib`

```python
import importlib
module = importlib.import_module("math")
print(module.sqrt(16))   # 4.0
```

## 25. Dynamic Import

```python
name = "math"
math_module = importlib.import_module(name)
```

## 26. Package Architecture

```
workorder/
├── __init__.py
├── models.py
├── validation.py
├── folders.py
├── sheets.py
└── main.py
```

## 27. Internal Imports

```python
# validation.py
from .models import WorkOrder
```

## 28. Import Architecture

```
workorder
├── models ← validation
├── models ← folders
└── models ← sheets
```

## 29. Circular Import

```python
# a.py
from b import B

# b.py
from a import A
```

**Error:**
- Circular import

## 30. Avoid Circular

```
Bad:  a ↔ b
Good: a → common ← b
```

## 31. `__init__.py` as API

```python
# equipment/__init__.py
from .ahu import AHU
from .vav import VAV
```

```python
from equipment import AHU, VAV
```

## 32. `__all__`

```python
__all__ = ["AHU", "VAV"]
```

**Explanation:**
- `from x import *` behavior

## 33. `__name__`, `__package__`, `__spec__`

```python
print(__name__)
print(__package__)
print(__spec__)
```

## 34. Absolute vs Relative Comparison

| Syntax | Meaning |
|--------|---------|
| `import cell` | module |
| `from cell import Cell` | specific name |
| `from equipment.cell import Cell` | absolute |
| `from .cell import Cell` | current package |
| `from ..cell import Cell` | parent |

## 35. `.cell` Answer

```
.
↓
current package

cell
↓
cell.py

Cell
↓
class
```

## 36. Mental Model

```
.py → Module
folder → Package
import → machinery
sys.path → search
sys.modules → cache
__name__ → identity
. → current package
.. → parent
```

## 37. Complete Example

```python
# cell.py
class Cell:
    def read(self):
        return "Temperature = 22.5"

# manager.py
from .cell import Cell

class Manager:
    def read_cell(self):
        cell = Cell()
        return cell.read()

# main.py
from equipment.manager import Manager

def main():
    manager = Manager()
    print(manager.read_cell())

if __name__ == "__main__":
    main()
```

**Output:**
```
Temperature = 22.5
```

## 38. Golden Rules

```
.py → module
package → organize
import → module import
from x import Y → specific
. → current package
.. → parent
__name__ → identity
__main__ → direct execution
sys.path → search
sys.modules → cache
importlib → dynamic
__init__.py → public API
```

---

# Lesson 54: Import Machinery — Finder, Loader, ModuleSpec

## 1. `import` Flow

```
1. sys.modules check
2. Find module
3. ModuleSpec
4. Create module
5. Execute code
6. sys.modules register
```

## 2. `sys.modules`

```python
import sys
print("math" in sys.modules)   # True
```

## 3. Import Caching

```python
import math
import math   # Second time cached
```

## 4. Finder

```
Finder → Module kahan hai?
```

## 5. Loader

```
Loader → Module load/execute kaise?
```

## 6. `ModuleSpec`

```python
import math
print(math.__spec__)
```

```
ModuleSpec
├── name
├── loader
├── origin
└── ...
```

## 7. `__spec__`

```python
import math
print(math.__spec__)
```

## 8. `__spec__.name`

```python
print(math.__spec__.name)   # math
```

## 9. `__spec__.loader`

```python
print(math.__spec__.loader)
```

## 10. `__spec__.origin`

```python
print(math.__spec__.origin)
```

**Output:**
```
built-in
```

## 11. `sys.meta_path`

```python
import sys
print(sys.meta_path)
```

**Explanation:**
- Meta path finders

## 12. Finder Sequence

```
import xyz
 ↓
Finder #1
 ↓
Finder #2
 ↓
Finder #3 (mila)
```

## 13. `sys.path` vs `sys.meta_path`

```
sys.meta_path → mechanisms
sys.path → locations
```

## 14. `PathFinder`

```python
import importlib.machinery
importlib.machinery.PathFinder
```

```
sys.meta_path
 ↓
PathFinder
 ↓
sys.path
 ↓
module file
```

## 15. `FileFinder`

```
sys.path → FileFinder → .py / package
```

## 16. Module Forms

```
.py source
built-in
extension
package
namespace package
```

## 17. Built-in Module

```python
import sys   # Built-in
```

## 18. Source Module

```python
# cell.py
class Cell:
    pass
```

## 19. Package Import

```python
import equipment
```

## 20. Submodule Import

```python
import equipment.cell
```

## 21. `__path__`

```python
equipment.__path__
```

## 22. `__file__`

```python
import mymodule
print(mymodule.__file__)
```

## 23. `__cached__`

```python
print(mymodule.__cached__)
```

## 24. `__pycache__`

```
project/
├── main.py
├── cell.py
└── __pycache__/
    └── cell.cpython-3xx.pyc
```

## 25. `.pyc`

```
cell.py → bytecode → .pyc
```

## 26. `.pyc` Machine Code Nahi

```
.py → source
.pyc → bytecode
machine code → CPU instructions
```

## 27. `__pycache__` Purpose

```
First: compile + cache
Later: cached bytecode
```

## 28. `.pyc` Manually Edit Nahi

- Python khud manage karta hai

## 29. `find_spec()`

```python
import importlib.util
spec = importlib.util.find_spec("math")
print(spec)
```

## 30. `find_spec()` Example

```python
spec = importlib.util.find_spec("json")
print(spec.name)
print(spec.loader)
print(spec.origin)
```

## 31. `import_module()`

```python
import importlib
module = importlib.import_module("math")
print(module.sqrt(25))   # 5.0
```

## 32. Plugin System

```
plugins/
├── hvac.py
├── electrical.py
└── plumbing.py
```

```python
plugin = importlib.import_module("plugins.hvac")
```

## 33. Custom Finder

```
import mydata
 ↓
Custom Finder
 ↓
ModuleSpec
 ↓
Custom Loader
 ↓
Module
```

## 34. Custom Finder Idea

```
Python: "mujhe myplugin chahiye"
Custom Finder: "pata hai kahan"
ModuleSpec
Custom Loader: "load karunga"
Module
```

## 35. `MetaPathFinder`

```python
import importlib.abc

class MyFinder(importlib.abc.MetaPathFinder):
    ...
```

## 36. `Loader`

```
create module
 ↓
execute module
```

## 37. Finder + Loader

```
import → sys.meta_path → Finder → ModuleSpec
                              ↓
                           Loader → execute → module
```

## 38. `ModuleSpec` Simple

```
ModuleSpec → import blueprint
Module → actual loaded module
```

## 39. Module vs ModuleSpec

```python
import math
print(type(math))         # <class 'module'>
print(type(math.__spec__)) # <class 'ModuleSpec'>
```

## 40. Deep Flow

```
import equipment.cell
 ↓
sys.modules check
 ↓
Finder
 ↓
ModuleSpec
 ↓
Loader
 ↓
Create module
 ↓
sys.modules register
 ↓
Execute code
 ↓
Loaded module
```

## 41. Module Code Execute

```python
# cell.py
print("Cell module loaded")
class Cell:
    pass

import cell
# Output: Cell module loaded
```

## 42. Top-level Side Effects

```python
# Bad
connect_to_production_database()
delete_old_records()
```

## 43. Import vs Execution

```
import → module load + execute
function call → function body
class definition → class creation
```

## 44. `reload()`

```python
import importlib
import mymodule
importlib.reload(mymodule)
```

## 45. Reload Caveats

- Purane references vs new objects

## 46. Work-Order Project

```python
from workorder.models import WorkOrder
from workorder.validation import validate
from workorder.folders import create_work_order_folders
```

## 47. Relative Import

```python
from .models import WorkOrder
```

## 48. Comparison Table

| Concept | Meaning |
|---------|---------|
| `sys.path` | Search locations |
| `sys.meta_path` | Finders |
| Finder | Locate module |
| `ModuleSpec` | Metadata |
| Loader | Load/execute |
| `sys.modules` | Cache |
| `__file__` | Location |
| `__path__` | Package search |
| `__pycache__` | Bytecode cache |
| `.pyc` | Cached bytecode |
| `importlib` | Import APIs |

## 49. Debugging

```python
import equipment
print(equipment)
print(equipment.__name__)
print(equipment.__file__)
print(equipment.__package__)
print(equipment.__spec__)
print(equipment.__path__)
```

## 50. Golden Mental Model

```
IMPORT
  ↓
sys.modules?
 yes → reuse
 no  → sys.meta_path
         ↓
       Finder
         ↓
     ModuleSpec
         ↓
       Loader
         ↓
    Module Object
         ↓
   Execute code
         ↓
    sys.modules
```

## 51. Core 5

```
Finder → locate
Loader → load/execute
ModuleSpec → metadata
sys.meta_path → finders
sys.modules → cache
```

```
.py → source
.pyc → bytecode
machine code → CPU
```

---

# Lesson 55: Attribute Access — `property`, Descriptor, `__getattribute__`

## 1. Simple Example

```python
class Equipment:
    def __init__(self):
        self.temperature = 22.5

ahu = Equipment()
print(ahu.temperature)   # 22.5
print(ahu.__dict__)      # {'temperature': 22.5}
```

## 2. `__getattribute__`

```python
class Equipment:
    def __init__(self):
        self.temperature = 22.5

    def __getattribute__(self, name):
        print("GET:", name)
        return super().__getattribute__(name)

ahu = Equipment()
print(ahu.temperature)
```

**Output:**
```
GET: temperature
22.5
```

## 3. Har Attribute

```python
print(ahu.__dict__)   # GET: __dict__
```

## 4. Recursion Danger

```python
# Bad
def __getattribute__(self, name):
    return self.__dict__[name]
# Infinite recursion
```

## 5. Correct Technique

```python
def __getattribute__(self, name):
    print("GET:", name)
    return super().__getattribute__(name)
```

## 6. `__getattr__`

```python
class Equipment:
    def __init__(self):
        self.temperature = 22.5

    def __getattr__(self, name):
        return f"{name} available nahi hai"

ahu = Equipment()
print(ahu.temperature)   # 22.5
print(ahu.pressure)      # pressure available nahi hai
```

## 7. `__getattribute__` vs `__getattr__`

```
__getattribute__ → har access
__getattr__ → fail hone par
```

```
obj.x
 ↓
__getattribute__
 ↓
success? yes → value
         no  → __getattr__
```

## 8. Descriptor

```python
class Temperature:
    def __get__(self, instance, owner):
        return 22.5

class Equipment:
    temperature = Temperature()

ahu = Equipment()
print(ahu.temperature)   # 22.5
```

## 9. Descriptor Core

```python
__get__()
__set__()
__delete__()
```

## 10. `property` Descriptor Hai

```python
@property
def temperature(self):
    return self._temperature
```

```
@property → property object → descriptor → attribute access
```

## 11. Property Getter

```python
class Equipment:
    def __init__(self):
        self._temperature = 22.5

    @property
    def temperature(self):
        return self._temperature

ahu.temperature   # 22.5 (not ahu.temperature())
```

## 12. Property Setter

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

## 13. Data Descriptor

```python
class PositiveNumber:
    def __get__(self, instance, owner): ...
    def __set__(self, instance, value): ...
```

## 14. Non-Data Descriptor

```python
class Descriptor:
    def __get__(self, instance, owner): ...
```

## 15. Attribute Lookup Priority

```
1. Data descriptor
2. Instance __dict__
3. Non-data descriptor
4. Class attribute
5. __getattr__
```

## 16. Data Descriptor Override

```python
class Descriptor:
    def __get__(self, instance, owner):
        return "descriptor value"
    def __set__(self, instance, value):
        print("SET:", value)

class Equipment:
    temperature = Descriptor()

ahu = Equipment()
ahu.__dict__["temperature"] = 100
print(ahu.temperature)   # descriptor value
```

## 17. Instance `__dict__`

```python
ahu = Equipment()
ahu.temperature = 22.5
print(ahu.__dict__)   # {'temperature': 22.5}
```

## 18. Class Attribute

```python
class Equipment:
    category = "HVAC"

ahu = Equipment()
print(ahu.category)       # HVAC
print(Equipment.category) # HVAC
```

## 19. Shadowing

```python
ahu.category = "Electrical"
print(ahu.category)       # Electrical
print(Equipment.category) # HVAC
```

## 20. Data Descriptor Priority

- Data descriptor instance `__dict__` se priority le sakta hai

## 21. Methods Descriptor

```python
class Equipment:
    def start(self):
        print("Started")

ahu = Equipment()
ahu.start   # bound method
```

## 22. `ahu.start()`

```
ahu → start → bound method → self = ahu
```

## 23. `classmethod` Descriptor

```python
@classmethod
def create(cls):
    return cls()
```

```
instance method → self
classmethod → class
```

## 24. `staticmethod` Descriptor

```python
@staticmethod
def convert(value):
    return value * 2
```

## 25. Single Picture

```
Attribute Access
 ↓
__getattribute__
 ↓
Descriptor lookup
 ├── Data descriptor
 └── Other lookup
      ↓
  __dict__ / class
      ↓
  __getattr__
```

## 26. `__setattr__`

```python
class Equipment:
    def __setattr__(self, name, value):
        print("SET:", name, value)
        super().__setattr__(name, value)

ahu = Equipment()
ahu.temperature = 25
# SET: temperature 25
```

## 27. `__setattr__` Recursion

```python
# Bad
def __setattr__(self, name, value):
    self.name = name   # Recursion

# Good
def __setattr__(self, name, value):
    super().__setattr__(name, value)
```

## 28. `__delattr__`

```python
class Equipment:
    def __delattr__(self, name):
        print("DELETE:", name)
        super().__delattr__(name)
```

## 29. Complete Picture

```
Read:  __getattribute__ → descriptor/namespace/class → __getattr__
Write: __setattr__ → descriptor __set__ → storage
Delete: __delattr__ → descriptor __delete__ → remove
```

## 30. `__getattr__` HVAC

```python
class Equipment:
    def __init__(self):
        self.temperature = 22.5

    def __getattr__(self, name):
        return "Point not available"

ahu = Equipment()
print(ahu.temperature)        # 22.5
print(ahu.damper_position)    # Point not available
```

## 31. Dynamic Points

```python
class Equipment:
    def __init__(self):
        self.points = {"temperature": 22.5, "humidity": 45, "damper": 60}

    def __getattr__(self, name):
        if name in self.points:
            return self.points[name]
        raise AttributeError(name)

ahu = Equipment()
print(ahu.temperature)   # 22.5
print(ahu.humidity)      # 45
```

## 32. `__getattr__` None Return

```python
# Bad
def __getattr__(self, name):
    return None   # Typo hide
```

**Explanation:**
- `ahu.temprature` → `None` (typo detect nahi)

## 33. `__getattribute__` Kab

```
logging
access control
proxy objects
lazy loading
```

## 34. `__getattr__` Kab

```
Missing attributes fallback
```

## 35. Property vs `__getattr__`

```
property → specific known attribute
__getattr__ → arbitrary unknown names
```

## 36. Descriptor vs Property

```
property → specific
Descriptor → reusable multiple fields
```

## 37. Descriptor Reusable

```python
class Equipment:
    temperature = PositiveNumber()
    humidity = PositiveNumber()
    pressure = PositiveNumber()
```

## 38. `__set_name__`

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name
```

## 39. Complete Descriptor

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
            raise ValueError(f"{self.name} cannot be negative")
        instance.__dict__[self.name] = value

class Equipment:
    temperature = PositiveNumber()
    humidity = PositiveNumber()

ahu = Equipment()
ahu.temperature = 22
ahu.humidity = 45
# ahu.temperature = -5  # ValueError
```

## 40. Full Chain

```
ahu.temperature
 ↓
__getattribute__("temperature")
 ↓
Equipment class lookup
 ↓
temperature descriptor?
 yes → descriptor.__get__(ahu, Equipment)
       ↓
      value
```

## 41. Sab Connect

```
@property → Descriptor
Instance methods → Function descriptor
classmethod → Descriptor
staticmethod → Descriptor
__getattribute__ → Central read
__getattr__ → Missing fallback
__setattr__ → Write
__delattr__ → Delete
__dict__ → Namespace
```

## 42. `__slots__` Connection

```
Normal: obj → __dict__ → attributes
Slots: obj → slots → fixed storage
```

## 43. Metaclass Connection

```
Object level: descriptors, __getattribute__, __dict__
Class level: metaclass
```

## 44. Interview Answer

```
obj.x:
__getattribute__
 ↓
data descriptor
 ↓
instance __dict__
 ↓
non-data descriptor/class
 ↓
__getattr__

obj.x = value:
__setattr__
 ↓
data descriptor __set__
 ↓
storage
```

## 45. Golden Rules

```
__getattribute__ → har read
__getattr__ → missing fallback
__setattr__ → assignment
__delattr__ → deletion
Descriptor → access control
property → built-in descriptor
__dict__ → namespace
Data descriptor → priority
Method → function descriptor
```

---

# Lesson 56: Object Model — `object`, `type`, Class, Instance

## 1. Everything Object

```python
x = 10                # int object
name = "AHU"          # str object
items = [1, 2, 3]     # list object
class Equipment: pass # class object
Equipment()           # instance object
```

## 2. Instance

```python
class Equipment:
    pass

ahu = Equipment()
print(type(ahu))   # <class 'Equipment'>
```

## 3. `type(ahu)`

```python
type(ahu)          # Equipment
ahu.__class__      # Equipment
```

## 4. `type(Equipment)`

```python
type(Equipment)    # <class 'type'>
```

```
ahu → Equipment
Equipment → type
```

## 5. `type` Kya Hai

```
type → default metaclass
    → classes create karti hai
```

## 6. `type()` Double Role

```python
# Role 1: Type discover
type(ahu)   # Equipment

# Role 2: Dynamic class
Employee = type("Employee", (), {})
```

## 7. Dynamic Class

```python
Employee = type(
    "Employee",
    (),
    {"company": "ABC"}
)

e = Employee()
print(e.company)   # ABC
```

## 8. `type(name, bases, namespace)`

```python
Animal = type(
    "Animal",   # Name
    (),         # Bases
    {}          # Namespace
)
```

## 9. Inheritance Dynamically

```python
class Equipment:
    def start(self):
        print("Started")

AHU = type("AHU", (Equipment,), {})
ahu = AHU()
ahu.start()   # Started
```

## 10. `object`

```python
class Equipment:
    pass

Equipment.__bases__   # (<class 'object'>,)
```

## 11. `object` MRO

```python
print(Equipment.__mro__)
# (Equipment, object)
```

## 12. `type(object)`

```python
type(object)   # <class 'type'>
```

```
object → type
```

## 13. `type(type)`

```python
type(type)   # <class 'type'>
```

```
type → type
```

## 14. `object` vs `type`

```
object → base class
type → metaclass
```

```python
issubclass(Equipment, object)   # True
isinstance(Equipment, type)     # True
```

## 15. Four Relationships

| Expression | Meaning |
|-----------|---------|
| `isinstance(ahu, Equipment)` | Instance |
| `issubclass(Equipment, object)` | Inherits |
| `isinstance(Equipment, type)` | Metaclass |
| `isinstance(type, type)` | Self |

## 16. Diagram

```
INSTANCE:
ahu → Equipment
Equipment → type
object → type
type → type

INHERITANCE:
Equipment → object
```

## 17. `isinstance` vs `issubclass`

```python
class Equipment: pass
class AHU(Equipment): pass

ahu = AHU()

isinstance(ahu, AHU)         # True
isinstance(ahu, Equipment)   # True
issubclass(AHU, Equipment)   # True
```

## 18. Class Bhi Object

```python
class Equipment:
    pass

Equipment.__dict__
Equipment.__mro__
Equipment.__bases__
Equipment.__name__
```

## 19. Class Creation Flow

```
class statement
 ↓
namespace prepare
 ↓
body execute
 ↓
metaclass
 ↓
class object
```

## 20. Custom Metaclass

```python
class MyMeta(type):
    pass

class Equipment(metaclass=MyMeta):
    pass

type(Equipment)   # MyMeta
```

## 21. Metaclass Role

```
Instance → class
Class → metaclass
```

## 22. Metaclass Hierarchy

```python
class MyMeta(type):
    pass

type(MyMeta)   # type
```

## 23. `type.__bases__`

```python
type.__bases__   # (<class 'object'>,)
```

## 24. Important Distinction

```
"is instance of" → isinstance()
"inherits from" → issubclass()
```

## 25. `type(type)` Self-reference

```
type → type
```

## 26. `object` + `type`

```
INSTANCE-OF:
ahu → Equipment → type
object → type
type → type

INHERITANCE:
Equipment → object
type → object
```

## 27. Table

| Entity | `type(entity)` | Parent |
|--------|---------------|--------|
| `ahu` | `Equipment` | — |
| `Equipment` | `type` | `object` |
| `object` | `type` | — |
| `type` | `type` | `object` |

## 28. `__class__`

```python
ahu.__class__        # Equipment
Equipment.__class__  # type
object.__class__     # type
```

## 29. `__class__` vs `type()`

```python
type(ahu) is ahu.__class__   # True
```

## 30. `__bases__`

```python
Equipment.__bases__   # (object,)
AHU.__bases__         # (Equipment,)
```

## 31. `__mro__`

```python
AHU.__mro__   # (AHU, Equipment, object)
```

## 32. Class `__dict__`

```python
Equipment.__dict__   # {'__module__', '__init__', ...}
```

## 33. Class Object Attributes

```python
class MyMeta(type):
    def __new__(mcls, name, bases, namespace):
        print("Creating:", name)
        return super().__new__(mcls, name, bases, namespace)

class Equipment(metaclass=MyMeta):
    pass
# Output: Creating: Equipment
```

## 34. Instance vs Class Creation

```
Instance:
Equipment()
 ↓
__new__
 ↓
__init__

Class:
class Equipment:
 ↓
metaclass
 ↓
__new__
 ↓
class object
```

## 35. Connection to Lessons

```
__new__ → instance
metaclass → class
```

## 36. Descriptor Connection

```python
class Equipment:
    @property
    def temperature(self):
        return 22.5

Equipment.__dict__["temperature"]         # property object
type(Equipment.__dict__["temperature"])   # <class 'property'>
```

## 37. Object Model Layers

```
LEVEL 1 — Instance: ahu
LEVEL 2 — Class: Equipment
LEVEL 3 — Metaclass: type / MyMeta
LEVEL 4 — object/type bootstrap
```

## 38. HVAC Example

```python
class Equipment:
    category = "HVAC"
    def start(self):
        print("Equipment started")

class AHU(Equipment):
    pass

ahu = AHU()
```

```
ahu → AHU
AHU → Equipment → object
AHU → type
```

## 39. `isinstance()` Deeper

```python
isinstance(ahu, Equipment)   # True
isinstance(ahu, object)      # True
```

## 40. `isinstance(Equipment, object)`

```python
isinstance(Equipment, object)   # True
```

## 41. `issubclass(type, object)`

```python
issubclass(type, object)   # True
```

## 42. `isinstance(object, type)`

```python
isinstance(object, type)   # True
```

## 43. Four Expressions

```python
isinstance(Equipment(), Equipment)   # True
isinstance(Equipment, type)          # True
isinstance(object, type)             # True
isinstance(type, type)               # True
```

## 44. `object` Root Class

```
object
 ↑
Equipment
 ↑
AHU
```

## 45. `type` Class Factory

```
type → classes create/manage
```

## 46. `type` Ordinary Nahi

```
type() → type inspection
type(name, bases, namespace) → dynamic class
type → metaclass
```

## 47. Final Diagram

```
type
 │
 ├──instance-of──→ Equipment
 ├──instance-of──→ object
 └──instance-of──→ type

Equipment
 ├──inherits-from──→ object
 └──instance-of──→ type
```

## 48. Important Distinction

```
Instance: ahu
Class: Equipment
Metaclass: type

ahu --instance of--> Equipment
Equipment --instance of--> type
Equipment --inherits from--> object
type --inherits from--> object
type --instance of--> type
```

## 49. One-line Mental Model

> Object batata hai "main kis class ka hoon"; class batati hai "main kis metaclass se bana hoon"; inheritance batati hai "main kis parent class se behavior leta hoon."

## 50. Golden Rules

```
1. Classes bhi objects hain
2. type(obj) → class
3. type(Class) → type
4. object → base class
5. type → default metaclass
6. Equipment inherits object
7. Equipment is instance of type
8. type is instance of type
9. __bases__ → direct parents
10. __mro__ → order
11. __class__ → class
12. __new__/__init__ → instance
13. metaclass → class control
```

---

# Lesson 57: ABC vs Protocol vs Duck Typing vs `collections.abc`

## 1. Problem

```python
class AHU:
    def start(self): print("AHU started")

class VAV:
    def start(self): print("VAV started")

class Pump:
    def start(self): print("Pump started")

def start_equipment(equipment):
    equipment.start()

start_equipment(AHU())
start_equipment(VAV())
start_equipment(Pump())
```

**Explanation:**
- Kaise pata chale objects acceptable hain?

## 2. Duck Typing

```python
def start_equipment(equipment):
    equipment.start()
```

**Explanation:**
- Type check nahi
- Sirf `start()` call

## 3. Duck Typing Philosophy

> Object ka naam/type se zyada important hai "object kya kar sakta hai."

## 4. Duck Typing Problem

```python
class BrokenEquipment:
    pass

start_equipment(BrokenEquipment())
# AttributeError: 'BrokenEquipment' object has no attribute 'start'
```

## 5. ABC Solution

```python
from abc import ABC, abstractmethod

class Startable(ABC):
    @abstractmethod
    def start(self):
        pass

class AHU(Startable):
    def start(self):
        print("AHU started")
```

## 6. ABC Explicit Inheritance

```python
class AHU(Startable):
```

**Explanation:**
- Nominal typing
- `AHU is a Startable`

## 7. ABC Benefit

```python
class AHU(Startable):
    pass

AHU()   # TypeError: Can't instantiate abstract class
```

## 8. Protocol

```python
from typing import Protocol

class Startable(Protocol):
    def start(self) -> None:
        ...

class AHU:
    def start(self):
        print("AHU started")
```

**Explanation:**
- Inheritance nahi
- Structure match

## 9. Structural Typing

```
AHU → has required structure → Startable-compatible
```

## 10. Nominal vs Structural

```
Nominal: explicit declaration
Structural: has required structure
```

## 11. Comparison Table

| Feature | ABC | Protocol |
|---------|-----|----------|
| Inheritance | Yes | No |
| Typing | Nominal | Structural |
| Runtime | Stronger | Limited |
| Loose coupling | Less | More |
| Purpose | Hierarchy | Interface |

## 12. Third-party Class

```python
class ExternalMotor:
    def start(self):
        print("Motor started")
```

**Explanation:**
- ABC: inheritance zaroori
- Protocol: structural compatible

## 13. Duck Typing vs Protocol

```
Duck: runtime call
Protocol: type-checking contract
```

## 14. Same Example

```python
# Duck
def start_equipment(equipment):
    equipment.start()

# Protocol
from typing import Protocol
class Startable(Protocol):
    def start(self) -> None: ...

def start_equipment(equipment: Startable):
    equipment.start()
```

## 15. Protocol Advantage

```python
def start_equipment(equipment: Startable):
```

**Explanation:**
- Reader ko clear

## 16. `@runtime_checkable`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Startable(Protocol):
    def start(self) -> None: ...

class AHU:
    def start(self):
        print("Started")

isinstance(AHU(), Startable)   # True
```

## 17. `runtime_checkable` Limitation

```
isinstance → members presence
Full static validation nahi
```

## 18. `collections.abc`

```python
from collections.abc import Iterable, Iterator, Sequence, Mapping, MutableMapping, Callable
```

## 19. `Iterable`

```python
from collections.abc import Iterable

def process(items: Iterable[str]):
    for item in items:
        print(item)

process(["A", "B"])
process(("A", "B"))
process({"A", "B"})
```

## 20. `Sequence`

```python
from collections.abc import Sequence

def first(items: Sequence[str]):
    return items[0]

first(["AHU", "VAV"])
first(("AHU", "VAV"))
```

## 21. `Mapping`

```python
from collections.abc import Mapping

def show_equipment(data: Mapping[str, str]):
    print(data["equipment_id"])
```

## 22. `MutableMapping`

```python
from collections.abc import MutableMapping

def update_status(data: MutableMapping[str, str]):
    data["status"] = "ON"
```

## 23. `Callable`

```python
from collections.abc import Callable

def execute(action: Callable[[], None]):
    action()

def start():
    print("Started")

execute(start)
```

## 24. Ye Protocol Jaisa

```
Iterable → iterate
Sequence → index
Mapping → key/value
Callable → ()
```

## 25. `collections.abc` vs Protocol

```
collections.abc → standard interfaces
Protocol → custom structural
```

## 26. ABC + `collections.abc`

```python
from collections.abc import Sequence
```

**Explanation:**
- Standard abstraction

## 27. `Iterable` Practical

```python
def create_folders(work_orders: Iterable[str]):
    for wo in work_orders:
        print("Creating:", wo)

create_folders(["WO-1001", "WO-1002"])

def work_orders():
    yield "WO-1001"
    yield "WO-1002"

create_folders(work_orders())
```

## 28. `Sequence` Kab

```python
def get_first_work_order(work_orders: Sequence[str]) -> str:
    return work_orders[0]
```

## 29. Design Principle

```python
# Specific
def process(data: list[str]): ...

# Better
def process(data: Iterable[str]): ...
```

## 30. Program to Interface

```python
# Restrictive
def process(data: list[dict]): ...

# Flexible
def process(data: Iterable[Mapping[str, str]]): ...
```

## 31. HVAC Architecture

```python
class AHU:
    def start(self): print("AHU started")

class VAV:
    def start(self): print("VAV started")

from typing import Protocol
class Startable(Protocol):
    def start(self) -> None: ...

def start_system(equipment: Startable) -> None:
    equipment.start()

start_system(AHU())
start_system(VAV())
```

## 32. ABC Version

```python
from abc import ABC, abstractmethod

class Startable(ABC):
    @abstractmethod
    def start(self) -> None: pass

class AHU(Startable):
    def start(self):
        print("AHU started")
```

## 33. Duck Typing Version

```python
def start_system(equipment):
    equipment.start()
```

## 34. Comparison

```
Duck → "start() call kar ke dekho"
Protocol → "start() capability ho"
ABC → "hierarchy ka member bano"
```

## 35. Kab Kya

```
Simple code → Duck typing
Public API → Protocol
Strong hierarchy → ABC
Standard collection → collections.abc
```

## 36. ABC Shared Implementation

```python
class Equipment(ABC):
    def log_start(self):
        print("Starting...")
    @abstractmethod
    def start(self):
        pass

class AHU(Equipment):
    def start(self):
        self.log_start()
        print("AHU started")
```

## 37. Protocol Capability

```python
class Startable(Protocol):
    def start(self) -> None: ...
```

**Explanation:**
- Focus: `start()` capability

## 38. Protocol Multiple

```python
class Startable(Protocol):
    def start(self) -> None: ...

class Stoppable(Protocol):
    def stop(self) -> None: ...

class Controllable(Startable, Stoppable, Protocol):
    pass
```

## 39. Interface Segregation

```
Startable → start()
Stoppable → stop()
Calibratable → calibrate()
```

## 40. Final Architecture

```
Required Behavior
├── Duck Typing → runtime
├── Protocol → structural
├── collections.abc → standard
└── ABC → hierarchy
```

## 41. Golden Mental Model

```
Duck → "Can you do it?"
Protocol → "Structure says yes"
ABC → "Belong to hierarchy"
collections.abc → "Standard capability"
```

## 42. Practical Rule

```
for x in data → Iterable
data[0] → Sequence
data["key"] → Mapping
data["key"] = value → MutableMapping
action() → Callable
equipment.start() → Protocol
Explicit hierarchy → ABC
```

---

# Lesson 58: `Generic[T]` + `TypeVar` + `Protocol` + Variance

## 1. `TypeVar`

```python
from typing import TypeVar
T = TypeVar("T")
```

**Explanation:**
- Placeholder

```python
def identity(value: T) -> T:
    return value

identity(10)     # T = int
identity("AHU")  # T = str
```

## 2. Generic Class

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

numbers = Storage[int]()
names = Storage[str]()
```

## 3. Generic Purpose

```
Storage[int] → set expects int, get returns int
Storage[str] → set expects str, get returns str
```

## 4. HVAC Example

```python
class TemperatureSensor:
    def read(self) -> float:
        return 22.5

class StatusSensor:
    def read(self) -> str:
        return "ON"
```

## 5. Generic Protocol

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Sensor(Protocol[T]):
    def read(self) -> T:
        ...
```

## 6. Generic Function

```python
def read_sensor(sensor: Sensor[T]) -> T:
    return sensor.read()

temperature = read_sensor(TemperatureSensor())   # float
status = read_sensor(StatusSensor())             # str
```

## 7. `Any` se Better

```python
# Bad
def read_sensor(sensor: Any) -> Any:
    return sensor.read()

# Good
def read_sensor(sensor: Sensor[T]) -> T:
    return sensor.read()
```

## 8. `T` Connection

```
Sensor[T] → read() → T → function returns T
```

## 9. Covariance

```python
class Animal: pass
class Dog(Animal): pass
```

## 10. Producer

```python
class Sensor(Protocol[T]):
    def read(self) -> T: ...
```

```
Sensor → produces → T
```

## 11. Covariant TypeVar

```python
T_co = TypeVar("T_co", covariant=True)

class Producer(Protocol[T_co]):
    def get(self) -> T_co: ...
```

```
Dog <: Animal
Producer[Dog] <: Producer[Animal]
```

## 12. Example

```python
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof")

class AnimalProducer(Protocol[T_co]):
    def get(self) -> T_co: ...

class DogProducer:
    def get(self) -> Dog:
        return Dog()
```

## 13. Covariance Shortcut

```
T_co → CO = OUT → Producer → returns T
```

## 14. Contravariance

```python
class Handler(Protocol[T]):
    def handle(self, value: T) -> None: ...
```

```
Handler → consumes → T
```

## 15. Contravariant TypeVar

```python
T_contra = TypeVar("T_contra", contravariant=True)

class Handler(Protocol[T_contra]):
    def handle(self, value: T_contra) -> None: ...
```

## 16. Direction Ulat

```
Animal
 ↑
Dog

Handler[Animal] can handle Dog
```

## 17. Mental Model

```
COVARIANCE → output → producer → same
CONTRAVARIANCE → input → consumer → opposite
INVARIANCE → input + output → no substitution
```

## 18. Invariance

```python
T = TypeVar("T")

class Storage(Generic[T]):
    def get(self) -> T: ...
    def set(self, value: T): ...
```

**Explanation:**
- Read + write → invariant

## 19. `list` Invariant

```
list[Dog] ≠ list[Animal]
```

## 20. `Sequence` Covariant

```
Sequence[Dog] → Sequence[Animal]
```

## 21. `Mapping` Nuanced

```
key/value positions matter
```

## 22. Callable Variance

```python
Callable[[Animal], Dog]
# Input: contravariant
# Output: covariant
```

## 23. `Callable[P, R]`

```python
P = ParamSpec("P")
R = TypeVar("R")

Callable[P, R]
```

```
P → parameters
R → return
```

## 24. Generic Repository

```python
T = TypeVar("T")

class Repository(Protocol[T]):
    def get(self, item_id: str) -> T | None: ...
    def save(self, item: T) -> None: ...
```

## 25. Repository Types

```
Repository[Equipment]
Repository[WorkOrder]
Repository[Employee]
```

## 26. Generic Handler

```python
T = TypeVar("T")

class Handler(Protocol[T]):
    def handle(self, item: T) -> None: ...
```

## 27. Producer + Consumer

```
Sensor[T] → PRODUCER
Repository[T] → STORAGE
Handler[T] → CONSUMER
```

## 28. HVAC Pipeline

```
Temperature Sensor → float → Repository → Handler → Alarm
```

## 29. Protocol + Generic

```python
class Sensor(Protocol[T]):
    def read(self) -> T: ...

# Sensor[float], Sensor[str], Sensor[bool]
```

## 30. TypeVar Bound

```python
T = TypeVar("T", bound=Equipment)

def start_equipment(equipment: T) -> T:
    equipment.start()
    return equipment
```

## 31. Generic + Bound

```python
T = TypeVar("T", bound=Equipment)

class Repository(Generic[T]):
    ...
```

```
Repository[AHU] → OK
Repository[VAV] → OK
Repository[str] → Error
```

## 32. Generic + Protocol + Bound

```python
class Startable(Protocol):
    def start(self) -> None: ...

T = TypeVar("T", bound=Startable)

def start_and_return(item: T) -> T:
    item.start()
    return item
```

## 33. Powerful Pattern

```
Concrete class → capability → Protocol → TypeVar bound → generic function
```

## 34. `Any` vs `T`

```python
# Any
def process(value: Any) -> Any: ...

# T
T = TypeVar("T")
def process(value: T) -> T: ...
```

```
Any → type checking weaken
T → relationship preserve
```

## 35. `object` vs `Any` vs `T`

```
Any → anything, don't check
object → anything, type-safe ops
T → specific, preserve
```

## 36. Work-Order Example

```python
@dataclass
class WorkOrder:
    number: str
    description: str

T = TypeVar("T")

class Repository(Protocol[T]):
    def save(self, item: T) -> None: ...
    def get(self, item_id: str) -> T | None: ...

class WorkOrderRepository:
    def save(self, item: WorkOrder) -> None:
        print("Saving:", item.number)
    def get(self, item_id: str) -> WorkOrder | None:
        return None
```

## 37. Equipment Version

```python
@dataclass
class Equipment:
    equipment_id: str

class EquipmentRepository:
    def save(self, item: Equipment) -> None:
        print("Saving:", item.equipment_id)
    def get(self, item_id: str) -> Equipment | None:
        return None
```

## 38. Full Architecture

```
T
├── Sensor[T] → produces
├── Repository[T] → stores
└── Handler[T] → consumes
```

## 39. Variance Visual

```
COVARIANCE: Producer[Dog] → Producer[Animal]
CONTRAVARIANCE: Consumer[Animal] → Consumer[Dog]
INVARIANCE: Storage[Dog] ≠ Storage[Animal]
```

## 40. Important Correction

- Variance → static type compatibility
- Runtime conversion nahi

## 41. Kab Specify

```
T = TypeVar("T") → invariant
T_co = covariant=True → producer
T_contra = contravariant=True → consumer
```

## 42. Common Mistake

```
covariant ≠ better
contravariant ≠ better
invariant ≠ bad
```

## 43. Golden Rules

```
TypeVar → placeholder
Generic[T] → type-parameterized
Protocol[T] → structural generic
T_co → covariant/output
T_contra → contravariant/input
T → invariant
Callable[P, R] → P parameters, R return
bound=Base → Base/subclass
Any → weak
object → universal
T → specific preserve
```

---

# Lesson 59: `TypeGuard` + `TypeIs` + Type Narrowing

## 1. Type Narrowing

```python
def process(value: int | str):
    if isinstance(value, int):
        print(value + 10)   # value: int
```

**Explanation:**
- `if` ke andar type narrower

## 2. `Union`

```python
int | str   # int OR str
```

## 3. Problem

```python
def process(value: int | str):
    if isinstance(value, int):
        print(value + 10)
    else:
        print(value.upper())
```

**Explanation:**
- Else mein `value: str`

## 4. `isinstance()` Role

```python
value: object = "AHU"
if isinstance(value, str):
    print(value.upper())
```

**Explanation:**
- `object` → `str`

## 5. `object` Narrowing

```python
def process(value: object):
    if isinstance(value, str):
        print(value.upper())
    elif isinstance(value, int):
        print(value + 10)
```

## 6. Custom Function

```python
def is_string(value: object) -> bool:
    return isinstance(value, str)

value: object
if is_string(value):
    value.upper()   # Static checker ko pata nahi
```

## 7. `TypeGuard`

```python
from typing import TypeGuard

def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)

value: object
if is_string(value):
    print(value.upper())   # value: str
```

## 8. `TypeGuard[T]` Meaning

```
True return → value is T
```

## 9. TypeGuard Function

```python
def is_int(value: object) -> TypeGuard[int]:
    return isinstance(value, int)

value: object
if is_int(value):
    print(value + 10)
```

## 10. Structure

```python
def is_something(value: SomeBroad) -> TypeGuard[Specific]:
    ...
```

## 11. HVAC Example

```python
class Equipment:
    pass

class AHU(Equipment):
    def start(self):
        print("AHU started")

from typing import TypeGuard

def is_ahu(equipment: Equipment) -> TypeGuard[AHU]:
    return isinstance(equipment, AHU)

equipment: Equipment = AHU()
if is_ahu(equipment):
    equipment.start()   # AHU
```

## 12. TypeGuard Bool Nahi

```
-> TypeGuard[AHU] → runtime True/False
TypeGuard → static info
```

## 13. Runtime Validation Nahi

```python
# Dangerous
def is_ahu(equipment: Equipment) -> TypeGuard[AHU]:
    return True   # WRONG
```

## 14. TypeGuard Purpose

```python
def is_valid_work_order(data: dict) -> TypeGuard[dict[str, str]]:
    ...

if is_valid_work_order(data):
    # data: dict[str, str]
```

## 15. Generic TypeGuard

```python
from typing import TypeGuard

def is_str_list(value: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in value)

items: list[object] = ["AHU", "VAV"]
if is_str_list(items):
    for item in items:
        print(item.upper())
```

## 16. Importance

```python
list[object] → verified → list[str]
```

## 17. TypeGuard vs `isinstance`

```
isinstance → built-in narrowing
TypeGuard → custom predicate
```

## 18. `TypeIs`

```python
from typing import TypeIs

def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)
```

**Explanation:**
- Python 3.13+

## 19. TypeGuard vs TypeIs

```
TypeGuard → True branch narrow
TypeIs → True + False branch narrow
```

## 20. TypeIs Example

```python
def is_str(value: object) -> TypeIs[str]:
    return isinstance(value, str)

value: str | int
if is_str(value):
    # value: str
else:
    # value: int
```

## 21. TypeGuard False Branch

```python
def is_str(value: object) -> TypeGuard[str]:
    ...

# True → str
# False → unknown
```

## 22. TypeIs Restrictive

```python
def is_str(value: str | int) -> TypeIs[str]:
    return isinstance(value, str)

# True → str
# False → int
```

## 23. Mental Model

```
TypeGuard → True → T
TypeIs → True → T, False → not T
```

## 24. `Optional` Narrowing

```python
temperature: float | None = None
if temperature is not None:
    print(temperature + 1)   # float
```

## 25. `Union` Narrowing

```python
def process(value: int | str):
    if isinstance(value, int):
        print(value + 1)
    else:
        print(value.upper())
```

## 26. `Literal` Narrowing

```python
from typing import Literal
Mode = Literal["auto", "manual"]

def set_mode(mode: Mode):
    if mode == "auto":
        ...
    else:
        ...
```

## 27. `Enum` Narrowing

```python
from enum import Enum

class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"

def configure(mode: Mode):
    if mode is Mode.AUTO:
        print("Automatic")
    else:
        print("Manual")
```

## 28. `issubclass()` Narrowing

```python
class Equipment: pass
class AHU(Equipment): pass

def inspect_class(cls: type[Equipment]):
    if issubclass(cls, AHU):
        print("AHU class")
```

## 29. `type[...]`

```python
type[Equipment]   # Equipment class object
```

## 30. Example

```python
def create_equipment(cls: type[Equipment]) -> Equipment:
    return cls()

ahu = create_equipment(AHU)
```

## 31. `isinstance` + `issubclass`

```
isinstance → object instance
issubclass → class subclass
```

## 32. Narrowing Flow

```
Broad → condition → narrower
object → isinstance(value, AHU) → AHU
Equipment → is_ahu(equipment) → TypeGuard[AHU] → AHU
```

## 33. Work-Order Practical

```python
from typing import TypedDict, TypeGuard

class WorkOrder(TypedDict):
    work_order_number: str
    code: str
    description: str
    area: str
    floor: str
    comment: str

def is_work_order(data: dict) -> TypeGuard[WorkOrder]:
    required = ["work_order_number", "code", "description", "area", "floor", "comment"]
    return all(key in data and isinstance(data[key], str) for key in required)

if is_work_order(row):
    print(row["work_order_number"])
```

## 34. Warning

```python
# TypeGuard likhne se runtime safe nahi
def is_work_order(data) -> TypeGuard[WorkOrder]:
    return True   # WRONG
```

## 35. TypeGuard + Protocol

```python
from typing import Protocol, TypeGuard

class Startable(Protocol):
    def start(self) -> None: ...

def is_startable(value: object) -> TypeGuard[Startable]:
    return callable(getattr(value, "start", None))

if is_startable(equipment):
    equipment.start()
```

## 36. Runtime Protocol Check

```python
@runtime_checkable
class Startable(Protocol):
    def start(self) -> None: ...

isinstance(obj, Startable)
```

**Explanation:**
- Runtime less detailed

## 37. TypeIs Kab

```
A | B → True A, False B
```

## 38. TypeGuard Kab

```
Broad → specific (custom validation)
```

## 39. Hierarchy

```
Type Narrowing
├── isinstance
├── issubclass
├── custom predicate
│   ├── TypeGuard
│   └── TypeIs
```

## 40. Golden Rules

```
Union → multiple types
isinstance → instance check
issubclass → class check
TypeGuard[T] → True branch T
TypeIs[T] → True T, False not T
object → broad
type[Equipment] → class object
Optional[T] → T | None
```

## 41. Important Example

```python
from typing import TypeGuard

class Equipment: pass
class AHU(Equipment):
    def start(self):
        print("AHU started")

def is_ahu(equipment: Equipment) -> TypeGuard[AHU]:
    return isinstance(equipment, AHU)

equipment: Equipment = AHU()
if is_ahu(equipment):
    equipment.start()
```

**Flow:**
```
Equipment → is_ahu() → TypeGuard[AHU] → AHU → start()
```

---

# Lesson 60: `match` / `case` — Structural Pattern Matching

## 1. Basic `match`

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

**Output:**
```
Equipment running
```

## 2. `case _`

```python
case _:
```

**Explanation:**
- Fallback (koi bhi)

## 3. Flow

```
value → match → case 1 → case 2 → matched case
```

## 4. Multiple Values

```python
day = "Saturday"

match day:
    case "Saturday" | "Sunday":
        print("Weekend")
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("Working day")
```

## 5. `|` vs `or`

```
case "ON" | "AUTO" → pattern alternatives
```

## 6. Variable Capture

```python
value = 10
match value:
    case x:
        print(x)   # 10
```

**Explanation:**
- `x` → capture pattern

## 7. `_` vs Variable

```python
case _:   # Ignore
case x:   # Capture
```

## 8. Literal Patterns

```python
match value:
    case 10:
        print("Ten")
    case "AHU":
        print("AHU")
    case True:
        print("True")
```

## 9. Type Patterns

```python
value = 100

match value:
    case int():
        print("Integer")
    case str():
        print("String")
```

**Output:**
```
Integer
```

## 10. `int()` Pattern

```python
match value:
    case int():
        print("integer")
```

## 11. Type + Capture

```python
value = 42

match value:
    case int(x):
        print(x)   # 42
```

## 12. HVAC Example

```python
class Equipment: pass
class AHU(Equipment): pass
class VAV(Equipment): pass

equipment = AHU()

match equipment:
    case AHU():
        print("AHU")
    case VAV():
        print("VAV")
    case Equipment():
        print("Other equipment")
```

**Output:**
```
AHU
```

## 13. Case Order

```python
# Specific pehle
case AHU():
case VAV():
case Equipment():
```

## 14. Sequence Patterns

```python
data = [10, 20]

match data:
    case [10, 20]:
        print("Exact list")
```

## 15. Capture Sequence

```python
data = [10, 20]

match data:
    case [a, b]:
        print(a)   # 10
        print(b)   # 20
```

## 16. Three Elements

```python
data = [10, 20, 30]

match data:
    case [a, b, c]:
        print(a, b, c)   # 10 20 30
```

## 17. `*rest`

```python
data = [10, 20, 30, 40]

match data:
    case [first, *rest]:
        print(first)   # 10
        print(rest)    # [20, 30, 40]
```

## 18. Exact vs Flexible

```python
case [a, b]:        # Exactly 2
case [a, *rest]:    # Variable
```

## 19. Nested Sequence

```python
data = [10, [20, 30]]

match data:
    case [a, [b, c]]:
        print(a, b, c)   # 10 20 30
```

## 20. Mapping Patterns

```python
equipment = {"type": "AHU", "status": "ON"}

match equipment:
    case {"type": "AHU", "status": "ON"}:
        print("Running AHU")
```

## 21. Capture Values

```python
equipment = {"type": "AHU", "status": "ON"}

match equipment:
    case {"type": equipment_type, "status": status}:
        print(equipment_type)   # AHU
        print(status)           # ON
```

## 22. Extra Keys

```python
equipment = {"type": "AHU", "status": "ON", "temperature": 22.5}

match equipment:
    case {"type": "AHU"}:
        print("Match")   # Extra keys OK
```

## 23. `**rest`

```python
match equipment:
    case {"type": "AHU", **rest}:
        print(rest)   # {"status": "ON", "temperature": 22.5}
```

## 24. Class Patterns

```python
class Equipment:
    def __init__(self, equipment_id, status):
        self.equipment_id = equipment_id
        self.status = status

ahu = Equipment("AHU-01", "ON")

match ahu:
    case Equipment("AHU-01", "ON"):
        print("Running AHU-01")
```

## 25. `__match_args__`

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    status: str

equipment = Equipment("AHU-01", "ON")

match equipment:
    case Equipment("AHU-01", "ON"):
        print("Match")
```

## 26. Keyword Class Pattern

```python
match equipment:
    case Equipment(equipment_id="AHU-01", status="ON"):
        print("Match")
```

## 27. Dataclass + Match

```python
from dataclasses import dataclass

@dataclass
class WorkOrder:
    number: str
    status: str
    floor: str

wo = WorkOrder("WO-1001", "OPEN", "34")

match wo:
    case WorkOrder(number="WO-1001", status="OPEN"):
        print("Open work order")
```

## 28. Guards

```python
temperature = 28

match temperature:
    case int() as temp if temp > 25:
        print("High temperature")
    case int() as temp:
        print("Normal temperature")
```

## 29. Guard Flow

```
value → pattern match? → yes → guard → True → execute
                              ↓
                           False → next case
```

## 30. `as` Pattern

```python
match value:
    case int() as number:
        print(number)
```

## 31. Type + Condition

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

**Output:**
```
High
```

## 32. OR Pattern + Capture

```python
mode = "AUTO"

match mode:
    case "AUTO" | "MANUAL":
        print("Control mode")
```

## 33. Nested Pattern

```python
row = {
    "equipment": {"type": "AHU", "status": "ON"},
    "floor": 34
}

match row:
    case {"equipment": {"type": "AHU", "status": "ON"}, "floor": floor}:
        print("AHU running on floor", floor)
```

**Output:**
```
AHU running on floor 34
```

## 34. Work-Order Example

```python
row = {
    "work_order": "WO-1001",
    "status": "OPEN",
    "priority": "HIGH"
}

match row:
    case {"work_order": wo, "status": "OPEN", "priority": "HIGH"}:
        print("High priority:", wo)
    case {"work_order": wo, "status": "OPEN"}:
        print("Open:", wo)
    case _:
        print("Other")
```

## 35. Pattern Order

```
Specific → general → fallback
```

## 36. `match` vs `if/elif`

```python
# Simple
if status == "ON": ...
elif status == "OFF": ...

# Match
match status:
    case "ON": ...
    case "OFF": ...
```

## 37. Pattern Power

```
type + value + sequence + mapping + class + nested + conditions
```

## 38. `match` vs Protocol

```
Protocol → capability
match → structure/value
```

## 39. `match` vs TypeGuard

```
TypeGuard → custom predicate narrowing
match → pattern matching
```

## 40. `match` + TypeGuard

```python
match equipment:
    case AHU():
        print("AHU")
    case VAV():
        print("VAV")
    case _:
        print("Unknown")
```

## 41. `case _`

```python
case _:
    print("Unknown")
```

**Explanation:**
- Default (agar koi match nahi)

## 42. Match vs Switch

```
Switch → case value
Match → pattern + structure + bindings + guard
```

## 43. Complete HVAC Example

```python
from dataclasses import dataclass

@dataclass
class Equipment:
    equipment_id: str
    status: str
    temperature: float

equipment = Equipment("AHU-01", "ON", 27.5)

match equipment:
    case Equipment(equipment_id="AHU-01", status="ON", temperature=temp) if temp >= 25:
        print("AHU-01 running with high temperature")
    case Equipment(equipment_id="AHU-01", status="ON", temperature=temp):
        print("AHU-01 normal")
    case Equipment(status="OFF"):
        print("Equipment OFF")
    case _:
        print("Unknown equipment")
```

## 44. Flow

```
Equipment → case Equipment(...) → ID? → status? → temp capture → temp >= 25? → YES
```

## 45. Work-Order Powerful

```python
row = {
    "work_order": "WO-1001",
    "code": "HVAC",
    "floor": "34",
    "status": "OPEN"
}

match row:
    case {"work_order": wo, "code": "HVAC", "status": "OPEN"}:
        print("HVAC WO:", wo)
    case {"work_order": wo, "status": "CLOSED"}:
        print("Closed:", wo)
    case _:
        print("Other")
```

## 46. Kab Use

```
Multiple structured cases
Nested dicts/lists
Different classes
Parsing/dispatch
```

## 47. Kab Avoid

```python
if x > 10 and y < 20:   # Simple if better
```

## 48. Mental Model

```
if → condition
match → pattern
```

## 49. Golden Rules

```
case _ → fallback
case A | B → OR
case [a, b] → sequence
case [first, *rest] → variable
case {"key": value} → mapping
case Class(...) → class
case ... if condition → guard
case Type() as value → type + capture
```

## 50. Final Picture

```
match
├── Literal → "ON"
├── Sequence → [a, b]
├── Mapping → {"status": x}
├── Class → Equipment(...)
└── Guard → if temp > 25
```

**Typing:**
```
isinstance → normal narrowing
TypeGuard → custom predicate
TypeIs → positive + negative
match/case → structural narrowing
```

---

**Ab ye guide complete hai (Lessons 51-60).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ Golden rules

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀