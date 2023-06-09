# Resume Assistant

Resume Assistant is a web application that helps users tailor their resumes according to specific job postings. It takes a user's resume and job search parameters, finds relevant job postings, and generates custom resume summaries matching the requirements of these job postings.

## Features

1. **File upload:** Users can upload their resumes in PDF, DOCX, or plain text format. The application reads these files and extracts the text for analysis.
2. **Job search:** The application uses the RapidAPI job search API to fetch relevant job postings based on the job title and location provided by the user.
3. **Custom resume generation:** For each job posting, the application uses OpenAI's GPT-3.5 model to generate a custom resume summary that matches the job requirements.

## Setup

Before running the application, please replace the RapidAPI(JSearch) and OpenAI API keys in the script with your own keys. You can obtain these keys by registering on the RapidAPI and OpenAI platforms, respectively.

The API keys can be found in the following functions in the script:

- RapidAPI key: `get_job_offers()`
- OpenAI key: `generate_resume_summaries()`

Please ensure that the keys are correctly replaced before proceeding with the usage of the application.



## Usage

Before running the application, please make sure to replace the RapidAPI and OpenAI API keys in the script with your own. You can find these keys in the `get_job_offers()` and `generate_resume_summaries()` functions, respectively.

1. Run the script with Python.
2. Access the web application in a browser at `http://localhost:5000`.
3. Upload your resume and enter your job search parameters.
4. Click the submit button to generate your custom resume summaries.



## Dependencies

- Flask
- docx2txt
- http.client
- json
- openai
- PyPDF2
- python-docx

## Note

Please replace the API keys in the script with your own before running the application.
