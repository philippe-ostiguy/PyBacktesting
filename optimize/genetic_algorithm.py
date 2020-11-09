""" Module to create a genetic algorithm """
from pnl import PnL
import numpy as np
from initialize import Initialize
import copy

class GenAlgo(PnL):

    def __init__(self,self_, min_results = 5, size_population = 20, generations = 20, co_rate = .65,
                 mutation_rate = .04):
        super().__init__()
        new_obj =  copy.deepcopy(self_)
        self.__dict__.update(new_obj.__dict__)
        del new_obj,self_
        self.min_results = min_results
        self.size_population = size_population
        self.generations = generations
        self.co_rate = co_rate
        self.mutation_rate = mutation_rate
        self.fitness_function = self.sharpe_ratio_ #string name of the fitness function
        self.nb_genes = len(self.op_param)
        self.population = []
        self.prob = 'probability'

    def __call__(self):
        """Function that runs the genetic algo"""
        self.create_chromosome()
        self.fitness_selection()

    def iterate_population(func):
        """ Decorator to run each chromosome with the size of the population"""

        def wrapper_(self):
            items_ = 0
            while (items_ < self.size_population):
                self.reset_value()
                self.pnl_dict = {}
                func(self)
                self.pnl_()
                if (self.pnl_dict[self.nb_trades_] == None):
                    continue
                if self.pnl_dict[self.nb_trades_] < self.min_results:
                    continue
                else:
                    self.population.append(self.pnl_dict)
                    if (self.population[items_][self.nb_trades_] > 150):
                        raise Exception("Error with the number of trades")
                    print(self.population[items_][self.ann_return_])
                    print(self.population[items_][self.sharpe_ratio_])
                    print(self.population[items_][self.nb_trades_])

                    items_+=1
        return wrapper_

    def fitness_selection(self):
        """Decorator to set probability to select each chromosome using the wheel selection.

        We truncate the Put the smallest performance evaluator to 0 and raise by some amount the others evaluators. It makes
        sure all values are equal or above 0
        """

        def wrapper_(self):
            min_val = min(item[self.fitness_function] for item in self.population)
            if min_val >= 0:
                min_val = 0
            self.fitt_total = 0
            for item in self.population:
                item[self.fitness_function] += min_val  # Truncated fitness function. Put the smalles
                self.fitt_total += item[self.fitness_function]
                item[self.fitness_function] = self.fitt_total
            func(self)
        return wrapper_

    @iterate_population
    def create_chromosome(self):
        """ Function that creates initial chromosomes randomly for initial population"""

        Initialize.__call__(self)
        self.optimize_param() #reinitialize parameters to optimize with all possible choices
        for item in range(len(self.op_param)):
            if len(self.op_param[item]) > 1:
                self.op_param[item][0][self.op_param[item][1]] = \
                    np.random.choice(self.op_param[item][0][self.op_param[item][1]])
            else:
                setattr(self, self.op_param[item][0], np.random.choice(getattr(self, self.op_param[item][0])))

    @iterate_population
    def create_gen(self):
        """ Create a new chromosome in the new generation"""


        pass


    @fitness_selection
    def fitness_selection_(self):
        """ Selection 2 chromosomes for next generation

        Using the roulette wheel selection
        """
        sum_ = 0
        for item in self.population:
            item[self.prob] = item[self.fitness_function]/self.fitt_total






