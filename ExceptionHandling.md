# Python Exception Handling — Basic se Advanced (Roman Urdu)

Python mein Exception Handling ka matlab hai program mein aane wali runtime errors ko handle karna, taake program achanak crash na ho aur hum user ko proper message de saken.

Misal ke taur par:

- User number ki jagah text enter kar de.
- Kisi aisi file ko open karein jo exist nahi karti.
- Zero se division karne ki koshish ho.
- JSON file ka data corrupt ho.
- Database ya API se data lene mein error aa jaye.

Hum is topic ko basic se advanced level tak practical examples ke saath seekhenge.

## 1. Error aur Exception mein farq

```
print(10 / 0)
```

Output:

```
ZeroDivisionError: division by zero
```

Yahan program runtime par exception raise karta hai.

Python mein errors ko samajhne ke liye yeh distinction yaad rakhein:

- Syntax error: Code ka syntax ghalat hai; misal ke taur par `if` ke baad colon na lagana.
- Exception: Code execute ho raha hota hai, lekin execution ke dauran koi problem aa jati hai.

```
# SyntaxErrorif 10 > 5    print("Yes")
```

```
# Runtime exceptionnumber = int("hello")
```

Doosri example mein `ValueError` raise hoga, kyun ke `"hello"` ko integer mein convert nahi kiya ja sakta.

## 2. `try` aur `except` — Basic handling

`try` ke andar woh code likhte hain jahan exception aane ka imkaan ho. `except` mein batate hain ke exception aane par kya karna hai.

```
try:    number = int(input("Number enter karein: "))    print(100 / number)except:    print("Koi error aa gaya!")
```

Agar user `abc` enter kare, ya `0` enter kare, dono surat mein generic message print hoga.

Lekin is code mein ek problem hai: `except:` har qisam ki exception ko pakar sakta hai, jis se asli problem chhup sakti hai.

Professional rule: Baghair zaroorat bare `except:` se parhez karein. Specific exceptions handle karein.

## 3. Specific exceptions handle karna

```
try:    number = int(input("Number enter karein: "))    result = 100 / number    print("Result:", result)except ValueError:    print("Sirf valid integer enter karein.")except ZeroDivisionError:    print("Zero se division nahi ho sakti.")
```

Ab Python exception ki type ke mutabiq relevant `except` block execute karega.

| Exception           | Kab hoti hai?                                            |
| ------------------- | -------------------------------------------------------- |
| `ValueError`        | Value expected format mein na ho                         |
| `TypeError`         | Ghalat types par operation kiya jaye                     |
| `ZeroDivisionError` | Zero se divide kiya jaye                                 |
| `FileNotFoundError` | File nahi milti                                          |
| `PermissionError`   | File ya resource access karne ki permission na ho        |
| `KeyError`          | Dictionary mein key na ho                                |
| `IndexError`        | List ya tuple ka index range se bahar ho                 |
| `AttributeError`    | Object par requested attribute ya method available na ho |
| `ImportError`       | Import karne mein problem aaye                           |
| `OSError`           | Operating system se related operation fail ho            |

Yaad rakhein ke `FileNotFoundError` aur `PermissionError`, `OSError` ki subclasses hain. Is liye exception handling mein specific exceptions ko pehle rakhna behtar hai.

## 4. `else` block

`else` sirf us waqt execute hota hai jab `try` block mein koi exception raise na ho.

```
try:    number = int(input("Number: "))    result = 100 / numberexcept ValueError:    print("Invalid number.")except ZeroDivisionError:    print("Zero allowed nahi.")else:    print("Calculation successful!")    print("Result:", result)
```

Execution flow:

`try` block

Risky operation execute karein

Success

`else`

Exception

`except`

`else` ka faida yeh hai ke aap success wala code exception-handling code se alag rakh sakte hain.

## 5. `finally` block

`finally` aam tor par har surat mein execute hota hai, chahe exception aaye ya na aaye. Yeh cleanup operations ke liye useful hai.

