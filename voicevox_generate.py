# -*- coding: utf-8 -*-
import requests
import pandas as pd
import os

# 使用する話者ID（例：四国めたん = 3、ずんだもん = 1）
speaker_id = 3

# 作業フォルダのパス（必要に応じて変更）
base_dir = os.path.expanduser("~/Desktop/HachijoDWeb")
csv_file = os.path.join(base_dir, "hachijo_100.csv")
output_dir = os.path.join(base_dir, "audio")
os.makedirs(output_dir, exist_ok=True)

# CSVファイルを読み込み（UTF-8 BOM対応）
df = pd.read_csv(csv_file, encoding="utf-8-sig")

# 各行に対して音声を生成
for index, row in df.iterrows():
    try:
        # 🔊 読み上げるテキスト（読みがな列に修正済）
        text = (
            f"「{row['読みがな']}」は、「{row['共通語']}」の意味です。"
            f"大賀郷では「{row['方言（大賀郷）']}」、三根では「{row['方言（三根）']}」、"
            f"中之郷では「{row['方言（中之郷）']}」、樫立では「{row['方言（樫立）']}」と言います。"
        )

        # ファイル名（001.mp3など）
        id_str = row['ID'].replace("H", "").zfill(3)
        filename = os.path.join(output_dir, f"{id_str}.mp3")

        # VOICEVOXへのリクエスト
        query = requests.post(
            "http://127.0.0.1:50021/audio_query",
            params={"text": text, "speaker": speaker_id}
        )
        query.raise_for_status()

        synthesis = requests.post(
            "http://127.0.0.1:50021/synthesis",
            params={"speaker": speaker_id},
            data=query.content
        )
        synthesis.raise_for_status()

        # 音声ファイル保存
        with open(filename, "wb") as f:
            f.write(synthesis.content)

        print(f"✅ {filename} 作成完了")

    except Exception as e:
        print(f"❌ エラー（{row['ID']}）: {e}")