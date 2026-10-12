# Python Threading — Basic se Advanced (Roman Urdu)

Python mein threading aik aisa concept hai jis ki madad se hum aik program ke andar multiple threads bana sakte hain, taake multiple tasks ko concurrently execute kiya ja sake.

Main tumhein threading zero se advanced level tak Roman Urdu mein samjhaunga, practical code examples, real-world projects, common mistakes aur interview concepts ke saath.

## 1. Threading kya hoti hai?

Sab se pehle 3 concepts samjho:

- Process: Running program ki apni execution environment hoti hai.
- Thread: Process ke andar execution ka aik flow hota hai.
- Concurrency: Multiple tasks ki progress aik hi time period mein hoti hai, chahe woh bari bari execute hon.

Misal ke taur par, tumhara program 3 kaam kar raha hai:

1. File download karna.
2. API se data lena.
3. File mein data save karna.

Agar har task ko bari bari execute karoge, to kuch tasks doosre task ke complete hone ka wait karenge. Threading ki madad se independent tasks ki progress overlap karwa sakte ho.

### Sequential vs Threading

Sequential execution

Task A — 2 sec

Task B — 2 sec

Task C — 2 sec

Total: taqreeban 6 seconds

Concurrent execution

Task A — 2 sec

Task B — 2 sec

Task C — 2 sec

Total: ideal case mein taqreeban 2 seconds, plus overhead

Yeh timings illustrative hain. Real performance task ki type, resources aur overhead par depend karti hai.

## 2. Threading kab use karni chahiye?

| Task ki type                                | Behtar approach                                |
| ------------------------------------------- | ---------------------------------------------- |
| API requests / network calls                | `threading` ya `ThreadPoolExecutor`            |
| Files read/write karna                      | Threading useful ho sakti hai                  |
| Database network queries                    | Threading useful ho sakti hai                  |
| Heavy CPU calculations                      | `multiprocessing` ya suitable native libraries |
| Bohat saari asynchronous network operations | `asyncio` bhi suitable hai                     |

Important: Python ke standard CPython build mein GIL (Global Interpreter Lock) aam tor par aik waqt mein sirf aik thread ko Python bytecode execute karne deta hai. Is liye CPU-heavy Python code mein threads se zaroori nahi ke speed improve ho. I/O-bound tasks mein threading phir bhi bohat useful hai.

## 3. Apna pehla thread banao

Python mein built-in `threading` module available hai.

```
import threadingdef say_hello():    print("Hello from thread!")thread = threading.Thread(target=say_hello)thread.start()thread.join()print("Main program finished")
```

Is code ko line by line samjho:

- `import threading`: threading module import hota hai.
- `def say_hello()`: woh function jo thread execute karega.
- `threading.Thread(...)`: naya thread object banata hai.
- `target=say_hello`: function ka reference deta hai; function ko abhi call nahi karte.
- `thread.start()`: thread ki execution shuru karta hai.
- `thread.join()`: main thread ko wait karwata hai jab tak doosra thread complete na ho.
- Aakhri `print()` tab chalega jab `join()` wala thread complete ho jayega.

### `start()` aur `run()` mein farq

```
thread.start()  # Thread ki execution start karta haithread.run()    # Method ko current thread mein directly execute karta hai
```

Aam tor par thread chalane ke liye `start()` use karo. `run()` ko directly call karna naya thread start nahi karta.

## 4. Multiple threads ek saath chalana

Ab hum 3 different tasks ko alag threads mein chalayenge.

```
import threadingimport timedef task(name):    print(f"{name} start hua")    time.sleep(2)    print(f"{name} complete hua")t1 = threading.Thread(target=task, args=("Task 1",))t2 = threading.Thread(target=task, args=("Task 2",))t3 = threading.Thread(target=task, args=("Task 3",))t1.start()t2.start()t3.start()t1.join()t2.join()t3.join()print("Sab tasks complete!")
```

### `args=("Task 1",)` mein comma kyun hai?

Python mein single-item tuple banane ke liye comma zaroori hai:

```
("Task 1",)  # Tuple("Task 1")   # String
```

Agar function ko arguments dene hain, to `args` tuple use hota hai.

`time.sleep(2)` sirf demonstration ke liye hai. Yeh current thread ko 2 seconds ke liye pause karta hai, poore program ko nahi.

Practice: Is example mein 3 tasks ke bajaye 5 tasks chalao aur observe karo ke total execution time sequential execution se kam ho sakta hai.

