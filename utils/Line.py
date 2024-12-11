import numpy as np

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.p1 = np.asarray([x1, y1],dtype=int)
        self.p2 = np.asarray([x2, y2],dtype=int)
        # self.x1 = x1
        # self.y1 = y1
        # self.x2 = x2
        # self.y2 = y2
        self.m = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else np.inf
        self.b = y1 - self.m * x1

    #given two lines, return the intersection point in parametric form (i.e. t1, t2)
    def intersection(self, other):
        x1, y1 = self.p1[0], self.p1[1]
        u1, v1 = self.p2[0], self.p2[1]
        x2, y2 = other.p1[0], other.p1[1]
        u2, v2 = other.p2[0], other.p2[1]

        A = np.array([[x1 - u1, u2 - x2], [y1 - v1, v2 - y2]])
        # print(A)
        if np.linalg.det(A) == 0:
            raise ValueError("Lines are parallel")
        b = np.asarray(([[u2 - u1], [v2 - v1]]))
        # print(b)
        A_inv = np.linalg.inv(A)
        # print(A_inv)

        return A_inv @ b

    # given two lines, return the intersection point in cartesian form (i.e. x, y)
    def cartesian_intersection(self, other):
        if self.m == other.m:
            raise ValueError("Lines are parallel")
        x = (self.b - other.b) / (other.m - self.m)
        y = self.m * x + self.b
        return np.asarray([x, y])

    #overload the [] operator to return the (x, y) point at a given t value
    def __getitem__(self, key):
        return (self.p1-self.p2)*key + self.p2

    #overload the str operator to return the string representation of the line
    def __str__(self):
        return f"Line: {self.p1} - {self.p2}"

    #overload the == operator to compare two lines
    def __eq__(self, other):
        return self.b == other.b and self.m == other.m

    #given 3 lines, return the nearest point to all 3 lines (if the all intersect, this is the intersection point)
    def three_lines_intersection(line1, line2, line3):
        C = np.asarray([[0, -1], [1, 0]])
        p1 = line2.cartesian_intersection(line3)
        p2 = line1.cartesian_intersection(line3)
        p3 = line1.cartesian_intersection(line2)

        n1 = C @ ((p2 - p3) / np.linalg.norm((p2 - p3)))
        n2 = C @ ((p1 - p3) / np.linalg.norm((p1 - p3)))
        n3 = C @ ((p1 - p2) / np.linalg.norm((p1 - p2)))

        D1 = np.asarray([[n1[0] ** 2, n1[0] * n1[1]], [n1[0] * n1[1], n1[1] ** 2]])
        D2 = np.asarray([[n2[0] ** 2, n2[0] * n2[1]], [n2[0] * n2[1], n2[1] ** 2]])
        D3 = np.asarray([[n3[0] ** 2, n3[0] * n3[1]], [n3[0] * n3[1], n3[1] ** 2]])
        D_inv = np.linalg.inv(D1 + D2 + D3)
        C = D1 @ p1 + D2 @ p2 + D3 @ p3
        return D_inv @ C

    def multiple_lines_intersection(lines):
        vp = np.zeros((2,))
        dict = {}
        for i in range(len(lines)):
            for j in range(i+1,len(lines)):
                linea = lines[i]
                lineb = lines[j]

                try:
                    inter = Line.intersection(linea,lineb)
                except ValueError:
                    continue

                dict[tuple(linea[inter[0]])] = (linea,lineb)
                vp += linea[inter[0]]
        keys = np.array([np.array(key) for key in dict.keys()])
        median_vp = np.median(keys,axis=0)
        avg_vp =vp/ len(lines)*(len(lines)-1)/2
        avg_vp = median_vp
        best = list(dict.keys())[0]
        for key in dict.keys():
            if np.linalg.norm(np.asarray(key)-avg_vp) < np.linalg.norm(np.asarray(best)-avg_vp):
                best = key

        return list(dict[best])

    def filter_outliears(clusters):
        stds = []
        means = []
        lines_filtered=None
        for lines in clusters:
            lines_filtered = [line for line in lines if line.m != np.inf]
            stds.append(np.std([line.m for line in lines_filtered]))
            means.append(np.mean([line.m for line in lines_filtered]))
        
        new_clusters = []
        for lines, curr_std, curr_mean in zip(clusters, stds, means):
            cluster = []
            other_stds = [x for x in stds if x != curr_std]
            other_means = [x for x in means if x != curr_mean]
            for line in lines:
                if abs(line.m - curr_mean) <1 * curr_std or all([abs(line.m - mean) > 2 * std for (std, mean) in zip(other_stds, other_means)]):
                    cluster.append(line)
            if len(cluster) < 2:
                cluster = lines
            new_clusters.append(cluster)
        return new_clusters