```
try:    file = open("data.txt", "r")    content = file.read()    print(content)except FileNotFoundError:    print("File nahi mili.")finally:    print("Operation complete.")
```

Yahan `finally` file na milne par bhi execute hoga.

Important: Is example mein agar file open ho jaye aur `read()` fail ho jaye, to file close karne ka code maujood nahi hai. File resources ke liye `with` zyada safe approach hai, jise hum aage dekhenge.

## 6. `raise` — Khud exception raise karna

Kabhi Python ki built-in validation kaafi nahi hoti. Aapko apne rules ke mutabiq exception raise karni hoti hai.

Misal: age negative nahi ho sakti.

```
def check_age(age):    if age < 0:        raise ValueError("Age negative nahi ho sakti.")    print("Age valid hai.")check_age(20)check_age(-5)
```

Jab `check_age(-5)` execute hoga, `ValueError` raise hoga.

Agar exception ko handle nahi kiya gaya, to program ka current execution terminate ho sakta hai aur traceback show hoga.

Isko handle karne ka tareeqa:

```
try:    check_age(-5)except ValueError as error:    print("Validation error:", error)
```

Output:

```
Validation error: Age negative nahi ho sakti.
```

`raise` ko business rules enforce karne ke liye use kiya ja sakta hai, jaise:

- Student ki age valid honi chahiye.
- Bank account ka withdrawal balance se zyada nahi hona chahiye.
- Product ki price negative nahi honi chahiye.
- Student ID duplicate nahi honi chahiye.

## 7. `as error` — Exception ki details lena

```
try:    result = int("abc")except ValueError as error:    print(type(error).__name__)    print(error)
```

Output:

```
ValueError
invalid literal for int() with base 10: 'abc'
```

Yahan `error` exception object hai. Is se aap exception ka message aur type access kar sakte hain.

Production code mein error ko log karna bhi useful hota hai:

```
import logginglogging.basicConfig(level=logging.ERROR)try:    number = int("abc")except ValueError:    logging.exception("Number conversion fail ho gayi.")
```

`logging.exception()` exception handler ke andar exception message ke saath traceback bhi log karta hai.

## 8. Multiple exceptions ek saath handle karna

Agar multiple exceptions ke liye same action karna ho, to tuple use karein.

```
try:    number = int(input("Number: "))    result = 100 / numberexcept (ValueError, ZeroDivisionError) as error:    print("Calculation fail:", error)
```

Yeh tab useful hai jab dono exceptions par same response dena ho.

Lekin agar har exception ka response alag hai, to separate `except` blocks zyada readable hote hain.

## 9. Exception hierarchy

Python mein exceptions ek hierarchy follow karti hain.

BaseException

Exception

Aam application exceptions

ValueError

TypeError

OSError

LookupError

KeyError, IndexError

Is hierarchy ki wajah se yeh code kaam karta hai:

```
try:    int("abc")except Exception as error:    print("Error:", error)
```

`Exception` aam application exceptions ko catch karta hai, jin mein `ValueError` bhi shamil hai.

Advanced rule: `except BaseException:` ya bare `except:` ko normal application logic mein use na karein. `KeyboardInterrupt`, `SystemExit` aur doosri control-flow exceptions ko ghair zaroori taur par catch karna program ke behavior ko kharab kar sakta hai.

## 10. Nested `try-except`

Jab ek operation ke andar doosra operation independently fail ho sakta ho, tab nested exception handling useful ho sakti hai.

```
try:    number = int(input("Number: "))    try:        result = 100 / number    except ZeroDivisionError:        print("Division ke liye zero valid nahi.")    else:        print("Result:", result)except ValueError:    print("Integer enter karein.")
```

Is example mein:

- Outer `try` input conversion handle karta hai.
- Inner `try` division handle karta hai.

Har jagah nested blocks banana zaroori nahi. Agar separate functions bana kar code zyada clear ho sakta hai, to woh approach prefer karein.