## 5. Main thread aur child threads

Jab Python program start hota hai, to aam tor par `MainThread` hota hai. Jab tum `threading.Thread()` banate ho aur us par `start()` call karte ho, to ek additional thread start hota hai.

```
import threadingdef worker():    print("Worker:", threading.current_thread().name)print("Main:", threading.current_thread().name)t = threading.Thread(    target=worker,    name="MyWorker")t.start()t.join()
```

Possible output:

```
Main: MainThread
Worker: MyWorker
```

Thread names debugging mein bohat useful hote hain.

### Thread ki important properties

```
import threadingdef worker():    print("Worker chal raha hai")t = threading.Thread(target=worker, name="Worker-1")print(t.name)print(t.is_alive())t.start()print(t.is_alive())t.join()print(t.is_alive())
```

- `t.name`: thread ka naam.
- `t.is_alive()`: batata hai ke thread abhi execute ho raha hai ya nahi.
- `t.ident`: thread ka identifier, jab assign ho chuka ho.
- `threading.active_count()`: currently active threading objects ki tadaad.
- `threading.current_thread()`: current thread object.

`is_alive()` ki value execution ke waqt par depend karti hai, is liye har run mein same output ki guarantee nahi.

## 6. Threading mein arguments aur return values

Thread ke target function ko arguments dena simple hai, lekin normal function ki tarah `Thread` object se direct return value nahi milti.

### Arguments dena

```
import threadingdef calculate(a, b):    print("Sum:", a + b)t = threading.Thread(    target=calculate,    args=(10, 20))t.start()t.join()
```

### Keyword arguments dena

```
import threadingdef greet(name, message):    print(f"{message}, {name}!")t = threading.Thread(    target=greet,    kwargs={        "name": "Ali",        "message": "Assalam-o-Alaikum"    })t.start()t.join()
```

iframe

### Return value hasil karna

Agar results collect karne hain, to `queue.Queue` ya `concurrent.futures.ThreadPoolExecutor` use karna behtar hai. Advanced aur professional Python mein `ThreadPoolExecutor` aksar sab se convenient option hota hai.

## 7. `ThreadPoolExecutor` — professional approach

Har task ke liye manually thread create karne ke bajaye thread pool manage kar sakte ho.

```
from concurrent.futures import ThreadPoolExecutorimport timedef download_file(file_id):    print(f"File {file_id} download ho rahi hai")    time.sleep(1)    return f"File {file_id} complete"with ThreadPoolExecutor(max_workers=3) as executor:    futures = [        executor.submit(download_file, i)        for i in range(1, 6)    ]    for future in futures:        print(future.result())print("Tamam downloads complete")
```

Is example mein 5 tasks hain, magar maximum 3 worker threads aik waqt mein execute ho sakte hain.

Important methods:

| Method               | Kaam                                         |
| -------------------- | -------------------------------------------- |
| `submit()`           | Task submit karta hai aur `Future` deta hai  |
| `future.result()`    | Result deta hai; zaroorat par wait karta hai |
| `future.done()`      | Batata hai task complete hua ya nahi         |
| `future.exception()` | Task se aane wali exception deta hai         |
| `map()`              | Multiple inputs par function chalata hai     |

`with` block complete hone par executor default taur par submitted tasks ke khatam hone ka wait karta hai.

### `submit()` aur `map()` ka farq

```
from concurrent.futures import ThreadPoolExecutordef square(n):    return n * nwith ThreadPoolExecutor(max_workers=3) as pool:    results = list(pool.map(square, [1, 2, 3, 4, 5]))print(results)
```

Output:

```
[1, 4, 9, 16, 25]
```

`map()` results input order mein deta hai, chahe tasks kisi aur order mein complete hue hon. `submit()` tumhein har task ke `Future` par alag control deta hai.

## 8. Thread safety aur race conditions

Yeh threading ka bohat important advanced topic hai.

Maan lo multiple threads aik shared variable ko update kar rahe hain:

```
import threadingcounter = 0def increment():    global counter    for _ in range(100_000):        counter += 1threads = [    threading.Thread(target=increment)    for _ in range(5)]for t in threads:    t.start()for t in threads:    t.join()print(counter)
```

iframe

Expected mathematical result `500000` hai. Lekin shared mutable state par synchronization ke baghair depend karna safe nahi. Is example ka result Python implementation, execution details aur concurrency behavior par depend kar sakta hai.

