Bilkul. Aapki updated sequence ke mutabiq **Lesson 91 se continue** karte hain. Lesson 90 ke baad ab `multiprocessing` ke **advanced shared-data mechanisms** cover karenge.

# Lesson 91 — `multiprocessing`

## `Manager`, Shared Memory, `Value`, `Array`

Lesson 90 mein humne dekha tha:

```text
Process
Pool
Queue
Pipe
```

Ab fundamental problem:

> Processes ki memory separate hoti hai. Agar do processes ko same data share karna ho to kaise karein?

Iske liye important mechanisms:

```text
multiprocessing
│
├── Manager
├── Value
├── Array
└── shared_memory
```

---

# 1. Problem: Process ki memory separate hai

Example:

```python
counter = 0
```

Main process:

```text
Process A
counter = 0
```

Child process:

```text
Process B
counter = 0
```

Dono alag memory spaces hain.

```text
┌──────────────┐       ┌──────────────┐
│ Process A    │       │ Process B    │
│              │       │              │
│ counter = 0  │       │ counter = 0  │
└──────────────┘       └──────────────┘
```

Agar Process B:

```python
counter += 1
```

kare, normally Process A ka `counter` automatically `1` nahi banega.

---

# 2. Is problem ke solutions

Python multiple approaches provide karta hai:

```text
Simple communication
        ↓
Queue / Pipe

Shared higher-level objects
        ↓
Manager

Simple shared primitive
        ↓
Value / Array

High-performance shared memory
        ↓
multiprocessing.shared_memory
```

Ab ek ek karte hain.

---

# 3. `Manager`

Import:

```python
from multiprocessing import Manager
```

Manager ek **server process** provide karta hai jo shared Python objects manage karta hai.

Mental model:

```text
Process A ──┐
            │
Process B ──┼──► Manager
            │
Process C ──┘
```

Manager ke through processes shared objects access kar sakte hain.

---

# 4. Basic Manager example

```python
import multiprocessing


def worker(shared_list):
    shared_list.append("AHU-01")


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:

        shared_list = manager.list()

        p = multiprocessing.Process(
            target=worker,
            args=(shared_list,)
        )

        p.start()
        p.join()

        print(shared_list)
```

Result:

```text
['AHU-01']
```

Yahan child process ne list mein item add kiya aur main process ne usay dekha.

---

# 5. Normal list vs Manager list

Normal:

```python
data = []
```

Process isolation ki wajah se directly share nahi hoti.

Manager:

```python
data = manager.list()
```

shared/proxied object provide karta hai.

Concept:

```text
Normal list
    ↓
Process-local

manager.list()
    ↓
Shared through Manager
```

---

# 6. Manager dictionary

```python
with multiprocessing.Manager() as manager:

    data = manager.dict()

    data["AHU-01"] = 22.5
    data["AHU-02"] = 23.1

    print(data)
```

Output conceptually:

```text
{
    "AHU-01": 22.5,
    "AHU-02": 23.1
}
```

---

# 7. Manager ke common objects

Manager se commonly:

```python
manager.list()
manager.dict()
manager.Namespace()
manager.Lock()
manager.Event()
manager.Queue()
```

jaise shared/proxy objects mil sakte hain.

Yani Manager sirf list ke liye nahi hai.

---

# 8. Manager ka mental model

Important:

> Manager actual object ko directly har process ki memory mein duplicate nahi karta; processes Manager ke managed objects ke saath proxy/IPC ke through interact karte hain.

Conceptually:

```text
Process A
   │
   │ proxy
   ▼
Manager Process
   │
   ▼
Shared Object

Process B
   │
   │ proxy
   └──────────────►
```

Isi wajah se Manager convenient hai, lekin free nahi.

---

# 9. Manager ka disadvantage

Manager convenient hai:

```text
manager.list()
manager.dict()
```

Lekin performance ordinary local Python objects jaisi nahi hoti.

Kyun?

```text
Process
   ↓
IPC / proxy
   ↓
Manager
   ↓
Object
```

Har operation mein communication overhead ho sakta hai.

Isliye:

> **Convenience ke liye Manager; high-performance data sharing ke liye shared memory consider karo.**

---

# 10. `Value`

Ab simple shared variable:

```python
multiprocessing.Value
```

Example:

```python
from multiprocessing import Value
```

Basic:

```python
counter = Value("i", 0)
```

Yahan:

```text
"i"
```

integer type ko represent karta hai.

Aur:

```text
0
```

initial value hai.

---

# 11. `Value` ko access kaise karte hain?

Important:

```python
counter.value
```

Example:

```python
print(counter.value)
```

Update:

```python
counter.value += 1
```

---

# 12. Complete example

```python
import multiprocessing


def worker(counter):
    counter.value += 1


if __name__ == "__main__":
    counter = multiprocessing.Value("i", 0)

    p = multiprocessing.Process(
        target=worker,
        args=(counter,)
    )

    p.start()
    p.join()

    print(counter.value)
```

Output:

```text
1
```

Yahan child process ne shared value modify ki.

---

# 13. `Value` ka mental model

```text
Process A
    │
    ├── counter.value
    │
    ▼
 Shared Memory
    ▲
    │
    └── Process B
```

Ye Manager se fundamentally different approach hai.

```text
Manager
→ proxy / managed object

Value
→ shared memory primitive
```

---

# 14. `Value` mein lock

`Value` synchronization support kar sakta hai.

Example:

```python
counter = multiprocessing.Value(
    "i",
    0,
    lock=True
)
```

Default behavior mein synchronization support available hota hai.

Lekin ye samajhna important hai:

```python
counter.value += 1
```

ek compound read-modify-write operation hai.

Multiple processes simultaneously update kar rahe hon to synchronization ko correctly design karna zaroori hai.

---

# 15. Explicit lock

```python
import multiprocessing


def worker(counter, lock):

    for _ in range(1000):
        with lock:
            counter.value += 1


if __name__ == "__main__":

    counter = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    processes = []

    for _ in range(4):
        p = multiprocessing.Process(
            target=worker,
            args=(counter, lock)
        )

        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(counter.value)
```

Expected:

```text
4000
```

Concept:

```text
Process 1 ──┐
Process 2 ──┤
Process 3 ──┼──► Lock ──► counter
Process 4 ──┘
```

---

# 16. `Array`

Agar ek value nahi, multiple primitive values share karne hain:

```python
multiprocessing.Array
```

Example:

```python
numbers = multiprocessing.Array(
    "i",
    [1, 2, 3, 4]
)
```

Concept:

```text
Shared Array

[1][2][3][4]
```

---

# 17. Array access

```python
print(numbers[0])
print(numbers[1])
```

Update:

```python
numbers[0] = 100
```

Result:

```text
[100, 2, 3, 4]
```

---

# 18. Complete Array example

```python
import multiprocessing


def worker(numbers):
    numbers[0] = 100


if __name__ == "__main__":

    numbers = multiprocessing.Array(
        "i",
        [1, 2, 3]
    )

    p = multiprocessing.Process(
        target=worker,
        args=(numbers,)
    )

    p.start()
    p.join()

    print(list(numbers))
```

Result:

```text
[100, 2, 3]
```

---

# 19. `Value` vs `Array`

Simple:

```text
Value
 ↓
one shared value

Array
 ↓
multiple shared values
```

Example:

```python
Value("i", 10)
```

vs

```python
Array("i", [10, 20, 30])
```

---

# 20. Type codes

`Value` aur `Array` mein type code use hota hai.

Examples:

```text
'i' → integer
'd' → double/float
'f' → float
'b' → signed char
```

Example:

```python
temperature = multiprocessing.Value(
    "d",
    22.5
)
```

Yahan:

```text
"d"
```

floating-point value ke liye use ho raha hai.

---

# 21. HVAC example — shared temperature

Suppose ek process sensor read kar raha hai:

```python
temperature = multiprocessing.Value(
    "d",
    22.0
)
```

Sensor process:

```python
temperature.value = 23.5
```

Monitoring process:

```python
print(temperature.value)
```

Concept:

```text
Sensor Process
      │
      ▼
Shared Value
23.5
      ▲
      │
Monitoring Process
```

Simple scalar data ke liye ye useful ho sakta hai.

---

# 22. Manager vs Value vs Array

| Mechanism          | Data                      |
| ------------------ | ------------------------- |
| `Manager().list()` | Python list               |
| `Manager().dict()` | Python dictionary         |
| `Value`            | Single primitive value    |
| `Array`            | Array of primitive values |

Aur performance perspective:

```text
Convenience
Manager
   ↓
Value / Array
   ↓
Shared Memory
Performance-oriented
```

Ye exact performance benchmark nahi, balki architectural intuition hai.

---

# 23. `shared_memory`

Ab advanced mechanism:

```python
from multiprocessing import shared_memory
```

Ye actual shared memory block create/access karne ke liye use ho sakta hai.

Mental model:

```text
Process A ───────┐
                 │
                 ▼
          Shared Memory
                 ▲
                 │
Process B ───────┘
```

Dono processes same memory region access kar sakte hain.

---

# 24. Shared memory kyun?

Suppose tumhare paas huge numeric data hai:

```text
Millions of values
```

Agar repeatedly:

```text
Process A
   ↓
serialize
   ↓
copy
   ↓
Process B
```

karna pade to overhead significant ho sakta hai.

Shared memory:

```text
Process A
   ↘
    Shared Memory
   ↗
Process B
```

data copying reduce karne ka mechanism provide karti hai.

---

# 25. Basic `shared_memory` example

```python
from multiprocessing import shared_memory


shm = shared_memory.SharedMemory(
    create=True,
    size=1024
)
```

Ab:

```text
1024 bytes
```

ka shared memory block create hua.

Memory name:

```python
print(shm.name)
```

---

# 26. Memory ko access karna

Shared memory ka buffer:

```python
shm.buf
```

provide karta hai.

Example:

```python
shm.buf[0] = 100
```

Read:

```python
print(shm.buf[0])
```

Yahan `buf` memory buffer interface provide karta hai.

---

# 27. Shared memory ko close karna

Jab process ka use finish:

```python
shm.close()
```

Aur jab shared memory block ko destroy karna ho:

```python
shm.unlink()
```

Concept:

```text
close()
→ current process ka handle close

unlink()
→ shared memory object ko remove
```

Cleanup bohat important hai.

---

# 28. Shared memory between processes

Process A:

```text
create shared memory
      ↓
write data
```

Process B:

```text
find shared memory by name
      ↓
attach
      ↓
read/write
```

Example conceptual:

```python
existing = shared_memory.SharedMemory(
    name=shm.name
)
```

---

# 29. Important: shared memory automatically synchronization nahi deti

Ye critical point hai.

Shared memory:

```text
shared data
```

provide karti hai.

Lekin:

```text
shared memory ≠ synchronization
```

Agar:

```text
Process A → write
Process B → read
```

simultaneously ho rahe hain, to synchronization design required ho sakta hai.

Possible tools:

```text
Lock
Semaphore
Event
Condition
```

---

# 30. Shared Memory + NumPy

High-performance numerical applications mein shared memory ko NumPy arrays ke saath combine kiya ja sakta hai.

Concept:

```text
Shared Memory
      ↓
NumPy ndarray
      ↓
Process A / Process B
```

Iska faida large numeric datasets ko processes ke darmiyan efficiently share karna ho sakta hai.

---

# 31. Manager vs Shared Memory

### Manager

```text
Python objects
list
dict
namespace
```

easy interface.

### Shared Memory

```text
raw memory
buffer
numeric data
```

zyada low-level aur performance-oriented.

Mental model:

```text
Manager
→ "Mujhe Python object share karna hai."

Shared Memory
→ "Mujhe memory region share karni hai."
```

---

# 32. Ek important architecture

Suppose tumhare paas:

```text
100 MB sensor dataset
```

aur CPU-heavy analysis:

```text
Process 1
Process 2
Process 3
Process 4
```

Agar har process ko complete dataset ki separate copy bhejo:

```text
100 MB × 4
```

potentially huge memory/copy overhead.

Shared memory architecture:

```text
              Shared Memory
             100 MB dataset
              /    |    \
             /     |     \
           P1      P2     P3
```

Processes same underlying memory region access kar sakte hain.

---

# 33. Lekin shared memory dangerous bhi ho sakti hai

Agar Process A:

```text
write index 10
```

aur Process B same waqt:

```text
read index 10
```

kar raha hai, synchronization issue aa sakta hai.

Isliye:

```text
Performance
   +
Correct synchronization
```

dono required hain.

---

# 34. Four mechanisms ka master comparison

| Mechanism       | Best for                        | Abstraction |
| --------------- | ------------------------------- | ----------- |
| `Manager`       | Python list/dict/object sharing | High        |
| `Value`         | Single primitive value          | Medium      |
| `Array`         | Primitive array                 | Medium      |
| `shared_memory` | High-performance shared memory  | Low         |

---

# 35. `Queue` ko bhi include karo

Ab multiprocessing communication ka complete map:

```text
                     multiprocessing
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
     Message            Shared              Direct
     Passing             Data             Communication
        │                  │                  │
      Queue       ┌────────┼────────┐        Pipe
                  ▼        ▼        ▼
               Manager  Value     Array
                            │
                            ▼
                     shared_memory
```

---

# 36. Kab kya use karna hai?

### Case 1 — Task bhejna hai

```text
Queue
```

### Case 2 — Do processes ko direct message exchange karna hai

```text
Pipe
```

### Case 3 — Shared dictionary/list chahiye

```text
Manager
```

### Case 4 — Ek simple counter/value share karna hai

```text
Value
```

### Case 5 — Simple numeric array share karna hai

```text
Array
```

### Case 6 — Large/high-performance memory sharing

```text
shared_memory
```

---

# 37. Threading se comparison

Lesson 87 mein:

```python
threading.Lock()
threading.Event()
queue.Queue()
```

use kiye.

Multiprocessing mein corresponding process-safe mechanisms bhi available hain:

```python
multiprocessing.Lock()
multiprocessing.Event()
multiprocessing.Queue()
```

Lekin ye assume nahi karna chahiye ke har `threading` object process-shared communication ke liye automatically suitable hai.

---

# 38. Sabse important conceptual difference

```text
Threading
─────────
Shared memory naturally available
       ↓
Synchronization required


Multiprocessing
───────────────
Memory isolated
       ↓
IPC / shared-memory mechanism required
```

Isliye multiprocessing architecture mein:

```text
communication
+
synchronization
```

explicitly design karna bohat important hai.

---

# 39. Lesson 91 ka final mental model

```text
Process
   │
   ├── Need to send tasks?
   │       ↓
   │      Queue
   │
   ├── Need direct communication?
   │       ↓
   │      Pipe
   │
   ├── Need Python objects?
   │       ↓
   │      Manager
   │
   ├── Need one primitive?
   │       ↓
   │      Value
   │
   ├── Need primitive array?
   │       ↓
   │      Array
   │
   └── Need high-performance shared memory?
           ↓
       shared_memory
```

### Ek line mein:

> **`Manager` convenience deta hai, `Value`/`Array` simple shared primitives dete hain, aur `shared_memory` low-level/high-performance memory sharing ke liye hai.**

---

## Aapki updated series

Ab sequence exactly ye hai:

```text
91 → multiprocessing: Manager, Shared Memory, Value, Array
92 → concurrent.futures
93 → GIL Deep Understanding
94 → GIL Bypass Techniques
95 → asyncio synchronization
96 → TaskGroup / Structured Concurrency
97 → timeout / wait_for / shield
98 → Async Context Managers + Iterators
99 → asyncio + threads/processes
100 → anyio
```

**Next: Lesson 92 — `concurrent.futures`: `ThreadPoolExecutor` + `ProcessPoolExecutor`**, jahan hum `submit()`, `Future`, `result()`, `map()`, `as_completed()`, exception handling aur ThreadPool vs ProcessPool ko deeply connect karenge.
# Lesson 92 — `concurrent.futures`

## `ThreadPoolExecutor` + `ProcessPoolExecutor`

Ab hum `threading` aur `multiprocessing` ko **higher-level aur easy API** se use karna seekhenge.

Pehle hum manually karte thay:

```python
threading.Thread(...)
multiprocessing.Process(...)
```

`concurrent.futures` mein Python humein **Executor + Future** ka concept deta hai.

---

# 1. `concurrent.futures` kya hai?

Iska basic idea:

```text
Aap tasks do
     ↓
Executor
     ↓
Worker Threads / Processes
     ↓
Future
     ↓
Result
```

Do main executors hain:

```python
ThreadPoolExecutor
ProcessPoolExecutor
```

### ThreadPoolExecutor

```text
Executor
   ↓
Threads
   ↓
I/O-bound work
```

Example:

* API calls
* Database queries
* Files read/write
* Network requests
* BMS/HVAC data read

---

### ProcessPoolExecutor

```text
Executor
   ↓
Processes
   ↓
CPU-bound work
```

Example:

* Heavy calculations
* Large data processing
* Image processing
* Mathematical computation

---

# 2. Executor kya hota hai?

Executor basically **worker management system** hai.

Aapko manually yeh nahi karna:

```python
Thread(...)
start()
join()
```

Ya:

```python
Process(...)
start()
join()
```

Executor khud workers manage karta hai.

Example:

```python
from concurrent.futures import ThreadPoolExecutor
```

Phir:

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    ...
```

Matlab:

> Maximum 4 worker threads available hain.

---

# 3. Sabse simple example

```python
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    return x * 2


with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(worker, [1, 2, 3, 4])

    print(list(results))
```

Output:

```text
[2, 4, 6, 8]
```

Yahan:

```python
executor.map(...)
```

ne multiple inputs ko worker function mein bheja.

---

# 4. `map()` ka concept

Suppose:

```python
items = [1, 2, 3, 4, 5]
```

Aur:

```python
def worker(x):
    return x * 10
```

Agar:

```python
results = executor.map(worker, items)
```

to conceptually:

```text
1 → worker → 10
2 → worker → 20
3 → worker → 30
4 → worker → 40
5 → worker → 50
```

Result:

```python
[10, 20, 30, 40, 50]
```

---

# 5. `submit()` — ek individual task

Ab doosra important method:

```python
executor.submit()
```

Example:

```python
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    return x * 2


with ThreadPoolExecutor(max_workers=4) as executor:

    future = executor.submit(worker, 10)

    print(future)
```

Yahan:

```python
future
```

result nahi hai.

Ye **Future object** hai.

---

# 6. Future kya hota hai?

Future ko simple language mein samjho:

> **Future = "result abhi available nahi, lekin baad mein milega."**

Example:

```python
future = executor.submit(worker, 10)
```

Concept:

```text
submit()
   ↓
Task worker ko diya
   ↓
Future object mila
   ↓
worker kaam karega
   ↓
result ready
   ↓
future.result()
```

Isliye:

```python
result = future.result()
```

---

# 7. `future.result()`

```python
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    return x * 2


with ThreadPoolExecutor(max_workers=4) as executor:

    future = executor.submit(worker, 10)

    result = future.result()

    print(result)
```

Output:

```text
20
```

Important:

```python
future
```

aur:

```python
future.result()
```

same cheez nahi hain.

```text
Future
  ↓
eventual result ka container/reference

result()
  ↓
actual result
```

---

# 8. Future ke important methods

Future ke kuch important methods:

```python
future.result()
future.done()
future.running()
future.cancel()
future.exception()
```

---

## `done()`

Check karta hai task complete hua ya nahi.

```python
if future.done():
    print("Task complete")
```

---

## `running()`

Check:

```python
if future.running():
    print("Task abhi run ho raha hai")
```

---

## `cancel()`

Task ko cancel karne ki koshish:

```python
future.cancel()
```

Lekin important rule:

> Agar task already running hai to normally `cancel()` usay stop nahi karta.

Example:

```text
PENDING
   ↓
RUNNING
   ↓
