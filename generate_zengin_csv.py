import csv
import zengin_code as zengin
import datetime
import os

def generate_zengin_data():
    """
    zengin-pyライブラリを使用して銀行・支店データを取得し、
    指定された形式で整形して返す。
    """
    data = []
    # zengin.banks()で全ての銀行情報を取得
    # zengin.Bankはイテレータなので、リストに変換して処理する
    banks = list(zengin.banks())

    for bank in banks:
        # 銀行に支店が存在するか確認
        if bank.branches:
            for branch in bank.branches:
                data.append({
                    "銀行番号": bank.code,
                    "銀行名カナ": bank.kana,
                    "支店番号": branch.code,
                    "支店名カナ": branch.kana,
                })
        else:
            # 支店情報がない銀行も出力したい場合は、ここに追加
            pass

    return data

def main():
    output_filename = "zengin_codes.csv"
    data_to_write = generate_zengin_data()

    if not data_to_write:
        print("No data to write for Zengin codes.")
        return

    # ヘッダーを生成 (順序を保証するためにリストで指定)
    fieldnames = ["銀行番号", "銀行名カナ", "支店番号", "支店名カナ"]

    # CSVファイルの出力
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
