from utils.vp_detection import VPDetection
import numpy as np
import matplotlib.pyplot as plt

from utils.read_image import open_image
from utils.Drawing import draw_vanishing_data, DrawLinesAndRectangle, draw_diffrence
from utils.vanishing import Vanishing
from utils.Line import Line

seed = 1337
length_thresh = 90
focal_length_all = 1102.79

img = open_image()

pil_img = img
img = np.array(img)
fake_img = plt.imread('.\\imgs\\fake.webp')
cant_decide_img = plt.imread('.\\imgs\\cant_decide.png')

# plot the image let the user draw rectangle and line
draw = DrawLinesAndRectangle(img)
mask_box = draw.get_rectangle()
user_lines = draw.get_lines()

# Selected object Vanishing Points:
# ----------------------
# calculate lines interactions
lines_in = np.array([Line(*line) for line in user_lines])
clusters_intersection_in = [Line.multiple_lines_intersection(cluster) for cluster in lines_in.reshape((-1,2))]
# calculate vanishing points
vanishing_data_in = Vanishing(clusters_intersection_in)

# Image Vanishing Points:
# ----------------------
# calcuate image VPs
vpd_all = VPDetection(length_thresh, None, focal_length_all, seed)
vpd_all.find_vps(img, mask_box)
vpd_all.set_model_lines_and_update_vps('out')

# calcualte clusters
vpd_all.create_clusters()
cluster_out = [[],[], []]
for i, cluster in enumerate(vpd_all.clusters):
    for index in cluster:
        cluster_out[i].append(vpd_all.lines[index])
    cluster_out[i] = sorted(cluster_out[i], key=lambda line: np.sqrt((line[0] - line[2])**2 + (line[1] - line[3])**2), reverse=True)

# calcuate vanishing points of out
cluster_lines_object = [[Line(*line) for line in cluster] for cluster in cluster_out]

cluster_intersection_out = [Line.multiple_lines_intersection(cluster) for cluster in cluster_lines_object]
vanishing_data_out = Vanishing(cluster_intersection_out)

# draw vanishing data
plt.gca().set_title('Selected PP:', color='red')
draw_vanishing_data(pil_img, vanishing_data_in, ax=plt.gca())
plt.gca().set_title('Background PP:', color='red')
draw_vanishing_data(pil_img, vanishing_data_out, cluster_lines_object, ax=plt.gca())

draw_diffrence(pil_img, vanishing_data_in, vanishing_data_out, fake_img, cant_decide_img, ax=plt.gca())