Jab multiple threads aik shared resource ko coordinated protection ke baghair access ya modify karte hain, to race condition paida ho sakti hai.

### Solution: `Lock`

```
import threadingcounter = 0lock = threading.Lock()def increment():    global counter    for _ in range(100_000):        with lock:            counter += 1threads = [    threading.Thread(target=increment)    for _ in range(5)]for t in threads:    t.start()for t in threads:    t.join()print(counter)  # 500000
```

`with lock:` ensure karta hai ke protected code section mein ek waqt mein sirf aik thread enter kare.

Rule: Shared mutable data ko synchronize karo. Sirf GIL par correctness ke liye bharosa mat karo.

## 9. `Lock`, `RLock`, `Semaphore` aur `Condition`

In tools ka maqsad threads ke darmiyan coordination aur shared resources ki safety maintain karna hai.

### 9.1 `Lock` — aik waqt mein aik thread

```
import threadinglock = threading.Lock()with lock:    print("Critical section")
```

`Lock` tab use karo jab shared variable, file ya doosra resource protected access maangta ho.

Lock ko manually bhi acquire aur release kar sakte ho:

```
lock.acquire()try:    print("Protected operation")finally:    lock.release()
```

`with lock:` aam tor par zyada safe aur readable hai, kyun ke exception aane par bhi lock release ho jata hai.

### 9.2 `RLock` — reentrant lock

Agar aik hi thread ko nested function calls ke through same lock dobara acquire karna ho, to `RLock` useful hai.

```
import threadinglock = threading.RLock()def outer():    with lock:        print("Outer")        inner()def inner():    with lock:        print("Inner")outer()
```

Yeh code successfully chalega. Ordinary `Lock` ke saath isi tarah nested acquisition karne se thread deadlock kar sakta hai.

`RLock` tabhi use karo jab reentrant behavior ki waqai zaroorat ho.

### 9.3 `Semaphore` — limited access

Agar tumhare paas 3 database connections hain aur tum ek waqt mein maximum 3 operations allow karna chahte ho, to `Semaphore(3)` use kar sakte ho.

```
import threadingimport timesemaphore = threading.Semaphore(3)def access_resource(task_id):    with semaphore:        print(f"Task {task_id}: resource use kar raha hai")        time.sleep(1)threads = [    threading.Thread(target=access_resource, args=(i,))    for i in range(1, 8)]for t in threads:    t.start()for t in threads:    t.join()
```

Maximum 3 threads semaphore ke protected section mein enter kar sakte hain.

### 9.4 `Event` — threads ko signal dena

`Event` aik thread ko doosre thread ke signal ka wait karne deta hai.

```
import threadingimport timeready = threading.Event()def worker():    print("Signal ka wait ho raha hai...")    ready.wait()    print("Signal mil gaya!")t = threading.Thread(target=worker)t.start()time.sleep(2)ready.set()t.join()
```

Important methods:

- `set()` — event signal ko set karta hai.
- `wait()` — signal aane tak wait karta hai.
- `clear()` — signal reset karta hai.
- `is_set()` — signal ki current state check karta hai.

### 9.5 `Condition` — specific condition ka wait

`Condition` tab useful hota hai jab thread ko kisi shared state ke particular condition meet hone ka wait karna ho.

```
import threadingcondition = threading.Condition()data_ready = Falsedef consumer():    global data_ready    with condition:        condition.wait_for(lambda: data_ready)        print("Data available hai")def producer():    global data_ready    with condition:        data_ready = True        condition.notify_all()t = threading.Thread(target=consumer)t.start()producer()t.join()
```

`wait_for()` condition ko check karta rehta hai aur condition true hone par execution continue karta hai. Yeh simple `sleep()` se zyada reliable synchronization pattern hai.

## 10. `Queue` — producer-consumer pattern

Real applications mein shared list par multiple threads se read/write karne ke bajaye `queue.Queue` bohat useful hai.

Producer

Tasks queue mein daalta hai

Thread-safe Queue

Tasks ko safe tareeqay se store karti hai

Worker 1

Worker 2

Complete example:

```
import threadingfrom queue import Queuetasks = Queue()def worker():    while True:        item = tasks.get()        try:            if item is None:                return            print(f"Processing: {item}")        finally:            tasks.task_done()for item in range(1, 6):    tasks.put(item)workers = [    threading.Thread(target=worker)    for _ in range(2)]for t in workers:    t.start()tasks.join()for _ in workers:    tasks.put(None)for t in workers:    t.join()print("All tasks processed")
```