FINISHED
```

Agar:

```text
PENDING
```

hai:

```python
future.cancel()
```

possible hai.

Lekin:

```text
RUNNING
```

ho gaya to cancellation normally fail ho jayegi.

---

# 9. Future lifecycle

Isko yaad rakho:

```text
PENDING
   ↓
RUNNING
   ↓
FINISHED
```

Ya:

```text
PENDING
   ↓
CANCELLED
```

Visual:

```text
             ┌──→ FINISHED
PENDING → RUNNING
   │
   └──────→ CANCELLED
```

---

# 10. `submit()` vs `map()`

Ye bohat important comparison hai.

| `submit()`                        | `map()`                     |
| --------------------------------- | --------------------------- |
| Individual task                   | Multiple tasks              |
| Future return karta hai           | Results ka iterator         |
| Flexible                          | Simple                      |
| Callback laga sakte hain          | Less flexible               |
| `as_completed()` ke saath useful  | Ordered results             |
| Different arguments easily handle | Same function over iterable |

### `submit`

```python
future = executor.submit(worker, 10)
```

### `map`

```python
results = executor.map(worker, [10, 20, 30])
```

Simple rule:

> **Ek task / custom control → `submit()`**

> **Bohat saare similar tasks → `map()`**

---

# 11. `as_completed()` — result jo pehle complete ho

Ye bohat powerful hai.

Suppose:

```text
Task A → 5 sec
Task B → 1 sec
Task C → 3 sec
```

Agar input order:

```text
A
B
C
```

hai.

`map()` results ko input order mein deta hai.

Lekin:

```python
as_completed()
```

completion order deta hai:

```text
B → C → A
```

Example:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def worker(x):
    return x * 2


with ThreadPoolExecutor(max_workers=3) as executor:

    futures = [
        executor.submit(worker, x)
        for x in [10, 20, 30]
    ]

    for future in as_completed(futures):
        print(future.result())
```

Yahan:

```python
as_completed(futures)
```

ka matlab:

> Jo Future pehle complete ho, uska result pehle process karo.

---

# 12. `map()` vs `as_completed()`

Example:

```text
Task 1 = 5 sec
Task 2 = 1 sec
Task 3 = 3 sec
```

### `map()`

Input:

```text
1 → 2 → 3
```

Result consumption:

```text
Task 1
Task 2
Task 3
```

Agar Task 1 slow hai to Task 2 ka ready result bhi practically wait kar sakta hai because results are presented in input order.

---

### `as_completed()`

```text
Task 2 → result
Task 3 → result
Task 1 → result
```

Isliye:

> **Fast result immediately process karna ho → `as_completed()`**

---

# 13. Exception handling

Suppose worker mein error hai:

```python
def worker(x):
    if x == 0:
        raise ValueError("Zero allowed nahi")

    return 100 / x
```

Ab:

```python
future = executor.submit(worker, 0)
```

Error immediately normal `submit()` call par necessarily nahi milta.

Error Future ke andar capture ho sakta hai.

Jab:

```python
future.result()
```

karoge to exception raise hoti hai.

Example:

```python
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    if x == 0:
        raise ValueError("Zero allowed nahi")

    return 100 / x


with ThreadPoolExecutor() as executor:

    future = executor.submit(worker, 0)

    try:
        result = future.result()
        print(result)

    except Exception as e:
        print("Error:", e)
```

Output:

```text
Error: Zero allowed nahi
```

Important mental model:

```text
worker()
   ↓
exception
   ↓
Future mein store
   ↓
future.result()
   ↓
exception dobara raise
```

---

# 14. Callback

Future ke complete hone ke baad callback execute karwa sakte ho.

```python
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    return x * 2


def callback(future):
    print("Result:", future.result())


with ThreadPoolExecutor() as executor:

    future = executor.submit(worker, 10)

    future.add_done_callback(callback)
```

Concept:

```text
submit()
   ↓
worker
   ↓
complete
   ↓
callback()
```

Callback mein `future.result()` se result le sakte hain.

Callback ko generally **lightweight** rakhna better hai.

---

# 15. `ThreadPoolExecutor`

Ab actual important distinction.

```python
from concurrent.futures import ThreadPoolExecutor
```

Example:

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    ...
```

Ye:

```text
5 worker threads
```

tak tasks execute kar sakta hai.

---

# 16. ThreadPool kis kaam ke liye?

Mostly:

```text
I/O-bound
```

Example:

```text
Thread 1 → API
Thread 2 → Database
Thread 3 → File
Thread 4 → Network
Thread 5 → API
```

Jab ek thread wait kar raha hai:

```text
API response...
```

doosra thread kaam kar sakta hai.

Isliye I/O workloads mein useful hai.

---

# 17. HVAC example

Suppose aapko 20 AHU ke data read karne hain:

```text
AHU-01
AHU-02
AHU-03
...
AHU-20
```

Har AHU ke liye:

```text
Temperature
Pressure
Fan Status
Airflow
Damper Position
```

Agar har request network/BMS/API se aa rahi hai, to:

```python
ThreadPoolExecutor
```

useful ho sakta hai.

Concept:

```text
             Executor
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
     AHU-01   AHU-02   AHU-03
       ↓        ↓        ↓
      API      API      API
```

Ye real-world I/O-bound use case hai.

---

# 18. `ProcessPoolExecutor`

Ab:

```python
from concurrent.futures import ProcessPoolExecutor
```

Example:

```python
from concurrent.futures import ProcessPoolExecutor


def cpu_task(x):
    return x * x


if __name__ == "__main__":

    with ProcessPoolExecutor() as executor:

        results = executor.map(
            cpu_task,
            [1, 2, 3, 4, 5]
        )

        print(list(results))
```

Output:

```text
[1, 4, 9, 16, 25]
```

---

# 19. ProcessPool kyun?

`ProcessPoolExecutor` multiple **processes** use karta hai.

```text
Main Process
    │
    ├── Process 1
    ├── Process 2
    ├── Process 3
    └── Process 4
```

Har process ki memory independent hoti hai.

Aur CPython ke normal GIL behavior ki wajah se CPU-bound pure-Python tasks ke liye multiple processes useful ho sakte hain.

---

# 20. ThreadPool vs ProcessPool

Sabse important table:

| Feature              | ThreadPoolExecutor                                | ProcessPoolExecutor                                      |
| -------------------- | ------------------------------------------------- | -------------------------------------------------------- |
| Worker               | Thread                                            | Process                                                  |
| Memory               | Shared process memory                             | Separate memory                                          |
| Best                 | I/O-bound                                         | CPU-bound                                                |
| GIL                  | Relevant                                          | Processes provide parallelism across interpreters        |
| Startup overhead     | Low                                               | Higher                                                   |
| Communication        | Shared memory + synchronization                   | IPC / serialization                                      |
| Shared mutable state | Lock etc.                                         | Explicit mechanisms                                      |
| Pickling             | Usually not the same constraint for task dispatch | Functions/args/results generally pickleable hone chahiye |

Simple:

```text
I/O → ThreadPool
CPU → ProcessPool
```

---

# 21. ProcessPool mein Windows ka important rule

Aap Windows use karte ho, isliye ye particularly important hai.

Use:

```python
if __name__ == "__main__":
```

Example:

```python
from concurrent.futures import ProcessPoolExecutor


def worker(x):
    return x * x


if __name__ == "__main__":

    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(worker, [1, 2, 3, 4])
        )

    print(results)
```

Is guard ko ignore karna Windows multiprocessing mein problems create kar sakta hai.

---

# 22. ProcessPool mein function kahan hona chahiye?

Generally worker function ko module level par define karna best hai:

```python
def worker(x):
    return x * x
```

Instead of unnecessarily nested/local functions.

Reason:

```text
Process
   ↓
task/function transfer
   ↓
serialization/pickling
```

Isliye ProcessPool mein:

* function pickleable hona chahiye
* arguments generally pickleable hone chahiye
* returned result generally pickleable hona chahiye

---

# 23. `shutdown()`

Executor ko manually close bhi kar sakte hain:

```python
executor.shutdown()
```

Conceptually:

```python
executor.shutdown(
    wait=True,
    cancel_futures=False
)
```

### `wait=True`

Existing tasks complete hone ka wait karega.

### `cancel_futures=True`

Jo pending futures abhi start nahi hue, unko cancel karne ki request karega.

Lekin jo already running hain unko forcibly stop karna iska purpose nahi hai.

---

# 24. `with` kyun better hai?

Instead of:

```python
executor = ThreadPoolExecutor()

# work

executor.shutdown()
```

use:

```python
with ThreadPoolExecutor() as executor:
    # work
```

Context manager automatically cleanup/shutdown handle karta hai.

Ye safer aur cleaner hai.

---

# 25. Complete architecture

Ab poora concept ek diagram mein:

```text
              concurrent.futures
                      │
                 Executor
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
 ThreadPoolExecutor       ProcessPoolExecutor
          ↓                       ↓
       Threads                 Processes
          ↓                       ↓
      I/O-bound              CPU-bound
          │                       │
          └───────────┬───────────┘
                      ↓
                    Future
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   result()       callback()   as_completed()
```

---

# 26. Ek important mental model

Isko strongly yaad rakho:

### `Executor`

> **Kaun kaam karega?**

### `submit()`

> **Ye task karo.**

### `Future`

> **Is task ka result baad mein milega.**

### `result()`

> **Mujhe result do.**

### `map()`

> **Ye function bohat saare inputs par chalao.**

### `as_completed()`

> **Jo pehle complete ho, uska result pehle do.**

---

# 27. Threading se difference

Humne Lesson 87 mein manually kiya:

```python
thread = Thread(target=worker)
thread.start()
thread.join()
```

Ab:

```python
with ThreadPoolExecutor() as executor:
    future = executor.submit(worker)
    result = future.result()
```

`concurrent.futures` ka goal hai:

> **Thread/process management ko high-level aur convenient banana.**

Aapko har worker ko manually create/manage karne ki zarurat kam ho jati hai.

---

# 28. `threading` → `ThreadPoolExecutor`

Concept:

```text
Manual:

Thread
Thread
Thread
Thread
join()
join()
join()
join()
```

vs

```text
High-level:

ThreadPoolExecutor
       ↓
submit/map
       ↓
Future
       ↓
result
```

---

# 29. `multiprocessing` → `ProcessPoolExecutor`

Manual:

```python
Process(...)
Process(...)
Process(...)
```

High-level:

```python
ProcessPoolExecutor()
```

Aur:

```python
executor.map(...)
```

ya:

```python
executor.submit(...)
```

---

# 30. `asyncio` se relation

Aage hum `asyncio` padhenge.

Abhi basic distinction:

```text
ThreadPoolExecutor
        ↓
Threads

ProcessPoolExecutor
        ↓
Processes

asyncio
        ↓
Event Loop + Tasks
```

`concurrent.futures` mainly **worker pools** ko easy banata hai.

`asyncio` ka model different hai: cooperative asynchronous execution through an event loop.

Aage Lesson 95 onward mein hum:

```text
asyncio.Queue
asyncio.Lock
asyncio.Event
asyncio.Condition
asyncio.Semaphore
```

detail mein dekhenge.

---

# 31. Final short memory

```text
Executor
   ↓
worker pool manage karta hai

submit()
   ↓
single task

map()
   ↓
many similar tasks

Future
   ↓
future result ka handle

result()
   ↓
actual result

as_completed()
   ↓
completion order

ThreadPoolExecutor
   ↓
I/O-bound

ProcessPoolExecutor
   ↓
CPU-bound
```

**Next Lesson 93:** `GIL (Global Interpreter Lock) — Deep Understanding` — hum detail mein dekhenge ke GIL exactly kya lock karta hai, thread CPU-bound Python ko parallel kyun nahi chala pata, aur ProcessPool is problem ko kaise bypass karta hai.
# Lesson 93 — GIL (Global Interpreter Lock) — Deep Understanding

Ab hum Python concurrency ka **sabse important aur commonly misunderstood concept** samjhenge:

> **GIL = Global Interpreter Lock**

Agar aap `threading`, `multiprocessing`, `ThreadPoolExecutor`, aur `ProcessPoolExecutor` ko properly samajhna chahte hain, to GIL clear hona zaroori hai.

---

## 1. Sabse pehle: GIL kya hai?

CPython mein GIL ek mechanism hai jo ek process ke andar Python interpreter ke **Python bytecode execution** ko synchronize karta hai.

Simple mental model:

```text
1 CPython Process
       │
       ├── Thread 1
       ├── Thread 2
       ├── Thread 3
       └── Thread 4
       
       ↓

Python bytecode
       ↓
    GIL
       ↓
At a given moment, normally
one thread executes Python bytecode
```

Iska matlab ye **nahi** hai ke:

> Python mein ek waqt mein sirf ek thread exist kar sakta hai.

Bilkul nahi.

Bohat saare threads simultaneously **exist aur runnable** ho sakte hain.

Issue ye hai ke normal CPython execution mein ek waqt mein ek thread hi Python bytecode execute karta hai.

---

# 2. CPU mein 4 cores hon to?

Suppose computer:

```text
CPU
├── Core 1
├── Core 2
├── Core 3
└── Core 4
```

Aur Python program:

```text
Thread 1
Thread 2
Thread 3
Thread 4
```

Aap naturally sochoge:

```text
Core 1 → Thread 1
Core 2 → Thread 2
Core 3 → Thread 3
Core 4 → Thread 4
```

Pure Python CPU-bound code ke case mein normal CPython GIL is straightforward multi-core execution ko prevent karta hai.

Mental model:

```text
Core 1 → Thread 1 → Python bytecode
Core 2 → waiting / other work
Core 3 → waiting / other work
Core 4 → waiting / other work
```

Lekin ek important correction:

**GIL ka matlab ye nahi ke baqi CPU cores hamesha completely idle rahenge.** Native libraries, OS work, I/O, extensions etc. CPU use kar sakte hain. GIL specifically Python interpreter ke protected execution ko affect karta hai.

---

# 3. CPU-bound example

Suppose:

```python
def calculate():
    total = 0

    for i in range(100_000_000):
        total += i

    return total
```

Ye CPU-bound workload hai.

Agar aap multiple threads use karo:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(calculate)
        for _ in range(4)
    ]

    results = [f.result() for f in futures]
```

Aapke paas 4 threads hain:

```text
Thread 1 ─┐
Thread 2 ─┤
Thread 3 ─┼──→ GIL → Python bytecode
Thread 4 ─┘
```

Ye normally 4 Python CPU tasks ko 4 cores par simultaneously execute nahi karega.

---

# 4. To threads useless hain?

**Bilkul nahi.**

Ye bohat important point hai.

GIL ka matlab:

> Threading useless hai

**galat hai.**

Threading especially **I/O-bound workloads** ke liye bohat useful hai.

Example:

```text
Thread 1 → API request → WAIT
Thread 2 → Database → WAIT
Thread 3 → File → WAIT
Thread 4 → Network → WAIT
```

Jab Thread 1 network response ka wait kar raha hai, doosra thread execute kar sakta hai.

---

# 5. I/O-bound example

Suppose:

```python
def get_data():
    response = requests.get(...)
    return response.json()
```

Yahan CPU continuously calculation nahi kar raha.

Mostly:

```text
Python
 ↓
Network request
 ↓
WAIT
```

Is waiting period mein doosre threads useful work kar sakte hain.

Concept:

```text
Thread 1
  ↓
Network
  ↓
WAIT
       ↘
Thread 2 → Python work
       ↘
Thread 3 → Python work
       ↘
Thread 4 → Python work
```

Isi wajah se:

```python
ThreadPoolExecutor
```

I/O-bound applications mein powerful hai.

---

# 6. GIL vs CPU core

Ye distinction yaad rakho:

### CPU core

Hardware resource hai.

```text
Core 1
Core 2
Core 3
Core 4
```

### Thread

Execution path hai.

```text
Thread 1
Thread 2
Thread 3
Thread 4
```

### GIL

CPython interpreter ke Python-bytecode execution ko synchronize karta hai.

```text
Threads
   ↓
GIL
   ↓
Python bytecode execution
```

GIL **CPU hardware lock nahi hai**.

---

# 7. GIL ek `threading.Lock` jaisa hai?

Conceptually kuch similarity hai, lekin exactly same cheez nahi.

Normal lock:

```python
lock = threading.Lock()

with lock:
    # critical section
```

Aap explicitly lock acquire/release karte ho.

GIL interpreter implementation ka internal synchronization mechanism hai.

Aap normally:

```python
gil.acquire()
```

nahi karte.

---

# 8. GIL ka main reason kya tha?

Historically CPython ka object model aur memory management thread-safety ko simple rakhne ke liye GIL ne important role play kiya.

Particularly:

```text
Python objects
reference counting
interpreter internals
C extensions
```

ko synchronize karna easier tha.

Isliye GIL CPython architecture ka historically important part raha.

---

# 9. Reference counting connection

Python objects ke liye CPython historically reference counting use karta hai.

Conceptually:

```python
a = object()
```

Object ke saath reference count maintain hota hai.

Agar:

```text
Thread 1 → object
Thread 2 → object
```

aur dono reference count ko simultaneously modify karen:

```text
Thread 1 → refcount +1
Thread 2 → refcount +1
```

to synchronization zaroori hai.

Agar synchronization incorrect ho:

```text
Race condition
```

ho sakti hai.

GIL historically CPython interpreter internals ke is class of concurrency concerns ko simpler banane mein important raha.

---

# 10. Lekin GIL ka matlab Python thread-safe hai?

**Nahi.**

Ye bohat important misconception hai.

GIL:

```text
≠
```

application-level thread safety.

Example:

```python
counter += 1
```

Do threads mein shared variable ho to aap blindly assume nahi kar sakte ke program logically race-free hai.

Aapko synchronization primitives ki zarurat ho sakti hai:

```python
Lock
RLock
Semaphore
Condition
Event
```

Jo hum Lesson 87–88 mein kar chuke hain.

---

# 11. GIL aur race condition different concepts hain

### GIL

Interpreter-level mechanism.

### Race condition

Application logic ka concurrency bug.

Example:

```text
Thread A:
read counter = 10

Thread B:
read counter = 10

Thread A:
write 11

Thread B:
write 11
```

Expected:

```text
12
```

Actual:

```text
11
```

Ye race-condition problem hai.

GIL ko dekh kar assume nahi karna chahiye ke aapka application automatically safe hai.

---

# 12. GIL thread switching

CPython multiple threads ko permanently ek hi thread ke paas nahi rakhta.

Conceptually:

```text
Thread A
   ↓
Python execution
   ↓
switch
   ↓
Thread B
   ↓
Python execution
   ↓
switch
   ↓
Thread C
```

Isliye threads **concurrent** appear karte hain.

Lekin CPU-bound pure Python workload mein ye necessarily:

```text
4 threads = 4 cores
```

nahi ban jata.

---

# 13. Concurrency vs Parallelism

Ye distinction ab GIL ke context mein crystal clear honi chahiye.

### Concurrency

Multiple tasks progress kar rahe hain.

```text
A → work
B → work
A → wait
C → work
B → wait
A → work
```

### Parallelism

Multiple tasks **same time** different CPU cores par execute ho rahe hain.

```text
Core 1 → A
Core 2 → B
Core 3 → C
Core 4 → D
```

Normal CPython mein pure Python CPU-bound threads GIL ki wajah se true multi-core Python-bytecode parallelism achieve nahi karte.

---

# 14. Process GIL ko kaise bypass karta hai?

Yahan `multiprocessing` powerful ho jata hai.

Suppose:

```text
Process 1
    ↓
Python interpreter
    ↓
GIL 1
```

aur:

```text
Process 2
    ↓
Python interpreter
    ↓
GIL 2
```

Ye **separate processes** hain.

Har process ka apna interpreter state hota hai.

Concept:

```text
CPU
├── Core 1 → Process 1 → Python
├── Core 2 → Process 2 → Python
├── Core 3 → Process 3 → Python
└── Core 4 → Process 4 → Python
```

