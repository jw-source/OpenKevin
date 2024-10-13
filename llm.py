from openai import OpenAI
from scrape_github import scrape_tags, scrape_md, scrape_dependencies, scrape_issues, scrape_pull_requests, scrape_commits
import json
import re
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1",
)

def generate_x_keywords(repo_url):
    tags = scrape_tags(repo_url)
    md = scrape_md(repo_url)
    dependencies = scrape_dependencies(repo_url)
    issues = scrape_issues(repo_url)
    pull_requests = scrape_pull_requests(repo_url)
    commit_history = scrape_commits(repo_url)
    repo_info = f"Commits: {commit_history}. Pull Requests: {pull_requests}. Issues: {issues}. Dependencies: {dependencies}. README.md: {md}. Tags: {tags}"
    response = client.chat.completions.create(
        model="grok-preview",
        seed=1,
        messages=[
        {
            "role": "system",
            "content": "You are an expert at finding and extracting keywords from a Github repo to query X. This is very important: Your goal is to use these keywords to find relevant research papers. Output the 5 most important keywords in JSON format"
        },
        {   "role": "user", 
            "content": repo_info
        },
    ],
    )
    output = response.choices[0].message.content
    output = output.replace("```", "").replace("json", "")
    print(output)
    data = json.loads(output)
    keywords = data["keywords"]
    print("Done generating keywords...")
    return keywords, repo_info

def generate_top_10(repo_info, context):
    response = client.chat.completions.create(
        model="grok-preview",
        seed=1,
        messages=[
        {
            "role": "system",
            "content": "You are an expert at creating a priority list of tasks to implement in an open source Github Repository based on research. This is very important: Your goal is to output the top 10 tasks to implement in the repository based on the information provided."
        },
        {   "role": "user", 
            "content": f"Potentially Useful Research: {context}. Repo Info: {repo_info}."
        },
    ],
    )
    output = response.choices[0].message.content
    tasks = re.split(r'\n(?=\d+\.)', output.strip())
    print("Done generating top 10 tasks...")
    return tasks
