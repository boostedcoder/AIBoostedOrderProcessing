# Orders Processor

This is a tool to process customer orders from an Excel sheet using the OpenAI GPT API.

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate to the repository:
```bash
cd orders_processor
```

3. Create a virtual environment:
```bash
python -m venv venv
```

4. Activate the virtual environment:
```bash
# Windows:
venv\Scripts\activate

# macOS and Linux:
source venv/bin/activate
```

5. Install the requirements:
```bash
pip install -r requirements.txt
```

6. Run the `process_orders.py` script:
```bash
python src/process_orders.py
```

## Note
Ensure you replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key in the `process_orders.py` script.
