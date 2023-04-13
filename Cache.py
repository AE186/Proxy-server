import json
import os
import sys

class LRUCache:
    def __init__(self, size) -> None:
        if os.path.exists('cache.json'):
            with open('cache.json') as f:
                f = json.load(f)
                if f['algo'] == 'LRU'and size == f['size']:
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
        print(self.queue)
        save = {}
        save['algo'] = 'LRU'
        save['size'] = self.size
        save['queue'] = self.queue
        save['map'] = self.map
        save['pairs'] = self.pairs
        
        with open('cache.json', 'w') as f:
            f.write(json.dumps(save))
    
    def details(self):
        print(self.queue)

class FIFOCache:
    def __init__(self, size) -> None:
        if os.path.exists('cache.json'):
            with open('cache.json') as f:
                f = json.load(f)
                if f['algo'] == 'FIFO'and size == f['size']:
                    self.queue = f['queue']
                    self.pairs = f['pairs']
                    self.size = f['size']
                    return
        
        self.queue = []
        self.pairs = {}
        self.size = size

    def refer(self, x):
        if x not in self.pairs:
            if len(self.queue) == self.size:
                delete = self.queue.pop(0)
                self.pairs.pop(delete)
            self.queue.append(x)

    def get(self, x):
        if x in self.pairs:
            return self.pairs[x]

        return None

    def put(self, x, val):
        if x not in self.pairs:
            self.refer(x)
            self.pairs[x] = val
    
    def save(self):
        print(self.queue)
        save = {}
        save['algo'] = 'FIFO'
        save['size'] = self.size
        save['queue'] = self.queue
        save['pairs'] = self.pairs
        
        with open('cache.json', 'w') as f:
            f.write(json.dumps(save))
    
    def details(self):
        print(self.queue)

class Cache:
    def __init__(self) -> None:
        with open('config.json') as f:
            config = json.load(f)
            algo = config['CACHING-ALGO']
            size = config['CACHE-SIZE']

        if algo == 'LRU':
            self.cache = LRUCache(size)
        elif algo == 'FIFO':
            self.cache = FIFOCache(size)
        else:
            print("Wrong Caching algo in config")
            sys.exit(0)
    
    def get(self, x):
        return self.cache.get(x)

    def put(self, x, val):
        self.cache.put(x, val)
    
    def save(self):
        self.cache.save()
    
    def details(self):
        self.cache.details()

