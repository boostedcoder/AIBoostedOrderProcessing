# AI Boosted Order Processing

This tool processes customer orders from an Excel sheet using the OpenAI GPT API.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/AIBoostedOrderProcessing.git
```

2. Navigate to the repository:
```bash
cd AIBoostedOrderProcessing
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

6. Run the Script:
```
python src/aiBoostedOrderProcessor.py <OpenAI_API_KEY> <path_to_excel_file.xlsx>
```

### Command-line Arguments:

1. `OpenAI_API_KEY`: This is your OpenAI GPT API key. It's required for the script to interact with the OpenAI GPT API for processing the orders.

2. `path_to_excel_file.xlsx`: This is the path to your Excel file containing the customer orders. Each row in the Excel file should have two columns: the first one for the customer's email address and the second one for their product order request in natural language.

## Note

Ensure you replace `your-username` in the `git clone` URL with your actual GitHub username.
This README provides a detailed step-by-step guide on setting up the project, installing dependencies, and running the script with the required command-line arguments.