Is example mein:

1. Producer 5 tasks queue mein daalta hai.
2. Do workers queue se tasks lete hain.
3. `get()` aik task nikalta hai.
4. `task_done()` us task ke complete hone ko mark karta hai.
5. `tasks.join()` tamam submitted tasks complete hone ka wait karta hai.
6. `None` sentinel workers ko terminate karne ka signal deta hai.

Yeh pattern background processing, email sending, file processing aur job queues mein use hota hai.

Important: Agar worker ke andar processing fail ho jaye, to `finally` mein `task_done()` call hona queue ke accounting ke liye zaroori hai. Production system mein exceptions ko log aur handle bhi karna chahiye.

## 11. Daemon aur non-daemon threads

Python mein threads default taur par apne parent/current thread ki daemon status inherit karte hain.

```
import threadingimport timedef background_task():    while True:        print("Background task")        time.sleep(1)t = threading.Thread(    target=background_task,    daemon=True)t.start()
```

- Daemon thread: Sirf daemon threads baqi hon to Python process unke complete hone ka wait nahi karta.
- Non-daemon thread: Python process aam tor par us ke complete hone tak terminate nahi hota.

Daemon threads ko un tasks ke liye use karna munasib hai jo process exit par abruptly stop ho sakte hain aur jinke cleanup ki guarantee zaroori nahi.

Database writes, transactions aur important file saving ke liye daemon thread par blindly depend mat karo.

Graceful shutdown ke liye `Event` zyada behtar hai:

```
import threadingimport timestop_event = threading.Event()def worker():    while not stop_event.is_set():        print("Working...")        stop_event.wait(1)t = threading.Thread(target=worker)t.start()time.sleep(3)stop_event.set()t.join()print("Worker safely stopped")
```

Python ka `Thread` API kisi running thread ko safely forcefully kill karne ka general-purpose method provide nahi karta. Is liye cooperative cancellation use ki jati hai.

## 12. Threading mein exception handling

Thread ke andar exception aaye to woh automatically main thread ke normal control flow mein propagate nahi hoti.

```
import threadingdef worker():    try:        result = 10 / 0    except ZeroDivisionError as error:        print("Worker error:", error)t = threading.Thread(target=worker)t.start()t.join()print("Main thread continue kar raha hai")
```

Agar errors ko caller tak return karna ho, to `ThreadPoolExecutor` ka `Future` convenient hai:

```
from concurrent.futures import ThreadPoolExecutordef divide(a, b):    return a / bwith ThreadPoolExecutor() as pool:    future = pool.submit(divide, 10, 0)    try:        print(future.result())    except ZeroDivisionError as error:        print("Task fail hua:", error)
```

`future.result()` task ki exception ko caller ke thread mein raise karta hai.

Advanced use cases mein `threading.excepthook` uncaught thread exceptions ki centralized reporting ke liye bhi use kiya ja sakta hai.

## 13. Deadlock kya hota hai?

Deadlock tab hota hai jab threads aik doosre ke resources ka wait karte rehte hain aur koi bhi aage nahi barh pata.

Example scenario:

- Thread A ke paas Lock 1 hai aur woh Lock 2 ka wait karta hai.
- Thread B ke paas Lock 2 hai aur woh Lock 1 ka wait karta hai.

Dono permanently wait kar sakte hain.

Deadlock se bachne ke tareeqay:

1. Multiple locks ko hamesha aik consistent order mein acquire karo.
2. Locks ko unnecessary der tak hold mat karo.
3. Lock ke andar network request ya lambi blocking operation se bacho.
4. Zaroorat par timeout use karo.
5. Nested locks ko simple rakho aur shared state ki design improve karo.

Timeout example:

```
import threadinglock = threading.Lock()if lock.acquire(timeout=2):    try:        print("Lock mil gaya")    finally:        lock.release()else:    print("Lock timeout: resource available nahi")
```

Timeout deadlock ko automatically solve nahi karta, lekin indefinite waiting se bachne mein madad karta hai.

## 14. `threading.local()` — har thread ka apna data

Kabhi tum chahte ho ke har thread ka variable alag ho, aur threads aik doosre ke variable ko overwrite na karein.

```
import threadinglocal_data = threading.local()def worker(name):    local_data.username = name    print(        threading.current_thread().name,        local_data.username    )threads = [    threading.Thread(        target=worker,        args=(f"User-{i}",),        name=f"Worker-{i}"    )    for i in range(3)]for t in threads:    t.start()for t in threads:    t.join()
```

