import struct
import sys
import os
import time


#========================[ GLOBAL VARIABLES FOR HELPER METHODS ]=========================

#Format Variables
HEADER_FORMAT = "<8sBBHHHHHIIIIH26s"
ENTRY_FORMAT = "<32sIIBBHQ12s"

#Size Variables
HEADER_SIZE = 64
ENTRY_SIZE = 64

def pack_header(magic,version, flags, reserved0, file_count, file_capacity,
                file_entry_size, reserved1, file_table_offset, data_start_offset,
                next_free_offset, free_entry_offset, deleted_files, reserved2):
    
    header = struct.pack(
        HEADER_FORMAT, 
        magic, #0
        version, #1
        flags, #2
        reserved0, #3
        file_count, #4
        file_capacity,#5
        file_entry_size, #6
        reserved1, #7
        file_table_offset, #8
        data_start_offset, #9
        next_free_offset, #10
        free_entry_offset, #11
        deleted_files, #12
        reserved2 #13
        )
        
    return header

def unpack_header(header_bytes):
    return struct.unpack(HEADER_FORMAT, header_bytes)

#pack_entry_emptty() is only used for mkfs and dfrgfs!!!
def pack_entry_empty(name, start, length, type,
        flag, reserved0, created, reserved1):
    empty_entry = struct.pack(
        ENTRY_FORMAT,
        name,
        start,
        length,
        type,
        flag,
        reserved0,
        created,
        reserved1
        )
    return empty_entry

#create new filesystem, populate header, fillout file entries with 0s for 32 entries,
#include values for header metadata
def mkfs(file_system_name):

    #========================[ FILE SYSTEM HEADER ]=========================

    #use b"..." (byte literal) for raw binary data 
    magic = b"ZVFSDSK1"     #8 bytes in total, string array format character: s (char[]), thus "8s"
    version = 1             #"B" 1 byte int format (unsigned bc values should never be negative + unsigned has twice the storage for us + security from overflow errors etc.)
    flags = 0               #"B" 1 byte int format 
    reserved0 = 0           #"H" 2 byte int (unsigned short)
    file_count = 0          #"H" 
    file_capacity = 32      #"H"
    file_entry_size = 64    #"H"
    reserved1 = 0           #"H"
    file_table_offset = 64      #"I" 4 byte unsigned int 
    data_start_offset = 2112    #"I"
    next_free_offset = data_start_offset    #"I"
    free_entry_offset = 0      #"I"
    deleted_files = 0           #"H"
    reserved2 = b"\x00" * 26     #26 times 00, so 26 bytes containing 0s, format char: "26s"


    #pack() header into byte format
    header = pack_header(magic,version, flags, reserved0, file_count, file_capacity,
                file_entry_size, reserved1, file_table_offset, data_start_offset,
                next_free_offset, free_entry_offset, deleted_files, reserved2)
    
    #========================[ FILE ENTRY ]=========================

    name = b"\x00" * 32         #"32s"
    start = 0                   #"I"
    length = 0                  #"I"
    type = 0                    #"B"
    flag = 0                    #"B"
    reserved0 = 0               #"H"
    created = 0                 #"Q"
    reserved1 = b"\x00" * 12    #"12s"


    empty_entry = pack_entry_empty(name, start, length, type, flag, 
                             reserved0, created, reserved1)
    
    #========================[ WRITE file_system_name.zvfs FILE ]=========================]

    #open new file in write binary mode
    with open(f"{file_system_name}.zvfs", "wb") as f:
        f.write(header)
        for _ in range(32):
            f.write(empty_entry) 

#==========================[ Get info about a .zvfs file ]============================]
def gifs(file_system_name):
    with open(f"{file_system_name}.zvfs", "rb") as f:

        header_bytes = f.read(HEADER_SIZE) # Read entire file system, I don't think extracting only necessary data would warrant difficulty to maintain for minimal efficiency increase 🤓

        header = unpack_header(header_bytes)

        #check struct.pack for proper index of data
        file_count = header[4]
        file_capacity = header[5]
        deleted_files = header[12] 

        remaining_entries = file_capacity - file_count - deleted_files # Count deleted files as well, they are only marked as deleted but still exist

        f.seek(0, 2)
        file_size = f.tell() #Jump to the end of the file, tells us where we are which should be current size

        print(f"The file system name is: {file_system_name}.zvfs " )
        print("-------------------------------------")
        print(f"The number of files present is: {file_count} ")
        print("-------------------------------------")
        print(f"The remaining free entries are: {remaining_entries} ")
        print("-------------------------------------")
        print(f"Number of files marked as deleted: {deleted_files} ")
        print("-------------------------------------")
        print(f"The total size of the file is: {file_size} ")
        print("-------------------------------------")


