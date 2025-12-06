import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.channels.FileChannel;
import java.io.RandomAccessFile;


public class zvfs {
    public static void main(String[] args){
        String usage = "Usage: java zvfs <function> <filesystem> <file>";

        if (args.length < 2 || args.length > 3){
            System.out.println(usage);
            return;
        }
    
    
    String function = args[0];
    String fileSystemName = args[1];
    String fileName = (args.length == 3) ? args[2] : null;
    
    if ("mkfs".equals(function)){
        mkfs(fileSystemName);
        String success = String.format("New file system %s created.", fileSystemName);
        System.out.println(success);
            return;
        }
    if ("gifs".equals(function)){
        gifs(fileSystemName);
        return;
    }
    if ("addfs".equals(function)){
        if (fileName == null){
            System.out.println("file name missing");
            System.out.println(usage);
            return;
        }
        addfs(fileSystemName, fileName);
        return;
    }
    if ("getfs".equals(function)){}
    if ("rmfs".equals(function)){
        if (fileName == null){
            System.out.println("file name missing");
            System.out.println(usage);
            return;
        }
        rmfs(fileSystemName, fileName);
        return;
    }
    if ("lsfs".equals(function)){}
    if ("dfrgfs".equals(function)){}
    if ("catfs".equals(function)){}


    }

    static void mkfs(String fileSystemName){
        try {
        
        //=================[ HEADER ]=================
        Header header = new Header();

        header.magic = "ZVFSDSK1".getBytes();
        header.version = 1;
        header.flags = 0;
        header.reserved0 = 0;
        header.fileCount = 0;
        header.fileCapacity = 32;
        header.fileEntrySize = 64;
        header.reserved1 = 0;
        header.fileTableOffset = 64;      
        header.dataStartOffset = 2112;
        header.nextFreeOffset = header.dataStartOffset;
        header.freeEntryOffset = 0;
        header.deletedFiles = 0;
        header.reserved2 = new byte[26];

        //turn header to bytes
        byte[] headerBytes = packHeader(header);

        //=================[ ENTRIES ]=================
        Entry emptyEntry = new Entry();   
        emptyEntry.name = new byte[32]; 
        emptyEntry.start = 0;
        emptyEntry.length = 0;    
        emptyEntry.type = 0;
        emptyEntry.flag =  0; 
        emptyEntry.reserved0 = 0;
        emptyEntry.created = 0;
        emptyEntry.reserved1 = new byte[12];

        byte[] emptyEntryBytes  = packEntry(emptyEntry);
        byte[] res = new byte[64+32*64];
        //HEADER WRITE
        System.arraycopy(headerBytes,0,res,0,64);
        //ENTRY WRITE
        for (int i=0 ; i < 32; i++) {
            int offset = 64 + i*64;
            System.arraycopy(emptyEntryBytes,0,res,offset,64);
        }
        //WRITE FILE
        Files.write(Paths.get(fileSystemName),res);

    } catch (Exception e) { 
        System.out.println("Error: Could not make filesystem: " + fileSystemName);
    }
    }

