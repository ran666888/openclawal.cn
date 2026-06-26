---
sidebar_position: 8
title: "Extending the CLI"
description: "Build wrapper CLIs that extend the OpenClaw TUI with custom widgets, keybindings, and layout changes"
---
# 扩展 CLI

OpenClaw 在 `HermesCLI` 上公开了受保护的扩展挂钩，因此包装器 CLI 可以添加小部件、键绑定和布局自定义，而无需覆盖 1000 多行 `run()` 方法。这可以使您的扩展与内部更改脱钩。

## 扩展点

有五种延伸接缝可供选择：

|钩|目的|当...时覆盖
|------|---------|------------------|
| `_get_extra_tui_widgets()` |将小部件注入布局 |您需要一个持久的 UI 元素（面板、状态行、迷你播放器）|
| `_register_extra_tui_keybindings(kb, *, input_area)` |添加键盘快捷键 |您需要热键（切换面板、传输控件、模式快捷键）|
| `_build_tui_layout_children(**小部件)` |完全控制小部件排序 |您需要重新排序或包装现有的小部件（罕见）|
| `process_command()` |添加自定义斜杠命令 |您需要`/mycommand`处理（预先存在的钩子）|
| `_build_tui_style_dict()` |自定义提示_工具包样式 |您需要自定义颜色或样式（预先存在的挂钩）|

前三个是新的受保护的钩子。最后两个已经存在。

## 快速入门：包装器 CLI

````蟒蛇
#!/usr/bin/env python3
"""my_cli.py — 扩展 Hermes 的示例包装器 CLI。"""

从 cli 导入 HermesCLI
从prompt_toolkit.layout导入FormattedTextControl，窗口
从prompt_toolkit.filters导入条件


MyCLI 类（HermesCLI）：

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._panel_visible = False

    def _get_extra_tui_widgets(自身):
        """在状态栏上方添加可切换的信息面板。"""
        cli_ref = 自我
        返回[
            窗口（
                FormattedTextControl(lambda: "📊 我的自定义面板内容"),
                高度=1，
                过滤器=条件（lambda：cli_ref._panel_visible），
            ),
        ]

    def _register_extra_tui_keybindings(self, kb, *, input_area):
        """F2 切换自定义面板。"""
        cli_ref = 自我

        @kb.add("f2")
        def _toggle_panel（事件）：
            cli_ref._panel_visible = 不是 cli_ref._panel_visible

    def process_command(self, cmd: str) -> bool:
        """添加 /panel 斜线命令。"""
        如果 cmd.strip().lower() == "/panel":
            self._panel_visible = 不是 self._panel_visible
            如果 self._panel_visible，则状态 =“可见”，否则“隐藏”
            print(f"面板现在处于 {state}")
            返回真
        返回 super().process_command(cmd)


如果 __name__ == "__main__":
    cli = MyCLI()
    cli.run()
````

运行它：

````bash
cd ~/.hermes/hermes-agent
源 .venv/bin/activate
蟒蛇 my_cli.py
````

## 钩子参考

### `_get_extra_tui_widgets()`

返回要插入到 TUI 布局中的提示工具包小部件列表。小部件出现在**间隔符和状态栏之间** - 在输入区域上方但在主输出下方。

````蟒蛇
def _get_extra_tui_widgets(self) -> 列表：
    return [] # 默认值：没有额外的小部件
````

每个小部件应该是一个提示工具包容器（例如“Window”、“ConditionalContainer”、“HSplit”）。使用 `ConditionalContainer` 或 `filter=Condition(...)` 使小部件可切换。

````蟒蛇
从prompt_toolkit.layout导入ConditionalContainer、Window、FormattedTextControl
从prompt_toolkit.filters导入条件

def _get_extra_tui_widgets(自身):
    返回[
        条件容器(
            Window(FormattedTextControl("状态：已连接")，高度=1),
            过滤器=条件(lambda: self._show_status),
        ),
    ]
````

### `_register_extra_tui_keybindings(kb, *, input_area)`

在 OpenClaw 注册自己的键绑定之后、构建布局之前调用。将您的键绑定添加到“kb”。

````蟒蛇
def _register_extra_tui_keybindings(self, kb, *, input_area):
    pass # 默认值：没有额外的按键绑定
````

参数：
- **`kb`** —prompt_toolkit 应用程序的 `KeyBindings` 实例
- **`input_area`** — 主要的 `TextArea` 小部件，如果您需要读取或操作用户输入

````蟒蛇
def _register_extra_tui_keybindings(self, kb, *, input_area):
    cli_ref = 自我

    @kb.add("f3")
    def _clear_input（事件）：
        输入区域.text = ""

    @kb.add("f4")
    def _insert_template（事件）：
        输入区域.text =“/搜索”
````

**避免与内置键绑定发生冲突**：“Enter”（提交）、“Escape Enter”（换行）、“Ctrl-C”（中断）、“Ctrl-D”（退出）、“Tab”（自动建议接受）。功能键 F2+ 和 Ctrl-组合通常是安全的。

### `_build_tui_layout_children(**小部件)`

仅当您需要完全控制小部件排序时才覆盖此设置。大多数扩展应该使用 `_get_extra_tui_widgets()` 来代替。

````蟒蛇
def _build_tui_layout_children（自我，*，sudo_widget，secret_widget，
    批准小部件，澄清小部件，model_picker_widget =无，
    spinner_widget=无、间隔、status_bar、input_rule_top、
    图像栏、输入区域、输入规则机器人、语音状态栏、
    完成菜单）->列表：
````

默认实现返回（任何“None”小部件都被过滤掉）：

````蟒蛇
[
    窗口(高度=0), # 锚点
    sudo_widget, # sudo 密码提示（有条件）
    Secret_widget, # 秘密输入提示（有条件）
    approval_widget, # 危险命令批准（有条件）
    clarify_widget, # 澄清问题 UI（有条件）
    model_picker_widget, # 模型选择器覆盖（有条件）
    spinner_widget, # 思维旋转器（有条件）
    spacer, # 填充剩余的垂直空间
    *self._get_extra_tui_widgets(), # 您的小部件位于此处
    status_bar, # 模型/令牌/上下文状态行
    input_rule_top, # ──── 输入上方的边框
    image_bar, # 附加图像指示器
    input_area, # 用户文本输入
    input_rule_bot, # ──── 输入下方边框
    voice_status_bar, # 语音模式状态（有条件）
    completions_menu, # 自动完成下拉菜单
]
````

## 布局图

默认布局从上到下：

1. **输出区域**——滚动对话历史记录
2. **垫片**
3. **额外的小部件** - 来自`_get_extra_tui_widgets()`
4. **状态栏** — 模型、上下文百分比、经过的时间
5. **图像栏** — 附加图像计数
6. **输入区**——用户提示
7. **语音状态**——录音指示灯
8. **完成菜单** — 自动完成建议

## 提示

- **状态更改后使显示无效**：调用`self._invalidate()`来触发prompt_toolkit重画。
- **访问代理状态**：`self.agent`、`self.model`、`self.conversation_history` 都可用。
- **自定义样式**：覆盖 `_build_tui_style_dict()` 并添加自定义样式类的条目。
- **斜线命令**：覆盖 `process_command()`，处理您的命令，并为其他所有内容调用 `super().process_command(cmd)`。
- **除非绝对必要，否则不要重写 `run()`** — 扩展钩子的存在是为了避免这种耦合。