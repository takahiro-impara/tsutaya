import os
import sys
import re
import time
#from pubsub import pub
#import traceback
import json
import datetime
import logging
import glob

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

#from model.SearchResult import SearchResult
from SearchResult import SearchResult
#from utils.messages import MSG_EACH_SEARCH_DONE
from StoreManager import store_data_json
import AreaManager as AM
from utils.driverOptions import options
from excel.ExcelManager import Excel
from csvs.CsvOutput import CSV

store_list_url = "https://store-tsutaya.tsite.jp/storelocator/result_sv.html"
store_locater_url = "https://store-tsutaya.tsite.jp/storelocator.html"
fmt_stock_url = "https://store-tsutaya.tsite.jp/item/{type}/{jancode}.html"
types = ['sell_dvd', 'sell_cd', 'sell_book', 'sell_game']
#types = ['sell_game']


if not os.path.exists('../log/'):
    os.mkdir('../log/')
else:
    rm_fiels = []
    rm_files = glob.glob('../log/*')

if len(rm_files) != 0:
    for rm_file in rm_files:
        os.remove(rm_file)

logdate_fmt = datetime.datetime.now().strftime('%Y%m%d%H')
logging.basicConfig(filename='../log/{0}-tsutaya.log'.format(logdate_fmt), level=logging.INFO)

