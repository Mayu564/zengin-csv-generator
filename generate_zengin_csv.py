import csv
import zengin_code as zengin
import datetime
import os
import mojimoji # ★ 変更: unicodedata ではなく mojimoji をインポート

# ★ 変更: mojimoji を使って半角カタカナに変換する関数
def hankaku_kana(text):
    """
    mojimojiライブラリを使用して全角カタカナ文字列を半角カタカナに変換する。
    """
    if not isinstance(text, str): # textが文字列であることを確認
        return text
    return mojimoji.zen_to_han(text, kana=True) # 全角カタカナを半角に変換

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

        # ★ 銀行名カナを半角に変換 (mojimojiを使用)
        bank_kana_hankaku = hankaku_kana(bank.kana)

        if branches_data:
            for branch in branches_data.values():
                if not branch.code:
                    continue

                # ★ 支店名カナを半角に変換 (mojimojiを使用)
                branch_kana_hankaku = hankaku_kana(branch.kana)

                data.append({
                    "銀行番号": bank.code,
                    "銀行名カナ": bank_kana_hankaku,
                    "支店番号": branch.code,
                    "支店名カナ": branch_kana_hankaku,
                })
        else:
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
