"""フォント生成で共有する既定値と制約値を定義するモジュール"""

from __future__ import annotations

from pathlib import Path


DEFAULT_INPUT_FONT = (
    Path("submodule")
    / "noto-cjk"
    / "Sans"
    / "Variable"
    / "TTF"
    / "Subset"
    / "NotoSansJP-VF.ttf"
)
"""既定で使う Noto Sans JP の subset 可変 TTF"""

DEFAULT_LICENSE_FILE = Path("submodule") / "noto-cjk" / "Sans" / "LICENSE"
"""生成物に同梱する Noto CJK Sans のライセンスファイル"""

MAX_POWERPOINT_EMBEDDABLE_GLYPHS = 65534
"""PowerPoint の埋め込みフォント展開で壊れないようにする最大グリフ数"""

NAME_IDS_TO_CLEAR = {
    1,  # Font Family
    2,  # Font Subfamily
    3,  # Unique font identifier
    4,  # Full font name
    6,  # PostScript name
    16,  # Typographic family
    17,  # Typographic subfamily
    18,  # Compatible full name
    21,  # WWS family
    22,  # WWS subfamily
}
"""生成時に作り直す name table の ID"""

STATIC_TABLES_TO_DROP = {
    "STAT",
    "avar",
    "cvar",
    "fvar",
    "gvar",
    "HVAR",
    "MVAR",
    "VVAR",
}
"""静的 TTF には不要な可変フォント由来テーブル"""

NAME_PLATFORMS = (
    (1, 0, 0),  # Macintosh, Roman, English
    (3, 1, 0x409),  # Windows, Unicode BMP, en-US
    (3, 10, 0x409),  # Windows, Unicode full repertoire, en-US
)
"""name record を書き込む platform / encoding / language の組"""
