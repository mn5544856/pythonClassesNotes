 # Python Logging — Basic se Advanced tak (Roman Urdu)

Python mein logging ka concept samajhne ke liye sab se pehle yeh samjho: jab tum koi Python program banate ho, to tumhein pata hona chahiye ke program ke andar kya ho raha hai, kahan error aaya, kis function ne kaam kiya aur program fail kyun hua.

Logging tumhein yeh sab information record karne mein help karti hai.

## 1. Logging kya hoti hai?

Maan lo tum ek login system bana rahe ho. Jab user login karta hai, tumhein pata karna hai:

- Login successful hua ya nahi.
- User ne ghalat password enter kiya ya nahi.
- Database connection fail hua ya nahi.
- Program kis waqt error ki wajah se crash hua.

In events ko record karna logging kehlata hai.

Python mein logging ke liye built-in `logging` module hota hai. Isay install karne ki zaroorat nahi.

### Logging vs print()

```
print("User logged in")
```

Yeh sirf message display karta hai.

```
import logginglogging.warning("Login attempt failed")
```

Yeh message ko uski severity ke saath record karta hai. Logging ko configure karke messages file mein bhi save kar sakte ho, aur unke saath timestamp, module ka naam aur doosri useful information bhi rakh sakte ho.

Yaad rakho: `print()` debugging ke liye useful hai, lekin logging real-world applications mein monitoring aur troubleshooting ke liye zyada powerful hai.

## 2. Logging ka sab se basic example

```
import logginglogging.basicConfig(level=logging.DEBUG)logging.debug("Yeh debugging information hai")logging.info("Program successfully start hua")logging.warning("Kuch unusual ho raha hai")logging.error("Operation fail ho gaya")logging.critical("Bohat serious problem hai")
```

Is code mein:

- `import logging` — logging module import karta hai.
- `basicConfig()` — logging ki basic settings configure karta hai.
- `level=logging.DEBUG` — DEBUG aur us se zyada severity wale messages allow karta hai.
- `logging.info()` waghera — mukhtalif levels ke messages generate karte hain.

Output kuch is tarah hoga:

```
DEBUG:root:Yeh debugging information hai
INFO:root:Program successfully start hua
WARNING:root:Kuch unusual ho raha hai
ERROR:root:Operation fail ho gaya
CRITICAL:root:Bohat serious problem hai
```

`root` default logger ka naam hai. Abhi timestamp nahi aa raha, kyun ke humne uska format configure nahi kiya.

## 3. Logging ke 5 levels — bohat important concept

1\. DEBUG

Level: 10

Program ki detailed internal information. Misal: function ko kya input mila, calculation ka result kya tha.

2\. INFO

Level: 20

Normal events. Misal: application start hui, user login hua, file successfully read hui.

3\. WARNING

Level: 30

Koi unusual situation hai, lekin program abhi kaam kar raha hai. Misal: disk space kam ho rahi hai.

4\. ERROR

Level: 40

Koi operation fail ho gaya. Misal: report generate nahi hui.

5\. CRITICAL

Level: 50

Bohat serious failure. Misal: application ka core system kaam nahi kar raha.

In levels ki numerical values bhi important hain, kyun ke Python inhi ki madad se decide karta hai ke kaun se messages show karne hain.

Golden rule: Agar `level=logging.WARNING` set hai, to WARNING, ERROR aur CRITICAL show honge. DEBUG aur INFO nahi.

Iski wajah yeh hai ke logging level ek minimum threshold hota hai.

## 4. `basicConfig()` ko deeply samjho

`basicConfig()` logging ki initial configuration set karta hai.

```
import logginglogging.basicConfig(    level=logging.DEBUG,    format="%(asctime)s - %(levelname)s - %(message)s",    datefmt="%Y-%m-%d %H:%M:%S")logging.info("Application start ho gayi")logging.error("Database connection fail ho gaya")
```

Possible output:

```
2026-10-12 20:10:00 - INFO - Application start ho gayi
2026-10-12 20:10:01 - ERROR - Database connection fail ho gaya
```

Har setting ka concept:

| Setting    | Kaam                                                   |
| ---------- | ------------------------------------------------------ |
| `level`    | Minimum severity set karta hai                         |
| `format`   | Log message ka structure set karta hai                 |
| `datefmt`  | Timestamp ka format set karta hai                      |
| `filename` | Logs ko file mein likhne ke liye file select karta hai |
| `filemode` | File write ya append mode mein kholni hai              |

### Common format placeholders

- `%(asctime)s` — date aur time
- `%(levelname)s` — INFO, ERROR, WARNING waghera
- `%(message)s` — actual log message
- `%(name)s` — logger ka naam
- `%(filename)s` — source file ka naam
- `%(funcName)s` — function ka naam
- `%(lineno)d` — code ki line number
- `%(process)d` — process ID
- `%(thread)d` — thread ID

Example:

```
import logginglogging.basicConfig(    level=logging.DEBUG,    format="%(asctime)s | %(name)s | "           "%(levelname)s | %(filename)s:%(lineno)d | %(message)s")def calculate():    logging.info("Calculation start hui")    result = 10 + 20    logging.debug("Result = %s", result)calculate()
```

Yahan `%(filename)s:%(lineno)d` se tumhein log generate karne wali file aur line ka pata chalega.

Important: `basicConfig()` aam tor par sirf tab configuration karta hai jab root logger ke paas pehle se handlers na hon. Is liye ise application ke start mein configure karo. Jupyter Notebook ya kisi pehle se configured environment mein `force=True` existing root handlers ko replace kar sakta hai; ise soch samajh kar use karo.

## 5. Logging ko file mein save karna

Real applications mein logs sirf terminal par dikhana kaafi nahi hota. Program band hone ke baad bhi logs chahiye hote hain.

```
import logginglogging.basicConfig(    filename="app.log",    level=logging.DEBUG,    format="%(asctime)s | %(levelname)s | %(message)s",    encoding="utf-8)logging.info("Application start hui")logging.warning("Storage space kam hai")logging.error("Payment process fail hua")
```

Ab logs `app.log` file mein likhe jayenge.

Ek chhoti correction: code mein `encoding` wali string ko close karna zaroori hai. Sahi configuration yeh hai:

```
import logginglogging.basicConfig(    filename="app.log",    level=logging.DEBUG,    format="%(asctime)s | %(levelname)s | %(message)s",    encoding="utf-8")logging.info("Application start hui")logging.warning("Storage space kam hai")logging.error("Payment process fail hua")
```

### `filemode="w"` aur `filemode="a"` mein farq

```
logging.basicConfig(    filename="app.log",    filemode="a",    level=logging.INFO)
```

