import pandas as pd
import time
import pyodbc
import config

class MAKE(): # 一條件尋找產品
    def __init__(self):
        self.cn = pyodbc.connect(config.conn_MAKE) # connect str 連接字串

    def get_wp12_sh(self): # 查詢不空白的產品貨號屬性碼
        s = """
            SELECT wp01,wp05,wp12,wp13,wp15 FROM rec_wp
            WHERE ISNULL(DATALENGTH(wp12),0) != 0
            """
        df = pd.read_sql(s, self.cn) #轉pd
        return df

    def get_newid_wq(self): # 查詢rec_wq new id
        s = """
            SELECT TOP 1 wq01 FROM rec_wq
            ORDER BY wq01 DESC
            """
        df = pd.read_sql(s, self.cn) #轉pd
        return df.iloc[0]['wq01']+1 if len(df.index)>0 else 1

    def is_wq02_exist(self, wq02): # 貨號是否存在
        s = "SELECT TOP 1 wq01 FROM rec_wq WHERE wq02 = '{0}'"
        s = s.format(wq02)
        df = pd.read_sql(s, self.cn) #轉pd
        return True if len(df.index)>0 else False

    def get_wq_err_count(self): # wq錯誤筆數
        # mgstr 廠商簡稱
        # s = "SELECT TOP 1 * FROM rec_wp"
        s = "SELECT COUNT(*) FROM rec_wq WHERE wq06 = 9"
        df = pd.read_sql(s, self.cn) #轉pd
        return df.iloc[0][0]

    def get_test1(self): # 廠商簡稱回傳廠商代號
        # mgstr 廠商簡稱
        s = "SELECT TOP 1 * FROM rec_wp"
        # s = "SELECT * FROM rec_wq"
        # s = "SELECT wq02,wq03,wq06 FROM rec_wq WHERE wq02 LIKE 'PPV1-%' AND wq06 = 1"
        df = pd.read_sql(s, self.cn) #轉pd
        return df

    def myedit_wq(self, dic_argument): # 新增或修改rec_wq
        # 依照貨號是否存在來判斷
        # 存在時則修改 不存在則新增
        dic = dic_argument
        s = ''
        curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime()) # 14碼時間
        if self.is_wq02_exist(dic['wq02']):
            # 存在時修改
            s = """
                UPDATE rec_wq
                SET wq03 = '{1}', wq04 = {2}, wq05 = '{3}', wq06 = {4}, wq07 = '{5}'
                WHERE wq02 = '{0}'
                """.format(dic['wq02'],dic['wq03'],dic['wq04'],curr_time, dic['wq06'],dic['wq07'])
        else:
            # 不存在時新增
            new_id = self.get_newid_wq()
            s = """
                INSERT INTO rec_wq (wq01,wq02,wq03,wq04,wq05,wq06,wq07)
                VALUES ({0},'{1}','{2}',{3},'{4}',{5},'{6}')
                """.format(new_id, dic['wq02'],dic['wq03'],dic['wq04'],curr_time, dic['wq06'],dic['wq07'])

        try:
            cur = self.cn.cursor()
            cur.execute(s) #執行
            cur.commit() #更新
            cur.close() #關閉
        except:
            print('error!')
            print(s)

    def runsql(self):
        SQL = 'ALTER TABLE rec_wp ADD wp15 int'
        # curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # SQL = """
        #     INSERT INTO rec_wq (wq01,wq02,wq03,wq04,wq05,wq06,wq07)
        #     VALUES ({0},'{1}','{2}',{3},'{4}',{5},'{6}')
        #     """
        # SQL=SQL.format(
        #     2,
        #     'PPV1-PV-016-A0-2-R-M-1-A-0-N-',
        #     '6AA03AA001AA1A01',
        #     4,
        #     curr_time,
        #     1,
        #     '')

        try:
            cur = self.cn.cursor()
            cur.execute(SQL) #執行
            cur.commit() #更新
            cur.close() #關閉
        except:
            print('error!')
            print(SQL)

def test1():
    db = MAKE()
    df = db.get_test1()
    print(df)

    # print(db.get_wq_err_count())
    # db.runsql()

if __name__ == '__main__':
    test1()
