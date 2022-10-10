import PyPDF2 
import csv
import xlrd

def get_rows_from_xls_file(file_path):
    rows = []
    wb = xlrd.open_workbook(file_path)
    sh = wb.sheet_by_index(0)
    col_values = sh.col_values(1)
    for j,k in enumerate(col_values):
        row_values = sh.row_values(j)
        rows.append(row_values)
    return rows
    
def get_rows_from_csv_file(file_path):
    rows = []
    with open(file_path, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows

def get_text_from_pdf_file(file_path):
    pdfFileObj = open(file_path, 'rb') 
    page_text = ""
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    for i in pdfReader.numPages:
        pageObj = pdfReader.getPage(i)  
        page_text += pageObj.extractText()
    pdfFileObj.close() 
    return page_text

if file_path.endswith('.pdf'):
    data = get_text_from_pdf_file(file_path)
elif file_path.endswith('.csv'):
    data = get_rows_from_csv_file(file_path)
elif file_path.endswith('.xls'):
    data = get_rows_from_xls_file(file_path)
