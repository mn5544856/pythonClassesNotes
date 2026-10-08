# Python OOP — Lessons 21-30 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 21: `Optional`, `Union`, `Literal`, `Final`, `ClassVar`, `Any`, `Never`, `NoReturn`

## 1. `Optional`

```python
from typing import Optional

name: Optional[str]
```

**Explanation:**
- `Optional[str]` → value `str` ho sakti hai **ya** `None`
- Modern Python: `str | None`

```python
def get_employee_name(employee_id: int) -> Optional[str]:
    if employee_id == 1:
        return "Ali"
    return None
```

**Explanation:**
- `-> Optional[str]` → return `str` ya `None`
- `if employee_id == 1:` → mil gaya to `"Ali"`
- `return None` → nahi mila to `None`

## 2. `Optional` "optional parameter" nahi

```python
def test(name: Optional[str]):
    ...
```

**Explanation:**
- `name: Optional[str]` → `name` `str` ya `None` ho sakta hai
- Lekin argument **dena zaroori** hai
- Optional parameter banane ke liye: `name: Optional[str] = None`

## 3. `Union`

```python
from typing import Union

value: Union[int, str]
```

**Explanation:**
- `Union[int, str]` → `int` **ya** `str`
- Modern: `int | str`

```python
def show_id(value: int | str):
    print(value)

show_id(100)
show_id("WO-100")
```

**Explanation:**
- `value: int | str` → dono types allowed
- `show_id(100)` → int
- `show_id("WO-100")` → str

## 4. `Optional` = `Union[T, None]`

```
Optional[str]  =  Union[str, None]  =  str | None
```

## 5. `Literal`

```python
from typing import Literal

status: Literal["open", "closed"]
```

**Explanation:**
- `Literal["open", "closed"]` → sirf ye 2 values allowed
- `status = "running"` → type checker error

```python
def set_mode(mode: Literal["auto", "manual"]):
    print(mode)

set_mode("auto")     # OK
set_mode("manual")   # OK
set_mode("random")   # Error
```

**Explanation:**
- `mode: Literal["auto", "manual"]` → sirf `"auto"` ya `"manual"`
- `set_mode("random")` → invalid

## 6. HVAC `Literal` Example

```python
def set_fan_mode(mode: Literal["auto", "manual", "off"]):
    ...
```

**Explanation:**
- `mode` sirf `"auto"`, `"manual"`, `"off"`
- `str` se zyada precise

## 7. `Final`

```python
from typing import Final

MAX_RETRIES: Final = 3
```

**Explanation:**
- `Final` → reassign nahi karna chahiye
- `MAX_RETRIES = 10` → type checker warning
- Runtime par lock nahi hota, sirf intent

```python
API_VERSION: Final = "v1"
DEFAULT_TIMEOUT: Final = 30
```

**Explanation:**
- Constants ke liye useful
- `Final` = "is value ko dobara assign mat karo"

## 8. `ClassVar`

```python
from typing import ClassVar

class Employee:
    company: ClassVar[str] = "ABC"

    def __init__(self, name: str):
        self.name = name
```

**Explanation:**
- `company: ClassVar[str]` → class variable
- `name` → instance variable
- Type checker ko clear batata hai

## 9. `Any`

```python
from typing import Any

value: Any
```

**Explanation:**
- `Any` → type checker almost kuch bhi accept kare
- `value` ho sakta hai: `int`, `str`, `list`, `dict`, etc.
- Maximum flexibility, minimum type safety

## 10. `Any` vs `object`

```python
value: Any = "Hello"
value.upper()   # OK (type checker)
```

```python
value: object = "Hello"
value.upper()   # Error
if isinstance(value, str):
    value.upper()   # OK
```

**Explanation:**
- `Any` → type checking relax
- `object` → broad type, lekin type checking maintain

## 11. `Never`

```python
from typing import Never

def fail(message: str) -> Never:
    raise RuntimeError(message)
```

**Explanation:**
- `-> Never` → function kabhi return nahi karta
- `raise RuntimeError(message)` → exception raise kiya

```python
def run_forever() -> Never:
    while True:
        print("Running...")
```

**Explanation:**
- Infinite loop, kabhi return nahi

## 12. `NoReturn`

```python
from typing import NoReturn

def fail(message: str) -> NoReturn:
    raise RuntimeError(message)
```

**Explanation:**
- `NoReturn` → purana annotation
- `Never` → modern preferred
- Dono ka matlab: function return nahi karta

## 13. `Literal` vs `Enum`

```python
# Literal
mode: Literal["auto", "manual"]
```

```python
# Enum
from enum import Enum

class Mode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
```

**Explanation:**
- `Literal` → typing constraint
- `Enum` → actual Python enumeration type
- Complex domain logic ke liye `Enum` useful

## 14. Complete Example

```python
from typing import ClassVar, Final, Literal, Optional

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

**Explanation:**
- `SYSTEM_NAME: ClassVar[Final[str]]` → class variable + final
- `temperature: Optional[float] = None` → `float` ya `None`, default `None`
- `mode: Literal["auto", "manual"] = "auto"` → sirf 2 values, default `"auto"`

## 15. Complete `typing` Map

| Type | Meaning |
|------|---------|
| `Any` | Type checking bypass |
| `TypeVar` | Generic type placeholder |
| `Generic` | Generic class/function |
| `Optional` | `T` or `None` |
| `Union` | Multiple types |
| `Literal` | Fixed values |
| `Final` | Reassign nahi |
| `ClassVar` | Class-level variable |
| `TypedDict` | Dictionary structure |
| `Protocol` | Structural interface |
| `Mapping` | Readable key-value |
| `MutableMapping` | Modifiable key-value |
| `Sequence` | Ordered/indexable |
| `Iterable` | `for` se iterate |
| `Iterator` | `next()` deta hai |
| `Callable` | Function ki tarah call |
| `Never` | No return |
| `Tuple` | Typed tuple |
| `Dict` | Typed dictionary |

## 16. Modern Syntax

| Old | Modern |
|-----|--------|
| `Optional[str]` | `str \| None` |
| `Union[int, str]` | `int \| str` |
| `List[int]` | `list[int]` |
| `Dict[str, int]` | `dict[str, int]` |
| `Tuple[str, int]` | `tuple[str, int]` |

---

# Lesson 22: Variance — Covariant, Contravariant, Invariant

## 1. Basic Hierarchy

```python
class Animal:
    pass

