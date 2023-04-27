import openai
import io
import email
import os

# Set up the OpenAI API client
openai.api_key = ''

folder_path = '' # Change this to the path of the folder containing the eml files



yes_file = 'yes_responses.txt'
no_file = 'no_responses.txt'
all_responses_file = 'all_responses.txt'

# Clear the contents of the text files
open(yes_file, 'w').close()
open(no_file, 'w').close()
open(all_responses_file, 'w').close()



for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith(".eml"):
            with open(os.path.join(root, filename), 'rb') as eml_file:
                email_text = eml_file.read()

                # Use io.BytesIO to create a file-like object from the bytes string
                eml_file_like_object = io.BytesIO(email_text)

                # Parse the EML message
                eml_message = email.message_from_binary_file(eml_file_like_object)

                # Extract the body text from the message
                body_text = None
                for part in eml_message.walk():
                    if part.get_content_type() == 'text/plain':
                        body_text = part.get_payload(decode=True)
                        break

                # Print the body text
                if body_text is not None:
                    email_body = body_text.decode('utf-8')

                    prompt = "Act as an IT forensics investigator, do the following email contain suspect content regarding criminal activity? " + email_body

                    # Generate text with GPT-3
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=50,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )

                    # Print the generated text
                    response_text = response.choices[0].text.strip()
                    print(f"File: {os.path.join(root, filename)} \n{response.choices[0].text}\n")

                    with open(all_responses_file, 'a') as all_f:
                        all_f.write(f"File: {os.path.join(root, filename)}\n{response_text}\n\n")

                    if response_text.lower().startswith("yes"):
                        with open(yes_file, 'a') as yes_f:
                            yes_f.write(f"File: {os.path.join(root, filename)}\n{response_text}\n\n")
                    elif response_text.lower().startswith("no"):
                        with open(no_file, 'a') as no_f:
                            no_f.write(f"File: {os.path.join(root, filename)}\n{response_text}\n\n")
