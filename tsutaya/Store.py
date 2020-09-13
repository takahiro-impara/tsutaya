class Store:
    def __init__(self, id:str, name:str, branch:str, businessHour:str, phone:str, address: str):
        self.id = id
        self.name = name
        self.branch = branch
        self.businessHour = businessHour
        self.phone = phone
        self.address = address

    def id(self):
        return self.id

    def name(self):
        return self.name()

    def branchName(self):
        return self.branch

    def businessHour(self):
        return self.businessHour

    def phone(self):
        return self.phone

    def address(self):
        return self.address