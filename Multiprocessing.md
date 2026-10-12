# Python Multiprocessing — Basic se Advanced (Roman Urdu)

Python mein Multiprocessing aik aisi technique hai jis se hum apne program ke multiple processes chala sakte hain. Har process ka apna Python interpreter aur aam tor par apni memory hoti hai.

Agar aap Python mein concurrency, threading aur async samajh chuke hain, to multiprocessing agla important topic hai. Isay hum basic se le kar advanced level tak examples ke saath samjhenge.

## 1. Multiprocessing kya hoti hai?

Socho aap ke paas 4 heavy calculations hain. Aik normal program inhein aik ke baad aik perform kar sakta hai. Multiprocessing mein hum mukhtalif processes par calculations distribute kar sakte hain, taa-ke multiple CPU cores par kaam parallel ho sake.

Main Process

Kaam ko divide karta hai

Process 1

Task A

Process 2

Task B

Process 3

Task C

Process 4

Task D

Conceptual diagram: actual parallelism available CPU cores, operating system aur workload par depend karti hai.

### Process aur Thread mein farq

| Feature         | Threading                                                 | Multiprocessing                           |
| --------------- | --------------------------------------------------------- | ----------------------------------------- |
| Execution unit  | Thread                                                    | Process                                   |
| Memory          | Aam tor par shared                                        | Alag memory spaces                        |
| CPU-heavy tasks | GIL ki wajah se pure Python code mein limited parallelism | Multiple CPU cores par parallelism mumkin |
| Communication   | Relatively easy                                           | IPC ki zaroorat ho sakti hai              |
| Resource cost   | Aam tor par kam                                           | Aam tor par zyada                         |
| Best use        | I/O-bound tasks                                           | CPU-bound tasks                           |

I/O-bound: Network requests, files read karna, API calls.

CPU-bound: Heavy mathematical calculations, image processing, large data transformations.

Python ke standard CPython build mein GIL (Global Interpreter Lock) hota hai. Multiprocessing alag processes ke zariye CPU-bound Python code ko multiple cores par chala sakti hai.

## 2. Sab se pehla multiprocessing program

Python ka built-in `multiprocessing` module use karte hain.

```
import multiprocessingimport osdef worker():    print("Worker process chal raha hai")    print("Process ID:", os.getpid())if __name__ == "__main__":    p = multiprocessing.Process(target=worker)    p.start()    p.join()    print("Main process complete")
```

### Code ko samjho

1. `multiprocessing.Process()` naya process banane ke liye use hota hai.
2. `target=worker` batata hai ke naye process mein kaunsa function execute hoga.
3. `p.start()` process ko start karta hai.
4. `p.join()` main process ko wait karwata hai jab tak worker finish nahi ho jata.
5. `os.getpid()` current process ki unique process ID deta hai.

`if __name__ == "__main__":` bohat important hai, khaas tor par Windows par. Is se child process ke start hone par main program baar baar unintended tareeqe se execute nahi hota.

Output ka order thora different ho sakta hai, kyun ke processes ka schedule operating system karta hai.

## 3. Multiple processes chalana

Ab 4 workers chalate hain.

```
import multiprocessingimport osimport timedef worker(number):    print(f"Worker {number}, PID: {os.getpid()}")    time.sleep(1)    print(f"Worker {number} complete")if __name__ == "__main__":    processes = []    for i in range(4):        p = multiprocessing.Process(            target=worker,            args=(i,)        )        processes.append(p)        p.start()    for p in processes:        p.join()    print("Tamam workers complete")
```

Yahan `args=(i,)` aik single argument tuple hai. Aakhri comma zaroori hai, warna `(i)` sirf aik integer hoga.

Is example mein 4 workers aik doosre ke saath overlap kar sakte hain. Har worker ka apna process ID hoga.

`join()` ko sab processes par call karne ka faida yeh hai ke main program tamam workers ke finish hone se pehle aage nahi barhega.

## 4. `Pool` — Professional multiprocessing ka important concept

Jab aap ke paas 1000 tasks hon, to har task ke liye naya process banana mehnga ho sakta hai. `Pool` processes ka aik group banata hai aur tasks ko un mein distribute karta hai.

