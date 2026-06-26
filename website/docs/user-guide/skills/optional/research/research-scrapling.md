---
title: "Scrapling"
sidebar_label: "Scrapling"
description: "Web scraping with Scrapling - HTTP fetching, stealth browser automation, Cloudflare bypass, and spider crawling via CLI and Python"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 乱七八糟

使用 Scrapling 进行网页抓取 - HTTP 抓取、隐形浏览器自动化、Cloudflare 绕过以及通过 CLI 和 Python 进行蜘蛛爬行。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/scrapling` 安装 |
|路径| `可选技能/研究/拼凑` |
|版本 | `1.0.0` |
|作者 |费阿祖尔 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `Web 抓取`、`浏览器`、`Cloudflare`、`Stealth`、`爬行`、`Spider` |
|相关技能| [`duckduckgo-search`](/docs/user-guide/skills/optional/research/research-duckduckgo-search), [`domain-intel`](/docs/user-guide/skills/optional/research/research-domain-intel) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 乱七八糟

[Scrapling](https://github.com/D4Vinci/Scrapling) 是一个网页抓取框架，具有反机器人绕过、隐形浏览器自动化和蜘蛛框架。它提供三种获取策略（HTTP、动态 JS、stealth/Cloudflare）和完整的 CLI。

**此技能仅用于教育和研究目的。** 用户必须遵守本地/国际数据抓取法律并尊重网站服务条款。

## 何时使用

- 抓取静态 HTML 页面（比浏览器工具更快）
- 抓取需要真实浏览器的 JS 渲染页面
- 绕过 Cloudflare Turnstile 或机器人检测
- 使用蜘蛛抓取多个页面
- 当内置的“web_extract”工具没有返回您需要的数据时

## 安装

````bash
pip install "scraping[全部]"
刮刮安装
````

最小安装（仅 HTTP，无浏览器）：
````bash
pip 安装报错
````

仅使用浏览器自动化：
````bash
pip install“scraping[fetchers]”
刮刮安装
````

## 快速参考

|方法|班级 |使用时间 |
|----------|--------|----------|
| HTTP | `Fetcher` / `FetcherSession` |静态页面、API、快速批量请求 |
|动态 | `DynamicFetcher` / `DynamicSession` | JS 渲染内容、SPA |
|隐身| `StealthyFetcher` / `StealthySession` | Cloudflare，反机器人程序保护网站 |
|蜘蛛 | `蜘蛛` |带有链接的多页面抓取|

## CLI 用法

### 提取静态页面

````bash
抓取提取物获取'https://example.com'output.md
````

使用 CSS 选择器和浏览器模拟：

````bash
抓取提取物获取'https://example.com'output.md \
  --css-选择器'.content'\
  --冒充“chrome”
````

### 提取 JS 渲染页面

````bash
抓取提取物 'https://example.com' output.md \
  --css-selector '.dynamic-content' \
  --禁用资源 \
  --网络空闲
````

### 提取受 Cloudflare 保护的页面

````bash
抓取摘录 Stealthy-fetch 'https://protected-site.com' output.html \
  --解决-cloudflare \
  --block-webrtc \
  --隐藏画布
````

### 发布请求

````bash
抓取摘录帖子“https://example.com/api”output.json \
  --json '{"query": "搜索词"}'
````

### 输出格式

输出格式由文件扩展名决定：
- `.html` -- 原始 HTML
- `.md` -- 转换为 Markdown
- `.txt` -- 纯文本
- `.json` / `.jsonl` -- JSON

## Python：HTTP 抓取

### 单个请求

````蟒蛇
从 scrapling.fetchers 导入 Fetcher

页面 = Fetcher.get('https://quotes.toscrape.com/')
引号 = page.css('.quote .text::text').getall()
对于引号中的 q：
    打印（q）
````

### 会话（持久 Cookie）

````蟒蛇
从 scrapling.fetchers 导入 FetcherSession

使用 FetcherSession(impersonate='chrome') 作为会话：
    page = session.get('https://example.com/', Stealthy_headers=True)
    links = page.css('a::attr(href)').getall()
    对于 links[:5] 中的链接：
        子 = session.get(链接)
        print(sub.css('h1::text').get())
````

### 发布/放置/删除

````蟒蛇
page = Fetcher.post('https://api.example.com/data', json={"key": "value"})
page = Fetcher.put('https://api.example.com/item/1', data={"name": "updated"})
页面 = Fetcher.delete('https://api.example.com/item/1')
````

### 使用代理

````蟒蛇
页面 = Fetcher.get('https://example.com', proxy='http://user:pass@proxy:8080')
````

## Python：动态页面（JS 渲染）

对于需要 JavaScript 执行的页面（SPA、延迟加载内容）：

````蟒蛇
从 scrapling.fetchers 导入 DynamicFetcher

页面 = DynamicFetcher.fetch('https://example.com', headless=True)
data = page.css('.js-loaded-content::text').getall()
````

### 等待特定元素

````蟒蛇
页面 = DynamicFetcher.fetch(
    'https://example.com',
    wait_selector=('.结果', '可见'),
    网络空闲=真，
）
````

### 禁用资源以提高速度

阻止字体、图像、媒体、样式表（快约 25%）：

````蟒蛇
从 scrapling.fetchers 导入 DynamicSession

使用 DynamicSession(headless=True,disable_resources=True,network_idle=True) 作为会话：
    页面 = session.fetch('https://example.com')
    items = page.css('.item::text').getall()
````

### 自定义页面自动化

````蟒蛇
从 playwright.sync_api 导入页面
从 scrapling.fetchers 导入 DynamicFetcher

defscroll_and_click（页面：页面）：
    page.mouse.wheel(0, 3000)
    page.wait_for_timeout(1000)
    page.click('button.load-more')
    page.wait_for_selector('.额外结果')

page = DynamicFetcher.fetch('https://example.com', page_action=scroll_and_click)
results = page.css('.extra-results .item::text').getall()
````

## Python：隐身模式（反机器人绕过）

对于受 Cloudflare 保护或大量指纹识别的站点：

````蟒蛇
从 scrapling.fetchers 导入 StealthyFetcher

页面 = StealthyFetcher.fetch(
    'https://protected-site.com',
    无头=真，
    solve_cloudflare=真，
    block_webrtc=真，
    hide_canvas=真，
）
content = page.css('.protected-content::text').getall()
````

### 秘密会议

````蟒蛇
从 scrapling.fetchers 导入 StealthySession

使用 StealthySession(headless=True,solve_cloudflare=True) 作为会话：
    page1 = session.fetch('https://protected-site.com/page1')
    page2 = session.fetch('https://protected-site.com/page2')
````

## 元素选择

所有获取器都使用以下方法返回一个“Selector”对象：

### CSS 选择器

````蟒蛇
page.css('h1::text').get() # 第一个 h1 文本
page.css('a::attr(href)').getall() # 所有链接 href
page.css('.quote .text::text').getall() # 嵌套选择
````

### XPath

````蟒蛇
page.xpath('//div[@class="content"]/text()').getall()
page.xpath('//a/@href').getall()
````

### 查找方法

````蟒蛇
page.find_all('div', class_='quote') # 按标签+属性
page.find_by_text('阅读更多', tag='a') # 按文本内容
page.find_by_regex(r'\$\d+\.\d{2}') # 通过正则表达式模式
````

### 相似元素

查找具有相似结构的元素（对于产品列表等有用）：

````蟒蛇
第一个产品 = page.css('.产品')[0]
all_similar = first_product.find_similar()
````

### 导航

````蟒蛇
el = page.css('.target')[0]
el.parent # 父元素
el.children # 子元素
el.next_sibling # 下一个兄弟
el.prev_sibling # 上一个同级
````

## Python：Spider 框架

对于多页面抓取，链接如下：

````蟒蛇
从 scrapling.spiders 导入 Spider、请求、响应

类 QuotesSpider(蜘蛛):
    名称=“引号”
    start_urls = ["https://quotes.toscrape.com/"]
    并发请求数 = 10
    下载延迟 = 1

    异步 def parse(self, 响应: 响应):
        对于response.css('.quote')中的引用：
            产量{
                "文本": quote.css('.text::text').get(),
                "作者": quote.css('.author::text').get(),
                "标签": quote.css('.tag::text').getall(),
            }

        next_page = response.css('.next a::attr(href)').get()
        如果下一页：
            产量响应.follow(next_page)

结果 = QuotesSpider().start()
print(f"刮掉了 {len(result.items)} 引号")
result.items.to_json("quotes.json")
````

### 多会话蜘蛛

将请求路由到不同的 fetcher 类型：

````蟒蛇
从 scrapling.fetchers 导入 FetcherSession、AsyncStealthySession

类SmartSpider（蜘蛛）：
    名称=“聪明”
    start_urls = ["https://example.com/"]

    defconfigure_sessions（自我，经理）：
        manager.add（“快”，FetcherSession（impersonate =“chrome”））
        manager.add（“隐形”，AsyncStealthySession（无头= True），懒惰= True）

    异步 def parse(self, 响应: 响应):
        对于response.css('a::attr(href)').getall()中的链接：
            如果链接中“受保护”：
                产量请求（链接，sid =“隐形”）
            其他：
                产量请求（链接，sid =“快”，回调= self.parse）
````

### 暂停/恢复爬行

````蟒蛇
蜘蛛 = QuotesSpider(crawldir="./crawl_checkpoint")
Spider.start() # Ctrl+C 暂停，重新运行从检查点恢复
````

## 陷阱

- **需要浏览器安装**：在 pip install 之后运行 `scrapling install` -- 如果没有它，`DynamicFetcher` 和 `StealthyFetcher` 将失败
- **超时**：DynamicFetcher/StealthyFetcher 超时以 **毫秒** 为单位（默认 30000），Fetcher 超时以 **秒** 为单位
- **Cloudflare 绕过**：`solve_cloudflare=True` 增加 5-15 秒的获取时间 - 仅在需要时启用
- **资源使用**：StealthyFetcher 运行真正的浏览器 - 限制并发使用
- **法律**：在抓取之前务必检查 robots.txt 和网站 ToS。该图书馆用于教育和研究目的
- **Python版本**：需要Python 3.10+