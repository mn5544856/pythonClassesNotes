# Python Async — Basic se Advanced tak (Roman Urdu)

Python mein `async` seekhne ke liye hum bilkul zero se start karenge, phir real-world projects, error handling, concurrency, `asyncio`, APIs aur advanced concepts tak jayenge.

Sab se pehle ek baat samjho: Async Python ka woh tareeqa hai jis mein program kisi operation ke complete hone ka wait karte hue doosra kaam bhi kar sakta hai.

Misal ke taur par, tumhara program 10 websites se data download kar raha hai. Normal code mein har website ka response aane ka wait ho sakta hai. Async mein program ek website ka wait karte hue doosri website ka kaam shuru kar sakta hai.

## 1. Synchronous vs Asynchronous

### Synchronous (normal Python)

Task 1 — 3 seconds

Task 2 — 3 seconds

Task 3 — 3 seconds

Total: taqreeban 9 seconds

### Asynchronous (async Python)

Task 1, 2 aur 3 overlap kar sakte hain

Agar teeno tasks 3-second ke wait operations hon, to total taqreeban 3 seconds ho sakta hai.

Yeh timing tab possible hai jab tasks ek doosre ka result aane se pehle independently start ho sakte hon aur unka wait asynchronous ho. Async har tarah ke code ko automatically fast nahi banata.

## 2. Async kin cheezon ke liye useful hai?

- API se data lena
- Web scraping
- Multiple network requests
- Database queries, agar driver async support karta ho
- Web servers aur chat applications
- Multiple files ya services ke I/O operations
- Aise programs jin mein bohat saara waiting time hota hai

Important: Async aur parallel processing ek cheez nahi hain. Async aam tor par ek thread mein multiple tasks ko bari bari CPU ka waqt deta hai, jabke multiprocessing multiple processes ke zariye CPU-intensive kaam parallel kar sakti hai.

## 3. Sab se pehla concept: `async def`

Normal Python function:

```
def greet():    print("Assalam-o-Alaikum")greet()
```

Output:

```
Assalam-o-Alaikum
```

Ab async function dekho:

```
async def greet():    print("Assalam-o-Alaikum")greet()
```

Is baar function ka body aam function ki tarah execute nahi hoga. `greet()` ek coroutine object return karega.

Yani `async def` likhne se function coroutine function ban jata hai. Usay execute karne ke liye humein aam tor par `await` aur event loop chahiye.

### Async function ko sahi tarah chalana

```
import asyncioasync def greet():    print("Assalam-o-Alaikum")asyncio.run(greet())
```

Output:

```
Assalam-o-Alaikum
```

Yahan:

- `async def` — coroutine function banata hai.
- `greet()` — coroutine object banata hai.
- `asyncio.run()` — event loop ke zariye coroutine ko chalata hai.
- `import asyncio` — Python ki asynchronous programming library import karta hai.

`asyncio.run()` aam tor par program ke top level par use hota hai. Agar tum pehle se kisi running event loop ke andar ho, jaise kisi async web framework mein, to wahan dobara `asyncio.run()` nahi chalana chahiye.

## 4. `await` kya hota hai?

`await` async programming ka sab se important concept hai.

Jab koi coroutine kisi doosre asynchronous operation ka wait karna chahti hai, to hum `await` use karte hain.

```
import asyncioasync def get_data():    print("Data lena shuru")    await asyncio.sleep(2)    print("Data mil gaya")asyncio.run(get_data())
```

Output:

```
Data lena shuru
Data mil gaya
```

Is program mein `asyncio.sleep(2)` do seconds ka asynchronous wait karta hai.

### `time.sleep()` aur `asyncio.sleep()` ka farq

```
import timeimport asyncioasync def example():    time.sleep(2)          # Blocking wait    await asyncio.sleep(2) # Non-blocking waitasyncio.run(example())
```

Is code mein pehle `time.sleep(2)` event loop ko block karega. Is liye async code ke andar aam tor par `asyncio.sleep()` use karna behtar hai.

