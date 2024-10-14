import csv
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import re

# Function to use Ollama's Llama 3 model for prompt generation
def prompts(prompt):    
    ollama = Ollama(
        base_url='http://localhost:11434',
        model="llama3"
    )
    print("Invoking..")
    answer = ollama.invoke(prompt)
    return answer

def extract_altered_prompt(response):
    result=response.split("Altered Prompt:")
    ap=None
    if len(result) > 1:
       ap=result[1] 
    return ap
    
# Sample prompt dataset (you can replace this with a better dataset)
prompts_list = [
    "What is the capital of France?",
    "Explain the theory of relativity in simple terms.",
    "What are the benefits of renewable energy?"
]

# Function to generate altered prompts using Ollama's Llama 3
def generate_altered_prompt(original_prompt):
    # Prompt template to instruct Ollama's Llama 3 for subtle alteration
    prompt_template = PromptTemplate(
        template="""
        Original prompt: {prompt}
        Subtly alter the above prompt and return only the altered version in the following format:

        Altered Prompt: "<Your altered prompt here>"
        """,
        input_variables=["prompt"],
    )
    
    prompt = prompt_template.format(prompt=original_prompt)
    
    # Generate the altered prompt using Ollama's Llama 3 model
    response = prompts(prompt)
    print(response)
    
    # Extract altered prompt from the response
    altered_prompt = extract_altered_prompt(response)
    
    return altered_prompt

# CSV file to store the synthetic dataset
csv_file = 'synthetic_dataset.csv'

# Write the header to the CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['original_prompt', 'altered_prompt'])  # Header

# Append original and altered prompts to CSV line by line
with open("malignant.csv", mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # Skip the header (assuming there's one)
    next(reader)
    
    # Loop through the rows and access the first column
    for row in reader:
        original_prompt = row[2]  # Access the first column (original_prompt in this case)
        altered_prompt = generate_altered_prompt(original_prompt)
        
        # Write the original and altered prompts to the CSV file
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([original_prompt, altered_prompt])  # Write altered prompt

print(f"Synthetic dataset created and saved to '{csv_file}'.")
