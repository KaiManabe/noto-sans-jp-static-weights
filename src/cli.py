"""コマンドライン引数を解釈し、フォント生成処理を呼び出すモジュール"""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont

from .config import DEFAULT_INPUT_FONT
from .csv_mapping import read_weight_mappings
from .font_builder import copy_license, generate_static_font, validate_input_font


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析して argparse.Namespace として返す"""

    parser = argparse.ArgumentParser(
        description=(
            "Generate static TTFs from the Noto Sans JP variable font in "
            "the noto-cjk submodule."
        )
    )
    parser.add_argument(
        "weights_csv",
        type=Path,
        help="CSV file with weight,name columns, e.g. weights.csv.",
    )
    parser.add_argument(
        "--input-font",
        type=Path,
        default=DEFAULT_INPUT_FONT,
        help=f"Variable TTF to instantiate. Default: {DEFAULT_INPUT_FONT}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("out"),
        help="Directory for generated TTF files. Default: out",
    )
    return parser.parse_args()


def main() -> None:
    """CSV の定義に従って静的 TTF 群と LICENSE を出力する"""

    args = parse_args()
    mappings = read_weight_mappings(args.weights_csv)

    input_font = TTFont(args.input_font)
    validate_input_font(input_font, mappings)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for mapping in mappings:
        generate_static_font(
            variable_font_path=args.input_font,
            output_dir=args.output_dir,
            mapping=mapping,
        )
    copy_license(args.output_dir)
