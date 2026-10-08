# Python Concurrency — Lessons 91-100 (Roman Urdu Detailed Guide)

Har lesson ka code + line-by-line explanation.

---

# Lesson 91: `multiprocessing` — Manager, Shared Memory, Value, Array

## 1. Problem: Process Memory Separate

```python
counter = 0
# Main process: counter = 0
# Child process: counter = 0 (separate)
```

**Explanation:**
- Processes ki memory separate hoti hai

## 2. Solutions

```
Simple communication → Queue / Pipe
Shared higher-level objects → Manager
Simple shared primitive → Value / Array
High-performance → shared_memory
```

## 3. `Manager`

```python
from multiprocessing import Manager

def worker(shared_list):
    shared_list.append("AHU-01")

with Manager() as manager:
    shared_list = manager.list()
    p = Process(target=worker, args=(shared_list,))
    p.start()
    p.join()
    print(shared_list)   # ['AHU-01']
```

**Explanation:**
- Manager server process provide karta hai
- Shared Python objects

## 4. Manager Mental Model

```
Process A ──┐
Process B ──┼──► Manager → Shared Object
Process C ──┘
```

## 5. Normal List vs Manager

```
Normal list → Process-local
manager.list() → Shared through Manager
```

## 6. Manager Dictionary

```python
data = manager.dict()
data["AHU-01"] = 22.5
data["AHU-02"] = 23.1
```

## 7. Manager Common Objects

```python
manager.list()
manager.dict()
manager.Namespace()
manager.Lock()
manager.Event()
manager.Queue()
```

## 8. Manager Disadvantage

```
Manager → IPC/proxy → overhead
```

## 9. `Value`

```python
counter = Value("i", 0)   # "i" = integer, 0 = initial
print(counter.value)      # 0
counter.value += 1        # 1
```

## 10. Complete Value Example

```python
def worker(counter):
    counter.value += 1

counter = multiprocessing.Value("i", 0)
p = Process(target=worker, args=(counter,))
p.start()
p.join()
print(counter.value)   # 1
```

## 11. Value Mental Model

```
Process A ──┐
            │ counter.value
            ▼
      Shared Memory
            ▲
Process B ──┘
```

## 12. `Value` with Lock

```python
counter = Value("i", 0, lock=True)
```

**Explanation:**
- `counter.value += 1` → compound operation
- Synchronization design zaroori

## 13. Explicit Lock

```python
def worker(counter, lock):
    for _ in range(1000):
        with lock:
            counter.value += 1

counter = Value("i", 0)
lock = Lock()

processes = []
for _ in range(4):
    p = Process(target=worker, args=(counter, lock))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

print(counter.value)   # 4000
```

## 14. `Array`

```python
numbers = Array("i", [1, 2, 3, 4])
print(numbers[0])      # 1
numbers[0] = 100
```

## 15. Complete Array Example

```python
def worker(numbers):
    numbers[0] = 100

numbers = Array("i", [1, 2, 3])
p = Process(target=worker, args=(numbers,))
p.start()
p.join()
print(list(numbers))   # [100, 2, 3]
```

## 16. Value vs Array

```
Value → one shared value
Array → multiple shared values
```

## 17. Type Codes

```
'i' → integer
'd' → double/float
'f' → float
'b' → signed char
```

```python
temperature = Value("d", 22.5)   # float
```

## 18. HVAC Shared Temperature

```python
temperature = Value("d", 22.0)
# Sensor process:
temperature.value = 23.5
# Monitoring process:
print(temperature.value)
```

## 19. Manager vs Value vs Array

| Mechanism | Data |
|-----------|------|
| `Manager().list()` | Python list |
| `Manager().dict()` | Python dictionary |
| `Value` | Single primitive |
| `Array` | Array of primitives |

## 20. `shared_memory`

```python
from multiprocessing import shared_memory

shm = shared_memory.SharedMemory(create=True, size=1024)
print(shm.name)
```

**Explanation:**
- 1024 bytes ka shared memory block

## 21. Memory Access

```python
shm.buf[0] = 100
print(shm.buf[0])
```

## 22. Shared Memory Cleanup

```python
shm.close()    # Current process handle close
shm.unlink()   # Shared memory remove
```

## 23. Shared Memory Between Processes

```python
existing = shared_memory.SharedMemory(name=shm.name)
```

## 24. Synchronization Warning

```
shared_memory ≠ synchronization
Lock/Semaphore/Event → design required
```

## 25. Shared Memory + NumPy

```
Shared Memory → NumPy ndarray → Process A / Process B
```

## 26. Manager vs Shared Memory

```
Manager → Python objects
Shared Memory → raw memory, buffer, numeric data
```

## 27. Architecture

```
Shared Memory
100 MB dataset
├── P1
├── P2
└── P3
```

## 28. Master Comparison

| Mechanism | Best for | Abstraction |
|-----------|----------|-------------|
| `Manager` | Python list/dict | High |
| `Value` | Single primitive | Medium |
| `Array` | Primitive array | Medium |
| `shared_memory` | High-performance | Low |

## 29. Complete Map

```
multiprocessing
├── Message Passing
│   └── Queue
├── Shared Data
│   ├── Manager
│   ├── Value
│   ├── Array
│   └── shared_memory
└── Direct Communication
    └── Pipe
```

## 30. Kab Kya

```
Task bhejna → Queue
Direct message → Pipe
Shared dict/list → Manager
Simple counter → Value
Numeric array → Array
High-performance → shared_memory
```

## 31. Threading vs Multiprocessing

```
Threading → Shared memory + Synchronization
Multiprocessing → Isolated memory + IPC/shared-memory
```

## 32. Final Model

```
Process
├── Need tasks? → Queue
├── Direct communication? → Pipe
├── Python objects? → Manager
├── One primitive? → Value
├── Primitive array? → Array
└── High-performance? → shared_memory
```

## 33. One-Line

```
Manager → convenience
Value/Array → simple shared primitives
shared_memory → low-level/high-performance
```

---

# Lesson 92: `concurrent.futures` — ThreadPoolExecutor + ProcessPoolExecutor

## 1. Basic Idea

```
Aap tasks do → Executor → Worker Threads/Processes → Future → Result
```

## 2. Two Executors

```python
ThreadPoolExecutor   # I/O-bound
ProcessPoolExecutor  # CPU-bound
```

## 3. Executor Kya Hai

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    ...
```

**Explanation:**
- Worker management system
- Manual Thread/Process management nahi

## 4. Simple Example

```python
def worker(x):
    return x * 2

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(worker, [1, 2, 3, 4])
    print(list(results))   # [2, 4, 6, 8]
```

## 5. `map()` Concept

```
1 → worker → 10
2 → worker → 20
3 → worker → 30
```

## 6. `submit()` — Individual Task

```python
future = executor.submit(worker, 10)
print(future)   # Future object
```

## 7. Future Kya Hai

```
submit() → Task worker ko diya → Future object mila
       → worker kaam karega → result ready → future.result()
```

## 8. `future.result()`

```python
future = executor.submit(worker, 10)
result = future.result()
print(result)   # 20
```

**Explanation:**
- `Future` → eventual result ka container
- `result()` → actual result

## 9. Future Methods

```python
future.result()
future.done()
future.running()
future.cancel()
future.exception()
```

## 10. `done()`

```python
if future.done():
    print("Task complete")
