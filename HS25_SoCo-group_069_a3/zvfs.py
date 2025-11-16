import struct
import sys

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
    free_entry_offset = 64      #"I"
    deleted_files = 0           #"H"
    reserved2 = b"\x00" * 26     #26 times 00, so 26 bytes containing 0s, format char: "26s"

    #all formats from above combined:
    header_format_string = "<8sBBHHHHHIIIIH26s" #little-endian "<" byteorder because sys.byteorder returns "little"

    #pack() header into byte format
    header = struct.pack(
        header_format_string, 
        magic,
        version,
        flags,
        reserved0,
        file_count,
        file_capacity,
        file_entry_size,
        reserved1,
        file_table_offset,
        data_start_offset,
        next_free_offset,
        free_entry_offset,
        deleted_files,
        reserved2
        )
    
    #========================[ FILE ENTRY ]=========================

    name = b"\x00" * 32         #"32s"
    start = 0                   #"I"
    length = 0                  #"I"
    type = 0                    #"B"
    flag = 0                    #"B"
    reserved0 = 0               #"H"
    created = 0                 #"Q"
    reserved1 = b"\x00" * 12    #"12s"

    file_entry_string = "<32sIIBBHQ12s"

    entry = struct.pack(
        file_entry_string,
        name,
        start,
        length,
        type,
        flag,
        reserved0,
        created,
        reserved1
        )
    
    #========================[ WRITE file_system_name.zvfs FILE ]=========================]

    #open new file in write binary mode
    with open(f"{file_system_name}.zvfs", "wb") as f:
        f.write(header)
        for _ in range(32):
            f.write(entry) 


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("too few args \n example usage: python zvfs.py <function> <arg1> <arg2>")
        sys.exit(1) #exit with error, return 1
    
    function = sys.argv[1].lower()
    args = sys.argv[2:]

    if function == "mkfs":
        file_system_name = args[0]
        mkfs(file_system_name)
        print(f"New file system '{file_system_name}.zvfs' created.")
        sys.exit(0) #exit with success, return 0
    if function == "gifs":
        pass
    if function == "addfs":
        pass
    if function == "getfs":
        pass
    if function == "rmfs":
        pass
    if function == "lsfs":
        pass
    if function == "dfrgfs":
        pass
    if function == "catfs":
        pass
