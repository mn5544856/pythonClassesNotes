# Python File Handling — Basic se Advanced, Exception Handling ke saath

Python mein File Handling ka matlab hai files ko create, read, write, update, delete aur manage karna. Real-world applications mein logs, configuration files, CSV reports, JSON data, user records aur large files handle karne ke liye yeh essential skill hai.

Hum isay step-by-step seekhenge: har concept ke saath code, output, exceptions aur practical examples.

## 1. File handling ka basic concept

Python mein file handle karne ka main function `open()` hai.

```
file = open("data.txt", "r")content = file.read()print(content)file.close()
```

`open()` file kholta hai, `read()` content parhta hai aur `close()` file band karta hai.

Lekin professional code mein file ko manually close karna bhool sakte hain. Isliye hum zyada tar `with open()` use karenge.

```
with open("data.txt", "r") as file:    content = file.read()    print(content)
```

`with` block se bahar nikalte hi file automatically close ho jati hai, chahe exception hi kyun na aa jaye.

## 2. File modes — kaunsa mode kab use hota hai?

| Mode            | Kaam                                 | File na ho to                       |
| --------------- | ------------------------------------ | ----------------------------------- |
| `"r"`           | Read karna                           | `FileNotFoundError`                 |
| `"w"`           | Write; purana content erase          | Nayi file ban jati hai              |
| `"a"`           | End mein content add karna           | Nayi file ban jati hai              |
| `"x"`           | Sirf nayi file create karna          | Existing file par `FileExistsError` |
| `"r+"`          | Read aur write                       | `FileNotFoundError`                 |
| `"w+"`          | Read aur write, purana content erase | Nayi file ban jati hai              |
| `"a+"`          | Read aur append                      | Nayi file ban jati hai              |
| `"rb"` / `"wb"` | Binary data read/write               | Mode ke mutabiq                     |

Important: `"w"` mode existing file ka content delete kar deta hai. Agar existing content preserve karna hai to `"a"` use karein.

## 3. File create aur write karna

Example 1 — Basic write

```
with open("student.txt", "w", encoding="utf-8") as file:    file.write("Name: Ali\n")    file.write("Age: 22\n")    file.write("Course: Python\n")
```

Is se `student.txt` file create hogi aur teen lines save hongi.

`write()` string ko file mein likhta hai. Yeh automatically newline add nahi karta, isliye `\n` use kiya hai.

Example 2 — Multiple lines

```
students = [    "Ali",    "Ahmed",    "Sara"]with open("students.txt", "w", encoding="utf-8") as file:    file.writelines(name + "\n" for name in students)
```

`writelines()` multiple strings likhta hai, magar newline automatically nahi lagata.

## 4. File read karne ke tareeqe

Maan lein `student.txt` mein yeh content hai:

```
Name: Ali
Age: 22
Course: Python
```

### A. `read()` — poori file

```
with open("student.txt", "r", encoding="utf-8") as file:    print(file.read())
```

### B. `readline()` — ek line

```
with open("student.txt", "r", encoding="utf-8") as file:    print(file.readline())    print(file.readline())
```

### C. `readlines()` — lines ki list

```
with open("student.txt", "r", encoding="utf-8") as file:    lines = file.readlines()    print(lines)
```

Output: `['Name: Ali\\n', 'Age: 22\\n', 'Course: Python\\n']`

### D. Loop — memory-efficient reading

```
with open("student.txt", encoding="utf-8") as file:    for line in file:        print(line.rstrip())
```

Badi files ke liye line-by-line iteration aam tor par `read()` se behtar hai, kyunki poori file ek saath memory mein load nahi hoti.

## 5. Exception handling — file handling ka sabse important part

File operations fail ho sakti hain. Misal ke taur par file exist nahi karti, permission nahi hai, disk full hai ya file ka data expected format mein nahi hai.

Python mein exceptions handle karne ke liye `try`, `except`, `else` aur `finally` use hote hain.

### Basic syntax

```
try:    # Risky operation    passexcept FileNotFoundError:    # File nahi mili    passexcept PermissionError:    # Permission nahi hai    passexcept OSError as error:    # Other operating-system errors    print(error)else:    # Sirf jab exception na aaye    passfinally:    # Har haal mein execute hota hai    pass
```

