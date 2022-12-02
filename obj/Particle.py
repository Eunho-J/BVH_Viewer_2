from abc import abstractmethod
from typing import List, Optional, Tuple
from typing_extensions import override
from attrdict import AttrDict

from np import *
import utils


class Particle:
    def __init__(self, 
                 mass:float = 1.0, 
                 position: np.ndarray = np.array([0,0,0,0], dtype=np.float32),
                 collision_enabled: bool = False
                 ) -> None:
        self.mass: float = mass
        self.position: np.ndarray = position
        self.velocity: np.ndarray = np.array([0,0,0,0], dtype=np.float32)
        self.force: np.ndarray = np.array([0,0,0,0], dtype=np.float32)
        self.pinned: bool = False
        self.collision_enabled: bool = collision_enabled
        
        self.position_prev: np.ndarray = position

    def pin(self):
        self.pinned = True

    def unpin(self):
        self.pinned = False
        
    def enable_collision(self):
        self.collision_enabled = True
        
    def disable_collision(self):
        self.collision_enabled = False

    def clear_force(self):
        self.force = np.zeros_like(self.force, dtype=np.float32)


class Particle_System:
    def __init__(self) -> None:
        self.particles: List[Particle] = []
        self.clock: float = 0.0
        self.forces: List[Force] = []
        self.colliders: List[Collider] = []

    def append_particle(self, particle:Particle) -> None:
        self.particles.append(particle)

    def remove_particle(self, particle:Particle) -> bool:
        if self.particles.count(particle):
            self.particles.remove(particle)
            return True
        else :
            return False

    def append_force(self, force) -> None:
        self.forces.append(force)

    def remove_force(self, force) -> bool:
        if self.forces.count(force):
            self.forces.remove(force)
            return True
        else :
            return False
        
    def append_collider(self, collider) -> None:
        self.colliders.append(collider)

    def remove_collider(self, collider) -> bool:
        if self.colliders.count(collider):
            self.colliders.remove(collider)
            return True
        else :
            return False

    def _clear_forces(self) -> None:
        for particle in self.particles:
            particle.clear_force()

    def _compute_forces(self) -> None:
        for force in self.forces:
            force.apply()
            
    def _compute_collisions(self) -> None:
        for particle in self.particles:
            if particle.collision_enabled:
                is_colliding = True
                while is_colliding:
                    
                    is_colliding = False
                    collider: Optional[Collider] = None
                    collision_point: Optional[np.ndarray] = None
                    distance_to_collision: float = 0.0
                    
                    for tmp_collider in self.colliders:
                        tmp_is_colliding, tmp_collision_point = tmp_collider.check_collision(particle)
                        if tmp_is_colliding:
                            tmp_distance_to_collision = utils.distance_of(particle.position_prev, tmp_collision_point)
                            if not is_colliding or distance_to_collision >= tmp_distance_to_collision:
                                is_colliding = tmp_is_colliding
                                collider = tmp_collider
                                collision_point = tmp_collision_point
                                distance_to_collision = tmp_distance_to_collision
                                
                    if is_colliding:
                        collider.apply_collision(particle, collision_point)

    def euler_step(self, dt:float) -> None:
        dt = dt / 1000
        self._clear_forces()
        self._compute_forces()
        # get state
        v_list = [ particle.velocity for particle in self.particles ]
        a_list = [ particle.force / particle.mass for particle in self.particles ]
        # scale vector with dt
        dx_list = [ v * dt for v in v_list ]
        dv_list = [ a * dt for a in a_list ]
        # update state
        for i, particle in enumerate(self.particles):
            if particle.pinned:
                continue
            #update position
            particle.position_prev = particle.position.copy()
            particle.position += dx_list[i]
            #update velocity
            particle.velocity += dv_list[i]
        
        self._compute_collisions()
        self.clock += dt
        
    def semi_implicit_euler_step(self, dt:float) -> None:
        dt = dt / 1000
        #get initial state
        v_init_list = [ particle.velocity.copy() for particle in self.particles ]
        x_init_list = [ particle.position.copy() for particle in self.particles ]
        
        self._clear_forces()
        self._compute_forces()
        # get state
        v_list = [ particle.velocity for particle in self.particles ]
        a_list = [ particle.force / particle.mass for particle in self.particles ]
        # scale vector with dt
        dx_list = [ v * dt for v in v_list ]
        dv_list = [ a * dt for a in a_list ]
        # update state
        for i, particle in enumerate(self.particles):
            if particle.pinned:
                continue
            #update position
            particle.position += dx_list[i]
            #update velocity
            particle.velocity += dv_list[i]
        
        self._clear_forces()
        self._compute_forces()
        # get state
        v_list = [ particle.velocity for particle in self.particles ]
        a_list = [ particle.force / particle.mass for particle in self.particles ]
        # scale vector with dt
        dx_list = [ v * dt for v in v_list ]
        dv_list = [ a * dt for a in a_list ]
        # reset state to initial and update
        for i, particle in enumerate(self.particles):
            if particle.pinned:
                continue
            particle.position = x_init_list[i]
            particle.velocity = v_init_list[i]
            #update position
            particle.position_prev = particle.position.copy()
            particle.position += dx_list[i]
            #update velocity
            particle.velocity += dv_list[i]
        
        self._compute_collisions()
        self.clock += dt
        
        
