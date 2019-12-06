import xlwt
from xlwt import *

# 设置分析输出的表格样式
# 表头样式设置
sheethead = XFStyle() # 初始化样式，此样式包含了单元格背景颜色和单元格边框两个属性。
pattern = Pattern()
pattern.pattern = Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 2 # 设置单元格背景色为红色
sheethead.pattern = pattern
borders = xlwt.Borders()#设置表格的边框，1是默认实线黑色。
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1
sheethead.borders = borders
# 检查项样式设置
stylecinfo = XFStyle()# 只有边框
borders = xlwt.Borders()
borders.left = 1
# borders.left = xlwt.Borders.THIN
borders.right = 1
borders.top = 1
borders.bottom = 1
stylecinfo.borders = borders
# 设备信息设置
styledinfo = XFStyle()# 初始化样式，带边框和表格内容居中。
borders = xlwt.Borders()
borders.left = 1
# borders.left = xlwt.Borders.THIN
borders.right = 1
borders.top = 1
borders.bottom = 1
styledinfo.borders = borders
alignment = xlwt.Alignment() # Create Alignment
alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
styledinfo.alignment = alignment