def getfs(file_path):
    #fs dict to store "header", "entries" & "data"
    file_system = {}

    with open(file_path, "rb") as f:
        header_bytes = f.read(HEADER_SIZE)
        header = unpack_header(header_bytes)
        file_system["header"] = header

        file_capacity = header[5]
        file_table_offset = header[8]
        data_start_offset = header[9] 

        f.seek(file_table_offset)

        file_entries = []

        for _ in range(file_capacity):
            entry_bytes = f.read(ENTRY_SIZE)
            file_entries.append(entry_bytes)
        
        file_system["entries"] = file_entries

        f.seek(data_start_offset)

        data = f.read()

        file_system["data"] = data

        return file_system

    
#==========================[ Adding files to the .zvfs file]============================]

def addfs(file_system_name, src_path):
    with open(f"{file_system_name}.zvfs", "r+b") as f:
        #===========================[ READ HEADER ]==========================
        f.seek(0)
        header_bytes = f.read(HEADER_SIZE)
        header = unpack_header(header_bytes)
        
        source_file_size = os.path.getsize(src_path) #get src file size
        
        with open(src_path, "rb") as source_file:
            data = source_file.read() #save file bytes of source file in "data"

        #extract relevant vars from header tuple
        file_table_offset = header[8]
        file_capacity = header[5]
        next_free_offset = header[10]

        #===========================[ FIND FREE ENTRY FIELD ]==========================
        
        f.seek(file_table_offset)
        #find the first empty file entry:
        for i in range(file_capacity): #for i = 0; i<32; i++ file entries
            entry = f.read(ENTRY_SIZE)
            (name, start, length, typ , flag, reserved0, created, reserved1) = struct.unpack(ENTRY_FORMAT, entry)
            if length == 0 and typ == 0: #type is called typ to avoid type() shadowing
                entry_offset = file_table_offset + i * ENTRY_SIZE
                break
        
        #===========================[ WRITE DATA ]==========================
        f.seek(next_free_offset)
        f.write(data)

        dest_file_name = os.path.basename(src_path) 
        encoded_name = dest_file_name.encode()[:32] #encode destinantion name to first 32 bytes
        name = encoded_name + (32-len(encoded_name))*b"\x00" #add zero padding to fill incase name didnt use all 32 bytes 


        created = int(time.time())
        reserved1 = 12 * b"\x00"
        
        entry = struct.pack(
        ENTRY_FORMAT,
        name,
        next_free_offset, #start
        source_file_size, #length
        1,                #type     
        0,                #flag
        0,                #reserved0
        created,
        reserved1
        )

        f.seek(entry_offset)
        f.write(entry)

        #===========================[ WRITE NEW HEADER ]==========================
        new_header = pack_header(
            header[0],  #magic
            header[1],  #version
            header[2],  #flags
            header[3],  #reserved0
            header[4]+1,  #file_count
            header[5],  #file_capacity
            header[6],  #file_entry_size
            header[7],  #reserved1
            header[8],  #file_table_offset
            header[9],  #data_start_offset
            header[10]+source_file_size, #next_free_offset
            header[11],  # free_entry_offset
            header[12],  # deleted_files
            header[13]   # reserved2
        )

        f.seek(0)
        f.write(new_header)

    print(f"Added '{dest_file_name}' ({source_file_size} bytes) to {file_system_name}.zvfs")



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("too few args \n example usage: python zvfs.py <function> <arg1> <arg2>")
        sys.exit(1) #exit with error, return 1
    
    function = sys.argv[1].lower()
    args = sys.argv[2:]

    if function == "mkfs": #python zvfs.py mkfs "fs_name"
        file_system_name = args[0]
        mkfs(file_system_name)
        print(f"New file system '{file_system_name}.zvfs' created.")
        sys.exit(0) #exit with success, return 0
    if function == "gifs":
        file_system_name = args[0]
        gifs(file_system_name)
        sys.exit(0)
    if function == "addfs": #usage: python zvfs.py addfs "fs_name" "example_file"
        file_system_name = args[0]
        src_path = args[1]
        addfs(file_system_name, src_path)
        sys.exit(0)

    if function == "getfs": #usage: python zvfs.py getfs "fs_name"
        path = args[0]
        file_system = getfs(path)
        print("==========================[ HEADER ]==========================")
        print(file_system["header"])
        print("==========================[ ENTRIES ]==========================")
        print(f"Number of files: {file_system['header'][4]}/32")
        print("==========================[ DATA ]==========================")
        print(f"Data size: {len(file_system['data'])} bytes")
        sys.exit(0)

    if function == "rmfs":
        pass
    if function == "lsfs":
        pass
    if function == "dfrgfs":
        pass
    if function == "catfs":
        pass
