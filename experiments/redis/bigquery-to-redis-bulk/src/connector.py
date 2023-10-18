import redis
from loader import Bigquery

r = redis.Redis(host="localhost", port=6379)
bq = Bigquery(google_cred=None)

if __name__ == "__main__":
    redis_connected = r.ping()
    print(f"Connection to Redis successful: {redis_connected}")
    
    bq_connected = bq.test_connection()
    print(f"Connection to BigQuery successful: {bq_connected}")