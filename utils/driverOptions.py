from selenium.webdriver.chrome.options import Options

options = Options()
# ヘッダレスモードを有効化する（コメントアウトするとブラウザが表示される）
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
options.add_argument("--disable-application-cache")
options.add_argument("--hide-scrollbars")