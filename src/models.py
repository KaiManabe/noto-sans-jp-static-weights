"""CSV から読み込んだウェイト定義を表すモデルを置くモジュール"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeightMapping:
    """1 つの静的フォントとして書き出すウェイトとファミリー名"""

    weight: int
    family_name: str
