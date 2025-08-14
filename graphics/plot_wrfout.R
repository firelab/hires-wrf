library(raster)
library(plotKML)
library(ncdf4)
library(raster)
library(rgdal)

nc <-nc_open("wrfout.nc")
v38 <- nc$var[[38]] #var 38 is T2 (v38$name)
varsize <- v38$varsize
ndims <-v38$ndims
nx<-varsize[1]
ny<-varsize[2]
#nlayers<-varsize[3]
nt <- varsize[ndims] #time is always last dimension

# Initialize start and count to read one layer and one timestep of the variable.
# start=(1,1,1,i) to read timestep i
# count=(nx,ny,nz,1) to read 1 tstep
for(i in 1:nt){
    print(i)
    assign(paste0("data", i),  ncvar_get( nc, v38, start=c(1,1,i), count=c(nx,ny,1) ))
    assign(paste0("r", i), raster(get(paste0("data", i))))
}

r<-brick(get(paste0("r1")), get(paste0("r2")), get(paste0("r3")), get(paste0("r4")), 
         get(paste0("r5")), get(paste0("r6")), get(paste0("r7")))
r<-raster::t(r) # rows,cols flipped when coerced from netcdf to raster, so transpose the matrix
r <- flip(r, direction='y') #then flip it about the y-axis

#now set CRS
#note this geotransform (extent) is only valid for cell-centered variables
#the extent needs to be modified for x/y-staggered variables (such as u, v)
dx <- as.numeric(ncatt_get( nc, 0, "DX" ))[2] #0 indicates global attribute
dy <- as.numeric(ncatt_get( nc, 0, "DY" ))[2]

lon0 <- gettextf( ncatt_get( nc, 0, "STAND_LON" ) )[2]
lat0 <- gettextf( ncatt_get( nc, 0, "MOAD_CEN_LAT" ) )[2]
lat1 <- gettextf( ncatt_get( nc, 0, "TRUELAT1" ) )[2]
lat2 <- gettextf( ncatt_get( nc, 0, "TRUELAT2" ) )[2]
prj <- paste (c( "+proj=lcc +lat_1=",lat1," +lat_2=",lat2," +lat_0=",lat0," +lon_0=",lon0," +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs" ), collapse = "" )

#convert centerLon, centerLat to spatialPoints
centerLon <- gettextf( ncatt_get( nc, 0, "CEN_LON" ) )[2]
centerLat <- gettextf( ncatt_get( nc, 0, "CEN_LAT" ) )[2]
lonlatCenter<-SpatialPoints( cbind( as.numeric(centerLon), as.numeric(centerLat) ), proj4string=CRS("+proj=longlat +ellps=WGS84"))
prjCenter <- spTransform( lonlatCenter, CRS(prj) ) #transform from latlon to WRF prj space

prjCenterX<-coordinates( prjCenter )[1]
prjCenterY<-coordinates( prjCenter )[2]
nrows <- nrow(r) 
ncols <- ncol(r)

xmin <- prjCenterX - ncols/2*dx
xmax <- prjCenterX + ncols/2*dx
ymin <- prjCenterY - nrows/2*dy
ymax <- prjCenterY + nrows/2*dy

#make a new skeleton raster brick
x <- brick(ncol=nx, nrow=ny, xmn=xmin, xmx=xmax, ymn=ymin, ymx=ymax)
proj4string(x) <- CRS(prj)
values(x) <- values(r) #this is the final projected image

crs<-CRS("+proj=longlat +datum=WGS84")
x_lonlat<-projectRaster(x, crs=crs)

#convert from K to F
x_lonlat <- x_lonlat * 9/5 - 459.7

#better KML with legend
kml(x_lonlat, alpha=0.5)

nc_close(nc)
