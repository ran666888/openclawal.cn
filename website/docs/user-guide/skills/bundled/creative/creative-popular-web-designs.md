---
title: "Popular Web Designs — 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS"
sidebar_label: "Popular Web Designs"
description: "54 real design systems (Stripe, Linear, Vercel) as HTML/CSS"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 流行的网页设计

54 个真实的设计系统（Stripe、Linear、Vercel）作为 HTML/CSS。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/流行网页设计` |
|版本 | `1.0.0` |
|作者 | OpenClaw + Teknium（设计系统源自 VoltAgent/awesome-design-md）|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 流行的网页设计

54 个现实世界的设计系统可供在生成 HTML/CSS 时使用。每个模板捕获一个
网站完整的视觉语言：调色板、排版层次、组件样式、间距
系统、阴影、响应行为和具有精确 CSS 值的实用代理提示。

## 相关设计技巧

- **`claude-design`** — 用于设计*流程和品味*（范围简短，
  生成变体、验证本地 HTML 工件、避免 AI 设计失误）。
  当用户想要精心设计的页面样式时，将其与此技能配对
  在知名品牌：“claude-design”驱动工作流程之后，该技能提供
  视觉词汇。
- **`design-md`** — 当可交付成果是正式的 DESIGN.md 代币规范时使用
  文件，而不是渲染的工件。

## 如何使用

1. 从下面的目录中选择一个设计
2.加载它： `skill_view(name="popular-web-designs", file_path="templates/<site>.md")`
3. 生成 HTML 时使用设计令牌和组件规范
4. 与“generative-widgets”技能配对，通过 cloudflared 隧道提供结果

每个模板的顶部都包含一个 **OpenClaw 实施说明** 块，其中包含：
- CDN 字体替换和 Google Fonts `<link>` 标签（准备粘贴）
- 主要和等宽字体的 CSS 字体系列堆栈
- 提醒使用“write_file”进行 HTML 创建和“browser_vision”进行验证

## HTML 生成模式

````html
<!DOCTYPE html>
<html lang="en">
<头>
  <元字符集=“UTF-8”>
  <meta name =“viewport”content =“width = device-width，initial-scale = 1.0”>
  <标题>页面标题</标题>
  <!-- 从模板的 Hermes 注释中粘贴 Google 字体 <link> -->
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
  <风格>
    /* 将模板的调色板应用为 CSS 自定义属性 */
    ：根{
      --颜色背景：#ffffff；
      --颜色文本：#171717；
      --颜色重音：#533afd；
      /* ...来自模板第 2 节的更多内容 */
    }
    /* 应用模板第 3 节中的排版 */
    身体{
      字体系列：“Inter”、system-ui、sans-serif；
      颜色：var(--颜色文本)；
      背景：var(--color-bg);
    }
    /* 应用模板第 4 节中的组件样式 */
    /* 应用模板第 5 节的布局 */
    /* 应用模板第 6 节中的阴影 */
  </风格>
</头>
<正文>
  <!-- 使用模板中的组件规格进行构建 -->
</正文>
</html>
````

使用“write_file”写入文件，使用“generative-widgets”工作流程（cloudflared 隧道）提供服务，
并使用“browser_vision”验证结果以确认视觉准确性。

## 字体替换参考

大多数网站使用 CDN 无法提供的专有字体。每个模板都映射到 Google 字体
保留设计特征的替代品。常见映射：

|专有字体| CDN 替代品 |人物 |
|---|---|---|
| Geist / Geist Sans | Geist Geist（在 Google 字体上）|几何压缩跟踪 |
| Geist 单声道 | Geist Mono（在 Google 字体上）|干净的等宽字体、连字|
| sohne-var（条纹）|来源 Sans 3 |轻量优雅|
|伯克利单声道 | JetBrains 单声道 |技术等宽 |
| Airbnb 谷物 VF | DM Sans | DM Sans |圆润、友好的几何形状|
|循环 (Spotify) | DM Sans | DM Sans |几何，温暖|
| FigmaSans|国际米兰|清洁人文主义者|
| Pin Sans（Pinterest）| DM Sans | DM Sans |友善、圆润|
| NVIDIA-欧洲、中东和非洲 | Inter（或 Arial 系统）|工业、清洁 |
| CoinbaseDisplay/Sans | DM Sans | DM Sans |几何，值得信赖|
|优步移动 | DM Sans | DM Sans |大胆、紧致|
| HashiCorp Sans | HashiCorp Sans国际米兰|企业，中立|
| waldenburg正​​常 (理智) |太空格罗泰斯克 |几何，略凝|
| IBM Plex Sans/Mono | IBM Plex Sans/Mono | IBM Plex Sans/Mono IBM Plex Sans/Mono | IBM Plex Sans/Mono | IBM Plex Sans/Mono可在 Google 字体上使用 |
|魔方（哨兵）|魔方 |可在 Google 字体上使用 |

当模板的 CDN 字体与原始字体（Inter、IBM Plex、Rubik、Geist）匹配时，不会
发生替代损失。当使用替代品时（DM Sans 代表 Circular，Source Sans 3
对于 sohne-var)，请严格遵循模板的粗细、大小和字母间距值 —
它们比特定字体具有更多的视觉识别性。

## 设计目录

### 人工智能与机器学习

|模板|网站 |风格|
|---|---|---|
| `克劳德.md` |人类克劳德 |温暖的赤土色，干净的编辑布局 |
| `cohere.md` |连贯|充满活力的渐变、数据丰富的仪表板美学 |
| `elevenlabs.md` |十一实验室 |黑暗的电影 UI，音频波形美学 |
| `minimax.md` |极小极大 |带有霓虹灯装饰的大胆深色界面 |
| `mistral.ai.md` |米斯特拉尔人工智能 |法国设计的极简主义，紫色调|
| `ollama.md` |奥拉玛 |终端优先，单色简约 |
| `opencode.ai.md` |开放代码人工智能 |以开发人员为中心的深色主题，完整的等宽字体 |
| `复制.md` |复制|干净的白色画布，代码转发 |
| `runwayml.md` |跑道ML |电影般的深色 UI，媒体丰富的布局 |
| `together.ai.md` |一起人工智能|技术性、蓝图式设计|
| `电压nt.md` |伏特代理|虚空黑色帆布，祖母绿口音，终端原生 |
| `x.ai.md` | xAI |鲜明的单色、未来主义极简主义、完整的等宽空间 |

### 开发者工具和平台

|模板|网站 |风格|
|---|---|---|
| `cursor.md` |光标|光滑的深色界面，渐变色调 |
| `expo.md` |世博会|深色主题、紧密的字母间距、以代码为中心 |
| `线性.app.md` |线性|超简约深色模式，精准，紫色调 |
| `可爱的.md` |可爱|有趣的渐变，友好的开发美学 |
| `mintlify.md` |精简|干净、绿色、阅读优化 |
| `posthog.md` |邮差猪 |有趣的品牌、开发人员友好的深色 UI |
| `raycast.md` |光线投射 |时尚的深色镀铬、充满活力的渐变装饰 |
| `重新发送.md` |重新发送 |最小的深色主题，等宽字体 |
| `哨兵.md` |哨兵|深色仪表板，数据密集，粉紫色调 |
| `supabase.md` |苏帕巴斯|深色翡翠主题，代码优先的开发者工具 |
| `超人.md` |超人|高级深色 UI、键盘优先、紫色发光 |
| `vercel.md` |韦尔塞尔 |黑白精准，Geist字体系统|
| `warp.md` |经纱 |类似深色 IDE 的界面，基于块的命令 UI |
| `zapier.md` |扎皮尔 |温暖的橙色，友好的插画驱动|

### 基础设施和云

|模板|网站 |风格|
|---|---|---|
| `clickhouse.md` |点击屋|黄色调的技术文档风格 |
| `composio.md` |作曲|现代黑暗与多彩集成图标|
| `hashicorp.md` |哈希公司|企业级干净、黑白|
| `mongodb.md` | MongoDB |绿叶品牌、开发者文档焦点 |
| `理智.md` |理智 |红色调，内容优先的编辑布局 |
| `stripe.md` |条纹|标志性紫色渐变，重量 300 优雅 |

### 设计与生产力

|模板|网站 |风格|
|---|---|---|
| `airtable.md` |空中桌 |丰富多彩、友好、结构化的数据美学 |
| `cal.md` |加州.com |干净中性的 UI，面向开发人员的简单性 |
| `clay.md` |粘土|有机的形状、柔和的渐变、艺术导向的布局 |
| `figma.md` |菲格玛 |充满活力的多色，俏皮又专业|
| `framer.md` |成帧器|大胆的黑色和蓝色、运动第一、设计前卫 |
| `对讲机.md` |对讲 |友好的蓝色调色板，对话式 UI 模式 |
| `miro.md` |米罗|亮黄色调，无限画布美感|
| `notion.md` |概念|温暖的极简主义、衬线标题、柔软的表面 |
| `pinterest.md` |兴趣 |红色调、砖石网格、图像优先布局 |
| `webflow.md` |网络流 |蓝色调、精美的营销网站美学 |

### 金融科技与加密货币

|模板|网站 |风格|
|---|---|---|
| `coinbase.md` |币库 |干净的蓝色身份、以信任为中心、制度感|
| `kraken.md` |克拉肯 |紫色调的深色用户界面，数据密集的仪表板 |
| `revolut.md` |革命|光滑的深色界面、渐变卡、金融科技精度 |
| `明智的.md` |明智|亮绿色口音，友好清晰 |

### 企业与消费者

|模板|网站 |风格|
|---|---|---|
| `airbnb.md` |爱彼迎 |温暖的珊瑚色、摄影驱动的圆形用户界面 |
| `苹果.md` |苹果|优质留白、SF Pro、电影图像 |
| `宝马.md` |宝马|深色优质表面，精确的工程美学 |
| `ibm.md` | IBM|IBM碳设计系统，结构化蓝色调色板|
| `nvidia.md` |英伟达 |绿黑能量，科技力量美学|
| `spacex.md` |太空探索技术公司 |鲜明的黑白、全出血图像、未来感 |
| `spotify.md` | Spotify |深色、粗体、专辑封面驱动的充满活力的绿色 |
| `uber.md` |优步 |大胆黑白，紧身型，都市能量|

## 选择设计

将设计与内容相匹配：

- **开发者工具/仪表板：** Linear、Vercel、Supabase、Raycast、Sentry
- **文档/内容站点：** Mintlify、Notion、Sanity、MongoDB
- **营销/登陆页面：** Stripe、Framer、Apple、SpaceX
- **深色模式用户界面：** 线性、光标、ElevenLabs、扭曲、超人
- **轻量/干净的用户界面：** Vercel、Stripe、Notion、Cal.com、Replicate
- **俏皮/友好：** PostHog、Figma、Lovable、Zapier、Miro
- **高级/豪华：** Apple、BMW、Stripe、Super human、Revolut
- **数据密集/仪表板：** Sentry、Kraken、Cohere、ClickHouse
- **等宽/终端美学：** Ollama、OpenCode、x.ai、VoltAgent