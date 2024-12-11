import numpy as np
from utils.Line import Line


# a class to calculate the vanishing points and lines of an image given 3 sets of lines
class Vanishing:
    def __init__(self, lines_clusters):
        if len(lines_clusters) != 3:
            raise ValueError("Vanishing points requires 3 lines sets")
        # self.__pil_img__ = pil_img
        self.lines_clusters = lines_clusters
        self.vanishing_points = []
        self.vanishing_lines = []
        self.__normals__ = []
        self.altitudes = []
        self.principal_point = None

        self.__initialize__()

    def __initialize__(self):
        self.__calc_vanishing_points__()  # calculate the vanishing points
        self.__calc_vanishing_lines__()   # calculate the vanishing lines
        self.__calc_altitudes__()         # calculate the altitudes and principal point

    # calculate the vanishing points
    def __calc_vanishing_points__(self):
        for cluster in self.lines_clusters:
            if len(cluster) != 2:
                raise ValueError("Vanishing points requires 2 lines per cluster")
            l1, l2 = cluster[0], cluster[1]
            self.vanishing_points.append(l1[l1.intersection(l2)[0]])

    # calculate the vanishing lines
    def __calc_vanishing_lines__(self):
        vl1 = Line(*self.vanishing_points[0], *self.vanishing_points[1])
        vl2 = Line(*self.vanishing_points[1], *self.vanishing_points[2])
        vl3 = Line(*self.vanishing_points[2], *self.vanishing_points[0])

        self.vanishing_lines.append(vl1)
        self.vanishing_lines.append(vl2)
        self.vanishing_lines.append(vl3)

    # calculate the altitudes and principal point
    def __calc_altitudes__(self):
        A = np.asarray([[0, -1], [1, 0]])
        n1 = A @ ((self.vanishing_points[1] - self.vanishing_points[2]) / np.linalg.norm((self.vanishing_points[1] - self.vanishing_points[2])))
        n2 = A @ ((self.vanishing_points[0] - self.vanishing_points[2]) / np.linalg.norm((self.vanishing_points[0] - self.vanishing_points[2])))
        n3 = A @ ((self.vanishing_points[0] - self.vanishing_points[1]) / np.linalg.norm((self.vanishing_points[0] - self.vanishing_points[1])))

        self.__normals__.append(n1)
        self.__normals__.append(n2)
        self.__normals__.append(n3)

        altitude1 = Line(*self.vanishing_points[0], *(self.vanishing_points[0] + -5000*n1))
        altitude2 = Line(*self.vanishing_points[1], *(self.vanishing_points[1] + 5000*n2))
        altitude3 = Line(*self.vanishing_points[2], *(self.vanishing_points[2] + -5000*n3))

        t1 = altitude1.intersection(self.vanishing_lines[1])
        t2 = altitude2.intersection(self.vanishing_lines[2])
        t3 = altitude3.intersection(self.vanishing_lines[0])

        po1 = altitude1[t1[0]]
        po2 = altitude2[t2[0]]
        po3 = altitude3[t3[0]]

        altitude1 = Line(*self.vanishing_points[0], *po1)
        altitude2 = Line(*self.vanishing_points[1], *po2)
        altitude3 = Line(*self.vanishing_points[2], *po3)

        self.altitudes.append(altitude1)
        self.altitudes.append(altitude2)
        self.altitudes.append(altitude3)

        self.principal_point = Line.three_lines_intersection(altitude1, altitude2, altitude3)
