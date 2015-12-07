# PsychrometricChart.py
#
# This python script plots a psychrometric chart in IP units at a user specified ambient pressure (default is 14.7 psi). 
# The chart includes reference lines for relative humidity, dry bulb temp, and wet bulb temp.
#

from math import exp, pow, log
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def ref_linesIP(p_atm, T_db_range):

    phi_ref=[]
    wb_ref=[]
    db_ref=[]
    W=[]

    # Create relative humidity reference lines from 10-100%, in increments of 10%.
    for i, phi in enumerate(range(10,101,10)):
        phi_ref.append([])
        for j, T_db in enumerate(T_db_range):
            # Calculate the saturation pressure, p_ws, over liquid water (2009 ASHRAE Fundamentals, eqn 6)
            p_ws=exp(-1.0440397E4/(T_db+459.67)-1.1294650E1-2.7022355E-2*(T_db+459.67)+1.2890360E-5*pow(T_db+459.67,2)-2.4780681E-9*pow(T_db+459.67,3)+6.5459673*log((T_db+459.67)))
            # Calculate water vapor pressure, p_w, at phi and p_ws(T_db)
            p_w=phi/100.0*p_ws
            # Calculate humidity ratio at p_w(phi,T_db)
            W=0.621945*p_w/(p_atm-p_w)
            phi_ref[i].append(W)
            # At saturation, find db and wb reference line endpoints for plotting.
            if phi==100 and round(T_db/10) == float(T_db)/10: #decrease divisor for smaller plot graduations
                # Find T_wb at W=0. (2009 ASHRAE Fundamentals, eqn 35)
                T_wbo=(1093.0-0.556*T_db)*phi_ref[i][j]/0.24+T_db
                wb_ref.append(([T_db, T_wbo],[phi_ref[i][j],0]))
                db_ref.append(([T_db, T_db],[phi_ref[i][j],0]))
    return phi_ref, wb_ref, db_ref

def ref_linesSI(p_atm, T_db_range):

    return

# Find humidity ratio, W(T_db,phi,p)
def humidity_ratio(p,T_db,phi):
    p_ws=exp(-1.0440397E4/(T_db+459.67)-1.1294650E1-2.7022355E-2*(T_db+459.67)+1.2890360E-5*pow(T_db+459.67,2)-2.4780681E-9*pow(T_db+459.67,3)+6.5459673*log((T_db+459.67)))
    p_w=phi/100.0*p_ws
    W=0.621945*p_w/(p-p_w)

    return W

def main():

    units='IP' #input("Units (IP,SI):")
    set_point='y' #input("Include setpoint (y/n)?:")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if units=='IP':
        p_atm_input = 14.7  #input ("Enter ambient pressure (psi, std_P = 14.7 psi):")

        if set_point=='y':
            st_point_Tdb = 75   #input ("Enter dry bulb temperature of state point (F):")
            st_point_rh = 45    #input ("Enter relative humidity (%):")
            st_point_W=humidity_ratio(p_atm_input,st_point_Tdb,st_point_rh)

        T_db_range=range(32,111)
        phi_ref, wb_ref, db_ref=ref_linesIP(float(p_atm_input), T_db_range)
        plt.xlabel('Dry Bulb Temperature (F)')
        plt.ylabel('Humidity Ratio (lb_w/lb_da)')

    if units=='SI':
        p_atm_input = 101.325#input ("Enter ambient pressure (kPa, std_P = 101.325 kPa):")

        if set_point=='y':
            st_point_Tdb = 25   #input ("Enter dry bulb temperature of state point (C):")
            st_point_rh = 45    #input ("Enter relative humidity (%):")
            st_point_W=humidity_ratio(p_atm_input,st_point_Tdb,st_point_rh)

        T_db_range=range(0,51)
        phi_ref, wb_ref, db_ref=ref_linesSI(float(p_atm_input), T_db_range)
        plt.xlabel('Dry Bulb Temperature (C)')
        plt.ylabel('Humidity Ratio (kg_w/kg_da)')

    for i in range(0, len(phi_ref)):
        plt.plot(T_db_range,phi_ref[i], 'b')

    for i in range(0, len(wb_ref)):
        plt.plot(wb_ref[i][0],wb_ref[i][1],'b:')
        #ax.annotate(wb_ref[i][0][0], xy=(wb_ref[i][0][0]-0.5, wb_ref[i][1][0]))

    for i in range(0, len(db_ref)):
        plt.plot(db_ref[i][0],db_ref[i][1],'b:')

    # Plot a state point
    if set_point=='y':
        plt.scatter(st_point_Tdb,st_point_W,color='r')

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.001))
    plt.xlim(min(T_db_range),max(T_db_range))
    plt.ylim(0,0.03)
    plt.show()

if __name__=='__main__': main()