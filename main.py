import time
import load_excel_gp
import line_notify_gp

def main():
    xls = load_excel_gp.Load_xls()
    n_count =   xls.get_nup_count() # 未修改數量
    last_date = xls.get_last_date() # 最後登入日期
    sys_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    if n_count == 0:
        print('no data')
        return
    else:
        message = f'圖面回饋尚有 {n_count} 筆未修改！Excel最後登記日期為{last_date}，系統檢查時間為{sys_time}'
        # print(message)
        line = line_notify_gp.Line()
        line.post_data(message)

if __name__ == '__main__':
    main()
    print('ok')