Isliye multiple processes pure-Python CPU-bound workloads ko multiple CPU cores par parallel execute kar sakte hain.

---

# 15. `ThreadPoolExecutor` vs `ProcessPoolExecutor`

Ab Lesson 92 aur 93 ko connect karo:

```text
CPU-bound pure Python
        ↓
ProcessPoolExecutor
        ↓
Multiple processes
        ↓
Multiple interpreters
        ↓
Multi-core parallelism
```

Aur:

```text
I/O-bound
   ↓
ThreadPoolExecutor
   ↓
Threads
   ↓
waiting time overlap
   ↓
better throughput
```

---

# 16. HVAC example

Suppose Honeywell/BMS se 5000 equipment points read karne hain:

```text
AHU
VAV
FCU
Pump
Fan
Temperature
Pressure
Damper
Flow
```

Agar problem:

```text
BMS/API/network/database communication
```

hai:

```text
ThreadPoolExecutor
```

useful ho sakta hai.

Because:

```text
Thread 1 → BMS request → WAIT
Thread 2 → BMS request → WAIT
Thread 3 → DB request → WAIT
Thread 4 → API request → WAIT
```

---

# 17. Heavy HVAC analytics

Ab maan lo data already memory mein aa gaya:

```text
5 million readings
```

Aur aap calculate kar rahe ho:

```text
Airflow statistics
Energy calculations
Anomaly detection
Complex mathematical transformations
```

Agar workload pure-Python aur CPU-heavy hai:

```text
ProcessPoolExecutor
```

consider kar sakte ho.

Concept:

```text
5 million records
       ↓
split
       ↓
Process 1 → chunk 1
Process 2 → chunk 2
Process 3 → chunk 3
Process 4 → chunk 4
       ↓
combine
```

---

# 18. Lekin har CPU task mein ProcessPool automatically best nahi

Ye bhi important hai.

Processes ka overhead hota hai:

```text
Process creation
Serialization
IPC
Data transfer
Memory
```

Agar task bohat chhota hai:

```python
x * x
```

to processes create karna task se zyada expensive ho sakta hai.

Example:

```text
Task = 0.0001 sec
Process overhead = much larger
```

To parallelization se speed **kam** bhi ho sakti hai.

Rule:

> Task sufficiently expensive hona chahiye ke parallelization overhead justify ho.

---

# 19. Pickling ka connection

ProcessPool mein:

```text
Main process
      ↓
serialize
      ↓
child process
      ↓
deserialize
```

Is process ko commonly pickling ke through implement kiya jata hai.

Example:

```python
executor.submit(worker, data)
```

Agar `data` bohat huge hai:

```text
Huge data
   ↓
serialization
   ↓
transfer
   ↓
deserialization
```

to performance hit ho sakta hai.

Isliye multiprocessing mein sirf:

> "CPU cores zyada hain"

dekhna enough nahi.

Data-transfer cost bhi dekhni hoti hai.

---

# 20. Native C extensions aur GIL

Ab ek advanced point.

Har Python operation necessarily same way se GIL hold nahi karta.

Some native/C extensions can release the GIL while performing long-running native operations.

Concept:

```text
Python thread
     ↓
C extension
     ↓
release GIL
     ↓
native computation
```

Isliye kuch libraries threads ke saath actual parallel CPU work kar sakti hain.

Ye reason hai ke:

> "Python mein threads CPU ke liye kabhi useful nahi"

bhi oversimplification hai.

Correct statement:

> **Pure-Python CPU-bound code in normal CPython generally doesn't get multi-core parallelism from threads because of the GIL. Native code that releases the GIL can behave differently.**

---

# 21. GIL ka scope

GIL ko is tarah samjho:

```text
CPython Process
│
├── Thread 1
├── Thread 2
├── Thread 3
└── Thread 4
       │
       ↓
      GIL
       │
       ↓
Python bytecode execution
```

Important:

**One process → generally one GIL-controlled interpreter execution context.**

Separate processes:

```text
Process 1 → own interpreter/GIL
Process 2 → own interpreter/GIL
Process 3 → own interpreter/GIL
```

---

# 22. GIL vs `multiprocessing.Lock`

Ye confuse mat karna.

### GIL

Interpreter-level.

### `multiprocessing.Lock`

Application-level inter-process synchronization.

Example:

```python
from multiprocessing import Lock
```

Aap explicitly use karte ho:

```python
with lock:
    ...
```

GIL automatically application ke shared data ko protect karne ka replacement nahi hai.

---

# 23. GIL vs `threading.Lock`

Same:

```text
GIL
  ↓
CPython interpreter mechanism

threading.Lock
  ↓
Aapke application ka synchronization tool
```

Example:

```python
lock = threading.Lock()

with lock:
    counter += 1
```

Yahan `Lock` ka purpose hai:

> Is critical section mein ek waqt mein ek thread enter kare.

---

# 24. Ek strong comparison

```text
                    GIL
                     │
          CPython interpreter level
                     │
          Python bytecode execution
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
     Thread                    Process
        ↓                         ↓
 same process               separate process
        ↓                         ↓
   same GIL context         separate interpreter
                                  ↓
                           own GIL context
```

---

# 25. GIL ko ek analogy se samjho

Ek office imagine karo:

```text
Office = Python process
Employees = Threads
One special key = GIL
```

Office mein 4 employees hain:

```text
Employee A
Employee B
Employee C
Employee D
```

Lekin special Python-code room ki ek key hai.

```text
        🔑
      GIL key
        ↓
Python execution room
```

Ek waqt mein ek employee room mein enter kar sakta hai.

Lekin jab employee:

```text
coffee lene
phone call
network response
database response
```

ke liye wait kar raha hai, doosra employee useful work kar sakta hai.

---

# 26. Process ka analogy

Ab 4 separate offices bana do:

```text
Office 1 → own key
Office 2 → own key
Office 3 → own key
Office 4 → own key
```

Ab:

```text
Core 1 → Office 1
Core 2 → Office 2
Core 3 → Office 3
Core 4 → Office 4
```

Yahi conceptual reason hai ke multiprocessing CPU-bound workloads ke liye useful ho sakti hai.

---

# 27. Ek important modern note

CPython ke recent versions mein GIL architecture evolve ho raha hai, including optional/free-threaded builds in newer Python releases.

Isliye future Python versions ke context mein:

> "Python mein GIL hamesha exactly isi tarah rahega"

keh dena technically correct nahi hoga.

Lekin **normal/default CPython builds aur traditional Python concurrency understanding** ke liye jo model humne abhi padha hai, woh abhi bhi fundamental hai.

---

# 28. Final decision tree

Jab bhi workload mile:

```text
                 Workload
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       I/O-bound           CPU-bound
          │                   │
          ↓                   ↓
   ThreadPoolExecutor   Pure Python?
                              │
                       ┌──────┴──────┐
                       ↓             ↓
                      Yes            No /
                       ↓          native code
                ProcessPool        ↓
                   often        Depends on
                  useful        library/GIL
```

---

# 29. Sabse important 8 points

1. **GIL CPython ka interpreter-level mechanism hai.**
2. Normal CPython mein ek process ke Python bytecode execution par GIL significant restriction lagata hai.
3. **Threading useless nahi hai.**
4. I/O-bound tasks ke liye threads bohat useful hain.
5. Pure-Python CPU-bound work ke liye threads normally multi-core Python-bytecode parallelism nahi dete.
6. Multiple processes separate interpreter/GIL contexts provide karte hain.
7. Isliye CPU-bound pure-Python workloads mein `ProcessPoolExecutor` useful ho sakta hai.
8. GIL **application-level thread safety ka replacement nahi hai** — `Lock`, `Condition`, etc. phir bhi relevant hain.

### One-line memory trick:

```text
I/O → Threads
CPU + Pure Python → Processes
Shared state → Synchronization
GIL → CPython Python-bytecode execution restriction
```

**Next Lesson 94:** **GIL Bypass Techniques — C Extensions + `multiprocessing`** — yahan hum dekhenge ke practically GIL ko bypass/release karke CPU parallelism kaise achieve hota hai, aur native libraries kis tarah GIL ko release karti hain.
# Lesson 94 — GIL Bypass Techniques

## C Extensions + `multiprocessing`

Ab hum practical level par dekhenge:

> **Agar GIL pure-Python CPU work ko multiple threads par true multi-core parallelism nahi deta, to us restriction ko practically kaise bypass/release kiya jata hai?**

Do major approaches:

```text
GIL problem
    │
    ├── 1. Multiple Processes
    │      ↓
    │   multiprocessing
    │
    └── 2. Native Code
           ↓
       C/C++/Rust extensions
           ↓
       GIL release
```

---

# 1. Sabse pehle: "GIL bypass" ka matlab

GIL bypass ke do different meanings ho sakte hain.

### Approach 1 — GIL ko avoid karna

Multiple processes:

```text
Process 1 → GIL 1
Process 2 → GIL 2
Process 3 → GIL 3
Process 4 → GIL 4
```

Yahan hum ek hi GIL ko bypass nahi kar rahe.

Hum **separate processes** use kar rahe hain.

---

### Approach 2 — GIL release karna

Native extension:

```text
Python Thread
     ↓
Native C/C++ code
     ↓
GIL released
     ↓
CPU computation
```

Yahan native code kuch operations ke dauran GIL release kar sakta hai.

---

# 2. Technique #1 — `multiprocessing`

Sabse practical aur Python-level solution:

```python
from multiprocessing import Process
```

Ya high-level:

```python
from concurrent.futures import ProcessPoolExecutor
```

---

# 3. Multiple processes ka architecture

Suppose 4 CPU cores hain:

```text
CPU
│
├── Core 1 ← Process 1
├── Core 2 ← Process 2
├── Core 3 ← Process 3
└── Core 4 ← Process 4
```

Har process:

```text
Process
 ├── Python interpreter
 ├── own memory
 └── own GIL context
```

Isliye:

```text
Process 1 → Python bytecode
Process 2 → Python bytecode
Process 3 → Python bytecode
Process 4 → Python bytecode
```

parallel run kar sakte hain.

---

# 4. CPU-bound example

Suppose:

```python
def calculate(n):
    total = 0

    for i in range(n):
        total += i * i

    return total
```

Ye CPU-bound hai.

Hum use:

```python
ProcessPoolExecutor
```

se parallel kar sakte hain.

```python
from concurrent.futures import ProcessPoolExecutor


def calculate(n):
    total = 0

    for i in range(n):
        total += i * i

    return total


if __name__ == "__main__":

    values = [
        10_000_000,
        10_000_000,
        10_000_000,
        10_000_000,
    ]

    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(calculate, values)
        )

    print(results)
```

Concept:

```text
10M → Process 1
10M → Process 2
10M → Process 3
10M → Process 4
```

---

# 5. Ye GIL ko kaise bypass karta hai?

Important:

```text
Wrong mental model:

4 processes
     ↓
one GIL
```

Correct:

```text
Process 1 → Interpreter 1 → GIL 1

Process 2 → Interpreter 2 → GIL 2

Process 3 → Interpreter 3 → GIL 3

Process 4 → Interpreter 4 → GIL 4
```

Isliye GIL of Process 1, Process 2 ke Python execution ko block nahi karta.

---

# 6. Lekin processes free nahi hain

Processes ka cost hota hai.

```text
Process
 ↓
Memory
 ↓
Startup
 ↓
Serialization
 ↓
IPC
```

Agar aap tiny task ko process mein bhejo:

```python
x * 2
```

to ho sakta hai overhead actual calculation se zyada ho.

Isliye:

> **Parallelization tab useful hoti hai jab task sufficiently expensive ho.**

---

# 7. Serialization ka major issue

Suppose:

```python
large_data = [...]
```

Aur:

```python
executor.submit(worker, large_data)
```

ProcessPool mein data ko worker process tak transfer karna pad sakta hai.

Concept:

```text
Main Process
     │
     ↓
Serialize
     │
     ↓
IPC
     │
     ↓
Worker Process
     │
     ↓
Deserialize
```

Agar data bohat huge hai:

```text
Calculation = 1 sec
Data transfer = 5 sec
```

to multiprocessing ka benefit khatam ho sakta hai.

---

# 8. Isliye chunking important hai

Agar 1 million records hain:

```text
1,000,000 records
```

Instead of har record ko separate process task banana:

```text
1 record
1 record
1 record
...
```

chunks use karna better ho sakta hai:

```text
Chunk 1 → 250,000
Chunk 2 → 250,000
Chunk 3 → 250,000
Chunk 4 → 250,000
```

Then:

```text
Process 1 → Chunk 1
Process 2 → Chunk 2
Process 3 → Chunk 3
Process 4 → Chunk 4
```

Isse task/IPC overhead reduce ho sakta hai.

---

# 9. Technique #2 — C Extensions

Ab deeper concept.

Python khud mostly C mein implemented hai — especially CPython.

Aap native C/C++ extension bana sakte ho jo Python se call ho:

```text
Python
  ↓
C extension
  ↓
native machine code
```

Native extension kuch operations ke during GIL release kar sakti hai.

---

# 10. GIL release ka conceptual model

Normally:

```text
Python thread
     ↓
Acquire GIL
     ↓
Python bytecode
     ↓
Release/switch
```

Native operation jo GIL release karta hai:

```text
Python thread
     ↓
GIL
     ↓
C extension
     ↓
release GIL
     ↓
native work
     ↓
reacquire GIL
     ↓
Python
```

Is dauran doosra Python thread bhi native work kar sakta hai.

---

# 11. Important: har C extension GIL release nahi karti

Ye assume nahi karna:

> "C extension hai, to GIL automatically release ho gaya."

**Nahi.**

Extension ko explicitly appropriate operations ke around GIL release karna hota hai.

Conceptually CPython C API mein mechanisms available hain jinke through extension native work ke waqt GIL release/reacquire kar sakti hai.

---

# 12. Conceptual C example

Old-style CPython C API mein conceptual pattern kuch is tarah hota hai:

```c
Py_BEGIN_ALLOW_THREADS

/* long-running native work */

Py_END_ALLOW_THREADS
```

Meaning roughly:

```text
Py_BEGIN_ALLOW_THREADS
        ↓
GIL release
        ↓
native computation
        ↓
Py_END_ALLOW_THREADS
        ↓
GIL reacquire
```

Ye C extension developer ke liye important mechanism hai.

---

# 13. Lekin ek condition hai

GIL release karte waqt native code ko Python objects ke saath unsafe interaction nahi karna chahiye.

Conceptually:

```text
GIL released
    ↓
native computation
    ↓
Python object manipulation ❌
```

Instead:

```text
GIL released
    ↓
independent native computation
    ↓
finish
    ↓
GIL reacquire
    ↓
Python objects access
```

Ye extension development ka important safety rule hai.

---

# 14. NumPy example

Practical world mein sabse important examples mein se ek:

```python
import numpy as np
```

NumPy ka heavy numerical work native compiled code mein perform ho sakta hai, aur suitable operations threads ke saath GIL behavior Python-level loops se different ho sakta hai.

Example:

```python
import numpy as np

a = np.random.rand(10_000_000)
b = np.random.rand(10_000_000)

c = a + b
```

Python mein:

```python
for i in range(...):
    c[i] = a[i] + b[i]
```

likhne ke bajaye NumPy native implementation use kar raha hai.

---

# 15. Pure Python vs NumPy

### Pure Python

```python
total = 0

for x in data:
    total += x
```

Ye Python bytecode level par heavy work karta hai.

GIL relevant hai.

---

### Native numerical library

```python
total = np.sum(data)
```

Heavy computation native compiled implementation mein ho sakta hai.

Isliye threading behavior significantly different ho sakta hai.

Lekin actual performance aur GIL behavior **specific operation/library/version** par depend karta hai.

---

# 16. Python loop vs vectorization

Suppose:

```python
data = [1, 2, 3, 4, 5]
```

Pure Python:

```python
result = []

for x in data:
    result.append(x * 2)
```

Native/vectorized library:

```python
result = np.array(data) * 2
```

Concept:

```text
Pure Python:
Python
 ↓
Python loop
 ↓
Python bytecode
 ↓
GIL relevant
```

versus:

```text
NumPy:
Python
 ↓
NumPy
 ↓
native compiled loop
 ↓
CPU
```

Isi wajah se scientific computing mein Python ko often orchestration layer ke taur par use kiya jata hai.

---

# 17. Cython bhi ek approach hai

Ek aur technology:

```text
Cython
```

Cython Python-like syntax ko C/C++ extension code mein compile karne mein help karta hai.

Concept:

```text
Python-like code
       ↓
    Cython
       ↓
C/C++ extension
       ↓
native execution
```

Cython code ko appropriate design ke saath GIL release karne ke liye use kiya ja sakta hai.

---

# 18. Rust extensions

Modern Python ecosystem mein Rust bhi use hota hai.

Popular approach:

```text
Python
   ↓
Rust extension
   ↓
native code
```

Tools/frameworks jaise:

```text
PyO3
maturin
```

Python ↔ Rust extension development ko easier banate hain.

Important concept same hai:

> Heavy native computation ko Python interpreter ke bahar execute karna.

---

# 19. C++ extensions

C++ bhi:

```text
Python
  ↓
C++ extension
  ↓
native code
```

use kar sakta hai.

Iska use high-performance applications mein hota hai.

---

# 20. Third technique — GIL-free / free-threaded CPython

Modern Python ecosystem mein ek aur major development hai:

```text
Free-threaded CPython
```

Concept:

```text
Traditional CPython
       ↓
       GIL
```

versus:

```text
Free-threaded build
       ↓
GIL disabled
```

Iska purpose Python threads ko multi-core CPU parallelism ke liye enable karna hai without relying on the traditional global lock.

Lekin yahan important distinction:

> **GIL-free build ka matlab automatically har Python program fast ho jayega nahi hai.**

There are compatibility and performance trade-offs, and extension support matters.

---

# 21. Traditional vs free-threaded

### Traditional CPython

```text
Thread 1 ─┐
Thread 2 ─┤
Thread 3 ─┼→ GIL
Thread 4 ─┘
```

### Free-threaded CPython

Conceptually:

```text
Thread 1 → Core 1
Thread 2 → Core 2
Thread 3 → Core 3
Thread 4 → Core 4
```

Lekin application ko thread-safe banana phir bhi zaroori hai.

GIL remove hone ka matlab:

```text
race conditions disappear
```

**nahi** hai.

Actually shared mutable state ke bugs aur important ho sakte hain.

---

# 22. GIL bypass ka comparison

| Technique                 | Basic idea                     | CPU parallelism         |
| ------------------------- | ------------------------------ | ----------------------- |
| `threading` + pure Python | Same process threads           | Normally limited by GIL |
| `multiprocessing`         | Multiple processes             | Yes                     |
| `ProcessPoolExecutor`     | Process pool abstraction       | Yes                     |
| Native C/C++ extension    | GIL release during native work | Possible                |
| Cython                    | Compiled/native code           | Possible                |
| Rust extension            | Native Rust code               | Possible                |
| Free-threaded CPython     | GIL disabled build             | True threading possible |

---

# 23. `ProcessPoolExecutor` vs native extension

Dono CPU performance improve kar sakte hain, lekin architecture different hai.

### ProcessPool

```text
Python
 ↓
Process 1
Process 2
Process 3
Process 4
```

Pros:

* Pure Python code bhi parallel ho sakta hai
* Existing Python code ko relatively easily parallelize kar sakte ho

Cons:

* Memory overhead
* Serialization
* IPC
* Process startup

---

### Native extension

```text
Python
 ↓
Native code
 ↓
CPU
```

Pros:

* High performance
* Large numeric operations efficient
* Data same process mein reh sakta hai

Cons:

* Native programming complexity
* Memory safety concerns
* Extension compatibility
* GIL management

---

# 24. HVAC/BMS example

Suppose aapke paas:

```text
100,000 HVAC readings
```

Columns:

