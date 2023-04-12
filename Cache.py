import json
import os
import sys

class LRUCache:
    def __init__(self, size) -> None:
        if os.path.exists('cache.json'):
            with open('cache.json') as f:
                f = json.load(f)
                if f['algo'] == 'LRU':
                    self.queue = f['queue']
                    self.map = f['map']
                    self.pairs = f['pairs']
                    self.size = f['size']
                    return
        
        self.queue = []
        self.map = {}
        self.pairs = {}
        self.size = size

    def refer(self, x):
        if x not in self.map:
            if len(self.queue) == self.size:
                last = self.queue[-1]
                self.map.pop(last)
                self.queue.pop()
                self.pairs.pop(last)

        else:
            self.queue.pop(self.map[x])
        
        self.queue.insert(0, x)
        
        for i in range(len(self.queue)):
            self.map[self.queue[i]] = i

    def get(self, x):
        if x in self.map:
            self.refer(x)
            return self.pairs[x]

        return None

    def put(self, x, val):
        if x not in self.map:
            self.refer(x)
            self.pairs[x] = val
    
    def save(self):
        save = {}
        save['algo'] = 'LRU'
        save['size'] = self.size
        save['queue'] = self.queue
        save['map'] = self.map
        save['pairs'] = self.pairs

        with open('cache.json', 'w') as f:
            f.write(json.dumps(save))

def getCache(algo, size):
    if algo == 'LRU':
        return LRUCache(size)
    # elif algo == 'LFU':
    #     return LFUCache(size)
    else:
        print("Wrong Caching algo in config")
        sys.exit(0)

