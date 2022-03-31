import numpy as np
import matplotlib.pyplot as plt
import math
from Gas import ideal_air

# this code is modified from Professor Smay's Rankine_work file

class otto():
    def __init__(self, v1=0.0005, T1=300, p1=101325, c_ratio=8, T3=2000, name='Otto Cycle'):
        """
        Constructor for air-standard Otto cycle.

        """
        self.v1 = v1
        self.T1 = T1
        self.p1 = p1
        self.T3 = T3
        self.c_ratio = c_ratio
        self.name = name
        self.efficiency = 0
        self.comp_work = 0
        self.power_work = 0
        self.heat_added = 0
        self.heat_rej = 0
        self.work_cycle = 0
        self.heat_cycle = 0
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.state4 = None

    def calc_efficiency(self):
        # calculate the 4 states
        # state 1: bottom-dead-center (BDC)
        self.state1 = ideal_air(T=self.T1, name='State 1')  # instantiate a gas object with conditions of state 1 using T1
        self.state1.p = self.p1
        self.state1.v = self.v1
        print("t1 =", self.state1.T)
        print("h1 =", self.state1.h)
        print("pr1 =", self.state1.pr)
        print("u1 =", self.state1.u)
        print("vr1 =", self.state1.vr)
        print("v1 =", self.state1.v)
        print("p1 =", self.state1.p)

        # state 2: top-dead-center (TDC), isentropically compressed from state 1
        vr2 = self.state1.vr/self.c_ratio  # first calculate vr2 to from compression ratio relationship
        self.state2 = ideal_air(vr=vr2, name='State 2')  # instantiate a gas object for state 2 using vr2
        self.state2.p = self.p1*self.state2.pr/self.state1.pr
        self.state2.v = self.v1/self.c_ratio
        print("t2 =", self.state2.T)
        print("h2 =", self.state2.h)
        print("pr2 =", self.state2.pr)
        print("u2 =", self.state2.u)
        print("vr2 =", self.state2.vr)
        print("v2 =", self.state2.v)
        print("p2 =", self.state2.p)

        # state 3: BDC, constant volume heat addition from state 2
        self.state3 = ideal_air(T=self.T3, name='State 3') # instantiate a gas object with for state 3 using T3
        # self.state3.p =
        self.state3.v = self.state2.v
        print("t3 =", self.state3.T)
        print("h3 =", self.state3.h)
        print("pr3 =", self.state3.pr)
        print("u3 =", self.state3.u)
        print("vr3 =", self.state3.vr)
        print("v3 =", self.state3.v)
        print("p3 =", self.state3.p)

        # state 4: TDC, isentropic expansion from state 3
        vr4 = self.state3.vr * self.c_ratio  # calculate vr4 from compression ratio relationship
        self.state4 = ideal_air(vr=vr4, name='State 4')
        self.state4.p = self.state3.p * self.state4.pr / self.state3.pr
        self.state4.v = self.state1.v
        print("t4 =", self.state4.T)
        print("h4 =", self.state4.h)
        print("pr4 =", self.state4.pr)
        print("u4 =", self.state4.u)
        print("vr4 =", self.state4.vr)
        print("v4 =", self.state4.v)
        print("p4 =", self.state4.p)

        self.comp_work = self.state2.u - self.state1.u  # calculate compression stroke work
        self.power_work = self.state3.u - self.state4.u  # calculate power stroke work
        self.heat_added = self.state3.u - self.state2.u  # calculate heat added
        self.heat_rej = self.state4.u - self.state1.u  # calculate heat rejected
        self.work_cycle = self.power_work - self.comp_work  # calculate work of the cycle
        self.heat_cycle = self.heat_added - self.heat_rej  # calculate net heat added
        self.efficiency = self.work_cycle/self.heat_added * 100  # calculate cycle efficiency
        return self.efficiency


    def print_summary(self):
        self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tCompression Stroke Work: {:0.3f} kJ/kg'.format(self.comp_work))
        print('\tPower Stroke Work: {:0.3f} kJ/kg'.format(self.power_work))
        print('\tCycle Work: {:0.3f} kJ/kg'.format(self.work_cycle))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        print('\tHeat Rejected: {:0.3f} kJ/kg'.format(self.heat_rej))
        print('\tNet Heat Added: {:0.3f} kJ/kg'.format(self.heat_cycle))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()


    # def plot_cycle_TS(self):
    #     # 1) Plot the saturated state lines
    #     # create arrays containing saturated fluid temperatures (blue), and saturated vapor (red)
    #     p_plot = np.logspace(0, math.log(22120, 9), 500)  # pressure data to plot from
    #     s = steam(1)
    #     t_fs = []
    #     s_fs = []
    #     t_gs = []
    #     s_gs = []
    #     for p in p_plot:  # use new_calc function in steam to not have to recreate the object to return both T and s
    #         s.new_calc(p, x=0)
    #         t_fs.append((s.T))
    #         s_fs.append((s.s))
    #         s.new_calc(p, x=1)
    #         t_gs.append((s.T))
    #         s_gs.append((s.s))
    #
    #     # Build the plot
    #     plt.plot(s_fs, t_fs, color='blue')
    #     plt.plot(s_gs, t_gs, color='red')
    #     plt.xlim(0, 9)
    #     plt.ylim(0, 550)
    #     plt.ylabel('T 'r'$(^{\circ}C)$')
    #     plt.xlabel('S 'r'$(\frac{kJ}{kg\cdot K})$')
    #     plt.title('Rankine Cycle - Superheated at turbine inlet')  # this will need modified with an if statement
    #
    #     # 2) Upper bounds for shading
    #     self.state4a = steam(self.state4.p, x=0)  # instantiate a new state at p = state 4 and x = 0
    #     # Section 1 (3 to 4a)
    #     s_fill_1 = np.linspace(self.state3.s, self.state4a.s, 50)  # lower bound between state 3 and 4a (left)
    #     t_fill_1 = np.interp(s_fill_1, [self.state3.s, self.state4a.s], [self.state3.T, self.state4a.T])  # interpolating linear line between 3 and 4a
    #     # Section 2 (4a to 1)
    #     s_fill_2 = np.linspace(self.state4a.s, self.state1.s, 50)  # lower bound between state 4a and 2 (right)
    #     t_fill_2 = [steam(self.state4.p, s=i).T for i in s_fill_2]
    #     # Section 3 (1 to 2)
    #     s_fill_3 = np.linspace(self.state1.s, self.state2.s, 25)
    #     t_fill_3 = np.interp(s_fill_3, [self.state1.s, self.state2.s], [self.state1.T, self.state2.T])
    #     # stitch the three sections together
    #     t_fill_high = np.concatenate((t_fill_1, t_fill_2, t_fill_3))
    #     s_fill = np.concatenate((s_fill_1, s_fill_2, s_fill_3))
    #
    #     # 3) Lower bound for shading
    #     t_fill_low = [self.state2.T for i in s_fill]
    #
    #     # 4) Add shading
    #     plt.fill_between(s_fill, t_fill_high, t_fill_low, color='grey', alpha=0.3, ec='green')
    #
    #     # 5) Add summary text using defined function plot_summary()
    #     text_x = 0.65
    #     text_y = 350
    #     plt.text(text_x, text_y, rankine.plot_summary(self), fontsize='small')  # summary description
    #
    #     # 6) Add state point markers
    #     plt.plot(self.state1.s, self.state1.T, marker='o', markerfacecolor='white', markeredgecolor='k')
    #     plt.plot(self.state2.s, self.state2.T, marker='o', markerfacecolor='white', markeredgecolor='k')
    #     plt.plot(self.state3.s, self.state3.T, marker='o', markerfacecolor='white', markeredgecolor='k')
    #
    #     plt.show()
    #
    #
    # def plot_summary(self):
    #     """
    #     This function creates the summary text for display on the rankine cycle plot
    #     """
    #     text = 'Summary:'
    #     text += '\n$\eta:$' + '{:0.1f}%'.format(self.efficiency)
    #     text += '\n$\eta_{turbine}:$' + '{:0.2f}'.format(self.turb_eff)
    #     text += '\n$W_{turbine}:$' + '{:0.1f} kJ/kg'.format(self.turbine_work)
    #     text += '\n$W_{pump}:$' + '{:0.1f} kJ/kg'.format(self.pump_work)
    #     text += '\n$Q_{boiler}:$' + '{:0.1f} kJ/kg'.format(self.heat_added)
    #     return text


def main():
    # Input unit conversion from Imperial to SI
    v1 = 0.02 * 0.0283168  # m^3 converted from ft^3
    T1 = 540 * 5/9  # deg K converted from deg R
    p1 = 1 * 101325  # pa converted from atm
    T3 = 3600 * 5/9  # deg K converted from deg R

    otto1 = otto(v1=v1, T1=T1, p1=p1, c_ratio=8, T3=T3, name='Otto Cycle')  # instantiate an otto object to test it
    otto1.print_summary()

if __name__=="__main__":
    main()