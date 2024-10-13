import requests
from bs4 import BeautifulSoup
import json 

def scrape_tags(repo_url):
    page = requests.get(repo_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all('a', class_='topic-tag')
    extracted_tags = [tag.text.strip() for tag in tags]
    extracted_tags = str(extracted_tags)
    print("Done scraping tags...")
    return extracted_tags

def scrape_md(repo_url):
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/README.md"
    response = requests.get(raw_url)
    md = response.text.strip().splitlines()
    md = str(md)
    print("Done scraping markdown...")
    return md

def scrape_dependencies(repo_url):
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/requirements.txt"
    response = requests.get(raw_url)
    dependencies = response.text.strip().splitlines()
    dependencies = str(dependencies)
    print("Done scraping dependencies...")
    return dependencies

def scrape_issues(repo_url):
    issues_url = repo_url + "/issues"
    page = requests.get(issues_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    issue_titles = soup.find_all('a', class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title')
    issues = []
    for issue in issue_titles:
        issue_number = issue.get('href').split('/')[-1]
        issue_title = issue.text.strip()
        issues.append(f"Issue #{issue_number}: {issue_title}")
    print("Done scraping issues...")
    print(issues)
    return issues

def scrape_pull_requests(repo_url):
    pulls_url = repo_url + "/pulls"
    page = requests.get(pulls_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    pull_request_titles = soup.find_all('a', class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title')
    pull_requests = []
    for pr in pull_request_titles:
        pr_number = pr.get('href').split('/')[-1]
        pr_title = pr.text.strip()
        pull_requests.append(f"Pull Request #{pr_number}: {pr_title}")
    print("Done scraping pull requests...")
    print(pull_requests)
    return pull_requests

def scrape_commits(repo_url):
    commits_url = repo_url + "/commits"
    page = requests.get(commits_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    script_tag = soup.find('script', {'data-target': 'react-app.embeddedData'})
    
    if script_tag:
        json_data = json.loads(script_tag.string)
        commit_groups = json_data['payload']['commitGroups']

        commits = []
        for group in commit_groups:
            for commit in group['commits']:
                commit_hash = commit['oid'][:7] 
                commit_message = commit['shortMessage']
                commits.append(f"Commit {commit_hash}: {commit_message}")

        print("Done scraping commit history...")
        print(commits)
        return commits
    else:
        print("Could not find the required script tag with commit data.")
        return []