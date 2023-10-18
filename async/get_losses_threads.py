import json
from time import time
from threading import Thread
from get_losses import parse

if __name__ == "__main__":
    with open("links.json", "r") as f:
        urls = json.loads(f.readline())

    start_time = time()
    threads = list()
    for url in urls*20:
        tr = Thread(target=parse, args=(url,))
        threads.append(tr)
        tr.start()
    [thread.join() for thread in threads]
    elapsed_time = time() - start_time
    print("Thread completed in {} seconds".format(elapsed_time))