Inka role samjhein:

- `try`: Woh code jahan exception aa sakti hai.
- `except`: Specific exception ko handle karta hai.
- `else`: Sirf tab execute hota hai jab `try` successful ho.
- `finally`: Cleanup ke liye; success aur failure dono mein execute hota hai.

### Example 1 — File missing ho to crash na ho

```
try:    with open("missing.txt", "r", encoding="utf-8") as file:        content = file.read()except FileNotFoundError:    print("Error: File nahi mili.")except PermissionError:    print("Error: File access ki permission nahi.")except OSError as error:    print(f"Operating system error: {error}")else:    print("File successfully read hui.")    print(content)finally:    print("File operation complete.")
```

Agar `missing.txt` maujood nahi hai to program ko traceback ke saath terminate karne ke bajaye expected message milega.

Professional rule: Hamesha mumkin ho to specific exceptions handle karein. `except Exception:` ya khaas taur par bare `except:` se har error ko chupana debugging ko mushkil bana sakta hai.

### Example 2 — Write operation with exception handling

```
try:    with open("report.txt", "w", encoding="utf-8") as file:        file.write("Monthly report\n")        file.write("Revenue: 5000\n")except PermissionError:    print("Write permission nahi hai.")except OSError as error:    print(f"File write failed: {error}")else:    print("Report successfully save ho gayi.")
```

Yaad rakhein: `with` file close kar deta hai, lekin woh write operation ko automatically successful nahi banata. Agar disk ya filesystem error ho, exception phir bhi aa sakti hai.

### Example 3 — `finally` ka real use

```
file = Nonetry:    file = open("data.txt", "r", encoding="utf-8")    print(file.read())except OSError as error:    print(f"Error: {error}")finally:    if file is not None:        file.close()
```

Yeh manually opened file ko close karta hai. Lekin normal file handling mein `with open()` behtar hai aur aam tor par is manual cleanup ki zaroorat nahi hoti.

## 6. Append aur file update karna

### Append — purana data preserve karna

```
try:    with open("log.txt", "a", encoding="utf-8") as file:        file.write("Application started\n")except OSError as error:    print(f"Log write failed: {error}")
```

Har baar program chalane par nayi line end mein add hogi.

### Existing file ka content update karna

Agar sirf ek word replace karna ho, to file read karke updated content write kar sakte hain.

```
from pathlib import Pathpath = Path("student.txt")try:    content = path.read_text(encoding="utf-8")    updated_content = content.replace("Ali", "Ahmed")    path.write_text(updated_content, encoding="utf-8")except FileNotFoundError:    print("Student file nahi mili.")except PermissionError:    print("File access denied.")except OSError as error:    print(f"Update failed: {error}")
```

Caution: Yeh poori file memory mein load karta hai. Chhoti text files ke liye theek hai; bohat badi files ke liye streaming ya temporary-file strategy use karein.

## 7. File pointer: `tell()` aur `seek()`

File pointer batata hai ke read/write position kahan hai.

```
with open("data.txt", "r", encoding="utf-8") as file:    print(file.tell())  # Initial position    print(file.read(5))  # Pehle 5 characters    print(file.tell())  # Current position    file.seek(0)  # Beginning par wapas    print(file.read(5))
```

- `tell()` current position deta hai.
- `seek(0)` beginning par le jata hai.

Text files mein Unicode aur encoding ki wajah se pointer ko har arbitrary character offset par set karna simple byte indexing jaisa nahi hota. Binary files mein offsets bytes ke hisaab se hote hain.

## 8. `pathlib` — modern file management

Python mein file paths manage karne ke liye `pathlib.Path` ek clean, cross-platform approach hai.

```
from pathlib import Pathpath = Path("data") / "student.txt"try:    path.parent.mkdir(parents=True, exist_ok=True)    path.write_text(        "Name: Ali\nAge: 22\n",        encoding="utf-8"    )    content = path.read_text(encoding="utf-8")    print(content)except OSError as error:    print(f"File operation failed: {error}")
```

Is code mein:

- `Path("data") / "student.txt"` path banata hai.
- `mkdir()` parent directory create karta hai.
- `exist_ok=True` existing directory par error se bachata hai.
- `write_text()` aur `read_text()` text operations simplify karte hain.

