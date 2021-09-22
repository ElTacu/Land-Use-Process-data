#District-to-district validation
#run from ./skims/valid_reports directory
args = commandArgs(trailingOnly=TRUE)
root = args[1]

source(file.path(root,"j.model_setup.R"))

load_ensemble("V:/tbm/joan/2010/iter1/ens/ens.gy.csv","gy")

load_mc_matrices(file.path(project.dir, 'model', fspe="/"))

mf.persons_hbw<-(mf.hwda + mf.hwdp + mf.hwpa + mf.hwbike + mf.hwprtr + mf.hwtr + mf.hwwalk)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\persons_hbw.csv"),"w")
district_squeeze_csv(mf.persons_hbw,ensemble.gy,"persons_hbw",outfile)
close(outfile)

mf.transit_hbw<-(mf.hwtr + mf.hwprtr)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\transit_hbw.csv"),"w")
district_squeeze_csv(mf.transit_hbw,ensemble.gy,"transit_hbw",outfile)
close(outfile)

mf.bike_hbw<-(mf.hwbike)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\bike_hbw.csv"),"w")
district_squeeze_csv(mf.bike_hbw,ensemble.gy,"bike_hbw",outfile)
close(outfile)

mf.active_hbw<-(mf.hwbike + mf.hwwalk)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\active_hbw.csv"),"w")
district_squeeze_csv(mf.active_hbw,ensemble.gy,"active_hbw",outfile)
close(outfile)

mf.persons_hbnw<-(mf.hoda + mf.hodp + mf.hopa + mf.hobike + mf.hoprtr + mf.hotr + mf.howalk + mf.hrda + mf.hrdp + mf.hrpa + mf.hrbike + mf.hrprtr + mf.hrtr + mf.hrwalk + mf.hsda + mf.hsdp + mf.hspa + mf.hsbike + mf.hsprtr + mf.hstr + mf.hswalk)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\persons_hbnw.csv"),"w")
district_squeeze_csv(mf.persons_hbnw,ensemble.gy,"persons_hbnw",outfile)
close(outfile)

mf.transit_hbnw<-(mf.hotr + mf.hoprtr + mf.hrprtr + mf.hrtr + mf.hsprtr + mf.hstr)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\transit_hbnw.csv"),"w")
district_squeeze_csv(mf.transit_hbnw,ensemble.gy,"transit_hbnw",outfile)
close(outfile)

mf.bike_hbnw<-(mf.hobike + mf.hrbike + mf.hsbike)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\bike_hbnw.csv"),"w")
district_squeeze_csv(mf.bike_hbnw,ensemble.gy,"bike_hbnw",outfile)
close(outfile)

mf.active_hbnw<-(mf.hobike + mf.howalk + mf.hrbike + mf.hrwalk + mf.hsbike + mf.hswalk)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\active_hbnw.csv"),"w")
district_squeeze_csv(mf.active_hbnw,ensemble.gy,"active_hbnw",outfile)
close(outfile)

mf.persons_nhb<-(mf.nhnwda + mf.nhnwdp + mf.nhnwpa + mf.nhnwbike + mf.nhnwtr + mf.nhnwwalk + mf.nhwda + mf.nhwdp + mf.nhwpa + mf.nhwbike + mf.nhwtr + mf.nhwwalk)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\persons_nhb.csv"),"w")
district_squeeze_csv(mf.persons_nhb,ensemble.gy,"persons_nhb",outfile)
close(outfile)

mf.transit_nhb<-(mf.nhnwtr + mf.nhwtr)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\transit_nhb.csv"),"w")
district_squeeze_csv(mf.transit_nhb,ensemble.gy,"transit_nhb",outfile)
close(outfile)

mf.bike_nhb<-(mf.nhnwbike + mf.nhwbike)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\bike_nhb.csv"),"w")
district_squeeze_csv(mf.bike_nhb,ensemble.gy,"bike_nhb",outfile)
close(outfile)

mf.active_nhb<-(mf.nhnwbike + mf.nhnwwalk + mf.nhwbike + mf.nhwwalk)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\active_nhb.csv"),"w")
district_squeeze_csv(mf.active_nhb,ensemble.gy,"active_nhb",outfile)
close(outfile)

persons_all<-(mf.persons_hbw + mf.persons_hbnw + mf.persons_nhb + mf.hbcda + mf.hbcdp + mf.hbcpa + mf.hbcbike + mf.hbcprtr + mf.hbctr + mf.hbcwalk + mf.schveh + mf.schpas + mf.schbus + mf.scwabi + mf.schtr)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\persons_all.csv"),"w")
district_squeeze_csv(persons_all,ensemble.gy,"persons_all",outfile)
close(outfile)

transit_all<-(mf.transit_hbw + mf.transit_hbnw + mf.transit_nhb + mf.hbcprtr + mf.hbctr + mf.schtr)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\transit_all.csv"),"w")
district_squeeze_csv(transit_all,ensemble.gy,"transit_all",outfile)
close(outfile)

mf.schbike<- mf.scwabi*0.1875
bike_all<-(mf.bike_hbw + mf.bike_hbnw + mf.bike_nhb + mf.hbcbike + mf.schbike)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\bike_all.csv"),"w")
district_squeeze_csv(bike_all,ensemble.gy,"bike_all",outfile)
close(outfile)

active_all<-(mf.active_hbw + mf.active_hbnw + mf.active_nhb + mf.hbcbike + mf.hbcwalk + mf.scwabi)
outfile<-file(file.path(root,"model\\reports\\auto_files\\dist2dist\\active_all.csv"),"w")
district_squeeze_csv(active_all,ensemble.gy,"active_all",outfile)
close(outfile)