### `Pool.map()` ka use

```
from multiprocessing import Poolimport osdef square(number):    return number * numberif __name__ == "__main__":    numbers = [2, 3, 4, 5, 6]    with Pool(processes=3) as pool:        results = pool.map(square, numbers)    print(results)
```

Output:

```
[4, 9, 16, 25, 36]
```

Is code mein:

- `Pool(processes=3)` teen worker processes ka pool banata hai.
- `pool.map()` list ke har element par `square()` execute karta hai.
- Results input ke order mein return hote hain.
- `with` block se pool ki cleanup automatically manage hoti hai.

Important: `pool.map()` blocking hota hai. Yani results aane tak calling code wait karta hai.

### `map()`, `starmap()` aur `imap()`

| Method                        | Kaam                                            |
| ----------------------------- | ----------------------------------------------- |
| `map(func, items)`            | Har item par function; tamam results list mein  |
| `starmap(func, items)`        | Har item ke andar arguments ko unpack karta hai |
| `imap(func, items)`           | Results iterator ke zariye lazily deta hai      |
| `imap_unordered(func, items)` | Results completion ke order mein deta hai       |

Misal ke taur par, agar function do arguments leta hai:

```
from multiprocessing import Pooldef multiply(a, b):    return a * bif __name__ == "__main__":    pairs = [(2, 3), (4, 5), (6, 7)]    with Pool(3) as pool:        results = pool.starmap(multiply, pairs)    print(results)
```

Output:

```
[6, 20, 42]
```

## 5. `ProcessPoolExecutor` — Modern Python approach

`concurrent.futures` module mein `ProcessPoolExecutor` milta hai. Yeh multiprocessing ke liye aik convenient aur readable interface hai.

```
from concurrent.futures import ProcessPoolExecutordef cube(n):    return n ** 3if __name__ == "__main__":    numbers = [2, 3, 4, 5, 6]    with ProcessPoolExecutor(max_workers=3) as executor:        results = list(executor.map(cube, numbers))    print(results)
```

Output:

```
[8, 27, 64, 125, 216]
```

`max_workers=3` maximum teen workers allow karta hai. `executor.map()` results ko input ke order mein deta hai.

Aap jab naya project bana rahe hon, to `ProcessPoolExecutor` aik achha default option hai. Lekin agar aap ko process lifecycle, IPC, queues ya shared memory par zyada control chahiye, to `multiprocessing` module seedha use kar sakte hain.

## 6. `submit()` aur `Future`

Jab har task ko alag submit karna ho aur us ka result baad mein lena ho, `submit()` use karein.

```
from concurrent.futures import ProcessPoolExecutordef calculate(n):    return n * nif __name__ == "__main__":    with ProcessPoolExecutor(max_workers=2) as executor:        future1 = executor.submit(calculate, 10)        future2 = executor.submit(calculate, 20)        print(future1.result())        print(future2.result())
```

Output:

```
100
400
```

`Future` aik object hai jo represent karta hai ke task ka result abhi pending hai ya available.

- `future.result()` result ka wait karta hai.
- `future.done()` batata hai ke task finish hua ya nahi.
- `future.exception()` task ki exception deta hai, agar koi exception hui ho.

`submit()` se aap tasks ko individual handle kar sakte hain. Lekin `.result()` foran call karne se us jagah execution wait kar sakta hai.

## 7. `Queue` — Processes ke darmiyan communication

Har process ki apni memory hoti hai. Is liye parent process ka normal variable child process mein automatically shared nahi hota.

Processes ke darmiyan data bhejne ke liye `multiprocessing.Queue` use kar sakte hain.

```
import multiprocessingdef worker(queue):    result = 10 * 10    queue.put(result)if __name__ == "__main__":    queue = multiprocessing.Queue()    p = multiprocessing.Process(        target=worker,        args=(queue,)    )    p.start()    result = queue.get()    p.join()    print("Result:", result)
```

Output:

```
Result: 100
```

Yahan:

- `queue.put()` data queue mein bhejta hai.
- `queue.get()` queue se data receive karta hai; data na ho to yeh wait kar sakta hai.
- Queue processes ke darmiyan data exchange ka safe aur convenient tareeqa hai.