class Dog(Animal):
    pass
```

**Explanation:**
- `Dog` is a subtype of `Animal`
- `animal: Animal = Dog()` → OK

## 2. `list` Problem

```python
dogs: list[Dog] = [Dog()]
animals: list[Animal] = dogs   # Error
```

**Explanation:**
- `list[Dog]` ko `list[Animal]` assign **nahi** kar sakte
- Kyunki `animals.append(Animal())` se `dogs` mein Animal aa jayega

## 3. Invariant

```
Dog <: Animal
lekin
list[Dog] ≠ list[Animal]
```

**Explanation:**
- `<:` → subtype
- `list` mutable hai, isliye invariant

## 4. `Sequence` Different

```python
from typing import Sequence

dogs: Sequence[Dog] = [Dog()]
animals: Sequence[Animal] = dogs   # OK
```

**Explanation:**
- `Sequence` read-only abstraction
- `Sequence[Dog]` → `Sequence[Animal]` allowed
- Ye **covariance** hai

## 5. Covariant

```
Dog → Animal
Sequence[Dog] → Sequence[Animal]
```

**Explanation:**
- `Sequence` covariant hai
- Kyunki `Sequence` mein append nahi kar sakte
- Producer/output ke liye covariant

## 6. `TypeVar` Covariant

```python
from typing import TypeVar, Generic

T_co = TypeVar("T_co", covariant=True)

class Box(Generic[T_co]):
    def __init__(self, value: T_co):
        self._value = value

    def get(self) -> T_co:
        return self._value
```

**Explanation:**
- `T_co = TypeVar("T_co", covariant=True)` → covariant TypeVar
- `Box[Dog]` → `Box[Animal]` allowed
- `get()` → value provide karta hai (producer)

## 7. Contravariant

```python
T_contra = TypeVar("T_contra", contravariant=True)

class Handler(Generic[T_contra]):
    def handle(self, value: T_contra):
        print(value)
```

**Explanation:**
- `T_contra` → contravariant
- Input/consumer ke liye
- `Handler[Animal]` → `Handler[Dog]` allowed

## 8. Variance Table

| Variance | Role | Direction |
|----------|------|-----------|
| Covariant | Producer/output | Same |
| Contravariant | Consumer/input | Opposite |
| Invariant | Read + write | None |

**Mnemonic:**
```
CO = OUT
CONTRA = IN
INVARIANT = BOTH
```

## 9. `Callable` Variance

```python
from typing import Callable

AnimalHandler = Callable[[Animal], None]
```

**Explanation:**
- `Callable[[Animal], None]` → `Animal` accept karta hai
- Input contravariant, output covariant

## 10. Storage Example

```python
T = TypeVar("T")

class Storage(Generic[T]):
    def get(self) -> T: ...
    def set(self, value: T): ...
```

**Explanation:**
- `T` → invariant
- Read + write dono karta hai
- `Storage[Dog]` → `Storage[Animal]` **nahi**

## 11. HVAC Example

```python
class Equipment: pass
class AHU(Equipment): pass

# Producer (Covariant)
class EquipmentProvider(Generic[T_co]):
    def get(self) -> T_co: ...

# Consumer (Contravariant)
class EquipmentHandler(Generic[T_contra]):
    def handle(self, equipment: T_contra): ...

# Storage (Invariant)
class EquipmentStorage(Generic[T]):
    def get(self) -> T: ...
    def set(self, value: T): ...
```

**Explanation:**
- `EquipmentProvider` → produce karta hai → covariant
- `EquipmentHandler` → consume karta hai → contravariant
- `EquipmentStorage` → read + write → invariant

## 12. Final Cheat Sheet

```
Dog <: Animal

Covariant:      Container[Dog] → Container[Animal]
Contravariant:  Consumer[Animal] → Consumer[Dog]
Invariant:      Container[Dog] X Container[Animal]
```

---

# Lesson 23: Generators, `yield`, `next()`, `yield from`

## 1. Normal vs Generator

```python
def numbers():
    return [1, 2, 3]
```

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

**Explanation:**
- `return [1, 2, 3]` → poori list ek saath
- `yield 1` → ek value, phir pause
- `numbers()` → generator object

## 2. `yield` Flow

```python
def numbers():
    yield 1
    yield 2
    yield 3

g = numbers()
print(next(g))   # 1
print(next(g))   # 2
print(next(g))   # 3
print(next(g))   # StopIteration
```

**Explanation:**
- `yield 1` → value do, pause
- `next(g)` → next value lo
- 4th `next()` → `StopIteration`

## 3. Generator = Iterator

```
Generator → Iterator → Iterable
```

**Explanation:**
- Generator object ke paas `next()` work karta hai
- Isliye iterator protocol follow karta hai

## 4. `for` Loop

```python
for number in numbers():
    print(number)
```

**Output:**
```
1
2
3
```

**Explanation:**
- `for` loop internally `iter()` + `next()` use karta hai

## 5. List vs Generator

```python
numbers = [x for x in range(1_000_000)]   # List
numbers = (x for x in range(1_000_000))   # Generator
```

**Explanation:**
- List → eager, sab memory mein
- Generator → lazy, need par value

## 6. Lazy Evaluation

```python
def numbers():
    print("1 generate")
    yield 1
    print("2 generate")
    yield 2

g = numbers()
print(next(g))
```

**Output:**
```
1 generate
1
```

**Explanation:**
- `g = numbers()` → function body execute nahi hoti
- `next(g)` → pehla `yield` tak execute
- Computation demand par

## 7. State Preserve

```python
def counter():
    print("Start")
    yield 1
    print("Middle")
    yield 2
    print("End")

g = counter()
next(g)   # Start, 1
next(g)   # Middle, 2
```

**Explanation:**
- `yield` ke baad function pause
- Python yaad rakhta hai kahan pause hua

## 8. `yield` vs `return`

```python
def test():
    return 10
    return 20   # unreachable
```

```python
def test():
    yield 10
    yield 20
```

**Explanation:**
- `return` → terminate + value
- `yield` → pause + value

## 9. Generator Expression

```python
numbers = (x * 2 for x in range(10))
for x in numbers:
    print(x)
```

**Output:**
```
0
2
4
6
8
...
```

**Explanation:**
- `( ... )` → generator expression
- `[ ... ]` → list comprehension

## 10. Generator Pipeline

```python
def numbers():
    for i in range(10):
        yield i

def even(numbers):
    for number in numbers:
        if number % 2 == 0:
            yield number

def square(numbers):
    for number in numbers:
        yield number * number

data = square(even(numbers()))
for value in data:
    print(value)
```

**Output:**
```
0
4
16
36
64
```

**Explanation:**
- `numbers()` → 0-9
- `even()` → 0, 2, 4, 6, 8
- `square()` → 0, 4, 16, 36, 64
- Lazy pipeline

## 11. `yield from`

```python
def numbers():
    yield 1
    yield 2
    yield 3

def all_numbers():
    yield from numbers()
```

**Explanation:**
- `yield from numbers()` → numbers ki values one-by-one yield
- Equivalent to `for x in numbers(): yield x`

## 12. Multiple Generators

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

for value in sensor_data():
    print(value)
```

**Output:**
```
22.5
23.0
250
255
```

**Explanation:**
- `yield from temperatures()` → pehle temperatures
- `yield from pressures()` → phir pressures

## 13. `send()`

```python
def receiver():
    value = yield
    print("Received:", value)

g = receiver()
next(g)         # Start
g.send(100)     # Received: 100
```

**Explanation:**
- `value = yield` → value receive karta hai
- `next(g)` → pehle `yield` tak start
- `g.send(100)` → `yield` expression = 100

## 14. Calculator with `send()`

```python
def calculator():
    total = 0
    while True:
        value = yield total
        total += value

calc = calculator()
print(next(calc))      # 0
print(calc.send(10))   # 10
print(calc.send(20))   # 30
print(calc.send(5))    # 35
```

**Explanation:**
- `value = yield total` → total bhejo, value lo
- `next(calc)` → pehla total = 0
- `calc.send(10)` → value = 10, total = 10

## 15. Infinite Generator

```python
def counter():
    number = 0
    while True:
        yield number
        number += 1

g = counter()
next(g)   # 0
next(g)   # 1
next(g)   # 2
```

**Explanation:**
- `while True:` → infinite loop
- `yield number` → value do, pause

## 16. Cheat Sheet

```
yield            → value do + pause
next(generator)  → next value
send(value)      → generator mein value bhejo
yield from       → doosre iterable se values forward
Generator        → lazy iterator
Iterable         → for loop possible
Iterator         → next() possible
```

---

# Lesson 24: `async`, `await`, Coroutine, Event Loop

## 1. Synchronous

```python
import time

def task(name):
    print(name, "start")
    time.sleep(2)
    print(name, "end")

task("A")
task("B")
```

**Output:**
```
A start
A end
B start
B end
```

**Explanation:**
- `time.sleep(2)` → program block
- Task A complete, phir Task B
- Total ~4 seconds

## 2. `async def`

```python
async def task():
    print("Task running")

result = task()
print(result)
```

**Output:**
```
<coroutine object task at 0x...>
```

**Explanation:**
- `async def` → coroutine function
- `task()` → coroutine object return
- Direct execute nahi hota

## 3. Coroutine

```python
async def task():
    print("Start")
    await something()
    print("End")
```

**Explanation:**
- Coroutine → pause aur resume ho sakta hai
- `await` → asynchronous wait

## 4. `asyncio.run()`

```python
import asyncio

async def hello():
    print("Hello")

asyncio.run(hello())
```

**Output:**
```
Hello
```

**Explanation:**
- `asyncio.run()` → event loop setup + run
- `hello()` → coroutine run hui

## 5. `asyncio.sleep()`

```python
import asyncio

async def task():
    print("Start")
    await asyncio.sleep(2)
    print("End")

asyncio.run(task())
```

**Output:**
```
Start
End
```

**Explanation:**
- `await asyncio.sleep(2)` → coroutine pause, event loop free
- `time.sleep(2)` → thread block

## 6. Sequential Async

```python
async def main():
    await task("A")
    await task("B")

asyncio.run(main())
```

**Explanation:**
- Pehle A complete, phir B
- Total ~4 seconds
- `async def` se automatically parallel nahi

## 7. Concurrent with `create_task()`

```python
async def main():
    task1 = asyncio.create_task(task("A"))
    task2 = asyncio.create_task(task("B"))
    await task1
    await task2
```

**Explanation:**
- `create_task()` → task schedule
- Dono concurrently wait
- Total ~2 seconds

## 8. Event Loop

```
Event Loop
    ↓
Task A, Task B, Task C
    ↓
jo ready hai, run karo
```

**Explanation:**
- Event loop tasks manage karta hai
- Task wait kar raha hai → doosra run karo

## 9. CPU vs I/O

```
I/O-bound   → asyncio useful
CPU-bound   → asyncio automatically parallel nahi
```

**Explanation:**
- API calls, network, file I/O → asyncio
- Heavy calculation → threading/multiprocessing

## 10. `asyncio.gather()`

```python
async def main():
    results = await asyncio.gather(
        task("A"),
        task("B"),
        task("C")
    )
    print(results)
```

**Output:**
```
['A done', 'B done', 'C done']
```

**Explanation:**
- `gather()` → multiple coroutines concurrently
- Sab complete hone ka wait

## 11. Coroutine vs Task

```
async def work()  → coroutine function
work()            → coroutine object
create_task(work()) → Task
```

**Explanation:**
- Coroutine → awaitable
- Task → scheduled coroutine

## 12. `async with`

```python
async with resource:
    ...
```

**Explanation:**
- `__aenter__()` / `__aexit__()`
- Async context manager

## 13. `async for`

```python
async for item in items:
    ...
```

