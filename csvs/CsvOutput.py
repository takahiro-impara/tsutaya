# -*- coding: utf-8 -*-
import csv
import os
import sys

if __name__ != '__main__':
    from csvs.OutputManager import csv_header
    from csvs.OutputManager import OutputManager
else:
    from OutputManager import csv_header
    from OutputManager import OutputManager

class CSV:
    def __init__(self, file_name):
        """
        コンストラクタ
        :param file_name: CSVファイル名
        """
        self.file_name = '../outputs/' + file_name

    def write_csv(self, data) -> list:
        """
        引数データのCSV書き込み処理を行う
        :param data: CSV書き込みデータ
        :return: 正常終了した場合True、それ以外は False
        """
        self.data = OutputManager(data).store_data_modified
        with open(self.file_name, 'w') as csv_file:
            # header を設定
            writer = csv.DictWriter(csv_file, fieldnames=csv_header)
            writer.writeheader()

            # データの書き込み
            for csv_line in self.data:
                if (csv_line['hasStock']) == 'True':
                    writer.writerow(csv_line)

if __name__ == '__main__':
    test_data = [{'business_hour': '朝09:00～深夜01:00', 'id': '1216', 'address': '群馬県高崎市江木町２８番地', 'name': 'TSUTAYA 江木店', 'tel': '027-328-7771', 'hasStock': 'True'}]

    cs = CSV('test-tmp.csv')
    cs.write_csv(test_data)