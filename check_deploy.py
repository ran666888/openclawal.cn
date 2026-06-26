import subprocess, json, os

token = os.environ.get("VERCEL_TOKEN", "")
if not token:
    print("NO TOKEN")
    exit(1)

cmd = ['curl', '-s', '-H', f'Authorization: Bearer {token}',
       'https://api.vercel.com/v1/deployments?projectId=prj_HaVxRISyAU1AR93H85dYWsCUY60l&limit=5']

result = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(result.stdout)

for d in data.get('deployments', []):
    msg = d.get('meta', {}).get('githubCommitMessage', '')[:50]
    url = d['url']
    state = d.get('readyState', '?')
    created = d.get('createdAt', '?')
    print(f"{url} | {state} | {created} | {msg}")