```text
Equipment ID
Temperature
Pressure
Airflow
Damper
Fan Speed
Timestamp
```

### Case A — Data BMS se retrieve karna

```text
Network/API
Database
BMS
```

Use:

```text
ThreadPoolExecutor
```

because I/O-bound.

---

### Case B — Heavy Python calculation

```text
100,000 readings
       ↓
complex calculations
```

Use:

```text
ProcessPoolExecutor
```

if computation is CPU-bound and sufficiently large.

---

### Case C — Massive numerical array processing

```text
NumPy
```

jaisi native numerical library potentially better approach ho sakti hai.

---

# 25. Ek aur important concept: "Python slow hai"

Ye statement incomplete hai.

Correct question:

> **Kaunsa part Python mein execute ho raha hai?**

Example:

```text
Python orchestration
       ↓
NumPy native code
       ↓
CPU
```

Yahan Python sirf instructions coordinate kar raha hai.

Isliye:

```text
Python ≠ necessarily slow
```

Performance workload architecture par depend karti hai.

---

# 26. GIL bypass ka decision tree

```text
CPU-heavy?
    │
    ├── No → I/O?
    │          ↓
    │       Threads / asyncio
    │
    └── Yes
         │
         ├── Pure Python?
         │      ↓
         │   ProcessPool
         │
         └── Numeric/native workload?
                ↓
          NumPy / native extension
```

Aur:

```text
Need maximum control/performance?
        ↓
C / C++ / Rust / Cython
```

---

# 27. Sabse important distinction

Ye 3 statements alag hain:

### 1.

```text
GIL bypass
```

Multiple processes se possible.

### 2.

```text
GIL release
```

Native extension kuch operations ke dauran kar sakti hai.

### 3.

```text
GIL-free Python
```

Free-threaded CPython build ka concept.

In teenon ko ek hi cheez mat samajhna.

---

# 28. Complete picture

Ab Lesson 87 se Lesson 94 tak ki chain:

```text
threading
   ↓
Threads
   ↓
I/O concurrency
   ↓
       GIL
        ↓
Pure Python CPU threads limited
        ↓
   ┌────┴────┐
   ↓         ↓
Processes   Native code
   ↓         ↓
multiprocessing   C/C++/Rust/Cython
   ↓         ↓
own interpreter   GIL can be released
   ↓
multi-core
parallelism
```

Aur high-level API:

```text
concurrent.futures
        │
   ┌────┴────┐
   ↓         ↓
ThreadPool  ProcessPool
```

---

# 29. Lesson 94 ki final memory

```text
GIL problem
    ↓
CPU-bound pure Python
    ↓
ThreadPool normally ideal nahi
    ↓
ProcessPoolExecutor
    ↓
multiple processes
    ↓
multi-core parallelism
```

Ya:

```text
Python
 ↓
Native C/C++/Rust
 ↓
GIL release where appropriate
 ↓
parallel native computation possible
```

Aur modern direction:

```text
Free-threaded CPython
 ↓
GIL disabled
 ↓
true Python threading possible
```

**One-line rule:**

> **Pure Python CPU work → processes; heavy native numerical work → native libraries/GIL-releasing operations; I/O work → threads/asyncio.**

**Next Lesson 95:** `asyncio` Advanced — **`asyncio.Queue`, `Lock`, `Event`, `Condition`, `Semaphore`**. Ismein hum dekhenge ke `threading` ke synchronization primitives aur `asyncio` ke synchronization primitives mein actual difference kya hai.
# Lesson 95 — `asyncio` Advanced

## `Queue`, `Lock`, `Event`, `Condition`, `Semaphore`

Ab hum `asyncio` ko synchronization ke level par samjhenge.

Aap ne pehle `threading` mein ye concepts dekhe:

```text
threading
├── Lock
├── RLock
├── Semaphore
├── Event
├── Condition
└── Queue
```

`asyncio` mein bhi similar concepts hain:

```text
asyncio
├── Lock
├── Semaphore
├── Event
├── Condition
└── Queue
```

Lekin **implementation aur behavior different** hai.

---

# 1. Sabse pehle `asyncio` ka mental model

Traditional threading:

```text
Thread 1
Thread 2
Thread 3
Thread 4
```

OS threads ko schedule karta hai.

`asyncio`:

```text
One event loop
      ↓
 ┌────┼────┐
 ↓    ↓    ↓
Task Task Task
```

Tasks cooperative way mein execution hand off karti hain.

Example:

```python
await something()
```

par current task event loop ko control de deti hai.

---

# 2. `asyncio` ka basic example

```python
import asyncio


async def worker():
    print("Start")
    await asyncio.sleep(1)
    print("End")


async def main():
    await worker()


asyncio.run(main())
```

Flow:

```text
main()
 ↓
worker()
 ↓
sleep()
 ↓
event loop
 ↓
1 second later
 ↓
worker continues
```

---

# 3. `asyncio` Lock

Syntax:

```python
lock = asyncio.Lock()
```

Use:

```python
async with lock:
    ...
```

Example:

```python
import asyncio


lock = asyncio.Lock()
counter = 0


async def worker():
    global counter

    async with lock:
        counter += 1
```

Yahan lock ensure karta hai ke critical section mein ek waqt mein ek asyncio task enter kare.

---

# 4. `threading.Lock` vs `asyncio.Lock`

Ye bohat important difference hai.

### Threading

```python
lock = threading.Lock()

with lock:
    ...
```

### Asyncio

```python
lock = asyncio.Lock()

async with lock:
    ...
```

Difference:

```text
threading.Lock
    ↓
Threads

asyncio.Lock
    ↓
asyncio Tasks
```

---

# 5. `asyncio.Lock` ko normal `with` se use nahi karna

Wrong:

```python
with lock:
    ...
```

Agar lock `asyncio.Lock()` hai.

Correct:

```python
async with lock:
    ...
```

Kyunkay acquisition asynchronous ho sakti hai.

---

# 6. Lock ka actual use

Suppose multiple tasks shared resource access kar rahi hain:

```text
Task A ─┐
Task B ─┼──→ Shared Resource
Task C ─┘
```

Lock:

```text
Task A → 🔒 → resource
Task B → wait
Task C → wait

Task A → unlock

Task B → 🔒 → resource
```

---

# 7. HVAC example

Suppose multiple async tasks ek shared equipment status dictionary update kar rahi hain:

```python
equipment_status = {}
lock = asyncio.Lock()
```

Task:

```python
async def update_status(equipment_id, status):

    async with lock:
        equipment_status[equipment_id] = status
```

Concept:

```text
AHU-01 task ─┐
AHU-02 task ─┼→ shared dictionary
AHU-03 task ─┘
```

Lock shared-state update ko protect karta hai.

---

# 8. `asyncio.Event`

`Event` ka concept:

> Ek task signal bhejti hai, doosri tasks us signal ka wait karti hain.

Create:

```python
event = asyncio.Event()
```

Wait:

```python
await event.wait()
```

Signal:

```python
event.set()
```

Reset:

```python
event.clear()
```

---

# 9. Event example

```python
import asyncio


event = asyncio.Event()


async def worker():
    print("Waiting...")

    await event.wait()

    print("Signal mil gaya!")


async def main():
    task = asyncio.create_task(worker())

    await asyncio.sleep(2)

    print("Signal send kar raha hoon")
    event.set()

    await task


asyncio.run(main())
```

Concept:

```text
Worker
  ↓
await event.wait()
  ↓
WAIT
  ↓
event.set()
  ↓
CONTINUE
```

---

# 10. Event ko traffic signal samjho

```text
RED
 ↓
Tasks wait

GREEN
 ↓
Tasks continue
```

Example:

```text
BMS connected?
    ↓
NO
    ↓
wait()

BMS connected
    ↓
event.set()
    ↓
tasks continue
```

---

# 11. Event vs Lock

Ye confuse mat karna.

### Lock

```text
"Kaun andar ja sakta hai?"
```

### Event

```text
"Signal aa gaya hai ya nahi?"
```

Example:

```text
Lock:
Only one task → critical section

Event:
Many tasks → wait for signal
```

---

# 12. `asyncio.Semaphore`

Semaphore ka matlab:

> Ek waqt mein maximum N tasks resource use kar sakti hain.

Create:

```python
semaphore = asyncio.Semaphore(3)
```

Use:

```python
async with semaphore:
    ...
```

---

# 13. Semaphore example

```python
import asyncio


semaphore = asyncio.Semaphore(2)


async def worker(name):
    async with semaphore:
        print(name, "started")

        await asyncio.sleep(2)

        print(name, "finished")


async def main():

    tasks = [
        asyncio.create_task(worker(f"Task-{i}"))
        for i in range(5)
    ]

    await asyncio.gather(*tasks)


asyncio.run(main())
```

Agar:

```text
Semaphore = 2
```

to maximum:

```text
2 tasks
```

resource section mein ek waqt mein hongi.

---

# 14. Semaphore ka visual

5 tasks:

```text
Task 1
Task 2
Task 3
Task 4
Task 5
```

Semaphore:

```text
Capacity = 2

[ Task 1 ] [ Task 2 ]
[         WAIT        ]
[         WAIT        ]
[         WAIT        ]
```

Jab Task 1 finish:

```text
[ Task 3 ] [ Task 2 ]
```

---

# 15. HVAC/API example

Suppose aapke paas:

```text
1000 VAV devices
```

Aur BMS API ek waqt mein sirf limited requests handle kar sakti hai.

Agar aap:

```python
await asyncio.gather(*1000_tasks)
```

blindly kar dein, to bohat saari requests simultaneously generate ho sakti hain.

Better:

```python
semaphore = asyncio.Semaphore(10)
```

Then:

```python
async def read_vav(vav_id):

    async with semaphore:
        return await read_from_bms(vav_id)
```

Ab:

```text
1000 tasks
      ↓
Semaphore(10)
      ↓
10 active requests
      ↓
next tasks
```

Ye **concurrency limiting** hai.

---

# 16. Lock vs Semaphore

Very important:

### Lock

```python
asyncio.Lock()
```

Capacity:

```text
1
```

### Semaphore

```python
asyncio.Semaphore(5)
```

Capacity:

```text
5
```

Conceptually:

```text
Lock
 ↓
maximum 1

Semaphore(5)
 ↓
maximum 5
```

Isliye aap keh sakte ho:

> Lock is essentially a one-at-a-time synchronization primitive, while Semaphore allows a bounded number of concurrent holders.

---

# 17. `asyncio.Queue`

Ab sabse powerful concepts mein se ek:

```python
asyncio.Queue()
```

Ye async producer-consumer architecture ke liye use hoti hai.

Create:

```python
queue = asyncio.Queue()
```

Producer:

```python
await queue.put(item)
```

Consumer:

```python
item = await queue.get()
```

---

# 18. Producer-consumer architecture

```text
Producer
   ↓
   ↓ put()
┌───────────┐
│ AsyncQueue│
└───────────┘
   ↓ get()
Consumer
```

Multiple producers/consumers:

```text
Producer 1 ─┐
Producer 2 ─┼→ Queue → Consumer 1
Producer 3 ─┘         → Consumer 2
```

---

# 19. Basic Queue example

```python
import asyncio


async def producer(queue):

    for i in range(5):
        await queue.put(i)
        print("Produced:", i)


async def consumer(queue):

    while True:
        item = await queue.get()

        print("Consumed:", item)

        queue.task_done()


async def main():

    queue = asyncio.Queue()

    consumer_task = asyncio.create_task(
        consumer(queue)
    )

    await producer(queue)

    await queue.join()

    consumer_task.cancel()


asyncio.run(main())
```

---

# 20. `queue.put()`

Async queue mein:

```python
await queue.put(item)
```

Agar queue bounded hai aur full ho gayi:

```text
Queue full
   ↓
producer waits
```

Yani producer automatically backpressure experience kar sakta hai.

---

# 21. `queue.get()`

Consumer:

```python
item = await queue.get()
```

Agar queue empty hai:

```text
Queue empty
   ↓
consumer waits
```

Jab item aata hai:

```text
item available
   ↓
consumer continues
```

---

# 22. `task_done()`

Har:

```python
queue.get()
```

ke corresponding processing ke baad:

```python
queue.task_done()
```

call karna important hai.

Example:

```python
item = await queue.get()

try:
    await process(item)
finally:
    queue.task_done()
```

---

# 23. `queue.join()`

Agar:

```python
await queue.join()
```

karoge to iska concept hai:

> Queue mein jo tasks currently outstanding hain, unki processing complete hone tak wait karo.

Flow:

```text
put()
 ↓
unfinished task count +1

get()
 ↓
process

task_done()
 ↓
unfinished task count -1

count = 0
 ↓
queue.join() returns
```

---

# 24. Bounded `asyncio.Queue`

Aap capacity define kar sakte ho:

```python
queue = asyncio.Queue(maxsize=10)
```

Ab queue maximum 10 pending items rakh sakti hai.

Agar:

```text
10 items
```

already queue mein hain:

```python
await queue.put(item)
```

wait kar sakta hai jab tak space available na ho.

Ye **backpressure** create karta hai.

---

# 25. Backpressure kya hota hai?

Suppose:

```text
Producer → 1000 items/sec
Consumer → 100 items/sec
```

Without limit:

```text
Queue
10
100
1000
10000
100000
...
```

Memory problem ho sakti hai.

Bounded queue:

```text
Producer
   ↓
Queue(maxsize=100)
   ↓
Consumer
```

Queue full:

```text
Producer WAIT
```

Yani producer ki speed indirectly control hoti hai.

---

# 26. `asyncio.Condition`

Ab advanced primitive:

```python
condition = asyncio.Condition()
```

Condition ka purpose:

> Shared state ki kisi condition ke true hone ka wait karna.

Example concept:

```text
Data available?
    ↓
NO → wait
YES → continue
```

---

# 27. Condition basic example

```python
import asyncio


condition = asyncio.Condition()
data_ready = False


async def consumer():

    global data_ready

    async with condition:

        while not data_ready:
            await condition.wait()

        print("Data ready!")


async def producer():

    global data_ready

    await asyncio.sleep(2)

    async with condition:

        data_ready = True
        condition.notify_all()
```

Main:

```python
async def main():

    await asyncio.gather(
        consumer(),
        producer()
    )
```

---

# 28. Condition ka important rule: `while`

Aapko generally:

```python
while not condition:
    await condition.wait()
```

use karna chahiye.

Sirf:

```python
if not condition:
    await condition.wait()
```

par rely nahi karna chahiye.

Reason:

> Wake-up ke baad condition ko dobara verify karna hota hai.

Mental model:

```text
WAIT
 ↓
WAKE
 ↓
condition check
 ↓
true? → continue
false? → wait again
```

---

# 29. `notify()` vs `notify_all()`

Condition mein:

```python
condition.notify()
```

usually ek waiting task ko wake karta hai.

Aur:

```python
condition.notify_all()
```

waiting tasks ko notify karta hai.

Concept:

```text
notify()
   ↓
one waiter

notify_all()
   ↓
all waiters
```

---

# 30. Condition vs Event

Ye important comparison hai.

### Event

Simple signal:

```text
"Signal aa gaya."
```

### Condition

State-based synchronization:

```text
"Shared state ab required condition mein hai?"
```

Example:

```text
Event:
BMS_CONNECTED

Condition:
queue has data
temperature reached threshold
equipment state changed
```

---

# 31. `asyncio` synchronization summary

| Primitive   | Main purpose                    |
| ----------- | ------------------------------- |
| `Lock`      | One task at a time              |
| `Semaphore` | Maximum N tasks                 |
| `Event`     | Signal/notification             |
| `Condition` | Wait for shared-state condition |
| `Queue`     | Producer-consumer communication |

---

# 32. Threading vs asyncio

Ab dono ko side-by-side dekho:

| Threading               | Asyncio                             |
| ----------------------- | ----------------------------------- |
| `threading.Lock`        | `asyncio.Lock`                      |
| `threading.Semaphore`   | `asyncio.Semaphore`                 |
| `threading.Event`       | `asyncio.Event`                     |
| `threading.Condition`   | `asyncio.Condition`                 |
| `queue.Queue`           | `asyncio.Queue`                     |
| Threads                 | Tasks                               |
| OS scheduling           | Event-loop scheduling               |
| Blocking calls possible | `await`-based cooperative execution |

---

# 33. Sabse important difference

Thread:

```text
OS thread
```

Async task:

```text
Event loop ke andar coroutine/task
```

Isliye:

```python
await asyncio.sleep(1)
```

aur:

```python
time.sleep(1)
```

same nahi hain.

### `asyncio.sleep()`

```text
Task waits
 ↓
event loop doosri task chala sakta hai
```

### `time.sleep()`

```text
Current thread BLOCK
 ↓
event loop bhi block ho sakta hai
```

Async code mein blocking functions bohat carefully use karni chahiye.

---

# 34. `asyncio.Queue` vs `queue.Queue`

Ye bhi important:

### `queue.Queue`

```python
from queue import Queue
```

Threads ke liye.

### `asyncio.Queue`

```python
import asyncio

queue = asyncio.Queue()
```

Async tasks ke liye.

Don't mix them casually.

---

# 35. Full async HVAC architecture

Ab ek realistic architecture:

```text
                BMS/API
                   │
          ┌────────┴────────┐
          ↓                 ↓
     Producer 1        Producer 2
          │                 │
          └────────┬────────┘
                   ↓
             asyncio.Queue
                   │
             ┌─────┴─────┐
             ↓           ↓
        Consumer 1   Consumer 2
             │           │
             └─────┬─────┘
                   ↓
             Shared State
                   ↑
                 Lock
```

Aur API rate limiting:

```text
BMS Requests
     ↓
Semaphore(10)
     ↓
maximum 10 concurrent requests
```

---

# 36. Ek complete conceptual application

Imagine:

```text
1000 VAVs
```

System:

```text
asyncio
│
├── Producer
│      ↓
│   VAV IDs
│      ↓
│   Queue
│
├── Consumers
│      ↓
│   Read BMS
│
├── Semaphore(10)
│      ↓
│   max 10 requests
│
├── Lock
│      ↓
│   shared results
│
└── Event
       ↓
   shutdown signal
```

Ye real-world async architecture ka strong pattern hai.

---

# 37. Ek aur important distinction: communication vs synchronization

### Queue

Primarily:

> **Data/task communication**

```text
Producer → Queue → Consumer
```

### Lock

Primarily:

> **Mutual exclusion**

```text
Task → critical section
```

### Semaphore

Primarily:

> **Concurrency limiting**

```text
max N active
```

### Event

Primarily:

> **Signaling**

```text
ready / stop / connected
```

### Condition

Primarily:

> **State-based waiting**

```text
wait until state changes
```

---

# 38. Memory trick

Isko yaad rakho:

```text
Lock       → "ONE"
Semaphore  → "N"
Event      → "SIGNAL"
Condition  → "STATE"
Queue      → "DATA"
```

Ye 5 words poora Lesson 95 yaad karwa denge.

---

# 39. Final architecture

```text
                    asyncio
                       │
                 Event Loop
                       │
             ┌─────────┼─────────┐
             ↓         ↓         ↓
           Task      Task      Task
             │         │         │
             ├─────────┼─────────┤
             ↓         ↓         ↓
           Lock    Semaphore    Event
             │         │         │
             └────── Condition ──┘
                       │
                     Queue
                       │
               Producer / Consumer
```

### Final one-line rules:

> **`asyncio.Lock` → ek task at a time**

> **`asyncio.Semaphore(N)` → maximum N tasks**

> **`asyncio.Event` → signal ka wait**

> **`asyncio.Condition` → state/condition ka wait**

> **`asyncio.Queue` → async producer-consumer communication**

**Next Lesson 96:** `asyncio.TaskGroup` — **Structured Concurrency (Python 3.11+)**. Ismein hum dekhenge `TaskGroup` `asyncio.create_task()` se kyun better/safer ho sakta hai, task failure par sibling tasks ke saath kya hota hai, aur `ExceptionGroup` ka connection kya hai.
# Lesson 96 — `asyncio.TaskGroup`

