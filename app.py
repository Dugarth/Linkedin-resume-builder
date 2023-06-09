from flask import Flask, render_template, request, send_file
import docx2txt
import http.client
import json
import openai
import PyPDF2
from docx import Document
from urllib.parse import quote
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        resume = request.files["resume"]
        text = extract_text_from_file(resume)
        job_title = request.form.get("job_title", "")
        location = request.form.get("location", "")
        job_info = f"{job_title}, {location}"
        job_offers = get_job_offers(job_info)
        
        if len(job_offers) == 0:
            print("No job offers were found with these parameters.")
            return render_template("index.html", message="No job offers were found with the provided parameters. Please try again.")

        job_offers = filter_job_descriptions(job_offers)
        resume_summaries = generate_resume_summaries(text, job_offers)
        output_file_path = save_resume_summaries(resume_summaries, job_offers)
        print("Resume summaries saved to:", output_file_path)
        return send_file(output_file_path, as_attachment=True)
    else:
        return render_template("index.html")


def extract_text_from_file(file):
    file_extension = file.filename.split(".")[-1]

    if file_extension == "pdf":
        # Extract text from PDF
        reader = PyPDF2.PdfFileReader(file)
        text = "\n".join(reader.getPage(i).extract_text() for i in range(reader.numPages))
        print("PDF text extracted")
    elif file_extension == "docx":
        # Extract text from Word document
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        print("DOCX text extracted")
    else:
        # Extract text from plain text file
        text = file.read().decode("utf-8")
        print("Text extracted from file")

    return text

def get_job_offers(job_info):
    headers = {
        'X-RapidAPI-Key': "9cc58a660amshb2823861842fa65p110cdajsn034838827075",
        'X-RapidAPI-Host': "jsearch.p.rapidapi.com"
    }

    encoded_job_info = quote(job_info)
    query = f"{encoded_job_info}"
    print("Querying job offers for:", job_info)

    conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
    conn.request("GET", f"/search?query={query}&page=1&num_pages=1&date_posted=month", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data = json.loads(data.decode("utf-8"))
    job_offers = data.get('data', [])[:10]
    job_offers_count = len(job_offers)

    if job_offers_count == 0:
        print("No job offers found for these parameters.")
        return []

    print(f"Job offers retrieved: {job_offers_count}")

    return job_offers

def generate_resume_summaries(text, job_offers):
    openai.api_key = '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'

    user_info = text

    resume_summaries = []
    for i, job in enumerate(job_offers, 1):
        job_title = job['job_title']
        job_description = job['job_description']
        print(f"Generating resume summary for Job Offer {i} - Title: {job_title}")
        prompt = f"""
        Take my job experience and skills below and apply it to the requested experience:
        {user_info}

        Using the information from the job posting below, match my relevant experience and skills to the wording of the posting and write a resume for me. Be sure to focus on the language and words used in the job posting when writing the resume to increase the chances of being selected as a candidate.

        Job Title: {job_title}
        Job Description: {job_description}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are the best resume writer."},
                {"role": "user", "content": prompt}
            ]
        )

        response_content = response['choices'][0]['message']['content']
        resume_summaries.append(response_content)

    return resume_summaries

def save_resume_summaries(resume_summaries, job_offers):
    output_file_path = "resume_summaries.txt"

    with open(output_file_path, "w", encoding="utf-8") as f:
        for i, (summary, job_offer) in enumerate(zip(resume_summaries, job_offers), 1):
            f.write(f"Job Offer {i}:\n")
            f.write(f"Summary: {summary}\n")
            f.write(f"Job Apply Link: {job_offer['job_apply_link']}\n\n")

    return output_file_path

def split_text_into_chunks(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def analyze_text(text):
    # Split text into chunks
    chunks = split_text_into_chunks(text)

    # Summarize each chunk using GPT-3.5
    openai.api_key = "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"
    summaries = []

    for chunk in chunks:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Please summarize the following text:\n\n{chunk}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )
        summaries.append(response.choices[0].text.strip())

    # Combine summaries and get the final summary
    combined_text = " ".join(summaries)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following text:\n\n{combined_text}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    final_summary = response.choices[0].text.strip()

    return final_summary

def filter_job_descriptions(job_offers):
    for job in job_offers:
        job_description = job['job_description']
        summary = analyze_text(job_description)
        job['job_description'] = summary
    return job_offers

if __name__ == "__main__":
    app.run(debug=True)