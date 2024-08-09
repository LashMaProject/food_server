import hashlib

def generate_hash_key(data):
    # Create an instance of the MD5 hash object
    hash_object = hashlib.md5()

    # Convert the data to bytes and update the hash object
    hash_object.update(data.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hash_key = hash_object.hexdigest()

    return hash_key

# Example usage
data = "Hello, World!"
hash_key = generate_hash_key(data)
print("Hash key:", hash_key)