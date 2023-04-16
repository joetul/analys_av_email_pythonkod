import openai
import io
import email
import os

# Set up the OpenAI API client
openai.api_key = ''

folder_path = '' # Change this to the path of the folder containing the eml files

#question1 = str(input("What are you looking for? "))

all_responses_file = 'all_responses.txt'

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

                    #prompt = "In your answer start with Yes or no and follow with an explanation. Do the following text include something about " + question1 + "?: " + email_body
                    prompt = "Analyze the following email: " + email_body
                    #print(prompt)
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