```

## 11. `running()`

```python
if future.running():
    print("Task running")
```

## 12. `cancel()`

```python
future.cancel()
```

**Explanation:**
- `PENDING` → cancel possible
- `RUNNING` → cancel fail

## 13. Future Lifecycle

```
PENDING → RUNNING → FINISHED
       └→ CANCELLED
```

## 14. `submit()` vs `map()`

| `submit()` | `map()` |
|------------|---------|
| Individual task | Multiple tasks |
| Future return | Results iterator |
| Flexible | Simple |
| Callback | Less flexible |
| `as_completed()` useful | Ordered results |

## 15. `as_completed()`

```python
from concurrent.futures import as_completed

futures = [executor.submit(worker, x) for x in [10, 20, 30]]

for future in as_completed(futures):
    print(future.result())
```

**Explanation:**
- Completion order

## 16. `map()` vs `as_completed()`

```
map() → input order
as_completed() → completion order
```

## 17. Exception Handling

```python
def worker(x):
    if x == 0:
        raise ValueError("Zero allowed nahi")
    return 100 / x

future = executor.submit(worker, 0)
try:
    result = future.result()
except Exception as e:
    print("Error:", e)
```

**Explanation:**
- Error Future mein store
- `result()` par raise

## 18. Callback

```python
def callback(future):
    print("Result:", future.result())

future = executor.submit(worker, 10)
future.add_done_callback(callback)
```

## 19. ThreadPoolExecutor

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    ...
```

**Explanation:**
- 5 worker threads
- I/O-bound

## 20. I/O-Bound Example

```
Thread 1 → API
Thread 2 → Database
Thread 3 → File
Thread 4 → Network
```

## 21. HVAC Example

```python
# 20 AHU data read
# Har request network/BMS/API se
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(read_ahu, ahu) for ahu in ahu_list]
```

## 22. ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_task(x):
    return x * x

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = executor.map(cpu_task, [1, 2, 3, 4, 5])
        print(list(results))   # [1, 4, 9, 16, 25]
```

## 23. ProcessPool Kyun

```
Main Process
├── Process 1
├── Process 2
├── Process 3
└── Process 4
```

- Har process ki memory independent
- CPU-bound pure-Python tasks

## 24. ThreadPool vs ProcessPool

| Feature | ThreadPool | ProcessPool |
|---------|-----------|-------------|
| Worker | Thread | Process |
| Memory | Shared | Separate |
| Best | I/O-bound | CPU-bound |
| GIL | Relevant | Processes parallel |
| Startup | Low | Higher |
| Communication | Shared memory | IPC/serialization |

## 25. Windows Rule

```python
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        ...
```

**Explanation:**
- Windows multiprocessing ke liye important

## 26. ProcessPool Function

```python
def worker(x):
    return x * x
```

**Explanation:**
- Module level par define karo
- Pickleable hona chahiye

## 27. `shutdown()`

```python
executor.shutdown(wait=True, cancel_futures=False)
```

- `wait=True` → Existing tasks complete
- `cancel_futures=True` → Pending cancel

## 28. `with` Kyun Better

```python
with ThreadPoolExecutor() as executor:
    # work
# Auto cleanup
```

## 29. Complete Architecture

```
concurrent.futures
├── ThreadPoolExecutor → Threads → I/O-bound
└── ProcessPoolExecutor → Processes → CPU-bound
     ↓
   Future
     ├── result()
     ├── callback()
     └── as_completed()
```

## 30. Mental Model

```
Executor → Kaun kaam karega?
submit() → Ye task karo
Future → Result baad mein milega
result() → Result do
map() → Function multiple inputs par chalao
as_completed() → Jo pehle complete ho, uska result pehle
```

## 31. Threading vs ThreadPoolExecutor

```python
# Manual
thread = Thread(target=worker)
thread.start()
thread.join()

# High-level
with ThreadPoolExecutor() as executor:
    future = executor.submit(worker)
    result = future.result()
```

## 32. Short Memory

```
Executor → Worker pool
submit() → Single task
map() → Many similar tasks
Future → Future result handle
result() → Actual result
as_completed() → Completion order
ThreadPool → I/O-bound
ProcessPool → CPU-bound
```

---

# Lesson 93: GIL — Global Interpreter Lock

## 1. GIL Kya Hai

```
1 CPython Process
├── Thread 1
├── Thread 2
├── Thread 3
└── Thread 4
     ↓
Python bytecode
     ↓
GIL
     ↓
At a given moment, normally one thread executes Python bytecode
```

**Explanation:**
- Threads simultaneously exist
- Ek waqt mein ek thread Python bytecode execute

## 2. CPU Mein 4 Cores

```
CPU
├── Core 1
├── Core 2
├── Core 3
└── Core 4

Thread 1 → Core 1 → Python bytecode
Thread 2 → waiting
Thread 3 → waiting
Thread 4 → waiting
```

## 3. CPU-Bound Example

```python
def calculate():
    total = 0
    for i in range(100_000_000):
        total += i
    return total

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(calculate) for _ in range(4)]
    results = [f.result() for f in futures]
```

**Explanation:**
- 4 threads 4 cores par simultaneously nahi

## 4. Threads Useless Nahi

```
Thread 1 → API request → WAIT
Thread 2 → Database → WAIT
Thread 3 → File → WAIT
Thread 4 → Network → WAIT
```

**Explanation:**
- I/O-bound useful

## 5. I/O-Bound Example

```python
def get_data():
    response = requests.get(...)
    return response.json()
```

**Explanation:**
- Network wait mein doosre threads useful work

## 6. GIL vs CPU Core

```
CPU core → Hardware resource
Thread → Execution path
GIL → CPython interpreter mechanism
```

## 7. GIL Lock Jaisa

```python
lock = threading.Lock()
with lock:
    # critical section
