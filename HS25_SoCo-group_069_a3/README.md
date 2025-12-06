# HS25 SoCo Assignment 3 Group 69: ZVFS File System

**Members:** Max Blöchlinger, Abraham Herzog, Luiz Hablützel

## Content

- **zvfs.py**
  [Step01]
  Implementation of 8 file system commands with support in terminal
- **zvfs.java**
  [Step02]
  Previous python implementation of the zvfs file system translated into java


## Usage Example

Here we will show general usecases for the operations of the filesystem. A more thorough documentation can be found [here](#operations).

 *Run these following lines in your terminal:*

  **To create a new filesystem**

  `python zvfs.py mkfs filesystem1.zvfs`

  *Now that you have created a new filesystem, you'd probably want to add two text files into your newly created filesystem:*

  **Create two files:**

  `echo Hello, world! > test_file1.txt`

  `echo The weather is nice today > test_file2.txt`

  **Add them both to the filesystem**

  `python zvfs.py addfs filesystem1.zvfs test_file1.txt`

  `python zvfs.py addfs filesystem1.zvfs test_file2.txt`

  **To list all files run:**

  `python zvfs.py lsfs filesystem1.zvfs`

  **To print the content of a text file in the filesystem run:**

  `python zvfs.py catfs filesystem1.zvfs test_file1.txt`

  **If you deleted the filesystem from *your disk* you can restore them by running:**

  `python zvfs.py getfs filesystem1.zvfs test_file1.txt`

  **To get the info of a filesystem you can run:**

  `python zvfs.py gifs filesystem1.zvfs`

  **To delete a texfile from the filesystem run:**

  `python zvfs.py rmfs filesystem1.zvfs test_file1.txt`

  **Finally if you want to defragment the filesystem run:**

  `python zvfs.py dfrgfs filesystem1.zvfs`

  Note, if you want to run these operations in jave you simply have to replace the python command in the beginning and omit the .py suffix:

  --> `java zvfs mkfs filesystem1.zvfs` to create a new filesystem in java


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

## Operations

**def mkfs(...):**

- Creates a new filesystem
- Populates the header and fills out file entries with zero bytes for 32 entries
- Packs the header into byte format

Showcase of mkfs:

`python zvfs.py mkfs filesystem1.zvfs` --> **New file system 'filesystem1.zvfs' created.**

*There now should be a new filesystem in your working directory called filesystem1.zvfs*

**def gifs(...):**
- Returns: file name, number of files present (non deleted), remaining free entries for new files (excluding deleted files), and the number of files marked as deleted
- Opens the file and extracts necessary header data and calculates the the remaining free entries

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
- Adds a file from from the users directory to the filesystem
- Scans the filesystem for first free entry, *next_free_offset* and inserts it there

Showcase of addfs:

*To showcase the usecase for this operation you first must add two files to your directory:*

```
echo Hello, world! > test_file1.txt
echo The weather is nice today > test_file2.txt
```

*Then we can call addfs:*

```
python zvfs.py addfs filesystem1.zvfs test_file1.txt
python zvfs.py addfs filesystem1.zvfs test_file2.txt
```

--> **Added 'test_file1.txt' (14 bytes) to filesystem1.zvfs**

--> **Added 'test_file2.txt' (26 bytes) to filesystem1.zvfs**

*Now both .txt files should be present in your newly created filesystem1.zvfs*

**def getfs(...):**
- Extracts a file from the filesystem to the users disk
- Locates the specified file by name

Showcase of getfs:

*To properly show the usecase of this operation we ask the user to first delete the file they wish to extract from their own directory:*

`rm test_file1.txt`

*And the you should be able to extract it from the created filesystem:*

`python zvfs.py getfs filesystem1.zvfs test_file1.txt`

*It should now have appeared back into your directory*


**def rmfs(...):**
- Locates the file it wants to delete in the filesystem
- Changes its flag byte from 0 to 1, however, the data is not deleted

Showcase of rmfs:

`python zvfs.py rmfs filesystem1.zvfs test_file1.txt`

*The file should now be deleted from the filesystem*

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

### Design Decision for zvfs.java
























































