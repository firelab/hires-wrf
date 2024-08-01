#!/usr/bin/env python

import subprocess
import datetime

RUN = '/home/natalie/src/wrf/WRF/run/'

#=============================================================================
#        Edit namelist.input
#=============================================================================
namelistFile = RUN + "namelist.input"
namelist = open(namelistFile, 'w')

start_year = datetime.date.today().year
start_month = datetime.date.today().month
start_day = datetime.date.today().day

end_year = (datetime.date.today() + datetime.timedelta(days=1)).year
end_month = (datetime.date.today() + datetime.timedelta(days=1)).month
end_day = (datetime.date.today() + datetime.timedelta(days=1)).day

namelist.write(" &time_control\n")
namelist.write(" run_days                     = 0\n")
namelist.write(" run_hours                    = 0\n")
namelist.write(" run_minutes                  = 0\n")
namelist.write(" run_seconds                  = 0\n")
namelist.write(" start_year                   = %s\n" % start_year)
namelist.write(" start_month                  = %s\n" % start_month)
namelist.write(" start_day                    = %s\n" % start_day)
namelist.write(" start_hour                   = 18\n")
namelist.write(" start_minute                 = 0\n")
namelist.write(" start_second                 = 0\n")
namelist.write(" end_year                     = %s\n" % end_year)
namelist.write(" end_month                    = %s\n" % end_month)
namelist.write(" end_day                      = %s\n" % end_day)
namelist.write(" end_hour                     = 05\n")
namelist.write(" end_minute                   = 0\n")
namelist.write(" end_second                   = 0\n")
namelist.write(" interval_seconds             = 3600\n")
namelist.write(" input_from_file              = .true.\n")
namelist.write(" history_interval             = 60\n")
namelist.write(" frames_per_outfile           = 1000\n")
namelist.write(" restart                      = .false.\n")
namelist.write(" restart_interval             = 5000\n")
namelist.write(" io_form_history              = 2\n")
namelist.write(" io_form_restart              = 2\n")
namelist.write(" io_form_input                = 2\n")
namelist.write(" io_form_boundary             = 2\n")
namelist.write(" debug_level                  = 0\n")
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &domains\n")
namelist.write(" time_step                    = 3\n")
namelist.write(" time_step_fract_num          = 0\n") 
namelist.write(" time_step_fract_den          = 1\n") 
namelist.write(" max_dom                      = 1\n") 
namelist.write(" e_we                         = 100\n") 
namelist.write(" e_sn                         = 100\n") 
namelist.write(" e_vert                       = 42\n") 
#namelist.write(" p_top_requested              = 5000\n") 
namelist.write(" eta_levels                   = 1.000,.9976,.995,.9929,.990,.9875,.985,.9825,.980,\n"
                                                ".975,.970,.965,.960,.955,.950,.940,.930,.920,.910,.900,\n"
                                                ".880,.860,.840,.820,.800,.770,.740,.700,.650,.600,.550,\n"
                                                ".500,.450,.400,.350,.300,.250,.200,.150,.100,.050,0.000\n")
namelist.write(" num_metgrid_levels           = 41\n") 
namelist.write(" num_metgrid_soil_levels      = 9\n") 
namelist.write(" dx                           = 1000\n") 
namelist.write(" dy                           = 1000\n") 
namelist.write(" grid_id                      = 1\n") 
namelist.write(" parent_id                    = 0\n") 
namelist.write(" i_parent_start               = 1\n") 
namelist.write(" j_parent_start               = 1\n") 
namelist.write(" parent_grid_ratio            = 1\n") 
namelist.write(" parent_time_step_ratio       = 1\n") 
namelist.write(" feedback                     = 0\n") 
namelist.write(" smooth_option                = 0\n") 
namelist.write(" sfcp_to_sfcp                 = .true.\n") 
namelist.write(" smooth_cg_topo               = .true.\n") 
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &physics\n")
namelist.write(" mp_physics                   = 3\n") 
namelist.write(" ra_lw_physics                = 1\n") 
namelist.write(" ra_sw_physics                = 1\n") 
namelist.write(" radt                         = 12\n") 
namelist.write(" sf_sfclay_physics            = 1\n") 
namelist.write(" sf_surface_physics           = 1\n") 
namelist.write(" bl_pbl_physics               = 1\n") 
namelist.write(" bldt                         = 0\n") 
namelist.write(" cu_physics                   = 0\n") 
namelist.write(" cudt                         = 0\n") 
namelist.write(" isfflx                       = 1\n") 
namelist.write(" ifsnow                       = 1\n") 
namelist.write(" icloud                       = 1\n") 
namelist.write(" surface_input_source         = 3\n") 
namelist.write(" num_soil_layers              = 4\n") 
namelist.write(" num_land_cat                 = 21\n") 
namelist.write(" sf_urban_physics             = 0\n") 
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &fdda\n")
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &dynamics\n")
namelist.write(" w_damping                    = 1\n") 
namelist.write(" diff_opt                     = 1\n") 
namelist.write(" km_opt                       = 4\n") 
namelist.write(" diff_6th_opt                 = 0\n") 
namelist.write(" diff_6th_factor              = 0.12\n") 
namelist.write(" base_temp                    = 290.\n") 
namelist.write(" damp_opt                     = 3\n") 
namelist.write(" zdamp                        = 5000.\n") 
namelist.write(" dampcoef                     = 0.2\n") 
namelist.write(" khdif                        = 0\n") 
namelist.write(" kvdif                        = 0\n") 
namelist.write(" non_hydrostatic              = .true.\n") 
namelist.write(" moist_adv_opt                = 1\n") 
namelist.write(" scalar_adv_opt               = 1\n") 
namelist.write(" epssm                        = 0.5\n") 
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &bdy_control\n")
namelist.write(" spec_bdy_width               = 5\n") 
namelist.write(" spec_zone                    = 1\n") 
namelist.write(" relax_zone                   = 4\n") 
namelist.write(" specified                    = .true.\n") 
namelist.write(" nested                       = .false.\n") 
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &grib2\n")
namelist.write(" /\n")
namelist.write("\n")

namelist.write(" &namelist_quilt\n")
namelist.write(" nio_tasks_per_group          = 0\n") 
namelist.write(" nio_groups                   = 1\n") 
namelist.write(" /\n")

namelist.close()

#=============================================================================
#        Run real.exe
#=============================================================================
p = subprocess.Popen(["ln -sf ../../WPS/met_em* ."], cwd = RUN, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

p = subprocess.Popen(["mpirun -np 1 ./real.exe"], cwd = RUN, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

