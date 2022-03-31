def plot_cycle_TS(self):

    plt.figure(1, figsize=(15, 5))
    plt.subplot(211)
    plt.plot([self.state1.v, self.state2.v, self.state3.v, self.state4.v, self.state1.v],
             [self.state1.p, self.state2.p, self.state3.p, self.state4.p, self.state1.p], 'o', c='r')
    # Plot from state 1 to 2
    plt.plot([self.state1.v, self.state2.v], [self.state1.p, self.state2.p], '-', c='y')
    # Plot from state 2 to 3
    plt.plot([self.state2.v, self.state3.v], [self.state2.p, self.state3.p], '-', c='g')
    # Plot from state 3 to 4
    plt.plot([self.state3.v, self.state4.v], [self.state3.p, self.state4.p], '-', c='b')
    # Plot from state 4 to 1
    plt.plot([self.state4.v, self.state1.v], [self.state4.p, self.state1.p], '-', c='k')
    plt.xlabel(r'P')
    plt.ylabel(r'V')
    plt.title(self.name)

    plt.subplot(212)
    plt.plot([self.state1.S, self.state2.S, self.state3.S, self.state4.S, self.state1.S],
             [self.state1.T, self.state2.T, self.state3.T, self.state4.T, self.state1.T], 'o', c='r')
    # Plot from state 1 to 2
    plt.plot([self.state1.S, self.state2.S], [self.state1.T, self.state2.T], '-', c='y')
    # Plot from state 2 to 3
    plt.plot([self.state2.S, self.state3.S], [self.state2.T, self.state3.T], '-', c='g')
    # Plot from state 3 to 4
    plt.plot([self.state3.S, self.state4.S], [self.state3.T, self.state4.T], '-', c='b')
    # Plot from state 4 to 1
    plt.plot([self.state4.S, self.state1.S], [self.state4.T, self.state1.T], '-', c='k')
    plt.xlabel(r'T')
    plt.ylabel(r'S')
    plt.title(self.name)

    plt.show()


def plot_summary(self):
    """
    This function creates the summary text for display on the rankine cycle plot
    """
    text = 'Summary:'
    text += '\nEfficiency: {:0.3f}%'.format(self.efficiency)
    text += '\nCompression Stroke Work: {:0.3f} kJ/kg'.format(self.comp_work)
    text += '\nPower Stroke Work: {:0.3f} kJ/kg'.format(self.power_work)
    text += '\nCycle Work: {:0.3f} kJ/kg'.format(self.work_cycle)
    text += '\nHeat Added: {:0.3f} kJ/kg'.format(self.heat_added)
    text += '\nHeat Rejected: {:0.3f} kJ/kg'.format(self.heat_rej)
    text += '\nNet Heat Added: {:0.3f} kJ/kg'.format(self.heat_cycle)
    return text
