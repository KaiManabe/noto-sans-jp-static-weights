"""コマンドライン実行用の薄い入口"""

from __future__ import annotations

from src.cli import main


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"error: {error}") from None
