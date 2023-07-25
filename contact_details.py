import re
import docx
import sys
sys.path.append('C:/Users/admin/Documents/resume_rating')
from preprocessing import docx_processing  as doc, textract_processing as txt
def extract_contact_info(resume_text):
    # Regular expressions for extracting phone numbers and email addresses
    phone_regex = r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *[x/#]{1}(\d+))?\b"
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    # Extract phone numbers
    phone_numbers = re.findall(phone_regex, resume_text)
    phone_numbers = ["".join(number) for number in phone_numbers]

    # Extract email addresses
    email_addresses = re.findall(email_regex, resume_text)

    return phone_numbers, email_addresses

# Example usage
#resume_documents = [
#    "John Doe\nPhone: 123-456-7890\nEmail: john@example.com",
#    "Jane Smith\nPhone: (555) 123-4567\nEmail: jane.smith@example.com"
#]
#
#for resume in resume_documents:
#    phone_numbers, email_addresses = extract_contact_info(resume)
#    print("Phone numbers:", phone_numbers)
#    print("Email addresses:", email_addresses)
#    print("--------")
#
def get_resume_text(resume_location):
    resume_list = []
    for doct in resume_location:
        resume_list.append(txt.get_content_as_string(doct))
    return resume_list
