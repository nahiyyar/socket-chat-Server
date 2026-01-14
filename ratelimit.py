import time

class RateLimiter:
    def __init__(self,max_req:int,window_sec:int):
        self.max_req = max_req
        self.window_sec = window_sec
        self.users = {}
    
    def allow_req(self,user_id:int):
        curr_time = time.time()

        if user_id not in self.users:
            self.users[user_id] = [curr_time,1]
            return True

        window_start,count = self.users[user_id]

        if curr_time - window_start >=self.window_sec:
            self.users[user_id] = [curr_time,1]
            return True
        
        if count < self.max_req:
            self.users[user_id][1]+=1
            return True
        
        return False

class BucketToken:
    def __init__(self,capacity:int,refill_rate:int):
        self.refill_rate = refill_rate
        self.capacity = capacity
        self.buckets = {}
    
    def allow_req(self,user_id:str) -> bool:
        now = time.time()

        if user_id not in self.buckets:
            self.buckets[user_id]={
                "tokens":self.capacity - 1,
                "last_refill":now
            }
            return True
    

        bucket = self.buckets[user_id]

        elapsed = now - bucket["last_refill"]
        refill = elapsed*self.refill_rate
        bucket["tokens"] = min(self.capacity,bucket["tokens"]+refill)
        bucket["last_refill"] = now

        if bucket["tokens"] >=1 :
            bucket["tokens"] -= 1
            return True

        return False

