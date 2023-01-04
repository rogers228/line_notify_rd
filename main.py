import time, datetime
import load_excel_gp
import load_excel_wn
import line_notify_gp
import tool_db_yst
import tool_mylog

def check_release(): #檢查結案待發行
    log = tool_mylog.MyLog()
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    line = line_notify_gp.Line()
    xls = load_excel_wn.Load_xls()
    df = xls.get_cgp()
    for i, r in df.iterrows():
        message = f"{r['品號']} {r['品名']} 已結案可以發行 {r['變更後版次']} 版\n系統檢查時間為{sys_time}"
        # print(message)
        line.post_data(message)

    log.write('檢查結案待發行 完成')

def check_timeout(): #檢查待發行已達提醒時間
    log = tool_mylog.MyLog()
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    line = line_notify_gp.Line()
    xls = load_excel_wn.Load_xls()
    df = xls.get_hhk()
    for i, r in df.iterrows():
        message = f"{r['品號']} {r['品名']} 提醒日期已到期\n系統檢查時間為{sys_time}"
        # print(message)
        line.post_data(message)

    log.write('檢查待發行已達提醒時間 完成')

def check_draw(): #檢查回饋待改圖
    log = tool_mylog.MyLog()
    xls = load_excel_gp.Load_xls()
    n_count =   xls.get_nup_count() # 未修改數量
    last_date = xls.get_last_date() # 最後登錄日期
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())

    if n_count == 0:
        # 20220629增加功能: 若無資料需要維護，在每個星期一時，會推播訊息，讓使用者知道系統仍然有在工作
        today = datetime.date.today()
        if today.weekday() == 0: # 星期一
            message = f'感謝您，系統檢查0筆回饋待改，Excel最後登記日期為{last_date}，系統檢查時間為{sys_time}'
            # print(message)
            line = line_notify_gp.Line()
            line.post_data(message, 'goodjob01.jpg')
        else:
            print('nice! it\'s no data.') # 無資料須要維護

    else:
        d1 = datetime.datetime.strptime(str(last_date),'%Y-%m-%d'); d2 = datetime.datetime.today()
        image = 'bomb01.jpg' if (d2 - d1).days > 7 else 'comeon01.jpg'
        message = f'圖面回饋尚有 {n_count} 筆未修改！Excel最後登記日期為{last_date}，系統檢查時間為{sys_time}'
        line = line_notify_gp.Line()
        line.post_data(message, image)

    log.write('檢查回饋待改圖 完成')

def bom_gtk(): # 檢查 bom建立作業未確認
    log = tool_mylog.MyLog()
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    line = line_notify_gp.Line()
    db = tool_db_yst.YST()
    n_count = db.ger_bom_gtk() # 未確認數量

    if n_count == 0:
        today = datetime.date.today()
        if today.weekday() == 0: # 星期一
            message = f'BOM建立作業經查已全數確認無異常,感謝您!\n系統檢查時間為{sys_time}'
            # print(message)
            line.post_data(message)

        else:
            print('nice! it\'s no data.') # 無資料須要維護

    else:
        message = f"BOM建立作業尚有 {n_count} 筆未確認!\n系統檢查時間為{sys_time}"
        # print(message)
        line.post_data(message)

    log.write('檢查bom建立作業未確認 完成')

def bom_gfw(): # 檢查 bom變更單未確認
    log = tool_mylog.MyLog()
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    line = line_notify_gp.Line()
    db = tool_db_yst.YST()
    n_count = db.ger_bom_gfw() # 未確認數量

    if n_count == 0:
        today = datetime.date.today()
        if today.weekday() == 0: # 星期一
            message = f"BOM變更單經查已全數確認無異常,感謝您!\n系統檢查時間為{sys_time}"
            # print(message)
            line.post_data(message)

        else:
            print('nice! it\'s no data.') # 無資料須要維護

    else:
        message = f"BOM變更單尚有 {n_count} 筆未確認!\n系統檢查時間為{sys_time}"
        # print(message)
        line.post_data(message)
    
    log.write('檢查bom變更單未確認 完成')

def check_ysmd(): # 檢查ysmd網站
    sys_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    try:
        response = requests.get("http://www.yeoshe.tw")
        
    except:
        message = f'ysmd選型app異常!請檢查!，系統檢查時間為{sys_time}'
        print(message)
        line = line_notify_gp.Line()
        line.post_data(message)

    else:
        if response.status_code == 200:
            today = datetime.date.today()
            message = f'恭喜您! ysmd選型app正常運作，系統檢查時間為{sys_time}'
            if today.weekday() == 0: # 星期一
                line = line_notify_gp.Line()
                line.post_data(message)
            else:
                print(message)


def main():
    check_draw() # 檢查回饋待改圖
    check_release() #檢查結案待發行
    check_timeout() #檢查待發行已達提醒時間
    bom_gtk()       # 檢查 bom建立作業未確認
    bom_gfw()       # 檢查 bom變更單未確認
    check_ysmd()    # 檢查 ysmd選型app

if __name__ == '__main__':
    main()
    print('line_notify is finished')