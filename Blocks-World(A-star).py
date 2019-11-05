import copy
from colorama import init
from termcolor import colored
from itertools import permutations, combinations
init()


def build_dict(config):
    down_dict = {}
    for stack in config:
        for h, block in enumerate(stack):
            if h == 0:
                down_dict[block] = "_"
            else:
                down_dict[block] = stack[h - 1]

    together_dict = {}
    blocks = [block for stack in config for block in stack]
    blocks.sort()
    block_combinations = tuple(combinations(blocks, 2))
    index_dict = {block: i for i, s in enumerate(config) for block in s}
    for combination in block_combinations:
        if index_dict[combination[0]] == index_dict[combination[1]]:
            together_dict[combination] = 1
        else:
            together_dict[combination] = 0
    return down_dict, together_dict


def search_in_list(input_list, element):
    for e in input_list:
        if e == element:
            return True
    return False


class Instance:
    def __init__(self, config, prev_instance=None, last_move=None):
        self.config = config
        self.down_dict, self.together_dict = build_dict(self.config)
        self.last_move = last_move
        if prev_instance:
            self.prev_instance = prev_instance
            self.g = prev_instance.g+1
        else:
            self.g = 0
            self.prev_instance = None
        self.h = self.get_heuristic()
        self.f = self.g + self.h

    def __str__(self):
        global no_of_blocks
        tbp = ""
        for i in range(no_of_blocks-1, -1, -1):
            for j, stack in enumerate(self.config):
                if len(stack) > i+1:
                    tbp += stack[i] + "  "
                elif len(stack) == i+1:
                    if j == self.last_move:
                        tbp += colored(stack[i], "red") + "  "
                    else:
                        tbp += stack[i] + "  "
                else:
                    tbp += "   "
            tbp += "\n"
        tbp += "_"*7
        return tbp

    def __eq__(self, other):
        return self.config == other.config

    def is_goal(self):
        global goal_down_dict
        return self.down_dict == goal_down_dict

    def get_stack_tops(self):
        return {s[-1]: i for i, s in enumerate(self.config) if len(s) > 0}

    def get_heuristic(self):
        global goal_down_dict, goal_together_dict
        h = 0
        for key in goal_down_dict.keys():
            if not self.down_dict[key] == goal_down_dict[key]:
                h += 1
        for key in self.together_dict.keys():
            if not self.together_dict[key] == goal_together_dict[key]:
                h += 1
        return h

    def get_possible_moves(self):
        tops = self.get_stack_tops()
        filled_stacks = list(tops.values())
        all_stacks = list(range(no_of_stacks))
        all_moves = list(permutations(all_stacks, 2))
        possible_moves = [move for move in all_moves if move[0] in filled_stacks and move[0] != self.last_move]
        return possible_moves

    def move(self, ithun, tithe):
        new_config = copy.deepcopy(self.config)
        new_config[tithe].append(new_config[ithun].pop())
        return new_config

    def get_possible_next_instances(self):
        possible_moves = self.get_possible_moves()
        instances = [Instance(self.move(move[0], move[1]), prev_instance=self, last_move=move[1]) for move in possible_moves]
        return instances

    def print_trace(self):
        previous_instances = [self]
        current_instance = self
        while current_instance.prev_instance is not None:
            previous_instances.append(current_instance.prev_instance)
            current_instance = current_instance.prev_instance
        previous_instances.reverse()
        for instance in previous_instances:
            print(instance)
            print("g : " + str(instance.g))
            print("h : " + str(instance.h))
            print("f : " + str(instance.f))
            print(colored("="*10, "cyan"))


no_of_blocks = 4
no_of_stacks = 3
init_config = [["A", "B", "C", "D"],
              [],
              []]
goal_config = [["A"],
              ["B", "C", "D"],
              []]
goal_down_dict, goal_together_dict = build_dict(goal_config)
open_list = []
closed_list = []

init_instance = Instance(init_config)

open_list.append(init_instance)

while len(open_list) > 0:
    instance = min(open_list, key=lambda i: i.f)
    if instance.is_goal():
        print("Done!!!\n")
        instance.print_trace()
        print(f"\nTotal configs visited : {len(closed_list)}")
        print(f"Total configs explored : {len(open_list)}")
        print(len(closed_list) + len(open_list))
        break
    open_list.remove(instance)
    closed_list.append(instance)
    next_instances = instance.get_possible_next_instances()
    new_instances = [instance for instance in next_instances if not search_in_list(closed_list, instance)]
    open_list.extend(next_instances)
    # print("Closed :")
    # for e in closed_list:
    #     print(e)
    #     print("g : " + str(e.g))
    #     print("h : " + str(e.h))
    #     print("f : " + str(e.f))
    # print("new_instances :")
    # for e in new_instances:
    #     print(e)
    #     print("h : " + str(e.h))
    if len(open_list) == 0:
        print("Bummer!!!")