```

**Explanation:**
- GIL interpreter internal
- `gil.acquire()` normally nahi karte

## 8. GIL Ka Main Reason

```
Python objects
Reference counting
Interpreter internals
C extensions
→ Synchronize easier
```

## 9. Reference Counting

```python
a = object()   # reference count
# Thread 1 → refcount +1
# Thread 2 → refcount +1
# Synchronization zaroori
```

## 10. GIL ≠ Thread Safety

```python
counter += 1   # Race condition possible
# Lock zaroori
```

**Explanation:**
- GIL application-level thread safety nahi

## 11. GIL vs Race Condition

```
GIL → Interpreter-level
Race condition → Application logic concurrency bug
```

## 12. GIL Thread Switching

```
Thread A → Python execution → switch → Thread B → switch → Thread C
```

**Explanation:**
- Concurrent appear
- CPU-bound multi-core nahi

## 13. Concurrency vs Parallelism

```
Concurrency → Multiple tasks progress
Parallelism → Multiple tasks same time different cores
```

## 14. Process GIL Bypass

```
Process 1 → Python interpreter → GIL 1
Process 2 → Python interpreter → GIL 2
```

**Explanation:**
- Separate processes

## 15. ThreadPool vs ProcessPool

```
CPU-bound pure Python → ProcessPoolExecutor → Multi-core
I/O-bound → ThreadPoolExecutor → Throughput
```

## 16. HVAC Example

```
BMS/API/network/database → ThreadPoolExecutor
```

## 17. Heavy Analytics

```
5 million readings → ProcessPoolExecutor
```

## 18. ProcessPool Overhead

```
Process creation
Serialization
IPC
Data transfer
Memory
```

## 19. Pickling

```
Main process → serialize → child process → deserialize
```

## 20. Native C Extensions

```
Python thread → C extension → release GIL → native computation
```

## 21. GIL Scope

```
CPython Process → Thread 1, 2, 3, 4 → GIL → Python bytecode
```

## 22. GIL vs multiprocessing.Lock

```
GIL → Interpreter-level
multiprocessing.Lock → Application-level inter-process
```

## 23. GIL vs threading.Lock

```
GIL → CPython mechanism
threading.Lock → Application synchronization
```

## 24. Comparison

```
GIL → CPython interpreter level
Thread → Same process
Process → Separate process
```

## 25. Analogy

```
Office = Python process
Employees = Threads
One special key = GIL
Ek waqt mein ek employee room mein
```

## 26. Process Analogy

```
Office 1 → own key
Office 2 → own key
Office 3 → own key
Office 4 → own key
```

## 27. Modern Note

```
CPython recent versions → GIL architecture evolve
Free-threaded builds → newer Python releases
```

## 28. Decision Tree

```
I/O-bound → ThreadPoolExecutor
CPU-bound pure Python → ProcessPoolExecutor
Native code → Depends on library/GIL
```

## 29. 8 Important Points

```
1. GIL CPython interpreter mechanism
2. Python bytecode execution restrict
3. Threading useless nahi
4. I/O-bound threads useful
5. CPU-bound threads multi-core nahi
6. Processes separate GIL contexts
7. CPU-bound → ProcessPool
8. GIL ≠ thread safety replacement
```

## 30. One-Line

```
I/O → Threads
CPU + Pure Python → Processes
Shared state → Synchronization
GIL → CPython bytecode restriction
```

---

# Lesson 94: GIL Bypass Techniques

## 1. GIL Bypass Meaning

```
GIL problem
├── 1. Multiple Processes → multiprocessing
└── 2. Native Code → C/C++/Rust extensions
```

## 2. Approach 1 — GIL Avoid

```
Process 1 → GIL 1
Process 2 → GIL 2
Process 3 → GIL 3
```

## 3. Approach 2 — GIL Release

```
Python Thread → Native C/C++ code → GIL released → CPU computation
```

## 4. Technique 1 — Multiprocessing

```python
from multiprocessing import Process
# Ya
from concurrent.futures import ProcessPoolExecutor
```

## 5. Multiple Processes Architecture

```
CPU
├── Core 1 ← Process 1
├── Core 2 ← Process 2
├── Core 3 ← Process 3
└── Core 4 ← Process 4
```

## 6. CPU-Bound Example

```python
def calculate(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

if __name__ == "__main__":
    values = [10_000_000] * 4
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(calculate, values))
```

## 7. GIL Bypass

```
Process 1 → Interpreter 1 → GIL 1
Process 2 → Interpreter 2 → GIL 2
Process 3 → Interpreter 3 → GIL 3
Process 4 → Interpreter 4 → GIL 4
```

## 8. Processes Cost

```
Process → Memory, Startup, Serialization, IPC
```

## 9. Serialization

```
Main Process → Serialize → IPC → Worker Process → Deserialize
```

## 10. Chunking

```
1,000,000 records
Chunk 1 → 250,000
Chunk 2 → 250,000
Chunk 3 → 250,000
Chunk 4 → 250,000
```

## 11. Technique 2 — C Extensions

```
Python → C extension → native machine code
```

## 12. GIL Release Model

```
Python thread → GIL → C extension → release GIL → native work → reacquire GIL
```

## 13. Har C Extension GIL Release Nahi

```
C extension hai → GIL automatically release? NO
Extension explicitly release kare
```

## 14. Conceptual C Example

```c
Py_BEGIN_ALLOW_THREADS
/* long-running native work */
Py_END_ALLOW_THREADS
```

## 15. Safety Condition

```
GIL released → native computation
GIL reacquired → Python objects access
```

## 16. NumPy Example

```python
import numpy as np

a = np.random.rand(10_000_000)
b = np.random.rand(10_000_000)
c = a + b
```

**Explanation:**
- Native implementation

## 17. Pure Python vs NumPy

```python
# Pure Python
total = 0
for x in data:
    total += x

# NumPy
total = np.sum(data)
```

## 18. Python Loop vs Vectorization

```python
# Pure Python
result = []
for x in data:
    result.append(x * 2)

# NumPy
result = np.array(data) * 2
```

## 19. Cython

```
Python-like code → Cython → C/C++ extension → native execution
```

## 20. Rust Extensions

```
Python → Rust extension → native code
PyO3, maturin
```

## 21. C++ Extensions

```
Python → C++ extension → native code
```

## 22. Free-Threaded CPython

```
Traditional → GIL
Free-threaded → GIL disabled
```

## 23. Traditional vs Free-Threaded

```
Traditional: Thread 1-4 → GIL
Free-threaded: Thread 1-4 → Core 1-4
```

## 24. Comparison Table

| Technique | Idea | CPU Parallelism |
|-----------|------|-----------------|
| Threading + pure Python | Same process | Limited by GIL |
| Multiprocessing | Multiple processes | Yes |
| ProcessPoolExecutor | Process pool | Yes |
| Native C/C++ | GIL release | Possible |
| Cython | Compiled | Possible |
| Rust | Native | Possible |
| Free-threaded | GIL disabled | True threading |

## 25. ProcessPool vs Native Extension

```
ProcessPool → Pure Python parallel, memory overhead, IPC
Native → High performance, same process, complexity
```

## 26. HVAC Example

```
BMS data retrieve → ThreadPoolExecutor
Heavy calculation → ProcessPoolExecutor
Numerical array → NumPy
```

## 27. Python Slow

```
Python orchestration → NumPy native → CPU
Python ≠ necessarily slow
```

## 28. Decision Tree

```
CPU-heavy?
├── Pure Python → ProcessPool
└── Numeric/native → NumPy/native
Maximum performance → C/C++/Rust/Cython
```

## 29. 3 Statements

```
1. GIL bypass → processes
2. GIL release → native extension
3. GIL-free → free-threaded CPython
```

## 30. Complete Picture

```
threading → I/O concurrency → GIL
multiprocessing → multi-core parallelism
Native code → GIL release
```

## 31. One-Line

```
Pure Python CPU → processes
Native numerical → native libraries
I/O → threads/asyncio
```

---

# Lesson 95: `asyncio` Advanced — Queue, Lock, Event, Condition, Semaphore

## 1. Asyncio Mental Model

```
One event loop → Task, Task, Task
Tasks cooperative way
await something() → event loop ko control
```

## 2. Basic Example

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

## 3. `asyncio.Lock`

```python
lock = asyncio.Lock()
counter = 0

async def worker():
    global counter
    async with lock:
        counter += 1
```

## 4. `threading.Lock` vs `asyncio.Lock`

```
threading.Lock → Threads
asyncio.Lock → asyncio Tasks
```

## 5. `asyncio.Lock` with `with`

```python
# Wrong
with lock:
    ...

# Correct
async with lock:
    ...
