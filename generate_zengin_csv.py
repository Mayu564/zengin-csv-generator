import csv
import zengin_code as zengin # ここは既に修正済みのはずです
import datetime
import os

def generate_zengin_data():
    """
    zengin-codeライブラリを使用して銀行・支店データを取得し、
    指定された形式で整形して返す。
    """
    data = []
    # zengin.Bank.all()で全ての銀行情報を取得
    banks_data = zengin.Bank.all

    for bank_data in banks_data: # ここも修正
        # 銀行コードがないものはスキップ (稀にデータに不備がある場合を想定)
        if not bank_data.code:
            continue

        # 支店情報を取得
        # zengin_codeではbank_data.branches.all()で全ての支店データを取得します
        branches_data = bank_data.branches.all()

        if branches_data:
            for branch_data in branches_data: # ここも修正
                # 支店コードがないものもスキップ (稀にデータに不備がある場合を想定)
                if not branch_data.code:
                    continue

                data.append({
                    "銀行番号": bank_data.code,
                    "銀行名カナ": bank_data.kana,
                    "支店番号": branch_data.code,
                    "支店名カナ": branch_data.kana,
                })
        else:
            # 支店情報がない銀行も出力したい場合は、以下のような処理を追加
            # ただし、全銀協のデータでは通常、支店がない銀行は掲載されないか、
            # もしくは本支店コードが同じ場合が多いです。
            # 例えば、本店情報のみを記載する場合など。
            # 今回は支店情報があるもののみを対象とします。
            pass

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
