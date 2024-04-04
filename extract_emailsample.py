import os
import base64
import email
import imaplib

# Create a folder to store the extracted emails. folder will be created on same directory where you save this code.
if not os.path.exists("ExtractedEmails"):
    os.makedirs("ExtractedEmails")

# Connect to Gmail, you need to enable IMAP access. 
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("Email", "pwd")
mail.select("inbox")

# Search for the top 10 emails in the inbox
result, data = mail.search(None, "ALL")
ids = data[0].split()[-10:]

# Loop through each email and extract the sender, subject, and body
for id in ids:
    result, data = mail.fetch(id, "(RFC822)")
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    sender = email_message["from"]
    subject = email_message["subject"]
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode("utf-8")
            break

 # Write the extracted information to a file with a fixed file name
fixed_file_name = "my_email.txt"
with open(f"ExtractedEmails/{fixed_file_name}", "w") as f:
    f.write(f"Sender: {sender}\nSubject: {subject}\n\n{body}")

mail.close()
mail.logout()
