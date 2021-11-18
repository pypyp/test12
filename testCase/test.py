import datetime,time,data
import xlrd

def change():
    l=[]
    measureTime ='2021-11-08 09:32:32'
    for i in range(1000):
        dict = {}
        dict["userId"] = 'dfs'
        dict["measureTime"] = measureTime
        measureTime = (datetime.datetime.strptime(measureTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        l.append(dict)
    dd = {
            "analysisModel": 0,
            "measures":l
    }
    return dd

def read_excel():
    #打开文件
    wb = xlrd.open_workbook(r'jiekou.xls')
    #获取所有sheet的名字
    print(wb.sheet_names())
    #获取第二个sheet的表明
    sheet2 = wb.sheet_names()[0]
    #sheet1索引从0开始，得到sheet1表的句柄
    sheet1 = wb.sheet_by_index(0)

    rowNum = sheet1.nrows
    colNum = sheet1.ncols
    print(rowNum,colNum)
    #s = sheet1.cell(1,0).value.encode('utf-8')
    s = sheet1.cell(3,2).value
    print(s)
    #获取某一个位置的数据
    # 1 ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    # print(sheet1.cell(1,2).ctype)
    # print(s)
    #print(s.decode('utf-8'))
    #获取整行和整列的数据
    #第二行数据
    row2 = sheet1.row_values(4)
    #第二列数据
    cols2 = sheet1.col_values(0)
    # print(row2,cols2)
    #python读取excel中单元格内容为日期的方式
    #返回类型有5种
    for i in range(rowNum):
        # print(sheet1.cell(i,3).ctype)
        if sheet1.cell(i,3).ctype == 1:
            print(i)
            # d = xlrd.xldate_as_tuple(sheet1.cell_value(i,2),wb.datemode)
            # print(d)
            # print(data(*d[:3]),end='')
            # print('\n')
if __name__ == '__main__':
    read_excel()
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(change())
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))