    static void gifs(String fileSystemName){
        try {
        FileSystem filesystem = loadfs(fileSystemName);

        Header header = filesystem.header;

        int remaining_entries = header.fileCapacity - header.fileCount - header.deletedFiles;

        long filesize = Files.size(Paths.get(fileSystemName));

        System.out.println("The file system name is: " + fileSystemName);
        System.out.println("-------------------------------------");
        System.out.println("The number of files present is: " + header.fileCount);
        System.out.println("-------------------------------------");
        System.out.println("The remaining entries are: " + remaining_entries);
        System.out.println("-------------------------------------");
        System.out.println("Number of deleted files marked as deleted: " + header.deletedFiles);
        System.out.println("-------------------------------------");
        System.out.println("The total size of the file is: " + filesize);
        System.out.println("-------------------------------------");

        } catch (Exception e) {
            System.out.println("Error when extracting data, Filesystem might be empty");
        }

    }

static void addfs(String fileSystemName, String fileName){
    try {
        // load current fs
        FileSystem fs = loadfs(fileSystemName);
        if (fs == null){
            System.out.println("Error: Can't load filesystem: " + fileSystemName);
            return;
        }

        Header header = fs.header;
        Entry[] entries = fs.entries;
        byte[] oldData = fs.data;

        // read file
        byte[] fileBytes = Files.readAllBytes(Paths.get(fileName));
        int fileSize = fileBytes.length;

        // new data = old data + new file bytes
        byte[] newData = new byte[oldData.length + fileSize];
        System.arraycopy(oldData, 0, newData, 0, oldData.length);
        System.arraycopy(fileBytes, 0, newData, oldData.length, fileSize);

        // abs offset
        int fileStart = header.dataStartOffset + oldData.length;

        // find first free entry
        int freeIndex = -1;
        for (int i = 0; i < entries.length; i++) {
            Entry e = entries[i];
            if (e.length == 0 && e.type == 0) {
                freeIndex = i;
                break;
            }
        }
        if (freeIndex == -1) {
            System.out.println("no free entry left in fs");
            return;
        }

        // new entry
        Entry newE = new Entry();
        newE.name = new byte[32];
        String baseName = Paths.get(fileName).getFileName().toString();
        byte[] nameBytes = baseName.getBytes();
        int nameLen = Math.min(nameBytes.length, 32);
        System.arraycopy(nameBytes, 0, newE.name, 0, nameLen);

        newE.start = fileStart;
        newE.length = fileSize;
        newE.type = 1;
        newE.flag = 0;
        newE.reserved0 = 0;
        newE.created = System.currentTimeMillis() / 1000L;
        newE.reserved1 = new byte[12];

        entries[freeIndex] = newE;

        // update header
        header.fileCount = header.fileCount + 1;
        header.nextFreeOffset = fileStart + fileSize;

        // rebuild whole fs
        int headerSize = 64;
        int entrySize = header.fileEntrySize;
        int fileCapacity = header.fileCapacity;
        int tableOffset = header.fileTableOffset;
        int totalSize = header.dataStartOffset + newData.length;

        byte[] out = new byte[totalSize];

        // header
        byte[] newHeaderBytes = packHeader(header);
        System.arraycopy(newHeaderBytes, 0, out, 0, headerSize);

        // entries
        for (int i = 0; i < fileCapacity; i++) {
            byte[] entryBytes = packEntry(entries[i]);
            int off = tableOffset + i * entrySize;
            System.arraycopy(entryBytes, 0, out, off, entrySize);
        }


        System.arraycopy(newData, 0, out, header.dataStartOffset, newData.length);

        // write back filesystem file
        Files.write(Paths.get(fileSystemName), out);

        System.out.println("Added '" 
            + Paths.get(fileName).getFileName().toString() 
            + "' (" + fileSize + " bytes) to " + fileSystemName);

    } catch (Exception ex) {
        System.out.println("Error: Could not add file: " + ex.getMessage());
    }
}



    static void getfs(String fileSystemName, String fileName){
        
    }

    static void rmfs(String fileSystemName, String fileName){
        try{
            FileSystem filesystem = loadfs(fileSystemName);
        
            int idx = -1;
            Entry target = null;
            
            for (int i = 0; i < filesystem.entries.length; i++){
                Entry entry = filesystem.entries[i];

                if (entry.length == 0 && entry.type == 0)
                    continue;
                

                // Check ending for null bytes
                int prefix = 0;
                for (int x = 0; x < entry.name.length; x++){
                    if(entry.name[x] == 0){
                        break;
                    } prefix++;
                }
                
                String entryname = new String(entry.name, 0, prefix, "UTF-8");

 
                if (entryname.equals(fileName) && entry.flag == 0) {
                    idx = i;
                    target = entry;
                    break;
                }
            }

            if (idx == -1){
                System.out.println("File couln't be found");
                return;
            }

            try (RandomAccessFile raf = new RandomAccessFile(fileSystemName, "rw"); 
                FileChannel channel = raf.getChannel()) {

                    target.flag = 1;

                    long position = 64 + (idx * 64);

                    byte[] eb = packEntry(target);
                    ByteBuffer b = ByteBuffer.wrap(eb);

                    channel.position(position);
                    channel.write(b);

                    filesystem.header.fileCount = filesystem.header.fileCount - 1;
                    filesystem.header.deletedFiles = filesystem.header.deletedFiles + 1;

                    byte[] hb = packHeader(filesystem.header);
                    ByteBuffer bb = ByteBuffer.wrap(hb);

                    channel.position(0);
                    channel.write(bb);

                }
                System.out.println("This file has been deleted successfully: " + fileName);
        } catch (Exception e) {
            System.out.println("Could not delete file");
        }
    }

    static void lsfs(String fileSystemName){
        
    }

    static void dfrgfs(String fileSystemName){
        
    }

    static void catfs(String fileSystemName, String fileName){
        
    }

    private static FileSystem loadfs(String fileSystemName) {
        FileSystem fileSystem = new FileSystem();

        try {
            //turn file into byte array
            byte[] allBytes = Files.readAllBytes(Paths.get(fileSystemName));

            //=================[ HEADER ]=================
            byte[] headerBytes = new byte[64];
            System.arraycopy(allBytes, 0, headerBytes, 0, 64);

            Header header = unpackHeader(headerBytes);
            fileSystem.header = header;

            int entrySize = header.fileEntrySize;
            int fileCapacity = header.fileCapacity;
            int tableOffset = header.fileTableOffset;

            //=================[ ENTRIES ]=================
            Entry[] entries = new Entry[fileCapacity];

            for (int i = 0; i < fileCapacity; i++) {
                int start = tableOffset + i * entrySize;

                byte[] entryBytes = new byte[entrySize];
                System.arraycopy(allBytes, start, entryBytes, 0, entrySize);

                entries[i] = unpackEntry(entryBytes);
            }

            fileSystem.entries = entries;

            //=================[ DATA ]=================
            int dataStart = header.dataStartOffset;
            int dataLength = allBytes.length - dataStart;

            byte[] dataRegion = new byte[dataLength];
            System.arraycopy(allBytes, dataStart, dataRegion, 0, dataLength);

            fileSystem.data = dataRegion;

            return fileSystem;

        } catch (Exception e) {
            System.out.println("Error: Can't load filesystem: " + fileSystemName);
            return null;
        }
    }


