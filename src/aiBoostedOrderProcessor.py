import openai
import pandas as pd
import json
import urllib.parse
import argparse

def process_order(api_key, email, order_text):
    openai.api_key = api_key
    prompt = f"From customer {email}, the order request is: '{order_text}'. Process this order and extract required structured data."
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200)
    return response.choices[0].text.strip()

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
        print(f"Processing Order from Customer: {row['email']}")
        response = process_order(args.api_key, row['email'], row['order'])
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

if __name__ == "__main__":
    main()
