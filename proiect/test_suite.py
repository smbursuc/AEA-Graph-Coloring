import unittest
import os
import time
import datetime
import csv
from tabucol import tabucol
from recursive_largest_first import recursive_largest_first
from dsatur import dsatur
from read_graph_instance import read_col_graph
import math
from new_heuristic import ant_col_with_local_search
import sys
from read_graph_instance import get_edges_vertexes
import argparse
from graph_helper import read_graph
import read_graph_instance
from numbers import Number
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
        self.test_coloring_algorithm("tabucol")

    def run_tests(self):
        coloring_algs = ["dsatur", "recursive_largest_first", "tabucol", "ant_col_with_local_search"]
        for coloring_alg in coloring_algs:
            self.test_coloring_algorithm(coloring_alg)

    def test_coloring_algorithm(self, alg_name):
        write_to_csv = True
        now = str(datetime.datetime.now())
        timestamp = now.replace('.','').replace(':','')
        
        fieldnames = ['Instance File', 'Number of Nodes', 'Number of Edges','Expected K','K','Execution Time','Solution found','Notes',"Iterations"]
        
        with open(f"{alg_name}_results/{alg_name}_results_{timestamp}.csv", 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for instance_file in os.listdir(self.instances_folder):
                test_cols = {}
                avg_fields = ['K','Execution Time','Solution found','Notes']

                for field in avg_fields:
                    test_cols.setdefault(field, [])

                test_nr = 10
                for i in range(test_nr):
                    with self.subTest(instance_file=instance_file):

                        # if not (instance_file == "david.col"):
                        #     continue
                        
                        print(f"Starting testing for {alg_name} number {i}...\n")
                        
                        # how do we read binary files?
                        if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                            self.skipped.append(instance_file)
                            continue



                        instance_path = os.path.join(self.instances_folder, instance_file)

                        print(f"Currently running {instance_file}...")

                        num_nodes, num_edges = get_edges_vertexes(instance_path)
                        name = get_instance_name(instance_file)
                        nodes, edges, colors, adjacency_matrix, color_matrix = read_graph(instance_path)


                        k = self.solutions[get_instance_name(instance_file)]

                        if k == -1:
                            continue
                        try:
                            
                            start_time = time.time()

                            color_number = 0
                            solution = None
                            meta_heurstic_check = False

                            if alg_name == "dsatur":
                                color_number = dsatur(adjacency_matrix, color_matrix)
                            
                            if alg_name == "recursive_largest_first":
                                color_number = recursive_largest_first(adjacency_matrix, color_matrix)
                            
                            if alg_name == "tabucol":
                                tabu_size = 7
                                rep = len(adjacency_matrix) // 2
                                nbmax = 10000
                                solution = tabucol(adjacency_matrix, k, tabu_size, rep, nbmax)
                                if solution != None:
                                    color_number = k
                                meta_heurstic_check = True
                            
                            if alg_name == "ant_col_with_local_search":
                                graph = read_graph_instance.read_col_graph("instances_k/" + instance_file)
                                solution = ant_col_with_local_search(graph, k, num_ants=10, evaporation_rate=0.1, iterations=100)
                                if solution != None:
                                    color_number = k
                                meta_heurstic_check = True

                            end_time = time.time()

                            execution_time_formatted = "{:.3f}".format(end_time - start_time)
                            print(f"Ended run with elapsed time: {execution_time_formatted}")

                            notes = None
                            if meta_heurstic_check:
                                # if antcol or tabucol was run but no solution was found mark it as failed
                                if solution is None:
                                    isSolution = "False"
                                    execution_time_formatted = "Fail"
                                    self.notPassed.append(instance_file)
                                elif solution == "timeout":
                                    isSolution = "False"
                                    execution_time_formatted = -1
                                    self.notPassed.append(instance_file)
                                else:
                                    isSolution = "True"
                                    self.passed.append(instance_file)
                            else:
                                if color_number == k:
                                    isSolution = "True"
                                else:
                                    isSolution = "False"


                            test_cols.setdefault(fieldnames[0], get_instance_name(instance_file))
                            test_cols.setdefault(fieldnames[1], num_nodes)
                            test_cols.setdefault(fieldnames[2], num_edges)
                            test_cols.setdefault(fieldnames[3], k)
                            test_cols[fieldnames[4]].append(color_number)
                            test_cols[fieldnames[5]].append(float(execution_time_formatted))
                            test_cols[fieldnames[6]].append(isSolution)
                            test_cols[fieldnames[7]].append(notes)
                            test_cols.setdefault(fieldnames[8], test_nr)

                            # if (execution_time_formatted == -1):
                            #     break

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
                        # if (color_number != k):
                        #     self.notPassed.append(instance_file)
                        #     self.assertEqual(color_number, k)
                        # else:
                        #     self.passed.append(instance_file)

                if write_to_csv and instance_file not in self.skipped:
                    notes_list = set(test_cols["Notes"])
                    notes_res = [x for x in notes_list if x != None]
                    if len(notes_res) > 0:
                        notes_res = notes_res[0]
                    else:
                        notes_res = None
                    
                    sol_f = sum([1 for x in test_cols["Solution found"] if x == "True"]) / len(test_cols["Solution found"])
                    if sol_f == 1:
                        sol_f = "True"
                    
                    if sol_f == 0:
                        sol_f = "False"

                    exec_t = [x for x in test_cols["Execution Time"] if x == -1]
                    if (len(exec_t) > 0):
                        exec_t = "Timeout"
                    else:
                        exec_t = sum(test_cols["Execution Time"]) / len(test_cols["Execution Time"])

                    # k_res = [x for x in test_cols["K"] if isinstance(x, Number)] / len(test_cols["K"])

                    writer.writerow({
                        fieldnames[0]:test_cols[fieldnames[0]],
                        fieldnames[1]:test_cols[fieldnames[1]],
                        fieldnames[2]:test_cols[fieldnames[2]],
                        fieldnames[3]:test_cols[fieldnames[3]],
                        fieldnames[4]:sum(test_cols["K"]) / len(test_cols["K"]),
                        fieldnames[5]:exec_t,
                        fieldnames[6]:sol_f,
                        fieldnames[7]:notes_res,
                        fieldnames[8]:test_nr
                    })
                

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

        for test in self.notPassed:
            print(f"The test {test} has not passed.")

        success_rate = math.floor(len(self.passed) / (self.testNr - len(self.skipped)) * 100)
        print(f"Success rate is: {success_rate}%")
        
        # print("\n")

        # for test in self.notPassed:
        #     print(f"The test {test} has not passed.")


if __name__ == '__main__':
    # unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphColoringAlgorithms)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestSuite()
    suite.addTest(TestGraphColoringAlgorithms("run_single_algorithm"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    

