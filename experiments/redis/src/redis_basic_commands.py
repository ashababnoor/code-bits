from redis_connector import *

def get_all_keys(r: redis.Redis) -> None:
    keys = r.keys(pattern="*")
    for key in keys:
        value = r.get(key)
        print(f"{key = } --> {value = }")


r = redis.Redis(host="localhost", port=6379)

print("Example of Redis keys command: redis.Redis.keys()")
print()
keys = r.keys(pattern="*")
print(f"{keys = }")

print()

print(f"Example of Redis get command: redis.Redis.get()")
print()
for key in keys:
    value = r.get(key)
    print(f"{key = } --> {value = }")

print()

print("Example of Redis set command: redis.Redis.set()")
print()
print(r.set(name="ceo", value="fahim"))
print(r.set(name="cto", value="adnan"))

print()

print("Looping over all keys to again to check newly added key:value")
print()
get_all_keys(r)