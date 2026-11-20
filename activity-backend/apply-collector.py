"""Keep known lab builds instrumented without changing their application code."""
from pathlib import Path
import re
import sys

VERSION = "20261120-kron1"
PAGES = "index snake tetris flight raycast xonix faces life edges sandbox microbit fruit garden motion roll microbit-pycharm scale kron".split()
RESOURCES = {
    "fruit": {"fruit-download-csv": "download_data", "fruit-copy-code": "copy_code"},
    "garden": {"g-csv": "download_data", "g-copy": "copy_code"},
}

def instrument(folder):
    folder = Path(folder)
    for name in PAGES:
        path = folder / (name + ".html")
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for control, event in RESOURCES.get(name, {}).items():
            pattern = r'<button\b[^>]*\bid="' + re.escape(control) + r'"[^>]*>'
            def annotate(match):
                tag = re.sub(r'\sdata-activity-event="[^"]*"', '', match.group())
                return tag[:-1] + ' data-activity-event="' + event + '">'
            text, count = re.subn(pattern, annotate, text)
            if count != 1:
                raise ValueError(f"Expected one {control} on {path}; found {count}")
        src = r'game-activity\.js(?:\?[^"\']*)?'
        if re.search(r'src=["\']' + src + r'["\']', text):
            text = re.sub(r'(src=["\'])' + src + r'(["\'])',
                          r'\g<1>game-activity.js?v=' + VERSION + r'\2', text)
        else:
            script = '<script defer src="game-activity.js?v=' + VERSION + '"></script>'
            if '</body>' not in text:
                raise ValueError(f"Missing closing body on {path}")
            text = text.replace('</body>', script + '</body>', 1)
        if 'href="privacy.html"' not in text:
            text = text.replace('</footer>', '<a href="privacy.html">Privacy &amp; activity counters</a></footer>', 1)
        if len(re.findall(r'src=["\']game-activity\.js', text)) != 1:
            raise ValueError(f"Duplicate or missing collector on {path}")
        if 'href="privacy.html"' not in text:
            raise ValueError(f"Missing privacy link on {path}")
        path.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    targets = sys.argv[1:] or [Path(__file__).resolve().parents[1] / "dist", Path(__file__).resolve().parents[1] / "deploy"]
    for target in targets:
        instrument(target)
    print("Collector markup and resource buttons checked.")