### File exists, rename, delete

```
from pathlib import Pathpath = Path("student.txt")try:    if path.exists() and path.is_file():        print("File exists.")        path.rename("student_backup.txt")except OSError as error:    print(f"File operation failed: {error}")
```

File delete karne ke liye:

```
from pathlib import Pathpath = Path("old_data.txt")try:    path.unlink(missing_ok=True)    print("Delete operation complete.")except OSError as error:    print(f"Delete failed: {error}")
```

`unlink()` file ko delete karta hai. `missing_ok=True` ka matlab file pehle se missing ho to `FileNotFoundError` raise nahi hoga. Directory delete karne ke liye alag methods hote hain.

## 9. Binary files — images, PDFs aur other files

Text files mein strings handle hoti hain. Binary files mein bytes handle hoti hain, isliye `"rb"` aur `"wb"` modes use hote hain.

```
try:    with open("source.pdf", "rb") as source:        data = source.read()    with open("copy.pdf", "wb") as destination:        destination.write(data)except FileNotFoundError:    print("Source PDF nahi mili.")except OSError as error:    print(f"Copy failed: {error}")
```

Yeh PDF ki byte content copy karta hai. Large files ke liye poori file memory mein load na karein:

```
def copy_file(source_path, destination_path):    try:        with open(source_path, "rb") as source:            with open(destination_path, "wb") as destination:                while True:                    chunk = source.read(64 * 1024)                    if not chunk:                        break                    destination.write(chunk)    except OSError as error:        print(f"Copy failed: {error}")        return False    return Truesuccess = copy_file("source.pdf", "copy.pdf")print("Success:", success)
```

Yeh 64 KiB chunks mein file copy karta hai, isliye memory usage large files ke liye controlled rehta hai.

## 10. JSON file handling — real-world data storage

JSON configuration aur structured records save karne ka common format hai.

```
import jsonstudent = {    "name": "Ali",    "age": 22,    "skills": ["Python", "SQL"]}try:    with open("student.json", "w", encoding="utf-8") as file:        json.dump(student, file, indent=4, ensure_ascii=False)except (OSError, TypeError, ValueError) as error:    print(f"JSON save failed: {error}")
```

JSON read karna:

```
import jsontry:    with open("student.json", "r", encoding="utf-8") as file:        student = json.load(file)except FileNotFoundError:    print("JSON file nahi mili.")except json.JSONDecodeError as error:    print(f"Invalid JSON at line {error.lineno}: {error.msg}")except OSError as error:    print(f"File access failed: {error}")else:    print(student["name"])    print(student["skills"])
```

Important distinction:

- `FileNotFoundError`: file missing hai.
- `JSONDecodeError`: file read hui, lekin JSON syntax invalid hai.
- `TypeError`: data JSON mein serialize nahi ho sakta, jaise unsupported custom objects.

## 11. CSV file handling — spreadsheet data

CSV tab useful hai jab data rows aur columns mein ho.

```
import csvstudents = [    {"name": "Ali", "age": 22},    {"name": "Sara", "age": 24},]try:    with open(        "students.csv",        "w",        newline="",        encoding="utf-8"    ) as file:        writer = csv.DictWriter(            file,            fieldnames=["name", "age"]        )        writer.writeheader()        writer.writerows(students)except OSError as error:    print(f"CSV write failed: {error}")
```

CSV read karna:

```
import csvtry:    with open(        "students.csv",        "r",        newline="",        encoding="utf-8"    ) as file:        reader = csv.DictReader(file)        for row in reader:            print(row["name"], row["age"])except FileNotFoundError:    print("CSV file nahi mili.")except (OSError, csv.Error) as error:    print(f"CSV read failed: {error}")
```

CSV values aam tor par strings ke taur par read hoti hain. Agar `age` ko integer chahiye, to `int(row["age"])` use karein aur malformed values ke liye `ValueError` handle karein.

## 12. Advanced exception handling: custom exceptions

Jab application ki apni business rule violate ho, custom exception useful hoti hai.