class TsutayaSell:
    def __init__(self, browser):
        """
        コンストラクタ
        :param browser: アクセスに使用するブラウザ。
        """
        sys.path.append(os.getcwd())
        self.browser = browser

    def open_item_page(self, type, jancode):
        """
        商品情報にアクセスし、type情報を特定する
        :param type:
        :param jancode:
        :return: 商品情報がヒットした場合はTrue,それ以外はFalse
        """
        print('call open_item_page')
        url = fmt_stock_url.format(jancode=jancode, type=type)
        print(url)
        self.browser.get(url)
        if self.is_error_page():
            print('encount error!')
            return False

        return True

    def is_error_page(self):
        """
        エラーページに遷移したかの判定を行う
        :return: エラーページに遷移した場合はTrue,それ以外はFalse
        """
        if self.browser.find_elements(By.ID, 'errorBlock'):
            print('encount error! is correct jan code??')
            return True
        else:
            return False

    def open_store_locater_page(self, pref):
        """
        各都道府県の店舗検索結果のページを表示する
        :param pref: 県情報
        :return: エラーページに遷移した場合はFalse、それ以外はTrueを返す
        """
        print('call open_store_locater_page')
        self.browser.get(store_locater_url)
        if self.is_error_page():
            print('encount error!')
            return False

        self.browser.find_element(By.XPATH, "//option[text()='{0}']".format(pref)).click()
        self.browser.execute_script("SearchSelectAdr()")
        return True

    def open_stock_page(self, url):
        """
        商品のストックページを開く
        :param jancode: 対象のJANコード
        :param store_id:　対象のstoreId

        :return: エラーページに遷移した場合Flaseを返す、それ以外はTrueを返す
        """
        print('call open_stock_page')
        print(url)
        self.browser.get(url)
        if self.is_error_page():
            print('encount error!')
            return False

    def read_stock_page(self, store_id, store_info):
        """
        open_stock_pageで開いたページの在庫状況を取得する
        :param
            store_id: 対象のstoreId
            store_info: 対象StoreIdの情報
        :return: 在庫情報を追加したstore_data
        """
        #state = self.browser.wait().until(EC.presence_of_element_located((By.CLASS_NAME, 'state')))
        stock_state = self.browser.find_element(By.CLASS_NAME, 'state').text
        if '－' in stock_state:
            store_info['hasStock'] = 'False'
            store_info['tel'] = '-'
            return store_info
        elif '○' in stock_state:
            #print("store:{store_id} {stock_state}".format(store_id=store_id, stock_state='在庫あり'))
            IsNextPhone = False
            for detail_line in (self.browser.find_element(By.CLASS_NAME, 'myStoreDetail').text.split('\n')):
                if IsNextPhone:
                    store_info['hasStock'] = 'True'
                    store_info['tel'] = detail_line.rstrip()
                    return store_info
                if (detail_line) == '電話番号：':
                    IsNextPhone = True
        else:
            store_info['hasStock'] = 'False'
            store_info['tel'] = '-'
            return store_info
    def read_store_page(self):
        """
        表示されたページ上の店舗情報を全て取得して、JSONファイルに出力する
        :return:　JSONファイル出力を行い、返り値にJSONデータを返す
        """

        iframe = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        self.browser.switch_to_frame(iframe)
        store_data = {}

        #while len(self.browser.find_elements(By.CLASS_NAME, 'next')):
        total_store = int(self.browser.find_element(By.CLASS_NAME, 'txt_k').text.rstrip().split('/')[-1].replace('全', '').replace('件', ''))
        for i in range((total_store // 20) + 1):
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wh')))
            tables = self.browser.find_elements(By.TAG_NAME, 'table')
            for table in tables:
                if table.get_attribute('summary') != '店舗情報':
                    continue
                data = {}
                store_link = table.find_element(By.TAG_NAME, 'a')
                store_name = store_link.text
                href = store_link.get_attribute('href')
                store_id = os.path.basename(href).split('.')[0]
                store_info = table.find_element(By.CLASS_NAME, 'wh').text.split('\n')
                address = store_info[1]
                if len(store_info) == 3:
                    business_hour = re.sub("\s", "", store_info[2]).replace("営業時間：", "")
                else:
                    # 営業時間ないやつがいる
                    business_hour = '記載なし'

                data['id'] = store_id
                data['name'] = store_name
                data['address'] = address
                data['business_hour'] = business_hour
                store_data[store_id] = data
                print(data)
            try:
                self.browser.find_element(By.CLASS_NAME, 'next').find_element(By.XPATH, "..").click()
            except:
                break
            # リンクを押したあとにページが更新されるのを待たないと、リンク押す前のページで判断してしまう
            time.sleep(0.6)
        print('Read all store info succeed.')
        print('Write to store data file...')
        #print(store_data)
        fw = open(store_data_json, 'w')
        json.dump(store_data, fw, indent=4)
        return store_data
if __name__ == '__main__':
    input_datas = []
    excel_file = '../input/Book.xlsx'
    excel_sheet = 'Sheet1'

    ex = Excel(excel_file)
    input_datas = ex.get_excel_data(excel_sheet)
    print(input_datas)
    #options = Options()

    for input_data in input_datas:
        store_datas = []
        sell_stock_urls = []
        target_area = []

        browser = webdriver.Chrome(chrome_options=options, executable_path='../resources/chromedriver.exe')
        ts = TsutayaSell(browser)
        jan_code = input_data['jan_code']
        group = input_data['area']
        _type = input_data['type']
        print(jan_code, group)

        if group == 'all':
            for area, pref in AM.__allArea.items():
                target_area += pref
        elif group in AM.__allArea.keys():
            target_area = AM.__allArea[group]
        else:
            target_area = [group]



        for type in types:
            if ts.open_item_page(type, jan_code):
                sell_stock_urls.append(fmt_stock_url.format(jancode=jan_code, type=type))

        for pref in target_area:
            ts.open_store_locater_page(pref)
            store_datas.append(ts.read_store_page())
        logging.info('検索対象の都道府県 {0}'.format(store_datas))
        try:
            for sell_stock_url in sell_stock_urls:
                write_lines = []
                for store_data in store_datas:
                    for store_id, store_info in store_data.items():
                        url = '{0}?storeId={1}'.format(sell_stock_url, store_id)
                        ts.open_stock_page(url)
                        write_lines.append(ts.read_stock_page(store_id, store_info))
                        print(write_lines[-1])
                        #logging.info(write_lines[-1])
                csv_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
                csv_file = '{0}_{1}_{2}_{3}.csv'.format(csv_date, jan_code, group, sell_stock_url.split('/')[-2])
                print(csv_file)
                CSV(csv_file).write_csv(write_lines)
                logging.info('success write csv: {0}'.format(csv_file))
        finally:
            print("取得予定の都道府県: {0}".format(store_datas))
            print("未取得の都道府県: {0}".format(store_datas[store_datas.index(store_data)+1:]))
            logging.info("取得予定の都道府県: {0}".format(store_datas))
            logging.info("未取得の都道府県: {0}".format(store_datas[store_datas.index(store_data)+1:]))

            browser.close()

