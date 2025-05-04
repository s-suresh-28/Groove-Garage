import ipfshttpclient

def upload_to_ipfs(file_path):
    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
        res = client.add(file_path)
        return res['Hash']  # Return only the IPFS hash
    except Exception as e:
        print("IPFS upload failed:", e)
        return None