```
from pathlib import Pathclass EmptyFileError(Exception):    """Raised when a required file is empty."""def read_required_file(filename):    path = Path(filename)    try:        content = path.read_text(encoding="utf-8")    except OSError as error:        raise RuntimeError(            f"Cannot read required file: {path}"        ) from error    if not content.strip():        raise EmptyFileError(f"{path} is empty")    return contenttry:    content = read_required_file("config.txt")    print(content)except EmptyFileError as error:    print(f"Validation error: {error}")except RuntimeError as error:    print(f"Application error: {error}")
```

Yahan teen important concepts hain:

- `EmptyFileError`: application-specific error.
- `raise`: khud exception raise karna.
- `raise ... from error`: original exception ko cause ke taur par preserve karna, taake debugging mein asal wajah nazar aaye.

`RuntimeError` yahan original `OSError` ko contextualize karta hai. Agar calling code ko file-specific errors par directly action lena ho, to custom exception ko `OSError` se inherit karwana ya original error ko propagate karna behtar design ho sakta hai.

## 13. Advanced: atomic file write

Agar program existing configuration file update kar raha hai aur write beech mein fail ho jaye, to file incomplete reh sakti hai. Ek common approach temporary file mein likh kar phir replace karna hai.

```
import jsonimport osimport tempfilefrom pathlib import Pathdef save_json_atomic(path, data):    path = Path(path)    temp_path = None    try:        with tempfile.NamedTemporaryFile(            mode="w",            encoding="utf-8",            dir=path.parent,            delete=False        ) as file:            temp_path = Path(file.name)            json.dump(data, file, indent=4)            file.flush()            os.fsync(file.fileno())        os.replace(temp_path, path)        temp_path = None    except (OSError, TypeError, ValueError) as error:        raise RuntimeError(            f"Could not save JSON to {path}"        ) from error    finally:        if temp_path is not None:            try:                temp_path.unlink(missing_ok=True)            except OSError:                pass
```

Example:

```
save_json_atomic(    Path("config.json"),    {"theme": "dark", "version": 1})
```

Is approach ke faide:

- Temporary file mein data pehle complete hota hai.
- `os.replace()` destination ko replace karta hai; same filesystem par replacement aam tor par atomic hoti hai.
- `finally` failed write ke baad temporary file clean karne ki koshish karta hai.

Yeh complete crash-proof transaction ya har platform par full durability guarantee nahi hai. Permissions, filesystem behavior aur concurrent writers ko production system mein alag se consider karna chahiye.

## 14. Production-level best practices

1\. Bare `except` avoid karein

`except:` ya unnecessary `except Exception:` se programming errors chhup sakte hain. Expected exceptions ko specifically catch karein.

2\. `with open()` prefer karein

Is se file cleanup automatic hota hai, including exceptional exits.

3\. Large files ko stream karein

`for line in file` ya chunk-based reads use karein, taake memory usage controlled rahe.

4\. File paths aur permissions validate karein

User-provided paths ko blindly trust na karein. Sensitive files ko overwrite ya delete karne se pehle access aur destination verify karein.

5\. Errors ko log karein

Production applications mein `print()` ke bajaye `logging` use karein, taake errors ke timestamps aur stack traces record ho saken.

## 15. Exception handling quick reference

| Exception              | Kab aati hai?                                                            |
| ---------------------- | ------------------------------------------------------------------------ |
| `FileNotFoundError`    | File ya path nahi milta                                                  |
| `PermissionError`      | Access ki permission nahi                                                |
| `IsADirectoryError`    | File ki jagah directory open karne ki koshish                            |
| `FileExistsError`      | Exclusive create mode `"x"` mein file pehle se maujood                   |
| `NotADirectoryError`   | Path ke kisi component ko directory hona chahiye tha, lekin woh nahi hai |
| `UnicodeDecodeError`   | Text decode karte waqt encoding mismatch ya invalid bytes                |
| `json.JSONDecodeError` | JSON syntax invalid                                                      |
| `csv.Error`            | CSV parsing ya writing error                                             |
| `OSError`              | Operating system ya filesystem operation fail                            |

Note: `FileNotFoundError`, `PermissionError` aur `IsADirectoryError` `OSError` ki subclasses hain. Agar aap pehle broad `OSError` catch kar lein, to baad ke specific handlers execute nahi honge.

## 16. Practice roadmap — basic se advanced

## Your practice checklist

