import pandas as pd
import random

# Define the number of unique customers and the number of orders
num_customers = 5
num_orders = 10

# Generate unique customer email addresses
customer_emails = [f"customer{str(i)}@example.com" for i in range(num_customers)]

# List of sample products
products = [
    "Laptop",
    "Smartphone",
    "Headphones",
    "Smartwatch",
    "Mouse",
    "Keyboard",
    "Monitor",
    "Speaker",
    "Tablet",
    "Charger"
]

# Generate random orders
orders = []
for _ in range(num_orders):
    email = random.choice(customer_emails)
    product = random.choice(products)
    quantity = random.randint(1, 10)
    order_text = f"I would like to order {quantity} {product}(s)."
    orders.append([email, order_text])

# Create a DataFrame and write to Excel
df = pd.DataFrame(orders, columns=["email", "order"])
df.to_excel("sample_orders.xlsx", index=False)
