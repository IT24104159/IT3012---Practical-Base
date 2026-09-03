in lab 1

in lab 02
1. Add agent_dir in __init__:
Locate __init__ inside VisualGridHuntGame and add a default direction variable:
        # Place this inside VisualGridHuntGame.__init__() right after self.agent_pos = [0, 0]
        self.agent_dir = 'Up'  # Tracks the direction the agent is currently facing
2. Update direction in execute_action:
At the top of execute_action(self, action: str), track the direction:

        Python
        # Place at the start of execute_action() in VisualGridHuntGame
        self.agent_dir = action  # Update facing direction

3. Replace get_percept:
Replace the existing get_percept method in VisualGridHuntGame with local sensory logic:

   def get_percept(self) -> dict:
    """Returns local sensory booleans instead of global position coordinates."""
    x, y = self.agent_pos

    # Calculate the adjacent coordinate directly ahead based on current direction
    next_x, next_y = x, y
    if self.agent_dir == 'Up':
        next_y = min(self.height - 1, y + 1)
    elif self.agent_dir == 'Down':
        next_y = max(0, y - 1)
    elif self.agent_dir == 'Left':
        next_x = max(0, x - 1)
    elif self.agent_dir == 'Right':
        next_x = min(self.width - 1, x + 1)

    # Check if the tile ahead is a wall or boundary boundary limit
    wall_ahead = (next_x, next_y) in self.walls or (next_x == x and next_y == y and action_would_hit_boundary(self, self.agent_dir))
    
    # Check simple boundary block
    if self.agent_dir == 'Up' and y == self.height - 1:
        wall_ahead = True
    elif self.agent_dir == 'Down' and y == 0:
        wall_ahead = True
    elif self.agent_dir == 'Left' and x == 0:
        wall_ahead = True
    elif self.agent_dir == 'Right' and x == self.width - 1:
        wall_ahead = True

    return {
        'wall_ahead': wall_ahead or ((next_x, next_y) in self.walls),
        'food_here': tuple(self.agent_pos) in self.food_positions,
        'smells_toxin': tuple(self.agent_pos) in self.toxic_traps,
        'score': self.score
    }

4. Creating SimpleReflexAgent in agent.py

5. Creating ModelBasedAgent in agent.py

6. Import your agent classes at the top of visual_grid_game.py:

        Python
        from agent import SimpleReflexAgent, ModelBasedAgent
7. Inside GridGameGUI.__init__(), initialize your active agent:

     # Add inside GridGameGUI.__init__()
    self.agent = ModelBasedAgent()  # Swap with SimpleReflexAgent() to test both