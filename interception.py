import pygame
import numpy as np

def magnitude(vector):
    return np.linalg.norm(vector)

def normalize(vector):
    return vector / magnitude(vector)

def find_intercept_vector(launcher_position, launcher_velocity, target_position, target_velocity, projectile_speed):
    # simple version ignoring velocity
    assert magnitude(launcher_velocity) == 0
    assert magnitude(target_velocity) == 0

    displacement = target_position - launcher_position

    vector = normalize(vector) * projectile_speed

    return vector


class Projectile:
    def __init__(self, pos, vel) -> None:
        self.pos = np.array(pos)
        self.vel = np.array(vel)
    
    def draw(self, surface):
        pygame.draw.circle(surface, "yellow", np.array(self.pos), 5)

class Shooter:
    shoot_speed = 1
    shoot_reload = 60

    def __init__(self, pos) -> None:
        self.pos = np.array(pos)
    
    def draw(self, surface):
        pygame.draw.circle(surface, "blue", np.array(self.pos), 15)
    
    def update(self, objects):
        pass

    def get_shot(self, target):
        return Projectile(self.pos, find_intercept_vector(
            self.pos, np.array((0, 0)), target.pos, target.vel
        ))

class Target:
    def __init__(self, pos, vel) -> None:
        self.pos = np.array(pos)
        self.vel = np.array(vel)
    
    def draw(self, surface):
        pygame.draw.circle(surface, "red", np.array(self.pos), 10)