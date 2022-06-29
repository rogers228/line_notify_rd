import time, datetime
import load_excel_gp
import line_notify_gp

def main():
    xls = load_excel_gp.Load_xls()
    n_count =   xls.get_nup_count() # 未修改數量
    last_date = xls.get_last_date() # 最後登錄日期
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())

    if n_count == 0:
        # 20220629增加功能: 若無資料需要維護，在每個星期一時，會推播訊息，讓使用者知道系統仍然有在工作
        today = datetime.date.today()
        # print(today)
        # print(type(today))
        # print(today.weekday())
    
        if today.weekday() == 0: # 星期一
            message = f'感謝您，系統檢查0筆回饋待改，Excel最後登記日期為{last_date}，系統檢查時間為{sys_time}'
            # print(message)
            line = line_notify_gp.Line()
            line.post_data(message)
        else:
            print('nice! it\'s no data.') # 無資料須要維護

        return
    else:
        message = f'圖面回饋尚有 {n_count} 筆未修改！Excel最後登記日期為{last_date}，系統檢查時間為{sys_time}'
        # print(message)
        line = line_notify_gp.Line()
        line.post_data(message)

if __name__ == '__main__':
    main()
    print('ok')