**Explanation:**
- `__aiter__()` / `__anext__()`
- `StopAsyncIteration`

## 14. Normal vs Async

```
Normal iteration:  __iter__() + __next__()
Async iteration:   __aiter__() + __anext__()

Normal context:    __enter__() + __exit__()
Async context:     __aenter__() + __aexit__()
```

## 15. Async Generator

```python
async def numbers():
    yield 1
    yield 2

async for number in numbers():
    print(number)
```

**Explanation:**
- `async def + yield` → async generator
- `async for` → iterate

## 16. Final Model

```
asyncio
    ↓
Event Loop
    ↓
Task A, Task B, Task C
    ↓
await → pause
    ↓
Event Loop → next ready task
```

**Key Point:** Asyncio I/O-bound work ke liye hai. Jab ek task wait kar raha ho, event loop doosra run karta hai.

---

# Lesson 25: `Task`, `Future`, Cancellation, Timeout

## 1. `Task`

```python
async def work():
    await asyncio.sleep(2)
    return "Done"

task = asyncio.create_task(work())
```

**Explanation:**
- `work()` → coroutine
- `create_task()` → schedule
- `task` → Task object

## 2. Task Result

```python
async def main():
    task = asyncio.create_task(work())
    result = await task
    print(result)

asyncio.run(main())
```

**Output:**
```
Done
```

**Explanation:**
- `await task` → complete hone tak wait
- `result` → return value

## 3. Task Status

```python
task.done()      # True/False
task.cancelled() # True/False
task.result()    # Result (agar complete)
```

**Explanation:**
- `done()` → complete?
- `cancelled()` → cancel?
- `result()` → value

## 4. `gather()`

```python
results = await asyncio.gather(
    get_temperature("AHU-01"),
    get_temperature("AHU-02"),
    get_temperature("AHU-03")
)
```

**Explanation:**
- Teeno concurrently run
- Results list mein

## 5. Exception Handling

```python
async def main():
    try:
        await work()
    except ValueError as e:
        print("Error:", e)
```

**Explanation:**
- Normal `try/except` async mein bhi
- `await work()` → exception propagate

## 6. Task Exception

```python
async def main():
    task = asyncio.create_task(work())
    try:
        await task
    except ValueError as e:
        print("Error:", e)
```

**Explanation:**
- `await task` → exception caller ko mili

## 7. Cancellation

```python
async def long_task():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Cancelled")

async def main():
    task = asyncio.create_task(long_task())
    await asyncio.sleep(2)
    task.cancel()
    await task
```

**Explanation:**
- `task.cancel()` → cancellation request
- `CancelledError` → task ke andar raise
- `await task` → cancellation complete

## 8. `CancelledError`

```python
try:
    await something()
except asyncio.CancelledError:
    cleanup()
```

**Explanation:**
- Cancellation ke waqt cleanup
- `finally:` bhi use kar sakte hain

## 9. Timeout

```python
try:
    result = await asyncio.wait_for(
        api_call(),
        timeout=5
    )
except asyncio.TimeoutError:
    print("Timeout")
```

**Explanation:**
- `wait_for()` → max time limit
- 5 seconds ke baad cancel

## 10. Modern Timeout

```python
async with asyncio.timeout(5):
    result = await api_call()
```

**Explanation:**
- `asyncio.timeout(5)` → 5 second limit
- `TimeoutError` → timeout par

## 11. `asyncio.sleep()` vs `time.sleep()`

```python
# Wrong
async def work():
    time.sleep(5)   # Blocks event loop

# Correct
async def work():
    await asyncio.sleep(5)   # Pauses coroutine
```

**Explanation:**
- `time.sleep()` → event loop block
- `await asyncio.sleep()` → coroutine pause

## 12. Concurrency vs Parallelism

```
Concurrency  → multiple tasks progress
Parallelism  → multiple CPU cores same time
```

**Explanation:**
- Asyncio → concurrency
- CPU parallelism → multiprocessing

## 13. HVAC Example

```python
async def main():
    results = await asyncio.gather(
        read_point("AHU-01.TEMP"),
        read_point("AHU-02.TEMP"),
        read_point("VAV-01.TEMP")
    )
    for result in results:
        print(result)
```

**Explanation:**
- Teeno points concurrently read
- Results collect

## 14. Task Lifecycle

```
Created → Scheduled → Running → Waiting → Completed
                              ↓
                         Cancelled
```

## 15. Complete Example

```python
import asyncio

async def read_equipment(equipment_id):
    print(f"{equipment_id}: reading...")
    try:
        await asyncio.sleep(2)
        return {"equipment_id": equipment_id, "temperature": 22}
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

**Explanation:**
- `async def` → coroutines
- `await` → async wait
- `gather()` → multiple operations
- `timeout` → max wait
- `CancelledError` → cleanup
- `asyncio.run()` → event loop

## 16. Quick Revision

```
Coroutine      → async def ka result
Task           → scheduled coroutine
Event Loop     → tasks manage
await          → pause + event loop free
gather()       → multiple concurrent
cancel()       → cancellation request
Timeout        → max time
asyncio        → async framework
```

---

# Lesson 26: Async Iterator, Async Generator, `async for`

## 1. Normal Iterator

```python
numbers = [10, 20, 30]
for number in numbers:
    print(number)
```

**Internally:**
```python
iterator = iter(numbers)
while True:
    try:
        number = next(iterator)
        print(number)
    except StopIteration:
        break
```

**Explanation:**
- `iter()` → iterator
- `next()` → value
- `StopIteration` → end

## 2. Async Iterator

```
Async Iterator
    ↓
aiter()
    ↓
anext()
    ↓
StopAsyncIteration
```

## 3. `async for`

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

**Output:**
```
0
1
2
```

**Explanation:**
- `async def + yield` → async generator
- `async for` → iterate
- Har value ke darmiyan async wait

## 4. Normal vs Async Generator

| Normal | Async |
|--------|-------|
| `def` | `async def` |
| `yield` | `yield` |
| `for` | `async for` |
| `next()` | `anext()` |
| `StopIteration` | `StopAsyncIteration` |

## 5. `__aiter__()` / `__anext__()`

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

async def main():
    async for number in AsyncCounter(3):
        print(number)
```

