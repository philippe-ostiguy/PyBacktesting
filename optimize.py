"""Module to run the program - use optimization tool if asked"""
from pnl import PnL
from manip_data import ManipData as md
from date_manip import DateManip as dm

class Optimize(PnL):

    def __init__(self):
        super().__init__()
        super().__call__()

    def __call__(self):

        if self.is_walkfoward: #If we use an optimizing technique

            self.optimize()

        #write results to csv
        md.write_data(self.dir_output, self.name_out,add_doc=self.doc_name_[self.training_name_],
                      is_walkfoward=self.is_walkfoward, **self.pnl_dict)

    def optimize(self):
        self.dict_date_ = dm.date_dict(self.date_debut, self.date_fin,
                                       **self.dict_name_)
        t= 5