from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import logging
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

def create_logger(name, level=logging.DEBUG):
    """Create and configure a logger."""
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler())
    return logger

def extract_post_request(request):
    """Extract POST request body as JSON."""
    try:
        return json.loads(request.body.decode('utf-8'))
    except ValueError as err:
        logging.error(err)
        return {}

def crawl_website(url):
    """Crawl website and return the HTML content."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    driver.quit()

    return html

def extract_product_list(html):
    """Extract product list from HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    products = []
    product_items = soup.find_all('li', class_='item')
    
    for product in product_items:
        try:
            title = product.find('a').text.strip()
        except AttributeError:
            title = 'N/A'
        try:
            product_id = product['data-id']
        except KeyError:
            product_id = 'N/A'
        try:
            link = product.find('a')['href']
        except (KeyError, TypeError):
            link = 'N/A'

        products.append({
            'title': title,
            'id': product_id,
            'link': f"https://www.thegioididong.com{link}" if link != 'N/A' else link
        })
    
    return products

def extract_info(title):
    """Extract structured information from product title."""
    clean_title = title.replace('\n', ' ').strip()
    product_name = re.search(r'(?<=Tặng Office)(.*?)(?=RAM)', clean_title)
    if not product_name:
        product_name = re.search(r'(?<=Trả góp 0%)(.*?)(?=RAM)', clean_title)
    product_name = product_name.group(0).strip() if product_name else 'N/A'

    price = re.search(r'(\d{1,3}(?:\.\d{3}){2,})₫', clean_title)
    price = price.group(0) if price else 'N/A'

    previous_price = re.findall(r'(\d{1,3}(?:\.\d{3}){2,})₫', clean_title)
    previous_price = previous_price[1] if len(previous_price) > 1 else 'N/A'

    promote = re.search(r'-\d{1,2}%', clean_title)
    promote = promote.group(0) if promote else 'N/A'
    status = 1 if 'Mẫu mới' in clean_title else 0

    return product_name, price, previous_price, promote, status

def get_product_details(driver, product_id, url):
    """Fetch detailed product information from URL."""
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    details = {}
    image_url = ''
    
    try:
        spec_section_id = f"specification-item-{product_id}"
        spec_section = soup.select_one(f"div#{spec_section_id}")
        if spec_section:
            spec_items = spec_section.select("ul.text-specifi li")
            for item in spec_items:
                key = item.find('strong').text.strip() if item.find('strong') else 'N/A'
                value = item.find('span').text.strip() if item.find('span') else 'N/A'
                details[key] = value

        image_section_id = f"specification-img-{product_id}"
        image_tag = soup.select_one(f"div#{image_section_id} img")
        image_url = image_tag['data-src'] if image_tag else 'N/A'
    except Exception as e:
        logging.error(f"Error extracting details from {url}: {e}")

    return {
        'details': details,
        'image': image_url,
    }

def fetch_product_details(row):
    """Fetch detailed information for a single product."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService()

    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        if row['link'] != 'N/A':
            full_url = row['link']
            product_id = row['id']
            product_data = get_product_details(driver, product_id, full_url)
            row['details'] = json.dumps(product_data['details'])
            row['image'] = 'https:' + product_data['image']
        else:
            row['details'] = json.dumps({})
            row['image'] = 'N/A'
    print(row)
    return row

def crawl_task():
    logger = create_logger("product_scraper")
    url = "https://www.thegioididong.com/laptop#c=44&o=13&pi=14"
    html_content = crawl_website(url)
    return html_content

def extract_task(html_content):
    products = extract_product_list(html_content)
    data_preprocess = pd.DataFrame(products)
    data_preprocess[['Product_Name', 'Price', 'Previous_Price', 'Promote', 'Status']] = data_preprocess['title'].apply(
        lambda x: pd.Series(extract_info(x))
    )
    data_preprocess['Manufacturer'] = data_preprocess['Product_Name'].apply(lambda x: x.split()[0])
    return data_preprocess

def details_task(data_preprocess):
    detailed_products = data_preprocess.apply(fetch_product_details, axis=1)
    detailed_products.to_csv("products.csv", index=False)
    logger = create_logger("product_scraper")
    logger.info("Scraping completed. Data saved to 'products.csv'.")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    owner='Thanh',
    dag_id='product_scraper',
    default_args=default_args,
    description='Crawl data from thegioididong.com',
    schedule_interval=timedelta(days=1),
)

crawl = PythonOperator(
    task_id='crawl_website',
    python_callable=crawl_task,
    dag=dag,
)

extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_task,
    op_args=["{{ task_instance.xcom_pull(task_ids='crawl_website') }}"],
    dag=dag,
)

details = PythonOperator(
    task_id='get_details',
    python_callable=details_task,
    op_args=["{{ task_instance.xcom_pull(task_ids='extract_data') }}"],
    dag=dag,
)

crawl >> extract >> details