## 11. Custom exceptions banana

Advanced projects mein apni exception classes define karna useful hota hai.

```
class InsufficientBalanceError(Exception):    """Jab account mein balance kam ho."""    passdef withdraw(balance, amount):    if amount <= 0:        raise ValueError("Amount positive hona chahiye.")    if amount > balance:        raise InsufficientBalanceError(            "Account mein balance kam hai."        )    return balance - amounttry:    remaining = withdraw(1000, 1500)    print("Remaining balance:", remaining)except InsufficientBalanceError as error:    print("Withdrawal fail:", error)except ValueError as error:    print("Invalid amount:", error)
```

Custom exceptions ka faida yeh hai ke caller samajh sakta hai ke operation kis business reason ki wajah se fail hua.

Ek professional project mein exceptions ko meaningful naam dein, jaise:

- `StudentNotFoundError`
- `DuplicateStudentError`
- `InvalidStudentDataError`
- `InsufficientBalanceError`

Custom exception ko aam tor par `Exception` se inherit karna chahiye.

## 12. `with` statement aur file handling

File handling mein `finally` ke zariye file close karne ke bajaye `with` statement zyada reliable aur simple hai.

```
try:    with open("students.txt", "r", encoding="utf-8") as file:        content = file.read()except FileNotFoundError:    print("Students file mojood nahi.")except PermissionError:    print("File access karne ki permission nahi.")else:    print(content)
```

`with` statement file ko context se bahar nikalte waqt automatically close kar deta hai, chahe reading ke dauran exception aaye.

Agar file ka path user input se aa raha ho, to `OSError` ki doosri subclasses bhi aa sakti hain. Is liye file handling mein sirf `FileNotFoundError` hi possible exception nahi hai.

## 13. JSON aur file exceptions

Student Record Management System mein JSON file se data read karte waqt kai qisam ki errors aa sakti hain.

```
import jsonfrom pathlib import Pathfile_path = Path("students.json")def load_students():    try:        with file_path.open("r", encoding="utf-8") as file:            data = json.load(file)    except FileNotFoundError:        return []    except json.JSONDecodeError as error:        raise ValueError(            "JSON file ka format invalid hai."        ) from error    except OSError as error:        raise RuntimeError(            "File read nahi ho saki."        ) from error    if not isinstance(data, list):        raise ValueError("JSON data list hona chahiye.")    return data
```

Is function mein teen important concepts hain:

1. `FileNotFoundError` par empty list return hoti hai.
2. `JSONDecodeError` par meaningful validation error raise hoti hai.
3. `raise ... from error` original exception ko cause ke taur par preserve karta hai.

Important: Missing file par empty list tabhi return karein jab application ke rules mein iska matlab “abhi koi records nahi” ho. Agar file ka missing hona configuration ya data loss ka signal hai, to usay chupana nahi chahiye.

JSON syntactically valid hone ka matlab yeh bhi nahi ke uske andar student records sahi format mein hain. Is liye schema aur field validation alag se karni hoti hai.

## 14. `raise ... from error` — Exception chaining

Jab low-level exception ko higher-level, meaningful exception mein convert karte hain, to original cause preserve karna chahiye.

```
def convert_price(value):    try:        return float(value)    except ValueError as error:        raise ValueError(            "Product price valid number honi chahiye."        ) from errortry:    convert_price("abc")except ValueError as error:    print(error)
```

`from error` Python ko batata hai ke nayi exception ki asal wajah purani exception thi. Debugging ke waqt traceback mein dono ka relation nazar aata hai.

Agar aap jaan boojh kar original exception ka cause suppress karna chahte hain, to `raise NewError(...) from None` use kar sakte hain. Lekin is se debugging ki information kam ho sakti hai.

## 15. `raise` without arguments — Original exception dobara raise karna

Kabhi exception catch karne ke baad logging karni hoti hai, magar exception ko suppress nahi karna hota.

