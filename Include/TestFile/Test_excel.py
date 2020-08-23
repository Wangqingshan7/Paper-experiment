import xlwt
book = xlwt.Workbook() # 新建工作簿
table = book.add_sheet('Over',cell_overwrite_ok=True) # 如果对同一单元格重复操作会发生overwrite Exception，cell_overwrite_ok为可覆盖
#sheet = book.add_sheet('Test') # 添加工作页
#sheet.write(1,1,'A') # 行，列，属性值 (1,1)为B2元素，从0开始计数
style = xlwt.XFStyle() # 新建样式
font = xlwt.Font() #新建字体
font.name = 'Times New Roman'
font.bold = True
style.font = font # 将style的字体设置为font
table.write(0,0,'Test',style)
book.save(filename_or_stream='Test.xls')