```

## 6. Lock Use

```
Task A → 🔒 → resource
Task B → wait
Task C → wait
Task A → unlock
```

## 7. HVAC Example

```python
equipment_status = {}
lock = asyncio.Lock()

async def update_status(equipment_id, status):
    async with lock:
        equipment_status[equipment_id] = status
```

## 8. `asyncio.Event`

```python
event = asyncio.Event()
await event.wait()    # Wait
event.set()           # Signal
event.clear()         # Reset
```

## 9. Event Example

```python
event = asyncio.Event()

async def worker():
    print("Waiting...")
    await event.wait()
    print("Signal mil gaya!")

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(2)
    event.set()
    await task
```

## 10. Event Traffic Signal

```
RED → Tasks wait
GREEN → Tasks continue
```

## 11. Event vs Lock

```
Lock → "Kaun andar ja sakta hai?"
Event → "Signal aa gaya?"
```

## 12. `asyncio.Semaphore`

```python
semaphore = asyncio.Semaphore(3)

async with semaphore:
    ...
```

## 13. Semaphore Example

```python
semaphore = asyncio.Semaphore(2)

async def worker(name):
    async with semaphore:
        print(name, "started")
        await asyncio.sleep(2)
        print(name, "finished")

async def main():
    tasks = [asyncio.create_task(worker(f"Task-{i}")) for i in range(5)]
    await asyncio.gather(*tasks)
```

## 14. Semaphore Visual

```
Capacity = 2
[Task 1] [Task 2]
[   WAIT     ]
[   WAIT     ]
```

## 15. HVAC/API Example

```python
semaphore = asyncio.Semaphore(10)

async def read_vav(vav_id):
    async with semaphore:
        return await read_from_bms(vav_id)
```

```
1000 tasks → Semaphore(10) → 10 active requests
```

## 16. Lock vs Semaphore

```
Lock → capacity 1
Semaphore(5) → capacity 5
```

## 17. `asyncio.Queue`

```python
queue = asyncio.Queue()
await queue.put(item)    # Producer
item = await queue.get() # Consumer
```

## 18. Producer-Consumer

```
Producer → put() → Queue → get() → Consumer
```

## 19. Basic Queue Example

```python
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
    consumer_task = asyncio.create_task(consumer(queue))
    await producer(queue)
    await queue.join()
    consumer_task.cancel()
```

## 20. `queue.put()`

```python
await queue.put(item)
# Full → producer waits
```

## 21. `queue.get()`

```python
item = await queue.get()
# Empty → consumer waits
```

## 22. `task_done()`

```python
item = await queue.get()
try:
    await process(item)
finally:
    queue.task_done()
```

## 23. `queue.join()`

```
put() → unfinished +1
task_done() → unfinished -1
count = 0 → join() returns
```

## 24. Bounded Queue

```python
queue = asyncio.Queue(maxsize=10)
```

## 25. Backpressure

```
Fast Producer → Queue(maxsize=100) → Slow Consumer
Queue full → Producer WAIT
```

## 26. `asyncio.Condition`

```python
condition = asyncio.Condition()
```

## 27. Condition Example

```python
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

## 28. `while` Rule

```python
while not condition:
    await condition.wait()
```

**Explanation:**
- Wake-up ke baad condition verify

## 29. `notify()` vs `notify_all()`

```
notify() → one waiter
notify_all() → all waiters
```

## 30. Condition vs Event

```
Event → "Signal aa gaya."
Condition → "Shared state condition mein hai?"
```

## 31. Summary Table

| Primitive | Purpose |
|-----------|---------|
| `Lock` | One task at a time |
| `Semaphore` | Maximum N tasks |
| `Event` | Signal |
| `Condition` | Wait for state |
| `Queue` | Producer-consumer |

## 32. Threading vs Asyncio

| Threading | Asyncio |
|-----------|---------|
| `threading.Lock` | `asyncio.Lock` |
| `threading.Semaphore` | `asyncio.Semaphore` |
| `threading.Event` | `asyncio.Event` |
| `threading.Condition` | `asyncio.Condition` |
| `queue.Queue` | `asyncio.Queue` |
| Threads | Tasks |
| OS scheduling | Event-loop |

## 33. Key Difference

```python
await asyncio.sleep(1)   # Task waits, event loop continues
time.sleep(1)            # Thread BLOCK, event loop blocked
```

## 34. `asyncio.Queue` vs `queue.Queue`

```
queue.Queue → Threads
asyncio.Queue → Async tasks
```

## 35. Full Async HVAC Architecture

```
BMS/API → Producer 1, Producer 2 → asyncio.Queue → Consumer 1, Consumer 2
BMS Requests → Semaphore(10) → max 10 concurrent
Shared State → Lock
```

## 36. Complete Application

```
1000 VAVs
├── Producer → VAV IDs → Queue
├── Consumers → Read BMS
├── Semaphore(10) → max 10 requests
├── Lock → shared results
└── Event → shutdown signal
```

## 37. Communication vs Synchronization

```
Queue → Data/task communication
Lock → Mutual exclusion
Semaphore → Concurrency limiting
Event → Signaling
Condition → State-based waiting
```

## 38. Memory Trick

```
Lock → "ONE"
Semaphore → "N"
Event → "SIGNAL"
Condition → "STATE"
Queue → "DATA"
```

## 39. Final Rules

```
asyncio.Lock → ek task at a time
asyncio.Semaphore(N) → maximum N tasks
asyncio.Event → signal wait
asyncio.Condition → state wait
asyncio.Queue → producer-consumer
```

---

# Lesson 96: `asyncio.TaskGroup` — Structured Concurrency

## 1. Problem

```python
task1 = asyncio.create_task(worker1())
task2 = asyncio.create_task(worker2())
task3 = asyncio.create_task(worker3())

await task1
await task2
await task3
```

**Explanation:**
- Manual lifecycle management

## 2. TaskGroup Idea

```python
async with asyncio.TaskGroup() as tg:
    ...
```

## 3. TaskGroup Example

```python
async def worker(name):
    await asyncio.sleep(1)
    print(name)

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker("A"))
        tg.create_task(worker("B"))
        tg.create_task(worker("C"))
```

## 4. Automatic Wait

```
enter TaskGroup → create tasks → tasks execute → wait → all complete → exit
```

## 5. `create_task()` vs `TaskGroup.create_task()`

```
asyncio.create_task() → individual task
tg.create_task() → group-managed task
```

## 6. Structured Concurrency

```
main() → TaskGroup → Task A, Task B, Task C
```

**Explanation:**
- Child tasks parent scope ke andar

## 7. Orphan Task Problem

```
Parent → creates task → returns
Task → still running
```

## 8. Exception Handling

```python
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
```

```
A failed → B cancelled
```

## 9. Ye Design Kyun Useful

```
Task A fails → cancel siblings → cleanup → report failure
```

## 10. `ExceptionGroup`

```
ExceptionGroup
├── ValueError
└── TypeError
```

## 11. `except*`

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

## 12. `except` vs `except*`

```
except → one exception
except* → exception group matching
```

## 13. TaskGroup Cancellation

```
A fails → B cancelled → C cancelled → cleanup → TaskGroup exits
```

## 14. `CancelledError` Swallow

