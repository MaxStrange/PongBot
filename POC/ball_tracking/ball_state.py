"""
A module for holding ball state classes
"""


class BallState:
    """
    A class to hold data about a ball's current position, radius, and velocity.
    """
    def __init__(self, x_pos=None, y_pos=None, d_pos=None, x_vel=None, y_vel=None, d_vel=None, radius=None):
        """
        Constructor
        :param x_pos:
        :param y_pos:
        :param d_pos:
        :param x_vel:
        :param y_vel:
        :param d_vel:
        :param radius:
        :return: void
        """
        self.__x_pos = x_pos
        self.__y_pos = y_pos
        self.__d_pos = d_pos
        self.__x_vel = x_vel
        self.__y_vel = y_vel
        self.__d_vel = d_vel
        self.__radius = radius

    def __str__(self):
        """
        As Str
        :return: The str representation of this object
        """
        return self.to_str()

    def to_str(self, as_int=False):
        """
        Returns a string version of the state
        :param as_int: If you want the values printed as integers
        :return: the string version of this BallState object
        """
        f = (lambda v: str(int(v))) if as_int else (lambda v: str(v))
        str_func = lambda var, val: var + ": " + f(val) + " "
        state_str = ""
        state_str += str_func("x", self.get_x_pos())
        state_str += str_func("y", self.get_y_pos())
        state_str += str_func("d", self.get_d_pos())
        state_str += str_func("vx", self.get_x_velocity())
        state_str += str_func("vy", self.get_y_velocity())
        state_str += str_func("vd", self.get_d_velocity())
        state_str += str_func("rad", self.get_radius())
        return state_str

    def format_for_sending(self):
        """
        Returns a string for sending over TCP port.
        :return: str for sending
        """
        x = self.get_x_pos()
        y = self.get_y_pos()
        d = self.get_d_pos()
        vx = self.get_x_velocity()
        vy = self.get_y_velocity()
        vd = self.get_d_velocity()
        return "%1.4f%1.4f%1.4f%1.4f%1.4f%1.4f" % (x, y, d, vx, vy, vd)

    def get_x_pos(self):
        """
        Gets the x pos
        :return: x pos
        """
        return self.__x_pos

    def get_y_pos(self):
        """
        Gets the y pos
        :return: y pos
        """
        return self.__y_pos

    def get_d_pos(self):
        """
        Gets the d pos
        :return: d pos
        """
        return self.__d_pos

    def get_x_velocity(self):
        """
        Gets the x velocity
        :return: x velocity
        """
        return self.__x_vel

    def set_x_velocity(self, x_vel):
        """
        Sets the x velocity
        :param x_vel: x velocity
        :return: void
        """
        self.__x_vel = x_vel

    def get_y_velocity(self):
        """
        Gets the y velocity
        :return: y velocity
        """
        return self.__y_vel

    def set_y_velocity(self, y_vel):
        """
        Sets y velocity
        :param y_vel: y velocity
        :return: void
        """
        self.__y_vel = y_vel

    def get_d_velocity(self):
        """
        Gets the d velocity
        :return: d velocity
        """
        return self.__d_vel

    def set_d_velocity(self, d_vel):
        """
        Sets d velocity
        :param d_vel: d velocity
        :return: void
        """
        self.__d_vel = d_vel

    def get_radius(self):
        """
        Gets the radius
        :return: radius
        """
        return self.__radius

    def set_radius(self, rad):
        """
        Sets the radius
        :return: void
        """
        self.__radius = rad