- `"a"` — purane logs ke end mein naye logs add hote hain. Yeh default mode hai.
- `"w"` — file dobara open hone par purana content overwrite ho sakta hai.

Production tip: Aksar `"a"` ya rotating log files use ki jati hain, taake har application restart par purane logs delete na hon.

## 6. Logger kya hota hai? — sab se important architecture

Abhi tak hum yeh use kar rahe thay:

```
logging.info("Application start hui")
```

Lekin large project mein multiple modules ho sakte hain:

```
my_project/
├── main.py
├── auth.py
├── database.py
└── payment.py
```

Agar har module ek hi root logger use kare, to logs ka source samajhna mushkil ho sakta hai.

Is liye named logger banaya jata hai.

```
import logginglogger = logging.getLogger(__name__)logger.info("User login attempt")
```

`__name__` current Python module ka naam deta hai. Agar file `auth.py` ke taur par import ho rahi hai, to logger ka naam aam tor par `auth` hoga.

Iska faida: log dekh kar pata chal sakta hai ke message kis module se aaya.

### Logger aur Handler mein farq

Is concept ko ek simple flow se samjho:

Application code

`logger.error("Payment failed")`

Logger

Message aur severity ko process karta hai

Handler

Decide karta hai log kahan bhejna hai

StreamHandler

Terminal / console

FileHandler

Log file

Logger message generate karta hai. Handler us message ko kisi destination tak pahunchata hai. Formatter message ka appearance set karta hai.

Ek logger ke saath multiple handlers bhi ho sakte hain, jaise WARNING aur ERROR terminal par aur tamam INFO-level messages file mein.

## 7. Logger + multiple handlers ka practical example

```
import logginglogger = logging.getLogger("my_app")logger.setLevel(logging.DEBUG)# Terminal handlerconsole = logging.StreamHandler()console.setLevel(logging.WARNING)# File handlerfile_handler = logging.FileHandler(    "app.log",    encoding="utf-8")file_handler.setLevel(logging.DEBUG)# Formatformatter = logging.Formatter(    "%(asctime)s | %(name)s | %(levelname)s | %(message)s")console.setFormatter(formatter)file_handler.setFormatter(formatter)logger.addHandler(console)logger.addHandler(file_handler)logger.debug("Debug information")logger.info("Application start hui")logger.warning("Unusual activity")logger.error("Payment fail hua")
```

Is example mein:

- Logger DEBUG level tak messages accept karta hai.
- Console handler sirf WARNING aur us se upar ke messages emit karta hai.
- File handler DEBUG aur us se upar ke messages file mein likhta hai.

Is liye DEBUG aur INFO file mein jayenge, jabke WARNING aur ERROR dono destinations par jayenge.

Advanced gotcha: Agar tum is code ko baar baar execute karte ho, to duplicate handlers add ho sakte hain aur messages multiple times print ho sakte hain. Production code mein handlers ko centrally configure karo, ya handlers add karne se pehle duplication ko handle karo. Named logger par `propagate` bhi relevant hai: agar parent/root logger par bhi matching handler laga ho, to message dobara emit ho sakta hai.

## 8. Exception logging — errors ko properly record karna

Yeh real-world Python development ka bohat important part hai.

Maan lo tum division kar rahe ho aur denominator zero aa jata hai.

```
result = 10 / 0
```

Python `ZeroDivisionError` raise karega. Agar tum sirf error message log karte ho, to exact traceback nahi milega.

### Ghalat approach

```
import loggingtry:    result = 10 / 0except ZeroDivisionError:    logging.error("Calculation fail hui")
```

Is se error ka message record hota hai, lekin traceback nahi.

### Behtar approach: `logging.exception()`

```
import logginglogging.basicConfig(    level=logging.DEBUG,    format="%(asctime)s | %(levelname)s | %(message)s")try:    result = 10 / 0except ZeroDivisionError:    logging.exception("Calculation fail hui")
```

`logging.exception()` ERROR level par message log karta hai aur current exception ka traceback bhi include karta hai. Isay exception handler ke andar use karna chahiye.

Output ka concept:

```
ERROR | Calculation fail hui
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```

Traceback se pata chalta hai ke error kis line aur kis function mein hua.

Doosra option:

```
try:    result = 10 / 0except ZeroDivisionError:    logging.error("Calculation fail hui", exc_info=True)
```

Yeh bhi current exception ka traceback include karta hai.

### `logger.exception()` vs `logger.error()`

| Method                             | Kya record karta hai?                       |
| ---------------------------------- | ------------------------------------------- |
| `logger.debug()`                   | Detailed diagnostic messages                |
| `logger.error()`                   | Error message                               |
| `logger.error(..., exc_info=True)` | Error message + current exception traceback |
| `logger.exception()`               | ERROR message + current exception traceback |

Aam tor par exception handler ke andar `logger.exception()` sab se readable choice hoti hai.

Important: Exception ko log karke chupana hamesha sahi nahi. Agar error recover nahi ho sakta, to usay re-raise karna ya application ko munasib tareeqe se fail karna bhi zaroori ho sakta hai.

## 9. `RotatingFileHandler` — jab log file bohat bari ho jaye

Socho tumhari application har second 100 log messages likh rahi hai. Kuch din baad `app.log` bohat bari ho jayegi.

Is problem ko solve karne ke liye log rotation use hoti hai.

```
import loggingfrom logging.handlers import RotatingFileHandlerlogger = logging.getLogger("server")logger.setLevel(logging.INFO)handler = RotatingFileHandler(    "server.log",    maxBytes=1_000_000,    backupCount=3,    encoding="utf-8")handler.setFormatter(    logging.Formatter(        "%(asctime)s | %(levelname)s | %(message)s"    ))logger.addHandler(handler)logger.info("Server start ho gaya")
```

Is configuration ka matlab:

- `maxBytes=1_000_000` — file ka target maximum size takreeban 1 MB hai.
- `backupCount=3` — teen purani rotated files rakhi ja sakti hain.
- Jab current file limit tak pohanchti hai, to purani file rotate hoti hai aur nayi log file shuru hoti hai.

Files kuch is tarah nazar aa sakti hain:

```
server.log
server.log.1
server.log.2
server.log.3
```

Yeh size-based rotation hai.

### `TimedRotatingFileHandler`

Agar tum file ko size ke bajaye time ke mutabiq rotate karna chahte ho:

```
from logging.handlers import TimedRotatingFileHandlerhandler = TimedRotatingFileHandler(    "daily.log",    when="midnight",    interval=1,    backupCount=7,    encoding="utf-8")
```