## Structured Concurrency — Python 3.11+

Ab hum `asyncio` ka ek **bohat important modern feature** seekhenge:

```python
asyncio.TaskGroup
```

Iska main purpose hai:

> **Multiple async tasks ko ek controlled group mein manage karna.**

Aur sabse important concept:

> **Agar group ki ek task fail ho jaye, to related sibling tasks ko properly cancel aur manage kiya ja sakta hai.**

---

# 1. Pehle problem samjho

Traditional approach:

```python
task1 = asyncio.create_task(worker1())
task2 = asyncio.create_task(worker2())
task3 = asyncio.create_task(worker3())

await task1
await task2
await task3
```

Ye kaam karta hai.

Lekin problem ye hai ke aapko manually tasks ki:

* lifecycle
* cancellation
* exceptions
* cleanup
* waiting

manage karni pad sakti hai.

---

# 2. `TaskGroup` ka idea

`TaskGroup`:

```python
async with asyncio.TaskGroup() as tg:
    ...
```

Is block ke andar jo tasks create hoti hain, woh ek **logical group** ka part ban jati hain.

Example:

```python
import asyncio


async def worker(name):
    await asyncio.sleep(1)
    print(name)


async def main():

    async with asyncio.TaskGroup() as tg:

        tg.create_task(worker("A"))
        tg.create_task(worker("B"))
        tg.create_task(worker("C"))


asyncio.run(main())
```

Concept:

```text
TaskGroup
   │
   ├── Task A
   ├── Task B
   └── Task C
```

---

# 3. `TaskGroup` automatically wait karta hai

Is code mein:

```python
async with asyncio.TaskGroup() as tg:

    tg.create_task(worker("A"))
    tg.create_task(worker("B"))
    tg.create_task(worker("C"))
```

Jab tak group ke tasks finish nahi hote, `async with` block complete nahi hota.

Concept:

```text
enter TaskGroup
      ↓
create tasks
      ↓
tasks execute
      ↓
wait for tasks
      ↓
all complete
      ↓
exit TaskGroup
```

Isliye separately:

```python
await task1
await task2
await task3
```

zaroori nahi.

---

# 4. `create_task()` vs `TaskGroup.create_task()`

Normal:

```python
task = asyncio.create_task(worker())
```

TaskGroup:

```python
tg.create_task(worker())
```

Difference:

```text
asyncio.create_task()
        ↓
individual task
        ↓
you manage lifecycle
```

versus:

```text
TaskGroup
   ↓
related tasks
   ↓
group manages lifecycle
```

---

# 5. Structured Concurrency kya hai?

Ye Lesson 96 ka **core concept** hai.

Structured concurrency ka idea:

> Child tasks ki lifecycle parent operation ke scope ke andar controlled honi chahiye.

Example:

```text
main()
  │
  └── TaskGroup
       ├── Task A
       ├── Task B
       └── Task C
```

Jab parent `TaskGroup` scope se bahar nikalta hai:

```text
TaskGroup
   ↓
children handled
   ↓
group exits
```

Yani tasks "orphan" nahi rehni chahiye.

---

# 6. Orphan task problem

Suppose:

```python
asyncio.create_task(worker())
```

kar diya.

Aur parent function return ho gaya.

Agar aap task ka lifecycle properly manage nahi karte, to architecture messy ho sakti hai:

```text
Parent
  ↓
creates task
  ↓
returns

Task
  ↓
still running
```

TaskGroup ka goal hai:

```text
Parent scope
    ↓
TaskGroup
    ↓
child tasks
    ↓
all managed
```

---

# 7. Sabse powerful feature: exception handling

Suppose:

```python
async def worker_a():
    await asyncio.sleep(1)
    raise ValueError("A failed")
```

Aur:

```python
async def worker_b():
    await asyncio.sleep(5)
    print("B finished")
```

Ab:

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(worker_a())
    tg.create_task(worker_b())
```

Kya hoga?

Task A fail karegi.

TaskGroup generally:

```text
Task A
  ↓
exception
  ↓
TaskGroup detects failure
  ↓
sibling Task B cancellation
  ↓
wait/cleanup
  ↓
exception group raised
```

Ye bohat important behavior hai.

---

# 8. Example

```python
import asyncio


async def worker_a():
    await asyncio.sleep(1)
    raise ValueError("A failed")


async def worker_b():
    try:
        await asyncio.sleep(5)
        print("B finished")

    except asyncio.CancelledError:
        print("B cancelled")
        raise


async def main():

    async with asyncio.TaskGroup() as tg:

        tg.create_task(worker_a())
        tg.create_task(worker_b())


asyncio.run(main())
```

Expected concept:

```text
A failed
   ↓
B cancelled
```

Task B ko 5 seconds complete hone ka wait nahi karaya jata.

---

# 9. Ye design kyun useful hai?

Imagine HVAC system:

```text
Read AHU
Read VAV
Read Chiller
```

Aapke tasks:

```text
Task A → AHU data
Task B → VAV data
Task C → Chiller data
```

Agar system ke liye ye teeno operations ek logical unit hain aur:

```text
Task A fails
```

to shayad:

```text
Task B
Task C
```

ko continue karna meaningful nahi.

TaskGroup:

```text
One important task fails
        ↓
cancel siblings
        ↓
cleanup
        ↓
report failure
```

Ye **fail-fast structured behavior** provide karta hai.

---

# 10. `ExceptionGroup`

Python 3.11 mein ek important feature introduce hua:

```python
ExceptionGroup
```

TaskGroup multiple task failures ko group karke raise kar sakta hai.

Example:

```text
Task A → ValueError
Task B → TypeError
Task C → success
```

To conceptually:

```text
ExceptionGroup
├── ValueError
└── TypeError
```

Ye single exception ke bajaye **multiple exceptions ka group** ho sakta hai.

---

# 11. `except*`

ExceptionGroup ke saath special syntax:

```python
except*
```

Example:

```python
try:

    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker_a())
        tg.create_task(worker_b())

except* ValueError as eg:
    print("ValueError handled")

except* TypeError as eg:
    print("TypeError handled")
```

Notice:

```python
except*
```

normal:

```python
except
```

se different hai.

---

# 12. `except` vs `except*`

### Normal exception

```python
try:
    ...
except ValueError:
    ...
```

Ek exception flow.

### ExceptionGroup

```python
try:
    ...
except* ValueError:
    ...
except* TypeError:
    ...
```

Group ke andar matching exceptions separately handle ho sakti hain.

---

# 13. `TaskGroup` cancellation

TaskGroup mein cancellation bohat important hai.

Suppose:

```text
Task A → failure
Task B → running
Task C → running
```

Then:

```text
A fails
 ↓
B cancelled
C cancelled
 ↓
cleanup
 ↓
TaskGroup exits with exception
```

Ye structured concurrency ka core benefit hai.

---

# 14. `CancelledError` ko swallow mat karo

Agar task cancellation handle karti hai:

```python
except asyncio.CancelledError:
    ...
```

to generally cancellation ko properly propagate karna chahiye:

```python
except asyncio.CancelledError:
    cleanup()
    raise
```

Important pattern:

```python
try:
    ...
except asyncio.CancelledError:
    cleanup()
    raise
```

Agar aap blindly cancellation ko swallow kar dete ho:

```python
except asyncio.CancelledError:
    pass
```

to structured concurrency behavior unexpectedly break ho sakta hai.

---

# 15. `TaskGroup` ka scope

Example:

```python
async def main():

    print("Before")

    async with asyncio.TaskGroup() as tg:

        tg.create_task(worker_a())
        tg.create_task(worker_b())

    print("After")
```

`After` tab execute hoga jab TaskGroup successfully complete ho ya exception handling ke baad control bahar aaye.

Concept:

```text
Before
  ↓
TaskGroup
  ↓
A + B
  ↓
wait
  ↓
After
```

---

# 16. `TaskGroup` aur `gather()`

Ab important comparison.

Aapne likely `asyncio.gather()` dekha hai:

```python
results = await asyncio.gather(
    worker_a(),
    worker_b(),
    worker_c()
)
```

`gather()` multiple awaitables ko concurrently run karne ka convenient mechanism hai.

Lekin `TaskGroup` ka purpose broader hai:

```text
gather()
   ↓
collect concurrent results

TaskGroup
   ↓
structured task lifecycle
   ↓
failure + cancellation management
```

---

# 17. `gather()` ka simple mental model

```text
A ─┐
B ─┼→ gather() → results
C ─┘
```

TaskGroup:

```text
TaskGroup
   │
   ├── A
   ├── B
   └── C
        │
        ↓
   lifecycle management
   cancellation
   exception grouping
```

---

# 18. Result collection

TaskGroup khud `gather()` ki tarah results ki list return nahi karta.

Example:

```python
async with asyncio.TaskGroup() as tg:

    task_a = tg.create_task(worker_a())
    task_b = tg.create_task(worker_b())

print(task_a.result())
print(task_b.result())
```

Yahan completed task objects se result retrieve kar sakte ho.

---

# 19. TaskGroup with return values

Example:

```python
import asyncio


async def worker(x):
    await asyncio.sleep(1)
    return x * 2


async def main():

    async with asyncio.TaskGroup() as tg:

        task1 = tg.create_task(worker(10))
        task2 = tg.create_task(worker(20))

    print(task1.result())
    print(task2.result())


asyncio.run(main())
```

Output:

```text
20
40
```

Important:

```python
tg.create_task(...)
```

Task object return karta hai.

---

# 20. TaskGroup nested ho sakta hai

Structured architecture mein nested groups bhi possible hain:

```text
Main
 │
 ├── TaskGroup A
 │    ├── Task 1
 │    └── Task 2
 │
 └── TaskGroup B
      ├── Task 3
      └── Task 4
```

Example conceptual architecture:

```text
Application
│
├── BMS TaskGroup
│    ├── AHU
│    └── VAV
│
└── Database TaskGroup
     ├── Read
     └── Write
```

---

# 21. HVAC example — complete structure

Suppose:

```text
Building
│
├── AHU monitoring
├── VAV monitoring
└── Chiller monitoring
```

Code concept:

```python
async def monitor_building():

    async with asyncio.TaskGroup() as tg:

        ahu_task = tg.create_task(
            monitor_ahu()
        )

        vav_task = tg.create_task(
            monitor_vav()
        )

        chiller_task = tg.create_task(
            monitor_chiller()
        )
```

Agar chiller monitoring critical failure de:

```text
Chiller Task
     ↓
failure
     ↓
TaskGroup
     ↓
cancel related monitoring tasks
     ↓
cleanup
     ↓
exception
```

---

# 22. TaskGroup + Semaphore

Ye aur powerful combination hai.

Suppose:

```text
1000 VAV
```

Tasks create karni hain, lekin maximum 10 API calls simultaneously:

```python
semaphore = asyncio.Semaphore(10)
```

Then:

```python
async def read_vav(vav_id):

    async with semaphore:
        return await read_from_bms(vav_id)
```

Aur TaskGroup:

```python
async with asyncio.TaskGroup() as tg:

    for vav_id in vav_ids:
        tg.create_task(read_vav(vav_id))
```

Architecture:

```text
TaskGroup
   ↓
1000 tasks
   ↓
Semaphore(10)
   ↓
10 active BMS requests
```

Ye production-style async architecture ke bohat qareeb hai.

---

# 23. TaskGroup + Queue

Aap producer-consumer architecture bhi bana sakte ho:

```text
TaskGroup
│
├── Producer 1
├── Producer 2
├── Consumer 1
└── Consumer 2
        │
        ↓
      Queue
```

Agar ek critical task fail ho:

```text
failure
 ↓
TaskGroup cancellation
 ↓
related tasks cancelled
```

Yani Queue aur TaskGroup ek doosre ke alternatives nahi hain.

Dono different problems solve karte hain:

```text
Queue → data flow
TaskGroup → task lifecycle
```

---

# 24. `create_task()` kab use karna?

`asyncio.create_task()` still useful hai.

For example:

```python
task = asyncio.create_task(background_operation())
```

Aap intentionally task ko manage karna chahte ho.

Lekin jab multiple related child tasks hain:

```python
async with asyncio.TaskGroup() as tg:
```

structured concurrency generally clearer approach hoti hai.

---

# 25. TaskGroup ka biggest benefit

Traditional:

```text
create task
    ↓
remember task
    ↓
await task
    ↓
handle exception
    ↓
cancel siblings?
    ↓
wait for cancellation?
    ↓
cleanup?
```

TaskGroup:

```text
async with TaskGroup
        ↓
create related tasks
        ↓
group manages lifecycle
        ↓
failure handling
        ↓
cancellation
        ↓
cleanup
```

Yani:

> **Less manual lifecycle management.**

---

# 26. `TaskGroup` ko ek family samjho

Analogy:

```text
Parent operation
      │
      └── Family
          ├── Child A
          ├── Child B
          └── Child C
```

Agar family ka ek critical child operation fail ho:

```text
failure
 ↓
parent handles group
 ↓
siblings may be cancelled
 ↓
all children accounted for
```

Ye structured concurrency ka mental model hai.

---

# 27. `TaskGroup` vs `ThreadPoolExecutor`

Ye bilkul different abstraction levels hain.

### TaskGroup

```text
asyncio
 ↓
coroutines/tasks
 ↓
event loop
```

### ThreadPoolExecutor

```text
concurrent.futures
 ↓
OS threads
 ↓
blocking/synchronous functions
```

TaskGroup automatically threads create nahi karta.

---

# 28. TaskGroup vs ProcessPoolExecutor

Same:

```text
TaskGroup
    ↓
async tasks
```

versus:

```text
ProcessPoolExecutor
    ↓
process workers
```

Agar async program mein CPU-heavy blocking work karna ho, aage hum executor integration bhi dekhenge.

---

# 29. Ek complete mental map

Ab tak:

```text
Concurrency
│
├── threading
│   ├── Lock
│   ├── Semaphore
│   ├── Event
│   ├── Condition
│   └── Queue
│
├── multiprocessing
│   ├── Process
│   ├── Queue
│   ├── Pipe
│   ├── Manager
│   └── Shared Memory
│
├── concurrent.futures
│   ├── ThreadPoolExecutor
│   ├── ProcessPoolExecutor
│   └── Future
│
└── asyncio
    ├── Task
    ├── Queue
    ├── Lock
    ├── Semaphore
    ├── Event
    ├── Condition
    └── TaskGroup
```

---

# 30. TaskGroup ki 7 key baatein

### 1.

```python
asyncio.TaskGroup
```

Python 3.11+ feature hai.

### 2.

```python
async with asyncio.TaskGroup() as tg:
```

use hota hai.

### 3.

```python
tg.create_task(...)
```

se child task create hoti hai.

### 4.

Group exit se pehle child tasks managed hoti hain.

### 5.

Ek task ki failure sibling tasks ki cancellation trigger kar sakti hai.

### 6.

Multiple exceptions `ExceptionGroup` mein aggregate ho sakti hain.

### 7.

`except*` se exception groups ko selectively handle kiya ja sakta hai.

---

# 31. Final memory trick

```text
TaskGroup = "Tasks ko family/group mein rakho."
```

```text
create_task()
    ↓
individual task
```

```text
TaskGroup
    ↓
related tasks
    ↓
structured lifecycle
    ↓
failure handling
    ↓
cancellation
    ↓
cleanup
```

### One-line difference:

> **`gather()` ka focus concurrent awaitables ke results par hai; `TaskGroup` ka focus related tasks ki structured lifecycle, cancellation aur exception management par hai.**

**Next Lesson 97:** `asyncio.timeout`, `asyncio.wait_for`, aur `asyncio.shield` — yani **async operations ko timeout dena, cancel karna, aur cancellation se protect karna**.
# Lesson 97 — `asyncio.timeout()`, `wait_for()`, `shield()`

## Async Timeout + Cancellation Control

Ab hum `asyncio` ka bohat practical topic parhte hain:

```text
Timeout
Cancellation
Protection from cancellation
```

Real applications mein ye bohat important hain, especially:

* API calls
* BMS/HVAC communication
* Database queries
* Network requests
* Device responses
* Background tasks

Basic problem:

> Agar koi async operation forever wait karne lage to kya karna hai?

---

# 1. Timeout ki zarurat kyun?

Suppose:

```python
await read_from_bms()
```

Aur BMS response nahi de raha.

Agar timeout nahi hai:

```text
Application
   ↓
BMS request
   ↓
WAIT...
   ↓
WAIT...
   ↓
WAIT...
   ↓
???
```

Program indefinitely wait kar sakta hai, depending on the underlying operation.

Humein kehna hai:

> **Maximum 5 seconds wait karo.**

Yahan `asyncio.timeout()` useful hai.

---

# 2. `asyncio.timeout()`

Python 3.11+ mein:

```python
asyncio.timeout()
```

available hai.

Basic syntax:

```python
async with asyncio.timeout(5):
    await operation()
```

Meaning:

> Is async context ke andar maximum 5 seconds allow hain.

---

# 3. Simple example

```python
import asyncio


async def slow_operation():
    await asyncio.sleep(10)
    return "Done"


async def main():

    try:
        async with asyncio.timeout(3):
            result = await slow_operation()

            print(result)

    except TimeoutError:
        print("Operation timed out")


asyncio.run(main())
```

Yahan:

```text
Operation = 10 sec
Timeout = 3 sec
```

Result:

```text
3 sec
 ↓
timeout
 ↓
operation cancelled
 ↓
TimeoutError
```

---

# 4. `asyncio.timeout()` ka mental model

```text
async with timeout(5)
        │
        ↓
   operation
        │
        ├── finishes before 5 sec
        │       ↓
        │     success
        │
        └── exceeds 5 sec
                ↓
             cancel
                ↓
          TimeoutError
```

---

# 5. Timeout ka actual mechanism

Ye important hai.

Timeout sirf:

```text
"clock check"
```

nahi karta.

Jab deadline expire hoti hai, current task ko cancellation ke through interrupt kiya jata hai.

Concept:

```text
Task
 ↓
await operation()
 ↓
timeout expires
 ↓
Task cancellation
 ↓
operation interrupted
 ↓
TimeoutError
```

Isliye timeout aur cancellation closely related hain.

---

# 6. `CancelledError` vs `TimeoutError`

Ye distinction important hai.

### Direct cancellation

```python
task.cancel()
```

Task ko:

```python
asyncio.CancelledError
```

mil sakta hai.

### Timeout context

```python
async with asyncio.timeout(5):
    ...
```

Deadline expire hone par outer code ko:

```python
TimeoutError
```

milta hai.

Simple:

```text
task.cancel()
    ↓
CancelledError

timeout expires
    ↓
cancellation internally
    ↓
TimeoutError externally
```

---

# 7. `asyncio.wait_for()`

Ab doosra timeout API:

```python
asyncio.wait_for()
```

Syntax:

```python
await asyncio.wait_for(
    operation(),
    timeout=5
)
```

Example:

```python
import asyncio


async def slow_operation():
    await asyncio.sleep(10)
    return "Done"


async def main():

    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=3
        )

        print(result)

    except TimeoutError:
        print("Timed out")


asyncio.run(main())
```

---

# 8. `timeout()` vs `wait_for()`

Dono timeout ke liye hain, lekin style different hai.

### `wait_for()`

Ek specific awaitable ko timeout:

```python
await asyncio.wait_for(
    operation(),
    timeout=5
)
```

### `timeout()`

Ek poore block ko deadline:

```python
async with asyncio.timeout(5):
    await operation_a()
    await operation_b()
```

---

# 9. Example difference

### `wait_for()`

```python
result = await asyncio.wait_for(
    read_ahu(),
    timeout=5
)
```

Basically:

> Sirf `read_ahu()` ko timeout do.

---

### `timeout()`

```python
async with asyncio.timeout(5):

    await read_ahu()

    await process_data()

    await save_data()
