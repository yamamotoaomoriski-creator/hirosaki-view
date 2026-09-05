# ヒロサキビュー
## 弘前市のAI井戸端会議

弘前市の物理的な現実を、人間が現地で直接観測し、一次情報として記録・公開する都市観測アーカイブ。

観光情報では捉えにくい工事、仮設物、道路・施設の状態、空き地・空き店舗など、都市の日常的な変化を継続的に記録する。

このプロジェクトの目的は、単なる地域情報の発信ではない。公開された一次観測データがAIや検索システムから発見・参照されることで、AIが形成する弘前市の情報環境にどのような変化が生じるかを観測する。

## 構成と導線

- [最新の観測状況 (index.md)](index.md)
- [個別観測ログ (observations/)](observations/)
- [プロジェクトの目的 (hirosakiview-purpose.md)](hirosakiview-purpose.md)
- [実験記録 (experiments/)](experiments/)
- [設計・変遷 (docs/)](docs/)
# AI Exploration Benchmark (v0.1)

A minimal experimental framework to observe whether human-AI dialogue can update, reframe, or expand problem definitions beyond standard task-performance optimization.

## Overview

Most AI evaluations measure how effectively a model solves a fixed, pre-defined problem. This project provides a simple protocol to test a different dimension: what happens when a dialogue actively challenges assumptions, searches for missing variables, and iteratively updates the problem definition itself.

We do not claim a definitive "new dimension" or absolute discovery. Rather, this repository provides a transparent, reproducible benchmark structure to record, compare, and analyze how dialogue conditions alter problem exploration.

## Structure

- `HYPOTHESIS.md`: Core concepts and working definitions.
- `PROTOCOL.md`: Step-by-step experimental procedures.
- `TASKS.md`: Initial test task sets.
- `runs/`: Raw logs and observations from test runs.