```python
# Bad
except asyncio.CancelledError:
    pass

# Good
except asyncio.CancelledError:
    cleanup()
    raise
```

## 15. TaskGroup Scope

```python
async def main():
    print("Before")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker_a())
        tg.create_task(worker_b())
    print("After")
```

## 16. TaskGroup vs `gather()`

```
gather() → collect concurrent results
TaskGroup → structured task lifecycle
```

## 17. `gather()` Mental Model

```
A, B, C → gather() → results
```

## 18. Result Collection

```python
async with asyncio.TaskGroup() as tg:
    task_a = tg.create_task(worker_a())
    task_b = tg.create_task(worker_b())

print(task_a.result())
print(task_b.result())
```

## 19. TaskGroup with Return Values

```python
async def worker(x):
    await asyncio.sleep(1)
    return x * 2

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(worker(10))
        task2 = tg.create_task(worker(20))
    print(task1.result())   # 20
    print(task2.result())   # 40
```

## 20. Nested TaskGroup

```
Main
├── TaskGroup A
│   ├── Task 1
│   └── Task 2
└── TaskGroup B
    ├── Task 3
    └── Task 4
```

## 21. HVAC Example

```python
async def monitor_building():
    async with asyncio.TaskGroup() as tg:
        ahu_task = tg.create_task(monitor_ahu())
        vav_task = tg.create_task(monitor_vav())
        chiller_task = tg.create_task(monitor_chiller())
```

## 22. TaskGroup + Semaphore

```python
semaphore = asyncio.Semaphore(10)

async def read_vav(vav_id):
    async with semaphore:
        return await read_from_bms(vav_id)

async with asyncio.TaskGroup() as tg:
    for vav_id in vav_ids:
        tg.create_task(read_vav(vav_id))
```

```
TaskGroup → 1000 tasks
Semaphore(10) → 10 active BMS requests
```

## 23. TaskGroup + Queue

```
TaskGroup
├── Producer 1
├── Producer 2
├── Consumer 1
└── Consumer 2
     ↓
   Queue
```

```
Queue → data flow
TaskGroup → task lifecycle
```

## 24. `create_task()` Kab

```python
task = asyncio.create_task(background_operation())
```

**Explanation:**
- Intentionally manage

## 25. TaskGroup Benefit

```
Traditional:
create task → remember → await → handle exception → cancel siblings → cleanup

TaskGroup:
async with TaskGroup → create → group manages → failure handling → cancellation → cleanup
```

## 26. TaskGroup Family Analogy

```
Parent → Family
├── Child A
├── Child B
└── Child C

Failure → parent handles → siblings cancelled → all accounted
```

## 27. TaskGroup vs ThreadPoolExecutor

```
TaskGroup → asyncio, coroutines/tasks, event loop
ThreadPoolExecutor → threads, blocking/synchronous
```

## 28. TaskGroup vs ProcessPoolExecutor

```
TaskGroup → async tasks
ProcessPoolExecutor → process workers
```

## 29. Complete Mental Map

```
Concurrency
├── threading
├── multiprocessing
├── concurrent.futures
│   ├── ThreadPoolExecutor
│   └── ProcessPoolExecutor
└── asyncio
    ├── Task
    ├── Queue
    ├── Lock
    ├── Semaphore
    ├── Event
    ├── Condition
    └── TaskGroup
```

## 30. TaskGroup 7 Key Points

```
1. Python 3.11+
2. async with asyncio.TaskGroup() as tg
3. tg.create_task(...)
4. Group exit se pehle child tasks managed
5. Ek failure sibling cancellation
6. ExceptionGroup
7. except* for groups
```

## 31. Final Memory

```
TaskGroup = "Tasks ko family/group mein rakho"
gather() → results focus
TaskGroup → lifecycle focus
```

---

# Lesson 97: `asyncio.timeout()`, `wait_for()`, `shield()`

## 1. Timeout Zarurat

```python
await read_from_bms()
# BMS response nahi → wait forever?
```

## 2. `asyncio.timeout()`

```python
async with asyncio.timeout(5):
    await operation()
```

## 3. Simple Example

```python
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
```

```
Operation = 10 sec
Timeout = 3 sec
→ timeout → TimeoutError
```

## 4. Timeout Mental Model

```
async with timeout(5)
├── finishes before 5 sec → success
└── exceeds 5 sec → cancel → TimeoutError
```

## 5. Timeout Mechanism

```
Task → await operation() → timeout expires → Task cancellation → TimeoutError
```

## 6. `CancelledError` vs `TimeoutError`

```
task.cancel() → CancelledError
timeout expires → cancellation internally → TimeoutError externally
```

## 7. `asyncio.wait_for()`

```python
await asyncio.wait_for(
    operation(),
    timeout=5
)
```

## 8. `wait_for()` Example

```python
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
```

## 9. `timeout()` vs `wait_for()`

```
wait_for() → specific awaitable timeout
timeout() → poore block ko deadline
```

## 10. Example Difference

```python
# wait_for()
result = await asyncio.wait_for(read_ahu(), timeout=5)

# timeout()
async with asyncio.timeout(5):
    await read_ahu()
    await process_data()
    await save_data()
```

## 11. Important Example

```
read_ahu = 2 sec
process = 2 sec
save = 2 sec
Total = 6 sec
timeout(5) → exceeds
```

## 12. `wait_for()` Nested

```python
await asyncio.wait_for(read_bms(), timeout=5)
# Sirf BMS operation protected
```

## 13. `timeout()` Advantage

```python
async with asyncio.timeout(10):
    data = await fetch_data()
    processed = await process(data)
    await save(processed)
```

## 14. Timeout Variable

```python
async with asyncio.timeout(10) as cm:
    await operation()
# cm.expired()
```

## 15. Timeout Reschedule

```python
async with asyncio.timeout(None) as cm:
    cm.reschedule(...)
```

## 16. Nested Timeout

```python
async with asyncio.timeout(10):
    async with asyncio.timeout(3):
        await operation()
```

## 17. `asyncio.shield()`

```python
await asyncio.shield(task)
```

**Explanation:**
- Outer task cancellation se protect

## 18. Shield Simple Idea

```
Normal: Parent cancel → Child may cancel
Shield: Parent cancel → shield protects child
```

## 19. Basic Example

```python
async def important_work():
    print("Important work started")
    await asyncio.sleep(5)
    print("Important work finished")

async def main():
    task = asyncio.create_task(important_work())
    try:
        await asyncio.shield(task)
    except asyncio.CancelledError:
        print("Parent cancelled")
    await task
```

## 20. Shield Misconception

```
shield() → Cancellation impossible? NO
Direct task.cancel() → task cancelled
```

## 21. Shield Diagram

```
cancellation
Parent Task ──────X
       │
    shield()
       │
Protected Task ──────→ continues
```

## 22. HVAC Example

```python
await asyncio.shield(save_current_equipment_state())
```

```
Shutdown → Parent cancelled → Critical save → continue
```

## 23. Shield + Timeout

```python
async with asyncio.timeout(10):
    await asyncio.shield(important_operation())
```

## 24. `wait_for()` + `shield()`

```python
task = asyncio.create_task(important_operation())

try:
    await asyncio.wait_for(
        asyncio.shield(task),
        timeout=3
    )
except TimeoutError:
    print("Wait timeout")
```

## 25. Timeout vs Shield

