import openai
import pandas as pd
import json
import urllib.parse

# Initialization
openai.api_key = 'YOUR_OPENAI_API_KEY'
base_amazon_url = "https://www.amazon.com/s?k="

def process_order(email, order_text):
    prompt = f"From customer {email}, the order request is: '{order_text}'. Process this order and extract required structured data."
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200)
    return response.choices[0].text.strip()

def amazon_uri(product_name):
    return base_amazon_url + urllib.parse.quote(product_name)

df = pd.read_excel("path_to_file.xlsx")  # Replace 'path_to_file.xlsx' with your file path.

all_orders = []

for index, row in df.iterrows():
    print(f"Processing Order from Customer: {row['email']}")
    response = process_order(row['email'], row['order'])
    structured_data = json.loads(response)
    print(structured_data)
    all_orders.append(structured_data)

    if 'ProductName' in structured_data:
        print(f"Amazon Search URL: {amazon_uri(structured_data['ProductName'])}")

# Submit a ChatGPT prompt for summary report
summary_prompt = f"Here is the summary of all orders: {json.dumps(all_orders)}. Provide a summary report."
summary_response = openai.Completion.create(engine="text-davinci-003", prompt=summary_prompt, max_tokens=200)
print(summary_response.choices[0].text.strip())

# Individual customer report
unique_emails = df['email'].unique()
for email in unique_emails:
    individual_orders = [order for order in all_orders if order['Customer email'] == email]
    individual_prompt = f"Here are the orders for {email}: {json.dumps(individual_orders)}. Provide a report based on the customer's orders."
    individual_response = openai.Completion.create(engine="text-davinci-003", prompt=individual_prompt, max_tokens=200)
    print(individual_response.choices[0].text.strip())

