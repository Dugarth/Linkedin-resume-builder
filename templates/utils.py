import openai
from docx2txt import process
import requests

def get_job_description(job_query, api_key):
    url = "https://jobsearcher.p.rapidapi.com/search"
    querystring = {"q": job_query, "country": "US"}
    headers = {
        'X-RapidAPI-Key': "9cc58a660amshb2823861842fa65p110cdajsn034838827075",
        'X-RapidAPI-Host': "jsearch.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200 and 'jobs' in response.json():
        return response.json()['jobs'][0]['body']
    else:
        return None

def generate_resume(doc_path, job_description, api_key):
    openai.api_key = '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'
    text = process(doc_path)
    prompt = f"I have a resume with the following details:\n{text}\nAnd I am applying for a job with this description:\n{job_description}\nHow should I modify my resume?"

    response = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=prompt,
      max_tokens=500,
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
      ]
    )

    resume = response['choices'][0]['message']['content']

    with open('resume_modified.txt', 'w') as f:
        f.write(resume)
