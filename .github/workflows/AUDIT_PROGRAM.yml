name: Hirosaki View Repository Audit

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  audit:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run repository audit
        shell: python
        run: |
          from pathlib import Path
          import re
          import unicodedata
          import sys

          ROOT = Path(".").resolve()
          errors = 0
          warnings = 0

          print("=" * 60)
          print("HIROSAKI VIEW — REPOSITORY AUDIT")
          print("=" * 60)

          # --------------------------------------------------
          # 1. 不可視Unicode / 正規化異常
          # --------------------------------------------------
          print("\n[1] PATH CHECK")

          suspicious_codes = {
              0x200B: "ZERO WIDTH SPACE",
              0x200C: "ZERO WIDTH NON-JOINER",
              0x200D: "ZERO WIDTH JOINER",
              0xFEFF: "ZERO WIDTH NO-BREAK SPACE / BOM",
          }

          for p in sorted(ROOT.rglob("*")):
              if ".git" in p.parts:
                  continue

              name = p.name
              found = []

              for ch in name:
                  if ord(ch) in suspicious_codes:
                      found.append(
                          f"U+{ord(ch):04X} {suspicious_codes[ord(ch)]}"
                      )

              normalized = unicodedata.normalize("NFC", name)

              if found:
                  warnings += 1
                  print(f"⚠ SUSPICIOUS PATH: {p.relative_to(ROOT)}")
                  for item in found:
                      print(f"    {item}")

              if normalized != name:
                  warnings += 1
                  print(
                      f"⚠ NORMALIZATION: {p.relative_to(ROOT)}"
                  )

          # --------------------------------------------------
          # 2. Markdownリンク検査
          # --------------------------------------------------
          print("\n[2] MARKDOWN LINK CHECK")

          link_pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')

          for md in sorted(ROOT.rglob("*.md")):
              if ".git" in md.parts:
                  continue

              try:
                  text = md.read_text(
                      encoding="utf-8",
                      errors="replace"
                  )
              except Exception as e:
                  print(f"⚠ READ ERROR: {md}: {e}")
                  errors += 1
                  continue

              for line_no, line in enumerate(
                  text.splitlines(), 1
              ):
                  for match in link_pattern.finditer(line):
                      target = match.group(1).strip()

                      # 外部URL / アンカー / mailto は除外
                      if target.startswith(
                          ("http://", "https://", "#", "mailto:")
                      ):
                          continue

                      # タイトル部分を除去
                      target_path = target.split()[0]

                      # URLエンコードされたものは一旦そのまま扱う
                      resolved = (
                          md.parent / target_path
                      ).resolve()

                      try:
                          resolved.relative_to(ROOT)
                      except ValueError:
                          warnings += 1
                          print(
                              f"⚠ OUTSIDE REPO: "
                              f"{md.relative_to(ROOT)}:"
                              f"{line_no} -> {target}"
                          )
                          continue

                      if not resolved.exists():
                          errors += 1
                          print(
                              f"✗ BROKEN LINK: "
                              f"{md.relative_to(ROOT)}:"
                              f"{line_no} -> {target}"
                          )

          # --------------------------------------------------
          # 3. 重要パス参照の検査
          # --------------------------------------------------
          print("\n[3] PATH REFERENCES")

          keywords = (
              "observations/",
              "experiments/",
              "実験/",
              "docs/",
              "runs/",
          )

          for md in sorted(ROOT.rglob("*.md")):
              if ".git" in md.parts:
                  continue

              text = md.read_text(
                  encoding="utf-8",
                  errors="replace"
              )

              for line_no, line in enumerate(
                  text.splitlines(), 1
              ):
                  if any(k in line for k in keywords):
                      print(
                          f"  {md.relative_to(ROOT)}:"
                          f"{line_no}: {line}"
                      )

          # --------------------------------------------------
          # 4. 観測ログの基本形式チェック
          # --------------------------------------------------
          print("\n[4] OBSERVATION FILE CHECK")

          observation_dirs = [
              p for p in ROOT.iterdir()
              if p.is_dir()
              and (
                  p.name == "observations"
                  or "observations" in p.name
              )
          ]

          for obs_dir in sorted(observation_dirs):
              print(
                  f"  Checking: "
                  f"{obs_dir.relative_to(ROOT)}"
              )

              for md in sorted(obs_dir.rglob("*.md")):
                  text = md.read_text(
                      encoding="utf-8",
                      errors="replace"
                  )

                  # 完全なスキーマ強制ではなく、
                  # 明らかな欠落だけ検出する。
                  required_candidates = [
                      "観測日時",
                      "場所",
                      "観測対象",
                  ]

                  missing = [
                      x for x in required_candidates
                      if x not in text
                  ]

                  if missing:
                      warnings += 1
                      print(
                          f"  ⚠ FORMAT: "
                          f"{md.relative_to(ROOT)}"
                      )
                      print(
                          f"      missing: "
                          f"{', '.join(missing)}"
                      )

          # --------------------------------------------------
          # 5. 結果
          # --------------------------------------------------
          print("\n" + "=" * 60)
          print("AUDIT RESULT")
          print("=" * 60)

          print(f"Errors   : {errors}")
          print(f"Warnings : {warnings}")

          if errors:
              print("\n❌ AUDIT FAILED")
              print(
                  "Broken references or other "
                  "blocking errors were detected."
              )
              sys.exit(1)

          if warnings:
              print("\n⚠ AUDIT PASSED WITH WARNINGS")
              print(
                  "Warnings require human/design review."
              )
          else:
              print("\n✓ AUDIT CLEAN")

          print("=" * 60)
これを置くと
GitHubへpush
      ↓
Actions自動起動
      ↓
この監査が実行
      ↓
結果がGitHubに保存
になる。
勝手にファイルを書き換えたり、renameしたり、commitしたりはしない。
そして今回の重要ポイントとして、
​実験/ が検出されたとしても、「警告」として出すだけ
にしてある。
つまり機械には「怪しい」を言わせるけど、「消せ」は言わせない。
置いた後
GitHubで、
Actions → Hirosaki View Repository Audit
を開けば実行結果が見える。
まずはこの1ファイルだけ置いて実行。
実行できたら、結果を俺に教えて。
今度はターミナル経由じゃなく、GitHub自身が吐いた一次資料を俺が読むところまで持っていける。
