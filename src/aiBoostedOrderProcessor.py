import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.simplefilter('ignore', category=NotOpenSSLWarning)

import openai
import pandas as pd
import json
import urllib.parse
import argparse
import requests

def call_openai_api(prompt, openai_key):
    """
    Call the OpenAI API with a given prompt.
    Returns the model's response as a dictionary.
    """
    # Define the endpoint and headers
    endpoint = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {
        "Authorization": f"Bearer {openai_key}",
        "Content-Type": "application/json"
    }

    # Define the data payload
    data = {
        "prompt": prompt,
        "max_tokens": 150  # You can adjust this as needed
    }

    # Make the API request
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()  # Raises an exception for HTTP errors

    # Extract the model's response from the API response
    response_text = response.json()["choices"][0]["text"].strip()

    try:
        # Attempt to convert the response to a dictionary
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Error: Could not decode the response into JSON. Response was: {response_text}")
        return None


def process_order(openai_key, email, order_request):
    # Generating the prompt for ChatGPT
    prompt = (f"Convert the following order request from customer '{email}': '{order_request}' "
              f"into structured JSON with fields 'Customer email', 'Product Name', 'Count of Product', "
              f"'ManualProcessingRequired', and 'CustomerSupportRequired'.")
    
    return call_openai_api(prompt, openai_key)


def amazon_uri(product_name):
    return base_amazon_url + urllib.parse.quote(product_name)

def main():
    parser = argparse.ArgumentParser(description="Process orders from Excel using OpenAI GPT API.")
    parser.add_argument("api_key", help="Your OpenAI API key")
    parser.add_argument("excel_path", help="Path to the Excel file with orders")
    args = parser.parse_args()

    base_amazon_url = "https://www.amazon.com/s?k="

    df = pd.read_excel(args.excel_path)

    all_orders = []

    for index, row in df.iterrows():
        response = process_order(args.api_key, row['email'], row['order'])
        try:
            structured_data = json.loads(response)
            print(structured_data)
            
            if not structured_data or 'ProductName' not in structured_data:
                print(f"Unexpected response for order {row['order']} from {row['email']}: {response}")
                continue
            
            all_orders.append(structured_data)

            if 'ProductName' in structured_data:
                print(f"Amazon Search URL: {amazon_uri(structured_data['ProductName'])}")

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
