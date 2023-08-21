import numpy as np, pygame


objects = []


def to_vector(v):
    return np.array(v, dtype=np.float32)

def vector_to_int_tuple(vector):
    return tuple(np.array(vector, dtype=int))

def magnitude(vector):
    return np.linalg.norm(vector)

def normalize(vector):
    return vector / magnitude(vector)


class DebugLine:
    def __init__(self, start, end, lifetime_countdown=-1) -> None:
        self.start = to_vector(start)
        self.end = to_vector(end)
        self.lifetime_countdown = lifetime_countdown

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.line(surface, "yellow", vector_to_int_tuple(self.start), vector_to_int_tuple(self.end))
    
    def update(self):
        if self.lifetime_countdown > 0:
            self.lifetime_countdown -= 1
        if not self.lifetime_countdown:
            self.valid = False


def find_intercept_vector(launcher_position, launcher_velocity, target_position, target_velocity, projectile_speed):
    # simple version ignoring velocity
    # assert magnitude(launcher_velocity) == 0
    # assert magnitude(target_velocity) == 0

    
    relative_position = target_position - launcher_position
    relative_velocity = target_velocity - launcher_velocity

    
    target_approach_mag = np.dot(relative_velocity, normalize(relative_position))
    target_approach = normalize(relative_position) * target_approach_mag
    target_drift = relative_velocity - target_approach

    assert magnitude((target_approach + target_drift) - relative_velocity) < 0.000001

    # time = magnitude(relative_position) / projectile_speed

    # target_pos = relative_position + (200, 200)

    # l = DebugLine(target_pos, target_pos, 60 * 5)
    # l.end += target_approach * 20
    # objects.append(l)

    # l = DebugLine(target_pos, target_pos, 60 * 5)
    # l.end += target_drift * 20
    # objects.append(l)


    projectile_drift = target_drift
    projectile_drift_mag = magnitude(projectile_drift)
    projectile_approach_mag = np.sqrt(projectile_speed**2 + projectile_drift_mag**2)
    projectile_approach = normalize(relative_position) * projectile_approach_mag

    relative_approach_mag = projectile_approach_mag - target_approach_mag
    time = magnitude(relative_position) / relative_approach_mag


    # total_drift = target_drift * time
    
    # objects.append(DebugLine(target_position + total_drift, launcher_position + total_drift, 60 * 2))


    vector = projectile_drift + projectile_approach

    
    impact = launcher_position + vector*time
    objects.append(DebugLine(launcher_position, impact, np.ceil(time)))
    # objects.append(DebugLine(launcher_position, target_position, np.ceil(time)))
    # objects.append(DebugLine(target_position, impact, np.ceil(time)))




    # todo
    # vector = normalize(target_position - launcher_position) * projectile_speed
    # objects.append(DebugLine(target_position, launcher_position, np.ceil(time)))

    return vector


class Projectile:
    radius = 5

    def __init__(self, pos, vel, lifetime_countdown=-1) -> None:
        self.pos = to_vector(pos)
        self.vel = to_vector(vel)
        self.lifetime_countdown = lifetime_countdown

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.circle(surface, "green", vector_to_int_tuple(self.pos), self.radius)
    
    def update(self):
        self.pos += self.vel

        if self.lifetime_countdown > 0:
            self.lifetime_countdown -= 1
        if not self.lifetime_countdown:
            self.valid = False

        for o in objects:
            if isinstance(o, Target) and magnitude(o.pos - self.pos) <= self.radius + o.radius:
                self.valid = False

class Shooter:
    radius = 15

    projectile_speed = 5
    projectile_lifetime = 60 * 4
    shoot_reload = 60

    def __init__(self, pos) -> None:
        self.pos = to_vector(pos)

        self.reload_countdown = 0

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.circle(surface, "blue", vector_to_int_tuple(self.pos), self.radius)
    
    def update(self):
        if self.reload_countdown > 0:
            self.reload_countdown -= 1

        if not self.reload_countdown:
            for o in objects:
                if isinstance(o, Target):
                    self.shoot_at_target(o)
                    break

    def shoot_at_target(self, target):
        self.reload_countdown = self.shoot_reload

        p = Projectile(self.pos, find_intercept_vector(
            self.pos, to_vector((0, 0)), target.pos, target.vel, self.projectile_speed
        ), self.projectile_lifetime)
        objects.append(p)


class Target:
    radius = 10

    def __init__(self, pos, vel) -> None:
        self.pos = to_vector(pos)
        self.vel = to_vector(vel)

        self.valid = True
    
    def draw(self, surface):
        pygame.draw.circle(surface, "red", vector_to_int_tuple(self.pos), self.radius)
    
    def update(self):
        self.pos += self.vel

        if self.pos[0] <= 0 + 100:
            self.vel[0] = abs(self.vel[0])
        if self.pos[0] >= 1500 - 100:
            self.vel[0] = -abs(self.vel[0])