### Real-world use cases

- Worker processes se results collect karna.
- Background tasks ko distribute karna.
- Image-processing pipeline mein aik stage ka result doosri stage ko dena.
- Multiple workers se errors ya status messages collect karna.

Agar queue mein bohat zyada data ho, to memory aur serialization overhead ka khayal rakhna zaroori hai.

## 8. `Pipe` — Do processes ke darmiyan direct communication

`Pipe()` do connection endpoints deta hai. Aik process doosre ko message bhej sakta hai.

```
import multiprocessingdef worker(connection):    connection.send("Worker ka message")    connection.close()if __name__ == "__main__":    parent_conn, child_conn = multiprocessing.Pipe()    p = multiprocessing.Process(        target=worker,        args=(child_conn,)    )    p.start()    message = parent_conn.recv()    p.join()    print(message)    parent_conn.close()
```

Output:

```
Worker ka message
```

Queue vs Pipe: Queue multiple producers aur consumers ke liye useful hoti hai. Pipe direct communication ke liye achhi hai, khaas tor par jab endpoints ka structure simple ho.

## 9. Shared memory: `Value` aur `Array`

Aam Python variables processes ke darmiyan automatically share nahi hote. Agar aap ko chhota sa shared numeric value ya array chahiye, to `Value` aur `Array` use kar sakte hain.

```
import multiprocessingdef worker(shared_value):    shared_value.value += 10if __name__ == "__main__":    value = multiprocessing.Value("i", 0)    p = multiprocessing.Process(        target=worker,        args=(value,)    )    p.start()    p.join()    print(value.value)
```

Output:

```
10
```

Yahan `"i"` integer type ko represent karta hai aur `value.value` shared integer ki value access karta hai.

### Aik bohat important race condition

Agar multiple processes ek hi waqt par yeh karein:

```
shared_value.value += 1
```

to result incorrect ho sakta hai. Is operation mein read, increment aur write ke multiple steps hain.

Isay `Lock` se protect karein:

```
import multiprocessingdef increment(counter, lock):    for _ in range(10000):        with lock:            counter.value += 1if __name__ == "__main__":    counter = multiprocessing.Value("i", 0)    lock = multiprocessing.Lock()    processes = [        multiprocessing.Process(            target=increment,            args=(counter, lock)        )        for _ in range(4)    ]    for p in processes:        p.start()    for p in processes:        p.join()    print(counter.value)
```

Expected output:

```
40000
```

`with lock:` aik waqt mein sirf aik process ko protected section execute karne deta hai.

Lekin yaad rakhein: lock contention performance ko slow kar sakti hai. Har calculation ko shared state par dependent banane ke bajaye independent tasks aur final aggregation aksar zyada efficient hoti hai.

## 10. `Lock`, `RLock`, `Semaphore` aur `Event`

Multiprocessing mein synchronization ka matlab hai processes ke darmiyan execution ko control karna, taa-ke race conditions aur unwanted access se bacha ja sake.

`Lock`

Aik waqt mein sirf aik process ko critical section access karne deta hai.

`RLock`

Wohi process lock ko dobara acquire kar sakta hai, agar us ne pehle acquire kiya ho.

`Semaphore`

Aik waqt mein limited processes ko resource access karne deta hai.

`Event`

Aik process doosre processes ko signal de sakta hai ke koi condition ya stage complete ho gayi hai.

### Semaphore ka example

Suppose aik service sirf 2 workers ko aik waqt mein resource access karne dena chahti hai.

```
import multiprocessingimport timedef worker(number, semaphore):    with semaphore:        print(f"Worker {number}: resource use kar raha hai")        time.sleep(1)        print(f"Worker {number}: resource release kar diya")if __name__ == "__main__":    semaphore = multiprocessing.Semaphore(2)    processes = [        multiprocessing.Process(            target=worker,            args=(i, semaphore)        )        for i in range(5)    ]    for p in processes:        p.start()    for p in processes:        p.join()
```

Is mein 5 workers hain, magar aik waqt mein maximum 2 workers semaphore ke protected section mein honge.

## 11. `Event` se processes ko signal dena

