import subprocess
import ipfshttpclient
from ipfs.cloudstore import UploadtoCloudStorage, DownloadfromCloudStorage, ChangeObjectRetention
import json, os ,fnmatch
from tinydb import TinyDB

# Define the local storage path
local_storage_path = '/Users/sidharth/Documents/dev/ipfs-osis/osis/tinydb.json'
# Create a TinyDB instance with the specified storage path
db = TinyDB(local_storage_path)


# Initialize the IPFS client
ipfs = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

class IPFSHandler:
    def UploadArtifact(self, filename):
        # Upload the artifact to Cloud Storage and set retention to 30 days
        response = UploadtoCloudStorage(filename)
        metadata = {
            "name": filename,
            "cloud-storage url": response
        }
        # Add metadata as an IPFS entry and get the CID
        cid = ipfs.add_json(metadata)
        cache = {
            "name": filename,
            "contentId": cid
        }
        db.insert(cache)
        print(f' {cid} : {filename}')

    def UploadDirectory(self, local_directory, pattern):

        for root, _, files in os.walk(local_directory):
            for filename in files:
                if pattern!=None and fnmatch.fnmatch(filename, pattern):
                    local_file_path = os.path.join(root, filename)
                    cloud_object_name = os.path.relpath(local_file_path, local_directory)
                    self.UploadArtifact(local_file_path)


    def listArtifacts(self):
        print(ipfs.pin.ls(type='all'))
        # recent_state = db.all()
        # for record in recent_state:
        #     print(record)

    def getId(self):
        print(ipfs.id())

    def readFile(self, CID): # Currently disfunctional
        print(ipfs.cat(CID))

    def PinfiletoIPFS(self, CID):
        try:
            response = json.loads(json.dumps(ipfs.get_json(CID))) 
            name, cloud_storage_url = response['name'], response['cloud-storage url']
            ChangeObjectRetention(name, cloud_storage_url, "pin")
        except Exception as e:
            print(f"Error retrieving metadata for CID {CID}: {e}")
            return None

    def UnpinfilefromIPFS(self, CID):
        try:
            response = json.loads(json.dumps(ipfs.get_json(CID))) 
            name, cloud_storage_url = response['name'], response['cloud-storage url']
            ChangeObjectRetention(name, cloud_storage_url, "unpin")
        except Exception as e:
            print(f"Error retrieving metadata for CID {CID}: {e}")

    def DownloadArtifact(self, CID):
        try:
            # Query the IPFS daemon to retrieve metadata associated with the CID
            response = json.loads(json.dumps(ipfs.get_json(CID))) 
            name, cloud_storage_url = response['name'], response['cloud-storage url']
            try:
                DownloadfromCloudStorage(name, cloud_storage_url)

            except Exception as e:
                print(f"Unable to retrive {name} from the bucket: {e}")
                return None


        except Exception as e:
            print(f"Error retrieving metadata for CID {CID}: {e}")
            return None

# Example usage
# handler = IPFSHandler()

# # Upload the artifact to IPFS and Cloud Storage
# CID = handler.upload("path/to/your/artifact", "ArtifactName")

# # Pin the file to IPFS
# handler.PinfiletoIPFS(CID)

# # Unpin the file from IPFS
# handler.UnpinfilefromIPFS(CID)

# Example usage
