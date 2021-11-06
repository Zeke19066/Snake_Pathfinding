"""
The communications can only be in a single item as a package.
multiple input/return values must be packaged and accesssed 
by index when needed at either end.
"""

def dummi(nums):
    val_1 = nums[0]+nums[1]
    val_2 = nums[0]-nums[1]
    out = [val_1, val_2]
    return out


# Setting up the Queue
from queue import Queue
from threading import Thread
import numpy as np

nums = []

for _ in range(8):
    item = [np.random.randint(10), np.random.randint(10)]
    nums.append(item)

q = Queue(maxsize=0) #set up the queue to hold all the nums
num_theads = min(50, len(nums)) # Use many threads (50 max, or one for each url)

#Populating Queue with tasks
results = [{} for x in nums];
for i in range(len(nums)): #load up the queue with the nums to fetch and the index for each job (as a tuple):
    q.put((i,nums[i]))#need the index and the input in each queue item.


# Threaded function for queue processing.
def crawl(q, result):
    while not q.empty():
        work = q.get() #fetch new work from the Queue
        try:
            data = dummi(work[1])
            result[work[0]] = data #Store data back at correct index
        except:
            result[work[0]] = {}
        q.task_done() #signal to the queue that task has been processed
    return True

threads = []
#Starting worker threads on queue processing
for i in range(num_theads):
    worker = Thread(target=crawl, args=(q,results))
    worker.setDaemon(True)    #setting threads as "daemon" allows main program to 
                              #exit eventually even if these dont finish 
                              #correctly.
    worker.start()
    threads.append(worker)

#for worker in threads:
#   worker.join()

q.join() #now we wait until the queue has been processed


print(results)
