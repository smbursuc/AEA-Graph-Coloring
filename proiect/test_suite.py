import unittest
import os

from tabu_col import tabucol
from recursive_largest_first import recursive_largest_first
from dsatur import dsatur
from read_graph_instance import read_col_graph
import math

import sys
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

    def test_tabucol(self):
        for instance_file in os.listdir(self.instances_folder):
            with self.subTest(instance_file=instance_file):
                print(f"Currently running {instance_file}...")

                if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                    print(f"Skipping {instance_file}...\n")
                    self.skipped.append(instance_file)
                    continue

                instance_path = os.path.join(self.instances_folder, instance_file)
                graph = read_col_graph(instance_path)

                k = self.solutions[get_instance_name(instance_file)]

                if k == -1:
                    continue

                try:
                    solution = tabucol(graph, k, tabu_size=10, rep=10, nbmax=10000)
                except RecursionError:
                    print(f"Recursion error in {get_instance_name(instance_file)}\n")
                    self.withErrors.append(instance_file)
                    continue
                
                if solution is None:
                    print(f"Could not find a solution for {instance_file} in the maximum amount of iterations")
                    self.notPassed.append(instance_file)
                    self.assertEqual(solution, k)
                else:
                    self.passed.append(instance_file)
                
                print("\n")

    def test_recursive_largest_first(self):
        for instance_file in os.listdir(self.instances_folder):
            with self.subTest(instance_file=instance_file):

                if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                    print(f"Skipping {instance_file}...")
                    self.skipped.append(instance_file)
                    continue

                name = get_instance_name(instance_file)

                instance_path = os.path.join(self.instances_folder, instance_file)
                graph = read_col_graph(instance_path)

                k = self.solutions[get_instance_name(instance_file)]

                if k == -1:
                    continue
                try:
                    color_number = recursive_largest_first(graph)
                except RecursionError:
                    print(f"Recursion error in {name}")
                    self.withErrors.append(instance_file)
                    continue
                
                if (color_number != k):
                    self.assertEqual(color_number, k)
                else:
                    self.passed.append(instance_file)

    def test_dsatur(self):
        for instance_file in os.listdir(self.instances_folder):
            with self.subTest(instance_file=instance_file):

                if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                    print(f"Skipping {instance_file}...")
                    self.skipped.append(instance_file)
                    continue

                name = get_instance_name(instance_file)

                instance_path = os.path.join(self.instances_folder, instance_file)
                graph = read_col_graph(instance_path)

                k = self.solutions[get_instance_name(instance_file)]

                if k == -1:
                    continue
                try:
                    color_number = dsatur(graph)
                except RecursionError:
                    print(f"Recursion error in {name}")
                    self.withErrors.append(instance_file)
                    continue
                
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
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphColoringAlgorithms)
    unittest.TextTestRunner(verbosity=2).run(suite)