0/8 complete

1\. Basic write/read

File create karein, 3 lines write karein aur phir read karein.

2\. Exception handling

Missing file read karke FileNotFoundError handle karein.

3\. Append and search

Log mein entries append karein aur specific word search karein.

4\. Path management

Directory create, file rename aur safely delete karein.

5\. JSON CRUD

Student records ko JSON mein save, read, update aur delete karein.

6\. CSV processing

CSV se records read karein aur invalid numeric values handle karein.

7\. Large file copying

Binary file ko chunks mein copy karein aur failures handle karein.

8\. Atomic writes

Temporary file aur os.replace() ke zariye safer updates implement karein.

## Ab agla lesson kaunsa karein?

Ek option select karein; us topic ko code, output, exercises aur exception handling ke saath detail mein cover kar sakte hain.

Level 1 — File handling fundamentals aur modes

Level 2 — `try/except/else/finally`, `raise` aur custom exceptions

Level 3 — JSON, CSV aur CRUD operations

Level 4 — Complete practical project: Student Record Management System

Level 5 — Production-grade file handling, logging aur atomic writes

Start selected lesson

# Python Student Record Management System — Complete Project

Is project mein hum ek practical Python application banayenge jo students ka data JSON file mein permanently save karegi. Aap isay terminal se run kar sakenge aur students ko add, view, search, update aur delete kar sakenge.

Project ka focus sirf code likhna nahi, balki professional file handling, data validation, exception handling, clean functions aur automated testing samajhna hai.

## 1. Project mein kya banega?

## Student Record Manager

Python · pathlib · JSON · unittest

Student records ko manage karne wali command-line application.

Create

Naya student add karna

Read

Records dekhna aur search

Update

Student information edit

Delete

Record remove karna

Hum yeh rules bhi implement karenge:

- Student ID unique honi chahiye.
- Name empty nahi ho sakta.
- Age 1 se 120 ke darmiyan integer honi chahiye.
- Marks 0 se 100 ke darmiyan honge.
- Invalid JSON, missing file aur file-system errors ko alag handle karenge.
- Automated tests se confirm karenge ke CRUD operations theek kaam karte hain.

## 2. Project structure

Apne computer par `student_manager` naam ka folder banayein.

```
student_manager/
│
├── main.py
├── student_manager.py
├── test_student_manager.py
│
└── data/
    └── students.json
```

Har file ka purpose:

| File                      | Purpose                       |
| ------------------------- | ----------------------------- |
| `main.py`                 | User menu aur input/output    |
| `student_manager.py`      | Business logic, JSON aur CRUD |
| `test_student_manager.py` | Automated unit tests          |
| `data/students.json`      | Permanent student records     |

`students.json` ko pehle manually banana zaroori nahi hai. Application khud create karegi.

## 3. Step 1 — Data model aur validation

Har student ka record is tarah store hoga:

```
{
    "id": "S001",
    "name": "Ali Khan",
    "age": 21,
    "course": "Python",
    "marks": 88.5
}
```

Hum `id` ko string rakhenge, taake `S001` jaisi IDs preserve rahen. Marks decimal ho sakte hain, jabke age integer honi chahiye.

Validation ka matlab hai data save karne se pehle check karna ke woh expected rules ko satisfy karta hai.

Misal ke taur par:

```
def validate_age(age):    if isinstance(age, bool) or not isinstance(age, int):        raise ValueError("Age must be an integer.")    if not 1 <= age <= 120:        raise ValueError("Age must be between 1 and 120.")
```

Yahan `isinstance(age, bool)` ka check important hai, kyunki Python mein `bool`, `int` ki subclass hai. Is check ke baghair `True` ko age `1` samjha ja sakta hai.

Ab isi concept ko poore project mein use karenge.

## 4. Step 2 — `student_manager.py` complete code

Yeh project ki main file hai. Is mein data validation, custom exceptions, file handling aur tamam CRUD functions honge.

`student_manager.py` file banayein aur yeh code paste karein:

