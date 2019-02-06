import time
start = time.time()

from queue import Queue
from copy import copy

class Node:
    solution = [] #type: list
    benefit = 0
    weight = 0
    current_benefit = 0
    current_weight = 0
    id = 0

    def __init__(self,solution,benefit,weight,current_benefit,current_weight,id):
        self.solution = solution
        self.benefit = benefit
        self.weight = weight
        self.current_benefit = current_benefit
        self.current_weight = current_weight
        self.id = id

class Solution:
    solution = [] #type: list
    final_benefit = 0
    final_weight = 0

    def __init__(self,solution, benefit, weight):
        self.solution = solution
        self.final_benefit = benefit
        self.final_weight = weight

solution = [] #type: list
benefit = 0
weight = 0
current_solution_bfs = Solution(solution, benefit, weight)
current_solution_dfs = Solution(solution, benefit, weight)

def read_file():
    input_file  = open("assignment1knapsack.txt", "r")
    input_file.readline()
    input_file.readline()
    input_file.readline()
    dimension_line = input_file.readline()
    dimension_sentence = dimension_line.split()
    dimension = int(dimension_sentence[1])
    # Dimension obtained.
    max_weight_line = input_file.readline()
    max_weight_sentence = max_weight_line.split()
    max_weight = int(max_weight_sentence[2])
    # Maximum weight obtained.
    input_file.readline()
    input_file.readline()
    items = [] #type: list
    while len(items) < dimension:
        item_line = input_file.readline()
        item_sentence = item_line.split()
        items.append([int(item_sentence[1]),int(item_sentence[2])])
        # Item obtained.
    # File read.
    return items, max_weight

# Knapsack by BFS function.

def knapsack_bfs():
    global current_solution_bfs
    items, max_weight = read_file()
    # I create the tree.
    empty_node_sol = [] #type: list
    while len(empty_node_sol) < len(items):
        empty_node_sol.append(-1)
    empty_node = Node(empty_node_sol, 0, 0, 0, 0, 0)
    queue = Queue(maxsize = 0)
    queue.put(empty_node)
    depth = len(items)
    while not queue.empty():
        node = queue.get()
        # I add the children to the tree.
        if not is_solution(node):
            for i in range (0, len(node.solution)):
                if node.solution[i] == -1:
                    depth = i
                    break
            if (node.current_weight+items[depth][1]) <= max_weight:
                if depth < len(items):
                    solution_0 = copy(node.solution)
                    solution_0[depth] = 0
                    child = Node(solution_0, items[depth][0], items[depth][1], node.current_benefit, node.current_weight, depth+1)
                    queue.put(child)
                    solution_1 = copy(node.solution)
                    solution_1[depth] = 1
                    child = Node(solution_1, items[depth][0], items[depth][1], node.current_benefit+items[depth][0], node.current_weight+items[depth][1], depth+1)
                    queue.put(child)
        #Is solution.
        if current_solution_bfs.final_benefit < node.current_benefit:
            current_solution_bfs.solution = node.solution
            current_solution_bfs.final_benefit = node.current_benefit
            current_solution_bfs.final_weight = node.current_weight
        """else:
            if current_solution_bfs.final_benefit == node.current_benefit:
                if current_solution_bfs.final_weight > node.current_weight:
                    current_solution_bfs.solution = node.solution
                    current_solution_bfs.final_benefit = node.current_benefit
                    current_solution_bfs.final_weight = node.current_weight"""
    # End for.

def is_solution(node):
    for i in range (0, len(node.solution)):
        if node.solution[i] == -1:
            return False
    return True

# Knapsack by DFS function.

def knapsack_dfs():
    global current_solution_dfs
    items, max_weight = read_file()
    # I create the tree.
    empty_node_sol = [] #type: list
    while len(empty_node_sol) < len(items):
        empty_node_sol.append(-1)
    empty_node = Node(empty_node_sol, 0, 0, 0, 0, 0)
    queue = Queue(maxsize = 0)
    queue.put(empty_node)
    depth = len(items)
    while not queue.empty():
        node = queue.get()
        # I add the children to the tree.
        if not is_solution(node):
            for i in range (0, len(node.solution)):
                if node.solution[i] == -1:
                    depth = i
                    break
            if (node.current_weight+items[depth][1]) <= max_weight:
                if depth < len(items):
                    solution_0 = copy(node.solution)
                    solution_0[depth] = 0
                    child = Node(solution_0, items[depth][0], items[depth][1], node.current_benefit, node.current_weight, depth+1)
                    queue.put(child)
                    solution_1 = copy(node.solution)
                    solution_1[depth] = 1
                    child = Node(solution_1, items[depth][0], items[depth][1], node.current_benefit+items[depth][0], node.current_weight+items[depth][1], depth+1)
                    queue.put(child)
        #Is solution.
        if current_solution_dfs.final_benefit < node.current_benefit:
            current_solution_dfs.solution = node.solution
            current_solution_dfs.final_benefit = node.current_benefit
            current_solution_dfs.final_weight = node.current_weight
        """else:
            if current_solution_dfs.final_benefit == node.current_benefit:
                if current_solution_dfs.final_weight > node.current_weight:
                    current_solution_dfs.solution = node.solution
                    current_solution_dfs.final_benefit = node.current_benefit
                    current_solution_dfs.final_weight = node.current_weight"""
    # End for.

# Main function.

print("BFS:")
knapsack_bfs()
# I change the array so it represents which nodes go into the knapsack.
solution2 = [] #type: list
sol = current_solution_bfs.solution
for i in range (0, len(sol)):   
    if sol[i] == 1:
        solution2.append(i+1)
# I print the solution.
print(solution2, current_solution_bfs.final_benefit, current_solution_bfs.final_weight)
print("DFS:")
knapsack_dfs()
# I change the array so it represents which nodes go into the knapsack.
solution3 = [] #type: list
sol_dfs = current_solution_dfs.solution
for i in range (0, len(sol_dfs)):   
    if sol_dfs[i] == 1:
        solution3.append(i+1)
# I print the solution.
print(solution3, current_solution_dfs.final_benefit, current_solution_dfs.final_weight)

print("Execution time:")
end = time.time()
print(end - start)