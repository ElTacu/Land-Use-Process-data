#District-to-district validation
#run from ./skims/valid_reports directory
args = commandArgs(trailingOnly=TRUE)
root = args[1]

source(file.path(root,"j.model_setup.R"))

load_ensemble("V:/tbm/joan/2010/iter1/ens/ens.gy.csv","gy")

load_ensemble("V:/tbm/joan/2010/iter1/ens/ens.gz.csv","gz")

load_mc_matrices(file.path(project.dir, 'model', fspe="/"))


create_csv <- function(path, obj, name)
{
    name_comp = sprintf("model\\reports\\auto_files\\dist2dist\\%s.csv",name)
    file_path = file.path(path,name_comp)
    outfile = file(file_path,"w")
    district_squeeze_csv(obj, ensemble.gy, name, outfile)
    close(outfile)    
}

create_csv_gz <- function(path, obj, name)
{
    name_comp = sprintf("model\\reports\\auto_files\\dist2dist\\%s_gz.csv",name)
    file_path = file.path(path,name_comp)
    outfile = file(file_path,"w")
    district_squeeze_csv(obj, ensemble.gz, name, outfile)
    close(outfile)    
}

mf.persons_hbw = (mf.hwda + mf.hwdp + mf.hwpa + mf.hwbike + mf.hwprtr + mf.hwtr + mf.hwwalk)
create_csv(root,mf.persons_hbw,"persons_hbw")
create_csv_gz(root,mf.persons_hbw,"persons_hbw")

mf.transit_hbw<-(mf.hwtr + mf.hwprtr)
create_csv(root,mf.transit_hbw,"transit_hbw")
create_csv_gz(root,mf.transit_hbw,"transit_hbw")

mf.bike_hbw<-(mf.hwbike)
create_csv(root,mf.bike_hbw,"bike_hbw")
create_csv_gz(root,mf.bike_hbw,"bike_hbw")

mf.active_hbw<-(mf.hwbike + mf.hwwalk)
create_csv(root,mf.active_hbw,"active_hbw")
create_csv_gz(root,mf.active_hbw,"active_hbw")

mf.persons_hbnw<-(mf.hoda + mf.hodp + mf.hopa + mf.hobike + mf.hoprtr + mf.hotr + mf.howalk + mf.hrda + mf.hrdp + mf.hrpa + mf.hrbike + mf.hrprtr + mf.hrtr + mf.hrwalk + mf.hsda + mf.hsdp + mf.hspa + mf.hsbike + mf.hsprtr + mf.hstr + mf.hswalk)
create_csv(root,mf.persons_hbnw,"persons_hbnw")
create_csv_gz(root,mf.persons_hbnw,"persons_hbnw")

mf.transit_hbnw<-(mf.hotr + mf.hoprtr + mf.hrprtr + mf.hrtr + mf.hsprtr + mf.hstr)
create_csv(root,mf.transit_hbnw,"transit_hbnw")
create_csv_gz(root,mf.transit_hbnw,"transit_hbnw")

mf.bike_hbnw<-(mf.hobike + mf.hrbike + mf.hsbike)
create_csv(root,mf.bike_hbnw,"bike_hbnw")
create_csv_gz(root,mf.bike_hbnw,"bike_hbnw")

mf.active_hbnw<-(mf.hobike + mf.howalk + mf.hrbike + mf.hrwalk + mf.hsbike + mf.hswalk)
create_csv(root,mf.active_hbnw,"active_hbnw")
create_csv_gz(root,mf.active_hbnw,"active_hbnw")

mf.persons_nhb<-(mf.nhnwda + mf.nhnwdp + mf.nhnwpa + mf.nhnwbike + mf.nhnwtr + mf.nhnwwalk + mf.nhwda + mf.nhwdp + mf.nhwpa + mf.nhwbike + mf.nhwtr + mf.nhwwalk)
create_csv(root,mf.persons_nhb,"persons_nhb")
create_csv_gz(root,mf.persons_nhb,"persons_nhb")

mf.transit_nhb<-(mf.nhnwtr + mf.nhwtr)
create_csv(root,mf.transit_nhb,"transit_nhb")
create_csv_gz(root,mf.transit_nhb,"transit_nhb")

mf.bike_nhb<-(mf.nhnwbike + mf.nhwbike)
create_csv(root,mf.bike_nhb,"bike_nhb")
create_csv_gz(root,mf.bike_nhb,"bike_nhb")

mf.active_nhb<-(mf.nhnwbike + mf.nhnwwalk + mf.nhwbike + mf.nhwwalk)
create_csv(root,mf.active_nhb,"active_nhb")
create_csv_gz(root,mf.active_nhb,"active_nhb")

persons_all<-(mf.persons_hbw + mf.persons_hbnw + mf.persons_nhb + mf.hbcda + mf.hbcdp + mf.hbcpa + mf.hbcbike + mf.hbcprtr + mf.hbctr + mf.hbcwalk + mf.schveh + mf.schpas + mf.schbus + mf.scwabi + mf.schtr)
create_csv(root,persons_all,"persons_all")
create_csv_gz(root,persons_all,"persons_all")

transit_all<-(mf.transit_hbw + mf.transit_hbnw + mf.transit_nhb + mf.hbcprtr + mf.hbctr + mf.schtr)
create_csv(root,transit_all,"transit_all")
create_csv_gz(root,transit_all,"transit_all")

mf.schbike<- mf.scwabi*0.1875
bike_all<-(mf.bike_hbw + mf.bike_hbnw + mf.bike_nhb + mf.hbcbike + mf.schbike)
create_csv(root,bike_all,"bike_all")
create_csv_gz(root,bike_all,"bike_all")

active_all<-(mf.active_hbw + mf.active_hbnw + mf.active_nhb + mf.hbcbike + mf.hbcwalk + mf.scwabi)
create_csv(root,active_all,"active_all")
create_csv_gz(root,active_all,"active_all")