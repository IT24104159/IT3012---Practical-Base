class SearchAgent:
    def __init__(self):
        self.path = []
        self.last_goal = None

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        open_set = []
        reached_states = set()

        g_cost = 0
        if heuristic_type == 'manhattan':
            h_cost = self.manhattan_distance(start_pos, goal_pos)
        elif heuristic_type == 'euclidean':
            h_cost = self.euclidean_distance(start_pos, goal_pos)
        else:
            h_cost = 0

        f_cost = g_cost + h_cost
        heapq.heappush(open_set, (f_cost, g_cost, start_pos, []))

        while open_set:
            f_cost, g_cost, current_pos, path = heapq.heappop(open_set)

            if current_pos == goal_pos:
                return path

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            directions = [
                ((-1, 0), 'Up'),
                ((1, 0), 'Down'),
                ((0, -1), 'Left'),
                ((0, 1), 'Right')
            ]

            for (dx, dy), action in directions:
                neighbor = (current_pos[0] + dx, current_pos[1] + dy)
                nx, ny = neighbor

                if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1]:
                    if neighbor not in walls and neighbor not in reached_states:
                        g_new = g_cost + 1

                        if heuristic_type == 'manhattan':
                            h_new = self.manhattan_distance(neighbor, goal_pos)
                        elif heuristic_type == 'euclidean':
                            h_new = self.euclidean_distance(neighbor, goal_pos)
                        else:
                            h_new = 0

                        f_new = g_new + h_new
                        heapq.heappush(open_set, (f_new, g_new, neighbor, path + [action]))

        return []

    def sense_and_act(self, percept: dict) -> str:
        """Calculates the A* path to the target food and returns the next move."""
        current_pos = percept['agent_pos']
        goal_pos = percept['food_pos']
        walls = percept.get('walls', set())
        grid_size = percept.get('grid_size', (10, 10))

        # Replan path if target food moves or path is empty
        if self.last_goal != goal_pos:
            self.path = []
            self.last_goal = goal_pos

        if not self.path:
            self.path = self.astar_search(
                start_pos=current_pos,
                goal_pos=goal_pos,
                walls=walls,
                grid_size=grid_size,
                heuristic_type='manhattan'
            )

        # Return next step in sequence
        if self.path:
            return self.path.pop(0)

        return None