```
import jsonimport mathimport osimport tempfilefrom pathlib import Path# ---------- Project paths ----------BASE_DIR = Path(__file__).resolve().parentDATA_DIR = BASE_DIR / "data"DATA_FILE = DATA_DIR / "students.json"# ---------- Custom exceptions ----------class StudentManagerError(Exception):    """Base exception for the student manager."""class StudentNotFoundError(StudentManagerError):    """Raised when a student does not exist."""class DuplicateStudentError(StudentManagerError):    """Raised when a student ID already exists."""class DataCorruptionError(StudentManagerError):    """Raised when stored JSON data is invalid."""# ---------- Validation ----------def validate_student(student):
```

### Is code ke important concepts

`pathlib.Path`

`Path(__file__).resolve().parent` current Python file ka actual directory locate karta hai. Isliye application kisi aur working directory se run ho tab bhi data path stable rehta hai.

Custom exceptions

`StudentNotFoundError` aur `DuplicateStudentError` business-rule failures ko clearly identify karte hain. `DataCorruptionError` batata hai ke saved data invalid hai.

`load_students()`

File read karne ke saath JSON syntax, record structure, field types aur duplicate IDs validate karta hai. Corrupt data ko silently empty list mein convert nahi karta.

`save_students()`

Data pehle temporary file mein likhta hai aur phir `os.replace()` se destination replace karta hai. Is se incomplete write ke wajah se purani file damage hone ka risk kam hota hai.

Ek zaroori limitation: Atomic replacement write failures ke khilaf protection deta hai, lekin yeh multi-process database transaction nahi hai. Do processes ek hi waqt par records modify karein to updates overwrite ho sakti hain. Concurrent users ke liye SQLite ya proper database behtar hoga.

## 5. Step 3 — `main.py`: User interface

Ab hum terminal menu banayenge. User options select karega aur program relevant CRUD function call karega.

`main.py` file mein yeh code likhein:

```
from student_manager import (    add_student,    get_all_students,    get_student,    update_student,    delete_student,    StudentManagerError,    StudentNotFoundError,    DuplicateStudentError,    DataCorruptionError,)def input_student():    """Collect and convert user input."""    student_id = input("Student ID: ").strip()    name = input("Name: ").strip()    try:        age = int(input("Age: ").strip())        marks = float(input("Marks (0-100): ").strip())    except ValueError as error:        raise ValueError(            "Age must be an integer and marks must be numeric."        ) from error    course = input("Course: ").strip()    return {        "id": student_id,        "name": name,        "age": age,        "course": course,
```

### `if __name__ == "__main__":` kyun use kiya?

```
if __name__ == "__main__":    main()
```

Iska matlab hai `main()` tab chale jab aap `main.py` ko directly run karein. Jab automated tests `main.py` ya doosre modules import karte hain, to menu automatically start nahi hota.

### Exception handling ka flow