```
Timeout → "Kitni der wait?"
Shield → "Cancellation se protect?"
```

## 26. Comparison

| Feature | Purpose |
|---------|---------|
| `timeout()` | Block/deadline |
| `wait_for()` | Specific awaitable |
| `shield()` | Outer cancellation protect |

## 27. Complete Picture

```
Task → await → running
task.cancel() → CancelledError
timeout → cancel → TimeoutError
shield → outer cancellation → protected
```

## 28. `try/finally`

```python
async def worker():
    try:
        await do_work()
    finally:
        await cleanup()
```

## 29. `CancelledError` Swallow

```python
# Bad
except asyncio.CancelledError:
    pass

# Good
except asyncio.CancelledError:
    await cleanup()
    raise
```

## 30. Timeout + Cleanup

```python
async def read_bms():
    try:
        return await actual_bms_request()
    finally:
        print("Cleanup")

try:
    async with asyncio.timeout(5):
        data = await read_bms()
except TimeoutError:
    print("BMS timeout")
```

## 31. HVAC Architecture

```python
async with asyncio.timeout(15):
    await asyncio.wait_for(read_bms(), timeout=5)
    await asyncio.shield(save_state())
```

## 32. Shield Overuse

```
Har operation shield → shutdown slow → background work remains
Shield sirf specific cancellation semantics ke liye
```

## 33. Timeout Overuse

```
Har operation random timeout → correct nahi
Workload ke according choose
```

## 34. TaskGroup + Timeout

```python
async with asyncio.timeout(30):
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task_a())
        tg.create_task(task_b())
        tg.create_task(task_c())
```

## 35. TaskGroup + Timeout + Semaphore

```
timeout → TaskGroup → Task, Task, Task → Semaphore(10) → BMS API
```

## 36. Deeper Difference

```
wait_for() → specific awaitable
timeout() → whole scope
```

## 37. Final Memory Map

```
asyncio
├── Lock → one task
├── Semaphore → max N
├── Event → signal
├── Condition → state
├── Queue → producer/consumer
├── TaskGroup → structured lifecycle
├── timeout → deadline
├── wait_for → awaitable timeout
└── shield → cancellation protection
```

## 38. One-Line

```
timeout() → deadline
wait_for() → specific awaitable timeout
shield() → outer cancellation protection
```

## 39. Golden Pattern

```python
try:
    await operation()
except asyncio.CancelledError:
    await cleanup()
    raise
```

---

# Lesson 98: Async Context Managers + Async Iterators

## 1. Normal Versions

```python
with resource:     # __enter__/__exit__
for item in obj:   # __iter__/__next__
```

## 2. Async Versions

```python
async with resource:  # __aenter__/__aexit__
async for item in obj: # __aiter__/__anext__
```

## 3. `async with`

```python
async with resource:
    await operation()
```

## 4. `__aenter__()` / `__aexit__()`

```python
class Resource:
    async def __aenter__(self):
        ...
    async def __aexit__(self, exc_type, exc, tb):
        ...
```

## 5. Simple Example

```python
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
```

## 6. `as conn`

```python
async with Connection() as conn:
    ...
# conn = await obj.__aenter__()
```

## 7. Internally

```python
manager = Connection()
conn = await manager.__aenter__()
try:
    await conn.read()
finally:
    await manager.__aexit__(...)
```

## 8. `__aexit__()` Arguments

```python
async def __aexit__(self, exc_type, exc, tb):
    ...
```

## 9. Exception Example

```python
class Resource:
    async def __aenter__(self):
        print("Acquire")
        return self
    async def __aexit__(self, exc_type, exc, tb):
        print("Release")
        if exc:
            print("Exception:", exc)

async with Resource():
    raise ValueError("Something went wrong")
```

## 10. Exception Suppress

```python
async def __aexit__(self, exc_type, exc, tb):
    if exc:
        print("Handled:", exc)
    return True
```

**Explanation:**
- `return True` → suppress
- `return False` / `None` → propagate

## 11. Async Context Manager Use

```
Database connection
HTTP session
Network connection
WebSocket
BMS connection
```

## 12. HVAC/BMS Example

```python
class BMSConnection:
    async def __aenter__(self):
        print("Connecting to BMS...")
        await connect_to_bms()
        return self
    async def __aexit__(self, exc_type, exc, tb):
        print("Disconnecting BMS...")
        await disconnect_from_bms()

async with BMSConnection() as bms:
    ahu = await bms.read("AHU-01")
    vav = await bms.read("VAV-101")
```

## 13. Normal vs Async Context Manager

| Normal | Async |
|--------|-------|
| `with` | `async with` |
| `__enter__()` | `__aenter__()` |
| `__exit__()` | `__aexit__()` |
| normal function | `async def` |

## 14. `async for`

```python
async for item in source:
    ...
```

## 15. Normal Iterator

```python
for item in obj:
    print(item)
# __iter__ + __next__
```

## 16. Async Iterator

```python
async for item in obj:
    print(item)
# __aiter__ + __anext__
```

## 17. Async Iterator Class

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

async def main():
    async for number in Counter(3):
        print(number)
```

## 18. `__aiter__()`

```python
def __aiter__(self):
    return self
```

**Explanation:**
- Normally `async def` nahi

## 19. `__anext__()`

```python
async def __anext__(self):
    ...
# return item OR raise StopAsyncIteration
```

## 20. `async for` Internally

```python
iterator = obj.__aiter__()
while True:
    try:
        item = await iterator.__anext__()
    except StopAsyncIteration:
        break
    process(item)
```

## 21. Normal vs Async Iterator

```
Normal: next() → immediate value
Async: await next() → wait → value
```

## 22. API Stream Example

```
Server → Data 1 → wait → Data 2 → wait → Data 3

async for data in stream:
    process(data)
```

## 23. HVAC Live BMS Readings

```python
async for reading in bms_stream():
    print(reading)
```

## 24. Async Generator

```python
async def counter():
    for i in range(5):
        await asyncio.sleep(1)
        yield i

async for value in counter():
    print(value)
```

## 25. `async def` + `yield`

```python
# Normal
def generator():
    yield 1
    yield 2

# Async
async def generator():
    yield 1
    await something()
    yield 2
```

## 26. Async Generator Model

```
async generator → async for → __aiter__() → __anext__() → await → value
```

## 27. `yield` vs `return`

```
yield → value do, continue
return → generator finish
```

## 28. Practical Example

```python
async def temperature_stream():
    temperatures = [22.1, 22.4, 22.8, 23.0]
    for temp in temperatures:
        await asyncio.sleep(1)
        yield temp

async def main():
    async for temp in temperature_stream():
        print("Temperature:", temp)
```

## 29. List vs Generator

```
List → ALL DATA → memory
Generator → one item → process → one item → process
```

## 30. Real-Time Data

```python
async def bms_stream():
    while True:
        reading = await read_bms()
        yield reading

async for reading in bms_stream():
    process(reading)
```

## 31. `async with` + `async for`

```python
async with BMSConnection() as bms:
    async for reading in bms.stream():
        print(reading)
```

## 32. Full Architecture

```
Application → async with BMSConnection() → Connection acquired
→ async for reading → AHU, VAV, Temperature → Connection released
```

## 33. Async Context Manager + Timeout

```python
async with BMSConnection() as bms:
    async with asyncio.timeout(10):
        data = await bms.read("AHU-01")