**Output:**
```
0
1
2
```

**Explanation:**
- `__aiter__()` → iterator return
- `__anext__()` → next value (async)
- `StopAsyncIteration` → end

## 6. `anext()`

```python
iterator = AsyncCounter(3)
print(await anext(iterator))   # 0
print(await anext(iterator))   # 1
print(await anext(iterator))   # 2
```

**Explanation:**
- `await anext(iterator)` → next value
- `StopAsyncIteration` → end

## 7. `async for` Internally

```python
async for item in iterator:
    print(item)
```

**Conceptually:**
```python
iterator = aiter(iterator)
while True:
    try:
        item = await anext(iterator)
        print(item)
    except StopAsyncIteration:
        break
```

## 8. HVAC Example

```python
async def read_equipment():
    equipment = ["AHU-01", "AHU-02", "VAV-01"]
    for equipment_id in equipment:
        await asyncio.sleep(1)
        yield {"equipment_id": equipment_id, "temperature": 22}

async def main():
    async for data in read_equipment():
        print(data)
```

**Output:**
```
{'equipment_id': 'AHU-01', 'temperature': 22}
{'equipment_id': 'AHU-02', 'temperature': 22}
{'equipment_id': 'VAV-01', 'temperature': 22}
```

**Explanation:**
- `async def + yield` → async generator
- `async for` → one-by-one process

## 9. Async Pipeline

```python
async def numbers():
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i

async def even_numbers(source):
    async for number in source:
        if number % 2 == 0:
            yield number

async def main():
    async for number in even_numbers(numbers()):
        print(number)
```

**Output:**
```
0
2
4
6
8
```

**Explanation:**
- `numbers()` → async generator
- `even_numbers()` → filter
- `async for` → consume

## 10. Three Types

| Type | Syntax | Use |
|------|--------|-----|
| Generator | `def + yield` | lazy values |
| Coroutine | `async def + return` | async operation |
| Async Generator | `async def + yield` | async stream |

## 11. Common Mistake

```python
data = await numbers()   # Wrong!
```

**Explanation:**
- Async generator ko directly `await` nahi karte
- `async for` use karo

## 12. Complete Architecture

```
asyncio
    ↓
Event Loop
    ↓
Task A, Task B, Task C
    ↓
await
    ↓
Async Generator
    ↓
async for
    ↓
process item
```

## 13. Final Mental Model

```
NORMAL:
Iterable → iter() → Iterator → next() → value → StopIteration

ASYNC:
Async Iterable → aiter() → Async Iterator → await anext() → value → StopAsyncIteration
```

**Key Point:** `async for` asynchronous version of `for` hai: har next value ko `await` karke receive karta hai.

---

# Lesson 27: Decorators — `@decorator`

## 1. Basic Decorator

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@decorator
def hello():
    print("Hello")

hello()
```

**Output:**
```
Before
Hello
After
```

**Explanation:**
- `decorator(func)` → function receive
- `wrapper()` → replacement function
- `@decorator` → `hello = decorator(hello)`

## 2. `@decorator` Conceptually

```python
@decorator
def hello():
    print("Hello")
```

**Equivalent:**
```python
def hello():
    print("Hello")

hello = decorator(hello)
```

**Explanation:**
- `@` magic nahi
- Function ko decorator mein pass kiya

## 3. Function as Object

```python
def hello():
    print("Hello")

x = hello
x()
```

**Output:**
```
Hello
```

**Explanation:**
- Function bhi object
- Variable mein rakh sakte ho

## 4. Function as Argument

```python
def hello():
    print("Hello")

def execute(func):
    func()

execute(hello)
```

**Output:**
```
Hello
```

**Explanation:**
- `execute(hello)` → function pass
- Higher-order function

## 5. Logger Decorator

```python
def logger(func):
    def wrapper():
        print("Running:", func.__name__)
        return func()
    return wrapper

@logger
def check_temperature():
    print("Temperature checked")

check_temperature()
```

**Output:**
```
Running: check_temperature
Temperature checked
```

**Explanation:**
- `func.__name__` → function ka naam
- `return func()` → original function call

## 6. `*args` / `**kwargs`

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def add(a, b):
    return a + b

print(add(10, 20))
```

**Output:**
```
30
```

**Explanation:**
- `*args` → positional arguments
- `**kwargs` → keyword arguments
- `func(*args, **kwargs)` → original call

## 7. `*args`

```python
def wrapper(*args):
    # args = (10, 20)
    func(*args)
    # func(10, 20)
```

## 8. `**kwargs`

```python
def wrapper(**kwargs):
    # kwargs = {"a": 10, "b": 20}
    func(**kwargs)
    # func(a=10, b=20)
```

## 9. Return Value

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("Calling")
        result = func(*args, **kwargs)
        print("Complete")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

result = add(10, 20)
print(result)
```

**Output:**
```
Calling
Complete
30
```

**Explanation:**
- `result = func(...)` → return value save
- `return result` → preserve

## 10. `functools.wraps`

```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Calling:", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

print(add.__name__)   # add
```

**Explanation:**
- `@wraps(func)` → metadata preserve
- `add.__name__` → `"add"` (wrapper nahi)

## 11. Timer Decorator

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def calculate():
    time.sleep(2)
    return 100

result = calculate()
```

**Output:**
```
calculate took 2.0001 seconds
```

**Explanation:**
- `time.perf_counter()` → precise time
- Original function unchanged

## 12. Multiple Decorators

```python
@decorator1
@decorator2
def hello():
    print("Hello")
```

**Equivalent:**
```python
hello = decorator1(decorator2(hello))
```

**Explanation:**
- Bottom decorator pehle
- Phir top

## 13. Decorator with Parameters

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Hello")

hello()
```

**Output:**
```
Hello
Hello
Hello
```

**Explanation:**
- `repeat(3)` → decorator factory
- 3 levels: `repeat` → `decorator` → `wrapper`

## 14. HVAC Example

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

class AHU:
    @log_command
    def start(self):
        print("AHU started")

ahu = AHU()
ahu.start()
```

