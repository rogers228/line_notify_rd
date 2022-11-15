import os
import json
import config
import tool_db_yst
import tool_db_make

class Check_Product_Model():
    def __init__(self, product_model_json, model_str, special_m):
        self.product_model_json = product_model_json # 產品選型 json檔
        self.model_str = model_str # 選型貨號
        self.special_m = special_m # 特殊代碼是第幾碼
        with open(self.product_model_json , mode='r', encoding='utf-8') as json_file:
            self.dic = json.load(json_file)

        self.err = {'err': False, 'message': ''}
        self.check_1() # 檢查選型 數量
        if self.err['err'] == True:
            # print(self.err['message'])
            return

        self.check_2() # 檢查選型 每個選型是否符合選項
        if self.err['err'] == True:
            # print(self.err['message'])
            return
        # print(self.dic)

        self.check_3() # 檢查選型 是否符合規則
        if self.err['err'] == True:
            # print(self.err['message'])
            return

    def get_err(self):
        return self.err

    def check_1(self): # 檢查選型 數量
        err = self.err
        dic = self.dic
        # print(self.model_str)
        lis_model = self.model_str.split('-')
        # print(lis_model)
        # print(dic['model_info'])
        if len(lis_model)-1 != dic['model_info']['m_count']:
            err['err'] = True; err['message'] = '選型數量不符!'; 
            return

    def check_2(self): # 檢查選型 每個選型是否符合選項
        err = self.err
        dic = self.dic
        # print(self.model_str)

        # 選型
        lis_model = self.model_str.split('-')[1:] # 不含首個
        # print(lis_model)
        # 將無記號替換為□ 以符合json
        for i, no in enumerate(lis_model):
            if no == '':
                lis_model[i] = '□'
        # print(lis_model)

        for i, no in enumerate(lis_model):
            # print(i, no)
            # print(dic['model_order'][f'model_{i+1}'])

            if (i+1) == self.special_m:
                # 目前為特殊代碼 故不檢查
                continue

            if no not in dic['model_order'][f'model_{i+1}']:
                options = ','.join(dic['model_order'][f'model_{i+1}'])
                err['err'] = True; err['message'] = f"第{i+1}個選型{no}不在選項{options}內"; 
                return

        # 檢查父子選項
        # print(dic['model_ischild'])
        for child, parent in dic['model_ischild'].items():
            # print(child, parent)
            no_parent = lis_model[int(parent)-1]
            # print('no_parent:', no_parent)
            no_child = lis_model[int(child)-1]
            # print('no_child:', no_child)
            # print(list(dic['model_child_memo'].keys()))
            # print(f'model_{parent}_{child}')
            if f'model_{parent}_{child}' in list(dic['model_child_memo'].keys()):
                lis_parent_options = list(dic['model_child_memo'][f'model_{parent}_{child}'].keys())
                # print(lis_parent_options)
                for parent_options in lis_parent_options:
                    if no_parent in parent_options.split(','):
                        # print('no_parent:', no_parent, 'isin')
                        lis_parent_child = list(dic['model_child_memo'][f'model_{parent}_{child}'][parent_options].keys())
                        # print(lis_parent_child)
                        if no_child not in lis_parent_child:
                            err['err'] = True; err['message'] = f"第{parent}父選項{no_parent}時,第{child}選項{no_child}不在選項{lis_parent_child}內"
                            return

    def check_3(self): # 檢查選型 是否符合規則
        err = self.err
        dic = self.dic
        # print(self.model_str)

        # 選型
        lis_model = self.model_str.split('-')[1:] # 不含首個
        # print(lis_model)
        # 將無記號替換為□ 以符合json
        for i, no in enumerate(lis_model):
            if no == '':
                lis_model[i] = '□'
        # print(lis_model)
        # print(list(dic['model_disable']['model_2'].keys()))

        for i, no in enumerate(lis_model):
            n = i+1 #第幾碼
            # print(f'n:{n}, no:{no}')
            # print(list(dic['model_disable'][f'model_{n}'].keys()))
            lis_selected = list(map(lambda e: e.replace('selected_',''), list(dic['model_disable'][f'model_{n}'].keys())))
            # print(lis_selected)

            # if all([
            #     no in lis_selected,
            #     dic['model_disable'][f'model_{n}'][f'selected_{no}'] != {}
            #     ]):
            if no in lis_selected:
                if dic['model_disable'][f'model_{n}'][f'selected_{no}'] != {}:
                    # print(f'no:{no} is have low')
                    dic_low = dic['model_disable'][f'model_{n}'][f'selected_{no}']
                    # print(dic_low)

                    for disable_m, lis_disable in dic_low.items():
                        # print(disable_m)
                        dm = int(disable_m.replace('disable_m_',''))
                        # print('dm:', dm)
                        # print(lis_disable)
                        if lis_model[dm-1] in lis_disable:
                            # print(f'第{n}碼選型{no}時,第{dm}碼不可選{lis_model[dm-1]}')
                            err['err'] = True; err['message'] = f'第{n}碼選型{no}時,第{dm}碼不可選{lis_model[dm-1]}'
                            return

