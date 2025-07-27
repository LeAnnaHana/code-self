import csv
import requests


def read_csv(file_path):
    data = []
    # Open and read the CSV file
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            data.append(
                {
                    "link": row['link'],
                    "Product_Name": row['Product_Name'],
                    "RAM": row['RAM'],
                    "SSD": row['SSD'],
                    "Price": row['Price'],
                    "Previous_Price": row['Previous_Price'],
                    "Promote": row['Promote'],
                    "Gift": row['Gift'],
                    "Status": row['Status']
                }
            )
    return data

# Sample CSV data
data = read_csv("project/data/Data_TGDD_Preprocess.csv")

api_url = 'http://128.199.221.17:8000/chat/documents/create/'


# Function to create a document for each product
def create_documents(data):
    headers = {'Content-Type': 'application/json'}
    for item in data:
        title = item['Product_Name']
        content = " ;\n ".join([f"{key}: {value}" for key, value in item.items() if key != 'Product_Name'])

        # Create the payload
        payload = {
            "title": title,
            "content": content
        }

        # Send the request
        response = requests.post(api_url, headers=headers, json=payload)

        # Print the response for debugging
        print(f"Sent document for {title}")
        print("Response:", response.status_code, response.text)


# Execute the function
create_documents(data)