| Function                 | Kya karta hai?                                                                 |
| ------------------------ | ------------------------------------------------------------------------------ |
| `time.sleep(2)`          | Current thread ko block karta hai                                              |
| `await asyncio.sleep(2)` | Wait ke dauran doosre async tasks ko chalne ka mauqa deta hai                  |
| `await some_coroutine()` | Coroutine ke result ka wait karta hai aur zaroorat par control chhor sakta hai |

Yaad rakho: `await` har function ke saath nahi lagaya ja sakta. Aam tor par awaitable object, jaise coroutine ya `asyncio.Task`, ke saath use hota hai.

## 5. Sequential async code vs concurrent async code

Yahan se async ki asal power samajh aati hai.

### Example A — Ek ke baad ek task

```
import asyncioasync def task(name, seconds):    print(f"{name} shuru")    await asyncio.sleep(seconds)    print(f"{name} complete")async def main():    await task("Task 1", 2)    await task("Task 2", 2)    await task("Task 3", 2)asyncio.run(main())
```

Taqreeban 6 seconds lagenge, kyun ke doosra task pehle ke complete hone ke baad start hota hai.

### Example B — Teeno tasks concurrent chalana

```
import asyncioasync def task(name, seconds):    print(f"{name} shuru")    await asyncio.sleep(seconds)    print(f"{name} complete")async def main():    await asyncio.gather(        task("Task 1", 2),        task("Task 2", 2),        task("Task 3", 2),    )asyncio.run(main())
```

Is baar taqreeban 2 seconds lagenge, kyun ke teeno tasks ka waiting time overlap karta hai.

### Execution timeline

Sequential — total lagbhag 6 seconds

Task 1

Task 2

Task 3

Concurrent — total lagbhag 2 seconds

Task 1

Task 2

Task 3

`asyncio.gather()` multiple awaitables ko schedule karke unke results ka wait karne ka ek convenient tareeqa hai. Results aam tor par input order mein milte hain, completion order mein zaroori nahi.

## 6. Coroutine, Task aur Future mein farq

Yeh teen concepts professional async code mein bohat important hain.

### Coroutine

`async def` se define hoti hai. Isay call karne par coroutine object milta hai.

```
async def fetch():    return "data"coro = fetch()
```

Sirf `fetch()` call karne se body execute nahi hota.

### Task

Event loop ko coroutine schedule karne ke liye use hota hai.

```
task = asyncio.create_task(fetch())result = await task
```

`create_task()` ko running event loop ke andar call karna chahiye.

### Future

Ek low-level awaitable object jo future result ya exception represent karta hai. Aksar `asyncio` ki internal machinery aur callback-based integrations mein use hota hai.

### `asyncio.create_task()` ka example

```
import asyncioasync def download():    print("Download start")    await asyncio.sleep(2)    print("Download complete")    return "File ready"async def main():    task = asyncio.create_task(download())    print("Doosra kaam kar raha hoon")    result = await task    print(result)asyncio.run(main())
```

Is example mein `download()` task ke taur par schedule hota hai. Event loop ko doosra kaam karne ka mauqa milta hai jab download coroutine wait kar rahi hoti hai.

Important: Task create karne ka matlab yeh nahi ke CPU par code lazmi ek hi waqt mein execute hoga. Normal `asyncio` tasks cooperative scheduling use karte hain.

## 7. `asyncio.gather()` vs `asyncio.TaskGroup`

Modern Python mein structured concurrency ke liye `asyncio.TaskGroup` bhi seekhna zaroori hai. Yeh Python 3.11 aur uske baad ke versions mein available hai.

### `gather()` ka example

```
import asyncioasync def get_user():    await asyncio.sleep(1)    return "Nouman"async def get_orders():    await asyncio.sleep(1)    return ["Order 1", "Order 2"]async def main():    user, orders = await asyncio.gather(        get_user(),        get_orders()    )    print(user)    print(orders)asyncio.run(main())
```

### `TaskGroup` ka example

```
import asyncioasync def get_user():    await asyncio.sleep(1)    return "Nouman"async def get_orders():    await asyncio.sleep(1)    return ["Order 1", "Order 2"]async def main():    async with asyncio.TaskGroup() as group:        user_task = group.create_task(get_user())        orders_task = group.create_task(get_orders())    print(user_task.result())    print(orders_task.result())asyncio.run(main())
```