\#chatgpt-mermaid-\_r_69l\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI","Helvetica","Apple Color Emoji","Arial",sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(237, 237, 237);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_69l\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_69l\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_69l\_ .error-icon{fill:rgb(48, 48, 48);}#chatgpt-mermaid-\_r_69l\_ .error-text{fill:rgb(237, 237, 237);stroke:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_69l\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_69l\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_69l\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_69l\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_69l\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_69l\_ .marker.cross{stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_69l\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI","Helvetica","Apple Color Emoji","Arial",sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_69l\_ p{margin:0;}#chatgpt-mermaid-\_r_69l\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI","Helvetica","Apple Color Emoji","Arial",sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ .cluster-label text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ .cluster-label span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_69l\_ .label text,#chatgpt-mermaid-\_r_69l\_ span{fill:rgb(237, 237, 237);color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ .node rect,#chatgpt-mermaid-\_r_69l\_ .node circle,#chatgpt-mermaid-\_r_69l\_ .node ellipse,#chatgpt-mermaid-\_r_69l\_ .node polygon,#chatgpt-mermaid-\_r_69l\_ .node path{fill:rgb(9, 23, 44);stroke:rgb(31, 78, 148);stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .rough-node .label text,#chatgpt-mermaid-\_r_69l\_ .node .label text,#chatgpt-mermaid-\_r_69l\_ .image-shape .label,#chatgpt-mermaid-\_r_69l\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_69l\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .rough-node .label,#chatgpt-mermaid-\_r_69l\_ .node .label,#chatgpt-mermaid-\_r_69l\_ .image-shape .label,#chatgpt-mermaid-\_r_69l\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_69l\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_69l\_ .root .anchor path{fill:rgb(175, 175, 175)!important;stroke-width:0;stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_69l\_ .arrowheadPath{fill:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_69l\_ .edgePath .path{stroke:rgb(175, 175, 175);stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .flowchart-link{stroke:rgb(175, 175, 175);fill:none;}#chatgpt-mermaid-\_r_69l\_ .edgeLabel{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_69l\_ .edgeLabel p{background-color:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_69l\_ .edgeLabel rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_69l\_ .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#chatgpt-mermaid-\_r_69l\_ .cluster rect{fill:rgb(48, 48, 48);stroke:rgba(255, 255, 255, 0.15);stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .cluster text{fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ .cluster span{color:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI","Helvetica","Apple Color Emoji","Arial",sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(48, 48, 48);border:1px solid rgba(255, 255, 255, 0.15);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_69l\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(237, 237, 237);}#chatgpt-mermaid-\_r_69l\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_69l\_ .icon-shape,#chatgpt-mermaid-\_r_69l\_ .image-shape{background-color:rgb(0, 0, 0);text-align:center;}#chatgpt-mermaid-\_r_69l\_ .icon-shape p,#chatgpt-mermaid-\_r_69l\_ .image-shape p{background-color:rgb(0, 0, 0);padding:2px;}#chatgpt-mermaid-\_r_69l\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_69l\_ .image-shape .label rect{opacity:0.5;background-color:rgb(0, 0, 0);fill:rgb(0, 0, 0);}#chatgpt-mermaid-\_r_69l\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_69l\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_69l\_ .node .neo-node{stroke:rgb(31, 78, 148);}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_69l\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_69l\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node .neo-line path{stroke:rgb(31, 78, 148);filter:none;}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_69l\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_69l\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_69l\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_69l\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_69l\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_69l\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(153, 206, 255);}#chatgpt-mermaid-\_r_69l\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_69l\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_69l\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .node rect,#chatgpt-mermaid-\_r_69l\_ .node circle,#chatgpt-mermaid-\_r_69l\_ .node ellipse,#chatgpt-mermaid-\_r_69l\_ .node polygon,#chatgpt-mermaid-\_r_69l\_ .node path{fill:rgb(0, 40, 77);stroke:rgba(255, 255, 255, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_69l\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_69l\_ .node.mermaid-decision .label-container{fill:rgb(0, 14, 26);stroke:rgb(26, 62, 95);stroke-dasharray:2px,2px;}#chatgpt-mermaid-\_r_69l\_ .edgePaths .flowchart-link{stroke:rgb(175, 175, 175);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_69l\_ .marker{fill:rgb(175, 175, 175);stroke:rgb(175, 175, 175);}#chatgpt-mermaid-\_r_69l\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI","Helvetica","Apple Color Emoji","Arial",sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}User selects menu optionInput collectionValidationCRUD functionOperation successful?Success messageException typeValueError: invalid inputStudentNotFoundErrorDuplicateStudentErrorFile or data errorReturn to menuYesNo

Is design ka faida yeh hai ke ek student ka invalid input poore program ko terminate nahi karta. Error display hota hai aur menu dobara show hota hai.

## 6. Step 4 — `test_student_manager.py`: Automated testing

Professional project mein sirf yeh check karna kaafi nahi ke program ek baar chal gaya. Humein test karna chahiye ke duplicate IDs reject hoti hain, invalid age accept nahi hoti, missing student par sahi exception aati hai aur JSON file corrupt hone par error properly report hota hai.

Python ka built-in `unittest` framework use karenge; extra package install karne ki zaroorat nahi.

`test_student_manager.py` mein yeh code likhein:

```
import jsonimport tempfileimport unittestfrom pathlib import Pathfrom unittest.mock import patchimport student_manager as smclass StudentManagerTests(unittest.TestCase):    def setUp(self):        # Each test gets its own temporary data directory.        self.temp_dir = tempfile.TemporaryDirectory()        self.data_dir = Path(self.temp_dir.name)        self.data_file = self.data_dir / "students.json"        self.dir_patch = patch.object(            sm, "DATA_DIR", self.data_dir        )        self.file_patch = patch.object(            sm, "DATA_FILE", self.data_file        )        self.dir_patch.start()        self.file_patch.start()        self.addCleanup(self.dir_patch.stop)        self.addCleanup(self.file_patch.stop)        self.addCleanup(self.temp_dir.cleanup)        self.student = {            "id": "S001",            "name": "Ali Khan",            "age": 21,
```