class Check_Model(): # 檢查產品選型
    def __init__(self):
        # db
        self.yst = tool_db_yst.YST()
        self.make= tool_db_make.MAKE()
        self.check_1()

    def check_1(self): # 檢查
        yst = self.yst
        make = self.make

        df_wp12 = make.get_wp12_sh()
        df_wp12[['wp15']] = df_wp12[['wp15']].fillna(value=0) # 特殊代碼null填充為0
        # print(df_wp12)

        if len(df_wp12.index) == 0:
            return
        #     print(f'即將檢查筆數:{len(df_wp12.index)}')

        for i, r in df_wp12.iterrows():
            # 將無記號替換為□ 以符合json
            if r['wp13']:
                lis_none = r['wp13'].split(',')
                lis_none = list(filter(None, lis_none)) # 移除空白
                lis_none = list(map(lambda e: int(e) , lis_none)) # 轉數字
                # print(lis_none)

            # print(i)
            # print(r['wp05'])
            json_file = os.path.join(config.product_model_json_path, f"{r['wp05']}.json") 
            # print('json_file:', json_file)
            lis_m_start = r['wp12'].split(',') # 產品選型屬性開頭碼
            lis_m_start = list(filter(None, lis_m_start)) # 移除空白
            special_m = int(r['wp15']) # 特殊代碼是第幾碼
            # print('special_m:', special_m)
            # print(lis_model)
            for model in lis_m_start:
                # print(model)
                df = yst.ger_model(model)
                if len(df.index) > 0:
                    print(f'model:{model}, 即將檢查筆數:{len(df.index)}')
                else:
                    continue
                
                for j, rm in df.iterrows():
                    # print("rm['MB080']:", rm['MB080'])
                    lis_model = rm['MB080'].split('-')
                    # print(lis_model)
                    # 將無記號替換為□ 以符合json
                    for none_m in lis_none:
                        if lis_model[none_m] == 'N':
                            lis_model[none_m] = '□'
                    # print(lis_model)
                    model_str = '-'.join(lis_model)
                    
                    # 檢查選型 
                    cpm = Check_Product_Model(json_file, model_str, special_m)
                    cpm_dic = cpm.get_err()

                    dic = {} # 寫入資料庫引數
                    dic['wq02'] = rm['MB080'] # 貨號
                    dic['wq03'] = rm['MB001'] # 品號
                    dic['wq04'] = r['wp01'] # 產品選型id
                    if cpm_dic['err'] == False: # 選型正確
                        dic['wq06'] = 1 # 0未查詢需要查循 1正確 9查詢後錯誤
                        dic['wq07'] = ''

                    elif cpm_dic['err'] == True: # 選型錯誤不合法
                        # print('model_str:', model_str)
                        # print(cpm_dic['message'])
                        dic['wq06'] = 9 # 0未查詢需要查循 1正確 9查詢後錯誤
                        dic['wq07'] = cpm_dic['message']
                    # print(dic)
                    make.myedit_wq(dic) # 將檢查結果寫入資料庫

def test1():
    json_file = config.product_model_json_ar
    model_str = 'PAAR-AR-16-F-R-01-B-F-G-10-Y-V-'
    pm = Check_Product_Model(json_file, model_str)

def test2():
    json_file = config.product_model_json_pv
    model_str = 'PPV2-PV-046-PA-A-R-M-1-A-0-N-'
    pm = Check_Product_Model(json_file, model_str)

def main():
    Check_Model() # 檢查產品選型

if __name__ == '__main__':
    main()