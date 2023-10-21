import redis
from loader import Bigquery

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r_ah = redis.Redis(host="localhost", port=6379, decode_responses=True)
r_stack = redis.Redis(host="localhost", port=6381, decode_responses=True)

bq = Bigquery(google_cred=None)

if __name__ == "__main__":
    # redis_connected = r.ping()
    # print(f"Connection to Redis successful: {redis_connected}")
    
    redis_stack_connected = r_ah.ping()
    print(f"Connection to Redis Stack successful: {redis_stack_connected}")

    bq_connected = bq.test_connection()
    print(f"Connection to BigQuery successful: {bq_connected}")