```

Meaning:

> Is **poore block** ki deadline 5 seconds hai.

---

# 10. Important example

Suppose:

```text
read_ahu = 2 sec
process = 2 sec
save = 2 sec
```

Total:

```text
6 sec
```

If:

```python
async with asyncio.timeout(5):
```

then total block 5 seconds se exceed nahi kar sakta.

Concept:

```text
0 sec → read
2 sec → process
4 sec → save
5 sec → timeout
```

---

# 11. `wait_for()` nested operations

Suppose:

```python
await asyncio.wait_for(
    read_bms(),
    timeout=5
)
```

Sirf BMS operation protected hai.

Baad ka code:

```python
process_data()
```

us timeout ke scope mein automatically nahi aata.

Ye major conceptual difference hai.

---

# 12. `asyncio.timeout()` ka advantage

Agar function mein multiple awaits hain:

```python
async with asyncio.timeout(10):

    data = await fetch_data()

    processed = await process(data)

    await save(processed)
```

Aap ek common deadline enforce kar sakte ho.

Ye large async workflows mein bohat useful hai.

---

# 13. Timeout object ko variable mein rakhna

Aap timeout context ko variable mein bhi capture kar sakte ho:

```python
async with asyncio.timeout(10) as cm:
    await operation()
```

Phir:

```python
cm.expired()
```

se check kiya ja sakta hai ke timeout expire hua ya nahi.

Concept:

```text
timeout context
      ↓
   Timeout
      ↓
 expired()?
```

---

# 14. Timeout reschedule

Advanced feature:

```python
async with asyncio.timeout(None) as cm:

    # later determine deadline
    cm.reschedule(...)
```

Yani timeout ko initially unset rakh kar later deadline set ki ja sakti hai.

Ye useful ho sakta hai jab timeout value runtime mein determine hoti hai.

---

# 15. Nested timeout

Timeout contexts nest bhi ho sakte hain.

Concept:

```python
async with asyncio.timeout(10):

    async with asyncio.timeout(3):
        await operation()
```

Inner timeout:

```text
3 sec
```

outer:

```text
10 sec
```

Jo relevant deadline pehle hit hogi uska effect hoga.

---

# 16. Ab `asyncio.shield()`

Ab interesting concept.

```python
asyncio.shield()
```

ka purpose:

> **Outer task cancellation se kisi awaitable ko protect karna.**

Syntax:

```python
await asyncio.shield(task)
```

---

# 17. Shield ka simple idea

Normally:

```text
Parent Task
   ↓
Child operation
```

Parent cancel:

```text
Parent cancelled
   ↓
Child may be cancelled
```

Shield:

```text
Parent Task
   ↓
shield()
   ↓
Child operation
```

Parent cancellation:

```text
Parent cancelled
      ↓
shield protects child
      ↓
child can continue
```

---

# 18. Basic example

```python
import asyncio


async def important_work():

    print("Important work started")

    await asyncio.sleep(5)

    print("Important work finished")


async def main():

    task = asyncio.create_task(
        important_work()
    )

    try:
        await asyncio.shield(task)

    except asyncio.CancelledError:
        print("Parent cancelled")

    await task


asyncio.run(main())
```

Concept:

```text
Parent
  ↓
shield
  ↓
Important Task

Parent cancelled
  ↓
shield prevents child cancellation
  ↓
child continues
```

---

# 19. Shield ka important misconception

`shield()` ka matlab:

> "Cancellation impossible ho gayi."

**Nahi.**

Shield sirf particular outer cancellation propagation ko protect karta hai.

Agar protected task ko directly cancel kar do:

```python
task.cancel()
```

to shield usko magically save nahi karta.

---

# 20. Shield ka diagram

```text
             cancellation
                  ↓
Parent Task ────────────────X
       │
       ↓
    shield()
       │
       ↓
Protected Task ─────────→ continues
```

Lekin:

```text
Direct cancellation
       ↓
Protected Task.cancel()
       ↓
Task cancelled
```

Shield direct cancellation ko block nahi karta.

---

# 21. Real-world HVAC example

Suppose system ko shutdown signal mil gaya:

```text
Application shutting down
```

Lekin ek critical operation:

```text
save_current_equipment_state()
```

abhi chal rahi hai.

Aap chahte ho ke parent cancellation ke bawajood ye important operation complete karne ki koshish kare.

Concept:

```python
await asyncio.shield(
    save_current_equipment_state()
)
```

Yani:

```text
Shutdown
   ↓
Parent cancelled
   ↓
Critical save
   ↓
continue
```

**Lekin** shutdown design mein indefinite shielding dangerous ho sakti hai, isliye critical work ko apni bounded timeout/deadline dena sensible hai.

---

# 22. Shield + timeout

Ye interesting combination hai.

```python
async with asyncio.timeout(10):

    await asyncio.shield(
        important_operation()
    )
```

Yahan aapko cancellation/deadline semantics carefully samajhni hoti hain.

Outer task timeout ho sakta hai, jabke shielded task background mein continue kar sakta hai.

Isliye shield use karte waqt task reference/lifecycle properly manage karna important hai.

---

# 23. `wait_for()` + `shield()`

Suppose:

```python
task = asyncio.create_task(
    important_operation()
)
```

Then:

```python
try:
    await asyncio.wait_for(
        asyncio.shield(task),
        timeout=3
    )

except TimeoutError:
    print("Wait timeout")
```

Important:

Timeout outer waiting operation ko affect kar sakta hai, jabke `shield` underlying task ko cancellation se protect kar sakta hai.

So:

```text
wait_for
   ↓
shield
   ↓
task
```

Ye powerful but advanced pattern hai.

---

# 24. Timeout vs Shield

Dono opposite-looking concerns solve karte hain:

### Timeout

```text
"Kitni der wait karna hai?"
```

### Shield

```text
"Cancellation se kis operation ko protect karna hai?"
```

---

# 25. `timeout()` vs `wait_for()` vs `shield()`

| Feature              | Purpose                       |
| -------------------- | ----------------------------- |
| `asyncio.timeout()`  | Block/deadline control        |
| `asyncio.wait_for()` | Specific awaitable timeout    |
| `asyncio.shield()`   | Outer cancellation se protect |

Memory:

```text
timeout()  → deadline
wait_for() → one awaitable timeout
shield()   → cancellation protection
```

---

# 26. Cancellation ka complete picture

Ab tak:

```text
Task
 ↓
await
 ↓
running
```

Cancellation:

```text
task.cancel()
 ↓
CancelledError
 ↓
cleanup
 ↓
raise
```

Timeout:

```text
deadline
 ↓
cancel current task
 ↓
TimeoutError externally
```

Shield:

```text
outer cancellation
 ↓
shield
 ↓
protected awaitable continues
```

---

# 27. `try/finally` ka role

Async cancellation mein cleanup bohat important hai.

Example:

```python
async def worker():

    try:
        await do_work()

    finally:
        await cleanup()
```

Agar cancellation aaye:

```text
do_work()
   ↓
CancelledError
   ↓
finally
   ↓
cleanup()
```

Isliye resource cleanup ke liye:

```python
finally:
```

bohat important hai.

---

# 28. `CancelledError` ko swallow karna

Bad pattern:

```python
async def worker():

    try:
        await operation()

    except asyncio.CancelledError:
        pass
```

Isse cancellation properly propagate nahi hoti.

Usually better:

```python
async def worker():

    try:
        await operation()

    except asyncio.CancelledError:
        await cleanup()
        raise
```

---

# 29. Timeout + cleanup

Example:

```python
async def read_bms():

    try:
        return await actual_bms_request()

    finally:
        print("Cleanup")
```

Then:

```python
try:
    async with asyncio.timeout(5):
        data = await read_bms()

except TimeoutError:
    print("BMS timeout")
```

Flow:

```text
BMS request
   ↓
5 sec
   ↓
timeout
   ↓
cancellation
   ↓
finally cleanup
   ↓
TimeoutError
```

---

# 30. HVAC architecture example

Suppose:

```text
BMS API
   ↓
Read AHU
   ↓
Process
   ↓
Save DB
```

Aap overall deadline:

```python
async with asyncio.timeout(15):
```

rakh sakte ho.

API request individually:

```python
await asyncio.wait_for(
    read_bms(),
    timeout=5
)
```

Aur critical state save ko:

```python
await asyncio.shield(
    save_state()
)
```

se protect kar sakte ho — agar architecture ko cancellation ke bawajood save complete karwana ho.

---

# 31. Lekin shield ka overuse mat karo

Agar har operation:

```python
asyncio.shield(...)
```

ho:

```text
Cancellation
   ↓
tasks continue
   ↓
shutdown slow
   ↓
background work remains
```

Ye application shutdown ko problematic bana sakta hai.

Shield sirf un operations ke liye use karo jinko specific cancellation semantics chahiye.

---

# 32. Timeout ka overuse bhi mat karo

Har operation ko random timeout:

```text
1 sec
1 sec
1 sec
```

dena bhi correct nahi.

Timeout workload ke nature ke according choose karna chahiye:

```text
Fast API → short timeout
Slow report → longer timeout
Critical operation → explicit deadline
```

---

# 33. `TaskGroup` + timeout

Previous lesson se connect karo:

```python
async with asyncio.timeout(30):

    async with asyncio.TaskGroup() as tg:

        tg.create_task(task_a())
        tg.create_task(task_b())
        tg.create_task(task_c())
```

Architecture:

```text
30-second deadline
       ↓
TaskGroup
 ├── A
 ├── B
 └── C
```

Agar overall timeout expire:

```text
timeout
 ↓
cancellation
 ↓
TaskGroup tasks handled/cancelled
 ↓
TimeoutError
```

Ye modern async architecture ka powerful pattern hai.

---

# 34. TaskGroup + timeout + semaphore

Ab Lesson 95–97 combine:

```text
                  timeout
                     │
                TaskGroup
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
        Task       Task       Task
          │          │          │
          └──────────┼──────────┘
                     ↓
               Semaphore(10)
                     ↓
                 BMS API
```

Real HVAC/BMS monitoring system mein ye architecture practical ho sakta hai.

---

# 35. `timeout()` aur `wait_for()` ka deeper difference

### `wait_for()`

Specific awaitable:

```python
await asyncio.wait_for(
    operation(),
    5
)
```

### `timeout()`

Scope:

```python
async with asyncio.timeout(5):
    ...
```

Isliye modern code mein jab **whole operation scope** ki deadline define karni ho to `asyncio.timeout()` often cleaner hota hai.

---

# 36. Final memory map

```text
asyncio
│
├── Lock
│     ↓
│   one task
│
├── Semaphore
│     ↓
│   max N tasks
│
├── Event
│     ↓
│   signal
│
├── Condition
│     ↓
│   state condition
│
├── Queue
│     ↓
│   producer/consumer
│
├── TaskGroup
│     ↓
│   structured task lifecycle
│
├── timeout
│     ↓
│   deadline
│
├── wait_for
│     ↓
│   awaitable timeout
│
└── shield
      ↓
   cancellation protection
```

---

# 37. Lesson 97 ki one-line memory

> **`timeout()` = deadline, `wait_for()` = specific awaitable ka timeout, `shield()` = outer cancellation se protected awaitable.**

Aur cancellation ka golden pattern:

```python
try:
    await operation()

except asyncio.CancelledError:
    await cleanup()
    raise
```

**Next Lesson 98:** **Async Context Managers + Async Iterators Deeply** — `async with`, `__aenter__`, `__aexit__`, `async for`, `__aiter__`, `__anext__`, async generators, aur inka real-world connection database/BMS/network resources ke saath.
# Lesson 98 — Async Context Managers + Async Iterators Deeply

Ab hum `asyncio` ke do bohat important Python protocols parhte hain:

```text
async with
async for
```

Inka connection directly **OOP + magic methods + resource management + asynchronous programming** se hai.

---

# 1. Pehle normal versions yaad karo

Normal context manager:

```python
with resource:
    ...
```

iske peeche:

```python
__enter__()
__exit__()
```

Normal iterator:

```python
for item in obj:
    ...
```

iske peeche:

```python
__iter__()
__next__()
```

Async versions:

```text
with
 ↓
__enter__ / __exit__

async with
 ↓
__aenter__ / __aexit__

for
 ↓
__iter__ / __next__

async for
 ↓
__aiter__ / __anext__
```

Yahi is lesson ka foundation hai.

---

# 2. `async with`

Syntax:

```python
async with resource:
    await operation()
```

Iska matlab hai:

> Resource ko asynchronously acquire karo aur block complete hone par asynchronously release karo.

Example:

```python
async with connection:
    await connection.execute()
```

---

# 3. `__aenter__()` aur `__aexit__()`

Agar class ko `async with` ke saath use karna hai:

```python
class Resource:

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc, tb):
        ...
```

Ye exactly normal context manager ka async equivalent hai.

---

# 4. Simple example

```python
import asyncio


class Connection:

    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(1)
        print("Connected")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("Closing...")
        await asyncio.sleep(1)
        print("Closed")


async def main():

    async with Connection() as conn:
        print("Using connection")


asyncio.run(main())
```

Output conceptually:

```text
Connecting...
Connected
Using connection
Closing...
Closed
```

---

# 5. `as conn` kya hai?

Yahan:

```python
async with Connection() as conn:
```

`conn` actually `__aenter__()` ka return value hota hai.

Concept:

```python
value = await obj.__aenter__()
```

Isliye:

```python
async def __aenter__(self):
    return self
```

common pattern hai.

---

# 6. Internally kya ho raha hai?

Ye:

```python
async with Connection() as conn:
    await conn.read()
```

conceptually roughly:

```python
manager = Connection()

conn = await manager.__aenter__()

try:
    await conn.read()

finally:
    await manager.__aexit__(...)
```

Exact language-level semantics thori zyada nuanced hain, lekin mental model ke liye ye bohat useful hai.

---

# 7. `__aexit__()` ke 3 arguments

```python
async def __aexit__(self, exc_type, exc, tb):
    ...
```

Arguments:

```text
exc_type → exception ki type
exc      → exception object
tb       → traceback
```

Agar koi exception nahi:

```text
exc_type = None
exc = None
tb = None
```

---

# 8. Exception example

```python
class Resource:

    async def __aenter__(self):
        print("Acquire")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("Release")

        if exc:
            print("Exception:", exc)
```

Use:

```python
async with Resource():
    raise ValueError("Something went wrong")
```

Flow:

```text
__aenter__()
     ↓
body
     ↓
ValueError
     ↓
__aexit__()
```

Important:

> Exception aaye tab bhi cleanup ho sakta hai.

Yahi context manager ka major benefit hai.

---

# 9. Exception suppress karna

`__aexit__()` agar:

```python
return True
```

return kare to exception suppress ho sakti hai.

Example:

```python
class Resource:

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):

        if exc:
            print("Handled:", exc)

        return True
```

Then:

```python
async with Resource():
    raise ValueError("Error")
```

Exception bahar propagate nahi hogi.

Lekin practical code mein **exceptions blindly suppress nahi karni chahiye**.

Usually:

```python
return False
```

ya simply:

```python
return None
```

better hai.

---

# 10. Async context manager ka real use

Ye especially useful hai jab resource acquire/release operations khud asynchronous hon.

Examples:

```text
Database connection
HTTP session
Network connection
WebSocket
Async file
Connection pool
BMS connection
Device session
```

---

# 11. HVAC/BMS example

Suppose BMS connection:

```python
class BMSConnection:

    async def __aenter__(self):
        print("Connecting to BMS...")
        await connect_to_bms()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("Disconnecting BMS...")
        await disconnect_from_bms()
```

Use:

```python
async with BMSConnection() as bms:

    ahu = await bms.read("AHU-01")
    vav = await bms.read("VAV-101")
```

Aapko manually:

```python
connect()
try:
    ...
finally:
    disconnect()
```

nahi likhna padta.

---

# 12. Normal vs Async Context Manager

| Normal          | Async            |
| --------------- | ---------------- |
| `with`          | `async with`     |
| `__enter__()`   | `__aenter__()`   |
| `__exit__()`    | `__aexit__()`    |
| normal function | `async def`      |
| `return`        | `await` possible |

Important:

`async with` ka matlab sirf ye nahi ke class asynchronous hai.

Actual requirement hai ke **enter/exit operations awaitable hon**.

---

# 13. `async for`

Ab second protocol:

```python
async for item in source:
    ...
```

Normal:

```python
for item in source:
```

Async:

```python
async for item in source:
```

---

# 14. Normal iterator ka model

Normal:

```python
for item in obj:
    print(item)
```

uses:

```python
__iter__()
__next__()
```

Async:

```python
async for item in obj:
    print(item)
```

uses:

```python
__aiter__()
__anext__()
```

---

# 15. Async iterator class

Example:

```python
class Counter:

    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __aiter__(self):
        return self

    async def __anext__(self):

        if self.current >= self.limit:
            raise StopAsyncIteration

        self.current += 1

        await asyncio.sleep(1)

        return self.current
```

Use:

```python
async def main():

    async for number in Counter(3):
        print(number)
```

Output:

```text
1
2
3
```

Lekin har value ke beech async wait possible hai.

---

# 16. `__aiter__()`

```python
def __aiter__(self):
    return self
```

Ye async iterator return karta hai.

Modern Python mein normally `__aiter__()` khud `async def` nahi hota.

Important distinction:

```python
def __aiter__(self):
    return self
```

Then:

```python
async def __anext__(self):
    ...
```

---

# 17. `__anext__()`

Ye actual next item produce karta hai:

```python
async def __anext__(self):
    ...
```

Agar item available hai:

```python
return item
```

Agar items finish:

```python
raise StopAsyncIteration
```

Bilkul normal iterator ke equivalent:

```text
normal iterator:
StopIteration

async iterator:
StopAsyncIteration
```

---

# 18. `async for` internally

Ye:

```python
async for item in obj:
    process(item)
```

mental model mein:

```python
iterator = obj.__aiter__()

while True:

    try:
        item = await iterator.__anext__()

    except StopAsyncIteration:
        break

    process(item)
```

Yahan sabse important point:

```python
await iterator.__anext__()
```

Isliye async iterator slow/network-based sources ke liye useful hai.

---

# 19. Normal iterator vs async iterator

### Normal:

```python
for x in data:
```

```text
next()
 ↓
immediate value
```

### Async:

```python
async for x in data:
```

```text
await next()
 ↓
wait for asynchronous data
 ↓
value
```

---

# 20. Real-world example — API stream

Suppose server gradually data send karta hai:

```text
Server
 ↓
Data 1
 ↓
wait
 ↓
Data 2
 ↓
wait
 ↓
Data 3
```

Aap:

```python
async for data in stream:
    process(data)
```

kar sakte ho.

Aapko poora response memory mein load karne ki zarurat nahi.

---

# 21. HVAC example — live BMS readings

Imagine:

```text
BMS
 ↓
AHU reading
 ↓
wait
 ↓
VAV reading
 ↓
wait
 ↓
Temperature
 ↓
wait
```

Async iterator:

```python
async for reading in bms_stream():

    print(reading)
```

Ye continuously asynchronous readings consume kar sakta hai.

---

# 22. Async generator

Python mein async iterator manually banana zaroori nahi.

Aap **async generator** use kar sakte ho.

Syntax:

```python
async def counter():

    for i in range(5):

        await asyncio.sleep(1)

        yield i
```

Use:

```python
async for value in counter():
    print(value)
```

Ye bohat important shortcut hai.

---

# 23. `async def` + `yield`

Normal generator:

```python
def generator():
    yield 1
    yield 2
```

Async generator:

```python
async def generator():
    yield 1
    await something()
    yield 2
```

Difference:

```text
generator
    ↓
yield

async generator
    ↓
await + yield
```

---

# 24. Async generator ka mental model

```text
async generator
      ↓
  async for
      ↓
  __aiter__()
      ↓
  __anext__()
      ↓
 await
      ↓
   value