Aik worker ko tab tak wait karwana jab tak main process usay signal na de:

```
import multiprocessingimport timedef worker(event):    print("Worker wait kar raha hai")    event.wait()    print("Signal mil gaya, worker aage chala")if __name__ == "__main__":    event = multiprocessing.Event()    p = multiprocessing.Process(        target=worker,        args=(event,)    )    p.start()    time.sleep(2)    event.set()    p.join()
```

`event.wait()` signal ka wait karta hai. `event.set()` signal set karta hai, aur wait karne wale processes aage barh sakte hain.

Production applications mein `sleep()` ko sirf demonstration ke liye use karein; actual coordination ke liye events, queues ya doosre synchronization primitives zyada munasib hain.

## 12. Advanced: Process start methods

Python mukhtalif tareeqon se child process start kar sakta hai.

| Method       | Concept                                                 |
| ------------ | ------------------------------------------------------- |
| `spawn`      | Naya interpreter start hota hai                         |
| `fork`       | Parent process ki state fork ke zariye inherit hoti hai |
| `forkserver` | Aik server process naye child processes fork karta hai  |

Start methods operating system aur Python version ke mutabiq different default rakh sakte hain. Windows par `spawn` use hota hai; modern macOS par bhi `spawn` default hai. Linux par aam tor par `fork` raha hai, lekin Python version aur platform ke mutabiq default verify karna chahiye.

### `spawn` explicitly use karna

```
import multiprocessingdef worker():    print("Spawn process chal raha hai")if __name__ == "__main__":    ctx = multiprocessing.get_context("spawn")    p = ctx.Process(target=worker)    p.start()    p.join()
```

`get_context("spawn")` aap ko specific start method use karne deta hai, baghair poore program ka global start method change kiye.

Advanced rule: Process ke target functions aur un ke arguments ko child process tak transfer karna possible hona chahiye. `spawn` ke saath aam tor par target function module ke top level par define hona chahiye; local functions aur lambdas aksar standard multiprocessing ke liye suitable nahi hote.

## 13. Pickling aur serialization

Processes ke darmiyan Python objects bhejne ke liye `multiprocessing` aksar `pickle` serialization use karta hai.

Aam tor par integers, strings, lists, dictionaries aur top-level functions ko transfer karna mumkin hota hai, jab un ke contents bhi serializable hon.

Misal ke taur par:

```
data = {    "student_id": 101,    "name": "Ali",    "marks": [80, 90, 85]}
```

Is tarah ka data queue mein bhejna aam tor par theek hai.

Lekin open file handles, kuch database connections, locks aur operating-system resources ko aam data ki tarah serialize nahi kiya ja sakta.

Best practice: Process ke andar file ya database connection khud open karein, aur processes ke darmiyan sirf zaroori data transfer karein.

## 14. Advanced: Exception handling aur worker failures

Multiprocessing mein exception ko handle karna is baat par depend karta hai ke aap `Process`, `Pool` ya `ProcessPoolExecutor` use kar rahe hain.

### `ProcessPoolExecutor` ke saath errors

```
from concurrent.futures import ProcessPoolExecutordef divide(a, b):    return a / bif __name__ == "__main__":    with ProcessPoolExecutor(max_workers=2) as executor:        futures = [            executor.submit(divide, 10, 2),            executor.submit(divide, 10, 0),        ]        for future in futures:            try:                print(future.result())            except ZeroDivisionError:                print("Error: zero se divide nahi kar sakte")            except Exception as exc:                print(f"Unexpected error: {exc}")
```

Output mein aik successful result aur aik error message milega. `future.result()` worker ki exception ko calling process mein raise kar sakta hai.

### Process exit code check karna

Jab aap seedha `Process` use karte hain, to `join()` ke baad `exitcode` check karein:

```
p.start()p.join()if p.exitcode == 0:    print("Process successfully complete hua")else:    print("Process fail hua:", p.exitcode)
```

Exit code `0` aam tor par successful completion ko represent karta hai; non-zero code failure ko indicate kar sakta hai.

Agar worker process unexpected tareeqe se crash ho jaye, to us ka result queue mein aane ki guarantee nahi hoti. Production systems mein timeout, exit-code checks aur failure recovery plan karna zaroori hai.

