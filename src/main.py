import imaplib
import email
from PyPDF2 import PdfWriter

# Gmail configuration
EMAIL = 'your_email@gmail.com'
PASSWORD = 'your_password'

# PDF output configuration
OUTPUT_PDF = 'emails_with_my_name.pdf'
MY_NAME = 'Your Name'

def fetch_emails():
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Search for emails mentioning your name
    result, data = mail.search(None, 'UNSEEN')  # Fetch unseen emails
    email_ids = data[0].split()

    emails_with_name = []

    for email_id in email_ids:
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Check if your name is mentioned in the email's subject
        if MY_NAME.lower() in msg['subject'].lower():
            emails_with_name.append(msg['subject'])

    # Create PDF listing emails mentioning your name
    create_pdf(emails_with_name)

def create_pdf(emails):
    # Create a PDF file listing emails mentioning your name
    with open(OUTPUT_PDF, 'wb') as output_file:
        writer = PdfWriter()
        for email_subject in emails:
            writer.add_page()
            writer.set_font("Arial", size=12)
            writer.cell(200, 10, txt=email_subject, ln=True, align="L")
        writer.output(output_file)

if __name__ == '__main__':
    fetch_emails()
