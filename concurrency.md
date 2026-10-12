# Python Concurrency — Basic se Advanced (Roman Urdu)

Python mein Concurrency aik bohat important concept hai. Agar aap Python ko professional level par seekhna chahte ho, to concurrency ke saath `threading`, `multiprocessing`, `asyncio`, `Future`, `Lock`, `Semaphore`, `Queue`, aur race conditions ko samajhna zaroori hai.

Hum isay step-by-step basic se advanced level tak seekhenge, code examples aur real-world projects ke saath.

## 1. Concurrency kya hoti hai?

Concurrency ka matlab hai ke program multiple tasks ko is tarah manage kare ke unki execution aik doosray ke darmiyan overlap kar sake.

Misal ke taur par, aapka program:

- Internet se data download kar raha hai.
- File read kar raha hai.
- User ka input le raha hai.
- Database se records fetch kar raha hai.

Agar har task ke complete hone ka intezar karna zaroori ho, to program slow feel ho sakta hai. Concurrency se hum in tasks ko efficiently manage kar sakte hain.

## Sequential vs Concurrent

Sequential — aik task ke baad doosra

Task A

Task B

Task C

A complete hoga, phir B, phir C.

Concurrent — tasks ki execution overlap kar sakti hai

Task A

Task B

Task C

Yeh conceptual timeline hai; actual execution tasks aur available resources par depend karti hai.

Yaad rakho: Concurrency ka matlab lazmi nahi ke tasks ek hi waqt par physically execute hon. Is ke baraks, parallelism mein multiple tasks waqai ek hi waqt mein execute ho sakte hain.

## 2. Concurrency aur Parallelism mein farq

| Feature    | Concurrency                               | Parallelism                           |
| ---------- | ----------------------------------------- | ------------------------------------- |
| Matlab     | Multiple tasks ko manage karna            | Multiple tasks ek saath execute karna |
| Main focus | Efficient task coordination               | Simultaneous computation              |
| Example    | Multiple websites se responses ka intezar | Multiple CPU cores par calculations   |
| Useful for | I/O-bound work                            | CPU-bound work                        |

I/O-bound tasks woh hain jo network, disk ya database ka intezar karte hain. CPU-bound tasks woh hain jin mein processor intensive calculations karta hai.

## 3. Python mein concurrency ke 3 main tools

