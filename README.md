# Noto Sans JP static-weights
- オリジナルの[Noto Sans JP](https://github.com/notofonts/noto-cjk)の各ウェイトを独立したファミリーとしてttf化したものです．
- PowerPointなどMS系アプリケーションでBoldサブファミリーがフォント一覧に表示されない問題を解決します．

# インストール方法
## Releasesからダウンロード
1. [こちら](https://github.com/KaiManabe/noto-sans-jp-static-weights/releases)から`noto_sans_jp_static_weights.zip`をダウンロードします
2. ダウンロードしたzipを展開します
3. 展開されたttfをインストールします

## Pythonで生成
1. venv等の仮想環境内で`requirements.txt`に記されているモジュールをインストールします
   1. e.g. `pip install -r requirements.txt`
2. weights.csvに任意のウェイトとフォント名の組み合わせを記述します
3. `python main.py weights.txt`を実行します
4. `out`ディレクトリにttfが出力されます


# License
The source code in this repository is licensed under the MIT License.

The generated font files are derived from Noto Sans JP / Noto CJK and are
licensed under the SIL Open Font License 1.1. See `out/LICENSE`.

This project is not affiliated with or endorsed by Google, Adobe, or SIL.

# 免責事項
本プロジェクトおよび生成されたフォントの使用により生じたいかなる損害、データの損失、業務上の損失、第三者との紛争その他一切の不利益について、作者は責任を負いません。利用者自身の責任で動作確認およびライセンス確認を行ってください。