```
def process_data():    try:        result = 10 / 0        return result    except ZeroDivisionError:        print("Debugging ke liye error detect hui.")        raisetry:    process_data()except ZeroDivisionError:    print("Caller ne exception handle kar li.")
```

`raise` baghair arguments ke current exception ko dobara raise karta hai aur uska traceback preserve karta hai.

Yeh approach us waqt useful hai jab lower-level function error ko observe kare, lekin final decision caller ko lene de.

## 16. `assert` aur exceptions ka farq

`assert` debugging ke dauran assumptions check karne ke liye use hota hai.

```
age = 20assert age >= 0, "Age negative nahi honi chahiye."print("Age:", age)
```

Agar condition false ho, to `AssertionError` aata hai.

Lekin user input validation ke liye sirf `assert` par depend na karein, kyun ke Python optimization mode (`-O`) mein assertions disable ho sakti hain.

Production validation ke liye:

```
def validate_age(age):    if age < 0:        raise ValueError("Age negative nahi ho sakti.")    return age
```

Yeh validation optimization mode mein bhi active rahegi.

## 17. `try` block ko chhota kyun rakhna chahiye?

Yeh code dekhein:

```
try:    number = int(input("Number: "))    result = 100 / number    print("Result:", result)    save_to_database(result)except ValueError:    print("Invalid input.")
```

Agar `save_to_database()` ke andar bhi `ValueError` aaye, to woh bhi `Invalid input` ke taur par report ho sakta hai, halaanke asal masla database processing mein ho.

Behtar approach:

```
try:    number = int(input("Number: "))except ValueError:    print("Valid integer enter karein.")else:    result = calculate_result(number)    save_to_database(result)
```

Is approach mein input conversion ka error aur baqi processing ke errors alag rehte hain.

Golden rule: `try` mein sirf woh statements rakhein jin ki exceptions aap us jagah handle karna chahte hain.

## 18. Exception handling aur unit testing

Professional development mein sirf exception handle karna kaafi nahi. Yeh bhi test karna hota hai ke expected exception raise ho rahi hai ya nahi.

```
import unittestdef withdraw(balance, amount):    if amount <= 0:        raise ValueError("Amount positive hona chahiye.")    if amount > balance:        raise InsufficientBalanceError(            "Balance kam hai."        )    return balance - amountclass TestWithdraw(unittest.TestCase):    def test_successful_withdrawal(self):        self.assertEqual(withdraw(1000, 300), 700)    def test_negative_amount(self):        with self.assertRaises(ValueError):            withdraw(1000, -100)    def test_insufficient_balance(self):        with self.assertRaises(InsufficientBalanceError):            withdraw(1000, 1500)if __name__ == "__main__":    unittest.main()
```

Is example mein `InsufficientBalanceError` class ko pehle define karna zaroori hai:

```
class InsufficientBalanceError(Exception):    pass
```

`assertRaises()` test karta hai ke operation ke dauran expected exception raise hui. Agar exception raise na ho, test fail ho jata hai.

Logging test karne ke liye `unittest.TestCase.assertLogs()` bhi use kiya ja sakta hai.

## 19. Production-level exception handling ke rules

| Rule                | Professional approach                                         |
| ------------------- | ------------------------------------------------------------- |
| Exception selection | Specific exception catch karein                               |
| Debugging           | Traceback aur original cause preserve karein                  |
| User messages       | Technical traceback ke bajaye clear message dikhayein         |
| Logging             | Errors ko relevant context ke saath log karein                |
| Cleanup             | File aur doosre resources ke liye context managers use karein |
| Validation          | User data ko explicitly validate karein                       |
| Custom exceptions   | Business rules ke liye meaningful exception classes banayein  |
| Testing             | Success aur failure dono paths test karein                    |
| Exception scope     | `try` block ko focused aur chhota rakhein                     |
| Error suppression   | Error ko bina reason ignore na karein                         |

