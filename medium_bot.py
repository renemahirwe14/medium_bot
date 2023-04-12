import openai
import requests
import json
import time
import re

openai.api_key = "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"

pabbly_webhook_url = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NmQwNTZjMDYzZTA0MzU1MjZjNTUzNCI_3D_pc"

post_data = {
    "title": "{{title}}",
    "content_format": "<h1>{{title}}</h1><br><br><br><br><p>{{content.replace('{ ', '\n')}}</p><br><br><br><br>",
    "tags": "{{tag1}},{{tag2}},{{tag3}},{{tag4}},{{tag5}}"
}



def generate_content():
    prompt = ''' Write a 500-word article on any of these topics: AI, Python, data science, machine learning, startups, entrepreneurship, or technology trends.
                 Ensure the article is well-organized into paragraphs and has a professional and unique tone.'''
    
    completions = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048)
    content = completions["choices"][0]["text"].strip()

    # Add subheadings
    content = re.sub(r"(AI|Python|data science|machine learning|startups|entrepreneurship|technology trends)", r"\n\n## \1\n", content)

    # Remove ## character from content
    content = re.sub(r'##\s*', '', content)

    # Add paragraph breaks after every 4-5 lines and at the end of sentences
    content = re.sub(r'((?:[^\n]*\n){5,6}[^\.\n]*[\.\n])', r'\1\n\n', content)

    # Add paragraph breaks at the end of paragraphs that are too long
    content = re.sub(r"(\n[^\n]{100,}\n)", r"\n\n\1", content)

    return content



def generate_title(content):
    prompt = f"Generate a suitable title for the following content:\n\n{content}\n\n"
    completions = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=128)
    title = completions["choices"][0]["text"].strip()
    return title

def generate_tags(content):
    prompt = f"Generate 5 tags related to the following content:\n\n{content}"
    completions = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=128)
    message = completions["choices"][0]["text"]

    tags = message.strip().split("\n")
    tags = [tag.replace("#", "").strip() for tag in tags]

    return tags


def send_text_to_pabbly(title, content, tags):
    headers = {
        "Content-Type": "application/json",
    }
    post_data = {
        "title": title,
        "content_format": f"<h1>{title}</h1><br><br><br><br><p>{content.replace('{{', '<br>').replace('}}', '</p>')}</p>",
        "tags": tags
    }

    # Remove # character from content
    content = re.sub(r'#\s*', '', content)

    response = requests.post(pabbly_webhook_url, headers=headers, json=post_data)
    return response.json()



def main():
    try:
        content = generate_content()
        print(f"Content:\n{content}")

        title = generate_title(content)
        print(f"Title: {title}")

        tags = generate_tags(content)
        print(f"Tags: {', '.join(tags)}")

        response = send_text_to_pabbly(title, content, tags)

        if "success" in response and response["success"]:
            print("Article posted successfully!")
        else:
            print(f"Article Status ----->: {response.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"---->: {type(e).__name__} - {str(e)}")


main()
while True:
    time.sleep(172800)
   