## 15. Timeout aur hung processes se bachao

Agar koi worker hang ho jaye, to program hamesha wait kar sakta hai. Is liye timeout ka use seekhna zaroori hai.

```
from concurrent.futures import ProcessPoolExecutor, TimeoutErrorimport timedef slow_task():    time.sleep(5)    return "Task complete"if __name__ == "__main__":    with ProcessPoolExecutor(max_workers=1) as executor:        future = executor.submit(slow_task)        try:            result = future.result(timeout=2)            print(result)        except TimeoutError:            print("Task ka result 2 seconds mein nahi mila")
```

Important: `future.result(timeout=2)` sirf wait karne ki muddat limit karta hai. Yeh zaroori nahi ke worker task cancel ho jaye. Executor ka context manager exit hote waqt running task ka wait bhi kar sakta hai.

Agar hard deadline aur cancellation zaroori ho, to Python version ke mutabiq available executor termination methods ya process lifecycle ko explicitly manage karna hota hai.

## 16. `Pool` ka `chunksize` aur performance tuning

Jab bohat zyada chhote tasks hon, to har task ko alag dispatch karne ka overhead barh sakta hai. `chunksize` tasks ko batches mein distribute karne mein madad karta hai.

```
with multiprocessing.Pool(4) as pool:    results = pool.map(square, numbers, chunksize=100)
```

Is example mein tasks ko takreeban 100-item chunks mein group kiya jata hai, jahan munasib ho.

- Chhote tasks ke liye bara `chunksize` overhead kam kar sakta hai.
- Uneven task durations mein chhota `chunksize` load balancing ko behtar kar sakta hai.
- Bohat bara `chunksize` kuch workers ko busy aur doosron ko idle chhor sakta hai.

Koi aik `chunksize` har workload ke liye best nahi hota. Representative data par benchmark karna chahiye.

## 17. `Manager` — Shared dictionary aur list

Agar aap ko processes ke darmiyan shared dictionary ya list chahiye, to `multiprocessing.Manager()` use kar sakte hain.

```
import multiprocessingdef worker(shared_data):    shared_data["count"] = shared_data.get("count", 0) + 1if __name__ == "__main__":    with multiprocessing.Manager() as manager:        shared_data = manager.dict()        shared_data["count"] = 0        processes = [            multiprocessing.Process(                target=worker,                args=(shared_data,)            )            for _ in range(4)        ]        for p in processes:            p.start()        for p in processes:            p.join()        print(shared_data)
```

Is example mein output lazmi taur par `{'count': 4}` nahi hoga. Kyun? Kyun ke `get()`, increment aur assignment aik atomic operation nahi hain. Multiple workers aik hi purani value read kar sakte hain.

Agar aap ko exact count chahiye, to lock use karein:

```
def worker(shared_data, lock):    with lock:        shared_data["count"] = shared_data.get("count", 0) + 1
```

Aur har process ko `args=(shared_data, lock)` pass karein.

Performance note: `Manager` ka shared data aik manager server process ke zariye access hota hai, is liye bohat frequent operations ke liye yeh `Value` ya local calculations se slow ho sakta hai.

## 18. Daemon processes aur process lifecycle

`Process` mein `daemon` property background worker ke lifecycle ko control karne ke liye use hoti hai.

```
p = multiprocessing.Process(target=worker)p.daemon = Truep.start()
```

Daemon process parent ke exit hone par terminate kiya ja sakta hai. Yeh guaranteed graceful shutdown ka substitute nahi hai.

Yaad rakhein:

- `start()` process start karta hai.
- `join()` process ke finish hone ka wait karta hai.
- `is_alive()` batata hai ke process abhi run kar raha hai ya nahi.
- `terminate()` process ko zabardasti terminate kar sakta hai; cleanup aur shared resources ke hawale se yeh risky hai.

Jahan mumkin ho, workers ko queue sentinel, event ya doosre cooperative shutdown mechanism se band karein.

## 19. Real-world mini project: Parallel square calculator

Ab hum in concepts ko aik chhote practical project mein combine karte hain.

