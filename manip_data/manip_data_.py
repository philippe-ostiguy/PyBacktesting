import csv
import functools

class ManipData():


    def __init__(self):
        pass

    @classmethod
    def write_data(cls, dir_output, name_out, **kwargs):
        """ Write data to a csv

        Parameters
        ----------
        dir_output : str
            directory where we want our data to be written
        name_out : str
            name of the file name
        **kwargs : keyword param
            dictionary with keys and items to be written
        """

        with open(dir_output + name_out + ".csv" , 'w', newline='') as f:
            writer = csv.writer(f)
            for key, item in kwargs.items():
                writer.writerow([key,item])
