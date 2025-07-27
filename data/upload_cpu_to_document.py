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
                    'Product_Name': row['Công nghệ CPU'],
                    'Number of Cores': row['Số nhân'],
                    'Number of Threads': row['Số luồng'],
                    'CPU Speed': row['Tốc độ CPU'],
                    'Max Speed': row['Tốc độ tối đa'],
                    'Cache Memory': row['Bộ nhớ đệm'],
                    'RAM': row['RAM'],
                    'RAM Type': row['Loại RAM'],
                    'RAM Bus Speed': row['Tốc độ Bus RAM'],
                    'Maximum Supported RAM': row['Hỗ trợ RAM tối đa'],
                    'Hard Drive': row['Ổ cứng'],
                    'Screen': row['Màn hình'],
                    'Resolution': row['Độ phân giải'],
                    'Refresh Rate': row['Tần số quét'],
                    'Color Gamut': row['Độ phủ màu'],
                    'Screen Technology': row['Công nghệ màn hình'],
                    'Graphics Card': row['Card màn hình'],
                    'Sound Technology': row['Công nghệ âm thanh'],
                    'Ports': row['Cổng giao tiếp'],
                    'Wireless Connection': row['Kết nối không dây'],
                    'Webcam': row['Webcam'],
                    'Other Features': row['Tính năng khác'],
                    'Keyboard Light': row['Đèn bàn phím'],
                    'Size': row['Kích thước'],
                    'Weight': row['Khối lượng tịnh'],
                    'Material': row['Chất liệu'],
                    'Battery Information': row['Thông tin Pin'],
                    'Charger Power': row['Công suất bộ sạc'],
                    'Operating System': row['Hệ điều hành'],
                    'Release Date': row['Thời điểm ra mắt'],
                    'Card Slot': row['Khe đọc thẻ nhớ'],
                    'Cooling': row['Tản nhiệt'],
                    'Touchscreen': row['Màn hình cảm ứng'],
                }
            )
    return data

# Sample CSV data
data = read_csv("project/data/expanded_product_data_cleaned.csv")

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
