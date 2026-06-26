#!/usr/bin/env python3
"""Replace Hermes text references with OpenClaw in HTML files.
Only modifies visible text content, not HTML tags/attributes/IDs."""

import os
import re

BASE = r"C:\Users\50148\projects\openclaw中文社区网站\dist"

FILES = [
    "docs/user-guide/cli/index.html",
    "docs/user-guide/configuration/index.html",
    "docs/user-guide/configuring-models/index.html",
    "docs/user-guide/security/index.html",
    "docs/user-guide/sessions/index.html",
    "docs/user-guide/desktop/index.html",
    "docs/user-guide/docker/index.html",
    "docs/user-guide/features/overview/index.html",
    "docs/user-guide/features/memory/index.html",
    "docs/user-guide/features/skills/index.html",
    "docs/user-guide/features/mcp/index.html",
    "docs/user-guide/features/browser/index.html",
    "docs/user-guide/features/tools/index.html",
    "docs/user-guide/features/cron/index.html",
    "docs/user-guide/features/vision/index.html",
    "docs/user-guide/features/voice-mode/index.html",
    "docs/user-guide/features/web-search/index.html",
]

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # === COMMON REPLACEMENTS (ALL FILES) ===
    
    # 1. ~/.hermes/ → ~/.openclaw/ (path references)
    content = content.replace('~/.hermes/', '~/.openclaw/')
    
    # 2. hermes command in code blocks and text - replace "hermes " with "openclaw " when it's the command
    # But be careful NOT to replace inside HTML attributes like class="hermes-xxx"
    # Strategy: replace "hermes " at word boundaries in text content
    
    # Replace specific command patterns
    content = content.replace('hermes chat ', 'openclaw chat ')
    content = content.replace('hermes config ', 'openclaw config ')
    content = content.replace('hermes desktop ', 'openclaw desktop ')
    content = content.replace('hermes dashboard ', 'openclaw dashboard ')
    content = content.replace('hermes tools ', 'openclaw tools ')
    content = content.replace('hermes doctor ', 'openclaw doctor ')
    content = content.replace('hermes auth ', 'openclaw auth ')
    content = content.replace('hermes uninstall ', 'openclaw uninstall ')
    content = content.replace('hermes update ', 'openclaw update ')
    content = content.replace('hermes logs ', 'openclaw logs ')
    content = content.replace('hermes sessions ', 'openclaw sessions ')
    content = content.replace('hermes portal ', 'openclaw portal ')
    content = content.replace('hermes plugins ', 'openclaw plugins ')
    content = content.replace('hermes cron ', 'openclaw cron ')
    content = content.replace('hermes kanban ', 'openclaw kanban ')
    content = content.replace('hermes profile ', 'openclaw profile ')
    content = content.replace('hermes onboard ', 'openclaw onboard ')
    content = content.replace('hermes setup ', 'openclaw setup ')
    content = content.replace('hermes gateway ', 'openclaw gateway ')
    content = content.replace('hermes -p ', 'openclaw -p ')
    content = content.replace('hermes -c ', 'openclaw -c ')
    content = content.replace('hermes -s ', 'openclaw -s ')
    content = content.replace('hermes --continue', 'openclaw --continue')
    content = content.replace('hermes --resume', 'openclaw --resume')
    content = content.replace('hermes --tui', 'openclaw --tui')
    content = content.replace('hermes --verbose', 'openclaw --verbose')
    content = content.replace('hermes --profile', 'openclaw --profile')
    content = content.replace('hermes --no-color', 'openclaw --no-color')
    content = content.replace('"hermes"', '"openclaw"')
    
    # hermes standalone command (at start or end of lines)
    content = content.replace('>hermes<', '>openclaw<')
    content = content.replace('hermes</span>', 'openclaw</span>')
    
    # 3. hermes-agent service/process name
    content = content.replace('hermes-agent', 'openclaw-agent')
    content = content.replace('hermes-agent-dev', 'openclaw-agent-dev')
    
    # 4. hermes state data path
    content = content.replace('~/.hermes/state.db', '~/.openclaw/state.db')
    
    # 5. systemctl references
    content = content.replace('systemctl status hermes-agent', 'systemctl status openclaw-agent')
    
    # 6. Docker image references
    content = content.replace('nousresearch/hermes-agent', 'openclaw/openclaw-agent')
    
    # 7. OPENCLAW_HOME / OPENCLAW_DESKTOP_CWD etc - already correct, but check for incorrect env vars
    content = content.replace('OPENCLAW_DESKTOP_CWD', 'OPENCLAW_DESKTOP_CWD')  # no-op
    
    # 8. "hermes" as product name in text (should rarely happen since files already say OpenClaw)
    # Replace standalone "hermes" at word boundaries in text content
    # Pattern: "hermes" followed by space, punctuation, or at end
    # But NOT inside HTML tags
    
    # More specific command patterns
    content = content.replace('`hermes`', '`openclaw`')
    content = content.replace('"hermes"', '"openclaw"')
    
    # Remaining "hermes" as start of line (in code blocks)
    content = content.replace('\nhermes ', '\nopenclaw ')
    
    # "hermes" followed by newline in code
    content = content.replace('>hermes<', '>openclaw<')
    content = content.replace('"hermes"', '"openclaw"')
    
    # 9. hermes-banner-dismissed-until in JavaScript - change to openclaw-banner-dismissed-until
    content = content.replace('"hermes-banner-dismissed-until"', '"openclaw-banner-dismissed-until"')
    
    # 10. .hermes.md → OPENCLAW.md references
    content = content.replace('.hermes.md', '.openclaw.md')
    
    # 11. ~/.hermes/checkpoints → ~/.openclaw/checkpoints 
    # Already handled by #1
    
    # 12. hermes skills install → openclaw skills install
    content = content.replace('hermes skills install', 'openclaw skills install')
    
    # 13. hermes skills browse → openclaw skills browse
    content = content.replace('hermes skills browse', 'openclaw skills browse')
    
    # === PAGE-SPECIFIC FIXES ===
    
    # Fix broken patterns where "hermes" was partially replaced
    # E.g. "openclaw chat" + remaining part
    # Check for doubled replacements
    
    # Fix: ensure "openclaw chat -q" works (was "hermes chat -q")
    content = content.replace('openclaw chat -q', 'openclaw chat -q')  # no-op, already correct
    
    if content != original:
        count = content.count('openclaw') - original.count('openclaw')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {filepath} - replaced {count}+ occurrences")
    else:
        print(f"· {filepath} - no changes")

def main():
    for f in FILES:
        filepath = os.path.join(BASE, f)
        if os.path.exists(filepath):
            replace_in_file(filepath)
        else:
            print(f"✗ {filepath} - NOT FOUND")

if __name__ == '__main__':
    main()
