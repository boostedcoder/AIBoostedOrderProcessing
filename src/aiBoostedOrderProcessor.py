import warnings
from urllib3.exceptions import HTTPWarning
import openai
import pandas as pd
import json
import urllib.parse
import argparse

warnings.simplefilter('ignore', category=HTTPWarning)

def call_openai_api(prompt):
    data = {
        "model": "gpt-4-0613",
        'max_tokens': 1000,
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    # Assuming you have set the API key and imported the OpenAI library
    response = openai.ChatCompletion.create(**data)
    return response.choices[0].message['content']


def call_openai_function_api(prompt, function_name, function_schema):
    # Assuming function_name is a user-defined function you're trying to "simulate"
    system_instruction = f"Use the call_{function_name} function to process the following input:"

    data = {
        "model": "gpt-4-0613",
        "functions": [
            function_schema
        ],
        'function_call': {
            'name': 'call_' + function_name,
        },
        'max_tokens': 1000,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
    }

    # Assuming you have set the API key and imported the OpenAI library
    response = openai.ChatCompletion.create(**data)
    return response.choices[0].message['function_call']['arguments']


def process_order(email, order_request):
    prompt = f"Convert the order request: '{order_request}' from '{email}' into JSON."
    function_schema = {
            "name": "call_" + "process_order",
            "description": "",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_email": { "type": "string", "description": "Well formed email of the customer or empty if unknown"},
                        "product_name": { "type": "string", "description": "Short product description or empty if unknown"},
                        "quantity": { "type": "integer", "description": "The count of the product"},
                        "ManualProcessingRequired": { "type": "boolean", "description": "True if the order request does not have complete information"},
                        "CustomerSupportRequired": { "type": "string", "description": "Support questions from the customer if there are any, or empty if none"}
                    }
            }
        }
    return call_openai_function_api(prompt, "process_order", function_schema)

def amazon_uri(product_name):
    return f"https://www.amazon.com/s?k={urllib.parse.quote(product_name)}"

def main():
    parser = argparse.ArgumentParser(description="Process orders from Excel using OpenAI GPT API.")
    parser.add_argument("api_key", help="Your OpenAI API key")
    parser.add_argument("excel_path", help="Path to the Excel file with orders")
    args = parser.parse_args()

    df = pd.read_excel(args.excel_path)
    all_orders = []

    openai.api_key = args.api_key

    for index, row in df.iterrows():
        response = process_order(row['email'], row['order'])
        try:
            structured_data = json.loads(response)
            
            if not structured_data or 'product_name' not in structured_data:
                print(f"Unexpected response for order {row['order']} from {row['email']}: {response}")
                continue

            print(f"Order Processed: {str(structured_data)}")
            
            all_orders.append(structured_data)

            if 'product_name' in structured_data:
                print(f"Amazon Search URL: {amazon_uri(structured_data['product_name'])}")

        except json.JSONDecodeError:
            print(f"Error: Could not decode the response into JSON. Response was: {response}")
            continue

    # Submit a ChatGPT prompt for summary report
    summary_prompt = f"Here is the summary of all orders: {json.dumps(all_orders)}. Provide a summary report."
    summary_response = call_openai_api(summary_prompt)
    print(summary_response)

    # Individual customer report
    unique_emails = df['email'].unique()
    for email in unique_emails:
        individual_orders = [order for order in all_orders if order['customer_email'] == email]
        
        individual_prompt = (
                    f"Here are the orders for customer {email}: {json.dumps(individual_orders)}. "
                    f"Analyze the orders and identify trends such as popular products, average order size, and frequency of orders. "
                    f"Is the customer's spending trending upwards or downwards? "
                    f"What are some recommendations for next steps or upsells for this customer?"
                )        
        individual_response = call_openai_api(individual_prompt)
        print(individual_response)

if __name__ == "__main__":
    main()
