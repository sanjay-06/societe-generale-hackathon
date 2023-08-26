import jwt,os.path, time

from config.db import collection
from fastapi import APIRouter, Depends,Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from config.db import permission
from config.jobs import JobMatcherApp
import urllib

jobs=APIRouter()
templates=Jinja2Templates(directory="html")

JobMatcher = JobMatcherApp()
user_data = {
        "name": "John Doe",
        "degree": [
            {
                "type": "Bachelor's",
                "specialization": "Computer Science",
                "start_date": "2016-09-01",
                "end_date": "2020-06-30",
                "college": "Tech University"
            }
        ],
        "interested_role": "Data Scientist",
        "experience": [
            {
                "company": "TechCorp",
                "role": "Data Analyst",
                "span": {"start_date": "2020-01-15", "end_date": "2022-02-28"},
                "desc": "Analyzed customer data for insights.",
                "tool_tech": "Python, SQL"
            },
            {
                "company": "Data Insights",
                "role": "Junior Data Scientist",
                "span": {"start_date": "2022-03-15", "end_date": "2023-05-20"},
                "desc": "Developed machine learning models for predictive analysis.",
                "tool_tech": "Python, TensorFlow, scikit-learn"
            }
        ],
        "skills": "Python, Machine Learning, Data Analysis",
        "expected_salary": "$80,000",
        "most_recent_company": "Data Insights",
        "most_recent_designation": "Junior Data Scientist"
    }
job_dataset = [
  {
    "Job_Title": "Software Engineer",
    "Company_Name": "TechCo",
    "Required_Skills": ["Python", "JavaScript", "SQL", "HTML", "CSS"],
    "Experience_Years_Required": 2,
    "Description": "Develop and maintain web applications using modern technologies."
  },
  {
    "Job_Title": "Data Scientist",
    "Company_Name": "DataAnalytics Inc.",
    "Required_Skills": ["Python"],
    "Experience_Years_Required": 3,
    "Description": "Extract insights from data and develop predictive models."
  },
  {
    "Job_Title": "Graphic Designer",
    "Company_Name": "DesignStudio",
    "Required_Skills": ["Adobe Photoshop", "Illustrator", "UI/UX Design", "Typography"],
    "Experience_Years_Required": 2,
    "Description": "Create visually appealing designs for digital and print media."
  },
  {
    "Job_Title": "Product Manager",
    "Company_Name": "InnovateTech",
    "Required_Skills": ["Product Development", "Market Research", "Project Management", "Communication"],
    "Experience_Years_Required": 4,
    "Description": "Lead the development and launch of new products."
  },
  {
    "Job_Title": "Sales Representative",
    "Company_Name": "SalesConnect",
    "Required_Skills": ["Communication", "Negotiation", "Client Relationship", "B2B Sales"],
    "Experience_Years_Required": 1,
    "Description": "Meet sales targets and build strong client relationships."
  },
  {
    "Job_Title": "Network Administrator",
    "Company_Name": "TechNet Solutions",
    "Required_Skills": ["Network Security", "LAN/WAN", "Firewalls", "IT Troubleshooting"],
    "Experience_Years_Required": 3,
    "Description": "Maintain and secure the organization's network infrastructure."
  },
  {
    "Job_Title": "Content Writer",
    "Company_Name": "ContentHub",
    "Required_Skills": ["Content Creation", "SEO", "Copywriting", "Social Media"],
    "Experience_Years_Required": 2,
    "Description": "Produce engaging and SEO-friendly content for websites and blogs."
  },
  {
    "Job_Title": "Financial Analyst",
    "Company_Name": "FinancePro",
    "Required_Skills": ["Financial Modeling", "Excel", "Data Analysis", "Investment Research"],
    "Experience_Years_Required": 3,
    "Description": "Analyze financial data to provide insights and recommendations."
  },
  {
    "Job_Title": "UX Designer",
    "Company_Name": "DesignInnovate",
    "Required_Skills": ["User Research", "Wireframing", "Prototyping", "Usability Testing"],
    "Experience_Years_Required": 2,
    "Description": "Design user-centric and intuitive digital experiences."
  },
  {
    "Job_Title": "Mechanical Engineer",
    "Company_Name": "Mechatronix",
    "Required_Skills": ["CAD Design", "Thermodynamics", "Material Science", "Prototyping"],
    "Experience_Years_Required": 3,
    "Description": "Design and develop mechanical components and systems."
  }
]

JobMatcher.set_jobs(job_dataset)

@jobs.post("/jobs", response_class=HTMLResponse)
async def submit_jobs(request : Request):
    form_data = await request.body()

    # Decode the bytes to a string and parse the form data
    form_data_str = form_data.decode("utf-8")
    parsed_data = urllib.parse.parse_qs(form_data_str)

    # Process the parsed form data
    processed_data = {}
    for key, value_list in parsed_data.items():
        processed_data[key] = value_list[0]
    # if content_type != "application/x-www-form-urlencoded":
    #     raise HTTPException(status_code=400, detail="Invalid content type")

    # # Process and parse the form_data here
    # processed_data = {}
    # key_value_pairs = form_data.split("&")
    # for pair in key_value_pairs:
    #     key, value = pair.split("=")
    #     processed_data[key] = value

    print(processed_data)
    import json
    processed_data['experience'] = [{"span": json.loads(processed_data['experience'])}]

    best_matches = JobMatcher.find_best_job_matches(processed_data)
    matches = JobMatcher.get_top_jobs(best_matches)
    return JSONResponse(content=matches)