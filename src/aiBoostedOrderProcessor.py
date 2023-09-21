import warnings
from urllib3.exceptions import NotOpenSSLWarning
import openai
import pandas as pd
import json
import urllib.parse
import argparse
import requests

warnings.simplefilter('ignore', category=NotOpenSSLWarning)

def call_openai_api(prompt, openai_key):
    headers = {
        "Authorization": f"Bearer {openai_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "get-4-0613",
        "prompt": prompt,
        "function_call": {
            "name": "process_order",
            "parameters": {
                "customer_email": "",
                "product_name": "",
                "quantity": 0,
                "ManualProcessingRequired": False,
                "CustomerSupportRequired": ""
            }
        },
        "max_tokens": 1000
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    response_text = response.json()["choices"][0]["text"].strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Error: Could not decode the response into JSON. Response was: {response_text}")
        return None

def process_order(openai_key, email, order_request):
    prompt = f"Convert the order request: '{order_request}' from '{email}' into JSON."
    return call_openai_api(prompt, openai_key)

def amazon_uri(product_name):
    return f"https://www.amazon.com/s?k={urllib.parse.quote(product_name)}"

def main():
    parser = argparse.ArgumentParser(description="Process orders from Excel using OpenAI GPT API.")
    parser.add_argument("api_key", help="Your OpenAI API key")
    parser.add_argument("excel_path", help="Path to the Excel file with orders")
    args = parser.parse_args()

    df = pd.read_excel(args.excel_path)
    all_orders = []

    for index, row in df.iterrows():
        response = process_order(args.api_key, row['email'], row['order'])
        try:
            structured_data = json.loads(response)
            
            if not structured_data or 'product_name' not in structured_data:
                print(f"Unexpected response for order {row['order']} from {row['email']}: {response}")
                continue
            
            all_orders.append(structured_data)

            if 'product_name' in structured_data:
                print(f"Amazon Search URL: {amazon_uri(structured_data['product_name'])}")

        except json.JSONDecodeError:
            print(f"Error: Could not decode the response into JSON. Response was: {response}")
            continue

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

if __name__ == "__main__":
    main()
