import ipfshttpclient
from decouple import config

class IPFSService:
    def __init__(self):
        api_addr = config('IPFS_API_ADDR', default=None)
        if not api_addr:
            raise Exception("IPFS_API_ADDR is not set in the environment.")

        try:
            self._client = ipfshttpclient.connect(api_addr)
        except Exception as e:
            raise Exception(f"Failed to connect to IPFS node: {e}")

    def add_file(self, file_content):
        """
        Adds a file (bytes) to IPFS.
        Returns the IPFS CID.
        """
        res = self._client.add_bytes(file_content, wrap_with_directory=True)
        return res['Hash']

    def get_file(self, cid):
        """
        Retrieves a file from IPFS by its CID.
        Returns the file content as bytes.
        """
        return self._client.cat(cid)

    def close(self):
        self._client.close()
