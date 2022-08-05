import pandas as pd
import pyodbc
import config

class YST(): # 一條件尋找產品
    def __init__(self):
        self.cn = pyodbc.connect(config.conn_yst) # connect str 連接字串

    def ger_fhi(self, mgstr): # 廠商簡稱回傳廠商代號
        # mgstr 廠商簡稱
        s = "SELECT TOP 1 MA001, MA002 FROM PURMA WHERE MA002 LIKE '{0}'"
        s = s.format(mgstr)
        df = pd.read_sql(s, self.cn) #轉pd
        return df.iloc[0]['MA001'].strip() if len(df.index) > 0 else ''

    def ger_ptd_kd(self, td001, td002, td004):
        # 查詢採購結案碼
        # N未結案 Y自動結案 y指定結案
        # '' 無紀錄回傳空字串
        # td001單別, td002單號, td004品號
        s = """
            SELECT TOP 1 TD016 FROM PURTD
            WHERE TD001 LIKE '{0}' AND
            TD002 LIKE '{1}' AND
            TD004 LIKE '{2}'
            """
        s = s.format(td001, td002, td004)
        df = pd.read_sql(s, self.cn) #轉pd
        # print(df)
        return df.iloc[0]['TD016'] if len(df.index) > 0 else ''

    def ger_tad_kd(self, ta001, ta002, ta006):
        # 查詢採購結案碼
        # 1.未生產,2.已發料,3.生產中,Y.已完工,y.指定完工
        # '' 無紀錄回傳空字串
        # ta001單別, ta002單號, ta006品號
        s = """
            SELECT TOP 1 TA011 FROM MOCTA
            WHERE TA001 LIKE '{0}' AND
            TA002 LIKE '{1}' AND
            TA006 LIKE '{2}'
            """
        s = s.format(ta001, ta002, ta006)
        df = pd.read_sql(s, self.cn) #轉pd
        # print(df)
        return df.iloc[0]['TA011'] if len(df.index) > 0 else ''

    def ger_bom_gtk(self): # BOM建立作業未確認 筆數
        s = """
            SELECT COUNT(*) FROM BOMMC
            WHERE MC016 LIKE 'N'
            """
        df = pd.read_sql(s, self.cn) #轉pd
        return df.iloc[0][0]

    def ger_bom_gfw(self): # BOM變更單未確認 筆數
        s = """
            SELECT COUNT(*) FROM BOMTA
            WHERE TA007 LIKE 'N'
            """
        df = pd.read_sql(s, self.cn) #轉pd
        return df.iloc[0][0]

def test1():
    db = YST()
    # ans = db.ger_ptd_kd('3301', '20220728011','4A506039')
    # print(ans)

    # ans = db.ger_tad_kd('5101', '20220801001','2BBL0050050502')
    # print(ans)

    ans = db.ger_bom_gfw()
    print(ans)

if __name__ == '__main__':
    test1()