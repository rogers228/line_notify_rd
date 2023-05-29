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
        # 查詢製令結案碼
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

    def ger_tad_mtc(self, tc004, tc005):
        # 查詢製令移轉  最後一筆
        # tc004 製令單別
        # tc005 製令單號
        s = """SELECT TOP 10
            TC001,TC002,TC003,
            md1.MD002 AS MD002A ,TC006,RTRIM(c1.MW002) AS MW002A,
            md2.MD002 AS MD002B,TC008,RTRIM(c2.MW002)AS MW002B,ta.TA024,
            TC013,
            TC010,TC016,TC036,TC014,TC037
            From SFCTC as tc
                LEFT JOIN CMSMW as c1 ON tc.TC007 = c1.MW001
                LEFT JOIN CMSMW as c2 ON tc.TC009 = c2.MW001
                LEFT JOIN SFCTA as ta ON tc.TC004 = ta.TA001 AND tc.TC005 = ta.TA002 AND tc.TC008=ta.TA003
                LEFT JOIN ((SELECT MD001, MD002 FROM CMSMD) UNION (SELECT MA001, MA002 FROM PURMA)) as md1 ON tc.TC023 = md1.MD001
                LEFT JOIN ((SELECT MD001, MD002 FROM CMSMD) UNION (SELECT MA001, MA002 FROM PURMA)) as md2 ON tc.TC041 = md2.MD001
            WHERE
                TC004 LIKE '{0}' AND
                TC005 LIKE '{1}' 
            ORDER BY TC002 DESC
            """
        s = s.format(tc004, tc005)

        df = pd.read_sql(s, self.cn) #轉pd
        new_columns = {'TC001': '移轉單別', 'TC002': '移轉單號', 'TC003': '序號','MD002A': '移出單位', 'TC006': '移出工序',
            'MW002A': '移出製程','MD002B': '移入單位', 'TC008': '移入工序','MW002B': '移入製程', 'TC014':'驗收數量', 'TC010':'單位' }
        df = df.rename(columns=new_columns)
        return df
    # seArr = Array("TC001", "TC002", "TC003", _
    #               "md1.MD002", "TC006", "RTRIM(c1.MW002)", _
    #               "md2.MD002", "TC008", "RTRIM(c2.MW002)", "ta.TA024", _
    #               "CASE WHEN TC013 = 1 THEN '1.正常完成' WHEN TC013 = 2 THEN '2.重工完成' WHEN TC013 = 3 THEN '3.退回重工' WHEN TC013 = 4 THEN '4.撥轉' WHEN TC013 = 5 THEN '5.盤盈損' WHEN TC013 = 6 THEN '6.投入' Else '' END", _
    #               "TC010", "TC016", "TC036", "TC014", "TC037")
    # seArr_s = Array("單別", "單號", "序號", _
    #                 "移出部門", "工序", "製程", _
    #                 "移入部門", "工序", "製程", "製程敘述", _
    #                 "型態", _
    #                 "單位", "報廢數量", "移轉數量", "驗收數量", "驗退數量")

    #     strSQL = strSQL & " From SFCTC as tc"
    #     strSQL = strSQL & " LEFT JOIN CMSMW as c1 ON tc.TC007 = c1.MW001"
    #     strSQL = strSQL & " LEFT JOIN CMSMW as c2 ON tc.TC009 = c2.MW001"
    #     strSQL = strSQL & " LEFT JOIN SFCTA as ta ON tc.TC004 = ta.TA001 AND tc.TC005 = ta.TA002 AND tc.TC008=ta.TA003"
    #     strSQL = strSQL & " LEFT JOIN ((SELECT MD001, MD002 FROM CMSMD) UNION (SELECT MA001, MA002 FROM PURMA)) as md1 ON tc.TC023 = md1.MD001"
    #     strSQL = strSQL & " LEFT JOIN ((SELECT MD001, MD002 FROM CMSMD) UNION (SELECT MA001, MA002 FROM PURMA)) as md2 ON tc.TC041 = md2.MD001"
        
    #     strSQL = strSQL & " WHERE TC004 LIKE '" & .ListView2.SelectedItem.text & "' AND "
    #     strSQL = strSQL & "TC005 LIKE '" & .ListView2.SelectedItem.ListSubItems(1).text & "'"
    #     strSQL = strSQL & " ORDER BY TC006,TC002,TC003"

        # (MB080 NOT IN ('PPV1-PV-016-A0-2-R-K-1-A-0-N-'))
def test1():
    db = YST()
    # ans = db.ger_ptd_kd('3301', '20220728011','4A506039')
    # print(ans)

    # ans = db.ger_tad_kd('5101', '20220801001','2BBL0050050502')
    # print(ans)

    # df = db.ger_model('PPV1-')
    df = db.ger_tad_mtc('5107', '20221121005')
    pd.set_option('display.max_rows', df.shape[0]+1) # 顯示最多列
    pd.set_option('display.max_columns', None) #顯示最多欄位
    print(df)

if __name__ == '__main__':
    test1()