```
from concurrent.futures import ProcessPoolExecutorimport osimport timedef calculate_square(number):    result = number ** 2    return {        "number": number,        "square": result,        "pid": os.getpid(),    }def main():    numbers = list(range(1, 11))    start_time = time.perf_counter()    with ProcessPoolExecutor(max_workers=4) as executor:        results = list(            executor.map(calculate_square, numbers)        )    elapsed = time.perf_counter() - start_time    for result in results:        print(            f"{result['number']} ka square = "            f"{result['square']}, "            f"PID = {result['pid']}"        )    print(f"Total elapsed time: {elapsed:.4f} seconds")
```

### Is project mein kya seekha?

1. `ProcessPoolExecutor` se worker processes manage kiye.
2. `executor.map()` se tasks distribute kiye.
3. Har worker ne dictionary ki shakal mein result return kiya.
4. `os.getpid()` se worker process identify kiya.
5. `time.perf_counter()` se elapsed time measure kiya.

Yeh learning project hai. Sirf 10 chhoti calculations ke liye multiprocessing aam tor par faida nahi degi, kyun ke process startup aur communication ka overhead calculation se zyada ho sakta hai.

## 20. Multiprocessing ke common pitfalls

1\. `if __name__ == "__main__":` bhool jana

Windows aur `spawn` environment mein recursive process creation ya startup errors ho sakte hain.

2\. Lambda ya local function ko target banana

Standard multiprocessing mein target functions ko module ke top level par define karein, khaas tor par `spawn` ke saath.

3\. Bohat zyada processes banana

CPU cores se bohat zyada CPU-heavy workers banana lazmi nahi ke performance improve kare.

4\. Shared variable ko lock ke baghair update karna

Race condition ki wajah se data incorrect ho sakta hai.

5\. Process ko join na karna

Parent process cleanup ya completion se pehle aage barh sakta hai.

6\. Har task ke liye bohat bara data bhejna

Pickling, copying aur inter-process communication ka overhead performance ko reduce kar sakta hai.

## 21. Threading, Async aur Multiprocessing kab use karein?

| Scenario                                     | Behtar starting point                        |
| -------------------------------------------- | -------------------------------------------- |
| Bohat si API requests                        | `asyncio` ya threading                       |
| Files ya network ka wait                     | Threading ya async                           |
| CPU-heavy mathematical calculations          | Multiprocessing                              |
| Image processing ke independent tasks        | Multiprocessing                              |
| Tasks ko background mein distribute karna    | `ProcessPoolExecutor` ya queue-based workers |
| Multiple processes mein shared numeric state | `Value`, `Array` aur locks                   |
| Shared dictionary/list                       | `Manager`, jab us ka overhead acceptable ho  |

## 22. Practice roadmap: Basic se advanced

## Learning checklist

0/15 complete

Level 1 — Fundamentals

Aik Process create aur start karo

Teen workers chalao aur PID print karo

start() aur join() ka farq samjho

Level 2 — Pools

Pool.map() se squares calculate karo

starmap() se do arguments pass karo

ProcessPoolExecutor se results return karo

Level 3 — Communication

Queue se worker ka result receive karo

Pipe se message bhejo

Value aur Lock se safe counter banao

Level 4 — Advanced

Worker exception handle karo

Future par timeout implement karo

spawn context ke saath test karo

Level 5 — Production

Chunk size benchmark karo

Worker failures aur exit codes handle karo

Parallel file-processing project banao

## Final understanding

Multiprocessing mein mastery ke liye in 5 concepts par sab se zyada focus karein:

1. Process lifecycle: `Process`, `start()`, `join()` aur exit codes.
2. Task distribution: `Pool` aur `ProcessPoolExecutor`.
3. Inter-process communication: `Queue`, `Pipe` aur `Manager`.
4. Synchronization: `Lock`, `Semaphore`, `Event` aur shared memory.
5. Production reliability: Exception handling, timeouts, start methods aur performance profiling.

Agla practical step yeh hoga ke aap Parallel File Processing System banayein, jo multiple files ko alag processes se process kare, errors ko log kare, aur tamam results ko aik final JSON report mein save kare. Is project se multiprocessing ke fundamentals se production-level patterns tak practice ho jayegi.