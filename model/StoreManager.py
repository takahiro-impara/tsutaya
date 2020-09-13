import json
from Store import Store

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
import util

store_data_json = util.resource_path('store-data/tsutaya.json')
#store_data_json = os.path.abspath('resources/store-data/tsutaya.json')

sys.path.append(os.getcwd())
class StoreManager:
    stores = {}

    def __init__(self, data, store_name):
        self.load(data, store_name)

    def load(self, data, store_name):
        with open(data, "r") as f:
            for k, v in json.load(f).items():
                store = Store(id=k,
                              name=store_name,
                              branch=v['name'] if 'name' in v else '-',
                              businessHour=v['business_hour'] if 'business_hour' in v else '-',
                              phone=v['phone'] if 'phone' in v else '-',
                              address=v['address'] if 'address' in v else '-')
                self.stores[store.id] = store

    def clear(self):
        self.stores.clear()

    def all_stores(self):
        return self.stores

    def all_store_ids(self):
        return self.stores.keys()

    def store_name(self, store_id: str):
        return self.stores[store_id].name

    def branch_name(self, store_id: str):
        return self.stores[store_id].branch

    def business_hour(self, store_id: str):
        return self.stores[store_id].businessHour.replace(u'／', '\n')

    def phone(self, store_id):
        return self.stores[store_id].phone

    def address(self, store_id):
        return self.stores[store_id].address

    def filter_by_area(self, area):
        result = []
        for store in self.stores.values():
            for a in area:
                print('area:' + a + ' address:' + store.address)
                if a in store.address:
                    result.append(store)
        return result

    def reload(self):
        self.clear()
        self.load(store_data_json, "TSUTAYA")


tsutaya = StoreManager(store_data_json, "TSUTAYA")

if __name__ == '__main__':
    print((tsutaya.all_stores()))
    print(tsutaya.all_stores())
