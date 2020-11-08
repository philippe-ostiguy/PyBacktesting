""" Module to create a genetic algorithm """
from pnl import PnL
import numpy as np
from initialize import Initialize
import copy

class GenAlgo(PnL):

    def __init__(self,self_, min_results = 10, size_population = 25, generations = 25, co_rate = .65, mutation_rate = .04,
                 fitness_function = PnL.sharpe_ratio):
        super().__init__()
        new_obj = copy.deepcopy(self_)
        self.__dict__.update(new_obj.__dict__)
        self.min_results = min_results
        self.size_population = size_population
        self.generations = generations
        self.co_rate = co_rate
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function
        self.nb_genes = len(self.op_param)
        self.population = []

    def __call__(self):
        """Function that runs the genetic algo"""
        self.create_chromosome()
        t = 5


    def iterate_population(func):
        """ Decorator to run each chromosome with the size of the population"""
        def wrapper_(self):
            for items_ in range(self.size_population):
                func(self)
                print(self.population[items_].pnl_dict[self.ann_return_])
                print(self.population[items_].pnl_dict[self.nb_trades_])
        return wrapper_


    @iterate_population
    def create_chromosome(self):
        """ Function that creates initial chromosomes randomly for initial population"""

        Initialize.__call__(self)
        self.optimize_param()
        for item in range(len(self.op_param)):
            if len(self.op_param[item]) > 1:
                self.op_param[item][0][self.op_param[item][1]] = \
                    np.random.choice(self.op_param[item][0][self.op_param[item][1]])
            else:
                setattr(self, self.op_param[item][0], np.random.choice(getattr(self, self.op_param[item][0])))
        self.eval_pop()

    def eval_pop(self):
        super().__call__()
        new_pop = copy.deepcopy(self)
        self.population.append(new_pop)