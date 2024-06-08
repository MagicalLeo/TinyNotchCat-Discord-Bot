import pickle


COMPLAINTS_FILE = 'complaints.pkl'
complaints = []

def load_complaints():
    global complaints
    try:
        with open(COMPLAINTS_FILE, 'rb') as f:
            complaints = pickle.load(f)
    except FileNotFoundError:
        complaints = []

def save_complaints():
    with open(COMPLAINTS_FILE, 'wb') as f:
        pickle.dump(complaints, f)