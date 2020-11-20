""" Module to create a genetic algorithm """
from pnl import PnL
import numpy as np
from initialize import Initialize
import copy
import random

class GenAlgo(PnL):
    """ Genetic algo that return the parameter `self.op_param` and pnl `self.pnl_dict` for the best chromosome
    """

    def __init__(self,self_, min_results = 10, size_population = 20, generations = 25, co_rate = .6,
                 mutation_rate = .10):
        """ Setting the parameters here

        Parameters
        ----------
        `self_` : class instance
            This is the instance of the class where GenAlgo() class is called. We copy it in the constructor here
        `self.min_results` : int
            Minimum numbers of results needed to consider a chromosome in the training period. If we have under this
            number, the chromosome is not considerd
        `self.population` : int
            Size of a population (number of chromosomes_
        `self.generations` : int
            Number of generations
        `self.co_rate` : float
            Cross-over rate
        `self.mutation_rate` : float
            Mutation rate
        `self.fitness_function` : str
            Name of the fitness function. Ex: `self.sharpe_ratio_` name is defined in `initialize.py` and function
            is defined in `pnl.py`

        """

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
        self.nb_genes = len(self.op_param) #nb of genes per chromosome
        self.results_pop = [] #pnl for the population
        self.population = []

    def __call__(self):
        """Function that runs the genetic algo. This is the "main" function

        First it creates the initial population in `self.create_chromosome()`. Then it optimize, run through each
        population and new generations in `self.run_generations()`. Finally the results are return with function
        `self.return_results()`

        Return
        ------
        `self.pnl_dict` : dict
            pnl of the best chromosome

        `self.op_param` : list
            parameters of the best chromosome
        """

        self.create_chromosome()
        self.run_generations()
        return self.return_results()

    def iterate_population(func):
        """ Decorator to run each chromosome with the size of the population

        The function will run through the entire population. If the sharpe_ratio is greater than `self.fitness_level`
        (3 by default), the algo stopped and return the pnl `self.pnl_dict` and the optimal parameters `self.op_param`
        """

        def wrapper_(self):
            items_ = 0
            results_tempo = []
            population_tempo = []
            while (items_ < self.size_population):
                self.reset_value()
                self.pnl_dict = {}
                Initialize.__call__(self)
                self.optimize_param()  # reinitialize parameters to optimize with all possible choices
                func(self)
                self.pnl_()
                if (not bool(self.pnl_dict)):
                    continue
                if self.pnl_dict[self.nb_trades_] < self.min_results:
                    continue
               # if self.pnl_dict[self.fitness_function] > self.fitness_level:
                #    return self.pnl_dict,self.op_param
                elif bool(self.pnl_dict) and self.pnl_dict[self.nb_trades_] >= self.min_results:
                    results_tempo.append(self.pnl_dict)
                    population_tempo.append(self.list_to_dict(self.op_param))
                    if (results_tempo[items_][self.nb_trades_] > 150):
                        raise Exception("Error with the number of trades")
                    items_+=1
            self.results_pop = results_tempo.copy()
            self.population = population_tempo.copy()

        return wrapper_

    def list_to_dict(self,list_):
        new_dict = {}
        for item in list_:
            if len(item) > 1:
                new_dict[item[1]] = item[0][item[1]]
            else:
                new_dict[item[0]] = getattr(self, item[0])

        return new_dict

    @iterate_population
    def create_chromosome(self):
        """ Function that creates initial 1 chromosome randomly for initial population. Each genes is set randomly"""

        for item in range(len(self.op_param)):
            if len(self.op_param[item]) > 1:
                self.op_param[item][0][self.op_param[item][1]] = \
                    np.random.choice(self.op_param[item][0][self.op_param[item][1]])
            else:
                setattr(self, self.op_param[item][0], np.random.choice(getattr(self, self.op_param[item][0])))

    def fitness_selection(func):
        """Decorator to select two new chromosomes for the next generations

        We truncate the Put the smallest performance evaluator to 0 and raise by some amount the others evaluators. It makes
        sure all values are equal or above 0. The function makes sure
        """

        def wrapper_(self):
            min_val = min(item[self.fitness_function] for item in self.results_pop)
            if min_val >= 0:
                min_val = 0
            self.fitt_total = 0
            for item in self.results_pop:
                item[self.fitness_function] -= min_val  # Truncated fitness function.
                self.fitt_total += item[self.fitness_function]

            if all(item[self.fitness_function] == 0 for item in self.results_pop): #if all sharpe ratio are the same
                                                                                    # at 0, it avoids mistake later
                for item in self.results_pop:
                    item[self.fitness_function]+=1

            def parent():

                nb_parent = 2
                parent_ = []
                parent_item = None
                for j in range(nb_parent):
                    item = 0
                    random_nb = self.fitt_total * random.random()
                    sum_results = 0
                    while( item < len(self.results_pop)):
                        sum_results += self.results_pop[item][self.fitness_function]
                        if random_nb <= sum_results:
                            if (parent_item is not None) and (parent_item == item):
                                random_nb = self.fitt_total * random.random()
                                sum_results = 0
                                item = 0
                                continue
                            else :
                                parent_.insert(item,self.population[item])
                                parent_item = item
                                break
                        item+=1

                if not bool(parent_):
                    raise Exception("Parent has no value")

                if len(parent_) != 2:
                    raise Exception("Don't have a father and mother")

                return parent_
            func(self, parent())

        return wrapper_

    def run_generations(self):
        """ Function that run generations"""
        for generation in range(self.generations):
            self.new_chromosomes()

    @iterate_population
    @fitness_selection
    def new_chromosomes(self, parent):
        """ Create a new chromosome in the new generation

        The function only keep one chromosome in `self.op_param` for evaluation
        """

        rand_number = random.random()
        if rand_number < self.mutation_rate:
            self.mutation(parent[0])

        elif rand_number < (self.mutation_rate + self.co_rate) :
            self.cross_over(parent[0],parent[1])

        else:
            self.assign_value(parent[0])

    def assign_value(self, parent):
        """ Function to assign the new value to each each gene in the chromosome
        """
        for item in range(len(self.op_param)):
            if len(self.op_param[item]) > 1:
                self.op_param[item][0][self.op_param[item][1]] = parent[self.op_param[item][1]]
            else:
                setattr(self, self.op_param[item][0], parent[self.op_param[item][0]])

    def mutation(self, parent):
        """ Function that mutate one gene of one parent

         It changes randomly the value of one gene with the possible in `initialize.py`"""
        item = random.randint(0,self.nb_genes -1 )
        if len(self.op_param[item]) > 1:
            while True:
                new_val = np.random.choice(self.op_param[item][0][self.op_param[item][1]])
                if parent[self.op_param[item][1]] != new_val:
                    parent[self.op_param[item][1]] = new_val
                    break
            self.assign_value(parent)  # assign father's value to new chromosome to be tested

        else:
            new_val = np.random.choice(getattr(self, self.op_param[item][0]))
            while True:
                new_val = np.random.choice(getattr(self, self.op_param[item][0]))
                if parent[self.op_param[item][0]] != new_val:
                    parent[self.op_param[item][0]] = new_val
                    break
            self.assign_value(parent)  # assign father's value to new chromosome to be tested


    def cross_over(self,father,mother):
        """ Function that cross-over one gene of one parent to the other parent"""

        item = random.randint(0,self.nb_genes -1 )
        if len(self.op_param[item]) > 1:

            father[self.op_param[item][1]] = mother[self.op_param[item][1]]
        else :

            father[self.op_param[item][0]] = mother[self.op_param[item][0]]
        self.assign_value(father) #assign father value to new chromosome to be tested

    def return_results(self):
        """Return the results of the best chromosome (1 chromosome)

        Return
        ------
        `self.pnl_dict` : dict
            pnl of the best chromosome

        `self.op_param` : list
            parameters of the best chromosome
        """

        for index, item in enumerate(self.results_pop):
            if index == 0:
                max_val = item[self.fitness_function]
                max_idx = index
            elif item[self.fitness_function] > max_val:
                max_val = item[self.fitness_function]
                max_idx = index


        return self.results_pop[max_idx], self.population[max_idx]