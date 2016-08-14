
import numpy as np

# Cosmological Constants
c = 299792458
H0 = 70 
om_m = 0.3
om_k = 0.0
om_A = 0.7

def f(z, om_m, om_k, om_A):
    '''
    Defines the function to be integrated.

    Arguments:
    z - redshift (variable)
    om_m - omega matter
    om_k - omega curvature
    om_A - omega lambda

    The return value is a tuple, with the first element holding the estimated
    value of the integral and the second element holding an upper bound on the
    error.
    '''
    return (om_m * ((1 + z)**3) + om_k * ((1 + z)**2) + om_A)**(-0.5)

def integrate(startx, endx, steps):
    '''
    Performs the integration of the function
    '''
    width = (float(endx) - float(startx))/steps
    runningsum = 0
    for i in range(steps):
        height = f(startx + i*width, om_m, om_k, om_A)
        area = height*width
        runningsum +=area
    return runningsum

def recession_velocity(redshift):
    return((c)*(integrate(0,redshift,100000)))
def gals_in_pair(id_host,z_host,id_comp,z_comp,delta_z,mass_ratio,mass_host,mass_comp,zhostl68,zhostu68,zcompl68,zcompu68,z_criteria,counted_id1,counted_id2,field):
    def redshift_proximity(host,comp,host_upper,host_lower,comp_upper,comp_lower,criteria):
        satisfy_redshift_proximity=False
        if criteria == 'Man':
            if host<=comp and 0<= host_upper-comp_lower:
                satisfy_redshift_proximity=True
            elif host>comp and 0<= comp_upper-host_lower:
                satisfy_redshift_proximity=True
        if criteria == 'B09':
            if (abs(host-comp))**2<=((abs(host_upper-host_lower)/2)**2 + (abs(comp_upper-comp_lower)/2)**2):
                satisfy_redshift_proximity = True
        if criteria == 'Hybrid':
            if host_upper == host_lower and comp_upper == comp_lower:
                reces_vel_host=recession_velocity(host)/10**3
                reces_vel_comp=recession_velocity(comp)/10**3
                if abs(reces_vel_host-reces_vel_comp)<=500:
                    satisfy_redshift_proximity = True
                elif abs(reces_vel_host-reces_vel_comp)>500:
                    satisfy_redshift_proximity = False
            elif host_upper!=host_lower and comp_upper == comp_lower:
                if abs(host-comp)<= abs(host_upper - host_lower)/2.0:
                    satisfy_redshift_proximity = True
                elif abs(host-comp)> abs(host_upper - host_lower)/2.0:
                    satisfy_redshift_proximity = False
            elif host_upper==host_lower and comp_upper != comp_lower:
                if abs(host-comp)<= abs(comp_upper - comp_lower)/2.0:
                    satisfy_redshift_proximity = True
                elif abs(host-comp)> abs(comp_upper - comp_lower)/2.0:
                    satisfy_redshift_proximity = False
            elif host_upper!=host_lower and comp_upper!=comp_lower:
                if (abs(host-comp))**2<=((abs(host_upper-host_lower)/2)**2 + (abs(comp_upper-comp_lower)/2)**2):
                    satisfy_redshift_proximity = True
                elif (abs(host-comp))**2>((abs(host_upper-host_lower)/2)**2 + (abs(comp_upper-comp_lower)/2)**2):
                    satisfy_redshift_proximity = False
        return(satisfy_redshift_proximity)
                    
                
    def is_massive(mass):
        if mass >=2E10:
            return(True)
        if mass<2E10:
            return(False)
    def is_major(mass_ratio):
        if mass_ratio<=4:
            return(True)
        if mass_ratio>4:
            return(False)
    def already_counted(gal_id,counted_id):
        if gal_id in counted_id:
            return(True)
        else :
            return(False)
    def which_redshift_bin_host(redshift):
        if redshift >=0.5 and redshift <=1.0:
            return(1)
        if redshift >1.0 and redshift <=1.5:
            return(2)
        if redshift >1.5 and redshift <=2.0:
            return(3)
        if redshift >2.0 and redshift <=2.5:
            return(4)
        if redshift >2.5 and redshift <=3.0:
            return(5)
    def which_redshift_bin_comp(redshift):
        if redshift >=0.0 and redshift <=1.0:
            return(1)
        if redshift >1.0 and redshift <=1.5:
            return(2)
        if redshift >1.5 and redshift <=2.0:
            return(3)
        if redshift >2.0 and redshift <=2.5:
            return(4)
        if redshift >2.5:
            return(5)
    
    def is_redshift_a_disaster(zlow,zup,redshift,how_strict):
        Bad_flag=0
        if zlow<=0 or abs(zup-zlow)/2.0 >=how_strict*(1+redshift):
            Bad_flag=1
        return(Bad_flag)        
    satisfy_redshift_proximity = redshift_proximity(z_host,z_comp,zhostu68,zhostl68,zcompu68,zcompl68,z_criteria)
    is_major=is_major(mass_ratio)
    is_host_massive=is_massive(mass_host)
    is_comp_massive=is_massive(mass_comp)
    which_redshift_host=which_redshift_bin_host(z_host)
    which_redshift_comp=which_redshift_bin_comp(z_comp)
    is_host_already_counted = already_counted(id_host,counted_id1)
    is_comp_already_counted = already_counted(id_comp,counted_id2)
    if field=='UDS':
        is_host_redshift_a_disaster=is_redshift_a_disaster(zhostl68,zhostu68,z_host,0.035)
        is_comp_redshift_a_disaster=is_redshift_a_disaster(zcompl68,zcompu68,z_comp,0.035)
    elif field=='GDS':
        is_host_redshift_a_disaster=is_redshift_a_disaster(zhostl68,zhostu68,z_host,0.041)
        is_comp_redshift_a_disaster=is_redshift_a_disaster(zcompl68,zcompu68,z_comp,0.041)
    elif field=='CMS':
        is_host_redshift_a_disaster=is_redshift_a_disaster(zhostl68,zhostu68,z_host,0.037)
        is_comp_redshift_a_disaster=is_redshift_a_disaster(zcompl68,zcompu68,z_comp,0.037)
    elif field=='EGS':
        is_host_redshift_a_disaster=is_redshift_a_disaster(zhostl68,zhostu68,z_host,0.042)
        is_comp_redshift_a_disaster=is_redshift_a_disaster(zcompl68,zcompu68,z_comp,0.042)
    elif field=='GDN':
        is_host_redshift_a_disaster=is_redshift_a_disaster(zhostl68,zhostu68,z_host,0.048)
        is_comp_redshift_a_disaster=is_redshift_a_disaster(zcompl68,zcompu68,z_comp,0.048)

    return([is_host_massive,is_comp_massive,is_major,satisfy_redshift_proximity,which_redshift_host,which_redshift_comp,is_host_already_counted,is_comp_already_counted,id_host,id_comp,is_host_redshift_a_disaster,is_comp_redshift_a_disaster])
            
            
            
    