`TaskGroup` ka faida yeh hai ke child tasks ka lifecycle ek scope ke andar manage hota hai. Agar koi task fail ho, to group aam tor par baqi tasks ko cancel karta hai aur exception ko structured tareeqe se report karta hai.

`gather()` bhi useful hai, lekin failure aur cancellation ka behavior dono approaches mein ek jaisa nahi hai.

## 8. Async mein exception handling

Async functions mein bhi normal Python ki tarah `try`, `except`, `else` aur `finally` use hote hain.

```
import asyncioasync def fetch_data():    await asyncio.sleep(1)    raise ValueError("Data invalid hai")async def main():    try:        await fetch_data()    except ValueError as error:        print(f"Error: {error}")    finally:        print("Operation finish ho gaya")asyncio.run(main())
```

Output:

```
Error: Data invalid hai
Operation finish ho gaya
```

### Task ke andar exception handle karna

```
import asyncioasync def worker():    await asyncio.sleep(1)    raise RuntimeError("Worker fail ho gaya")async def main():    task = asyncio.create_task(worker())    try:        await task    except RuntimeError as error:        print(f"Task error: {error}")asyncio.run(main())
```

Agar task ka exception retrieve ya handle na kiya jaye, to unhandled task exception ki warnings ya debugging problems paida ho sakti hain.

### Cancellation ko samjho

```
import asyncioasync def worker():    try:        while True:            print("Kaam chal raha hai")            await asyncio.sleep(1)    except asyncio.CancelledError:        print("Task cancel ho raha hai")        raiseasync def main():    task = asyncio.create_task(worker())    await asyncio.sleep(2.5)    task.cancel()    try:        await task    except asyncio.CancelledError:        print("Cancellation confirm")asyncio.run(main())
```

`CancelledError` ko aam tor par cleanup ke liye handle karo aur phir re-raise karo. Isay chup chaap ignore karna task cancellation ke expected behavior ko kharab kar sakta hai.

## 9. `asyncio.wait_for()` aur timeout

Real-world applications mein API ya database hamesha waqt par response nahi dete. Is liye timeout lagana important hai.

```
import asyncioasync def slow_api():    await asyncio.sleep(5)    return "API response"async def main():    try:        result = await asyncio.wait_for(            slow_api(),            timeout=2        )        print(result)    except TimeoutError:        print("API timeout ho gayi")asyncio.run(main())
```

Yahan operation 5 seconds leta, lekin humne maximum 2 seconds ka timeout diya. Is liye `TimeoutError` handle hoga.

Python 3.11+ mein `asyncio.timeout()` context manager bhi available hai:

```
async def main():    try:        async with asyncio.timeout(2):            result = await slow_api()            print(result)    except TimeoutError:        print("Time limit khatam")
```

Timeout cancellation ke zariye operation ko rokne ki koshish karta hai. Lekin agar operation cancellation ko sahi handle nahi karta, to real-world behavior ko samajhna zaroori hai.

## 10. `asyncio.Semaphore` — concurrency limit karna

Socho tumhein 1,000 URLs se data lena hai. Agar saare 1,000 requests ek hi waqt mein bhej do, to server, network ya API rate limit ka masla aa sakta hai.

Semaphore ek waqt mein active operations ki tadaad limit karta hai.

```
import asyncioasync def fetch(url, semaphore):    async with semaphore:        print(f"Request start: {url}")        await asyncio.sleep(1)        print(f"Request complete: {url}")        return f"Data from {url}"async def main():    semaphore = asyncio.Semaphore(3)    urls = [f"https://example.com/{i}" for i in range(10)]    results = await asyncio.gather(        *(fetch(url, semaphore) for url in urls)    )    print(f"Total results: {len(results)}")asyncio.run(main())
```

Is program mein maximum 3 operations ek waqt mein semaphore ke andar kaam kar sakte hain.

- `asyncio.Semaphore(3)` — limit 3.
- `async with semaphore` — slot acquire aur release automatically.
- `asyncio.gather()` — saare requests ko schedule karta hai.
- `results` — tamam successful results input order mein rakhta hai.

