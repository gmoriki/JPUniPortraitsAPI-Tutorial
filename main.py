# %%

import requests

# 共通するコンテンツを取得する関数を定義

base_url = "https://edit.portraits.niad.ac.jp/api/v1/SchoolBasicSurvey/"
accesskey = "XXXX"  # ご自身のキーを設定ください

# *************　関数定義　*************


def retrieve_content_data(api_type, year, orgid):
    """
    指定したAPIタイプ、年度、および組織IDを使用して、コンテンツデータを取得します。

    この関数は指定したURLからJSON形式のデータを取得し、その中から特定のコンテンツデータを抽出します。

    Parameters:
    api_type (str): APIの種類を示す文字列です。APIのエンドポイントに対応しています。
    year (int or str): 情報を取得する年度を示します。
    orgid (str): 情報を取得する組織のIDを示します。必要なIDはAPIの種類によって異なります。

    Returns:
    dict: 取得したコンテンツデータ。JSON形式のデータから抽出されます。

    Example:
    >>> content = retrieve_content_data("getSchoolFacilities", 2021, "0292")
    >>> print(content)
    { ... }

    Note:
    実行する前に`base_url`と`accesskey`が適切に設定されていることを確認してください。
    また、HTTPSリクエストはSSL/TLS証明書の検証を行います。
    """
    search_url = base_url + api_type
    payload = {"accesskey": accesskey, "year": year, "orgid": orgid}

    # *************　API呼び出し　*************
    res = requests.get(search_url, params=payload, verify=True)
    jsondata = res.json()

    status_flg_dict = jsondata["GET_STATUS_LIST"]["RESULT"]

    if status_flg_dict["STATUS"] != "0":
        print(status_flg_dict["ERROR_MSG"])
        return status_flg_dict["ERROR_MSG"]

    content_data = jsondata["GET_STATUS_LIST"]["DATALIST_INF"]["DATA_INF"][0]["CONTENT"]

    return content_data


# *************　データの取得・表示　*************
# 学校施設調査票API情報取得
# XX大学の寄宿舎施設の面積を取得

base_data = retrieve_content_data("getSchoolFacilities", 2021, "0292")


area_yoto = "寄宿舎施設"

for area_datum in base_data["GAKKO_TOCHI_YOTO_AREA"][0]["AREA"]:
    if area_datum["AREA_YOTO"] == area_yoto:
        print("寄宿舎施設の面積:" + area_datum["AREA"] + area_datum["AREA_TANI"])

# %%
# 学生教員等状況票API情報取得
# XX大学の職員数を取得

base_data = retrieve_content_data("getStudentFacultyStatus", 2021, "0292")

shokuin_data = base_data["SHOKUIN_SU"][0]
print("職員数:" + shokuin_data["SHOKUIN_SU_KEI"])

# %%
# 大学院学生内訳票API情報取得
# XX大学の入学志願者数(男)を取得

base_data = retrieve_content_data("getGraduateStudentsDetail", 2021, "0256-64-22-GS01-09-1")

nyugaku_data = base_data["NYUGAKU_JOKYO"]["SENKO"][0]
print("入学志願者数(男):" + nyugaku_data["NYUGAKU_SHIGANSHA_SU_KEI_M"])

# %%
# 本科学生内訳票API情報取得

# うまくいくはずなのに「該当データなし」になる...?
base_data = retrieve_content_data("getJuniorCollegeUndergraduateStudentsDetail", 2021, "0172")


# %%
# 外国人学生調査票API情報取得

# タイからの留学生数(女)を取得

base_data = retrieve_content_data("getForeignStudent", 2021, "0292-1Z11")
ryugakusei_data = base_data["RYUGAKUSEI"][0]["GAKUMON_KOKUBETSU"]
print("タイからの留学生数(女):" + ryugakusei_data["CHIIKI"][0]["KUNI_GAKUSEI_SU_KEI_F"])


# %%
# 卒業後の状況調査票(2-1)API情報取得
# XX大学院研究科に進学した学部生数(男)を取得
base_data = retrieve_content_data("getStatusAfterGraduationGraduates", 2021, "0292-27-27-1G01-00-1")
sotugyo_data = base_data["GAKKA_SENKO"][0]["JOKYO_SOTSUGYOSHA_SU"][0]
print("XX大学院研究科に進学した学部生数(男):" + sotugyo_data["SOTSUGYOSHA_SU"][0]["SOTSUGYOSHA_SU"])

# %%
# 卒業後の状況調査票(2-2)API情報取得
# 産業分類Eに就職した学生数(男)

base_data = retrieve_content_data("getStatusAfterGraduationJobs", 2021, "0292-27-27-1G01-00-1")
sotugyo_data = base_data["GAKKA_SENKO"][0]["SANGYO_SHUSHOKUSHA_SU"]["SHUSHOKUSHA_SU"]

sangyo_name = "E 製造業／7 電子部品・デバイス・電子回路製造業"

# 特定の産業分類に就職した学生数を出力
for sangyo_datum in sotugyo_data:
    if (sangyo_datum["SHUSHOKUSHA_SANGYO_BUNRUI"] == sangyo_name) & (sangyo_datum["SHUSHOKUSHA_SEX"] == "男"):
        print("産業分類Eに就職した学生数(男):" + sangyo_datum["SHUSHOKUSHA_SU"])
