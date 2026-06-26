import json, os, urllib.request, urllib.error

TOKEN = os.environ.get('VERCEL_TOKEN', '')
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def api(method, path, data=None, team_id=None):
    url = f'https://api.vercel.com{path}'
    if team_id:
        url += f'?teamId={team_id}'
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:1000]}

TEAM = 'team_gtsmcbv7u3ls0t2R2rpKY8U6'
DEPLOYMENT_UID = 'dpl_B8uGe5WUWKCeCVfCwVU9NX3C4Wgf'
DOMAIN = 'openclawal.cn'

# Method 1: Create alias for the deployment
print("=== 尝试 1: 创建部署别名 ===")
result = api('POST', f'/v1/deployments/{DEPLOYMENT_UID}/aliases', {
    'domain': DOMAIN,
    'redirect': None
}, team_id=TEAM)
print(json.dumps(result, indent=2)[:1500])

# If that fails, try method 2
if 'error' in result:
    print("\n=== 尝试 2: 添加域名到项目 ===")
    result2 = api('POST', f'/v10/projects/openclaw/domains', {
        'name': DOMAIN
    }, team_id=TEAM)
    print(json.dumps(result2, indent=2)[:1500])