[Threading in Python: A Detailed Explanation | by Yogeshkrishnanseeniraj | Medium](https://images.openai.com/static-rsc-4/SmNn4ziqqWF_BY3wkv57Bfy5f9FAQvOklR-BFcoq0IpuY28nt9BuAMDSMF11cru_qBcWe7_RlyfH3MeMSDC0rCgmw9nD0JKn9UtbBpJDMiZdHNa4C74EVsr_kFMx2Wak7e-5wnIC_8jyeXGga1MwaixuPMEtmKm6ftA9gek1apY?purpose=inline)

1\. `threading`

I/O-bound tasks, jaise APIs call karna, files read karna aur network requests.

Threads aik process ke andar memory share karte hain.

[If You Think Concurrency = Parallelism, Read This Before Your Next Interview | by The Latency Gambler | Medium](https://images.openai.com/static-rsc-4/vJ725ocVNJ5HzS08vw6YaxbpIPq6Ro7MnbgQiLFQ8JNxXJEwdzJooPAOfP2v79iA74ztqoHSZRjo0AF744ReCI5LB65CPs-k1AzZ-qx9nTjmaUsoDGtGZ1Uqlcts1Vgw08szTSnAFlZKR6LsQlSym1p64RxzZzT7405qQ7mPlF4?purpose=inline)

2\. `multiprocessing`

CPU-heavy calculations ko multiple processes mein distribute karna.

Har process ka apna Python interpreter aur aam tor par apni memory hoti hai.

[Python asyncio: All you need to know with Examples | by Mostafa Farrag | Medium](https://images.openai.com/static-rsc-4/TWMB0QrmXpxdhWALIH0-NIunUse5iEhJipBpZAeT1wQmEUVKfFxVujL5k_RfZEaZwaZ-MsuIR5mPdUbdFhlYezjz9QACJ2Q2cCX5gObC-X0ZUE0sJjo3O_kEU2XwkUHPni4tgqD9iI2HA2lXq7VxmB3-fZ_w5c2_ArpcN5-yFVc?purpose=inline)

3\. `asyncio`

Bohat saare I/O tasks ko `async` aur `await` ke zariye efficiently manage karna.

Aik event loop cooperative tareeqay se tasks ko schedule kar sakta hai.

Ek aur important baat: standard GIL-enabled CPython mein threads aam tor par pure Python CPU-bound code ko multiple cores par parallel execute nahi karte. Python ke free-threaded builds mein yeh behavior different ho sakta hai.

## 4. Sab se pehla practical example: Sequential execution

Pehle samjho ke concurrency ke baghair program kaise chalta hai.

```
import timedef task(name):    print(f"{name} start")    time.sleep(2)    print(f"{name} complete")start = time.perf_counter()task("Task A")task("Task B")task("Task C")end = time.perf_counter()print(f"Total time: {end - start:.2f} seconds")
```

Expected output:

```
Task A start
Task A complete
Task B start
Task B complete
Task C start
Task C complete
Total time: 6.00 seconds
```

`time.sleep(2)` program ko 2 seconds ke liye wait karwata hai. Teen tasks sequentially chal rahe hain, is liye total time taqreeban 6 seconds hai.

`time.perf_counter()` elapsed time measure karne ke liye useful hai.

## 5. Threading — multiple threads chalana

Ab isi example ko concurrent banate hain.

```
import timeimport threadingdef task(name):    print(f"{name} start")    time.sleep(2)    print(f"{name} complete")start = time.perf_counter()threads = []for name in ["A", "B", "C"]:    thread = threading.Thread(        target=task,        args=(name,)    )    threads.append(thread)    thread.start()for thread in threads:    thread.join()end = time.perf_counter()print(f"Total time: {end - start:.2f} seconds")
```

Expected total time taqreeban 2 seconds hoga, scheduling overhead ke ilawa.

### Code ki explanation

- `threading.Thread()` aik naya thread object banata hai.
- `target=task` batata hai ke kaunsa function execute karna hai.
- `args=(name,)` function ko argument deta hai. Comma zaroori hai, kyun ke single-element tuple hai.
- `thread.start()` thread ko execute karne ke liye start karta hai.
- `thread.join()` current thread ko tab tak wait karwata hai jab tak specified thread complete na ho.

Important: `start()` aur `join()` alag hain. `start()` task ko shuru karta hai, jabke `join()` uske complete hone ka intezar karta hai.

### Khud try karo

Agar `time.sleep(2)` ko `time.sleep(4)` kar do, to teen concurrent tasks ka total time aam tor par 4 seconds ke qareeb hoga, 12 seconds nahi.

## 6. ThreadPoolExecutor — professional approach

Har task ke liye manually thread banana hamesha zaroori nahi. Python ka `concurrent.futures` module thread pool provide karta hai.

```
import timefrom concurrent.futures import ThreadPoolExecutordef download_file(file_id):    print(f"Downloading file {file_id}")    time.sleep(2)    return f"File {file_id} downloaded"with ThreadPoolExecutor(max_workers=3) as executor:    results = executor.map(        download_file,        [1, 2, 3, 4, 5]    )    for result in results:        print(result)
```

Yahan `max_workers=3` ka matlab hai ke aik waqt mein maximum 3 worker tasks execute ho sakte hain. Paanch tasks teen workers ke darmiyan process honge.

`executor.map()` input ke order mein results return karta hai, chahe tasks mukhtalif waqt mein complete hon.

### `submit()` aur `Future`

Agar aapko har task ka result alag se manage karna hai, to `submit()` aur `Future` use kar sakte ho.

```
from concurrent.futures import ThreadPoolExecutor, as_completedimport timedef calculate(value):    time.sleep(value)    return value * valuewith ThreadPoolExecutor(max_workers=3) as executor:    futures = [        executor.submit(calculate, value)        for value in [3, 1, 2]    ]    for future in as_completed(futures):        try:            print("Result:", future.result())        except Exception as exc:            print("Task failed:", exc)
```

Is mein:

- `submit()` task schedule karta hai aur `Future` return karta hai.
- `future.result()` result deta hai. Agar task abhi complete nahi hua, to yeh wait kar sakta hai.
- `as_completed()` futures ko completion order mein yield karta hai.
- Task ke andar exception aaye, to `future.result()` par woh exception raise hota hai.

Advanced code mein `Future` ko task ki state, result aur error manage karne ke liye use kiya jata hai.

## 7. Race Condition — concurrency ka bara masla

Race condition tab hoti hai jab multiple threads shared data ko access ya modify karte hain aur final result execution timing par depend karta hai.

Misal:

```
import threadingcounter = 0def increment():    global counter    for _ in range(100_000):        counter += 1threads = [    threading.Thread(target=increment)    for _ in range(4)]for thread in threads:    thread.start()for thread in threads:    thread.join()print(counter)
```

Is code mein expected logical result `400000` hai. Lekin shared mutable state ko bina synchronization modify karna safe design nahi hai. GIL-enabled CPython mein bhi compound operations ko automatically application-level atomic samajhna durust nahi.

Is maslay ka hal: Lock.

### 7.1 Lock ka use

```
import threadingcounter = 0lock = threading.Lock()def increment():    global counter    for _ in range(100_000):        with lock:            counter += 1threads = [    threading.Thread(target=increment)    for _ in range(4)]for thread in threads:    thread.start()for thread in threads:    thread.join()print(counter)  # 400000
```

`with lock:` ensure karta hai ke aik waqt mein sirf aik thread protected section execute kare.

Lock ko sirf critical section mein rakho. Agar poora task lock ke andar chala do, to concurrency ka faida kam ho sakta hai.

### 7.2 Deadlock kya hota hai?

Deadlock tab ho sakta hai jab threads aik doosray ke resources ka intezar karte rahen aur koi aage na barh sake.

Misal:

- Thread A ne Lock 1 liya aur Lock 2 ka intezar kar raha hai.
- Thread B ne Lock 2 liya aur Lock 1 ka intezar kar raha hai.

Bachne ke tareeqay:

1. Locks hamesha aik consistent order mein acquire karo.
2. Lock ko minimum waqt ke liye hold karo.
3. Zaroorat par timeout use karo.
4. Nested locks ko carefully design karo.

## 8. Threading ke advanced synchronization tools

Python mein sirf `Lock` hi nahi, doosray synchronization primitives bhi hain.

| Tool          | Use case                                                |
| ------------- | ------------------------------------------------------- |
| `RLock`       | Wohi thread aik lock ko dobara acquire kar sake         |
| `Semaphore`   | Concurrent access ki maximum limit control karna        |
| `Event`       | Aik thread se doosray threads ko signal dena            |
| `Condition`   | Kisi condition ke true hone ka wait karna               |
| `Barrier`     | Multiple threads ko aik synchronization point par rokna |
| `queue.Queue` | Threads ke darmiyan safely data transfer karna          |

### Semaphore example

Maan lo aapke paas aik service hai jo aik waqt mein maximum 2 requests handle kar sakti hai.

```
import threadingimport timesemaphore = threading.Semaphore(2)def request(request_id):    with semaphore:        print(f"Request {request_id} started")        time.sleep(2)        print(f"Request {request_id} finished")threads = [    threading.Thread(target=request, args=(i,))    for i in range(1, 6)]for thread in threads:    thread.start()for thread in threads:    thread.join()
```

Paanch requests execute hongi, lekin aik waqt mein maximum do requests semaphore ke protected section mein hongi.

### Thread-safe Queue

Producer-consumer pattern mein aik thread data banata hai aur doosra process karta hai.

```
import threadingfrom queue import Queuejobs = Queue()def producer():    for item in range(5):        jobs.put(item)def consumer():    while True:        item = jobs.get()        try:            if item is None:                return            print("Processing:", item)        finally:            jobs.task_done()worker = threading.Thread(target=consumer)worker.start()producer()jobs.put(None)  # Worker ko stop signaljobs.join()worker.join()
```

`Queue` threads ke darmiyan data transfer ko synchronize karti hai. `task_done()` har retrieved item ke processing complete hone ko indicate karta hai; `join()` queue ke tamam submitted items complete hone ka wait karta hai.

## 9. Multiprocessing — CPU-bound tasks ke liye

Agar task bohat zyada calculations karta hai, jaise image processing, large mathematical computations ya data transformation, to multiprocessing useful ho sakti hai.

```
from concurrent.futures import ProcessPoolExecutorimport timedef square(number):    return number * numberif __name__ == "__main__":    numbers = range(1, 11)    with ProcessPoolExecutor(max_workers=4) as executor:        results = list(executor.map(square, numbers))    print(results)
```

Output:

```
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

Yahan alag processes mein tasks execute ho sakte hain, jis se CPU-bound work multiple CPU cores par parallel chal sakta hai.

### `if __name__ == "__main__":` kyun?

Khaas taur par Windows par process start karne ke liye module ko dobara import kiya ja sakta hai. Main guard child processes ko anjaane mein dobara process pool create karne se bachata hai.

Multiprocessing ke kuch trade-offs:

- Process create karne ka overhead.
- Data serialization (pickling) aur inter-process communication ka kharcha.
- Processes ke darmiyan shared memory ko manage karne ki complexity.
- Worker functions aur unke arguments ka aam tor par pickle-compatible hona zaroori hai.

Har chhoti calculation ke liye process pool banana zaroori nahi. Pehle benchmark karo.

## 10. Asyncio — modern Python concurrency

`asyncio` asynchronous programming ke liye use hota hai. Yeh khaas taur par tab useful hai jab aapko bohat saare network requests, API calls ya doosre I/O operations manage karne hon.

### 10.1 `async` aur `await` samjho

```
import asyncioasync def task(name):    print(f"{name} started")    await asyncio.sleep(2)    print(f"{name} completed")async def main():    await task("A")    await task("B")    await task("C")asyncio.run(main())
```

Yahan total time taqreeban 6 seconds hoga. Wajah yeh hai ke `await task()` har task ko sequentially complete karwata hai.

`async def` coroutine function banata hai, jabke `await` kisi awaitable operation ke complete hone ka intezar karta hai.

### 10.2 `asyncio.gather()` se concurrent tasks

Ab teen tasks ko concurrently execute karte hain.

```
import asyncioimport timeasync def task(name):    print(f"{name} started")    await asyncio.sleep(2)    print(f"{name} completed")    return nameasync def main():    start = time.perf_counter()    results = await asyncio.gather(        task("A"),        task("B"),        task("C")    )    print("Results:", results)    print(f"Time: {time.perf_counter() - start:.2f}s")asyncio.run(main())
```

Expected time taqreeban 2 seconds hoga.

Asal farq: `asyncio.sleep()` event loop ko doosray tasks chalane ka mauqa deta hai. `time.sleep()` event-loop thread ko block kar deta hai.

### 10.3 `asyncio.create_task()`

Agar aap coroutine ko background mein schedule karna chahte ho, to `create_task()` use kar sakte ho.

```
import asyncioasync def download(name, delay):    await asyncio.sleep(delay)    return f"{name} downloaded"async def main():    task1 = asyncio.create_task(download("File A", 2))    task2 = asyncio.create_task(download("File B", 1))    result1 = await task1    result2 = await task2    print(result1)    print(result2)asyncio.run(main())
```

Dono tasks overlap karte hain. `task2` pehle complete ho sakta hai, lekin code `task1` ka result pehle await kar raha hai.

### 10.4 Async task errors aur cancellation

Production applications mein sirf tasks start karna kaafi nahi. Unke exceptions aur cancellation ko bhi handle karna hota hai.

```
import asyncioasync def worker():    try:        await asyncio.sleep(10)    except asyncio.CancelledError:        print("Worker cancelled")        raiseasync def main():    task = asyncio.create_task(worker())    await asyncio.sleep(0.1)    task.cancel()    try:        await task    except asyncio.CancelledError:        print("Cancellation handled")asyncio.run(main())
```

`task.cancel()` cancellation request karta hai. `CancelledError` ko handle karne ke baad aam tor par dobara raise karna behtar hota hai, taake cancellation ka signal sahi tarah propagate ho.

## 11. Advanced asyncio: Semaphore aur timeout

Maan lo 100 APIs call karni hain, lekin aap aik waqt mein sirf 10 requests allow karna chahte ho.

```
import asynciosemaphore = asyncio.Semaphore(10)async def fetch(item_id):    async with semaphore:        await asyncio.sleep(1)        return f"Data {item_id}"async def main():    results = await asyncio.gather(        *(fetch(i) for i in range(100))    )    print(len(results))asyncio.run(main())
```

Semaphore concurrent operations ko limit karta hai. Yeh code demonstration ke liye hai; real API requests ke liye actual asynchronous HTTP client use karna hoga.

### Timeout lagana

```
import asyncioasync def slow_operation():    await asyncio.sleep(10)    return "Done"async def main():    try:        result = await asyncio.wait_for(            slow_operation(),            timeout=2        )        print(result)    except TimeoutError:        print("Operation timed out")asyncio.run(main())
```

Agar operation 2 seconds mein complete nahi hota, to timeout exception raise hoti hai aur operation cancel kiya jata hai. External system par pehle se bheji hui request ka side effect zaroori nahi ke undo ho jaye.

## 12. `asyncio.TaskGroup` — structured concurrency

Python 3.11 aur uske baad ke versions mein `TaskGroup` related tasks ko aik group mein manage karne ka clean tareeqa hai.

```
import asyncioasync def fetch_data(item_id):    await asyncio.sleep(1)    return f"Data {item_id}"async def main():    async with asyncio.TaskGroup() as group:        tasks = [            group.create_task(fetch_data(i))            for i in range(3)        ]    results = [task.result() for task in tasks]    print(results)asyncio.run(main())
```

`TaskGroup` ke faide:

- Group ke tasks context se nikalne se pehle complete hote hain.
- Task fail hone par group baqi tasks ki cancellation aur errors ko structured tareeqay se manage karta hai.
- Task lifecycle ko track karna asaan hota hai.

Agar multiple tasks fail hon, to errors `ExceptionGroup` ki shakal mein mil sakte hain.

## 13. `asyncio` ke andar blocking code se bachna

Yeh aik common mistake hai:

```
import asyncioimport timeasync def bad_task():    time.sleep(5)  # Event loop block ho jayega
```

Is tarah ka blocking code doosray async tasks ko bhi rok sakta hai.

Agar blocking I/O function ko badal nahi sakte, to usay thread mein run karwa sakte ho:

```
import asyncioimport timedef blocking_function():    time.sleep(2)    return "Completed"async def main():    result = await asyncio.to_thread(blocking_function)    print(result)asyncio.run(main())
```

`asyncio.to_thread()` Python 3.9+ mein available hai. Yeh blocking I/O ko event-loop thread se bahar execute karne ke liye useful hai.

Pure Python CPU-bound work ke liye, GIL-enabled CPython mein, `ProcessPoolExecutor` zyada suitable ho sakta hai.

## 14. Kaunsa tool kab use karna hai?

## Decision guide

I/O-bound

Network requests, files, blocking database calls

`threading` ya `ThreadPoolExecutor` use karo. Agar libraries asynchronous hain aur bohat saare I/O tasks hain, to `asyncio` consider karo.

CPU-bound

Heavy calculations, image processing, computation

GIL-enabled CPython mein `multiprocessing` ya `ProcessPoolExecutor` consider karo.

Task coordination

Shared data, workers, controlled access

Threads ke liye `Lock`, `Semaphore` aur `Queue`; async code ke liye `asyncio.Lock`, `asyncio.Semaphore` aur `asyncio.Queue` use karo.

| Feature         | Threading                                    | Multiprocessing            | Asyncio                       |
| --------------- | -------------------------------------------- | -------------------------- | ----------------------------- |
| Execution unit  | Thread                                       | Process                    | Coroutine/task                |
| I/O-bound       | Bohat useful                                 | Possible, lekin overhead   | Bohat useful                  |
| CPU parallelism | GIL-enabled CPython mein aam tor par limited | Haan, multiple processes   | Khud se CPU parallelism nahi  |
| Memory          | Process ke andar shared                      | Aam tor par separate       | Aik event loop mein shared    |
| Complexity      | Synchronization                              | IPC aur process management | Async-compatible code zaroori |

## 15. Advanced concepts jo professional level par aane chahiye

In topics ko bhi master karna zaroori hai:

1. Thread safety: shared data ko concurrent modification se protect karna.
2. Race conditions: execution order ki wajah se incorrect results.
3. Deadlocks: threads ka aik doosray ke resources ka intezar karte rehna.
4. Starvation: kisi task ko resources ya execution ka mauqa na milna.
5. Backpressure: producer ki speed ko consumer ki capacity ke mutabiq manage karna.
6. Bounded queues: memory ko unlimited tasks se bharne se bachana.
7. Cancellation aur timeouts: slow ya unnecessary operations ko control karna.
8. Exception propagation: worker tasks ke failures ko main program tak pohanchana.
9. Graceful shutdown: workers ko safely stop karna aur pending work complete karna.
10. Testing aur benchmarking: actual performance aur concurrency bugs verify karna.
11. Context propagation: tracing IDs aur request metadata ko tasks tak pohanchana.
12. Distributed concurrency: multiple machines par tasks coordinate karna, jaise message queues aur distributed workers ke zariye.

## 16. Apni understanding test karo

1\. Concurrency aur parallelism mein bunyadi farq kya hai?

Dono bilkul aik cheez hain

Concurrency task coordination hai; parallelism simultaneous execution hai

Concurrency sirf CPU calculations ke liye hai

2\. Teen independent I/O tasks mein har task 2 seconds wait karta hai. Concurrent execution ka expected time kya hai?

6 seconds

2 seconds ke qareeb

0 seconds

3\. Shared counter ko multiple threads se safely update karne ke liye kya use kar sakte hain?

threading.Lock

time.sleep only

print()

4\. Heavy CPU-bound Python computation ke liye GIL-enabled CPython mein kya aksar suitable hai?

Har jagah asyncio.sleep()

ProcessPoolExecutor

Sirf sequential threads

Quiz reset karo

## 17. Recommended learning roadmap

1. Foundation: sequential execution, `time.sleep()`, concurrency vs parallelism.
2. Threading: `Thread`, `join()`, `Lock`, `RLock`, `Semaphore`, `Event`.
3. Thread pools: `ThreadPoolExecutor`, `Future`, `submit()`, `map()`, `as_completed()`.
4. Multiprocessing: `Process`, process pools, IPC, pickling aur shared memory.
5. Asyncio: coroutines, `await`, `gather()`, tasks, queues, timeouts aur cancellation.
6. Production: bounded concurrency, retries, error handling, logging, graceful shutdown aur testing.
7. Projects: concurrent file downloader, API fetcher, producer-consumer system aur CPU-intensive parallel processor.

Meri recommendation: Pehle `threading` aur `ThreadPoolExecutor` ko practical examples ke saath master karo. Uske baad `asyncio` aur phir `multiprocessing` seekho. Is order se aapko har approach ka purpose aur trade-off clearly samajh aayega.