Har thread ko `local_data.username` ki apni value milti hai.

Yeh pattern thread-specific context, legacy database connection handling aur kuch request-processing systems mein kaam aa sakta hai. Modern applications mein explicit context passing ya context variables bhi relevant ho sakte hain, khaas taur par jab `asyncio` use ho raha ho.

## 15. `Barrier` — sab threads ka aik point par wait karna

`Barrier` multiple threads ko tab tak rok sakta hai jab tak required threads us point par na pohanch jayein.

```
import threadingimport timebarrier = threading.Barrier(3)def worker(name):    print(f"{name}: preparation start")    time.sleep(1)    print(f"{name}: barrier ka wait")    barrier.wait()    print(f"{name}: next phase start")threads = [    threading.Thread(target=worker, args=(f"Worker-{i}",))    for i in range(3)]for t in threads:    t.start()for t in threads:    t.join()
```

Is example mein teenon threads apni preparation ke baad barrier par pohanchte hain. Jab teeno arrive ho jate hain, tab woh aglay phase mein ja sakte hain.

Yeh synchronized simulation, parallel test phases aur coordinated processing mein useful hai.

## 16. Thread cancellation aur timeout

Thread ko safely cancel karne ke liye `Event` use kar sakte ho. Lekin thread pool mein submitted tasks ke liye `Future.cancel()` bhi important hai.

```
from concurrent.futures import ThreadPoolExecutorimport timedef task():    time.sleep(3)    return "Complete"with ThreadPoolExecutor(max_workers=1) as pool:    future = pool.submit(task)    cancelled = future.cancel()    print("Cancel hua:", cancelled)
```

Agar task abhi start nahi hua, to `cancel()` usay cancel kar sakta hai. Agar task already running hai, to `cancel()` aam tor par usay stop nahi kar sakta.

Running tasks ke liye cooperative cancellation use karo, jaisa `Event` wale example mein dekha.

`future.result(timeout=2)` bhi available hai. Yeh caller ko maximum specified wait time deta hai, magar timeout aane se background task khud-ba-khud terminate nahi hota.

## 17. `BoundedSemaphore` aur resource limits

`Semaphore` ke similar `BoundedSemaphore` bhi hota hai.

```
import threadingslots = threading.BoundedSemaphore(2)with slots:    print("Resource use ho raha hai")
```

`BoundedSemaphore` initial capacity se zyada permits release karne ki programming error ko detect karne mein madad karta hai. Limited connections, concurrent downloads aur rate-limited resources mein yeh useful hai.

## 18. CPU-bound aur I/O-bound tasks ka farq

Yeh decision Python concurrency mein bohat important hai.

I/O-bound

API calls, network requests, disk reads, database waits.

Aksar `ThreadPoolExecutor` suitable hai.

CPU-bound

Pure Python mein heavy calculations, image transformations aur computational loops.

Aksar `ProcessPoolExecutor` ya optimized native libraries behtar hoti hain.

### I/O-bound example

```
from concurrent.futures import ThreadPoolExecutorimport timedef fetch_data(n):    time.sleep(1)  # Network wait ko simulate karna    return f"Data {n}"with ThreadPoolExecutor(max_workers=5) as pool:    results = list(pool.map(fetch_data, range(10)))print(results)
```

Yeh example waiting time ko overlap karta hai.

### CPU-bound ke liye multiprocessing

```
from concurrent.futures import ProcessPoolExecutordef square(n):    return n * nif __name__ == "__main__":    with ProcessPoolExecutor() as pool:        results = list(pool.map(square, range(10)))    print(results)
```

`ProcessPoolExecutor` alag processes use karta hai, jo standard GIL wale CPython mein CPU parallelism ke liye useful ho sakte hain. Windows par `if __name__ == "__main__":` guard zaroori hai.

## 19. Advanced best practices

Production code mein in principles ko follow karo:

- Thread ki tadaad limit karo; har task ke liye unlimited threads create mat karo.
- `ThreadPoolExecutor` se worker lifecycle manage karo.
- Shared state ko `Lock`, `Queue` ya doosri synchronization primitives se protect karo.
- Thread names aur Python `logging` module use karo.
- Network calls par timeouts set karo.
- Exceptions ko explicitly handle karo.
- Shutdown ke waqt running tasks ko cooperative signal do.
- Thread pool ke andar ek task se doosre task ka `Future.result()` wait karte waqt deadlock ka risk samjho.
- Benchmark ke baghair yeh assume mat karo ke threading performance improve karegi.
- GIL ke behavior ko apne Python version aur build ke context mein samjho.