    //=================[ FILESYSTEM, HEADER & ENTRY CLASSES ]=================

    private static class FileSystem {
        Header header;
        Entry[] entries;
        byte[] data;
    }

    private static class Header {
        byte[] magic;      
        int version;       
        int flags;         
        int reserved0;     
        int fileCount;     
        int fileCapacity;  
        int fileEntrySize; 
        int reserved1;     
        int fileTableOffset;
        int dataStartOffset;
        int nextFreeOffset;
        int freeEntryOffset;
        int deletedFiles;  
        byte[] reserved2;  
    }

    private static class Entry {
        byte[] name;       
        int start;         
        int length;        
        int type;          
        int flag;          
        int reserved0;     
        long created;      
        byte[] reserved1;  
    }
    
   //=================[ HELPER FUNCTIONS ]=================

    private static byte[] packHeader(Header header){
        ByteBuffer buffer = ByteBuffer.allocate(64); //allocate 64 bytes for buffer
        buffer.order(ByteOrder.LITTLE_ENDIAN); //set ByteOrder to little endian like "<" in .py 
        
        buffer.put(header.magic);                       //8s
        buffer.put((byte)header.version);               //B
        buffer.put((byte)header.flags);                 //B
        buffer.putShort((short)header.reserved0);       //H
        buffer.putShort((short)header.fileCount);       //H
        buffer.putShort((short)header.fileCapacity);    //H
        buffer.putShort((short)header.fileEntrySize);   //H
        buffer.putShort((short)header.reserved1);       //H
        buffer.putInt(header.fileTableOffset);          //I
        buffer.putInt(header.dataStartOffset);          //I
        buffer.putInt(header.nextFreeOffset);           //I
        buffer.putInt(header.freeEntryOffset);          //I
        buffer.putShort((short)header.deletedFiles);    //H
        buffer.put(header.reserved2);                   //26s
            
        return buffer.array();
    }

    private static byte[] packEntry(Entry e) {
        ByteBuffer buffer = ByteBuffer.allocate(64);
        buffer.order(ByteOrder.LITTLE_ENDIAN);

        buffer.put(e.name);
        buffer.putInt(e.start);
        buffer.putInt(e.length);
        buffer.put((byte) e.type);
        buffer.put((byte) e.flag);
        buffer.putShort((short) e.reserved0);
        buffer.putLong(e.created);
        buffer.put(e.reserved1);

        return buffer.array();
    }

    private static Entry unpackEntry(byte[] data) {
        ByteBuffer b = ByteBuffer.wrap(data); 
        b.order(ByteOrder.LITTLE_ENDIAN);

        Entry e = new Entry();

        e.name = new byte[32];
        b.get(e.name);

        e.start  = b.getInt();
        e.length = b.getInt(); 

        e.type = Byte.toUnsignedInt(b.get());
        e.flag = Byte.toUnsignedInt(b.get());

        e.reserved0 = Short.toUnsignedInt(b.getShort());

        e.created = b.getLong();    

        e.reserved1 = new byte[12];
        b.get(e.reserved1);

        return e;
    }


    private static Header unpackHeader(byte[] packedHeader){
        ByteBuffer buffer = ByteBuffer.wrap(packedHeader);
        buffer.order(ByteOrder.LITTLE_ENDIAN);

        Header header = new Header();

        //Bytes
        header.magic = new byte[8];
        buffer.get(header.magic);
        header.version = Byte.toUnsignedInt(buffer.get());
        header.flags = Byte.toUnsignedInt(buffer.get());

        //H
        header.reserved0 = Short.toUnsignedInt(buffer.getShort());
        header.fileCount = Short.toUnsignedInt(buffer.getShort());
        header.fileCapacity = Short.toUnsignedInt(buffer.getShort());
        header.fileEntrySize = Short.toUnsignedInt(buffer.getShort());
        header.reserved1 = Short.toUnsignedInt(buffer.getShort());
        
        //I
        header.fileTableOffset = buffer.getInt();
        header.dataStartOffset = buffer.getInt();
        header.nextFreeOffset = buffer.getInt();
        header.freeEntryOffset = buffer.getInt();
        //H
        header.deletedFiles = Short.toUnsignedInt(buffer.getShort());
        //26s 
        header.reserved2 = new byte[26];
        buffer.get(header.reserved2);

        return header;
    }

}
