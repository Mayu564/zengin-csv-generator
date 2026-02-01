import csv
import zengin_code as zengin
import datetime
import os
import unicodedata # ★ 追加: unicodedataモジュールをインポート

# ★ 追加: 全角カタカナを半角カタカナに変換する関数
def hankaku_kana(text):
    """
    全角カタカナ文字列を半角カタカナに変換する。
    長音符、濁点、半濁点も適切に処理する。
    """
    # NFKC正規化で、全角カタカナを一度半角カタカナに変換しやすくする
    # その後、追加で濁点・半濁点の結合文字を処理
    return unicodedata.normalize('NFKC', text) \
        .replace('ｶﾞ', 'ｶﾞ').replace('ｷﾞ', 'ｷﾞ').replace('ｸﾞ', 'ｸﾞ').replace('ｹﾞ', 'ｹﾞ').replace('ｺﾞ', 'ｺﾞ') \
        .replace('ｻﾞ', 'ｻﾞ').replace('ｼﾞ', 'ｼﾞ').replace('ｽﾞ', 'ｽﾞ').replace('ｾﾞ', 'ｾﾞ').replace('ｿﾞ', 'ｿﾞ') \
        .replace('ﾀﾞ', 'ﾀﾞ').replace('ﾁﾞ', 'ﾁﾞ').replace('ﾂﾞ', 'ﾂﾞ').replace('ﾃﾞ', 'ﾃﾞ').replace('ﾄﾞ', 'ﾄﾞ') \
        .replace('ﾊﾞ', 'ﾊﾞ').replace('ﾋﾞ', 'ﾋﾞ').replace('ﾌﾞ', 'ﾌﾞ').replace('ﾍﾞ', 'ﾍﾞ').replace('ﾎﾞ', 'ﾎﾞ') \
        .replace('ﾊﾟ', 'ﾊﾟ').replace('ﾋﾟ', 'ﾋﾟ').replace('ﾌﾟ', 'ﾌﾟ').replace('ﾍﾟ', 'ﾍﾟ').replace('ﾎﾟ', 'ﾎﾟ') \
        .replace('ｳﾞ', 'ｳﾞ') # 小さい文字や特殊な文字も考慮

def generate_zengin_data():
    """
    zengin-codeライブラリを使用して銀行・支店データを取得し、
    指定された形式で整形して返す。
    """
    data = []
    banks_data = zengin.Bank.all

    for bank in banks_data.values():
        if not bank.code:
            continue

        branches_data = bank.branches

        # ★ 銀行名カナを半角に変換
        bank_kana_hankaku = hankaku_kana(bank.kana)

        if branches_data:
            for branch in branches_data.values():
                if not branch.code:
                    continue

                # ★ 支店名カナを半角に変換
                branch_kana_hankaku = hankaku_kana(branch.kana)

                data.append({
                    "銀行番号": bank.code,
                    "銀行名カナ": bank_kana_hankaku, # ★ ここを修正
                    "支店番号": branch.code,
                    "支店名カナ": branch_kana_hankaku, # ★ ここを修正
                })
        else:
            # 支店情報がない銀行の場合でも、銀行名だけは出力したいケース
            # 今回は、支店データがある場合のみ出力という方針を維持します。
            pass

    return data

def main():
    output_filename = "zengin_codes.csv"
    data_to_write = generate_zengin_data()

    if not data_to_write:
        print("No data to write for Zengin codes. It might be an issue with data retrieval or processing.")
        return

    fieldnames = ["銀行番号", "銀行名カナ", "支店番号", "支店名カナ"]

    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_write)
        print(f"CSV file '{output_filename}' generated successfully with {len(data_to_write)} records.")
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        exit(1)

if __name__ == "__main__":
    main()