Iska maqsad daily rotation aur limited historical files rakhna hai. Production mein timezone aur rotation ke waqt ka khayal rakhna chahiye.

## 10. Logging ki hierarchy aur `propagate`

Python logging mein loggers hierarchical hote hain.

Misal:

```
root
 └── my_app
      ├── my_app.auth
      ├── my_app.database
      └── my_app.payment
```

Agar tum likho:

```
logger = logging.getLogger("my_app.database")
```

To yeh logger apne parent `my_app` aur phir root ki taraf hierarchy mein aata hai.

Default taur par `propagate=True` hota hai, is liye message parent loggers ke handlers tak bhi ja sakta hai.

### Iska faida

Tum root ya application-level logger par ek handler configure kar sakte ho aur tamam modules ke logs central destination par collect kar sakte ho.

### Duplicate logs kyun aate hain?

Maan lo:

- Child logger ke paas console handler hai.
- Root logger ke paas bhi console handler hai.
- Child logger ka `propagate=True` hai.

Ek hi record child handler aur root handler dono se emit ho sakta hai.

Solution configuration par depend karta hai: ya sirf parent handlers use karo, ya child logger par `propagate=False` set karo jab uske apne handlers hon.

```
logger = logging.getLogger("my_app.payment")logger.propagate = False
```

Yeh setting tab useful hai jab tum jaan boojh kar child logger ke logs ko parent tak nahi bhejna chahte.

## 11. `logging.config.dictConfig()` — professional configuration

Jab application chhoti hoti hai, `basicConfig()` kaafi hota hai. Bari application mein loggers, handlers aur formatters ko ek jagah configure karna zyada manageable hota hai.

Python ka `logging.config` module `dictConfig()` provide karta hai.

```
import loggingimport logging.configLOGGING_CONFIG = {    "version": 1,    "disable_existing_loggers": False,    "formatters": {        "standard": {            "format": (                "%(asctime)s | %(name)s | "                "%(levelname)s | %(message)s"            )        }    },    "handlers": {        "console": {            "class": "logging.StreamHandler",            "level": "INFO",            "formatter": "standard",        },        "file": {            "class": "logging.FileHandler",            "level": "DEBUG",            "filename": "app.log",            "encoding": "utf-8",            "formatter": "standard",        },    },    "root": {        "level": "DEBUG",        "handlers": ["console", "file"],    },
```

Is configuration mein:

- `formatters` message ka format define karta hai.
- `handlers` output destinations define karte hain.
- `root` default logger ki configuration rakhta hai.
- `disable_existing_loggers=False` existing named loggers ko automatically disable karne se bachata hai.

Yeh configuration dictionaries ke zariye logging ko organize karti hai. Bari applications mein isi tarah ki configuration ko separate Python module ya trusted configuration file mein rakhna asaan hota hai.

Security note: Agar configuration file mein Python object construction ya custom handlers involve hon, to untrusted configuration ko load mat karo. Logging configuration bhi application security ka hissa hai.

## 12. Logging mein performance — advanced concept

Agar tum bohat zyada logs generate kar rahe ho, to unnecessary string formatting performance ko affect kar sakti hai.

### Preferred approach

```
logger.debug("User ID: %s", user_id)
```

Is approach mein logging module formatting ko tab karta hai jab record process hota hai.

### Alternative

```
logger.debug(f"User ID: {user_id}")
```

F-string foran evaluate hoti hai, chahe DEBUG message filter ho kar output mein na bhi aaye.

Agar message simple hai, to dono readable hain. Lekin high-volume logging mein parameterized logging behtar habit hai.

Aur agar calculation expensive hai:

```
if logger.isEnabledFor(logging.DEBUG):    logger.debug("Detailed result: %s", expensive_calculation())
```

Yahan calculation sirf tab hogi jab DEBUG level enabled hoga.

## 13. Security aur production best practices

Logging ka maqsad information collect karna hai, lekin har information log karna sahi nahi.

- Passwords, access tokens, API keys aur session cookies log mat karo.
- Sensitive personal data ko logs mein expose karne se bacho.
- User-provided text ko carefully handle karo; attacker log injection ke zariye fake entries create kar sakta hai.
- File permissions aur log retention ko control karo.
- Rotating files ya centralized log storage use karo.
- ERROR aur CRITICAL ko actual failures ke liye reserve rakho; har normal event ko ERROR mat banao.
- High-traffic applications mein blocking file I/O ko consider karo. `QueueHandler` aur `QueueListener` logging ko separate thread mein process karne mein madad kar sakte hain.
- Multiple processes ke ek hi file mein likhne par coordination ka khayal rakho; ordinary file handlers automatically har multi-process scenario ko safely coordinate nahi karte.

### `QueueHandler` aur `QueueListener` ka basic concept

Agar application mein logging slow ho rahi hai, to application thread se records queue mein bheje ja sakte hain. Ek listener thread un records ko file ya doosre handlers tak pahunchata hai.

```
Application threads
        |
        v
   QueueHandler
        |
        v
       Queue
        |
        v
   QueueListener
        |
        v
 File / other handlers
```

Is pattern se logging I/O ka kuch kaam application ke main execution path se alag ho sakta hai. Lekin queue configuration, shutdown aur multiprocessing behavior ko carefully manage karna hota hai.

## 14. Filters — logs ko condition ke mutabiq control karna

Logger level decide karta hai ke kaun se severity levels accept honge. Lekin kabhi tumhein message ki content ya kisi aur condition ki bunyaad par logs filter karne hote hain.

Misal: sirf `payment` category ke records process karne hain.

```
import loggingclass PaymentFilter(logging.Filter):    def filter(self, record):        return "payment" in record.getMessage().lower()logger = logging.getLogger("my_app")logger.setLevel(logging.DEBUG)handler = logging.StreamHandler()handler.addFilter(PaymentFilter())handler.setFormatter(    logging.Formatter("%(levelname)s: %(message)s"))logger.addHandler(handler)logger.info("Payment successful")logger.info("User logged in")logger.error("Payment failed")
```

Is example mein handler sirf woh messages emit karega jin mein `payment` lafz hai.

`logging.Filter` ko aur advanced tareeqe se bhi use kar sakte ho, jaise logger name, user-defined record attributes ya application-specific conditions check karna.

Production mein message text ke bajaye structured attributes filter karna aksar zyada reliable hota hai.

## 15. Structured logging — JSON format

Jab tumhare logs ko monitoring system, log analytics tool ya doosri application ne process karna ho, to JSON format useful hota hai.

Example log:

```
{
  "level": "ERROR",
  "event": "payment_failed",
  "user_id": 123,
  "order_id": 456
}
```

Is tarah har field ko alag search ya filter kiya ja sakta hai.

