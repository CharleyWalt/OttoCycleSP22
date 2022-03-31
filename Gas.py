import numpy as np
from scipy.interpolate import griddata


class Gas():
    """
    The gas class is used to find air properties where the air is modeled as an ideal gas which is
    the working fluid for the  piston-cylinder arrangement.
    """

    def __init__(self, T=None, h=None, pr=None, u=None, v_r=None, name=None):
        """
        :param T: temperature in degrees K
        :param h: enthalpy in kJ/kg
        :param pr: relative pressure
        :param u: internal energy in kJ/kg
        :param v_r: relative energy
        :param name: a convenient identifier
        """
        # assign arguments to class properties
        self.T = T  # Temperature - degrees K
        self.h = h  # Enthalpy - kJ/kg
        self.pr = pr  # Relative Pressure
        self.u = u  # Internal Energy - kJ/kg
        self.v_r = v_r  # Specific Volume
        self.name = name  # a useful identifier
        if T == None and h == None and pr == None and u == None and v_r == None:
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
        Ta, ha, pra, ua, v_ra = np.loadtxt('air_properties.txt', skiprows=1, unpack=True)

        # get air properties
        if self.T is not None:
            self.h = float(griddata(Ta, ha, self.T))
            self.pr = float(griddata(Ta, pra, self.T))
            self.u = float(griddata(Ta, ua, self.T))
            self.v_r = float(griddata(Ta, v_ra, self.T))
        if self.h is not None:
            self.T = float(griddata(ha, Ta, self.h))
            self.pr = float(griddata(ha, pra, self.h))
            self.u = float(griddata(ha, ua, self.h))
            self.v_r = float(griddata(ha, v_ra, self.h))
        if self.pr is not None:
            self.T = float(griddata(pra, Ta, self.pr))
            self.h = float(griddata(pra, ha, self.pr))
            self.u = float(griddata(pra, ua, self.pr))
            self.v_r = float(griddata(pra, v_ra, self.pr))
        if self.u is not None:
            self.T = float(griddata(ua, Ta, self.u))
            self.h = float(griddata(ua, ha, self.u))
            self.pr = float(griddata(ua, pra, self.u))
            self.v_r = float(griddata(ua, v_ra, self.u))
        if self.v_r is not None:
            self.T = float(griddata(v_ra, Ta, self.v_r))
            self.h = float(griddata(v_ra, ha, self.v_r))
            self.pr = float(griddata(v_ra, pra, self.v_r))
            self.u = float(griddata(v_ra, ua, self.v_r))
        return Ta, ha, pra, ua, v_ra

    def print(self):
        pass


def main():
    pass


# the following if statement causes main() to run
# only if this file is being run explicitly, not if it is
# being imported into another Python program as a module
if __name__ == "__main__":
    main()
