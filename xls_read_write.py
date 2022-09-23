import xlrd
wb = xlrd.open_workbook('MONTHLY SHIPMENT LOG TEMPLATE.xls')
sh = wb.sheet_by_index(0)
for i in range(0,2): 
    col_values = sh.col_values(i)
    col_values = col_values[1:len(col_values)] 
    for j,k in enumerate(col_values):
        row_values = sh.row_values(j)
        row_values =  row_values[1:len(row_values)]
        print(k, row_values[7:10])
