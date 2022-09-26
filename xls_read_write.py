import xlrd
import xlwt
wb = xlrd.open_workbook('MONTHLY SHIPMENT LOG TEMPLATE.xls')
book = xlwt.Workbook()
sheet1 = book.add_sheet('CURRENT')
sh = wb.sheet_by_index(0)

group_list = {
    "colnames": ['group_name', 'Bankers Trust', 'Centex', 'MISC G2 Subprime', 'SBMSI Master'],
    'abs':['_BT', '_CX', '_M2', '_SB'], 
    'mbs':[ 'BTR', '', '', 'SBA'],
    'alt_a':[ 'ZBT', '', 'ZM2', 'ZSB']
}
col_values = sh.col_values(1)
#col_values = col_values[1:len(col_values)] 
for j,k in enumerate(col_values):
    row_values = sh.row_values(j)
    if k in group_list['colnames']:
        for row_name in ['abs','mbs', 'alt_a']:
            for row_value in group_list[row_name]:
                for m,i in enumerate(row_values):
                    if i == row_value:
                        style = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
                        print(j, i, m)
                        sheet1.write(j, m , i , style)
                    else:
                        sheet1.write(j, m , i )
    else:
        for m,i in enumerate(row_values): 
            sheet1.write(j, m , i )
book.save('test.xls')
