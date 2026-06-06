"""可変 TTF から静的 TTF を生成し、出力物を整えるモジュール"""

from __future__ import annotations

import shutil
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

from .config import (
    DEFAULT_INPUT_FONT,
    DEFAULT_LICENSE_FILE,
    MAX_POWERPOINT_EMBEDDABLE_GLYPHS,
    STATIC_TABLES_TO_DROP,
)
from .models import WeightMapping
from .names import set_static_names


def drop_variable_tables(font: TTFont) -> None:
    """静的フォントには不要な可変フォント由来のテーブルを削除する"""

    for table_tag in STATIC_TABLES_TO_DROP:
        if table_tag in font:
            del font[table_tag]


def set_weight_metadata(font: TTFont, mapping: WeightMapping) -> None:
    """OS/2 と head に静的フォントとしてのウェイト情報を設定する"""

    if "OS/2" in font:
        os2 = font["OS/2"]
        os2.usWeightClass = mapping.weight

        bold_bit = 1 << 5
        regular_bit = 1 << 6
        os2.fsSelection &= ~(bold_bit | regular_bit)
        os2.fsSelection |= regular_bit

    if "head" in font:
        bold_bit = 1 << 0
        font["head"].macStyle &= ~bold_bit


def generate_static_font(
    variable_font_path: Path,
    output_dir: Path,
    mapping: WeightMapping,
) -> Path:
    """指定されたウェイトを可変 TTF から静的 TTF として書き出す"""

    variable_font = TTFont(variable_font_path)
    static_font = instantiateVariableFont(
        variable_font,
        {"wght": mapping.weight},
        inplace=False,
        optimize=True,
    )
    drop_variable_tables(static_font)
    set_weight_metadata(static_font, mapping)
    family_name, subfamily_name, output_stem = set_static_names(static_font, mapping)
    static_font["name"].removeUnusedNames(static_font)

    output_path = output_dir / f"{output_stem}.ttf"
    static_font.save(output_path)
    print(f"Wrote {output_path} ({family_name} / {subfamily_name})")
    return output_path


def copy_license(output_dir: Path) -> None:
    """Noto CJK Sans のライセンスファイルを出力ディレクトリへコピーする"""

    if not DEFAULT_LICENSE_FILE.exists():
        raise ValueError(f"license file not found: {DEFAULT_LICENSE_FILE}")

    output_path = output_dir / DEFAULT_LICENSE_FILE.name
    shutil.copy2(DEFAULT_LICENSE_FILE, output_path)
    print(f"Wrote {output_path}")


def validate_input_font(font: TTFont, mappings: list[WeightMapping]) -> None:
    """入力フォントが静的化と PowerPoint 埋め込みに使えるか検査する"""

    if "fvar" not in font:
        raise ValueError("input font is not a variable font; missing fvar table")

    if font["maxp"].numGlyphs > MAX_POWERPOINT_EMBEDDABLE_GLYPHS:
        raise ValueError(
            "input font has 65535 glyphs, which produces embedded fonts that "
            "PowerPoint's Windows font embedding API cannot decompress. Use "
            f"the subset JP variable font instead: {DEFAULT_INPUT_FONT}"
        )

    weight_axis = next(
        (axis for axis in font["fvar"].axes if axis.axisTag == "wght"),
        None,
    )
    if weight_axis is None:
        raise ValueError("input font does not have a wght axis")

    for mapping in mappings:
        if not weight_axis.minValue <= mapping.weight <= weight_axis.maxValue:
            raise ValueError(
                f"weight {mapping.weight} is outside the input font's wght axis "
                f"range {weight_axis.minValue:g}..{weight_axis.maxValue:g}"
            )