```

## 34. Async Iterator + Timeout

```python
async for reading in stream:
    try:
        async with asyncio.timeout(5):
            await process(reading)
    except TimeoutError:
        print("Processing timeout")
```

## 35. Async Iterator + Queue

```python
# Queue version
async def producer(queue):
    while True:
        reading = await read_bms()
        await queue.put(reading)

# Async generator version
async def readings():
    while True:
        yield await read_bms()
```

## 36. Queue vs Async Generator

```
Async generator → one producer, sequential
Queue → multiple producers, buffering, backpressure
```

## 37. OOP Connection

```
Callable → __call__()
Iterable → __iter__ + __next__
Context Manager → __enter__ + __exit__
Async Iterator → __aiter__ + __anext__
Async Context Manager → __aenter__ + __aexit__
```

## 38. Protocol Map

```
obj() → __call__()
for x in obj → __iter__ + __next__
with obj → __enter__ + __exit__
async for x in obj → __aiter__ + __anext__
async with obj → __aenter__ + __aexit__
```

## 39. Important Distinction

```
async with → resource acquisition/release asynchronous
async for → next item obtain asynchronous
```

## 40. Comparison

| Syntax | Protocol | Purpose |
|--------|----------|---------|
| `with` | `__enter__`, `__exit__` | sync resource |
| `async with` | `__aenter__`, `__aexit__` | async resource |
| `for` | `__iter__`, `__next__` | sync iteration |
| `async for` | `__aiter__`, `__anext__` | async iteration |

## 41. Common Mistake

```python
# Wrong
async with open("data.txt") as f:
    ...

# Right
with open("data.txt") as f:
    ...
```

## 42. Common Mistake 2

```python
# Wrong
for item in async_iterator:
    ...

# Right
async for item in async_iterator:
    ...
```

## 43. Common Mistake 3

```python
# Wrong
async def __aiter__(self):
    ...

# Right
def __aiter__(self):
    return self

async def __anext__(self):
    ...
```

## 44. Common Mistake 4

```python
# Wrong in async
time.sleep(5)

# Right
await asyncio.sleep(5)
```

## 45. Object Protocol Model

```
Object
├── callable? __call__
├── iterable? __iter__
├── context manager? __enter__/__exit__
├── async iterable? __aiter__/__anext__
└── async context manager? __aenter__/__aexit__
```

## 46. Final Map

```
Python Object
├── Sync
│   ├── with → __enter__/__exit__
│   └── for → __iter__/__next__
└── Async
    ├── async with → __aenter__/__aexit__
    └── async for → __aiter__/__anext__
```

## 47. Golden Memory

```
async with → resource lifecycle asynchronous
async for → iteration asynchronous
Foundation → Python Data Model / OOP protocols
```

---

# Lesson 99: `asyncio` + Threads + Processes

## 1. Problem

```python
async def main():
    await read_bms()
    await read_database()

def old_library():
    time.sleep(10)   # Blocking
```

## 2. Golden Rule

```
Async application → Event loop ke andar blocking operation directly mat chalao
Blocking → Thread ya Process
```

## 3. `asyncio.to_thread()`

```python
async def main():
    result = await asyncio.to_thread(blocking_work)
    print(result)
```

```
asyncio → to_thread() → Thread → blocking_work()
```

## 4. Arguments

```python
result = await asyncio.to_thread(read_equipment, "AHU-01")
```

## 5. Multiple Blocking Functions

```python
async def main():
    results = await asyncio.gather(
        asyncio.to_thread(read_equipment, "AHU-01"),
        asyncio.to_thread(read_equipment, "AHU-02"),
        asyncio.to_thread(read_equipment, "AHU-03"),
    )
```

## 6. `to_thread()` Kab

```
Blocking file operations
Legacy synchronous library
Blocking database client
Blocking HTTP library
OS/file operations
```

## 7. `to_thread()` vs ThreadPoolExecutor

```python
# Simple
await asyncio.to_thread(func)

# Advanced
loop.run_in_executor(executor, func)
```

## 8. `run_in_executor()`

```python
async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        result = await loop.run_in_executor(executor, blocking_task)
```

## 9. Comparison

| | `to_thread()` | `run_in_executor()` |
|--|---------------|---------------------|
| Simple | ✅ | ❌ |
| Thread | ✅ | ✅ |
| Custom executor | ❌ | ✅ |
| Modern | ✅ | Low-level |

## 10. `to_thread()` Concept

```
Event Loop → submit blocking function → Thread Pool → function()
→ result → await resumes
```

## 11. Thread CPU Problem

```python
def cpu_heavy():
    for i in range(100_000_000):
        ...

await asyncio.to_thread(cpu_heavy)   # Parallel nahi
```

**Explanation:**
- GIL

## 12. CPU-Bound → Process

```python
async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(
            executor,
            cpu_heavy,
            10_000_000
        )
```

## 13. Thread vs Process

```
asyncio
├── Blocking I/O → Thread
└── CPU-heavy → Process
```

## 14. Asyncio CPU

```
asyncio → waiting efficiently
CPU heavy → parallel nahi automatically
```

## 15. HVAC Example

```python
def read_vav(vav_id):
    # Blocking BMS call
    ...

async def monitor():
    tasks = [
        asyncio.to_thread(read_vav, vav)
        for vav in vavs
    ]
    results = await asyncio.gather(*tasks)
```

## 16. 500 Threads

```python
semaphore = asyncio.Semaphore(10)

async def read_vav(vav_id):
    async with semaphore:
        return await asyncio.to_thread(blocking_read_vav, vav_id)
```

```
500 VAV tasks → Semaphore(10) → max 10 concurrent
```

## 17. TaskGroup + `to_thread()`

```python
async def monitor(vavs):
    async with asyncio.TaskGroup() as tg:
        for vav in vavs:
            tg.create_task(
                asyncio.to_thread(blocking_read_vav, vav)
            )
```

## 18. Production Architecture

```
TaskGroup
├── Task → Semaphore → to_thread() → Threads → BMS
```

## 19. Asyncio + Process

```
Asyncio → ProcessPool → CPU workers
```

## 20. Data Transfer

```
ProcessPoolExecutor → arguments/results serialized/pickled
```

## 21. Thread vs Process Memory

```
Threads → Shared memory
Processes → Separate memory
```

## 22. Complete Picture

```
Application → asyncio
├── I/O waiting → Thread
└── Heavy CPU → Process
```

## 23. Event Loop Block

```python
# Dangerous
async def main():
    time.sleep(10)

# Better
async def main():
    await asyncio.sleep(10)

# Actual blocking
await asyncio.to_thread(blocking_function)
```

## 24. Three Types of Waiting

```
Async waiting → await network_call()
Thread-based → await asyncio.to_thread(blocking_function)
Process-based → ProcessPoolExecutor
```

## 25. `to_thread()` Cancellation

```
Async Task cancellation ≠ force kill thread
```

## 26. Process Cancellation

```
Future cancellation ≠ actual OS process terminate
```

## 27. `run_in_executor()` Kab

```python
executor = ThreadPoolExecutor(max_workers=20)
result = await loop.run_in_executor(executor, blocking_function)
```

## 28. Modern Recommendation

```
Simple blocking → await asyncio.to_thread(func)
Custom executor → await loop.run_in_executor(executor, func)
CPU-heavy → ProcessPoolExecutor
```

## 29. Complete BMS Architecture

```
asyncio
├── BMS I/O
├── API I/O
└── Database I/O
     ↓
