""" Module to create a genetic algorithm """
from pnl import PnL
import numpy as np
from initialize import Initialize
import copy

class GenAlgo():

    def __init__(self,self_, min_results = 10, population = 25, generations = 25, co_rate = .65, mutation_rate = .04,
                 fitness_function = PnL.sharpe_ratio):

        new_obj = copy.deepcopy(self_)
        self.__dict__.update(new_obj.__dict__)
        self.init_ = copy.deepcopy(Initialize)
        self.min_results = min_results
        self.population = population
        self.generations = generations
        self.co_rate = co_rate
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function
        self.nb_genes = len(self.op_param)

    def __call__(self):
        """Function that runs the genetic algo"""
        self.create_chromosome()

    def iterate_population(func):
        """ Decorator to run the size of a population"""
        def wrapper_(self):
            for items_ in range(self.population):
                func(self)

            return population
        return wrapper_

    @iterate_population
    def create_chromosome(self):
        """ Function that creates initial chromosomes for initial population"""

        self.init_.__call__(self)
        for item in range(len(self.op_param)):
            if len(self.op_param[item]) > 1:
                self.op_param[item][0][self.op_param[item][1]] = \
                    np.random.choice(self.op_param[item][0][self.op_param[item][1]])
            else:
                setattr(self, self.op_param[item][0], np.random.choice(getattr(self, self.op_param[item][0])))










