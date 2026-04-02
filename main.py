import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

def run_ibm_pipeline():
    # --- PART 1: WEB SCRAPING ---
    print("🌐 Scraping Programming Languages...")
    url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/datasets/Programming_Languages.html'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    
    lang_data = []
    for row in soup.find('table').find_all('tr')[1:]:
        cols = row.find_all('td')
        lang_data.append({
            'Language': cols[1].getText().strip(),
            'AverageAnnualSalary': int(cols[3].getText().strip().replace('$', '').replace(',', ''))
        })
    df_lang = pd.DataFrame(lang_data)
    df_lang.to_csv('popular-languages.csv', index=False)

    # --- PART 2: API COLLECTION ---
    print("📊 Collecting Job Postings via API...")
    api_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/module%201/datasets/githubposting.json'
    data = requests.get(api_url).json()
    
    techs = ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL Server', 'PostgreSQL', 'MongoDB']
    t_list = list(data['technology'].values())
    j_list = list(data['number of job posting'].values())
    
    job_results = []
    for t in techs:
        count = sum(int(j_list[i]) for i in range(len(t_list)) if t.lower() == t_list[i].lower())
        job_results.append({'Technology': t, 'NumberOfJobs': count})
    
    df_jobs = pd.DataFrame(job_results).sort_values('NumberOfJobs', ascending=False)
    df_jobs.to_excel('job-postings.xlsx', index=False)

    # --- PART 3: VISUALIZATION ---
    print("📈 Creating Demand Chart...")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_jobs, x='NumberOfJobs', y='Technology', hue='Technology', palette='magma', legend=False)
    plt.title('Job Demand by Technology')
    plt.tight_layout()
    plt.savefig('chart_demand.png')
    
    print("\n✅ Success! Check your folder for .csv, .xlsx, and .png files.")

if __name__ == "__main__":
    run_ibm_pipeline()