Ek aur important baat: sensitive data, passwords, access tokens aur private records ko exception logs mein expose nahi karna chahiye.

## 20. Advanced practice project

Ab concepts ko ek practical program mein apply karein. Yeh mini Student Record Management System ka starting point hai.

```
import jsonimport loggingfrom pathlib import Pathlogging.basicConfig(    filename="student_app.log",    level=logging.ERROR,    format="%(asctime)s - %(levelname)s - %(message)s")DATA_FILE = Path("students.json")class StudentNotFoundError(Exception):    passclass DuplicateStudentError(Exception):    passdef load_students():    try:        with DATA_FILE.open("r", encoding="utf-8") as file:            data = json.load(file)    except FileNotFoundError:        return []    except json.JSONDecodeError as error:        logging.exception("Student JSON corrupt hai.")        raise ValueError("Student data file invalid hai.") from error    except OSError as error:        logging.exception("Student file read nahi hui.")        raise RuntimeError("Student data read nahi ho saka.") from error    if not isinstance(data, list):        raise ValueError("Student data list honi chahiye.")    return datadef save_students(students):    try:        with DATA_FILE.open("w", encoding="utf-8") as file:            json.dump(students, file, indent=4)    except OSError as error:        logging.exception("Student data save nahi hua.")        raise RuntimeError("Student data save nahi ho saka.") from errordef add_student(student_id, name):    student_id = student_id.strip()    name = name.strip()    if not student_id or not name:        raise ValueError("Student ID aur name lazmi hain.")    students = load_students()    if any(s.get("id") == student_id for s in students):        raise DuplicateStudentError("Student ID pehle se mojood hai.")    students.append({        "id": student_id,        "name": name    })    save_students(students)def main():    try:        student_id = input("Student ID: ")        name = input("Student name: ")        add_student(student_id, name)        print("Student successfully add ho gaya.")    except (ValueError, DuplicateStudentError) as error:        print("Validation error:", error)    except RuntimeError as error:        print("Storage error:", error)    except KeyboardInterrupt:        print("\nProgram cancel kar diya gaya.")if __name__ == "__main__":    main()
```

Is starter project mein `load_students()`, `save_students()` aur `add_student()` functions exception handling ka practical use dikhate hain. Production system ke liye update, delete, record-level schema validation, atomic file writes aur comprehensive unit tests bhi add karne honge.

## 21. Apni understanding test karein

## Exception Handling Quiz

0/5 answered

1\. Agar int('abc') execute karein to kaunsi exception aayegi?

TypeError

ValueError

IndexError

2\. Kaunsa block try mein exception na aane par execute hota hai?

except

finally

else

3\. Original exception ko cause ke taur par preserve karne ka tareeqa kya hai?

raise from error

print(error)

assert error

4\. File ko safely close karne ka preferred tareeqa kya hai?

Bare except

with statement

Har jagah raise

5\. Production code mein input validation ke liye kis par depend nahi karna chahiye?

Explicit if checks

ValueError

assert

Check Answers

## 22. Basic se advanced tak learning roadmap

1. Beginner: `try`, `except`, `else`, `finally`, `raise` aur common built-in exceptions.
2. Intermediate: Multiple exceptions, exception hierarchy, nested handling, file handling aur JSON errors.
3. Advanced: Custom exceptions, exception chaining, traceback, logging aur context managers.
4. Professional: Unit testing, `assertRaises`, `assertLogs`, atomic file operations aur application-level error handling.
5. Expert practice: Student Record Management System mein CRUD operations, validation, corrupt JSON recovery aur automated failure tests.

Meri recommendation: Pehle `try-except-else-finally` ko achhi tarah samjhein, phir `raise` aur custom exceptions practice karein. Uske baad file/JSON handling aur testing ko ek complete project mein combine karein. Is tarah aap sirf syntax nahi, balkay real applications mein errors handle karna bhi seekhenge.&#x20;