```

Python automatically required async iteration machinery handle karta hai.

---

# 25. `yield` vs `return`

Generator:

```python
yield value
```

ka matlab:

> Value do, lekin generator ko completely finish mat karo.

`return`:

```python
return
```

ka matlab generator finish.

Async generator bhi isi concept ko follow karta hai.

---

# 26. Async generator ka practical example

```python
import asyncio


async def temperature_stream():

    temperatures = [22.1, 22.4, 22.8, 23.0]

    for temp in temperatures:

        await asyncio.sleep(1)

        yield temp


async def main():

    async for temp in temperature_stream():

        print("Temperature:", temp)


asyncio.run(main())
```

Output gradually:

```text
Temperature: 22.1
Temperature: 22.4
Temperature: 22.8
Temperature: 23.0
```

---

# 27. Ye `list` se different kyun?

Agar:

```python
temperatures = [1000000 values]
```

to list mein sab values memory mein ho sakti hain.

Async generator:

```python
async for temp in temperature_stream():
```

values ko gradually produce kar sakta hai.

Mental model:

```text
List:
ALL DATA → memory

Generator:
one item → process
one item → process
one item → process
```

---

# 28. Async generator + real-time data

Suppose:

```python
async def bms_stream():

    while True:

        reading = await read_bms()

        yield reading
```

Then:

```python
async for reading in bms_stream():

    process(reading)
```

Architecture:

```text
BMS
 ↓
await read
 ↓
yield reading
 ↓
async for
 ↓
process
 ↓
await next reading
```

Ye monitoring systems mein bohat natural pattern hai.

---

# 29. `async with` + `async for`

Ab dono protocols combine karte hain.

```python
async with BMSConnection() as bms:

    async for reading in bms.stream():

        print(reading)
```

Yahan:

```text
async with
   ↓
connection lifecycle

async for
   ↓
stream lifecycle
```

Ye extremely useful async architecture hai.

---

# 30. Full conceptual architecture

```text
Application
     │
     ▼
async with BMSConnection()
     │
     ▼
Connection acquired
     │
     ▼
async for reading
     │
     ├── AHU
     ├── VAV
     ├── Temperature
     └── Pressure
     │
     ▼
Connection released
```

---

# 31. Async context manager + timeout

Previous lesson bhi connect kar sakte hain:

```python
async with BMSConnection() as bms:

    async with asyncio.timeout(10):

        data = await bms.read("AHU-01")
```

Ab:

```text
BMS connection
      ↓
10 sec deadline
      ↓
read AHU
```

---

# 32. Async iterator + timeout

Aap stream ke individual operation ko bhi timeout de sakte ho, architecture ke hisaab se.

Concept:

```python
async for reading in stream:

    try:
        async with asyncio.timeout(5):
            await process(reading)

    except TimeoutError:
        print("Processing timeout")
```

---

# 33. Async iterator aur Queue ka connection

Previous lessons mein `asyncio.Queue` dekhi thi.

Producer:

```python
async def producer(queue):

    while True:

        reading = await read_bms()

        await queue.put(reading)
```

Consumer:

```python
async def consumer(queue):

    while True:

        reading = await queue.get()

        try:
            process(reading)
        finally:
            queue.task_done()
```

Async generator kabhi-kabhi isi producer-stream problem ko simpler bana sakta hai:

```python
async def readings():

    while True:
        yield await read_bms()
```

Then:

```python
async for reading in readings():
    process(reading)
```

---

# 34. Kab Queue aur kab async generator?

### Async generator

Jab:

```text
one producer
→ sequential consumption
```

simple stream chahiye.

### Queue

Jab:

```text
multiple producers
→ buffering
→ multiple consumers
→ backpressure
```

chahiye.

Example:

```text
Multiple BMS producers
        ↓
      Queue
        ↓
Multiple consumers
```

Queue zyada appropriate ho sakti hai.

---

# 35. Async context manager ka OOP connection

Aap pehle protocols parh chuke ho:

```text
Callable
Iterable
Iterator
Mapping
Sequence
```

Ab:

```text
Context Manager
Async Context Manager
Async Iterator
```

Protocols ka basic idea same hai:

> Object ko particular behavior provide karna hai to required special methods implement karo.

---

# 36. Protocol map

```text
obj()
 ↓
__call__()

for x in obj
 ↓
__iter__ + __next__

with obj
 ↓
__enter__ + __exit__

async for x in obj
 ↓
__aiter__ + __anext__

async with obj
 ↓
__aenter__ + __aexit__
```

Ye Python data model ka bohat important part hai.

---

# 37. Ek aur important distinction

`async with` ka matlab:

```text
resource acquisition/release asynchronous hai
```

`async for` ka matlab:

```text
next item obtain karna asynchronous hai
```

Dono ka purpose different hai.

---

# 38. Quick comparison

| Syntax       | Protocol                  | Purpose         |
| ------------ | ------------------------- | --------------- |
| `with`       | `__enter__`, `__exit__`   | sync resource   |
| `async with` | `__aenter__`, `__aexit__` | async resource  |
| `for`        | `__iter__`, `__next__`    | sync iteration  |
| `async for`  | `__aiter__`, `__anext__`  | async iteration |

---

# 39. Common mistake #1

Galat:

```python
async with open("data.txt") as f:
    ...
```

Normal `open()` normal file object deta hai, async context manager nahi.

Async file libraries mein async-specific APIs use hoti hain.

Concept:

```text
normal resource → with
async resource  → async with
```

---

# 40. Common mistake #2

Galat:

```python
for item in async_iterator:
    ...
```

Agar object asynchronous iterator hai to:

```python
async for item in async_iterator:
```

use karo.

---

# 41. Common mistake #3

Async iterator mein:

```python
async def __aiter__(self):
```

modern Python ke normal async-iterator protocol ke liye generally wrong pattern hai.

Usually:

```python
def __aiter__(self):
    return self
```

aur:

```python
async def __anext__(self):
    ...
```

---

# 42. Common mistake #4

Async code ke andar:

```python
time.sleep(5)
```

Ye event loop block karega.

Instead:

```python
await asyncio.sleep(5)
```

Use karo.

Difference:

```text
time.sleep()
 ↓
event loop blocked

asyncio.sleep()
 ↓
control event loop ko return
```

---

# 43. Advanced OOP mental model

Python object ko sirf attributes/methods ka collection mat samjho.

Object **protocols implement** karta hai.

Example:

```text
Object
 │
 ├── callable?
 │      __call__
 │
 ├── iterable?
 │      __iter__
 │
 ├── context manager?
 │      __enter__/__exit__
 │
 ├── async iterable?
 │      __aiter__/__anext__
 │
 └── async context manager?
        __aenter__/__aexit__
```

Python phir syntax ke through automatically correct protocol invoke karta hai.

---

# 44. Final mental map

```text
                    Python Object
                         │
          ┌──────────────┴──────────────┐
          │                             │
       Sync                           Async
          │                             │
   ┌──────┴──────┐              ┌───────┴────────┐
   │             │              │                │
  with          for         async with        async for
   │             │              │                │
__enter__     __iter__      __aenter__       __aiter__
__exit__      __next__      __aexit__        __anext__
```

### Golden memory:

> **`async with` resource lifecycle ko asynchronous banata hai, aur `async for` iteration ko asynchronous banata hai.**

Aur dono ka asli foundation **Python Data Model / OOP protocols** hain.

**Next Lesson 99:** `asyncio` ko **threads aur processes ke saath mix karna** — `run_in_executor()`, `to_thread()`, CPU-bound vs I/O-bound work, event loop ko block hone se bachana, aur real BMS/HVAC architecture.
# Lesson 99 — `asyncio` + Threads + Processes

Ab hum ek bohat important real-world topic par hain:

```text
asyncio
   │
   ├── Thread
   │
   └── Process
```

Ye samajhna zaroori hai kyun ke **asyncio har type ke kaam ke liye suitable nahi hota**.

---

# 1. Problem kya hai?

Maan lo aapka async application ye kaam kar raha hai:

```python
async def main():
    await read_bms()
    await read_database()
    await read_api()
```

Ye asynchronous hai.

Lekin achanak aapke paas ek **normal blocking function** aa jata hai:

```python
def old_library():
    time.sleep(10)
```

Agar aap isko directly async function mein chala do:

```python
async def main():
    old_library()
```

to problem hogi.

### Kyun?

```text
Event Loop
    │
    ├── Task A
    ├── Task B
    ├── Task C
    │
    └── old_library()
           ↓
       BLOCK 10 sec
```

Event loop dusre tasks ko properly run nahi kar paega.

---

# 2. Golden rule

Async application mein:

> **Event loop ke andar blocking operation directly mat chalao.**

Blocking operation ko:

```text
Thread
```

ya

```text
Process
```

mein bhejo.

---

# 3. `asyncio.to_thread()`

Modern Python mein easiest solution:

```python
await asyncio.to_thread(function)
```

Example:

```python
import asyncio
import time


def blocking_work():
    time.sleep(5)
    return "Done"


async def main():

    result = await asyncio.to_thread(blocking_work)

    print(result)


asyncio.run(main())
```

Yahan:

```text
asyncio
   ↓
to_thread()
   ↓
Thread
   ↓
blocking_work()
```

Event loop directly block nahi hota.

---

# 4. Arguments kaise pass karein?

```python
def read_equipment(equipment_id):
    time.sleep(2)
    return f"Reading {equipment_id}"
```

Async:

```python
result = await asyncio.to_thread(
    read_equipment,
    "AHU-01"
)
```

Equivalent concept:

```python
await asyncio.to_thread(function, arg1, arg2)
```

---

# 5. Multiple blocking functions

Maan lo:

```python
async def main():

    results = await asyncio.gather(
        asyncio.to_thread(read_equipment, "AHU-01"),
        asyncio.to_thread(read_equipment, "AHU-02"),
        asyncio.to_thread(read_equipment, "AHU-03"),
    )

    print(results)
```

Architecture:

```text
                 asyncio
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Thread     Thread    Thread
       AHU-01     AHU-02    AHU-03
```

Ye I/O-bound blocking functions ke liye useful hai.

---

# 6. `to_thread()` kab use karein?

Particularly:

```text
Blocking file operations
Legacy synchronous library
Blocking database client
Blocking HTTP library
Blocking SDK
OS/file operations
Network calls
```

Example:

```python
result = await asyncio.to_thread(
    legacy_library.read_data
)
```

---

# 7. `to_thread()` vs `ThreadPoolExecutor`

Aap pehle `ThreadPoolExecutor` parh chuke ho.

### Simple case:

```python
await asyncio.to_thread(func)
```

Easy.

### Advanced control:

```python
loop.run_in_executor(
    executor,
    func
)
```

`ThreadPoolExecutor` use kar sakte ho.

---

# 8. `run_in_executor()`

Classic asyncio mechanism:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor


def blocking_task():
    return "Done"


async def main():

    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(max_workers=4) as executor:

        result = await loop.run_in_executor(
            executor,
            blocking_task
        )

        print(result)


asyncio.run(main())
```

Flow:

```text
asyncio Event Loop
        │
        │ run_in_executor()
        ↓
ThreadPoolExecutor
        │
        ↓
blocking_task()
```

---

# 9. `to_thread()` vs `run_in_executor()`

|                       | `to_thread()`                | `run_in_executor()`     |
| --------------------- | ---------------------------- | ----------------------- |
| Simple                | ✅                            | ❌                       |
| Thread                | ✅                            | ✅                       |
| Custom executor       | ❌ directly                   | ✅                       |
| Modern convenient API | ✅                            | More low-level          |
| Context propagation   | designed for current context | depends on executor/use |

Simple rule:

> **Normal blocking function → `asyncio.to_thread()`**

Agar executor par detailed control chahiye:

> **`run_in_executor()`**

---

# 10. `to_thread()` ke peeche kya concept hai?

Mental model:

```text
await asyncio.to_thread(func)
```

roughly:

```text
Event Loop
    │
    ├── submit blocking function
    │
    ↓
Thread Pool
    │
    ↓
function()
    │
    ↓
result
    │
    ↓
await resumes
```

Aapka async task result ka wait karta hai, lekin event loop baaki tasks ko run kar sakta hai.

---

# 11. Important: Thread CPU problem solve nahi karta

Maan lo:

```python
def cpu_heavy():
    for i in range(100_000_000):
        ...
```

Aur:

```python
await asyncio.to_thread(cpu_heavy)
```

Kya ab CPU-bound Python magically parallel ho jayega?

**Normally nahi.**

Reason:

```text
CPython
   ↓
GIL
   ↓
Python bytecode
```

Thread I/O-bound blocking work ke liye useful hai, lekin pure Python CPU-heavy work ke liye process zyada appropriate hota hai.

---

# 12. CPU-bound work → Process

Example:

```python
from concurrent.futures import ProcessPoolExecutor
import asyncio


def cpu_heavy(n):
    return sum(i * i for i in range(n))


async def main():

    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:

        result = await loop.run_in_executor(
            executor,
            cpu_heavy,
            10_000_000
        )

        print(result)


asyncio.run(main())
```

Flow:

```text
Async Event Loop
       │
       ↓
ProcessPoolExecutor
       │
       ↓
Separate Process
       │
       ↓
CPU-heavy Python
```

---

# 13. Thread vs Process

Ye previous lessons ka important connection hai:

```text
                asyncio
                   │
          ┌────────┴────────┐
          │                 │
       Blocking I/O       CPU-heavy
          │                 │
          ↓                 ↓
        Thread            Process
```

### I/O-bound:

```python
await asyncio.to_thread(...)
```

### CPU-bound:

```python
ProcessPoolExecutor
```

---

# 14. `asyncio` khud CPU work nahi karta

Ye bohat important concept hai.

`asyncio` ka main strength:

```text
waiting efficiently
```

hai.

Example:

```python
await network_request()
```

CPU free hota hai jab network response ka wait ho raha ho.

Lekin:

```python
calculate_10_billion_numbers()
```

mein CPU busy hai.

Asyncio us CPU calculation ko automatically parallel nahi banata.

---

# 15. HVAC/BMS example

Maan lo aapke paas 500 VAVs hain.

BMS library synchronous hai:

```python
def read_vav(vav_id):
    # blocking BMS call
    ...
```

Aap async application bana rahe ho.

Wrong:

```python
async def monitor():

    for vav in vavs:
        reading = read_vav(vav)
```

Ye event loop ko block kar sakta hai.

Better:

```python
async def monitor():

    tasks = [
        asyncio.to_thread(read_vav, vav)
        for vav in vavs
    ]

    results = await asyncio.gather(*tasks)
```

Architecture:

```text
                 Asyncio
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Thread     Thread    Thread
          ↓         ↓         ↓
       VAV-01    VAV-02    VAV-03
```

---

# 16. Lekin 500 threads?

Yahan ek aur problem aa sakti hai.

Aap theoretically:

```python
500 tasks
```

create kar sakte ho.

Lekin BMS server ko:

```text
500 simultaneous requests
```

bhejna zaroori nahi.

Isliye previous lesson ka:

```python
asyncio.Semaphore()
```

use kar sakte ho.

Example:

```python
semaphore = asyncio.Semaphore(10)


async def read_vav(vav_id):

    async with semaphore:

        return await asyncio.to_thread(
            blocking_read_vav,
            vav_id
        )
```

Ab:

```text
500 VAV tasks
      ↓
Semaphore(10)
      ↓
maximum 10 concurrent calls
      ↓
BMS
```

Ye production architecture mein bohat useful pattern hai.

---

# 17. `TaskGroup` + `to_thread()`

Aap Lesson 96 ka `TaskGroup` bhi combine kar sakte ho:

```python
async def monitor(vavs):

    async with asyncio.TaskGroup() as tg:

        for vav in vavs:

            tg.create_task(
                asyncio.to_thread(
                    blocking_read_vav,
                    vav
                )
            )
```

Ab:

```text
TaskGroup
   │
   ├── Task → Thread
   ├── Task → Thread
   ├── Task → Thread
   └── Task → Thread
```

TaskGroup lifecycle manage karta hai.

Thread actual blocking function execute karta hai.

---

# 18. Semaphore + TaskGroup + Thread

Production-style mental model:

```text
                    TaskGroup
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
        Task           Task          Task
          │             │             │
          ↓             ↓             ↓
     Semaphore      Semaphore     Semaphore
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                    to_thread()
                        ↓
                     Threads
                        ↓
                      BMS
```

Ye powerful architecture hai.

---

# 19. `asyncio` + Process

Suppose BMS readings aa gayi:

```python
readings = [...]
```

Ab aapko heavy analytics karni hain:

```text
500,000 readings
       ↓
statistical calculation
       ↓
anomaly detection
       ↓
forecasting
```

Agar pure Python CPU-heavy hai:

```text
Asyncio
   ↓
ProcessPool
   ↓
CPU workers
```

---

# 20. Important data-transfer issue

Process alag memory use karta hai.

Isliye:

```python
ProcessPoolExecutor
```

mein arguments/results ko generally serialize/pickle karna padta hai.

Example:

```python
executor.submit(cpu_task, data)
```

mein `data` process boundary cross karega.

Isliye huge data repeatedly process ko bhejna expensive ho sakta hai.

---

# 21. Thread aur Process ka memory difference

```text
Threads:

Process
 ├── Thread 1
 ├── Thread 2
 └── Thread 3

Shared memory
```

Processes:

```text
Process 1
   └── Memory

Process 2
   └── Separate Memory

Process 3
   └── Separate Memory
```

Isliye thread mein shared-state race conditions ka concern zyada hota hai.

Process mein IPC/data transfer ka concern zyada hota hai.

---

# 22. `asyncio` + Thread + Process complete picture

```text
                       Application
                            │
                         asyncio
                            │
                 ┌──────────┴──────────┐
                 │                     │
             I/O waiting          Heavy CPU
                 │                     │
                 ↓                     ↓
              Thread               Process
                 │                     │
                 ↓                     ↓
        Blocking library       CPU calculation
```

---

# 23. Event loop ko kab block karte ho?

Ye code dangerous hai:

```python
async def main():

    time.sleep(10)
```

Kyun?

```text
Event Loop
   ↓
time.sleep()
   ↓
BLOCKED
```

Better:

```python
async def main():

    await asyncio.sleep(10)
```

Agar actual blocking function hai:

```python
await asyncio.to_thread(blocking_function)
```

---

# 24. Three types of waiting

Ye distinction yaad rakho:

### Async waiting

```python
await network_call()
```

Event loop other tasks chala sakta hai.

### Thread-based blocking

```python
await asyncio.to_thread(blocking_function)
```

Blocking function thread mein chala.

### Process-based CPU work

```text
ProcessPoolExecutor
```

Heavy CPU work separate process mein.

---

# 25. `to_thread()` aur cancellation

Ek subtle point:

```python
task = asyncio.create_task(
    asyncio.to_thread(blocking_function)
)
```

Agar async task cancel ho jaye, underlying already-running thread function ko arbitrary point par safely force-stop nahi kiya ja sakta.

Ye important hai.

```text
Async Task cancellation
        ≠
force kill thread
```

Isliye blocking function ideally:

* finite ho
* reasonable ho
* cancellation-sensitive design ho where possible

---

# 26. Process cancellation bhi alag concept hai

Process ko cancel karna:

```text
Future cancellation
```

aur:

```text
actual OS process terminate
```

same cheez nahi hain.

Agar process already running hai to `Future.cancel()` necessarily running process ko magically stop nahi karta.

Ye distinction production systems mein important hai.

---

# 27. `run_in_executor()` kab useful hai?

Suppose custom pool chahiye:

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(
    max_workers=20
)
```

Then:

```python
loop = asyncio.get_running_loop()

