from StoreManager import tsutaya


class SearchResult:
    def __init__(self, store_id, has_stock):
        self.hasStock = has_stock
        self.storeName = tsutaya.store_name(store_id)
        self.branch = tsutaya.branch_name(store_id)
        self.address = tsutaya.address(store_id)
        self.phone = tsutaya.phone(store_id)
        self.businessHour = tsutaya.business_hour(store_id)
