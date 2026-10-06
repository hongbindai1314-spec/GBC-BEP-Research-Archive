from pathlib import Path
import hashlib

root = Path(__file__).resolve().parent
out = root/"SHA256SUMS.txt"
rows = []
for p in sorted(root.rglob("*")):
    if p.is_file() and p != out and ".git" not in p.parts:
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        rows.append(f"{h}  {p.relative_to(root)}")
out.write_text("\n".join(rows)+"\n", encoding="utf-8")
print(out)