#--------------------Forces------------------
ForceType = AttrDict({
    'gravity': 0,
    'drag': 1,
    'damped_spring': 2,
})

class Force:
    def __init__(self, force_type:int, p:Particle, system:Particle_System) -> None:
        self.p: Particle = p
        self.system: Particle_System = system
        self.force_type: int = force_type
        
    @abstractmethod
    def apply(self):
        pass


class Drag_Force(Force):
    def __init__(self, p: Particle, system: Particle_System, k:float) -> None:
        super().__init__(ForceType.drag, p, system)
        self.k: float = k

    @override
    def apply(self):
        self.p.force -= self.k * self.p.velocity


class Damped_Spring_Force(Force):
    def __init__(self, p: Particle, system: Particle_System, p2: Particle,
                    ks: float, kd: float, r:float = 0) -> None:
        super().__init__(ForceType.damped_spring, p, system)
        self.p2: Particle = p2
        self.ks: float = ks
        self.kd: float = kd
        self.r: float = r
        if self.r <= 0:
            self.r = utils.distance_of(p.position, p2.position)

    @override
    def apply(self):
        current_distance = utils.distance_of(self.p.position, self.p2.position)
        dv = self.p2.velocity - self.p.velocity
        dx = self.p2.position - self.p.position
        dx_unit = utils.numpy_get_unit(dx)
        
        f = self.ks * (current_distance - self.r) * dx_unit + \
            self.kd * utils.decompose_by(dv, dx)

        self.p.force += f
        self.p2.force -= f
        
class Gravity_Force(Force):
    def __init__(self, p: Particle, system: Particle_System, g: float = 9.8) -> None:
        super().__init__(ForceType.gravity, p, system)
        self.g: float = g
        self.direction_unit = np.array([0,-1,0,0], dtype=np.float32)

    @override
    def apply(self):
        self.p.force += self.p.mass * self.g * self.direction_unit



#-----------------Collider-------------------

class Collider:
    def __init__(self, k: float = 1.0, myu: float = 0.0) -> None:
        self.k: float = k
        self.eps: float = 0.00000001
        self.myu: float = myu
    
    @abstractmethod
    def apply_collision(self, particle: Particle, collision_point: np.ndarray):
        pass
    
    @abstractmethod
    def check_collision(self, particle: Particle) -> Tuple[bool, Optional[np.ndarray]]:
        pass
    
    @abstractmethod
    def apply_contact(self, particle: Particle):
        pass

    @abstractmethod
    def check_contact(self, particle: Particle):
        pass
    
    
class Infinite_Plane_Collider(Collider):
    def __init__(self, 
                 normal_vector: np.ndarray = np.array([0,1,0,0], dtype=np.float32),
                 passing_point: np.ndarray = np.array([0,0,0,1], dtype=np.float32),
                 k: float = 1.0,
                 myu: float = 0.0
                ) -> None:
        super().__init__(k, myu)
        self.norm: np.ndarray = utils.numpy_get_unit(normal_vector)
        self.passpoint: np.ndarray = passing_point
        
    @override
    def apply_collision(self, particle: Particle, collision_point: np.ndarray):
        
        assert collision_point is not None
        
        decomposed_movement = utils.decompose_by(particle.position - collision_point, self.norm)
        decomposed_velocity = utils.decompose_by(particle.velocity, self.norm)
    
        # particle.position_prev = collision_point
        
        particle.position -= (1 + self.k) * decomposed_movement
        particle.velocity -= (1 + self.k) * decomposed_velocity
        
    @override
    def check_collision(self, particle: Particle) -> Tuple[bool, Optional[np.ndarray]]:
        line_vector: np.ndarray = particle.position - particle.position_prev
        collision_point: Optional[np.ndarray] = None
        
        line_dot = np.dot(line_vector, self.norm)
        
        if line_dot != 0:
            t = np.dot((self.passpoint - particle.position_prev), self.norm) / line_dot
            
            if 0 < t <= 1:
                collision_point = line_vector * t + particle.position_prev
                    
                return True, collision_point
        return False, collision_point
    
    @override
    def apply_contact(self, particle: Particle):
        pass
    
    @override
    def check_contact(self, particle: Particle):
        pass
    
    
class Triangle_Plane_Collider(Collider):
    def __init__(self,
                 vertex1: np.ndarray,
                 vertex2: np.ndarray,
                 vertex3: np.ndarray,
                 k: float = 1.0
                ) -> None:
        super().__init__(k)