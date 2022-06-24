import time
import openpyxl
import pandas as pd
import json
import config

class Load_xls(): #讀取excel
    def __init__(self):
        self.file = config.sys_excel
        self.wb = openpyxl.load_workbook(self.file)
        self.sh = self.wb['車銑床回饋區']
        self.x_title = 1 #標題列位置
        self.x_data_statr = 2 # 資料開始
        self.x_data_over = 500 #資料結束
        self.load_df() # load data return self.df

    def load_df(self): # 產品資料
        sh = self.sh
        x_title = self.x_title #標題列位置
        x_data_statr = self.x_data_statr # 資料開始
        x_data_over  = self.x_data_over  #資料結束
        lis_title = []
        for i in range(1, sh.max_column+1):
            lis_title.append(sh.cell(x_title,i).value)

        # print(lis_title)
        lis_standard = {'日期': None,'提出人': None,'圖號(版別)': None,'問題': None,'完成日期': None,
                        '修改人員\n(改完簽名)': None} # 合法欄位 excel第n欄
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
                row_data.append(sh.cell(i, lis_standard[key]).value)
            lis_data.append(row_data)
        # print(lis_data)
        df = pd.DataFrame(lis_data, columns = lis_standard) # 建立 DataFrame
        df = df.fillna('') # 填充NaN為空白
        self.df = df

    def get_nup(self): # 尚未修改的資料
        df = self.df
        df_w = df.loc[(df['日期'] != '') & (df['完成日期'] == '')] # 篩選
        df_g = df_w.copy() #複製
        df_g['日期'] =  pd.to_datetime(df_g['日期'], format='Y-%m-%d') # 時間格式化  轉時間
        df_g['日期'] = df_g['日期'].dt.strftime('%Y-%m-%d')  #格式化後 再轉回文字
        return df_g

    def getjson_nup(self):
        df = self.get_nup()
        # print(df) , date_format='iso'
        json_str = '{"data":' + df.to_json(orient="records") + '}'

        dic_data = json.loads(json_str)  # string-json variable to dict
        dic_data['lasttime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        json_s = json.dumps(dic_data, indent=4, ensure_ascii=False) # dict to format json
        return json_s

    def get_nup_count(self):
        df = self.get_nup()
        return len(df.index)

    def get_last_date(self): # 最後登入日期
        df = self.df
        df_w = df.loc[df['日期'] != ''] # 篩選
        # print(df_w)
        last_date = df_w["日期"].max().to_period('D')
        return last_date


def test1():
    xls = Load_xls()
    print(xls.get_nup_count())
    print(xls.get_last_date())

    # xls.get_last_date()

if __name__ == '__main__':
    test1()
    print('ok')