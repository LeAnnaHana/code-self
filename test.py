from .chatbot.memo.signals import create_document_to_vector_db
import pandas as pd
# get data from ./data/cleaned_dat_no_nan.csv
DATA_PATH = './data/cleaned_data_no_nan.csv'
data = pd.read_csv(DATA_PATH)
# save data to database
create_document_to_vector_db(data)
