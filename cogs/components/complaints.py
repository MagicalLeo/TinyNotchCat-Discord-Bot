import pickle
import random

class Complaint:
    def __init__(self, file = 'docs/complaints.pkl'):
        self.file = file
        self.complaints = []
        self.__load_complaints()

    def __load_complaints(self):
        try:
            with open(self.file, 'rb') as f:
                self.complaints = pickle.load(f)
        except FileNotFoundError:
            print('complaint file not found')
            self.complaints = []

    def __save_complaints(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.complaints, f)
    
    def add_complaint(self, complaint):
        self.complaints.append(complaint)
        self.__save_complaints()
    
    def get_complaint(self):
        if len(self.complaints) == 0:
            return None
        return random.choice(self.complaints)

    def clear_complaints(self):
        self.complaints = []
        self.__save_complaints()