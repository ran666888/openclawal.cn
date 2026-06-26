import json, os, urllib.request

token = os.environ.get('VERCEL_TOKEN')
req = urllib.request.Request(
    'https://api.vercel.com/v1/projects/openclaw',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)

for a in data.get('alias', []):
    print(f"domain: {a['domain']}, deployment: {a.get('deployment')}, env: {a.get('environment')}, target: {a.get('target')}")

print(f"\nProtection: {json.dumps(data.get('ssoProtection', {}), indent=2)}")
