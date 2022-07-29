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

    # def ger_fst(self, mgstr): # 線別回傳線別代號
    #     s = "SELECT TOP 1 MD001 FROM CMSMD WHERE MD002 LIKE '{0}'"
    #     s = s.format(mgstr)
    #     df = pd.read_sql(s, self.cn) #轉pd
    #     return df.iloc[0]['MD001'].strip() if len(df.index) > 0 else ''

    # def ger_ffdic(self, mgstr): # 供應商回傳dic資訊
    #     dic = {'內外':0,'代號':''}
    #     fhi = self.ger_fhi(mgstr) #供應商
    #     if fhi != '':
    #         dic['內外'] = 2
    #         dic['代號'] = fhi
    #         return dic
    #     fst = self.ger_fst(mgstr) #供應商
    #     if fst != '':
    #         dic['內外'] = 1
    #         dic['代號'] = fst
    #         return dic
    #     return dic

    # def ger_cms_count(self): # 製程回傳製程代號
    #     # mgstr 廠商簡稱
    #     s = "SELECT COUNT(*) FROM CMSMW"
    #     df = pd.read_sql(s, self.cn) #轉pd
    #     return df.iloc[0][0]

    # def ger_cms_all(self): # 製程回傳製程代號
    #     # mgstr 廠商簡稱
    #     s = "SELECT MW001, MW002 FROM CMSMW ORDER BY MW001"
    #     df = pd.read_sql(s, self.cn) #轉pd
    #     return df

    # def ger_cms(self, mgstr): # 製程回傳製程代號
    #     # mgstr 廠商簡稱
    #     s = "SELECT TOP 1 MW001, MW002 FROM CMSMW WHERE MW002 LIKE '{0}'"
    #     s = s.format(mgstr)
    #     df = pd.read_sql(s, self.cn) #轉pd
    #     return df.iloc[0]['MW001'] if len(df.index) > 0 else ''

def test1():
    db = YST()
    ans = db.ger_ptd_kd('3301', '20220728011','4A506039')
    print(ans)

    ans = db.ger_tad_kd('5101', '20220801001','2BBL0050050502')
    print(ans)


if __name__ == '__main__':
    test1()