**Output:**
```
Command: start
AHU started
Command completed
```

**Explanation:**
- `@log_command` → start method wrap
- Logging add ki

## 15. Decorator vs Inheritance

```
Inheritance  → class relationship
Decorator    → function/class enhance
```

## 16. `@property` = Decorator

```python
@property
def salary(self):
    ...
```

**Equivalent:**
```python
salary = property(salary)
```

**Explanation:**
- `@property` bhi decorator
- Function ko property object banata hai

## 17. Golden Mental Model

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

@decorator
def function(...):
    ...
```

**Meaning:**
```
function → decorator(function) → wrapper → function()
```

## 18. Quick Revision

```
Decorator    → function/class wrap
@decorator   → decorator(function)
wrapper      → original function ke around
*args        → positional args
**kwargs     → keyword args
@wraps       → metadata preserve
Factory      → decorator with parameters
```

---

# Lesson 28: Class Decorators + `__call__()`

## 1. `__call__()`

```python
class Employee:
    def __call__(self):
        print("Employee called")

emp = Employee()
emp()
```

**Output:**
```
Employee called
```

**Explanation:**
- `__call__()` → object callable
- `emp()` → `emp.__call__()`

## 2. Mental Model

```
emp()  →  emp.__call__()
```

## 3. `__call__()` with Arguments

```python
class Calculator:
    def __call__(self, a, b):
        return a + b

calc = Calculator()
print(calc(10, 20))
```

**Output:**
```
30
```

**Explanation:**
- `calc(10, 20)` → `calc.__call__(10, 20)`

## 4. State + Callable

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(counter())   # 1
print(counter())   # 2
print(counter())   # 3
```

**Explanation:**
- Object state maintain karta hai
- Har call par `count` badhta hai

## 5. `callable()`

```python
def hello():
    pass

print(callable(hello))   # True

class Test:
    def __call__(self):
        pass

obj = Test()
print(callable(obj))     # True

class Test2:
    pass

obj2 = Test2()
print(callable(obj2))    # False
```

**Explanation:**
- `callable()` → check
- `__call__()` → callable

## 6. Class Decorator

```python
def add_logging(cls):
    cls.logged = True
    return cls

@add_logging
class Employee:
    pass
```

**Equivalent:**
```python
class Employee:
    pass

Employee = add_logging(Employee)
```

**Explanation:**
- `add_logging(cls)` → class receive
- `cls.logged = True` → attribute add
- `return cls` → modified class

## 7. Class Decorator Modifies Class

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

**Output:**
```
ABC
```

**Explanation:**
- `cls.company = "ABC"` → class attribute add
- `emp.company` → accessible

## 8. Equipment Registration

```python
equipment_registry = {}

def register_equipment(cls):
    equipment_registry[cls.__name__] = cls
    return cls

@register_equipment
class AHU:
    pass

@register_equipment
class VAV:
    pass

print(equipment_registry)
```

**Output:**
```
{'AHU': <class '__main__.AHU'>, 'VAV': <class '__main__.VAV'>}
```

**Explanation:**
- `cls.__name__` → class ka naam
- `equipment_registry[name] = cls` → register
- Class create hote hi register

## 9. Class Decorator with Method

```python
def add_status(cls):
    def status(self):
        return f"{self.__class__.__name__} is running"
    cls.status = status
    return cls

@add_status
class AHU:
    pass

ahu = AHU()
print(ahu.status())
```

**Output:**
```
AHU is running
```

**Explanation:**
- `def status(self):` → method define
- `cls.status = status` → class mein add
- `ahu.status()` → method call

## 10. Class Wrapper Decorator

```python
def decorate(cls):
    class Wrapper:
        def __init__(self, *args, **kwargs):
            print("Creating object")
            self.obj = cls(*args, **kwargs)

        def __getattr__(self, name):
            return getattr(self.obj, name)

    return Wrapper

@decorate
class Employee:
    def __init__(self, name):
        self.name = name

emp = Employee("Ali")
print(emp.name)
```

**Output:**
```
Creating object
Ali
```

**Explanation:**
- `class Wrapper:` → replacement class
- `self.obj = cls(*args, **kwargs)` → original object
- `__getattr__` → attribute forward

## 11. `__call__()` + Decorator

```python
class Logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Before")
        result = self.func(*args, **kwargs)
        print("After")
        return result

@Logger
def hello():
    print("Hello")

hello()
```

**Output:**
```
Before
Hello
After
```

**Explanation:**
- `@Logger` → `hello = Logger(hello)`
- `hello()` → `Logger.__call__()`
- `self.func()` → original hello

## 12. Class Decorator with Arguments

```python
class Logger:
    def __init__(self, message):
        self.message = message

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(self.message)
            return func(*args, **kwargs)
        return wrapper

@Logger("Running function")
def hello():
    print("Hello")

hello()
```

**Output:**
```
Running function
Hello
```

**Explanation:**
- `Logger("Running function")` → Logger object
- `__call__(hello)` → decorator
- `wrapper` → returned

## 13. State in Class Decorator

```python
class Counter:
    def __init__(self, func):
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print("Calls:", self.calls)
        return self.func(*args, **kwargs)

@Counter
def hello():
    print("Hello")

hello()
hello()
hello()
```

**Output:**
```
Calls: 1
Hello
Calls: 2
Hello
Calls: 3
Hello
```

**Explanation:**
- `self.calls = 0` → state
- `self.calls += 1` → har call par badhta
- State preserve

## 14. `update_wrapper`

```python
from functools import update_wrapper

class Logger:
    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print("Calling:", self.func.__name__)
        return self.func(*args, **kwargs)
```

**Explanation:**
- `update_wrapper(self, func)` → metadata copy
- `self.func.__name__` → original naam

## 15. HVAC Example

```python
class CommandCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} time(s)")
        return self.func(*args, **kwargs)

class AHU:
    @CommandCounter
    def start(self):
        print("AHU started")

ahu = AHU()
ahu.start()
ahu.start()
```

**Output:**
```
start called 1 time(s)
AHU started
start called 2 time(s)
AHU started
```

