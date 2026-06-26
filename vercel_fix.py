import json, os, urllib.request, urllib.error

TOKEN = os.environ.get('VERCEL_TOKEN')
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def api(method, path, data=None):
    url = f'https://api.vercel.com{path}'
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:500]}

# 1. 获取最新生产部署
print("=== 最新部署 ===")
deploys = api('GET', '/v1/projects/openclaw') 
print(f"Project accountId: {deploys.get('accountId')}")

# 2. 查最新的 production deployments
deployments = api('GET', '/v1/projects/openclaw/deployments?target=production&limit=1')
if 'error' in deployments:
    print(f"查部署失败: {deployments}")
else:
    print(json.dumps(deployments, indent=2)[:2000])

# 3. 查所有deployments
all_deploys = api('GET', '/v1/deployments?projectId=openclaw&limit=3')
print(f"\n=== 最近部署 ===")
print(json.dumps(all_deploys, indent=2)[:2000])
