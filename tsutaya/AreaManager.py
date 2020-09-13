__allArea = {'北海道': ['北海道'],
             '東北': ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'],
             '関東': ['茨城県', '栃木県', '群馬県', '埼玉県', '東京都', '神奈川県', '千葉県'],
             '中部・信越': ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
             '近畿': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
             '中国・四国': ['鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県'],
             '九州・沖縄': ['福岡県', '長崎県', '佐賀県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']}


def AreaGroups() -> [str]:
    return __allArea.keys()


def AllArea() -> {str: [str]}:
    return __allArea


def __isInArea(area_name, address):
    for a in __allArea[area_name]:
        if a in address:
            return True
    return False

def GetAreasFromGroup(group: str):
    return __allArea[group]

def IsGroup(group: str):
    return True if group in __allArea.keys() else False

def IsInHokkaido(address: str):
    return __isInArea('北海道', address)


def IsInTohoku(address: str):
    return __isInArea('東北', address)


def IsInKanto(address: str):
    return __isInArea('関東', address)


def IsInTyubu(address: str):
    return __isInArea('中部', address)


def IsInKinki(address: str):
    return __isInArea('近畿', address)


def IsInTyugoku(address: str):
    return __isInArea('中国・四国', address)


def IsInShikoku(address: str):
    return __isInArea('中国・四国', address)


def IsInKyusyu(address: str):
    return __isInArea('九州・沖縄', address)


def IsInOkinawa(address: str):
    return __ + IsInOkinawa('九州・沖縄', address)

#print(GetAreasFromGroup('中部・信越'))
