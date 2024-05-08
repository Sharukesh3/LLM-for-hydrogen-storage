import PyPDF2
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("shayanathif/BART_Hydrogen_Model")
tokenizer = AutoTokenizer.from_pretrained("shayanathif/BART_Hydrogen_Model")

def summarize(input_text=None, pdf_file=None):
    if input_text is None and pdf_file is None:
        return "Please provide either text input or a PDF file."
    elif input_text:
        # Input is a text string
        input_data = input_text
    else:
        # Input is a PDF file
        try:
            with open(pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                input_data = ''

                # Extract text from each page
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    input_data += page.extract_text()
        except Exception as e:
            # Handle file reading errors
            print(f"Error reading file: {e}")
            return "Error reading the file."

    # Tokenize the input text
    inputs = tokenizer(input_data, return_tensors="pt", truncation=True, max_length=1024)

    # Generate the summary
    summary_ids = model.generate(**inputs, max_length=150, num_beams=4, early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary