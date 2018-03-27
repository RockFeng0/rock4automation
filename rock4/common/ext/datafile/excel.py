# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.datafile.excel

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      pyrunner.ext.datafile.excel,v 1.0 2016年3月16日
    FROM:   2016年3月16日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import os

class Excel():
    ''' xls/xlsx data process center. Please encode the system to utf-8 '''         
    def __init__(self):
        self.info_script = os.path.abspath(__file__)
    
    def open_excel(self,excel,sheet="Sheet1"):
        '''Sample usage:
            open_excel("d:/auto/buffer/test.xlsx","Sheet1")
        '''
        self.excel = self.excel_workbook(excel)
        self.sheet = self.excel_sheet(sheet)                
            
    def excel_nrows(self):        
        return self.sheet.nrows
    
    def excel_ncols(self):
        return self.sheet.ncols
    
    def excel_cellxy(self, rowx, colx):
        '''
        Sample usage:
            excel_cellxy(0,0)
            excel_cellxy(1,2)
        Return:
            cell value
        Description:
            If the cell value is number, 1234 will get as 1234.0, so fix this issue.
        
        Reference:
            http://stackoverflow.com/quespyrunnerns/2739989/reading-numeric-excel-data-as-text-using-xlrd-in-python
            http://www.lexicon.net/sjmachin/xlrd.html  (Search for "ctype")
            
            self.sheet.cell(rowx, colx).ctype:
                Type symbol    Type number    Python value
                XL_CELL_EMPTY    0           empty string u''
                XL_CELL_TEXT     1           a Unicode string
                XL_CELL_NUMBER   2           float
                XL_CELL_DATE     3           float
                XL_CELL_BOOLEAN  4           int; 1 means TRUE, 0 means FALSE
                ......
        '''
        
        cell_value = self.sheet.cell(rowx, colx).value
        
        if self.sheet.cell(rowx, colx).ctype in (2,3) and int(cell_value) == cell_value:
            cell_value = int(cell_value)
        #sys should encode to the encoding which is same as current edit tab. Such as utf-8
        
        return cell_value
    
    
    def excel_cell(self, rowx, col_name):
        ''' 
        Sample usage:
            excel_cell(0,"Title")
            excel_cell(0,"Name")
        return:
            the cell value that the row is rowx and column is col_name you specify. 
        '''        
        for colx in xrange(0, self.excel_ncols()):
            if self.excel_cellxy(0, colx) == col_name:                
                return self.excel_cellxy(rowx, colx)
     
    def excel_sheet(self,sheet):
        '''open the sheet in Excel
        Define:
            a xls/xlsx obj's sheet. named: self.sheet
        '''
        try:
            return self.excel.sheet_by_name(sheet)
        except Exception,e:
            raise Exception("\n\tp_dataprocess exception 2.0: ",e)
               
    def excel_workbook(self,excel):
        '''open the sheet in Excel
        Define:
            a xls/xlsx obj's excel. named: self.excel
        '''       
        if os.path.isfile(excel):
            import xlrd
            return xlrd.open_workbook(excel)            
        else:
            raise Exception("\n\tp_dataprocess exception 1.0: can't find a workbook('%s')." %(excel))

def usage_Excel():
    e = Excel()
    e.open_excel("d:/auto/buffer/test.xlsx", "TestCase")
    print repr(e.excel_cell(2, "CaseTypeSDFE"))
    print e.excel_cell(2, "Description")
    print "columns: %d, rows: %d" %(e.excel_ncols(),e.excel_nrows())
    
if __name__ == "__main__":
    usage_Excel()
    
    