result = await loop.run_in_executor(
    executor,
    blocking_function
)
```

Aap pool size/control explicitly manage kar sakte ho.

---

# 28. Modern recommendation

Simple blocking function:

```python
await asyncio.to_thread(func)
```

Custom executor:

```python
await loop.run_in_executor(executor, func)
```

CPU-heavy:

```python
ProcessPoolExecutor
```

---

# 29. Complete BMS architecture

Imagine application ko:

1. BMS se readings leni hain
2. API calls karni hain
3. Data process karna hai
4. Database mein save karna hai

Architecture:

```text
                       asyncio
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ↓                  ↓                  ↓
    BMS I/O             API I/O          Database I/O
       │                  │                  │
       └──────────────┬───┴──────────────────┘
                      │
                      ↓
                  asyncio tasks
                      │
                      ↓
                 CPU-heavy work
                      │
                      ↓
               ProcessPoolExecutor
```

---

# 30. Golden decision table

| Work                               | Best approach         |
| ---------------------------------- | --------------------- |
| Async HTTP client                  | `asyncio`             |
| Async DB driver                    | `asyncio`             |
| Async BMS API                      | `asyncio`             |
| Blocking HTTP library              | `asyncio.to_thread()` |
| Blocking SDK                       | `asyncio.to_thread()` |
| Blocking file/library              | `asyncio.to_thread()` |
| Pure Python CPU-heavy              | `ProcessPoolExecutor` |
| Large CPU computation              | Process               |
| Many concurrent I/O tasks          | asyncio               |
| Need thread-specific blocking work | Thread                |
| Need true process isolation        | Process               |

---

# 31. Sab concepts ko connect karo

Ab tak ki series:

```text
asyncio
  │
  ├── Queue
  ├── Lock
  ├── Event
  ├── Condition
  ├── Semaphore
  │
  ├── TaskGroup
  │
  ├── timeout()
  ├── wait_for()
  ├── shield()
  │
  ├── async with
  ├── async for
  │
  └── Threads / Processes
          │
          ├── to_thread()
          └── run_in_executor()
```

Ye ab ek complete async toolbox ban raha hai.

---

# 32. Sabse important mental model

### `asyncio`

> **Wait ko efficiently manage karo.**

### Thread

> **Blocking I/O ko event loop se bahar chalao.**

### Process

> **CPU-heavy work ko separate process mein chalao.**

### Semaphore

> **Concurrency limit karo.**

### TaskGroup

> **Tasks ka lifecycle manage karo.**

### Queue

> **Data flow/buffering manage karo.**

---

# 33. One-line memory trick

```text
Asyncio = WAIT
Thread  = BLOCKING I/O
Process = CPU
```

Aur HVAC example:

```text
BMS async API
     ↓
 asyncio

Legacy BMS SDK
     ↓
 to_thread()

Heavy analytics
     ↓
 ProcessPool
```

**Next Lesson 100 — `anyio`: Unified Async API**

Ismein hum dekhenge ke `asyncio` ke concepts ko **AnyIO** kis tarah ek common abstraction ke through asyncio/Trio dono ke saath use karne deta hai, aur `TaskGroup`, cancellation, locks, streams aur structured concurrency ko framework-independent style mein kaise likhte hain.
# Lesson 100 — `anyio` — Unified Async API

Ab hum `asyncio` se ek level upar ja rahe hain.

Aap ne ab tak mostly:

```text
asyncio
 ├── Task
 ├── TaskGroup
 ├── Queue
 ├── Lock
 ├── Semaphore
 ├── timeout
 ├── async with
 ├── async for
 └── Thread / Process integration
```

parha.

Ab question:

> Agar application ko sirf `asyncio` par tightly depend nahi karna ho to?

Yahan **AnyIO** ka concept aata hai.

---

# 1. AnyIO kya hai?

`AnyIO` ek **asynchronous compatibility / abstraction library** hai jo common async programming APIs provide karti hai.

Mental model:

```text
                    Your Application
                          │
                        AnyIO
                          │
              ┌───────────┴───────────┐
              ↓                       ↓
           asyncio                  Trio
```

Yani application code ko higher-level async primitives mil sakte hain, jabke backend asyncio ya Trio ho sakta hai.

---

# 2. Simple example

Normal asyncio:

```python
import asyncio

async def main():
    await asyncio.sleep(1)
    print("Done")

asyncio.run(main())
```

AnyIO style:

```python
import anyio

async def main():
    await anyio.sleep(1)
    print("Done")

anyio.run(main)
```

Concept:

```text
asyncio.sleep()
       ↓
backend-specific

anyio.sleep()
       ↓
common abstraction
```

---

# 3. AnyIO ka main faida

Agar aap directly:

```python
asyncio.create_task()
asyncio.sleep()
asyncio.Lock()
```

use karte ho to code asyncio-specific ho jata hai.

AnyIO mein:

```python
anyio.sleep()
anyio.create_task_group()
anyio.Lock()
```

jaise abstractions use kiye ja sakte hain.

Iska goal:

> Application ko async backend ke implementation details se zyada independent rakhna.

---

# 4. AnyIO ka sabse important concept: Task Group

AnyIO mein structured concurrency ka important primitive:

```python
async with anyio.create_task_group() as tg:
    ...
```

Example:

```python
import anyio


async def worker(name):
    await anyio.sleep(1)
    print(name)


async def main():

    async with anyio.create_task_group() as tg:

        tg.start_soon(worker, "A")
        tg.start_soon(worker, "B")
        tg.start_soon(worker, "C")


anyio.run(main)
```

Output:

```text
A
B
C
```

Order guaranteed nahi hai.

---

# 5. `asyncio.TaskGroup` se comparison

Aapne Lesson 96 mein dekha:

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(worker("A"))
```

AnyIO:

```python
async with anyio.create_task_group() as tg:
    tg.start_soon(worker, "A")
```

Difference:

```text
asyncio:
create_task(coroutine)

AnyIO:
start_soon(function, *args)
```

---

# 6. `start_soon()` ka important point

AnyIO:

```python
tg.start_soon(worker, "AHU-01")
```

Ye function aur arguments leta hai.

Aap generally coroutine object manually create nahi karte.

Concept:

```text
start_soon()
    ↓
Task Group
    ↓
start task
```

---

# 7. Structured concurrency

AnyIO ka task group bhi structured concurrency follow karta hai.

```text
Parent scope
     │
     ├── Task A
     ├── Task B
     └── Task C
```

Parent scope ke bahar ye child tasks uncontrolled nahi rehte.

Ye same philosophy hai jo hum `asyncio.TaskGroup` mein dekh chuke hain.

---

# 8. Failure behavior

Suppose:

```python
async def worker_a():
    raise ValueError("AHU failed")


async def worker_b():
    await anyio.sleep(10)
```

Task group:

```python
async with anyio.create_task_group() as tg:
    tg.start_soon(worker_a)
    tg.start_soon(worker_b)
```

Agar ek task fail hota hai, task-group structured cancellation ke through sibling tasks ko stop/cancel kar sakta hai aur error propagate hota hai.

Mental model:

```text
Task A
  ↓
ERROR
  ↓
Task Group
  ↓
cancel siblings
  ↓
cleanup
  ↓
propagate error
```

---

# 9. `anyio.run()`

Asyncio mein:

```python
asyncio.run(main())
```

AnyIO:

```python
anyio.run(main)
```

Ye application ka async entry point hai.

Example:

```python
import anyio


async def main():
    print("Hello")


if __name__ == "__main__":
    anyio.run(main)
```

---

# 10. Sleep

Asyncio:

```python
await asyncio.sleep(2)
```

AnyIO:

```python
await anyio.sleep(2)
```

Concept same:

```text
await
 ↓
current task gives control
 ↓
event loop/backend other work run karta hai
```

---

# 11. Cancellation

AnyIO cancellation model ko bhi structured concurrency ke saath integrate karta hai.

Example:

```python
import anyio


async def worker():

    try:
        while True:
            print("Working...")
            await anyio.sleep(1)

    finally:
        print("Cleanup")


async def main():

    async with anyio.create_task_group() as tg:
        tg.start_soon(worker)
        await anyio.sleep(3)

        tg.cancel_scope.cancel()


anyio.run(main)
```

Concept:

```text
TaskGroup
    ↓
cancel_scope.cancel()
    ↓
child task cancellation
    ↓
finally
    ↓
cleanup
```

---

# 12. `CancelScope`

AnyIO ka important concept:

```python
tg.cancel_scope
```

Cancellation ko scope ke through manage kiya ja sakta hai.

Mental model:

```text
Cancel Scope
     │
     ├── Task A
     ├── Task B
     └── Task C
```

Cancel scope:

```text
cancel()
 ↓
scope ke tasks affected
```

Ye structured cancellation ko samajhne ke liye important hai.

---

# 13. Timeout

AnyIO mein timeout ke liye cancel scopes ka concept use hota hai.

Example:

```python
with anyio.fail_after(5):

    await slow_operation()
```

Meaning:

> Agar operation 5 seconds ke andar complete nahi hua to timeout.

Another concept:

```python
with anyio.move_on_after(5):
    await slow_operation()
```

Difference:

### `fail_after`

Timeout par exception raise karta hai.

### `move_on_after`

Timeout par scope se bahar move kar deta hai without propagating timeout in the same way.

Mental model:

```text
fail_after
   ↓
timeout
   ↓
error

move_on_after
   ↓
timeout
   ↓
continue after scope
```

---

# 14. Asyncio vs AnyIO timeout concept

Aapne asyncio mein:

```python
asyncio.timeout(5)
```

dekha.

AnyIO mein:

```python
anyio.fail_after(5)
```

ya:

```python
anyio.move_on_after(5)
```

use kiya ja sakta hai.

Important:

> Exact exception/control-flow semantics ko library documentation/version ke mutabiq samajhna chahiye; sirf names dekh kar one-to-one equivalence assume nahi karni chahiye.

---

# 15. AnyIO Lock

AnyIO:

```python
lock = anyio.Lock()
```

Use:

```python
async with lock:
    shared_data += 1
```

Same mental model:

```text
Lock
 ↓
one task at a time
```

---

# 16. AnyIO Semaphore

```python
semaphore = anyio.Semaphore(10)
```

Use:

```python
async with semaphore:
    await read_bms()
```

Meaning:

```text
100 tasks
   ↓
Semaphore(10)
   ↓
maximum 10 active
```

Exactly wahi concept jo asyncio Semaphore mein dekha.

---

# 17. HVAC example

Suppose:

```text
1000 VAVs
```

Aap nahi chahte ke BMS server par 1000 simultaneous requests chali jayein.

AnyIO:

```python
import anyio


semaphore = anyio.Semaphore(10)


async def read_vav(vav_id):

    async with semaphore:

        return await read_bms(vav_id)
```

Then:

```python
async with anyio.create_task_group() as tg:

    for vav_id in vav_ids:
        tg.start_soon(read_vav, vav_id)
```

Architecture:

```text
                Task Group
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
    VAV Task      VAV Task      VAV Task
       │            │            │
       └────────────┼────────────┘
                    ↓
              Semaphore(10)
                    ↓
                   BMS
```

---

# 18. AnyIO Streams

AnyIO ka ek bohat important area **streams** hain.

Streams ka purpose:

> Async data ko efficiently send/receive karna.

Concept:

```text
Producer
   ↓
Stream
   ↓
Consumer
```

Ye Queue se related lagta hai, lekin streams higher-level communication abstraction provide kar sakti hain.

---

# 19. Memory stream

AnyIO mein memory object streams use ki ja sakti hain.

Conceptually:

```python
send, receive = anyio.create_memory_object_stream()
```

Producer:

```python
await send.send("AHU-01")
```

Consumer:

```python
value = await receive.receive()
```

Architecture:

```text
Producer
   │
   ↓
Send Stream
   │
   ↓
Memory Buffer
   │
   ↓
Receive Stream
   │
   ↓
Consumer
```

---

# 20. Queue vs Stream

Asyncio:

```python
asyncio.Queue()
```

AnyIO:

```text
Memory Object Stream
```

Conceptual difference:

```text
Queue
 ↓
data queue

Stream
 ↓
communication channel abstraction
```

Streams sender aur receiver ko explicitly separate kar sakte hain.

---

# 21. Producer-consumer example

```python
import anyio


async def producer(send):

    for i in range(5):

        await send.send(i)

        await anyio.sleep(1)

    await send.aclose()


async def consumer(receive):

    async for value in receive:

        print("Received:", value)


async def main():

    send, receive = anyio.create_memory_object_stream(10)

    async with anyio.create_task_group() as tg:

        tg.start_soon(producer, send)
        tg.start_soon(consumer, receive)


anyio.run(main)
```

Yahan interesting cheez:

```python
async for value in receive:
```

Stream khud asynchronous iterable provide kar sakta hai.

---

# 22. Ab previous lessons connect ho rahe hain

Aapne:

```text
async for
```

Lesson 98 mein padha.

Ab:

```text
AnyIO stream
     ↓
async for
```

Naturally combine ho raha hai.

---

# 23. AnyIO + async context manager

Streams ko context manager ke through manage kiya ja sakta hai.

Concept:

```python
async with send:
    await send.send(data)
```

Yani:

```text
async with
     ↓
resource lifecycle

async for
     ↓
data flow
```

Exactly Lesson 98 ka connection.

---

# 24. AnyIO + Threads

AnyIO blocking function ko thread mein run karne ke liye API provide karta hai.

Conceptually:

```python
result = await anyio.to_thread.run_sync(blocking_function)
```

Architecture:

```text
AnyIO
  ↓
to_thread.run_sync()
  ↓
Thread
  ↓
Blocking function
```

Ye Lesson 99 ke:

```python
asyncio.to_thread()
```

ka corresponding abstraction samajh sakte ho.

---

# 25. AnyIO + Process

AnyIO ka focus primarily async concurrency abstraction par hai.

CPU-heavy work ke liye aap architecture mein process-based tools/libraries use kar sakte ho.

Mental model:

```text
AnyIO
  │
  ├── async tasks
  ├── async streams
  ├── cancellation
  ├── locks
  ├── semaphores
  │
  └── blocking bridge → thread
```

CPU-heavy process work ko application architecture mein separately handle karna common hai.

---

# 26. AnyIO ka biggest benefit

Suppose aap library bana rahe ho.

Agar directly:

```python
import asyncio
```

har jagah use kar diya:

```python
asyncio.Lock
asyncio.TaskGroup
asyncio.sleep
asyncio.Queue
```

to library asyncio-specific ho sakti hai.

AnyIO abstraction use karne se:

```text
Library
   ↓
AnyIO
   ↓
async backend
```

architecture zyada flexible ho sakta hai.

---

# 27. Lekin AnyIO ki zarurat har project mein nahi

Ye bhi important hai.

Agar aapka application:

```text
sirf asyncio
+
FastAPI
+
asyncio-compatible libraries
```

use karta hai, to direct asyncio perfectly reasonable hai.

AnyIO ka benefit tab zyada attractive hota hai jab:

* reusable async libraries likhni hon
* backend abstraction useful ho
* structured concurrency chahiye
* streams/cancellation abstractions chahiye
* ecosystem already AnyIO use karta ho

---

# 28. AnyIO vs asyncio

| Feature                 | asyncio            | AnyIO                     |
| ----------------------- | ------------------ | ------------------------- |
| Python standard library | ✅                  | ❌                         |
| Async runtime           | ✅                  | abstraction               |
| TaskGroup               | ✅                  | ✅                         |
| Lock                    | ✅                  | ✅                         |
| Semaphore               | ✅                  | ✅                         |
| Cancellation            | asyncio model      | structured cancellation   |
| Streams                 | limited primitives | strong stream abstraction |
| Trio compatibility      | ❌                  | ✅                         |
| Thread bridge           | `to_thread()`      | `to_thread.run_sync()`    |
| Backend abstraction     | ❌                  | ✅                         |

---

# 29. `asyncio` ko replace karta hai?

Simple answer:

**Nahi, exactly replace nahi karta.**

Better mental model:

```text
asyncio
   ↓
actual Python async runtime/backend

AnyIO
   ↓
higher-level async abstraction
```

AnyIO asyncio ke upar bhi run kar sakta hai.

---

# 30. Trio kya hai?

AnyIO ko samajhne ke liye Trio ka basic idea pata hona useful hai.

Trio ek async framework/runtime hai jiska design structured concurrency ko strongly emphasize karta hai.

Architecture:

```text
                    AnyIO
                  /       \
                 /         \
           asyncio          Trio
```

Aapka application higher-level AnyIO APIs use kar sakta hai.

---

# 31. Why this architecture useful hai?

Imagine:

```text
Your BMS application
        ↓
AnyIO
        ↓
async backend
```

Application ka business logic:

```python
async def read_ahu():
    ...
```

backend-specific details se relatively separate ho sakta hai.

---

# 32. Lekin ek limitation

Agar aapko specifically asyncio ka feature chahiye:

```python
asyncio.get_running_loop()
```

ya koi asyncio-specific API:

```python
asyncio.Future
asyncio.Protocol
```

use karoge to abstraction break ho sakti hai.

Isliye:

> Abstraction use kar rahe ho to abstraction ke level par rehna better hota hai.

---

# 33. OOP/protocol connection

Aapne Python protocols par detailed study ki hai.

AnyIO ko bhi isi angle se samjho:

```text
Implementation
      ↓
Abstract async behavior
      ↓
Application
```

For example:

```text
Lock
Stream
Task Group
Cancel Scope
```

Application ko implementation ke low-level details se isolate kiya ja sakta hai.

---

# 34. Complete async ecosystem map

Ab tak ki lessons ko ek diagram mein dekho:

```text
                         ASYNC PYTHON
                              │
                 ┌────────────┴────────────┐
                 │                         │
              asyncio                    AnyIO
                 │                         │
       ┌─────────┼──────────┐       ┌──────┴──────┐
       │         │          │       │             │
     Tasks     Queue      Locks   TaskGroup     Streams
       │         │          │       │             │
       ├── timeout            │      │          Producer
       ├── shield             │      │             ↓
       └── TaskGroup          │      │          Consumer
                              │      │
                              └──────┴──────
```

---

# 35. HVAC/BMS complete architecture

Aapke domain mein isko aise imagine karo:

```text
                 BMS Monitoring System
                         │
                        AnyIO
                         │
                 Task Group
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
      AHU              VAV              Chiller
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                  Semaphore(10)
                         ↓
                     BMS API
                         ↓
                     Readings
                         ↓
                  Memory Stream
                         ↓
                    Processing
                         ↓
                 Database / Alarm
```

Agar BMS SDK blocking ho:

```text
BMS SDK
   ↓
to_thread.run_sync()
   ↓
Thread
```

Agar heavy analytics ho:

```text
Readings
   ↓
ProcessPool / CPU worker
```

---

# 36. Sab se important memory trick

```text
asyncio
= Python ka standard async toolkit

AnyIO
= common/high-level async abstraction

TaskGroup
= tasks ka structured lifecycle

Semaphore
= concurrency limit

Stream
= async data flow

Cancel Scope
= cancellation boundary

to_thread
= blocking sync function ko async application se safely bridge karna
```

---

# 37. Aapki complete journey

Aap ne ab roughly ye progression cover kar li:

```text
Threading
    ↓
Multiprocessing
    ↓
concurrent.futures
    ↓
GIL
    ↓
asyncio
    ↓
asyncio synchronization
    ↓
TaskGroup
    ↓
Timeout / Cancellation
    ↓
Async Context Manager
    ↓
Async Iterator
    ↓
asyncio + Threads/Processes
    ↓
AnyIO
```

Ye Python concurrency ka kaafi strong foundation hai.

### Next Lesson 101

Ab hum **Advanced Python Concurrency Architecture** ki taraf ja sakte hain: **Asyncio + Queue + TaskGroup + Semaphore + cancellation ko combine karke ek complete Producer–Consumer system** banayenge — specifically BMS/HVAC example ke saath, jahan hundreds of VAV/AHU readings concurrently process hongi.
