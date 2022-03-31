import numpy as np
from scipy.interpolate import griddata


class ideal_air():
    """
    The ideal air class is used to find air properties where the air is modeled as an ideal gas which is
    the working fluid for the  piston-cylinder arrangement.
    """

    def __init__(self, T=None, h=None, pr=None, u=None, vr=None, name=None):
        """
        :param T: temperature in degrees K
        :param h: enthalpy in kJ/kg
        :param pr: relative pressure
        :param u: internal energy in kJ/kg
        :param vr: relative energy
        :param name: a convenient identifier
        """
        # assign arguments to class properties
        self.T = T  # Temperature - degrees K
        self.h = h  # Enthalpy - kJ/kg
        self.pr = pr  # Relative Pressure
        self.u = u  # Internal Energy - kJ/kg
        self.vr = vr  # Specific Volume
        self.p = 0
        self.v = 0
        self.s = 0
        self.name = name  # a useful identifier
        if T == None and h == None and pr == None and u == None and vr == None:
            return
        else:
            self.calc()

    def calc(self):
        """
         The air standard Otto cycle is an ideal cycle that approximates a spark-ignition internal
         combustion engine. The air properties table will be used to help interpolate the different
         properties for each process that will be used in the Otto module.
        :return: nothing returned, just set the properties
        """
        # 1. Determine known properties
        # 2. find all unknown air properties by interpolation

        # read in the air property data from files
        Ta, ha, pra, ua, vra = np.loadtxt('ideal_air_table_SI.txt', skiprows=1, unpack=True)

        # get air properties
        if self.T is not None:
            self.h = float(griddata(Ta, ha, self.T))
            self.pr = float(griddata(Ta, pra, self.T))
            self.u = float(griddata(Ta, ua, self.T))
            self.vr = float(griddata(Ta, vra, self.T))
            return
        if self.h is not None:
            self.T = float(griddata(ha, Ta, self.h))
            self.pr = float(griddata(ha, pra, self.h))
            self.u = float(griddata(ha, ua, self.h))
            self.vr = float(griddata(ha, vra, self.h))
            return
        if self.pr is not None:
            self.T = float(griddata(pra, Ta, self.pr))
            self.h = float(griddata(pra, ha, self.pr))
            self.u = float(griddata(pra, ua, self.pr))
            self.vr = float(griddata(pra, vra, self.pr))
            return
        if self.u is not None:
            self.T = float(griddata(ua, Ta, self.u))
            self.h = float(griddata(ua, ha, self.u))
            self.pr = float(griddata(ua, pra, self.u))
            self.vr = float(griddata(ua, vra, self.u))
            return
        if self.vr is not None:
            self.T = float(griddata(vra, Ta, self.vr))
            self.h = float(griddata(vra, ha, self.vr))
            self.pr = float(griddata(vra, pra, self.vr))
            self.u = float(griddata(vra, ua, self.vr))
            return
        return Ta, ha, pra, ua, vra


    def print(self):
        pass


def main():
    pass


# the following if statement causes main() to run
# only if this file is being run explicitly, not if it is
# being imported into another Python program as a module
if __name__ == "__main__":
    main()
