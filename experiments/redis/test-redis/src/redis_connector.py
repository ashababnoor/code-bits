import redis

r = redis.Redis(host="localhost", port=6379)
ping_output = r.ping()

if __name__ == "__main__":
    print(f"Ping successful: {ping_output}")