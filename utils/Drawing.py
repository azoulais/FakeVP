import matplotlib.pyplot as plt

import matplotlib.lines as mlines
import numpy as np
from PIL import Image
from matplotlib.patches import Rectangle, ConnectionPatch
from utils.vanishing import Vanishing
import numpy as np

DEFAULT_MARGINS = 100
COLORS = ['red', 'blue', 'green']


class DrawLinesAndRectangle():
    def __init__(self, img):
        self.lines = []
        self.rectangle = []
        self.is_rectangle_created = False
        self.image = img
        self.line_scaler_x = 0
        self.line_scaler_y = 0
        self.__plot(self.image, 'Select Object On The Image:')
    
    def __plot(self, image, title):
        self.ax = plt.gca()
        self.ax.set_title(title, color='red')
        self.ax.imshow(image)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.__on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.__on_release)
        plt.axis('off')
        plt.show()

    def __get_color(self):
        colors = ['r', 'b', 'g']
        return colors[(len(self.lines) -1) // 2]

    def __on_press(self, event):
        shape = [event.xdata, event.ydata]
        if self.is_rectangle_created:
            self.lines.append(shape)
        else:
            self.rectangle = shape

    def __on_release(self, event):
        shape = self.rectangle if not self.is_rectangle_created else self.lines[-1]

        shape += [event.xdata, event.ydata]
        if self.is_rectangle_created:
            draw = ConnectionPatch((shape[0], shape[1]), (shape[2], shape[3]),"data", "data", linewidth=4, color=self.__get_color())
            self.ax.add_patch(draw) 
        else:
            x1, y1, x2, y2 = self.rectangle
            x1, y1, x2, y2 = min(int(x1), int(x2)), min(int(y1), int(y2)), max(int(x1), int(x2)), max(int(y1), int(y2))
            draw = Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='b', facecolor='none')
            self.is_rectangle_created = True
            # Crop the image
            cropped_image = self.image[int(y1):int(y2), int(x1):int(x2)]
            
            # update line scalers
            self.line_scaler_x = x1
            self.line_scaler_y = y1

            self.__plot(cropped_image, 'Selected Lines:')
        plt.draw()

    def __scale_line(self, line):
        return [line[0] + self.line_scaler_x,
                line[1] + self.line_scaler_y,
                line[2] + self.line_scaler_x,
                line[3] + self.line_scaler_y]

    def get_lines(self):
        return [self.__scale_line(line) for line in self.lines]
    
    def get_rectangle(self):
        return self.rectangle
    

# a class to draw the vanishing points and lines on an image


