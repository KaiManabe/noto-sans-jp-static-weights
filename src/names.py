"""TTF の name table と出力ファイル名を整える処理をまとめたモジュール"""

from __future__ import annotations

import hashlib
import re

from fontTools.ttLib import TTFont

from .config import NAME_IDS_TO_CLEAR, NAME_PLATFORMS
from .models import WeightMapping


def clean_name_table(font: TTFont) -> None:
    """既存のファミリー名・スタイル名に関わる name record を削除する"""

    name_table = font["name"]
    name_table.names = [
        record for record in name_table.names if record.nameID not in NAME_IDS_TO_CLEAR
    ]


def set_name(font: TTFont, name_id: int, value: str) -> None:
    """指定した name ID に同じ文字列を主要 platform 向けに書き込む"""

    for platform_id, encoding_id, language_id in NAME_PLATFORMS:
        if platform_id == 1:
            try:
                value.encode("mac_roman")
            except UnicodeEncodeError:
                continue
        font["name"].setName(value, name_id, platform_id, encoding_id, language_id)


def collapse_spaces(value: str) -> str:
    """連続する空白を 1 つの半角スペースにまとめる"""

    return re.sub(r"\s+", " ", value).strip()


def postscript_part(value: str) -> str:
    """PostScript 名に使える ASCII 英数字だけの部品を作る"""

    cleaned = re.sub(r"[^A-Za-z0-9]", "", value)
    if cleaned:
        return cleaned

    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"Font{digest}"


def postscript_name(family_name: str, subfamily_name: str) -> str:
    """ファミリー名とサブファミリー名から nameID 6 の PostScript 名を作る"""

    if subfamily_name.lower() == "regular":
        name = postscript_part(family_name)
    else:
        name = f"{postscript_part(family_name)}-{postscript_part(subfamily_name)}"
    if len(name) <= 63:
        return name

    digest = hashlib.sha1(name.encode("ascii")).hexdigest()[:8]
    return f"{name[:54]}-{digest}"


def filename_part(value: str) -> str:
    """ファミリー名から Windows で扱いやすいファイル名の stem を作る"""

    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "", value)
    cleaned = collapse_spaces(cleaned).replace(" ", "_").rstrip("._")
    return cleaned or "Font"


def full_name(family_name: str, subfamily_name: str) -> str:
    """nameID 4 に入れるフルネームを作る"""

    if subfamily_name.lower() == "regular":
        return family_name
    return f"{family_name} {subfamily_name}"


def set_static_names(font: TTFont, mapping: WeightMapping) -> tuple[str, str, str]:
    """CSV の name を独立ファミリー名として name table に反映する"""

    family_name = collapse_spaces(mapping.family_name)
    subfamily_name = "Regular"
    font_full_name = collapse_spaces(full_name(family_name, subfamily_name))
    ps_name = postscript_name(family_name, subfamily_name)
    unique_name = f"{ps_name};{mapping.weight}"
    output_stem = filename_part(family_name)

    clean_name_table(font)
    set_name(font, 1, family_name)
    set_name(font, 2, subfamily_name)
    set_name(font, 3, unique_name)
    set_name(font, 4, font_full_name)
    set_name(font, 6, ps_name)

    return family_name, subfamily_name, output_stem
