import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;
import java.util.Arrays;


public class zvfs {
    public static void main(String[] args){
        String usage = "Usage: java zvfs <function> <filesystem> <file>";

        if (args.length < 2 || args.length > 3){
            System.out.println(usage);
            return;
        }
    
    
    String function = args[0];
    String fileSystemName = args[1];
    String fileName = (args.length > 3) ? args[2] : null;
    
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
    if ("rmfs".equals(function)){}
    if ("lsfs".equals(function)){}
    if ("dfrgfs".equals(function)){}
    if ("catfs".equals(function)){}


    }

    static void mkfs(String fileSystemName){

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
        
    }

    static void getfs(String fileSystemName, String fileName){
        
    }

    static void rmfs(String fileSystemName, String fileName){

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