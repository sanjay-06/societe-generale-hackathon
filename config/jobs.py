import numpy as np
import requests
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcherApp:
    def __init__(self):
        self.users = []
        self.jobs = []
        self.mentors = []
        self.freelancers = []

    def add_user(self, user_data):
        self.users.append(user_data)
    
    def add_job(self, job_data):
        self.jobs.append(job_data)
    
    def set_jobs(self, job_database):
        self.jobs = job_database

    def add_mentor(self, mentor_data):
        self.mentors.append(mentor_data)
    
    def add_freelancer(self, freelancer_data):
        self.freelancers.append(freelancer_data)
    
    def calculate_cosine_similarity(self, user_skills, job_skills):
        user_skills = set(user_skills.split(', '))
        job_skills = set(job_skills)
        
        all_skills = list(user_skills.union(job_skills))
        
        user_vector = [1 if skill in user_skills else 0 for skill in all_skills]
        job_vector = [1 if skill in job_skills else 0 for skill in all_skills]
        
        similarity = cosine_similarity([user_vector], [job_vector])
        
        return similarity[0][0]
    

    def calculate_total_experience(self, user_experience):
        total_experience_years = 0
        
        for experience in user_experience:
            start_date = datetime.strptime(experience["span"]["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(experience["span"]["end_date"], "%Y-%m-%d")
            
            experience_duration = (end_date - start_date).days / 365.0  # Calculate experience in years
            total_experience_years += experience_duration
        
        return total_experience_years

    def find_best_job_matches(self, user_data):
        best_matches = []
        user_skills = user_data["skills"]
        
        total_user_experience = self.calculate_total_experience(
            user_data.get("experience", [])
        )
        
        for idx, job in enumerate(self.jobs):
            job_skills = job["Required_Skills"]
            skill_similarity = self.calculate_cosine_similarity(user_skills, job_skills)
            

            job_experience_years_required = job["Experience_Years_Required"]
            experience_relevance = max(
                0, 1 - abs(total_user_experience - job_experience_years_required)
            )
            
            # Combine skill similarity and experience relevance
            combined_similarity = skill_similarity * experience_relevance
            
            best_matches.append((job["Job_Title"], job["Company_Name"], combined_similarity))
        
        best_matches.sort(key=lambda x: x[2], reverse=True)
        return best_matches

    def recommend_courses(self, user_data, job_index):
        job_skills = self.jobs[job_index]["Required_Skills"]
        user_skills = set(user_data["skills"].split(', '))
        print(job_skills,user_skills)
        # Identify skill gap
        skill_gap = [skill for skill in job_skills if skill not in user_skills]
        
        # Suggest relevant courses for skill gap
        suggested_courses = []
        
        for skill in skill_gap:
            # Fetch course names from Open Library API based on skill
            url = f"https://openlibrary.org/search.json?q={skill}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                docs = data.get("docs", [])[:2]
                for doc in docs:
                    course_name = doc.get("title", "Unknown Course")
                    suggested_courses.append(course_name)
        
        return suggested_courses
    
    def suggest_development_plan(self, user_data, target_role):
        user_skills = set(user_data["skills"].split(', '))
        required_skills = None
        
        for job in self.jobs:
            if job["Job_Title"] == target_role:
                required_skills = set(job["Required_Skills"])
                break
        
        if not required_skills:
            return None
        
        skill_gap = required_skills - user_skills
        # Suggest a development plan to acquire missing skills
        suggested_plan = []
        
        for skill in skill_gap:
            # You might use a skill-to-resource mapping for suggesting learning resources
            # Here, we're just generating a simple suggestion
            suggested_plan.append(f"Learn {skill}")
        
        return suggested_plan
    
    def get_top_jobs(self, best_matches):
        jobs_dump = []
        for job_title, company, similarity in best_matches:
            if similarity >0 :
                jobs_dump.append({"designation": job_title,"company": company,"similarity": similarity})
        
        return jobs_dump

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
    "Required_Skills": ["Python", "R", "Machine Learning", "Data Analysis", "Statistical Modeling"],
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


# Example usage
if __name__ == "__main__":
    app = JobMatcherApp()
    
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
    app.set_jobs(job_dataset)
    # app.add_user(user_data)
    
    best_matches = app.find_best_job_matches(user_data)
    print("Best Job Matches:")
    for job_title, company, similarity in best_matches:
        if similarity >0 :
            print(f"Job Title: {job_title}, Company: {company}, Similarity Score: {similarity}")
    
    job_index = 7  # Assuming the user selects the first recommended job
    suggested_courses = app.recommend_courses(user_data, job_index)
    print("Suggested Courses:", suggested_courses)
    
    target_role = "Data Scientist"  # Assuming the user wants to transition to this role
    development_plan = app.suggest_development_plan(user_data, target_role)
    print("Suggested Development Plan:", development_plan)

