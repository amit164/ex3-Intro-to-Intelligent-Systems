# Amit Sharabai 323784298

# import customized_valid_actions
import random
import sys

from pddlsim.executors.executor import Executor
from pddlsim.local_simulator import LocalSimulator
from pddlsim.parser_independent import Literal, Disjunction, Conjunction

from data_structres import *

# read arguments
domain_path = sys.argv[1]
problem_path = sys.argv[2]


def get_current_goal(goal_option):
    if isinstance(goal_option, Literal):
        return goal_option.args
    goals_list = []
    for sub_goal in goal_option.parts:
        goals_list.append(get_current_goal(sub_goal))
        # return get_current_goal(sub_goal)
    return random.choice(goals_list)


def find_ball_place(state, ball):
    ball_places = state["at-ball"]
    ball_places = list(ball_places)
    for ball_place in ball_places:
        if ball_place[0] == ball:
            return ball_place[1]


def filter_options(options, filter):
    new_options = []
    for option in options:
        if option.find(filter) != -1:
            new_options.append(option)
    return new_options


class BehaviorExecutor(Executor):
    def __init__(self):
        super(BehaviorExecutor, self).__init__()
        self.graph = Graph()

    def create_graph(self, domain_name):
        if domain_name == "maze":
            states_list = {"north": 0.5, "east": 0.75, "west": 0.8, "south": 0.75}
        else:
            states_list = {"connected": 0.5}
        # add edges
        for state in self.services.parser.initial_state:
            if state in states_list:
                for edge in self.services.parser.initial_state[state]:
                    self.graph.addEdge(edge[0], edge[1])

    def initialize(self, services):
        self.services = services
        self.create_graph(self.services.parser.domain_name)

    def next_action(self):
        if self.services.goal_tracking.reached_all_goals():
            return None
        options = self.services.valid_actions.get()
        if len(options) == 0: return None
        if len(options) == 1: return options[0]
        if self.services.parser.domain_name == 'maze':
            return self.pick_best_maze_path(options)
        else:
            return self.pick_best_football_path(options)

    def pick_best_maze_path(self, options):
        moves = {"move-north": 0.5, "move-east": 0.25, "move-west": 0.2, "move-south": 0.25}
        min_w = sys.maxsize
        min_option = None
        for option in options:
            goal_tile = None
            player = option.split(" ")[1]
            # CHOOSE GOAL
            for goal in self.services.goal_tracking.uncompleted_goals:
                # CHECK IF PLAYER ON THIS OPTION IS RELEVANT TO THIS GOAL
                if self.is_relevant(goal, player):
                    goal_tile = get_current_goal(goal)[1]
                else:
                    continue
            if goal_tile is None:
                continue
            pred, dist = self.graph.bfs((option.split(" ")[3].split(")")[0]))
            path = self.graph.get_min_path(pred, goal_tile)
            weight = len(path) ** 2 * moves[option.split(" ")[0].split("(")[1]]
            if weight < min_w and weight != 0:
                min_w = weight
                min_option = option
        return min_option

    def is_relevant(self, goal, player):
        if isinstance(goal, Literal):
            if not self.services.parser.test_condition(goal, self.services.perception.get_state()):
                return goal.args[0] == player
            return False
        for sub_goal in goal.parts:
            if self.is_relevant(sub_goal, player):
                return True
        return False

    def pick_best_football_path(self, options):
        # CREATE A LIST OF RELEVANT BALLS TO GOAL
        relevant_balls = []
        for goal in self.services.goal_tracking.uncompleted_goals:
            sub_balls = self.find_balls(goal)
            if sub_balls is not None:
                relevant_balls.extend(sub_balls)
        # FIND DISTANCE BETWEEN THE CURRENT PLACE OF ROBOT AND ANY BALL WHILE FINDING THE CLOSEST
        min_dist = sys.maxsize
        robot_place = self.services.perception.get_state()["at-robby"]
        robot_place = list(robot_place)[0][0]
        for ball in relevant_balls:
            if ball is None:
                continue
            ball_place = find_ball_place(self.services.perception.get_state(), ball)
            # FIND DISTANCE BETWEEN THR ROBOT AND THE BALL
            pred, dist = self.graph.bfs(robot_place)
            path_to_ball = self.graph.get_min_path (pred, ball_place)
            if path_to_ball is None:
                pass
            goal_tile = self.find_goal_for_player(ball)
            # IF DISTANCE IS 1 => KICK THE BALL
            if len(path_to_ball) == 0:
                kick_options = filter_options(options, "kick")
                return self.find_best_kick(goal_tile, kick_options)
            # ELSE, CONTINUE CHECKING THE CLOSEST BALL
            # THE DISTANCE FORMULA IS = 0.5* (path to ball)^2 + 0.2 * (path to goal)^3
            pred, dist = self.graph.bfs(ball_place)
            path_to_goal = self.graph.get_min_path(pred, goal_tile)
            distance = 0.5*len(path_to_ball)**2 + 0.2 * len(path_to_goal)**3
            if distance < min_dist:
                min_dist = distance
                min_path = path_to_ball
        for option in options:
            move = "(move " + robot_place + " " + min_path[0] + ")"
            if option == move:
                return option
        return random.choice(options)

    def find_balls(self, goal):
        if isinstance(goal, Literal):
            if not self.services.parser.test_condition(goal, self.services.perception.get_state()):
                if goal.predicate == "at-ball":
                    return goal.args[0]
        all_balls = []
        if isinstance(goal, Disjunction) or isinstance(goal, Conjunction):
            for sub_goal in goal.parts:
                some_balls = self.find_balls(sub_goal)
                if isinstance(some_balls, list):
                    all_balls.extend(some_balls)
                else:
                    all_balls.append(some_balls)
            return all_balls

    def find_best_kick(self, goal_tile, options):
        min_w = sys.maxsize
        if goal_tile is None:
            random.choice(options)
        min_option = None
        for option in options:
            func = option.split(" ")[0].split("(")[1]
            if func == "move":
                optional_move = option.split(" ")[2].split(")")[0]
            else:
                optional_move = option.split(" ")[3]
            pred, dist = self.graph.bfs(optional_move)
            path = self.graph.get_min_path(pred, goal_tile)
            if len(path) < min_w and len(path) != 0:
                min_w = len(path)
                min_option = option
        if min_option is None:
            random.choice(options)
        return min_option

    def find_goal_for_player(self, min_ball):
        # CHOOSE GOAL
        for goal in self.services.goal_tracking.uncompleted_goals:
            # CHECK IF BALL RELEVANT TO THIS GOAL
            if self.is_relevant(goal, min_ball):
                return get_current_goal(goal)[1]


print LocalSimulator().run(domain_path, problem_path, BehaviorExecutor())
