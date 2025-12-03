import java.nio.ByteBuffer;
import java.nio.ByteOrder;

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
    if ("gifs".equals(function)){}
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
    //static void packHeader()
    //static void unpackHeader()
    //static void packEmptyEntry()

    private static byte[] packEntry(Entry entry) {
        ByteBuffer buffer = ByteBuffer.allocate(64);
        buffer.order(ByteOrder.LITTLE_ENDIAN);

        buffer.put(entry.name);
        buffer.putInt(entry.start);
        buffer.putInt(entry.length);
        buffer.put((byte) entry.type);
        buffer.put((byte) entry.flag);
        buffer.putShort((short) entry.reserved0);
        buffer.putLong(entry.created);
        buffer.put(entry.reserved1);

        return buffer.array();
    }

    static void mkfs(String fileSystemName){

    }

    static void gifs(String fileSystemName){
        //get info about a file system 
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
    //HELPER STUFF

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


}