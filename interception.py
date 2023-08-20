import numpy as np, pygame

def to_vector(v):
    return np.array(v, dtype=np.float32)

def vector_to_int_tuple(vector):
    return tuple(np.array(vector, dtype=int))

def magnitude(vector):
    return np.linalg.norm(vector)

def normalize(vector):
    return vector / magnitude(vector)

def find_intercept_vector(launcher_position, launcher_velocity, target_position, target_velocity, projectile_speed):
    # simple version ignoring velocity
    assert magnitude(launcher_velocity) == 0
    assert magnitude(target_velocity) == 0

    displacement = target_position - launcher_position

    vector = normalize(displacement) * projectile_speed

    return vector


class Projectile:
    radius = 5

    def __init__(self, pos, vel) -> None:
        self.pos = to_vector(pos)
        self.vel = to_vector(vel)

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.circle(surface, "yellow", vector_to_int_tuple(self.pos), self.radius)
    
    def update(self, objects):
        self.pos += self.vel

        for o in objects:
            if isinstance(o, Target) and magnitude(o.pos - self.pos) <= self.radius + o.radius:
                self.valid = False

class Shooter:
    radius = 15

    projectile_speed = 4
    shoot_reload = 60

    def __init__(self, pos) -> None:
        self.pos = to_vector(pos)

        self.reload_countdown = 0

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.circle(surface, "blue", vector_to_int_tuple(self.pos), self.radius)
    
    def update(self, objects):
        if not self.reload_countdown:
            for o in objects:
                if isinstance(o, Target):
                    self.shoot_at_target(objects, o)
                    break

    def shoot_at_target(self, objects, target):
        self.reload_countdown = self.shoot_reload
        objects.append(Projectile(self.pos, find_intercept_vector(
            self.pos, to_vector((0, 0)), target.pos, target.vel, self.projectile_speed
        )))

class Target:
    radius = 10

    def __init__(self, pos, vel) -> None:
        self.pos = to_vector(pos)
        self.vel = to_vector(vel)

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.circle(surface, "red", vector_to_int_tuple(self.pos), self.radius)
    
    def update(self, objects):
        self.pos += self.vel