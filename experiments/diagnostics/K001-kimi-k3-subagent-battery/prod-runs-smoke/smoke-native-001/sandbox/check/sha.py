import hashlib

with open("smoke/hello.py", "rb") as f:
    data = f.read()

print("sha256:", hashlib.sha256(data).hexdigest())
print("bytes:", len(data))
