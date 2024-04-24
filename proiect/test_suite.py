import unittest
import os
import time
import csv
from tabu_col import tabucol
from recursive_largest_first import recursive_largest_first
from dsatur import dsatur
from read_graph_instance import read_col_graph
import math
from new_heuristic import ant_col_with_local_search
import sys
from read_graph_instance import get_edges_vertexes
import argparse
sys.setrecursionlimit(1000)  # Set the recursion limit to a higher value, e.g., 5000

def get_instance_name(instance_file):
    index = instance_file.find('.col')
    return instance_file[:index]

def read_solutions(solution_file):
    with open(solution_file, "r") as file:
        lines = file.readlines()

    values = {}
    for line in lines:
        instance_name = get_instance_name(line)
        
        parts = line.split(' ')

        solution = parts[2]
        solution = solution.replace(',', '')
        if solution.isdigit():
            solution = int(solution)
        else:
            solution = -1
        
        values[instance_name] = solution

    # for key, value in values.items():
    #     print(key, value)

    return values

class TestGraphColoringAlgorithms(unittest.TestCase):
    def setUp(self):
        self.instances_folder = "instances_k"
        self.solution_file = "solutions.txt"
        self.solutions = read_solutions(self.solution_file)
        self.passed = []
        self.notPassed = []
        self.skipped = []
        self.withErrors = []
        self.testNr = len(os.listdir(self.instances_folder))
        print(f"Total number of tests is {self.testNr}")

    def run_single_algorithm(self):
        self.test_coloring_algorithm("ant_col_with_local_search")

    def run_tests(self):
        coloring_algs = ["dsatur", "recursive_largest_first", "tabucol", "ant_col_with_local_search"]
        for coloring_alg in coloring_algs:
            self.test_coloring_algorithm(coloring_alg)

    def test_coloring_algorithm(self, alg_name):
        with open(f"csv_output/{alg_name}_results.csv", 'w', newline='') as csvfile:
            fieldnames = ['Instance File', 'Number of Nodes', 'Number of Edges','Expected K','K','Execution Time','Solution found','Notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for instance_file in os.listdir(self.instances_folder):
                with self.subTest(instance_file=instance_file):
                    
                    print(f"Starting testing for {alg_name}...\n")
                    
                    # how do we read binary files?
                    if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                        self.skipped.append(instance_file)
                        continue



                    instance_path = os.path.join(self.instances_folder, instance_file)

                    print(f"Currently running {instance_file}...")

                    num_nodes, num_edges = get_edges_vertexes(instance_path)
                    name = get_instance_name(instance_file)
                    graph = read_col_graph(instance_path)


                    k = self.solutions[get_instance_name(instance_file)]

                    if k == -1:
                        continue
                    try:
                        
                        start_time = time.time()

                        color_number = 0
                        solution = None
                        meta_heurstic_check = False

                        if alg_name == "dsatur":
                            color_number = dsatur(graph)
                        
                        if alg_name == "recursive_largest_first":
                            color_number = recursive_largest_first(graph)
                        
                        if alg_name == "tabucol":
                            solution = tabucol(graph, k, tabu_size=10, rep=10, nbmax=10000)
                            meta_heurstic_check = True
                        
                        if alg_name == "ant_col_with_local_search":
                            solution = ant_col_with_local_search(graph, k, num_ants=10, evaporation_rate=0.1, iterations=100)
                            meta_heurstic_check = True

                        end_time = time.time()

                        execution_time_formatted = "{:.3f}".format(end_time - start_time)
                        print(f"Ended run with elapsed time: {execution_time_formatted}")

                        resulted_k = None
                        notes = None
                        if meta_heurstic_check:
                            # if antcol or tabucol was run but no solution was found mark it as failed
                            if solution is None:
                                isSolution = "False"
                                resulted_k = "Fail"
                                execution_time_formatted = "Fail"
                            else:
                                isSolution = "True"
                                resulted_k = k
                        else:
                            # these are for heuristic algorithms
                            isSolution = "True"
                            resulted_k = color_number
                        
                        writer.writerow({
                            fieldnames[0]:get_instance_name(instance_file),
                            fieldnames[1]:num_nodes,
                            fieldnames[2]:num_edges,
                            fieldnames[3]:k,
                            fieldnames[4]:resulted_k,
                            fieldnames[5]:execution_time_formatted,
                            fieldnames[6]:isSolution,
                            fieldnames[7]:notes
                        })
                    except RecursionError:
                        writer.writerow({
                            fieldnames[0]:get_instance_name(instance_file),
                            fieldnames[1]:num_nodes,
                            fieldnames[2]:num_edges,
                            fieldnames[3]:k,
                            fieldnames[4]:'Fail',
                            fieldnames[5]:'Fail',
                            fieldnames[6]:'False',
                            fieldnames[7]:'Recursion error'
                        })
                        print(f"Recursion error in {name}")
                        self.withErrors.append(instance_file)
                        continue
                    
                    # assert the result for console output
                    if (color_number != k):
                        self.assertEqual(color_number, k)
                    else:
                        self.passed.append(instance_file)

                

    def tearDown(self):
        print("\nTEST RECAP\n")
        for test in self.passed:
            print(f"The test {test} has passed.")
        print("\n")

        for test in self.skipped:
            print(f"The test {test} was skipped.")
        print("\n")

        for test in self.withErrors:
            print(f"The test {test} encountered an error.")
        print("\n")

        success_rate = math.floor(len(self.passed) / self.testNr * 100)
        print(f"Success rate is: {success_rate}%")
        
        # print("\n")

        # for test in self.notPassed:
        #     print(f"The test {test} has not passed.")


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphColoringAlgorithms)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    