# a class to draw the vanishing points and lines on an image
class Drawing:
    def __init__(self, pil_img, vanishing_data, default_margins=DEFAULT_MARGINS, ax = plt):
        self.__pil_img__ = pil_img
        self.__vanishing_data__ = vanishing_data
        self.__default_margins__ = default_margins
        self.img_width, self.img_height = pil_img.size
        self.__showed__ = None
        self.__initialize__()
        ax.axis('off')
        self.ax=ax


    def __initialize__(self):
        self.__calc_margins__()



    # calculate the margins needed to add in order to draw the vanishing points and lines
    def __calc_margins__(self):
        points = self.__vanishing_data__.vanishing_points
        if self.__vanishing_data__.principal_point is not None:
            points.append(self.__vanishing_data__.principal_point)
        top = min([0] + [point[1] for point in points]) - self.__default_margins__
        right = max([self.img_width] + [point[0] for point in points]) + self.__default_margins__
        bottom = max([self.img_height] + [point[1] for point in points]) + self.__default_margins__
        left = min([0] + [point[0] for point in points]) - self.__default_margins__

        self.top = int(0 - top)
        self.right = int(right - self.img_width)
        self.bottom = int(bottom - self.img_height)
        self.left = int(0 - left)


    # add the calculated margins to the image (white background)
    def __add_margins__(self):
        self.new_width = self.img_width + self.right + self.left
        self.new_height = self.img_height + self.top + self.bottom
        result = Image.new(self.__pil_img__.mode, (self.new_width, self.new_height), (255, 255, 255))
        result.paste(self.__pil_img__, (self.left, self.top))
        self.im_margined = result

    # draw a line given two points (on the image with the new margins)
    def draw_line_from_points(self, point1, point2, color='red', dashed=False, linewidth=2):
        left = self.left if self.__showed__ == 'margined' else 0
        top = self.top if self.__showed__ == 'margined' else 0
        line = mlines.Line2D([point1[0] + left, point2[0] + left], [point1[1] + top, point2[1] + top], color=color,
                             linestyle='dashed' if dashed else 'solid', linewidth=linewidth)
        # Add the line to the plot
        self.ax.add_line(line)

    # draw a line given the line object (on the image with the new margins)
    def draw_Line(self, line, color='red', dashed=False, linewidth=2):
        left = self.left if self.__showed__ == 'margined' else 0
        top = self.top if self.__showed__ == 'margined' else 0
        # Draws the given line on the margined image
        line = mlines.Line2D([line.p1[0] + left, line.p2[0] + left],
                             [line.p1[1] + top, line.p2[1] + top], color=color,
                             linestyle='dashed' if dashed else 'solid', linewidth=linewidth)
        # Add the line to the plot
        self.ax.add_line(line)

    # draw a circle given the center and radius (on the image with the new margins)
    def draw_circle(self, center, radius=15, color='red'):
        left = self.left if self.__showed__ == 'margined' else 0
        top = self.top if self.__showed__ == 'margined' else 0
        circle = plt.Circle((center[0] + left, center[1] + top), radius, color=color)
        self.ax.add_patch(circle)

    #add the margined image to the plot
    def show_margined_image(self):
        self.__showed__ = 'margined'
        self.__add_margins__()
        self.ax.imshow(self.im_margined)

    def show_original_image(self):
        self.__showed__ = 'original'
        self.ax.imshow(self.__pil_img__)

    #draw the (given) base lines on the image
    def draw_base_lines(self,colors = COLORS):
        for set, color in zip(self.__vanishing_data__.lines_clusters, colors):
            for line in set:
                self.draw_Line(line, color=color)

    # draw the (given) base lines on the image with an extension to the intersection point (vanishing point)
    def draw_extended_base_lines(self):
        for set, vp, color in zip(self.__vanishing_data__.lines_clusters, self.__vanishing_data__.vanishing_points,
                                  COLORS):
            for line in set:
                self.draw_line_from_points(vp, line.p2, color=color, dashed=True)

    # draw the vanishing lines on the image
    def draw_vanishing_lines(self, color='gray'):
        for line in self.__vanishing_data__.vanishing_lines:
            self.draw_Line(line, color=color)

    # draw the altitudes of the triangle created by the vanishing lines
    def draw_altitudes(self, color='deepskyblue'):
        for line in self.__vanishing_data__.altitudes:
            self.draw_Line(line, color=color, dashed=True)

    # draw the principal point on the image
    def draw_principal_point(self, color = 'deepskyblue'):
        self.draw_circle(self.__vanishing_data__.principal_point, color=color)


    def draw_lines(self,clusters,colors = COLORS):
            for set, color in zip(clusters, colors):
                for line in set:
                    self.draw_Line(line, color=color)

def draw_vanishing_data(pil_img, vanishing_data, cluster_lines_object = None, ax=plt):
    draw_image = Drawing(pil_img, vanishing_data, ax=ax)   # create the drawing object to draw the vanishing data on the image with appropriate margins
    draw_image.show_original_image()
    # draw_image.show_margined_image()    # if cluster_lines_object != None:
    #     draw_image.draw_lines(cluster_lines_object)
    draw_image.draw_base_lines()                # draw the given base lines
    draw_image.draw_extended_base_lines()       # draw the base lines extended to the vanishing points
    draw_image.draw_vanishing_lines()           # draw the vanishing lines
    draw_image.draw_altitudes()                 # draw the altitudes
    draw_image.draw_principal_point()           # draw the principal point
    plt.show()

def draw_diffrence(pil_img, vanishing_data_in: Vanishing, vanishing_data_out: Vanishing, fake_img, cant_decide_img, ax=plt):
    draw_image_in = Drawing(pil_img, vanishing_data_in, ax=ax)
    draw_image_out = Drawing(pil_img, vanishing_data_out, ax=ax)
    draw_image_in.show_original_image()
    draw_image_in.draw_principal_point()
    draw_image_out.draw_principal_point()
    draw = ConnectionPatch(vanishing_data_in.principal_point, vanishing_data_out.principal_point,"data", "data", linewidth=4, color='r')
    ax.add_patch(draw) 
    threshold = (pil_img.height + pil_img.width) // 7
    if np.sqrt((vanishing_data_in.principal_point[0] - vanishing_data_out.principal_point[0]) ** 2 + (vanishing_data_in.principal_point[1] - vanishing_data_out.principal_point[1]) ** 2) > threshold:
        ax.set_title('Object is FAKE', color='red')
    else:
        ax.set_title('Cant Decide', color='red')
    plt.show()