Python ke standard logging module mein custom formatter se JSON output banaya ja sakta hai. Neeche ek basic example hai:

```
import jsonimport loggingclass JsonFormatter(logging.Formatter):    def format(self, record):        data = {            "level": record.levelname,            "logger": record.name,            "message": record.getMessage(),        }        if record.exc_info:            data["exception"] = self.formatException(                record.exc_info            )        return json.dumps(data)logger = logging.getLogger("my_app")logger.setLevel(logging.INFO)handler = logging.StreamHandler()handler.setFormatter(JsonFormatter())logger.addHandler(handler)logger.propagate = Falselogger.info(    "Order created",    extra={"order_id": 456})try:    10 / 0except ZeroDivisionError:
```

Is example ka formatter basic fields aur exception traceback ko JSON mein convert karta hai. Lekin `extra={"order_id": 456}` se milne wala `order_id` automatically JSON mein include nahi hota, kyun ke formatter abhi us field ko explicitly read nahi kar raha.

Agar order ID bhi chahiye, to formatter mein yeh add karo:

```
if hasattr(record, "order_id"):    data["order_id"] = record.order_id
```

Important: JSON logging ka matlab sirf JSON string print karna nahi. Achhi structured logging mein consistent field names, timestamps, request IDs aur sensitive-data controls bhi shamil hote hain.

## 16. Complete practical project — logging ko real code mein use karo

Ab ek chhota application banate hain jismein logging, named logger, file output aur exception handling sab use hon.

```
import loggingfrom logging.handlers import RotatingFileHandlerdef setup_logging():    logger = logging.getLogger("shop")    logger.setLevel(logging.DEBUG)    # Duplicate handlers se bachao    if logger.handlers:        return logger    formatter = logging.Formatter(        "%(asctime)s | %(levelname)s | "        "%(name)s | %(message)s"    )    # Console: INFO aur us se upar    console = logging.StreamHandler()    console.setLevel(logging.INFO)    console.setFormatter(formatter)    # File: DEBUG aur us se upar    file_handler = RotatingFileHandler(        "shop.log",        maxBytes=1_000_000,        backupCount=3,        encoding="utf-8",    )    file_handler.setLevel(logging.DEBUG)    file_handler.setFormatter(formatter)    logger.addHandler(console)    logger.addHandler(file_handler)    logger.propagate = False
```

### Is project mein kya seekha?

1. `setup_logging()` configuration ko ek jagah rakhta hai.
2. `getLogger("shop")` application-specific logger deta hai.
3. Console par INFO aur higher severity messages aate hain.
4. File mein DEBUG se shuru hone wale tamam levels record hote hain.
5. `RotatingFileHandler` log file ko unlimited grow hone se rokne mein madad karta hai.
6. `logger.exception()` validation error ke saath traceback record karta hai.
7. `if __name__ == "__main__"` main program ko import hone par automatically run hone se bachata hai.

Is code ko `shop.py` ke naam se save karke run kar sakte ho. Successful order par total `300` aayega. Agar negative price ya quantity doge, to validation error log hogi.

## 17. Apni understanding test karo

## Logging knowledge check

0/5 answered

1\. Agar level=logging.WARNING hai, kaun se levels show honge?

Sirf WARNING

DEBUG, INFO aur WARNING

WARNING, ERROR aur CRITICAL

Sirf ERROR aur CRITICAL

2\. Exception ka traceback log karne ka sab se seedha tareeqa kya hai?

logging.info()

logging.exception() exception handler ke andar

print()

logging.disable()

3\. Formatter ka main kaam kya hai?

Error ko fix karna

Log file delete karna

Log record ka output format tay karna

Logger ko database se connect karna

4\. Log file ko size limit par rotate karne ke liye kya use hota hai?

StreamHandler

RotatingFileHandler

NullHandler

Filter