### Logging ke saath threading

```
import loggingimport threadinglogging.basicConfig(    level=logging.INFO,    format="%(asctime)s %(threadName)s %(levelname)s: %(message)s")def worker():    logging.info("Task start hua")    logging.info("Task complete hua")t = threading.Thread(    target=worker,    name="Worker-1")t.start()t.join()
```

`threadName` logs mein batata hai ke kis thread ne message generate kiya. Multiple modules aur production applications mein centralized logging debugging ko kaafi asaan banati hai.

## 20. Real-world mini project: Concurrent task processor

Ab tamam important concepts ko aik practical project mein combine karte hain. Yeh program tasks ko queue mein rakhega, 3 worker threads se process karega, errors ko handle karega aur logging use karega.

```
import loggingimport threadingimport timefrom queue import Queuelogging.basicConfig(    level=logging.INFO,    format="%(asctime)s | %(threadName)s | %(levelname)s | %(message)s")task_queue = Queue()stop_event = threading.Event()def process_task(task_id):    """Task processing ko simulate karta hai."""    if task_id == 4:        raise ValueError("Invalid task ID: 4")    time.sleep(0.5)    return f"Task {task_id} successfully processed"def worker():    while True:        if stop_event.is_set() and task_queue.empty():            return        try:            task_id = task_queue.get(timeout=0.2)        except Exception:            continue        try:            result = process_task(task_id)            logging.info(result)        except Exception:            logging.exception(                "Task %s process nahi ho saka",                task_id            )        finally:            task_queue.task_done()def main():    threads = [        threading.Thread(            target=worker,            name=f"Worker-{i}"        )        for i in range(1, 4)    ]    for t in threads:        t.start()    try:        for task_id in range(1, 11):            task_queue.put(task_id)        task_queue.join()    finally:        stop_event.set()        for t in threads:            t.join()    logging.info("All tasks complete")if __name__ == "__main__":    main()
```

### Project mein kya seekha?

- `Queue`: tasks ko safely distribute karna.
- `Thread`: multiple workers chalana.
- `Event`: workers ko shutdown signal dena.
- `try/except`: task failure handle karna.
- `finally`: har retrieved task ki queue accounting complete karna.
- `logging`: errors aur successful tasks ka record rakhna.
- `join()`: tasks aur threads ke complete hone ka wait karna.

Production note: Is project mein `except Exception` sirf worker ko unexpected task failures ke baad zinda rakhne ke liye use hua hai. Production code mein expected exceptions ko specifically catch karna, unexpected exceptions ko log karna, aur shutdown logic ko tested rakhna behtar hai.

## 21. Threading mastery roadmap

## Learning checklist

0/6 complete

Thread basics

Thread, start(), join(), args, kwargs

Beginner

ThreadPoolExecutor

submit(), map(), Future aur timeout

Beginner–Intermediate

Synchronization

Lock, RLock, Semaphore, Event

Intermediate

Queues and coordination

Queue, Condition, Barrier, producer-consumer

Intermediate–Advanced

Failures and shutdown

Exceptions, cancellation, graceful shutdown

Advanced

Production patterns

Logging, testing, deadlocks, performance, resource limits

Advanced

## 22. Apni understanding test karo

1\. \`thread.start()\` aur \`thread.join()\` ka kya farq hai?

Dono thread start karte hain

start execution shuru karta hai, join completion ka wait karta hai

join thread ko kill karta hai

2\. CPU-heavy pure Python tasks ke liye standard CPython mein kya aksar behtar hai?

Har task ke liye daemon thread

Sirf Lock use karna

ProcessPoolExecutor

3\. \`Queue.task_done()\` ka kya role hai?

Queue delete karta hai

Retrieved task ko completed mark karta hai

Thread ko terminate karta hai

4\. Kya \`Future.cancel()\` running thread ko forcefully stop karta hai?

Haan, hamesha

Nahi, aam tor par sirf abhi tak start na hone wale task ko cancel karta hai

Sirf daemon threads ko

Quiz reset karo

Final recommendation: Pehle `Thread` aur `join()` ko achhi tarah practice karo, phir `ThreadPoolExecutor`, `Lock`, `Queue` aur graceful shutdown par focus karo. In concepts ke baad tum concurrent file processing, API fetching aur background job systems banane ke liye achhi foundation hasil kar loge.