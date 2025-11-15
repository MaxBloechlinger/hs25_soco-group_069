import struct

#create new filesystem, populate header, fillout file entries with 0s for 32 entries,
#include values for header metadata
def mkfs(file_system_name):

    #========================[ Header Fields ]=========================]

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

    reserved2 = 26 * b"\x00" #= 26 times 00s, so 26 bytes containing 0, format char: "26s"

