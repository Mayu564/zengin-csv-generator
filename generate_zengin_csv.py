import csv
import zengin_code as zengin
import datetime
import os

def generate_zengin_data():
    """
    zengin-codeライブラリを使用して銀行・支店データを取得し、
    指定された形式で整形して返す。
    """
    data = []
    # zengin.Bank.all は、{銀行コード: Bankオブジェクト} のOrderedDict
    banks_data = zengin.Bank.all

    # banks_data の値が zengin.Bank オブジェクトなので、values() でループ
    for bank in banks_data.values(): # ここを修正！

        # bank.code は zengin.Bank オブジェクトの属性として存在します
        if not bank.code:
            continue

        # bank.branches も {支店コード: Branchオブジェクト} のOrderedDict
        branches_data = bank.branches

        if branches_data:
            # branches_data の値が zengin.Branch オブジェクトなので、values() でループ
            for branch in branches_data.values(): # ここを修正！
                # branch.code も zengin.Branch オブジェクトの属性として存在します
                if not branch.code:
                    continue

                data.append({
                    "銀行番号": bank.code,
                    "銀行名カナ": bank.kana,
                    "支店番号": branch.code,
                    "支店名カナ": branch.kana,
                })
        else:
            pass # 支店がない場合はスキップ

    return data

def main():
    output_filename = "zengin_codes.csv"
    data_to_write = generate_zengin_data()

    if not data_to_write:
        print("No data to write for Zengin codes. It might be an issue with data retrieval or processing.")
        return

    # ヘッダーを生成 (順序を保証するためにリストで指定)
    fieldnames = ["銀行番号", "銀行名カナ", "支店番号", "支店名カナ"]

    # CSVファイルの出力
    try:
        with open(output_filename, 'w', newline='', encoding='shift_jis') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_write)
        print(f"CSV file '{output_filename}' generated successfully with {len(data_to_write)} records.")
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        exit(1)

if __name__ == "__main__":
    main()
