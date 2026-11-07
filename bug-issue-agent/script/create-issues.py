import json
import urllib.request
import urllib.parse

# ---------------------------------------------------------------------------
# 1. GITLAB
# ---------------------------------------------------------------------------
def create_gitlab_issue(domain, project_id, token, title, description=""):
    encoded_project_id = urllib.parse.quote(str(project_id), safe="")
    url = f"https://{domain}/api/v4/projects/{encoded_project_id}/issues"
    
    headers = {
        "PRIVATE-TOKEN": token,
        "Content-Type": "application/json"
    }
    payload = json.dumps({"title": title, "description": description}).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# ---------------------------------------------------------------------------
# 2. GITHUB
# ---------------------------------------------------------------------------
def create_github_issue(owner, repo, token, title, body=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
    }
    payload = json.dumps({"title": title, "body": body}).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# ---------------------------------------------------------------------------
# 3. JIRA
# ---------------------------------------------------------------------------
def create_jira_issue(domain, email, api_token, project_key, summary, description="", issue_type="Task"):
    url = f"https://{domain}/rest/api/3/issue"
    
    auth_str = f"{email}:{api_token}"
    auth_b64 = urllib.parse.quote(auth_str)
    import base64
    auth_header = "Basic " + base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = json.dumps({
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}]
                }]
            }
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())