### Tests kaise run karne hain?

Terminal ya Command Prompt mein project folder open karein aur yeh command run karein:

```
python -m unittest -v test_student_manager.py
```

Agar aapke system par `python` command available nahi hai, Windows par `py -m unittest -v test_student_manager.py` bhi try kar sakte hain.

Successful run mein har test ke saamne `ok` aur end mein `OK` nazar aayega. Total 8 tests execute hone chahiye.

Test coverage

- Create aur read
- Duplicate ID
- Invalid age aur Boolean age
- Update aur delete
- Missing student
- Corrupt JSON
- File se data dobara load karna

Tests temporary directory use karte hain. Isliye test run karne se aapki real project wali `data/students.json` file modify nahi honi chahiye.

## 7. Step 5 — Project run karein

Project folder mein terminal open karein:

```
python main.py
```

Aapko is tarah ka menu nazar aayega:

```
========== STUDENT MANAGER ==========

1. Add student
2. View all students
3. Search student
4. Update student
5. Delete student
0. Exit

Choose an option:
```

### Example: Naya student add karna

Option `1` select karein:

```
Choose an option: 1
Student ID: S001
Name: Ali Khan
Age: 21
Marks (0-100): 88.5
Course: Python

Student S001 successfully added.
```

Application `data/students.json` mein data save kar degi. File ka content kuch is tarah hoga:

```
[
    {
        "id": "S001",
        "name": "Ali Khan",
        "age": 21,
        "course": "Python",
        "marks": 88.5
    }
]
```

Program close karke dobara run karein. Record phir bhi available hoga, kyunki data memory ke bajaye JSON file mein save kiya gaya hai.

### Example: Update aur delete

- Option `4` select karein, ID `S001` dein, phir marks update karne ke liye option `4` select karein aur `95` enter karein.
- Option `5` select karein, ID `S001` dein aur confirmation ke liye `yes` enter karein.
- Option `2` se verify karein ke record update ya delete ho gaya hai.

## 8. Error-handling checklist

| Scenario                | Expected behavior                                                            |
| ----------------------- | ---------------------------------------------------------------------------- |
| Duplicate ID            | `DuplicateStudentError`                                                      |
| Student nahi mila       | `StudentNotFoundError`                                                       |
| Age `150`               | `ValueError`                                                                 |
| Age `True`              | `ValueError`                                                                 |
| Marks `-10` ya `101`    | `ValueError`                                                                 |
| JSON syntax invalid     | `DataCorruptionError`                                                        |
| File read/write failure | `StudentManagerError`, ya directory creation ki kuch failures mein `OSError` |
| Invalid menu option     | Error message aur menu dobara                                                |

Ek chhoti production improvement: `main.py` ke `try` block ke baad ek additional handler add karein, taake directory creation jaise raw operating-system errors bhi user ko readable message dein:

```
        except OSError as error:            print(f"Filesystem error: {error}")
```

Yeh handler `main()` ke existing `except` blocks ke andar, unke saath hi hona chahiye. Is se unexpected file-system failures par application ke achanak terminate hone ka risk kam hota hai.

## 9. Project se aapne kya seekha?

### Concepts mastered

File handling

open(), with, read, write aur JSON persistence

Path management

pathlib, directory creation aur portable paths

CRUD

Create, Read, Update aur Delete

Validation

Types, ranges, required fields aur unique IDs

Exception handling

Specific exceptions, custom exceptions aur exception chaining

Safer writes

Temporary files, flush, fsync aur os.replace

Testing

unittest, assertRaises, fixtures aur isolated test data

Agla professional step: Is project ko aur robust banane ke liye logging, pagination, sorting, search by course, backup/restore, CLI argument parsing aur SQLite migration add ki ja sakti hai. JSON-based version single-user ya learning project ke liye achha hai; multiple concurrent users aur transactional data ke liye SQLite ya server database zyada munasib hoga.