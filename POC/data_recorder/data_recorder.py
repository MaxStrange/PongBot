"""
A module for holding a class for recording data.
"""


class DataRecorder:
    """
    A class for recording data.
    """
    def __init__(self, log_file):
        """
        Constructor.
        :param log_file: The file to log data in (an already open file handle)
        :return: void
        """
        self.log_file = log_file

    def record_data(self, x, y, d, nx, ny, nd):
        """
        Record the measured and predicted data.
        """
        f = lambda i: str(int(i))
        data_point = "" + f(x) + "," + f(y) + "," + f(d) + "," + f(nx) + "," + f(ny) + "," + f(nd) + "," + "\n"
        self.log_file.write(data_point)