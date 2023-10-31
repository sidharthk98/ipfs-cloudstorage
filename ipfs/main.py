from IPFS import IPFSHandler

def main():
    handler = IPFSHandler()
    handler.upload_to_cloud_storage('/path/to/your/file')

if __name__ == "__main__":
    main()
