import time
import openpyxl
import pandas as pd
import json
import config
import tool_db_yst

class Load_xls(): #讀取excel
    def __init__(self):
        self.file = config.excel_wn
        self.wb = openpyxl.load_workbook(self.file)
        self.sh = self.wb['待追蹤、修改']
        self.x_title = 1 #標題列位置
        self.x_data_statr = 2 # 資料開始
        self.x_data_over = 500 #資料結束
        self.load_df() # load data return self.df
        self.db = tool_db_yst.YST() 

    def load_df(self): # 產品資料
        sh = self.sh
        x_title = self.x_title #標題列位置
        x_data_statr = self.x_data_statr # 資料開始
        x_data_over  = self.x_data_over  #資料結束
        lis_title = []
        for i in range(1, sh.max_column+1):
            lis_title.append(sh.cell(x_title,i).value)

        # print(lis_title)
        lis_standard = {'品號': None,'品名': None,'變更後版次': None,'收件日': None,'最近檢查日期': None,
                        '單別': None,'單號': None,'提醒日期': None,'製程進度': None} # 合法欄位 excel第n欄

        for e in list(lis_standard.keys()):
            if e in lis_title:
                for i in range(1, sh.max_column+1):
                    if e == sh.cell(x_title, i).value:
                        lis_standard[e] = i
                        break
            else:
                self.err = {'is_err': True, 'message': f"缺少 '{e}' 欄位!"}
                print(self.err)
                return
        # print(lis_standard)

        lis_data = []
        for i in range(x_data_statr, x_data_over+1):
            row_data = []
            for key in list(lis_standard.keys()):
                myvalue = str(sh.cell(i, lis_standard[key]).value)
                if myvalue == 'None':
                    myvalue = ''
                row_data.append(myvalue)
                # row_data.append(str(sh.cell(i, lis_standard[key]).value))
            lis_data.append(row_data)
        # print(lis_data)
        df = pd.DataFrame(lis_data, columns = lis_standard) # 建立 DataFrame
        df = df.fillna('') # 填充NaN為空白
        df['收件日'] =  pd.to_datetime(df['收件日'], format='%Y-%m-%d %H:%M:%S')
        self.df = df


    def get_cgp(self): #應查詢資料
        df = self.df
        db = self.db

        df_w = df.loc[(df['品號'] != '') & (df['單別'] != '')] # 篩選

        lis_data = []
        for i, r in df_w.iterrows():
            if str(r['單別'])[:1] == '3':
                # print(r['單別'])
                # print(r['單號'])
                # print(r['品號'])
                # kd = db.ger_ptd_kd(r['單別'], r['單號'], r['品號']) 
                # print('kd:', kd)
                if db.ger_ptd_kd(r['單別'], r['單號'], r['品號']) in ['y', 'Y']:
                    lis_data.append([r['品號'], r['品名'], r['變更後版次']])

            elif str(r['單別'])[:1] == '5':
                # kd = db.ger_tad_kd(r['單別'], r['單號'], r['品號']) 
                # print('kd:', kd)                
                if db.ger_tad_kd(r['單別'], r['單號'], r['品號']) in ['y', 'Y']:
                    lis_data.append([r['品號'], r['品名'], r['變更後版次']])

        # print(lis_data)
        df_y = pd.DataFrame(lis_data, columns = ['品號', '品名', '變更後版次']) # 建立 DataFrame
        df_y = df_y.fillna('') # 填充NaN為空白
        return df_y

    def test(self):
        df = self.df
        pd.set_option('display.max_rows', df.shape[0]+1) # 顯示最多列
        pd.set_option('display.max_columns', None) #顯示最多欄位
        print(df)
        print(df.dtypes) # 所有欄位資料類型

def test1():
    xls = Load_xls()
    xls.test()
    # df = xls.get_cgp()
    # print(df)
    
    # xls.get_last_date()

if __name__ == '__main__':
    test1()
    print('ok')