import time
from pymongo import MongoClient


class Build_reverse_identity_dictionary:
    def __init__(self):

        self.people_identity_dict = dict()
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["smartshark"]
        self.people_data = self.db["people"]
        self.identity_data = self.db["final_identity"]
        self.people_records = list(self.people_data.find({}))
        self.identity_records = list(self.identity_data.find({}))
        self.reverse_identity_dict = dict()

    def reading_identity_and_people_and_building_reverse_identity_dictionary(self):
        for identity_element in self.identity_records:
            identity = identity_element["_id"]
            people_list = identity_element["people"]
            for person in people_list:
                self.reverse_identity_dict[person] = identity

    def print_identity_resolution_table(self):
        print(f"number of people in the dictionary is : {len(self.reverse_identity_dict.keys())}")
        for value in self.reverse_identity_dict.values():
            count = 0
            for k1 in self.reverse_identity_dict.keys():
                if self.reverse_identity_dict[k1] == value:
                    count = count + 1
            if count > 1:
                print(f" the number of keys for the value {value} is {count} ")



if __name__ == "__main__":
    start_time = time.time()
    RD = Build_reverse_identity_dictionary()
    RD.reading_identity_and_people_and_building_reverse_identity_dictionary()