asyncio tasks → CPU-heavy → ProcessPoolExecutor
```

## 30. Decision Table

| Work | Best |
|------|------|
| Async HTTP | asyncio |
| Async DB | asyncio |
| Blocking HTTP | `to_thread()` |
| Blocking SDK | `to_thread()` |
| Pure Python CPU | ProcessPool |
| Many I/O tasks | asyncio |

## 31. Connection

```
asyncio
├── Queue, Lock, Event, Condition, Semaphore
├── TaskGroup
├── timeout, wait_for, shield
├── async with, async for
└── Threads/Processes
    ├── to_thread()
    └── run_in_executor()
```

## 32. Mental Model

```
asyncio → Wait efficiently
Thread → Blocking I/O
Process → CPU
Semaphore → Concurrency limit
TaskGroup → Lifecycle
Queue → Data flow
```

## 33. One-Line

```
Asyncio = WAIT
Thread = BLOCKING I/O
Process = CPU

BMS async API → asyncio
Legacy BMS SDK → to_thread()
Heavy analytics → ProcessPool
```

---

# Lesson 100: `anyio` — Unified Async API

## 1. AnyIO Kya Hai

```
Your Application → AnyIO → asyncio / Trio
```

**Explanation:**
- Async compatibility/abstraction library

## 2. Simple Example

```python
import anyio

async def main():
    await anyio.sleep(1)
    print("Done")

anyio.run(main)
```

## 3. AnyIO Faida

```python
# Asyncio-specific
asyncio.create_task()
asyncio.sleep()
asyncio.Lock()

# AnyIO abstraction
anyio.sleep()
anyio.create_task_group()
anyio.Lock()
```

## 4. Task Group

```python
async with anyio.create_task_group() as tg:
    tg.start_soon(worker, "A")
    tg.start_soon(worker, "B")
```

## 5. `TaskGroup` Comparison

```python
# Asyncio
tg.create_task(worker("A"))

# AnyIO
tg.start_soon(worker, "A")
```

## 6. `start_soon()`

```python
tg.start_soon(worker, "AHU-01")
```

**Explanation:**
- Function + args

## 7. Structured Concurrency

```
Parent scope
├── Task A
├── Task B
└── Task C
```

## 8. Failure Behavior

```
Task A → ERROR → Task Group → cancel siblings → cleanup → propagate
```

## 9. `anyio.run()`

```python
if __name__ == "__main__":
    anyio.run(main)
```

## 10. Sleep

```python
await anyio.sleep(2)
```

## 11. Cancellation

```python
async with anyio.create_task_group() as tg:
    tg.start_soon(worker)
    await anyio.sleep(3)
    tg.cancel_scope.cancel()
```

## 12. `CancelScope`

```
Cancel Scope
├── Task A
├── Task B
└── Task C
cancel() → scope ke tasks affected
```

## 13. Timeout

```python
with anyio.fail_after(5):
    await slow_operation()
```

## 14. `move_on_after`

```python
with anyio.move_on_after(5):
    await slow_operation()
```

**Explanation:**
- Timeout par scope se bahar without error

## 15. Asyncio vs AnyIO Timeout

```python
# Asyncio
asyncio.timeout(5)

# AnyIO
anyio.fail_after(5)
anyio.move_on_after(5)
```

## 16. AnyIO Lock

```python
lock = anyio.Lock()

async with lock:
    shared_data += 1
```

## 17. AnyIO Semaphore

```python
semaphore = anyio.Semaphore(10)

async with semaphore:
    await read_bms()
```

## 18. HVAC Example

```python
semaphore = anyio.Semaphore(10)

async def read_vav(vav_id):
    async with semaphore:
        return await read_bms(vav_id)

async with anyio.create_task_group() as tg:
    for vav_id in vav_ids:
        tg.start_soon(read_vav, vav_id)
```

## 19. AnyIO Streams

```
Producer → Stream → Consumer
```

## 20. Memory Stream

```python
send, receive = anyio.create_memory_object_stream()
await send.send("AHU-01")
value = await receive.receive()
```

## 21. Queue vs Stream

```
Queue → data queue
Stream → communication channel abstraction
```

## 22. Producer-Consumer

```python
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
```

## 23. AnyIO + Async Context Manager

```python
async with send:
    await send.send(data)
```

## 24. AnyIO + Threads

```python
result = await anyio.to_thread.run_sync(blocking_function)
```

## 25. AnyIO + Process

```
AnyIO
├── async tasks
├── streams
├── cancellation
└── blocking bridge → thread
```

## 26. AnyIO Biggest Benefit

```
Library → AnyIO → async backend
```

## 27. AnyIO Zarurat Nahi

```
sirf asyncio, FastAPI → direct asyncio fine
AnyIO → reusable libraries, backend abstraction
```

## 28. AnyIO vs Asyncio

| Feature | Asyncio | AnyIO |
|---------|---------|-------|
| Standard library | ✅ | ❌ |
| Async runtime | ✅ | Abstraction |
| TaskGroup | ✅ | ✅ |
| Lock | ✅ | ✅ |
| Streams | Limited | Strong |
| Trio compat | ❌ | ✅ |

## 29. Asyncio Replace?

```
Nahi, exactly replace nahi karta
asyncio → actual runtime
AnyIO → higher-level abstraction
```

## 30. Trio

```
AnyIO
├── asyncio
└── Trio
```

## 31. Why Useful

```
BMS application → AnyIO → async backend
```

## 32. Limitation

```
asyncio-specific API → abstraction break
```

## 33. OOP Connection

```
Implementation → Abstract async behavior → Application
```

## 34. Complete Ecosystem Map

```
ASYNC PYTHON
├── asyncio
│   ├── Tasks, Queue, Locks
│   ├── timeout, shield, TaskGroup
│   └── Streams (limited)
└── AnyIO
    ├── TaskGroup, Streams
    ├── Producer/Consumer
    └── Cancel scopes
```

## 35. HVAC/BMS Architecture

```
BMS Monitoring → AnyIO → TaskGroup
├── AHU, VAV, Chiller
└── Semaphore(10) → BMS API → Readings → Memory Stream
    → Processing → Database
```

## 36. Memory Trick

```
asyncio → Python standard async toolkit
AnyIO → common/high-level async abstraction
TaskGroup → structured lifecycle
Semaphore → concurrency limit
Stream → async data flow
CancelScope → cancellation boundary
to_thread → blocking sync bridge
```

## 37. Complete Journey

```
Threading → Multiprocessing → concurrent.futures → GIL
→ asyncio → asyncio synchronization → TaskGroup
→ Timeout/Cancellation → Async Context Manager
→ Async Iterator → asyncio + Threads/Processes → AnyIO
```

**Ab ye guide complete hai (Lessons 91-100).** Har lesson mein:
- ✅ Code
- ✅ Output
- ✅ Line-by-line explanation
- ✅ Mental models
- ✅ Golden rules

Agar kisi specific topic ko aur detail mein samjhana ho, to batao! 🚀