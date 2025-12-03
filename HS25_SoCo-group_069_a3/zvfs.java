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

    static void mkfs(String fileSystemName){
        byte magic = "ZVFSDSK1"
        byte version = 1;
        byte flags = 0;
        byte reserved0 = 0;
        byte file_count = 0;
        byte file_capacity = 32;
        byte file_entry_size = 64;
        byte reserved1 = 0;
        byte file_table_offset = 64;
        byte data_start_offset = 2112;
        byte next_free_offset = data_start_offset;
        byte free_entry_offset = 0;
        byte deleted_files = 0;
        byte[] reserved2 = new byte[26]

        //byte[] header = Continue here
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
    
}