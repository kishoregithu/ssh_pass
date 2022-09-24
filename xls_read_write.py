import xlrd
import xlwt
wb = xlrd.open_workbook('MONTHLY SHIPMENT LOG TEMPLATE.xls')
book = xlwt.Workbook()
sheet1 = book.add_sheet('CURRENT')
sh = wb.sheet_by_index(0)

col_values = sh.col_values(1)
#col_values = col_values[1:len(col_values)] 
for j,k in enumerate(col_values):
    row_values = sh.row_values(j)
    #row_values =  row_values[1:len(row_values)]
    #print(k, row_values[7:10])
    if 'ABS' in row_values[8]:
        style = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
        print(j, row_values[8])
        sheet1.write(j, 7, 'ABS', style)

book.save('test.xls')
