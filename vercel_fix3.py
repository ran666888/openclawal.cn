import json, os, urllib.request, urllib.error

TOKEN = os.environ['VERCEL_TOKEN']
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
        return {'error': e.code, 'body': e.read().decode()[:1000]}

DEPLOYMENT_UID = 'dpl_B8uGe5WUWKCeCVfCwVU9NX3C4Wgf'
DOMAIN = 'openclawal.cn'
TEAM = 'team_gtsmcbv7u3ls0t2R2rpKY8U6'

# 删除旧的域别名
print("=== 删旧别名 ===")
result = api('DELETE', f'/v1/aliases/domain?domain={DOMAIN}&teamId={TEAM}')
print(json.dumps(result, indent=2)[:500])

# 重新添加到部署
print("\n=== 加别名到当前部署 ===")
result2 = api('POST', f'/v1/deployments/{DEPLOYMENT_UID}/aliases?teamId={TEAM}', {
    'alias': DOMAIN
})
print(json.dumps(result2, indent=2)[:1000])
