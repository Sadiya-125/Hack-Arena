import pygame
import random
import numpy as np
from simulation.enviroment import Environment
from simulation.agent import Agent
from ml_models.cnn_model import EvacuationCNN
from ml_models.training import train_model

class EvacuationSimulation:
    def __init__(self, num_agents=20):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Crowd Evacuation Simulation")
        
        self.environment = Environment()
        self.cnn_model = EvacuationCNN()
                                                                
        # Create agents
        self.agents = [
            Agent(random.randint(50, 200), 
                  random.randint(50, 550)) 
            for _ in range(num_agents)
        ]
    
    def get_agent_state(self, agent):
        # Create a dummy state for the CNN model based on the agent's position
        state = np.zeros((64, 64, 1), dtype=np.uint8)
        # Place the agent in the state
        x, y = agent.x // 10, agent.y // 10  # Scale down position for 64x64
        if 0 <= x < 64 and 0 <= y < 64:
            state[y, x] = 255  # Mark agent's position
        return state
    
    def check_evacuation(self, agent):
        return (agent.x, agent.y) == self.environment.exit_point
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Get state and make prediction for each agent
            for agent in self.agents:
                state = self.get_agent_state(agent)
                movement = self.cnn_model.predict_movement(state)
                agent.update_position(movement, self.environment)
                
                # Check if the agent has evacuated
                if self.check_evacuation(agent):
                    agent.evacuated = True
            
            # Clear screen and redraw everything
            self.screen.fill((255, 255, 255))  # White background
            self.environment.draw_obstacles(self.screen)
            
            for agent in self.agents:
                agent.draw(self.screen)
            
            pygame.draw.circle(self.screen, (0, 255, 0), self.environment.exit_point, 10)
            evacuated_count = sum(1 for agent in self.agents if agent.evacuated)
            font = pygame.font.SysFont(None, 36)
            evac_text = font.render(f"Evacuated: {evacuated_count}/{len(self.agents)}", True, (0, 0, 0))
            self.screen.blit(evac_text, (10, 10))
            
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

# Main execution
if __name__ == "__main__":
    train_model()
    simulation = EvacuationSimulation(num_agents=20)
    simulation.run()