## About:
Created an autonomous AI codegen tool that takes in a GitHub url, collects repo issues, pull requests, and more.

Uses this context to query X for recent arXiv papers and feature updates to take insight from (ex. new python dependency, security updates, novel research findings, etc.)

Automatically updates code using updated knowledge from these research papers and X. 

Generates and executes new code within a Replit shell to safely test out updated changes without affecting the original codebase. 

## Usage: 
```bash
# Clone the repository
git clone https://github.com/jw-source/OpenKevin
```
```bash
# Add API keys to .env

# Create venv
python3 -m venv .venv

# Set the venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```
