"""Module to run the program - use optimization tool if asked"""
from pnl import PnL
from manip_data import ManipData as md
from date_manip import DateManip as dm
from optimize.genetic_algorithm import GenAlgo as ga
import copy

class Optimize(PnL):

    def __init__(self):
        super().__init__()

    def __call__(self):

        # If the systeme do a walkfoward analysis
        if self.is_walkfoward:
            self.walf_foward()
        else :
            self.execute_()

    def execute_(self,add_doc=""):
        """ Just runs the whole program

         Load data (and clean), calculate indicators, check for signal, calculate pnl + write to results to file
         """

        # If the systeme optimize the parameters
        if self.is_optimize:
            self.optimize()

        else :
            self.init_series()
            super().__call__()

        md.write_csv_(self.dir_output, self.name_out, add_doc=add_doc,
                      is_walkfoward=self.is_walkfoward, **self.pnl_dict)

    def optimize(self):
        """ This function return the actual parameters to be tested
        """

        self.optimize_param()
        ga(self).__call__()

    def walf_foward(self):
        md_ = md

        _first_time = True
        self.dict_date_ = dm.date_dict(self.date_debut, self.date_fin,
                                       **self.dict_name_)

        if (len(self.dict_date_)) == 0:
            raise Exception("Total period not long enough for optimization")

        for key,value in self.dict_date_.items():
            for key_, value_ in self.dict_name_.items():
                self.date_debut = self.dict_date_[key][key_][0]
                self.date_fin = self.dict_date_[key][key_][1]
                if _first_time :
                    md_(self.dir_output,self.name_out,extension = key_).erase_content()
                self.execute_(add_doc=key_)
            _first_time = False