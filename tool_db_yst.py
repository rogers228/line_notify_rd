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

    def ger_model(self, model): # 依型號開頭碼查詢 品號 貨號
        # mgstr 廠商簡稱
        # 僅查詢 非正確的 wq06不是1者 
        s = """
            SELECT RTRIM(MB001) AS MB001,MB080
            FROM INVMB
            WHERE
                (MB002 NOT LIKE '%停用%') AND
                (MB080 LIKE '{0}%')
                AND (MB080 NOT IN (
                    SELECT wq02 FROM YEOSHE_MAKE.dbo.rec_wq WHERE wq02 LIKE '{0}%' AND wq06 = 1
                    ))
            """

        s = s.format(model)
        # print(s)
        df = pd.read_sql(s, self.cn) #轉pd
        return df



        # (MB080 NOT IN ('PPV1-PV-016-A0-2-R-K-1-A-0-N-'))
def test1():
    db = YST()
    # ans = db.ger_ptd_kd('3301', '20220728011','4A506039')
    # print(ans)

    # ans = db.ger_tad_kd('5101', '20220801001','2BBL0050050502')
    # print(ans)

    df = db.ger_model('PPV1-')
    print(df)

if __name__ == '__main__':
    test1()