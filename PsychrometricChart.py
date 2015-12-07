# This script will plot a psychrometric chart in IP units at a user specified ambient pressure.  Default, P_std=14.7 psi
#


from math import exp, pow, log
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def ref_linesIP(p_atm, T_db_range):

    phi_ref=[]
    wb_ref=[]
    db_ref=[]

    for i, phi in enumerate(range(10,101,10)):
        phi_ref.append([])
        for j, T_db in enumerate(T_db_range):
            p_ws=exp(-1.0440397E4/(T_db+459.67)-1.1294650E1-2.7022355E-2*(T_db+459.67)+1.2890360E-5*pow(T_db+459.67,2)-2.4780681E-9*pow(T_db+459.67,3)+6.5459673*log((T_db+459.67)))
            p_w=phi/100.0*p_ws
            phi_ref[i].append(0.621945*p_w/(p_atm-p_w))
            if phi==100 and round(T_db/10) == float(T_db)/10:
                T_wbo=(1093.0-0.556*T_db)*phi_ref[i][j]/0.24+T_db
                wb_ref.append(([T_db, T_wbo],[phi_ref[i][j],0]))
                db_ref.append(([T_db, T_db],[phi_ref[i][j],0]))
    return phi_ref, wb_ref, db_ref

def ref_linesSI(p_atm, T_db_range):

    return

def main():

    units=1#input("Units (1=IP,2=SI):")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if units==1:
        p_atm_input = 14.7#input ("Enter ambient pressure (psi, std_P = 14.7 psi):")
        T_db_range=range(32,111)
        phi_ref, wb_ref, db_ref=ref_linesIP(float(p_atm_input), T_db_range)
        plt.xlabel('Dry Bulb Temperature (F)')

        ax.annotate('100', xy=(84,.0281), color='b')
        ax.annotate('80', xy=(90.5,.0267), color='b')
        ax.annotate('60', xy=(96.5,.0240), color='b')
        ax.annotate('40', xy=(102.5,.0190), color='b')
        ax.annotate('20', xy=(107,.0107), color='b')

    if units==2:
        p_atm_input = 101.325#input ("Enter ambient pressure (kPa, std_P = 101.325 kPa):")
        T_db_range=range(0,51)
        phi_ref, wb_ref, db_ref=ref_linesSI(float(p_atm_input), T_db_range)
        plt.xlabel('Dry Bulb Temperature (C)')

    for i in range(0, len(phi_ref)):
        plt.plot(T_db_range,phi_ref[i], 'b')

    for i in range(0, len(wb_ref)):
        plt.plot(wb_ref[i][0],wb_ref[i][1],'b:')

    for i in range(0, len(db_ref)):
        plt.plot(db_ref[i][0],db_ref[i][1],'b:')

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.001))
    plt.xlim(min(T_db_range),max(T_db_range))
    plt.ylim(0,0.03)
    plt.ylabel('Humidity Ratio')
    plt.show()

if __name__=='__main__': main()