Professional tip: Agar tumhare paas bohat bari input list hai, to hazaron tasks ek saath create karne ke bajaye `asyncio.Queue` aur limited worker tasks use karna zyada scalable ho sakta hai.

## 11. `asyncio.Queue` aur worker pattern

Yeh producer-consumer pattern hai. Producer queue mein jobs daalta hai aur workers un jobs ko process karte hain.

```
import asyncioasync def worker(queue, worker_id):    while True:        item = await queue.get()        try:            if item is None:                return            print(f"Worker {worker_id}: {item}")            await asyncio.sleep(1)        finally:            queue.task_done()async def main():    queue = asyncio.Queue(maxsize=5)    workers = [        asyncio.create_task(worker(queue, i))        for i in range(3)    ]    for item in range(10):        await queue.put(item)    await queue.join()    for _ in workers:        await queue.put(None)    await asyncio.gather(*workers)asyncio.run(main())
```

Is example mein:

- Queue mein maximum 5 pending items buffer ho sakte hain.
- 3 workers jobs process karte hain.
- `queue.get()` next job ka wait karta hai.
- `queue.task_done()` har retrieved item ki processing ko acknowledge karta hai.
- `queue.join()` tamam queued jobs ki completion ka wait karta hai.
- `None` workers ko shutdown karne ka signal hai.

Agar worker ke andar exception aaye, to production implementation mein failed jobs, retries aur graceful shutdown ka plan bhi banana chahiye.

## 12. Async context manager aur async iterator

Advanced async programming mein tumhein `async with` aur `async for` bhi milenge.

### `async with`

Aise resources ke liye use hota hai jinhein asynchronously open ya close karna ho, jaise kuch database connections aur HTTP sessions.

Conceptual example:

```
async with async_resource() as resource:    result = await resource.read()
```

Yeh sirf syntax ka example hai; `async_resource()` ko kisi actual async context manager se replace karna hoga.

### `async for`

Asynchronous iterator se items ek ek karke retrieve karta hai.

```
import asyncioasync def numbers():    for number in range(3):        await asyncio.sleep(1)        yield numberasync def main():    async for number in numbers():        print(number)asyncio.run(main())
```

Output:

```
0
1
2
```

`async def` ke andar `yield` use karne se asynchronous generator banta hai. Har item ke darmiyan async operation ho sakta hai.

## 13. Async file handling

Normal Python mein file access aam tor par synchronous hota hai:

```
with open("data.txt", encoding="utf-8") as file:    content = file.read()
```

Yeh file operation event loop ko block kar sakta hai, khaas taur par agar operation slow ho.

Agar tumhari application ko event loop responsive rakhna hai, to `asyncio.to_thread()` ke zariye blocking file operation ko alag thread mein chala sakte ho:

```
import asynciofrom pathlib import Pathdef read_file():    return Path("data.txt").read_text(encoding="utf-8")async def main():    content = await asyncio.to_thread(read_file)    print(content)asyncio.run(main())
```

`asyncio.to_thread()` Python 3.9+ mein available hai.

Yeh yaad rakho ke `pathlib.Path` khud async API nahi deta. `aiofiles` jaisi third-party library bhi istemal ki ja sakti hai. Chhoti local file ke liye async library hamesha zaroori nahi hoti; decision workload par depend karta hai.

## 14. Async HTTP requests — real-world example

APIs se data lena async ka common use case hai. Is ke liye `aiohttp` ya `httpx` ka async client use kar sakte ho.

Install:

```
pip install aiohttp
```

Example:

```
import asyncioimport aiohttpasync def fetch_json(session, url):    async with session.get(url) as response:        response.raise_for_status()        return await response.json()async def main():    urls = [        "https://jsonplaceholder.typicode.com/users/1",        "https://jsonplaceholder.typicode.com/users/2",        "https://jsonplaceholder.typicode.com/users/3",    ]    timeout = aiohttp.ClientTimeout(total=10)    async with aiohttp.ClientSession(timeout=timeout) as session:        results = await asyncio.gather(            *(fetch_json(session, url) for url in urls)        )    for result in results:        print(result["name"])asyncio.run(main())
```

