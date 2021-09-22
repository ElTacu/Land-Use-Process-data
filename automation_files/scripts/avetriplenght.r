suppressMessages(library(reshape))
suppressMessages(library(Hmisc))

args = commandArgs(trailingOnly=TRUE)
root = args[1]

atl_trips = file.path(root,"model\\reports\\auto_files\\average_trip_length.csv")
outfile = file(atl_trips,"w")


source(paste(root,"j.model_setup.R", sep='/'))
###################################################################loadData()
mf.tdist <<- readEmme(bank, "mftdist")

load(file=paste(project.dir,"/model_hbo/mf.hbodth.dat", sep=""))
load(file=paste(project.dir,"/model_hbo/mf.hbodtm.dat", sep=""))
load(file=paste(project.dir,"/model_hbo/mf.hbodtl.dat", sep=""))

load(file=paste(project.dir,"/model_hbr/mf.hbrdth.dat", sep=""))
load(file=paste(project.dir,"/model_hbr/mf.hbrdtm.dat", sep=""))
load(file=paste(project.dir,"/model_hbr/mf.hbrdtl.dat", sep=""))

load(file=paste(project.dir,"/model_hbs/mf.hbsdth.dat", sep=""))
load(file=paste(project.dir,"/model_hbs/mf.hbsdtm.dat", sep=""))
load(file=paste(project.dir,"/model_hbs/mf.hbsdtl.dat", sep=""))

load(file=paste(project.dir,"/model_hbw/mf.hbwdth.dat", sep=""))
load(file=paste(project.dir,"/model_hbw/mf.hbwdtm.dat", sep=""))
load(file=paste(project.dir,"/model_hbw/mf.hbwdtl.dat", sep=""))

load(file=paste(project.dir,"/model_sc/mf.colldt.dat", sep=""))

load(file=paste(project.dir,"/model_nh/mf.nhbwdt.dat", sep=""))
load(file=paste(project.dir,"/model_nh/mf.nhnwdt.dat", sep=""))

load(file=paste(project.dir,"/model/mf.persontrips.dat", sep=""))

#HBSHOP 
mf.hs = mf.hbsdth + mf.hbsdtm + mf.hbsdtl
#HBR
mf.hr = mf.hbrdth + mf.hbrdtm + mf.hbrdtl 
#HBO
mf.ho = mf.hbodth + mf.hbodtm + mf.hbodtl
#total hbnw
mf.hbnw = mf.hs + mf.hr + mf.ho


#Home based work
mf.hmw = mf.hbwdth + mf.hbwdtm + mf.hbwdtl

avg_hbwdth = round(weighted.mean(mf.tdist, mf.hbwdth),digits = 1)
avg_hbwdtm = round(weighted.mean(mf.tdist, mf.hbwdtm),digits = 1)
avg_hbwdtl = round(weighted.mean(mf.tdist, mf.hbwdtl),digits = 1)
avg_hbw = round(weighted.mean(mf.tdist, mf.hmw),digits = 1)

avg_hs = round(weighted.mean(mf.tdist, mf.hs),digits = 1)
avg_hr = round(weighted.mean(mf.tdist, mf.hr),digits = 1)
avg_ho = round(weighted.mean(mf.tdist, mf.ho),digits = 1)
avg_hbnw = round(weighted.mean(mf.tdist, mf.hbnw),digits = 1)

avg_nhbwdt = round(weighted.mean(mf.tdist, mf.nhbwdt),digits = 1)
avg_nhnwdt = round(weighted.mean(mf.tdist, mf.nhnwdt),digits = 1)
tot_nhb = mf.nhbwdt + mf.nhnwdt
avg_nhb = round(weighted.mean(mf.tdist, tot_nhb),digits = 1)

avg_col = round(weighted.mean(mf.tdist, mf.colldt),digits = 1)

avg_all = round(weighted.mean(mf.tdist, mf.persontrips),digits = 1)

cat("hbwl","Low Inc",avg_hbwdtl,"\n",sep=",",file=outfile)
cat("hbwm","Med Inc",avg_hbwdtm,"\n",sep=",",file=outfile)
cat("hbwh","Hi Inc",avg_hbwdth,"\n",sep=",",file=outfile)
cat("TotalHBW","Total HBW",avg_hbw,"\n",sep=",",file=outfile)

cat("hbshop","Shop",avg_hs,"\n",sep=",",file=outfile)
cat("hbrec","Rec",avg_hr,"\n",sep=",",file=outfile)
cat("hbother","Other",avg_ho,"\n",sep=",",file=outfile)
cat("TotalHBNW","Total HNNW",avg_hbnw,"\n",sep=",",file=outfile)

cat("nhbw","Work ",avg_nhbwdt,"\n",sep=",",file=outfile)
cat("nhbnw","Non-Work",avg_nhnwdt,"\n",sep=",",file=outfile)
cat("TotalNHB","Total NHB",avg_nhb,"\n",sep=",",file=outfile)

cat("college","College",avg_col,"\n",sep=",",file=outfile)
cat("All","All Purpose",avg_all,"\n",sep=",",file=outfile)

close(outfile)