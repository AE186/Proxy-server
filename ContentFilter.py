import json
import re
import os

class Filter:
    def __init__(self):
        if os.path.exists('filter.json'):
            with open('filter.json') as f:
                f = json.load(f)
                self.filter_list = f['blocked-urls']
        else:
            self.filter_list = []
            with open('filter.json') as f:
                f.write(json.dumps({'blocked-urls': []}))
    
    def block(self, url):
        for ele in self.filter_list:
            if re.search(ele, url):
                return True
        
        return False
    
    def Add_url(self, url):
        for i in range(len(self.filter_list)):
            if self.filter_list[i] == url:
                return
        
        self.filter_list.append(url)

        with open('filter.json') as f:
            new_config = json.load(f)
        
        new_config['blocked-urls'] = self.filter_list

        with open('filter.json', 'w') as f:
            f.write(json.dumps(new_config))
    
    def remove_url(self, url):
        for i in range(len(self.filter_list)):
            if self.filter_list[i] == url:
                self.filter_list[i], self.filter_list[len(self.filter_list)-1] = self.filter_list[len(self.filter_list)-1], self.filter_list[i]
                self.filter_list.pop()

                with open('filter.json') as f:
                    new_config = json.load(f)
                
                new_config['blocked-urls'] = self.filter_list

                with open('filter.json', 'w') as f:
                    f.write(json.dumps(new_config))
                
                break
