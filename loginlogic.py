import pandas as pd
 # Read the spreadsheet
df = pd.read_csv('/home/alen/Desktop/llm_model/notification_data/data - Sheet1.csv')

def login(username, password):
    if ((df['Username'] == username) & (df['Password'] == password)).any():
        return True  # Login successful
    else:
        return False  # Login failed