Yeh example:

1. Ek shared HTTP session banata hai.
2. Teen API requests concurrent chalata hai.
3. Har response ka status check karta hai.
4. JSON data parse karta hai.
5. Session ko automatically close karta hai.

Is code ko chalane ke liye internet connection aur `aiohttp` installed hona chahiye. Production code mein network errors, timeouts, retries, rate limits aur failed individual requests ko bhi handle karna zaroori hai.

## 15. Async aur CPU-intensive tasks

Async ka matlab yeh nahi ke har calculation fast ho jayegi.

Misal:

```
async def calculate():    total = sum(i * i for i in range(10_000_000))    return total
```

Is function mein koi `await` nahi hai. Jab calculation chal rahi hogi, event loop doosre tasks ko run nahi kar sakta.

CPU-intensive work ke liye:

- `ProcessPoolExecutor` ya `multiprocessing` consider karo.
- Blocking I/O ke liye `asyncio.to_thread()` consider karo.
- Network I/O ke liye native async libraries use karo.

Sahi approach workload aur library support par depend karti hai.

## 16. Advanced async: common mistakes

| Mistake                                       | Behtar approach                                   |
| --------------------------------------------- | ------------------------------------------------- |
| `async def` ko call karke chhor dena          | `await` ya task scheduling use karo               |
| Async code mein `time.sleep()`                | `await asyncio.sleep()`                           |
| Har operation ke liye unlimited tasks         | Semaphore ya bounded worker queue                 |
| Task errors ignore karna                      | Exceptions ko retrieve aur handle karo            |
| Har jagah `asyncio.run()` call karna          | Ek suitable application entry point rakho         |
| CPU-heavy calculation event loop mein karna   | Process pool ya suitable thread strategy          |
| Cancellation ko ignore karna                  | Cleanup karo aur cancellation ko preserve karo    |
| HTTP client har request ke liye dobara banana | Jahan suitable ho, shared session/client use karo |

## 17. Practice: apni async knowledge test karo

Neeche interactive quiz hai. Har sawal ka jawab select karo aur check karo ke concept samajh aaya ya nahi.

1\. \`async def\` function ko call karne par aam tor par kya milta hai?

Integer

Coroutine object

Thread

2\. Async wait ke liye kaunsa function sahi hai?

time.sleep(2)

await asyncio.sleep(2)

asyncio.stop(2)

3\. Teen independent 2-second async waits ko concurrent chalane ka kya faida hai?

Har wait 0 seconds ka ho jata hai

Total wait taqreeban 2 seconds ho sakta hai

CPU automatically 3 guna fast hota hai

4\. Ek waqt mein maximum 5 requests chalani hon to kya use kar sakte hain?

asyncio.Semaphore(5)

time.sleep(5)

asyncio.Future(5)

5\. CPU-intensive Python calculation ke liye aam tor par kya consider karna chahiye?

Har jagah await likhna

Process pool

asyncio.sleep(0) ko repeat karna

Answers check karo

## 18. Basic se professional mastery tak roadmap

Level 1

Async foundations

Synchronous vs async, coroutine, async def, await, asyncio.run

Level 2

Concurrency

create_task, gather, TaskGroup, as_completed, wait

Level 3

Reliability

Exception handling, cancellation, timeouts, retries, cleanup

Level 4

Resource management

Semaphore, Lock, Event, Queue, bounded workers

Level 5

Real-world I/O

Async HTTP clients, database drivers, async generators, async context managers

Level 6

Production mastery

Testing, logging, structured concurrency, performance profiling, thread/process integration

Meri recommendation: pehle `async def`, `await`, `asyncio.sleep()`, `create_task()` aur `gather()` ko practical code ke saath master karo. Uske baad exceptions, cancellation, timeouts aur semaphore par jao. Phir ek Async API Data Fetcher Project banao jo multiple APIs se data le, concurrency limit kare, timeouts handle kare, logging kare aur unit tests pass kare.

Yeh sequence tumhein sirf syntax nahi, balkay real-world asynchronous Python applications develop karna sikhayega.