**Explanation:**
- `@CommandCounter` → `start = CommandCounter(start)`
- `start()` → `CommandCounter.__call__()`
- `self.count` → state

## 16. Final Mental Model

```
DECORATOR
    ↓
Function Decorator  →  wrapper
Class Decorator     →  class modify/replace
    ↓
Class-based decorator
    ↓
__init__(func)  →  store
__call__()      →  execute
```

**Key Lines:**
```python
@Logger
def hello(): ...
```
= 
```python
hello = Logger(hello)
```

```python
hello()
```
= 
```python
hello.__call__()
```

---

# Lesson 29: Closures + `nonlocal`

## 1. Closure

```python
def outer():
    message = "Hello"

    def inner():
        print(message)

    return inner

func = outer()
func()
```

**Output:**
```
Hello
```

**Explanation:**
- `outer()` → finish ho gaya
- `inner()` → `message` yaad rakha
- Ye closure hai

## 2. Closure Flow

```
outer()
    ↓
message = "Hello"
    ↓
inner create
    ↓
inner return
    ↓
outer finish
    ↓
func() → still remembers message
```

## 3. Closure Parts

```python
def multiplier(x):
    def multiply(value):
        return value * x
    return multiply
```

**Explanation:**
- `x` → outer variable
- `multiply()` → use karta hai
- Closure

## 4. Multiple Closures

```python
double = multiplier(2)
triple = multiplier(3)

print(double(10))   # 20
print(triple(10))   # 30
```

**Explanation:**
- `double` → remembers `x = 2`
- `triple` → remembers `x = 3`
- Independent closures

## 5. Closure + Decorator

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("Calling function")
        return func(*args, **kwargs)
    return wrapper
```

**Explanation:**
- `func` → outer variable
- `wrapper()` → uses `func`
- Closure

## 6. `__closure__`

```python
def outer():
    x = 10

    def inner():
        return x

    return inner

func = outer()
print(func.__closure__)
print(func.__code__.co_freevars)
```

**Output:**
```
(<cell at 0x...>,)
('x',)
```

**Explanation:**
- `__closure__` → closure info
- `co_freevars` → free variable names

## 7. `nonlocal` Problem

```python
def counter():
    count = 0

    def increment():
        count += 1
        return count

    return increment
```

**Error:**
```
UnboundLocalError
```

**Explanation:**
- `count += 1` → Python `count` ko local samajhta hai
- Lekin `count` outer function ka hai
- Isliye error

## 8. `nonlocal` Solution

```python
def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

counter_fn = counter()
print(counter_fn())   # 1
print(counter_fn())   # 2
print(counter_fn())   # 3
```

**Explanation:**
- `nonlocal count` → outer `count` modify
- `count += 1` → outer variable update

## 9. `nonlocal` vs `global`

```python
# nonlocal
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1

# global
x = 10
def change():
    global x
    x += 1
```

**Explanation:**
- `nonlocal` → enclosing function
- `global` → module/global

## 10. Closure as State

```python
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter1 = counter()
counter2 = counter()

print(counter1())   # 1
print(counter1())   # 2
print(counter2())   # 1
print(counter2())   # 2
```

**Explanation:**
- `counter1` → apna `count`
- `counter2` → apna `count`
- Independent state

## 11. Closure vs Class

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
- Closure → function + captured state
- Class → object + attributes + methods

## 12. HVAC Example

```python
def create_reader(equipment_id):
    count = 0

    def read():
        nonlocal count
        count += 1
        print(equipment_id, "reading number:", count)

    return read

ahu_reader = create_reader("AHU-01")
vav_reader = create_reader("VAV-01")

ahu_reader()
ahu_reader()
vav_reader()
```

**Output:**
```
AHU-01 reading number: 1
AHU-01 reading number: 2
VAV-01 reading number: 1
```

**Explanation:**
- `create_reader("AHU-01")` → closure with `equipment_id`
- `count` → state
- Har reader ka apna state

## 13. Configuration Closure

```python
def create_validator(minimum):
    def validate(value):
        return value >= minimum
    return validate

temperature_validator = create_validator(18)
pressure_validator = create_validator(100)

print(temperature_validator(22))   # True
print(temperature_validator(15))   # False
```

**Explanation:**
- `temperature_validator` → remembers `minimum = 18`
- `pressure_validator` → remembers `minimum = 100`

## 14. Decorator with Configuration

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator
```

**Explanation:**
- `repeat(times)` → closure
- `decorator(func)` → closure
- `wrapper()` → `times` + `func` capture

## 15. `nonlocal` Decorator

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

@count_calls
def start_ahu():
    print("AHU started")

start_ahu()
start_ahu()
start_ahu()
```

**Output:**
```
Call: 1
AHU started
Call: 2
AHU started
Call: 3
AHU started
```

**Explanation:**
- `count = 0` → outer variable
- `nonlocal count` → modify
- `count` → calls ke darmiyan preserve

## 16. Closure vs Global

```python
# Bad
count = 0
def increment():
    global count
    count += 1

# Good
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

**Explanation:**
- Global → accessible from anywhere
- Closure → encapsulated state

## 17. Closure + Encapsulation

```python
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

**Explanation:**
- `count` → outer se accessible nahi
- Limited/private-like state

## 18. `nonlocal` vs Mutable Object

```python
# No nonlocal needed
def outer():
    data = []
    def inner():
        data.append(10)   # mutation

# nonlocal needed
def outer():
    data = []
    def inner():
        nonlocal data
        data = [10]       # rebinding
```

**Explanation:**
- Mutation → same object change
- Rebinding → naye object se bind

## 19. Closure Flow

```python
def power(exponent):
    def calculate(number):
        return number ** exponent
    return calculate

square = power(2)
cube = power(3)

print(square(5))   # 25
print(cube(5))     # 125
```

**Explanation:**
- `square` → remembers `exponent = 2`
- `cube` → remembers `exponent = 3`

## 20. Closure + Decorator Connection

```
Nested Function
    ↓
Outer variable capture
    ↓
Closure
    ↓
