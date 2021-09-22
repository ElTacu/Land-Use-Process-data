## Assumes run from ./model directory
## Requires mf.persontrips.dat file produced by forecast.sh -r flag
args = commandArgs(trailingOnly=TRUE)
root = args[1]

source(paste(root,"j.model_setup.R", sep='/'))
load_ensemble("V:/tbm/joan/2010/iter1/ens/ens.gy.csv","gy")
load(paste(project.dir, 'model/mf.persontrips.dat', sep='/'))

mf.tdist = readEmme(bank,"mftdist")

tripLengths = mf.tdist * mf.persontrips

p_trips = file.path(root,"model\\reports\\auto_files\\person_trips.csv")
tt_length = file.path(root,"model\\reports\\auto_files\\total_trip_lengths.csv")

outfile = file(p_trips,"w")
outfi = file(tt_length,"w")

district_squeeze_csv(mf.persontrips,ensemble.gy,"person_trips",outfile)
district_squeeze_csv(tripLengths,ensemble.gy,"total_trip_lengths",outfi)


close(outfile)
close(outfi)
