import json
import config

class Check_Product_Model():
    def __init__(self, product_model_json, model_str):
        self.product_model_json = product_model_json # 產品選型 json檔
        self.model_str = model_str # 選型貨號
        with open(self.product_model_json , mode='r', encoding='utf-8') as json_file:
            self.dic = json.load(json_file)

        self.err = {'err': False, 'message': ''}
        self.check_1() # 檢查選型 數量
        if self.err['err'] == True:
            print(self.err['message'])
            return

        self.check_2() # 檢查選型 每個選型是否符合選項
        if self.err['err'] == True:
            print(self.err['message'])
            return        
        # print(self.dic)

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
        print(lis_model)

        for i, no in enumerate(lis_model):
            # print(i, no)
            # print(dic['model_order'][f'model_{i+1}'])
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

def test1():
    json_file = config.product_model_json_ar
    model_str = 'PAAR-AR-16-F-R-01-B-F-G-10-Y-V-'
    pm = Check_Product_Model(json_file, model_str)

def test2():
    json_file = config.product_model_json_pv
    model_str = 'PPV2-PV-046-PA-C-R-M-1-A-0-N-'
    pm = Check_Product_Model(json_file, model_str)

if __name__ == '__main__':
    test2()