import hashlib


def hash_value(value: str, encoding: str = "utf-8") -> str:

    value_bytes = str(value).encode(encoding=encoding)
    hash_object = hashlib.md5()
    hash_object.update(value_bytes)
    return hash_object.hexdigest()
