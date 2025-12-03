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

 *Run these following lines in your terminal:*

  **Creating a new filesystem**

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

*def pack_header(...):*

- Takes as input all header metadata specified and uses `struct.pack` and the global `HEADER_FORMAT` to turn them into 64 bytes

*def unpack_header(...):*

- Extracts the 64 bytes using `struct.unpack()` and `HEADER_FORMAT` to turn them into a tuple of values

*def pack_empty_entry(...):*

- Creates a 64 byte file entry, for mkfs and dfrgfs 

*Filesystem Loader - loadfs*

We decided that, instead of every function needing to unpack the header and read it, and scan for the necessary information each time, to centralise this functionality into one function. It essentially stores the information into a dictionary for each function to access their required information more easily instead of having to parse with each function through the header and unpack it.

**Operations**

*def mkfs(...):*


## java.py

### Design Decision for zvfs.java
























































