import redis
from loader import Bigquery

redis_local = redis.Redis(host="localhost", port=6380, decode_responses=True)
redis_local_apt = redis.Redis(host="localhost", port=6379, decode_responses=True)

bq = Bigquery(google_cred=None)

if __name__ == "__main__":
    
    redis_local_apt_connected = redis_local_apt.ping()
    print(f"Connection to Redis Stack successful: {redis_local_apt_connected}")

    bq_connected = bq.test_connection()
    print(f"Connection to BigQuery successful: {bq_connected}")
