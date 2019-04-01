import numpy as np
import os
import sys
import pprint

from numpy.random import random_sample as rand
from astropy import units as u
from astropy.coordinates import SkyCoord


class Cone:
    """
    """

    def __init__(self):
        """
        Not intended to be instantiated.
        """
        pass

    @staticmethod
    def random_skycoord():
        """
        """
        ra_rad = (2 * np.pi * rand()) * u.rad
        dec_rad = np.arcsin(2. * (rand() - 0.5)) * u.rad

        skycoord = SkyCoord(ra_rad, dec_rad)
        return skycoord

    @staticmethod
    def random_coords():
        """
        """
        ra_rad = (2 * np.pi * rand()) * u.rad
        ra_deg = ra_rad.to_value(u.deg)
        dec_rad = np.arcsin(2. * (rand() - 0.5)) * u.rad
        dec_deg = dec_rad.to_value(u.deg)

        return {'ra':ra_deg, 'dec':dec_deg}

    @staticmethod
    def random_cone(min_radius, max_radius):
        """
        """
        if not (0 <= min_radius < max_radius):
            raise ValueError('min-radius must be in the range [0,max_radius).')
        coords = Cone.random_coords()
        coords['radius'] = (max_radius - min_radius) * rand() + min_radius
        return coords

    @staticmethod
    def generate_random(num_points, min_radius, max_radius):
        """
        Yield objects with random (and legal) ra, dec, and radius attirbutes.
        """
        if not (0 <= min_radius < max_radius):
            raise ValueError('min-radius must be in the range [0,max_radius).')
        if num_points <= 0:
            raise ValueError('num_points must be a positive number.')

        def cones(num_points, min_radius, max_radius):
            for i in range(num_points):
                cone = Cone.random_cone(min_radius, max_radius)
                yield cone

        return cones(num_points, min_radius, max_radius)

    @staticmethod
    def write_random(num_points, min_radius, max_radius, filename=None):
        generator = Cone.generate_random(num_points, min_radius, max_radius)

        stream = sys.stdout
        if filename is not None:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            stream = open(filename, "w", encoding="utf-8")

        pp = pprint.PrettyPrinter(width=100, stream=stream, compact=True)
        stream.write("[")
        sep = ''
        indent = '    '
        for cone in generator:
            s = pp.pformat(cone)
            stream.write(f'{sep}\n{indent}{s}')
            sep = ','
        stream.write("\n]\n")

        if filename is not None:
            stream.close()
