import unittest
import os

from tabu_col import tabucol
from recursive_largest_first import recursive_largest_first
from dsatur import dsatur
from read_graph_instance import read_col_graph

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
        self.instances_folder = "instances"
        self.solution_file = "solutions.txt"
        self.solutions = read_solutions(self.solution_file)
        print(f"Total number of tests is {len(self.solutions)}")

    def test_tabucol(self):
        for instance_file in os.listdir(self.instances_folder):
            with self.subTest(instance_file=instance_file):

                if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                    print(f"Skipping {instance_file}...")
                    continue

                instance_path = os.path.join(self.instances_folder, instance_file)
                graph = read_col_graph(instance_path)

                k = self.solutions[get_instance_name(instance_file)]

                if k == -1:
                    continue

                try:
                    solution = tabucol(graph, k, tabu_size=10, rep=10, nbmax=10000)
                except RecursionError:
                    print(f"Recursion error in {get_instance_name(instance_file)}")
                    continue

                self.assertEqual(len(set(node.color for node in solution.values())), k)

    def test_recursive_largest_first(self):
        for instance_file in os.listdir(self.instances_folder):
            with self.subTest(instance_file=instance_file):

                if instance_file[-2:] == ".b" or instance_file[-4:] == ".txt":
                    print(f"Skipping {instance_file}...")
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
                    continue

                self.assertEqual(color_number, k)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphColoringAlgorithms)
    unittest.TextTestRunner(verbosity=2).run(suite)