5\. \`logger.debug(f'Result: {expensive_call()}')\` mein kya masla ho sakta hai?

F-string kabhi kaam nahi karti

DEBUG disabled ho tab bhi function evaluate ho sakta hai

Logger hamesha CRITICAL ban jata hai

File lazmi delete hoti hai

Check answers

## 18. Basic se advanced tak learning roadmap

1. Beginner: `import logging`, 5 levels, `basicConfig()` aur `print()` se difference.
2. Beginner–Intermediate: `format`, `datefmt`, file logging aur named loggers.
3. Intermediate: Handlers, formatters, `logging.exception()`, `exc_info` aur logger hierarchy.
4. Upper Intermediate: Rotating files, `dictConfig()`, filters aur duplicate logs ki debugging.
5. Advanced: Structured JSON logging, `QueueHandler`, multi-process applications, performance aur secure log management.

### Final recap — yeh 7 cheezein yaad rakho

| Concept              | Simple meaning                                                    |
| -------------------- | ----------------------------------------------------------------- |
| Logger               | Log record generate karta hai                                     |
| Level                | Message ki severity batata hai                                    |
| Handler              | Message ko console, file ya doosri destination par bhejta hai     |
| Formatter            | Message ka format tay karta hai                                   |
| Filter               | Extra conditions ki bunyaad par records allow ya reject karta hai |
| `logger.exception()` | Exception ke saath traceback record karta hai                     |
| Rotation             | Log files ko size ya time ke mutabiq manage karti hai             |

Agar tum in concepts ko khud code karke samajh lete ho, to tum simple scripts se le kar APIs, web applications aur production services tak logging implement karne ki achhi bunyaad bana loge.

# Python Logging: Professional Mastery — Part 2

Ab hum Python Logging ke in 8 topics ko Roman Urdu mein concepts, practical code, real-world examples aur common mistakes ke saath detail mein seekhenge.

Is part ka goal sirf logging methods yaad karna nahi, balkay yeh samajhna hai ke production application mein logs kaise design, collect, test aur monitor kiye jate hain.

## Advanced logging ka overall roadmap

1\. Contextual logging

`extra`, `LoggerAdapter`, request ID, user ID aur order ID.

2\. Custom levels aur handlers

Apne logging levels aur output destinations banana.

3\. Queue-based logging

`QueueHandler` aur `QueueListener` se logging I/O ko alag rakhna.

4\. Centralized logging

Multiple Python files aur packages se logs ko ek jagah collect karna.

5\. Logging tests

`assertLogs()` se expected logs verify karna.

6\. Async aur multiprocessing

Concurrent applications mein logs safely manage karna.

7\. Production monitoring

Log aggregation, debugging, alerts aur observability.

8\. Complete real-world project

In concepts ko ek production-style application mein integrate karna.

# Topic 1 — `extra` aur `LoggerAdapter`

## 1.1 Contextual logging kya hoti hai?

Maan lo tumhari e-commerce application mein 1,000 users ek hi waqt par requests bhej rahe hain.

Logs mein sirf yeh likha hai:

```
INFO - Order process hui
ERROR - Order process fail hui
INFO - Order process hui
```

Ab sawal yeh hai ke error kis user ka tha? Kis order ka tha? Kis request mein issue aaya?

In messages mein context nahi hai.

Contextual logging ka matlab hai log message ke saath relevant information bhi record karna, taake event ko identify aur trace karna asaan ho.

Misal:

```
INFO  | request_id=req-101 | order_id=5001 | Order process hui
ERROR | request_id=req-102 | order_id=5002 | Order process fail hui
```

Ab tum `request_id` ya `order_id` ke zariye related events dhoond sakte ho.

Contextual logging ke liye Python mein `extra` aur `LoggerAdapter` do useful options hain.

## 1.2 `extra` parameter

`extra` logging record mein additional attributes add karta hai.

```
import logginglogging.basicConfig(    level=logging.INFO,    format=(        "%(levelname)s | request_id=%(request_id)s | "        "order_id=%(order_id)s | %(message)s"    ))logger = logging.getLogger("shop")logger.info(    "Order process hui",    extra={        "request_id": "req-101",        "order_id": 5001,    })
```

Output:

```
INFO | request_id=req-101 | order_id=5001 | Order process hui
```

Yahan `extra` dictionary ke keys logging record ke attributes ban jate hain.

### Lekin ek important rule

Agar formatter mein `%(request_id)s` likha hai, to har relevant log record mein `request_id` hona chahiye. Agar attribute missing hua, to formatting error ho sakta hai.

Doosra rule: `extra` mein `message`, `name`, `levelname` aur doosre existing `LogRecord` attributes ko overwrite karne ki koshish nahi karni chahiye.

## 1.3 Har baar `extra` likhna kyun inconvenient hai?

Socho ek request mein 20 log statements hain:

```
logger.info(    "Request start",    extra={"request_id": "req-101"})logger.info(    "Database query start",    extra={"request_id": "req-101"})logger.info(    "Response ready",    extra={"request_id": "req-101"})
```

Har statement mein same context repeat ho raha hai. Is se code lengthy hota hai aur kisi statement mein context bhoolne ka risk hota hai.

Yahan `LoggerAdapter` kaam aata hai.

## 1.4 `LoggerAdapter` — context automatically attach karna

```
import logginglogging.basicConfig(    level=logging.INFO,    format="%(levelname)s | %(request_id)s | %(message)s")base_logger = logging.getLogger("shop")logger = logging.LoggerAdapter(    base_logger,    {"request_id": "req-101"})logger.info("Request start")logger.info("Database query start")logger.info("Response ready")
```

Output:

```
INFO | req-101 | Request start
INFO | req-101 | Database query start
INFO | req-101 | Response ready
```

Ab har log statement mein `request_id` manually dene ki zaroorat nahi. Adapter apne context ko log records ke saath attach karta hai.

### Dono mein farq

| Feature                      | `extra`                                  | `LoggerAdapter`                        |
| ---------------------------- | ---------------------------------------- | -------------------------------------- |
| Context kahan diya jata hai? | Har logging call par                     | Adapter banate waqt                    |
| Best use case                | Ek individual event ki additional fields | Multiple events ke liye shared context |
| Code duplication             | Zyada ho sakti hai                       | Kam ho sakti hai                       |
| Example                      | `extra={"order_id": 5001}`               | Adapter ke paas `request_id`           |

Aam tor par dono ko combine bhi kiya ja sakta hai. Python ke current versions mein `LoggerAdapter` ke `merge_extra` behavior ko samajhna zaroori hai; default behavior mein adapter ka context use hota hai aur per-call `extra` automatically merge nahi hota.

## 1.5 Real-world example: request aur order context

Ab ek practical function dekho jahan request ID aur order ID dono ka context use ho raha hai.

```
import logginglogging.basicConfig(    level=logging.INFO,    format=(        "%(levelname)s | request=%(request_id)s | "        "%(message)s"    ))base_logger = logging.getLogger("shop")def process_order(request_id, order_id):    logger = logging.LoggerAdapter(        base_logger,        {"request_id": request_id},    )    logger.info("Order processing start")    try:        if order_id <= 0:            raise ValueError("Invalid order ID")        logger.info(            "Order %s successfully processed",            order_id,            extra={"request_id": request_id},        )    except ValueError:        logger.exception(            "Order %s process nahi hui",            order_id,
```

Yahan formatter ke liye `request_id` har record par available hai. Order ID ko message mein include kiya gaya hai, jabke request ID adapter provide karta hai.

Production applications mein request ID middleware ya request-handling layer se generate ya propagate karna behtar hai, taake ek request ke tamam related logs ko correlate kiya ja sake.

# Topic 2 — Custom logging levels aur custom handlers

## 2.1 Custom logging level kya hai?

Python ke standard levels hain:

```
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50
```

Kabhi application mein ek additional category chahiye hoti hai. Misal ke taur par, tum ek `NOTICE` level rakhna chahte ho jo INFO se zyada important ho, lekin WARNING se kam.

Technically custom level register kiya ja sakta hai.

```
import loggingNOTICE = 25logging.addLevelName(NOTICE, "NOTICE")logger = logging.getLogger("shop")logger.setLevel(logging.DEBUG)logger.log(NOTICE, "Daily report generate hui")
```

`logging.addLevelName()` number ko display hone wale naam se associate karta hai. `logger.log()` diye gaye numeric level par record banata hai.

Important: Sirf `addLevelName()` karne se `logger.notice()` method automatically nahi banta. Uske liye custom method implement karna padega.

### Custom levels ko limited kyun rakhna chahiye?

Agar har developer apne levels banata rahe, to log filtering, monitoring aur team conventions mushkil ho jati hain. Aksar standard levels kaafi hote hain. Custom level tab banao jab uska clear operational purpose ho.

## 2.2 Custom logging handler kya hai?

Handler ka kaam log records ko destination tak pahunchana hai.

Built-in handlers mein:

- `StreamHandler` — console ya stream.
- `FileHandler` — file.
- `RotatingFileHandler` — size-based rotating files.
- `TimedRotatingFileHandler` — time-based rotation.
- `QueueHandler` — queue mein records bhejna.

Agar tumhein logs kisi custom destination par bhejne hon, to apna handler bana sakte ho.

```
import loggingclass AlertHandler(logging.Handler):    def emit(self, record):        try:            message = self.format(record)            # Demo: alert destination ki jagah console            print(f"[ALERT SYSTEM] {message}")        except Exception:            self.handleError(record)logger = logging.getLogger("monitor")logger.setLevel(logging.DEBUG)handler = AlertHandler()handler.setLevel(logging.ERROR)handler.setFormatter(    logging.Formatter("%(levelname)s: %(message)s"))logger.addHandler(handler)logger.propagate = Falselogger.info("Normal operation")logger.error("Payment service unavailable")
```

Output:

```
[ALERT SYSTEM] ERROR: Payment service unavailable
```

Is handler mein:

- `emit()` actual log record process karta hai.
- `self.format(record)` formatter apply karta hai.
- `handleError(record)` handler ke andar formatting ya emission fail hone par logging system ki configured error handling ko invoke karta hai.

Yeh sirf educational example hai. Real alert handler mein network timeouts, retries, duplicate alerts aur secure credentials ko handle karna hoga. Har ERROR par foran alert bhejna bhi zaroori nahi; warna alert fatigue ho sakti hai.

# Topic 3 — `QueueHandler` aur `QueueListener`

## 3.1 Queue-based logging ki zaroorat kyun hai?

Maan lo tumhari web application har request ke liye log file mein likhti hai. File I/O slow ho sakti hai. Agar application ka main thread har log statement par disk write ka intezar kare, to response latency barh sakti hai.

Queue-based logging ka concept:

1. Application log record generate karti hai.
2. `QueueHandler` record queue mein daalta hai.
3. `QueueListener` queue se records nikalta hai.
4. Listener actual file ya console handler ko record deta hai.

Application

Log event generate hota hai

QueueHandler

Record queue mein enqueue karta hai

Queue

Pending records

QueueListener

Background thread records process karta hai

Log file

Console

Iska faida yeh hai ke application thread ko aam tor par sirf queue mein record dalna hota hai. Lekin queue insertion, record preparation aur queue full hone ki handling ka cost phir bhi hota hai.

## 3.2 Complete working example

```
import loggingimport queuefrom logging.handlers import QueueHandler, QueueListenerlog_queue = queue.Queue()# Actual destinationsfile_handler = logging.FileHandler(    "queue_app.log",    encoding="utf-8",)console_handler = logging.StreamHandler()formatter = logging.Formatter(    "%(asctime)s | %(levelname)s | %(message)s")file_handler.setFormatter(formatter)console_handler.setFormatter(formatter)# Queue se records nikal kar destinations ko bhejnalistener = QueueListener(    log_queue,    file_handler,    console_handler,    respect_handler_level=True,)logger = logging.getLogger("queue_app")logger.setLevel(logging.DEBUG)logger.propagate = Falselogger.addHandler(QueueHandler(log_queue))listener.start()
```

### Is code ke important points

- `queue.Queue()` thread-safe queue banata hai.
- `QueueHandler(log_queue)` records queue mein bhejta hai.
- `QueueListener(...)` background thread mein records process karta hai.
- `respect_handler_level=True` se destination handlers ke apne levels bhi respect hote hain.
- `listener.stop()` listener ko band karne se pehle pending records process karne deta hai, jab tak queue aur handler operations normally complete ho sakein.

Production mein: Queue bounded ho sakti hai. Agar queue full ho, to log records drop hone ka risk hota hai. Is behavior ko explicitly design aur monitor karna chahiye.

### Threading aur multiprocessing ka farq

`queue.Queue` threads ke darmiyan sharing ke liye hai, processes ke darmiyan nahi. Multiprocessing mein aam tor par `multiprocessing.Queue` use ki jati hai aur logging pipeline ko process lifecycle ke mutabiq configure kiya jata hai.

`QueueHandler` ko multiprocessing ke saath use karte waqt Python ki official logging documentation mein diye gaye deadlock aur multiprocessing logger ke interaction warnings ko bhi samajhna zaroori hai.

# Topic 4 — Multiple modules mein centralized logging

## 4.1 Project ki structure

Real application mein har module ka apna logger ho sakta hai, lekin configuration ideally ek central jagah par honi chahiye.

```
shop_project/
│
├── main.py
├── logging_config.py
│
└── shop/
    ├── __init__.py
    ├── auth.py
    ├── database.py
    └── orders.py
```

Recommended convention:

- `logging_config.py` — handlers, formatters aur root configuration.
- `main.py` — application startup par configuration call karta hai.
- Har module — `logging.getLogger(__name__)` use karta hai.
- Modules apne andar baar baar root handlers configure nahi karte.

## 4.2 `logging_config.py`

```
import loggingfrom logging.config import dictConfigdef configure_logging():    dictConfig({        "version": 1,        "disable_existing_loggers": False,        "formatters": {            "standard": {                "format": (                    "%(asctime)s | %(levelname)s | "                    "%(name)s | %(message)s"                )            }        },        "handlers": {            "console": {                "class": "logging.StreamHandler",                "level": "INFO",                "formatter": "standard",            },            "file": {                "class": "logging.handlers.RotatingFileHandler",                "filename": "shop.log",                "maxBytes": 1_000_000,                "backupCount": 3,                "encoding": "utf-8",                "level": "DEBUG",                "formatter": "standard",            },        },
```

## 4.3 `shop/orders.py`

```
import logginglogger = logging.getLogger(__name__)def create_order(order_id):    logger.info("Order %s create kar rahe hain", order_id)    if order_id <= 0:        logger.warning("Invalid order ID: %s", order_id)        return False    logger.info("Order %s create ho gaya", order_id)    return True
```

## 4.4 `main.py`

```
from logging_config import configure_loggingfrom shop.orders import create_orderdef main():    configure_logging()    create_order(501)    create_order(-1)if __name__ == "__main__":    main()
```

Ek subtle point: is example mein module import configuration se pehle hota hai, lekin module sirf named logger create karta hai; woh khud log emit nahi karta. Is liye configuration startup mein call karne ke baad actual logging sahi configured hoti hai. Agar imports ke dauran hi logs emit hon, to configuration ko aur pehle execute karna chahiye.

Is design se tamam modules ke logs central configuration se control hote hain, aur logger name se source module identify kiya ja sakta hai.

# Topic 5 — Unit testing mein logs test karna (`assertLogs`)

## 5.1 Logging ko test kyun karte hain?

Unit tests sirf function ka return value test nahi karte. Kabhi yeh bhi ensure karna hota hai ke:

- Invalid input par WARNING log hui.
- Failure par ERROR log hui.
- Log message mein relevant information maujood hai.
- Exception ka traceback record hua.

Python ka `unittest` framework `assertLogs()` provide karta hai.

## 5.2 Basic example

```
import loggingimport unittestdef validate_price(price):    logger = logging.getLogger("shop.pricing")    if price < 0:        logger.warning("Negative price received")        return False    return Trueclass TestPricing(unittest.TestCase):    def test_negative_price_logs_warning(self):        with self.assertLogs(            "shop.pricing",            level="WARNING"        ) as captured:            result = validate_price(-10)        self.assertFalse(result)        self.assertEqual(len(captured.records), 1)        self.assertEqual(            captured.records[0].levelname,            "WARNING",        )        self.assertIn(            "Negative price",            captured.output[0],        )
```

### Is example ko samjho

`assertLogs("shop.pricing", level="WARNING")` selected logger ke WARNING aur us se higher-level records capture karta hai.

`captured.records` actual `LogRecord` objects ki list hai.

`captured.output` formatted log strings ki list hai.

Agar expected level ka koi log generate na hua, to test fail ho jayega.

## 5.3 Exception logging ko test karna

```
import loggingimport unittestdef divide(a, b):    logger = logging.getLogger("calculator")    try:        return a / b    except ZeroDivisionError:        logger.exception("Division failed")        raiseclass TestCalculator(unittest.TestCase):    def test_zero_division_is_logged(self):        with self.assertLogs(            "calculator",            level="ERROR"        ) as captured:            with self.assertRaises(ZeroDivisionError):                divide(10, 0)        record = captured.records[0]        self.assertEqual(record.levelname, "ERROR")        self.assertIsNotNone(record.exc_info)        self.assertIn("Division failed", record.getMessage())
```

Yahan hum verify kar rahe hain ke:

1. Exception raise hota hai.
2. ERROR log generate hoti hai.
3. Record mein exception information bhi maujood hai.

Professional tip: Har log message ko exact string ke saath test karna zaroori nahi. Un tests ko priority do jo operationally important behavior, severity aur required context verify karte hain.

# Topic 6 — Async applications aur multiprocessing logging

## 6.1 Async logging mein kya challenge hai?

Python ke `asyncio` applications mein bohat se tasks ek event loop share karte hain.

Agar har task log karte waqt slow disk ya network I/O ka intezar kare, to event loop ke doosre tasks bhi delay ho sakte hain.

Misal:

```
async def handle_request():    logger.info("Request received")    result = await fetch_data()    logger.info("Request completed")    return result
```

Yeh code apne aap mein valid hai. Masla tab hota hai jab logging handler slow ya blocking I/O karta hai.

Solution: Queue-based logging ya koi non-blocking logging architecture use karo. Yaad rakho, `async def` ke andar synchronous logging call automatically asynchronous nahi ban jati.

## 6.2 Async example with queue-based logging

Yeh example `asyncio` ke multiple tasks aur queue-based logging ko combine karta hai.

```
import asyncioimport loggingimport queuefrom logging.handlers import QueueHandler, QueueListenerdef setup_logging():    log_queue = queue.Queue()    file_handler = logging.FileHandler(        "async_app.log",        encoding="utf-8",    )    file_handler.setFormatter(        logging.Formatter(            "%(asctime)s | %(levelname)s | %(message)s"        )    )    listener = QueueListener(log_queue, file_handler)    logger = logging.getLogger("async_app")    logger.setLevel(logging.INFO)    logger.propagate = False    logger.handlers.clear()    logger.addHandler(QueueHandler(log_queue))    listener.start()    return logger, listener, file_handlerasync def worker(task_id, logger):    logger.info("Task %s start hui", task_id)    await asyncio.sleep(0.1)
```

Is example mein:

- `asyncio.gather()` multiple tasks ko concurrently execute karta hai.
- Logging calls records queue mein bhejti hain.
- Listener background thread mein file writes karta hai.
- `finally` block cleanup karta hai.

Yeh demonstration hai. Real application mein logger ko baar baar initialize karne se bachna chahiye, aur queue capacity, shutdown behavior aur task context ko bhi manage karna chahiye.

### Async tasks mein request context

Agar har async task ka apna request ID ho, to Python ka `contextvars` module useful hota hai. Is se task-local context maintain kiya ja sakta hai, bina har function mein request ID manually pass kiye.

Lekin `contextvars` ko formatter mein automatically include karne ke liye tumhein filter, adapter ya custom record factory se context ko `LogRecord` par attach karna hota hai.

## 6.3 Multiprocessing logging

Multiprocessing mein multiple processes ek application ke liye logs generate kar sakte hain.

Misal:

```
Main process
    ├── Worker process 1
    ├── Worker process 2
    └── Worker process 3
```

Agar har process ek hi log file ko independently write kare, to rotation aur concurrent writes ke issues aa sakte hain.

Recommended architecture:

```
Worker 1 ──┐
Worker 2 ──┼──> multiprocessing.Queue
Worker 3 ──┘            |
                         v
                 Central listener
                         |
                         v
                    Rotating file
```

Har worker mein `QueueHandler` aur shared `multiprocessing.Queue` configure ki ja sakti hai. Parent process listener aur actual file handler own karta hai.

Important production rules:

- Har process mein alag `FileHandler` ko same rotating file par chalane se bacho.
- Shared queue aur listener ka lifecycle carefully manage karo.
- Processes band karne se pehle workers ko records enqueue karne ka mauqa do.
- Queue full hone aur worker crashes ke behavior ko define karo.
- Multiprocessing logger ke internal records ko usi queue mein route karte waqt recursion ya deadlock ke risks ko samjho.

Core concept: Threads ke liye `queue.Queue`, aur processes ke darmiyan communication ke liye aam tor par `multiprocessing.Queue` use hoti hai.

# Topic 7 — Production debugging, log aggregation aur monitoring

## 7.1 Logging aur monitoring mein farq

Logging batati hai ke application ke andar kya events hue.

Monitoring metrics aur system health batati hai ke application overall kaisi perform kar rahi hai.

| Logging                    | Monitoring                             |
| -------------------------- | -------------------------------------- |
| Specific events aur errors | Error rate, latency, CPU, memory       |
| Detailed troubleshooting   | Trends aur system health               |
| Example: payment timeout   | Example: 5% requests fail ho rahi hain |
| Log records se search      | Metrics aur alerts se detection        |

Production systems mein dono ko saath use kiya jata hai.

## 7.2 Log aggregation kya hoti hai?

Agar tumhare paas 20 servers hain, to har server ki log file manually check karna practical nahi.

Log aggregation ka matlab hai multiple applications aur servers se logs ko ek central platform par collect karna, jahan unhein search, filter aur analyze kiya ja sake.

API server

Application logs

Worker

Job logs

Cloud service

Service logs

Other services

Infrastructure logs

Log collector / aggregation pipeline

Collect, parse, enrich aur forward

Central log platform

Search · Dashboards · Alerts · Investigation

Centralized logging ke liye aam options mein Elastic Stack, Grafana Loki, cloud-provider logging services aur managed observability platforms shamil hain. Selection budget, scale, retention, access controls aur operational requirements par depend karta hai.

## 7.3 Production mein useful fields

Aik well-designed structured log mein aam tor par yeh fields hoti hain:

```
{
  "timestamp": "2026-10-12T17:00:00Z",
  "level": "ERROR",
  "service": "order-api",
  "environment": "production",
  "request_id": "req-101",
  "event": "payment_failed",
  "message": "Payment provider timeout",
  "duration_ms": 2500
}
```

Yeh example schema hai; timestamp aur values illustrative hain.

In fields se tum yeh sawalat answer kar sakte ho:

- Kya issue sirf production mein aa raha hai?
- Kis service mein error rate barhi hai?
- Kya ek request multiple services se guzri?
- Payment provider kitna slow hai?
- Kya problem kisi specific release ke baad shuru hui?

Sensitive data, credentials aur unnecessary personal information log nahi karni chahiye.

## 7.4 Alerting ka practical concept

Har ERROR par alert bhejna achhi strategy nahi. Is ke bajaye meaningful conditions define karo.

Misal:

- 5 minutes mein error rate 5% se zyada ho.
- Payment service unavailable ho.
- API ki p95 latency threshold se zyada ho.
- Background jobs repeatedly fail ho rahi hon.

Yeh thresholds sirf examples hain; actual values service ke SLO, traffic aur business impact ke mutabiq define hoti hain.

Golden rule: Logs events explain karte hain; metrics problems detect karne mein madad karti hain; traces distributed request ka safar samjhati hain.

# Topic 8 — Real-world logging architecture design karna

Ab tak humne individual concepts seekhe. Ab inhein ek production-style order processing application mein combine karte hain.

## 8.1 Architecture kaisi honi chahiye?

API / Application layer

Request receive aur validate hoti hai

Context layer

Request ID, service name, environment

Named loggers

auth · orders · payments · database

Central logging pipeline

Formatter · Queue · Handlers · Rotation

Log destination

Console / local file / centralized platform

Architecture ka basic principle yeh hai ke business logic aur logging configuration ko separate rakho. Har function ko yeh decide nahi karna chahiye ke log file kahan hai ya handler kaise configure karna hai.

## 8.2 Recommended project structure

```
order_service/
├── main.py
├── logging_config.py
├── context.py
├── services/
│   ├── __init__.py
│   ├── orders.py
│   └── payments.py
└── tests/
    ├── test_orders.py
    └── test_logging.py
```

Har component ka role:

| File                | Responsibility                        |
| ------------------- | ------------------------------------- |
| `logging_config.py` | Handlers, formatters aur levels       |
| `context.py`        | Request context manage karna          |
| `orders.py`         | Order business logic aur related logs |
| `payments.py`       | Payment events aur errors             |
| `main.py`           | Application startup aur shutdown      |
| `tests/`            | Behavior aur logging verification     |

## 8.3 Complete mini-project

Neeche ek runnable single-file example hai jo named logger, contextual fields, JSON logging, file rotation aur exception handling combine karta hai.

```
import jsonimport loggingfrom logging.handlers import RotatingFileHandlerclass JsonFormatter(logging.Formatter):    def format(self, record):        data = {            "level": record.levelname,            "logger": record.name,            "message": record.getMessage(),        }        for field in ("request_id", "order_id", "service"):            if hasattr(record, field):                data[field] = getattr(record, field)        if record.exc_info:            data["exception"] = self.formatException(                record.exc_info            )        return json.dumps(data)def setup_logging():    logger = logging.getLogger("order_service")    logger.setLevel(logging.DEBUG)    logger.propagate = False    # Existing handlers ko repeat mein add na karo    if logger.handlers:        return logger    formatter = JsonFormatter()
```

Is example mein `LoggerAdapter` request ID aur service name attach karta hai. `extra` har event ka order ID add karta hai. Custom formatter in fields ko JSON mein include karta hai. Rotating handler logs ko limited files mein rakhta hai.

Ek important technical nuance: standard `LoggerAdapter` ka default behavior per-call `extra` ko adapter ke context ke saath merge nahi karta. Is code mein agar `order_id` ko har record par lazmi chahiye, to adapter ko custom `process()` method ya supported `merge_extra` option ke saath configure karna hoga. Python ke current versions mein `merge_extra=True` use kar sakte ho.

Corrected adapter initialization:

```
context_logger = logging.LoggerAdapter(    logger,    {        "request_id": request_id,        "service": "orders",    },    merge_extra=True,)
```

Isay pehle wale code mein use karo, taake `order_id` formatter tak pohanch sake. Agar tumhara Python version `merge_extra` support nahi karta, to custom adapter implement karna hoga ya context ko har record par explicitly attach karna hoga.

## 8.4 Production deployment se pehle checklist

### Production readiness

0 / 10

Logging configuration application startup par ek martaba hoti hai

Har module getLogger(\_\_name\_\_) use karta hai

Logs mein timestamp, severity, service aur useful context hota hai

Exceptions ke saath traceback record hota hai

Passwords, API keys aur sensitive data redact kiya jata hai

Log rotation ya centralized retention policy configured hai

Duplicate handlers aur propagate behavior test kiya gaya hai

Queue full, shutdown aur worker failure behavior define hai

Important log events ke unit tests maujood hain

Monitoring aur alert thresholds operational requirements ke mutabiq hain

Reset checklist

## Final assessment — kya tum professional logging ke liye ready ho?

Professional mastery ka matlab yeh nahi ke tum har logging class ka naam yaad kar lo. Iska matlab yeh hai ke tum practical problems solve kar sako:

- Ek failed request ke tamam related logs ko request ID se trace karna.
- Slow logging ko queue-based architecture se optimize karna.
- Multiple modules aur workers ke logs ko centralize karna.
- Automated tests se verify karna ke important errors log ho rahe hain.
- Production mein useful alerts generate karna, bina unnecessary noise ke.
- Logs ko secure, searchable aur operationally useful rakhna.

Meri recommendation: Is sequence mein practice karo: pehle `extra` aur `LoggerAdapter`, phir centralized logging, uske baad `assertLogs()`, phir queue-based logging aur aakhir mein monitoring. Har topic par chhota program khud likho aur jaan boojh kar errors introduce karke logs inspect karo.

Jab tum in 8 topics ko code, tests aur ek complete project mein implement kar loge, to tumhari Python logging ki understanding basic se professional application development tak kaafi strong ho jayegi.