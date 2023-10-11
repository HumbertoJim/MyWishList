import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class DataManager:
    def __init__(self, name, fields=[]):
        self._path = BASE_DIR / '{0}.dat'.format(name)
        self._fields = fields
        try:
            if not os.path.exists(self._path):
                raise Exception()
            data = pd.read_csv(self._path)
            data = data[fields]
        except:
            data = {}
            for field in fields:
                data[field] = []
            data = pd.DataFrame(data)
        self.data = data
    
    def add(self, values={}):
        try:
            index = 0
            if self.data.shape[0] > 0:
                index = self.data.index.values[-1] + 1
            row = []
            for field in self._fields:
                row.append(values[field])
            self.data.loc[index] = row
            self.save()
            return index
        except:
            pass

    def update(self, id, field, value):
        try:
            self.data.loc[id, field] = value
        except:
            pass

    def save(self):
        self.data.to_csv(self._path)

    def delete(self, id):
        try:
            self.data = self.data.drop(id)
        except:
            pass