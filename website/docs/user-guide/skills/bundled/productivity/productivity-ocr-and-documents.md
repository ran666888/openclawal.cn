---
title: "Ocr And Documents — Extract text from PDFs/scans (pymupdf, marker-pdf)"
sidebar_label: "Ocr And Documents"
description: "Extract text from PDFs/scans (pymupdf, marker-pdf)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Ocr 和文档

从 PDF/扫描件中提取文本（pymupdf、marker-pdf）。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/生产力/ocr 和文档` |
|版本 | `2.3.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `PDF`、`文档`、`研究`、`Arxiv`、`文本提取`、`OCR` |
|相关技能| [`powerpoint`](/docs/user-guide/skills/bundled/productivity/productivity-powerpoint) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# PDF 和文档提取

对于 DOCX：使用“python-docx”（解析实际文档结构，比 OCR 好得多）。
对于 PPTX：请参阅“powerpoint”技能（使用具有完整幻灯片/笔记支持的“python-pptx”）。
此技能涵盖 **PDF 和扫描文档**。

## 第 1 步：远程 URL 可用吗？

如果文档有 URL，**始终先尝试 `web_extract`**：

````
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
````

这通过 Firecrawl 处理 PDF 到 Markdown 的转换，没有本地依赖性。

仅在以下情况下使用本地提取：文件位于本地、web_extract 失败或需要批处理。

## 步骤 2：选择本地提取器

|特色| pymupdf (~25MB) |标记-pdf (~3-5GB) |
|--------------------|-----------------|---------------------|
| **基于文本的 PDF** | ✅ | ✅ |
| **扫描的 PDF (OCR)** | ❌ | ✅（90 多种语言）|
| **表格** | ✅（基本）| ✅（高精度）|
| **方程/LaTeX** | ❌ | ✅ |
| **代码块** | ❌ | ✅ |
| **表格** | ❌ | ✅ |
| **页眉/页脚删除** | ❌ | ✅ |
| **阅读顺序检测** | ❌ | ✅ |
| **图像提取** | ✅（嵌入）| ✅（有上下文）|
| **图像 → 文本 (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown 输出** | ✅（通过 pymupdf4llm）| ✅（原生，更高品质）|
| **安装尺寸** | 〜25MB | ~3-5GB（PyTorch + 型号）|
| **速度** |即时 | ~1-14s/页 (CPU), ~0.2s/页 (GPU) |

**决定**：使用 pymupdf 除非您需要 OCR、方程、表格或复杂的布局分析。

如果用户需要标记功能但系统缺少~5GB可用磁盘：
> “本文档需要 OCR/高级提取 (marker-pdf)，PyTorch 和模型需要 ~5GB。您的系统有 [X]GB 可用空间。选项：释放空间，提供 URL，以便我可以使用 web_extract，或者我可以尝试 pymupdf，它适用于基于文本的 PDF，但不适用于扫描文档或方程。”

---

## pymupdf（轻量级）

````bash
pip 安装 pymupdf pymupdf4llm
````

**通过帮助程序脚本**：
````bash
python script/extract_pymupdf.py document.pdf # 纯文本
python script/extract_pymupdf.py document.pdf --markdown # Markdown
python script/extract_pymupdf.py document.pdf --tables # 表
python script/extract_pymupdf.py document.pdf --images out/ # 提取图像
python script/extract_pymupdf.py document.pdf --metadata # 标题、作者、页码
python script/extract_pymupdf.py document.pdf --pages 0-4 # 特定页面
````

**内联**：
````bash
python3-c“
导入 pymupdf
doc = pymupdf.open('文档.pdf')
对于文档中的页面：
    打印(page.get_text())
”
````

---

## 标记-pdf（高质量 OCR）

````bash
# 首先检查磁盘空间
python 脚本/extract_marker.py --check

pip 安装标记-pdf
````

**通过帮助程序脚本**：
````bash
python script/extract_marker.py document.pdf # Markdown
python script/extract_marker.py document.pdf --json # 带有元数据的 JSON
python script/extract_marker.py document.pdf --output_dir out/ # 保存图像
python script/extract_marker.py Scand.pdf # 扫描的 PDF (OCR)
python script/extract_marker.py document.pdf --use_llm # LLM 提升准确性
````

**CLI**（与标记pdf一起安装）：
````bash
mark_single document.pdf --output_dir ./output
标记 /path/to/folder --workers 4 # 批处理
````

---

## Arxiv 论文

````
# 仅摘要（快速）
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# 全文
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# 搜索
web_search(query="arxiv GRPO 强化学习 2026")
````

## 拆分、合并和搜索

pymupdf 本地处理这些 - 使用 `execute_code` 或内联 Python：

````蟒蛇
# 拆分：将第 1-5 页提取到新的 PDF
导入 pymupdf
doc = pymupdf.open("报告.pdf")
新= pymupdf.open()
对于范围（5）内的 i：
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save(“pages_1-5.pdf”)
````

````蟒蛇
# 合并多个PDF
导入 pymupdf
结果 = pymupdf.open()
对于 ["a.pdf", "b.pdf", "c.pdf"] 中的路径：
    结果.insert_pdf(pymupdf.open(路径))
结果.保存（“合并.pdf”）
````

````蟒蛇
# 在所有页面中搜索文本
导入 pymupdf
doc = pymupdf.open("报告.pdf")
对于 i，枚举（doc）中的页面：
    结果 = page.search_for("收入")
    如果结果：
        print(f"第 {i+1} 页：{len(结果)} 匹配(es)")
        打印（page.get_text（“文本”））
````

不需要额外的依赖项——pymupdf 在一个包中涵盖了拆分、合并、搜索和文本提取。

---

## 注释

- `web_extract` 始终是 URL 的首选
- pymupdf 是安全的默认设置 - 即时、无模型、在任何地方都可以使用
-marker-pdf 适用于 OCR、扫描文档、方程式、复杂布局 — 仅在需要时安装
- 两个帮助程序脚本都接受“--help”以充分使用
- 首次使用时，marker-pdf 将 ~2.5GB 模型下载到 `~/.cache/huggingface/`
- 对于 Word 文档：`pip install python-docx`（比 OCR 更好 — 解析实际结构）
- 对于 PowerPoint：请参阅“powerpoint”技能（使用 python-pptx）