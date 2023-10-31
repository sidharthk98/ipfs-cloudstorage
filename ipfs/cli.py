import argparse
from ipfs.ipfs import IPFSHandler

def main():
    parser = argparse.ArgumentParser(description="osis ipfs pin")
    parser.add_argument(
        "command", 
        choices=["upload", "dump", "pin", "unpin", "download","cat","ls","id"], 
        help="""
        upload - To upload a single file |
        dump - To upload a directory [Use --pattern for pattern matching] |
        download - To pull a artifact providing the ContentId |
        pin - To pin a artifact to the IPFS cluster using the ContentId |
        unpin - To unpin the artifact from the IPFS cluster |
        """,
        )
    parser.add_argument("payload", nargs='?', default=None, help="CID for pin, unpin, or download; filename for upload")
    parser.add_argument("--pattern", nargs="?", help=" Usage: osis dump <directory_path> --pattern '*.<file_pattern>'")
    
    # Parse the command line arguments
    args = parser.parse_args()

    # Access the selected subcommand and its arguments
    command = args.command
    payload = args.payload
    pattern = args.pattern if args.pattern else '*'
    
    handler = IPFSHandler()

    if command == "upload":
        handler.UploadArtifact(payload)
    if command == "dump":
        handler.UploadDirectory(payload,pattern)
    elif command == "pin":
        handler.PinfiletoIPFS(payload)
    elif command == "unpin":
        handler.UnpinfilefromIPFS(payload)
    elif command == "download":
        handler.DownloadArtifact(payload)
    elif command == "cat":
        handler.readFile(payload)
    elif command == "ls":
        handler.listArtifacts()
    elif command == "id":
        handler.getId()


if __name__ == "__main__":
    main()