Decorator wrapper ko state milti hai
```

## 21. Quick Revision

```
Closure     → inner function + captured outer variables
nonlocal    → enclosing function ka variable modify
global      → module/global variable modify
Nested      → function ke andar function
Decorator   → closure ka practical use
Captured    → outer scope variable
```

## 22. Key Example

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
- `counter()` finish ke baad bhi `count` zinda
- `increment()` closure ke through capture

---

# Lesson 30: Scope aur LEGB Rule

## 1. LEGB

```
L → Local
E → Enclosing
G → Global
B → Built-in
```

**Explanation:**
- Python name ko isi order mein search karta hai

## 2. Local Scope

```python
def employee():
    name = "Ali"
    print(name)

employee()
```

**Output:**
```
Ali
```

**Explanation:**
- `name` → `employee()` ka local variable
- Bahar accessible nahi

## 3. Enclosing Scope

```python
def outer():
    x = 10
    def inner():
        print(x)
    inner()

outer()
```

**Output:**
```
10
```

**Explanation:**
- `inner()` mein `x` local nahi
- `outer()` ka `x` → enclosing

## 4. Enclosing Diagram

```
Global
  │
  └── outer()
        │ x = 10
        └── inner()
              │ print(x)
              ↓
           x = 10
```

## 5. Global Scope

```python
x = 100

def test():
    print(x)

test()
```

**Output:**
```
100
```

**Explanation:**
- `x = 100` → global
- `test()` mein `x` nahi mila
- Global se mila

## 6. Built-in Scope

```python
def test():
    print(len([1, 2, 3]))

test()
```

**Output:**
```
3
```

**Explanation:**
- `len` → built-in
- L → E → G → B search

## 7. LEGB Example

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

**Output:**
```
Local
```

**Explanation:**
- `inner()` mein `x` → Local
- Baaki scopes check nahi kiye

## 8. Local Remove

```python
x = "Global"

def outer():
    x = "Enclosing"
    def inner():
        print(x)
    inner()

outer()
```

**Output:**
```
Enclosing
```

**Explanation:**
- Local → nahi
- Enclosing → mil gaya

## 9. Enclosing Remove

```python
x = "Global"

def outer():
    def inner():
        print(x)
    inner()

outer()
```

**Output:**
```
Global
```

**Explanation:**
- Local → nahi
- Enclosing → nahi
- Global → mil gaya

## 10. Name Lookup vs Assignment

```python
x = 10

def test():
    print(x)

test()
```

**Output:**
```
10
```

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
- `x = 20` → new local variable
- Global `x` unchanged

## 11. `global` Keyword

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
- `global x` → global variable modify
- `x = 20` → global update

## 12. `nonlocal`

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
- `nonlocal x` → enclosing `x` modify
- `x = 20` → outer `x` update

## 13. `global` vs `nonlocal`

| Keyword | Target |
|---------|--------|
| Nothing | Local |
| `nonlocal` | Enclosing function |
| `global` | Global/module |

## 14. `UnboundLocalError`

```python
x = 10

def test():
    print(x)
    x = 20

test()
```

**Error:**
```
UnboundLocalError
```

**Explanation:**
- `x = 20` → Python `x` ko local samajhta hai
- `print(x)` → local `x` value-less
- Error

## 15. `global` Solution

```python
x = 10

def test():
    global x
    print(x)
    x = 20

test()
```

**Output:**
```
10
```

**Explanation:**
- `global x` → explicit global
- `print(x)` → global value

## 16. `if` / `for` Scope

```python
if True:
    x = 10

print(x)
```

**Output:**
```
10
```

```python
for i in range(3):
    x = i

print(x)
```

**Output:**
```
2
```

**Explanation:**
- `if` / `for` new scope nahi banate
- Function scope different

## 17. Function Scope

```python
def test():
    x = 10

test()
print(x)
```

**Error:**
```
NameError
```

**Explanation:**
- `def` → new local scope

## 18. Class Scope

```python
class Employee:
    company = "ABC"

    def show(self):
        print(company)   # Error
```

**Explanation:**
- Class scope LEGB ke `E` level par nahi
- `self.company` ya `Employee.company` use karo

## 19. `self` Scope Nahi

```python
class Employee:
    def __init__(self, name):
        self.name = name
```

**Explanation:**
- `self` → local parameter
- `self.name` → object attribute

## 20. Built-in Shadowing

```python
len = 100
print(len([1, 2, 3]))   # Error
```

**Explanation:**
- `len = 100` → global
- LEGB: G → `len = 100`
- Built-in `len()` nahi mila

## 21. Shadowing

```python
x = "Global"

def test():
    x = "Local"
    print(x)

test()
```

**Output:**
```
Local
```

**Explanation:**
- Local `x` ne global `x` shadow kiya

## 22. LEGB + Decorator

```python
def decorator(func):
    message = "Running"

    def wrapper():
        print(message)
        return func()

    return wrapper
```

**Explanation:**
- `message` → enclosing
- `func` → enclosing
- Closure

## 23. LEGB Diagram

```
Built-in
    ↑
Global
    ↑
Enclosing
    ↑
Local
    ↑
current function
```

**Lookup:**
```
L → E → G → B → NameError
```

## 24. Real Example

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

**Output:**
```
HVAC Company
```

**Explanation:**
- Local → `"HVAC Company"`
- Baaki scopes nahi

## 25. Debugging Method

```
NameError: name 'x' is not defined
```

Check:
1. Local mein `x`?
2. Enclosing mein `x`?
3. Global mein `x`?
4. Built-in mein `x`?

## 26. Golden Rules

```
1. Function new local scope
2. Nested function enclosing access
3. Module-level names global
4. L → E → G → B order
5. Assignment → local binding
```

## 27. Final Mental Model

```
Python Name Lookup

x
↓
Local → Enclosing → Global → Built-in → NameError
```

```
global    → Global scope modify
nonlocal  → Enclosing function modify
LEGB      → Search order
```

**Key Point:** Scope batata hai variable kahan accessible hai; LEGB batata hai Python kis order mein scopes check karega.

---

**Ab ye guide complete hai.** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ HVAC examples

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