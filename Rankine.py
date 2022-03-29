from Steam import steam
import numpy as np
import matplotlib.pyplot as plt
import math

# this code is modified from Professor Smay's Rankine_work file

class rankine():
    def __init__(self, p_low=8, p_high=8000, t_high=None, turb_eff=1.00, name='Rankine Cycle'):
        '''
        Constructor for rankine power cycle.  If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param name: a convenient name
        '''
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.turb_eff = turb_eff
        self.name = name
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0
        self.state1 = None
        self.state2 = None
        self.state2s = None
        self.state3 = None
        self.state4 = None
        self.state4a = None

    def calc_efficiency(self):
        # calculate the 4 states
        # state 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if(self.t_high == None):
            self.state1 = steam(self.p_high, x=1.0, name='Turbine Inlet')  # instantiate a steam object with conditions of state 1 as saturated steam, named 'Turbine Inlet'
        else:
            self.state1 = steam(self.p_high,T=self.t_high,name='Turbine Inlet')  # instantiate a steam object with conditions of state 1 at t_high, named 'Turbine Inlet'
        # state 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.state2s = steam(self.p_low, s=self.state1.s, name="Turbine Exit, Ideal")  # instantiate a steam object with conditions of state 2s, named 'Turbine Exit, Ideal'
        self.state2 = steam(self.p_low, h=(self.state1.h - self.turb_eff*(self.state1.h - self.state2s.h)), name="Turbine exit, Actual")  # instantiate a steam object with conditions of state 2, named 'Turbine Exit, Actual'
        # state 3: pump inlet (p_low, x=0) saturated liquid
        self.state3 = steam(self.p_low,x=0, name='Pump Inlet') # instantiate a steam object with conditions of state 3 as saturated liquid, named 'Pump Inlet'
        # state 4: pump exit (p_high,s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.state4 = steam(self.p_high,s=self.state3.s, name='Pump Exit')
        self.state4.h = self.state3.h+self.state3.v*(self.p_high-self.p_low)

        self.turbine_work= self.state1.h - self.state2.h # calculate turbine work
        self.pump_work= self.state4.h - self.state3.h # calculate pump work
        self.heat_added= self.state1.h - self.state4.h # calculate heat added
        self.efficiency=100.0*(self.turbine_work - self.pump_work)/self.heat_added
        return self.efficiency

    def print_summary(self):
        if self.efficiency==None:
            self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()


    def plot_cycle_TS(self):
        # 1) Plot the saturated state lines
        # create arrays containing saturated fluid temperatures (blue), and saturated vapor (red)
        p_plot = np.logspace(0, math.log(22120, 9), 500)  # pressure data to plot from
        s = steam(1)
        t_fs = []
        s_fs = []
        t_gs = []
        s_gs = []
        for p in p_plot:  # use new_calc function in steam to not have to recreate the object to return both T and s
            s.new_calc(p, x=0)
            t_fs.append((s.T))
            s_fs.append((s.s))
            s.new_calc(p, x=1)
            t_gs.append((s.T))
            s_gs.append((s.s))

        # Build the plot
        plt.plot(s_fs, t_fs, color='blue')
        plt.plot(s_gs, t_gs, color='red')
        plt.xlim(0, 9)
        plt.ylim(0, 550)
        plt.ylabel('T 'r'$(^{\circ}C)$')
        plt.xlabel('S 'r'$(\frac{kJ}{kg\cdot K})$')
        plt.title('Rankine Cycle - Superheated at turbine inlet')  # this will need modified with an if statement

        # 2) Upper bounds for shading
        self.state4a = steam(self.state4.p, x=0)  # instantiate a new state at p = state 4 and x = 0
        # Section 1 (3 to 4a)
        s_fill_1 = np.linspace(self.state3.s, self.state4a.s, 50)  # lower bound between state 3 and 4a (left)
        t_fill_1 = np.interp(s_fill_1, [self.state3.s, self.state4a.s], [self.state3.T, self.state4a.T])  # interpolating linear line between 3 and 4a
        # Section 2 (4a to 1)
        s_fill_2 = np.linspace(self.state4a.s, self.state1.s, 50)  # lower bound between state 4a and 2 (right)
        t_fill_2 = [steam(self.state4.p, s=i).T for i in s_fill_2]
        # Section 3 (1 to 2)
        s_fill_3 = np.linspace(self.state1.s, self.state2.s, 25)
        t_fill_3 = np.interp(s_fill_3, [self.state1.s, self.state2.s], [self.state1.T, self.state2.T])
        # stitch the three sections together
        t_fill_high = np.concatenate((t_fill_1, t_fill_2, t_fill_3))
        s_fill = np.concatenate((s_fill_1, s_fill_2, s_fill_3))

        # 3) Lower bound for shading
        t_fill_low = [self.state2.T for i in s_fill]

        # 4) Add shading
        plt.fill_between(s_fill, t_fill_high, t_fill_low, color='grey', alpha=0.3, ec='green')

        # 5) Add summary text using defined function plot_summary()
        text_x = 0.65
        text_y = 350
        plt.text(text_x, text_y, rankine.plot_summary(self), fontsize='small')  # summary description

        # 6) Add state point markers
        plt.plot(self.state1.s, self.state1.T, marker='o', markerfacecolor='white', markeredgecolor='k')
        plt.plot(self.state2.s, self.state2.T, marker='o', markerfacecolor='white', markeredgecolor='k')
        plt.plot(self.state3.s, self.state3.T, marker='o', markerfacecolor='white', markeredgecolor='k')

        plt.show()


    def plot_summary(self):
        """
        This function creates the summary text for display on the rankine cycle plot
        """
        text = 'Summary:'
        text += '\n$\eta:$' + '{:0.1f}%'.format(self.efficiency)
        text += '\n$\eta_{turbine}:$' + '{:0.2f}'.format(self.turb_eff)
        text += '\n$W_{turbine}:$' + '{:0.1f} kJ/kg'.format(self.turbine_work)
        text += '\n$W_{pump}:$' + '{:0.1f} kJ/kg'.format(self.pump_work)
        text += '\n$Q_{boiler}:$' + '{:0.1f} kJ/kg'.format(self.heat_added)
        return text


def main():
    rankine1= rankine(8,8000, t_high=500, turb_eff=0.95, name='Rankine Cycle - Superheated at turbine inlet') #instantiate a rankine object to test it.
    #t_high is specified
    #if t_high were not specified, then x_high = 1 is assumed
    eff=rankine1.calc_efficiency()
    print(eff)
    rankine1.print_summary()
    rankine1.plot_cycle_TS()

if __name__=="__main__":
    main()