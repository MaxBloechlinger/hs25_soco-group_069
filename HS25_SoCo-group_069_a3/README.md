# HS25 SoCo Assignment 3 Group 69: ZVFS File System

**Members:** Max Blöchlinger, Abraham Herzog, Luiz Hablützel

## Content

- **zvfs.py**
  [Step01]
  Implementation of 8 file system commands with support in terminal demonstrated in filesystem1.zvfs
- **zvfs.java**
  [Step02]
  Previous python implementation of the zvfs file system translated into java demonstrated in filesystem2.zvfs

## Step01 Python filesystem1.zvfs

Here we will show the exact demonstration requested by Step01 of the Assignment thereby completely fullfilling the assigned task. 
A more thorough documentation can be found [here](#python-operations) for python and [here](#java-operations) for Java.

_Run these following lines in your terminal:_

---

### 1. Create a new filesystem
**Command:**
```bash
python zvfs.py mkfs filesystem1.zvfs
```

**Output:**
```

```

---

### 2. Create two test files
**Command:**
```bash
echo Hello, world! > test_file1.txt
echo The weather is nice today > test_file2.txt
```

**No Output**

---

### 3. Add both files to the filesystem
**Command:**
```bash
python zvfs.py addfs filesystem1.zvfs test_file1.txt
python zvfs.py addfs filesystem1.zvfs test_file2.txt
```

**Output:**
```

```

---

### 4. List all filesystem files
**Command:**
```bash
python zvfs.py lsfs filesystem1.zvfs
```

**Output:**
```

```

---

### 5. Print contents of test_file1.txt
**Command:**
```bash
python zvfs.py catfs filesystem1.zvfs test_file1.txt
```

**Output:**
```

```

---

### 6. Delete test_file1.txt from disk and restore it
**Command:**
```bash
rm test_file1.txt
python zvfs.py getfs filesystem1.zvfs test_file1.txt
```

**Output:**
```

```

---

### 7. Show filesystem information
**Command:**
```bash
python zvfs.py gifs filesystem1.zvfs
```

**Output:**
```

```

---

### 8. Delete test_file1.txt inside the filesystem & show results
**Command:**
```bash
python zvfs.py rmfs filesystem1.zvfs test_file1.txt
python zvfs.py gifs filesystem1.zvfs
python zvfs.py lsfs filesystem1.zvfs
```

**Output:**
```

```

---

### 9. Defragment filesystem & show results
**Command:**
```bash
python zvfs.py dfrgfs filesystem1.zvfs
python zvfs.py gifs filesystem1.zvfs
python zvfs.py lsfs filesystem1.zvfs
```

**Output:**
```

```

Note, if you want to run these operations in java you simply have to replace the python command in the beginning and omit the .py suffix:

--> `java zvfs mkfs filesystem1.zvfs` to create a new filesystem in java

## Step02 Python filesystem2.zvfs

Here we will show the exact demonstration requested by Step02 of the Assignment thereby completely fullfilling the assigned task. 
A more thorough documentation can be found [here](#python-operations) for python and [here](#java-operations) for Java.

_Run these following lines in your terminal:_

### 0. Compile the zvfs.java file [already done]
**Command:**
```bash
javac zvfs.java
```

### 1. Create a new filesystem
**Command:**
```bash
java zvfs mkfs filesystem2.zvfs
```

**Output:**
```

```

---

### 2. Create two test files
**Command:**
```bash
echo Hello, world! > test_file1.txt
echo The weather is nice today > test_file2.txt
```

**No Output**

---

### 3. Add both files to the filesystem
**Command:**
```bash
java zvfs addfs filesystem2.zvfs test_file1.txt
java zvfs addfs filesystem2.zvfs test_file2.txt
```

**Output:**
```

```

---

### 4. List all filesystem files
**Command:**
```bash
java zvfs lsfs filesystem2.zvfs
```

**Output:**
```

```

---

### 5. Print contents of test_file1.txt
**Command:**
```bash
java zvfs catfs filesystem2.zvfs test_file1.txt
```

**Output:**
```

```

---

### 6. Delete test_file1.txt from disk and restore it
**Command:**
```bash
rm test_file1.txt
java zvfs getfs filesystem2.zvfs test_file1.txt
```

**Output:**
```

```

---

### 7. Show filesystem information
**Command:**
```bash
java zvfs gifs filesystem2.zvfs
```

**Output:**
```

```

---

### 8. Delete test_file1.txt inside filesystem & show results
**Command:**
```bash
java zvfs rmfs filesystem2.zvfs test_file1.txt
java zvfs gifs filesystem2.zvfs
java zvfs lsfs filesystem2.zvfs
```

**Output:**
```

```

---

### 9. Defragment filesystem & show results
**Command:**
```bash
java zvfs dfrgfs filesystem2.zvfs
java zvfs gifs filesystem2.zvfs
java zvfs lsfs filesystem2.zvfs
```

**Output:**
```

```


## zvfs.py

### Design Decision for zvfs.py

Regarding the model design of the filesystem, i.e., header, number of files supported in each .zvfs file or length of every filename we adhered to the specifications of the asg03 pdf.

**Global Format Variables**

For the code we decided it would be good practice to create global variables for the Format variables and Size variables, this ensured consistency and avoids repetition since we can simply call the variables when they are required.

```
#Format Variables
HEADER_FORMAT = "<8sBBHHHHHIIIIH26s"
ENTRY_FORMAT = "<32sIIBBHQ12s"

#Size Variables
HEADER_SIZE = 64
ENTRY_SIZE = 64

```

**Helper Functions**

**def pack_header(...):**

- Takes as input all header metadata specified and uses `struct.pack` and the global `HEADER_FORMAT` to turn them into 64 bytes

**def unpack_header(...):**

- Extracts the 64 bytes using `struct.unpack()` and `HEADER_FORMAT` to turn them into a tuple of values

**def pack_empty_entry(...):**

- Creates a 64 byte file entry, for mkfs and dfrgfs

**Filesystem Loader - loadfs**

We decided that, instead of every function needing to unpack the header and read it, and scan for the necessary information each time, to centralise this functionality into one function. It essentially stores the information into a dictionary for each function to access their required information more easily instead of having to parse with each function through the header and unpack it.

## Python Operations

**def mkfs(...):**

- Creates a new filesystem
- Populates the header and fills out file entries with zero bytes for 32 entries
- Packs the header into byte format

Showcase of mkfs:

`python zvfs.py mkfs filesystem1.zvfs` --> **New file system 'filesystem1.zvfs' created.**

_There now should be a new filesystem in your working directory called filesystem1.zvfs_

**def gifs(...):**

- Returns: file name, number of files present (non deleted), remaining free entries for new files (excluding deleted files), and the number of files marked as deleted
- Opens the file and extracts necessary header data and calculates the remaining free entries

Showcase of gifs:

`python zvfs.py gifs filesystem1.zvfs`

```
The file system name is: filesystem1.zvfs
-------------------------------------
The number of files present is: 2
-------------------------------------
The remaining free entries are: 30
-------------------------------------
Number of files marked as deleted: 0
-------------------------------------
The total size of the file is: 2152
-------------------------------------
```

**def addfs(...):**

- Adds a file from the users directory to the filesystem
- Scans the filesystem for first free entry, _next_free_offset_ and inserts it there

Showcase of addfs:

_To showcase the usecase for this operation you first must add two files to your directory:_

```
echo Hello, world! > test_file1.txt
echo The weather is nice today > test_file2.txt
```

_Then we can call addfs:_

```
python zvfs.py addfs filesystem1.zvfs test_file1.txt
python zvfs.py addfs filesystem1.zvfs test_file2.txt
```

--> **Added 'test_file1.txt' (14 bytes) to filesystem1.zvfs**

--> **Added 'test_file2.txt' (26 bytes) to filesystem1.zvfs**

_Now both .txt files should be present in your newly created filesystem1.zvfs_

**def getfs(...):**

- Extracts a file from the filesystem to the users disk
- Locates the specified file by name

Showcase of getfs:

_To properly show the usecase of this operation we ask the user to first delete the file they wish to extract from their own directory:_

`rm test_file1.txt`

_And the you should be able to extract it from the created filesystem:_

`python zvfs.py getfs filesystem1.zvfs test_file1.txt`

_It should now have appeared back into your directory_

**def rmfs(...):**

- Locates the file it wants to delete in the filesystem
- Changes its flag byte from 0 to 1, however, the data is not deleted

Showcase of rmfs:

`python zvfs.py rmfs filesystem1.zvfs test_file1.txt`

_The file should now be deleted from the filesystem_

**def lsfs(...):**

- Lists all the files in the provided file system and for every file, print its name, size (in bytes) and creation time
- Iterates through file entries and sorts out relevant ones (non deleted files or empty files)

Showcase of lsfs:

`python zvfs.py lsfs filesystem1.zvfs`

```
filesystem1.zvfs:
-test_file1.txt [size: 14 bytes; created: 06.12.2025 14:44]
-test_file2.txt [size: 26 bytes; created: 06.12.2025 14:44]
```

**def dfrgfs(...):**

- Defragments the file system. This operation removes all files marked from deletion from the system, along with their respective file entries. Afterwards, it compacts the file entries and the file data (moves everything up to fill up the available space, so that no 64 byte block gaps exist)
- Loads all non-deleted files into memory and overwrites the filesystem with only relevant files

Showcase of dfrgfs:

`python zvfs.py dfrgfs filesystem1.zvfs` --> **Defragmentation complete: defragmented 1 file and freed 1 byte**

**def catfs(...):**

- Prints out the file contents of a specified file from the filesystem to the console
- Locates the file in the filesystem, extracts the relevant data and prints it directly to the console

Showcase of catfs:

`python zvfs.py catfs filesystem1.zvfs test_file1.txt` --> **Hello, world!**

## zvfs.java

### Challenges coming from Python

Starting off, translating our implementation from python to java was not as straightforward as we initially assumed it would be.

The biggest obstacle was coding in a completely new language. Java not being dynamically typed meant we had to refamiliarize ourselves with its strict syntax in a short time, read a lot of documentations to understand the key differences to python and truly understand the contrast. Learning the binary packing logic of java `ByteBuffer` and the `java.nio` package being among them. 

Knowing C made this drawback bearable since C also is statically typed meaning there was less confusion when it came to defining and initializing variables. 

All in all, the time and effort it took was larger by a significant margin. Since in Python, once the idea was understood, we could start coding more immediate than with Java. It still required understanding and research, however, with Java this time investment was compounded by us needing to invest more time into properly understanding Java as a language and reading/ summarizing its documentations.

### Design Decision for zvfs.java

For the Java implementation we mostly adhered to our python decisions. We used similar Helper Functions and implemented 3 classes for FileSystem, Header & Entry.

**Helper Classes**

**private static class FileSystem{...}**

- stores all the entries for the FileSystem Object
- Holds and decodes header data

**private static class Header{...}**

- stores all the entries for the Header Object

**private static class Entry{...}**

- stores all the entries for the Entry Object

*For these classes we used `byte[]` for strings and typical value declaration for numerical values `int`, `long`, `short`*

Filesystem Class for Example:

```
private static class FileSystem {
        Header header;
        Entry[] entries;
        byte[] data;
    }
```


**Helper Functions**

These act as specific packers and unpackers, stemming from the NIO *requirements*

- **private static byte[] packHeader(Header header)**
- Allocates 64 byte ByteBuffer
- Note that we implemented the LITTLE_ENDIAN `buffer.order(ByteOrder.LITTLE_ENDIAN)` here to ensure compatability with the python implementation

- **private static byte[] packEntry(Entry e)**
- Turns the Entry object into a 64 byte array.
- The filename will be put into the first 32 bytes and the rest will be initialized to 0

- **private static Header unpackHeader(byte[] packedHeader)**
- Converts the 64 bytes from the file back into a Header object

- **private static Entry unpackEntry(byte[] data)**
- Converts the 64 bytes from the file back into an Entry object ensuring easier access of the stored data like its name

## Java Operations

As a preface, to run these commands the user first has to compile the java code before running these operations:
`javac zvfs.java`

**static void mkfs(...):**

- Creates a new filesystem
- Populates the header and fills out file entries with zero bytes for 32 entries
- Packs the header into byte format
- Allocates an array of size 2112 bytes --> 64 (header) + 32 * 64 (entries)

Showcase of mkfs:

` java zvfs mkfs filesystem2.zvfs` --> **New file system filesystem2.zvfs created.**

_There now should be a new filesystem in your working directory called filesystem2.zvfs_

**static void gifs(...):**

- Returns: file name, number of files present (non deleted), remaining free entries for new files (excluding deleted files), and the number of files marked as deleted
- Opens the file and extracts necessary header data and calculates the the remaining free entries
- Uses `Files.size(Paths.get(fileSystemName))` to efficiently get the size of the file

Showcase of gifs:

`java zvfs gifs filesystem2.zvfs`

```
The file system name is: filesystem2.zvfs
-------------------------------------
The number of files present is: 0
-------------------------------------
The remaining entries are: 32
-------------------------------------
Number of deleted files marked as deleted: 0
-------------------------------------
The total size of the file is: 2112
-------------------------------------
```

**static void addfs(...):**

- Adds a file from from the users directory to the filesystem
- Scans the filesystem for first free entry, _next_free_offset_ and inserts it there
- Uses `System.currentTimeMillis() / 1000L;` for time concistency

Showcase of addfs:

_To showcase the usecase for this operation you first must add two files to your directory:_

```
echo Hello, world! > test_file3.txt
echo The weather is nice today > test_file4.txt
```

_Then we can call addfs:_

```
java zvfs addfs filesystem2.zvfs test_file3.txt
java zvfs addfs filesystem2.zvfs test_file4.txt
```

--> **Added 'test_file3.txt' (14 bytes) to filesystem2.zvfs**

--> **Added 'test_file4.txt' (26 bytes) to filesystem2.zvfs**

_Now both .txt files should be present in your newly created filesystem2.zvfs_

**static void getfs(...):** 

- Extracts a file from the filesystem to the users disk
- Locates the specified file by name

Showcase of getfs:

_To properly show the usecase of this operation we ask the user to first delete the file they wish to extract from their own directory:_

`rm test_file3.txt`

_And the you should be able to extract it from the created filesystem:_

`java zvfs getfs filesystem2.zvfs test_file3.txt` --> **Extracted 'test_file3.txt' (14 bytes) from filesystem2.zvfs**

_It should now have appeared back into your directory_

**static void rmfs(...):** 

- Locates the file it wants to delete in the filesystem
- Changes its flag byte from 0 to 1, however, the data is not deleted
- Uses **FileChannel** to *seek* only the specified file

Showcase of rmfs:

`java zvfs rmfs filesystem2.zvfs test_file3.txt` --> **This file has been deleted successfully: test_file3.txt**

_The file should now be deleted from the filesystem_

**static void lsfs(...):**

- Lists all the files in the provided file system and for every file, print its name, size (in bytes) and creation time
- Iterates through file entries and sorts out relevant ones (non deleted files or empty files)
- Skips through entries whos flag is set to 1 or length 0

Showcase of lsfs:

`java zvfs lsfs filesystem2.zvfs`

```
filesystem2.zvfs:
-test_file3.txt[size: 14 bytes; created: Sun Dec 07 16:45:19 CET 2025]
-test_file4.txt[size: 26 bytes; created: Sun Dec 07 16:45:19 CET 2025]
```

**static void dfrgfs(...):** 

- Defragments the file system. This operation removes all files marked from deletion from the system, along with their respective file entries. Afterwards, it compacts the file entries and the file data (moves everything up to fill up the available space, so that no 64 byte block gaps exist)
- Loads all non-deleted files into memory and overwrites the filesystem with only relevant files

Showcase of dfrgfs:

`java zvfs dfrgfs filesystem2.zvfs` --> **Defragmentation complete: defragmented 2 files and freed 0 bytes**

**static void catfs(...):**

- Prints out the file contents of a specified file from the filesystem to the console
- Locates the file in the filesystem, extracts the relevant data and prints it directly to the console

Showcase of catfs:

`java zvfs catfs filesystem2.zvfs test_file3.txt` --> **Hello, world!**


### LLM Declaration

**Abraham Prompts**:

_Created GPT called SoCo Tutor:_

Socratically explain concepts an questions and what needs to be considered about the asked question. your goal is it to build a foundational knowledge about the question asked. The given pdf are the requirements for the project, so as you can see llm's are allowed but no direct answers and solutions.

- "What are some good api documentations for this project?"
- "Can you summarize this: https://docs.python.org/3/library/io.html"
- "Can you summarise this: https://docs.python.org/3/library/struct.html"
- "Summarise and explain thuroughly this chapter of the source material: **Chapter 17, Software design by example**
- "Explain the difference between rb and r"
- "Summarise this: 
- "Summarise this: 
- "Explaint the format my friend used and explain it: **pasted a snipped of the code**
- "Explain rb and wb, explain thuroughly"
- "How do I open a file in Java in read and write mode"
- "Explain RandomAccessFile"
- "When should one use FileChannel and RandomAccessFile"
- "In python to open and write a file we can use r+b, explain alternative java concepts, if possible list them and check which ones align with Java NIO"
- "In Python, I used f.seek(). What is the equivalent method in Java's FileChannel to jump to a specific byte offset?"
- "What is the difference between Files.size() and calculating the size based on the file header offsets?"
- "In python I was able to use loadfs to access the data I needed, why does this not work here"

*Where I pasted a snippet of code:*

- "Why is there no output here"
- "Why does this code not work"
- "What would be the correct syntax for this"
- "Explain this code my friend wrote"
- "Why is this code underscored red?"
- "Why can't I use ++ here"
- "Is this idea correct?"
- "Is this an ok approach?"
- "Why does int not work here"
- "Why does it have to be long"
- "Does there have to be a try except block here?"
- "What is the problem here"
- "Can I do this the same in Java like in my python implementation"
- "Check for any spelling mistakes"
- "Is this ok"
- "Explain this to me like I am 5"
- "In total, is this ok now"
