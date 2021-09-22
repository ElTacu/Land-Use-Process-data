options(java.parameters = "-Xmx4g" )
library("XLConnect")
wb = loadWorkbook("H:/rtp/2018rtp/jan2016runs/2015/iter14/model/reports/CutlineComparison_results.xlsx",create=F)
excel.file <- file.path("H:/rtp/2018rtp/jan2016runs/2015/iter14/model/reports/CutlineComparison_results.xlsx")
elements <- readWorksheetFromFile(excel.file, sheet=1)
# elements
saveWorkbook(wb)
