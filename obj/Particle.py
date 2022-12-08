from abc import abstractmethod
from typing import List, Optional, Tuple
from typing_extensions import override
from attrdict import AttrDict

from np import *
import utils


class Particle:
    def __init__(self, 
                 mass:float = 1.0, 
                 position: np.ndarray = np.array([0,0,0,0], dtype=np.float64),
                 collision_enabled: bool = False,
                 pinned: bool = False
                 ) -> None:
        self.mass: float = mass
        self.position: np.ndarray = position
        self.velocity: np.ndarray = np.array([0,0,0,0], dtype=np.float64)
        self.force: np.ndarray = np.array([0,0,0,0], dtype=np.float64)
        self.pinned: bool = pinned
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
        self.force = np.zeros_like(self.force, dtype=np.float64)
        
    def overwrite(self, mass, position, collision, pinned):
        self.mass = mass
        self.position = position
        self.position_prev = position.copy()
        self.pinned = pinned
        self.collision_enabled = collision
        
        self.velocity = np.zeros_like(self.velocity)
        self.force = np.zeros_like(self.force)


class Particle_System:
    def __init__(self) -> None:
        self.particles: List[Particle] = []
        self.clock: float = 0.0
        self.forces: List[Force] = []
        self.colliders: List[Collider] = []
        
        self.append_force(Gravity_Force(None, self))

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

        # update state
        for i, particle in enumerate(self.particles):
            if particle.pinned:
                continue
            

            #update position
            particle.position_prev = particle.position.copy()
            particle.position += particle.velocity * dt
            
            for collider in self.colliders:
                if collider.check_contact(particle, dt):
                    collider.apply_contact(particle, dt)
            #update velocity
            particle.velocity += particle.force * dt / particle.mass
        
        self._compute_collisions()
        self.clock += dt
        
    def semi_implicit_euler_step(self, dt:float) -> None:
        dt = dt / 1000
        self._clear_forces()
        self._compute_forces()
        
        # update state
        for i, particle in enumerate(self.particles):
            if particle.pinned:
                continue
            
            for collider in self.colliders:
                if collider.check_contact(particle, dt):
                    collider.apply_contact(particle, dt)
                    
            particle.velocity += particle.force * dt / particle.mass
            particle.position_prev = particle.position.copy()
            particle.position += particle.velocity * dt
        
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
                    ks: float, kd: float, r: Optional[float] = None) -> None:
        super().__init__(ForceType.damped_spring, p, system)
        self.p2: Particle = p2
        self.ks: float = ks
        self.kd: float = kd
        self.r: float = r
        if self.r is None:
            self.r = utils.distance_of(p.position, p2.position)

    @override
    def apply(self):
        current_distance = utils.distance_of(self.p.position, self.p2.position)
        dv = self.p2.velocity - self.p.velocity
        dx = self.p2.position - self.p.position
        dx_unit = utils.numpy_get_unit(dx)
        
        dv_size = np.linalg.norm(utils.decompose_by(dv,dx))
        
        f = self.ks * (current_distance - self.r) * dx_unit + self.kd * utils.decompose_by(dv, dx)

        self.p.force += f
        self.p2.force -= f
        
class Gravity_Force(Force):
    def __init__(self, p: Particle, system: Particle_System, g: float = 9.8) -> None:
        super().__init__(ForceType.gravity, p, system)
        self.g: float = g
        self.direction_unit = np.array([0,-1,0,0], dtype=np.float64)

    @override
    def apply(self):
        for particle in self.system.particles:
            particle.force += particle.mass * self.g * self.direction_unit
        # self.p.force += self.p.mass * self.g * self.direction_unit



#-----------------Collider-------------------

class Collider:
    def __init__(self, k: float = 1.0, myu: float = 0.0, collision_enabled: bool = True, contact_enabled: bool = True) -> None:
        self.k: float = k
        self.eps: float = 0.002
        self.myu: float = myu
        self.collision_enabled = collision_enabled
        self.contact_enabled = contact_enabled
    
    @abstractmethod
    def apply_collision(self, particle: Particle, collision_point: np.ndarray):
        pass
    
    @abstractmethod
    def check_collision(self, particle: Particle) -> Tuple[bool, Optional[np.ndarray]]:
        pass
    
    @abstractmethod
    def apply_contact(self, particle: Particle, dt: float):
        pass

    @abstractmethod
    def check_contact(self, particle: Particle, dt: float) -> bool:
        pass
    
    
class Infinite_Plane_Collider(Collider):
    def __init__(self, 
                normal_vector: np.ndarray = np.array([0,1,0,0], dtype=np.float64),
                passing_point: np.ndarray = np.array([0,0,0,1], dtype=np.float64),
                k: float = 1.0,
                myu: float = 0.0,
                collision_enabled: bool = True,
                contact_enabled: bool = True
                ) -> None:
        super().__init__(k, myu, collision_enabled, contact_enabled)
        self.norm: np.ndarray = utils.numpy_get_unit(normal_vector)
        self.passpoint: np.ndarray = passing_point
        
    @override
    def apply_collision(self, particle: Particle, collision_point: np.ndarray):
        
        assert collision_point is not None
        
        decomposed_movement = utils.decompose_by(particle.position - collision_point, self.norm)
        decomposed_velocity = utils.decompose_by(particle.velocity, self.norm)
    
        particle.position_prev = collision_point - self.eps * decomposed_movement
        
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
    def apply_contact(self, particle: Particle, dt: float):
        # apply contact force
        down_force = utils.decompose_by(particle.force, self.norm)
        passpoint_to_particle = particle.position - self.passpoint
        up_direction = utils.decompose_by(passpoint_to_particle, self.norm)

        parallel_force = particle.force - down_force

        down_velocity = utils.decompose_by(particle.velocity, self.norm)
        parallel_velocity = particle.velocity - down_velocity

        if np.dot(down_force, up_direction) < 0: 
            # means down_force is actually down directing

            if np.linalg.norm(parallel_velocity) < self.eps * self.myu:
                particle.velocity = utils.decompose_by(particle.velocity, self.norm)
                parallel_velocity -= parallel_velocity

            friction_for_velocity = np.array([0,0,0,0], dtype=np.float64)
            particle.force = parallel_force.copy()
            if np.linalg.norm(parallel_velocity) > 0:
                friction_for_velocity = self.myu * np.linalg.norm(down_force) * utils.numpy_get_unit(parallel_velocity)

            maximum_friction_force = particle.mass * parallel_velocity / dt
            
            if np.linalg.norm(friction_for_velocity) > np.linalg.norm(maximum_friction_force):
                friction_for_velocity = maximum_friction_force

            # friction_for_current_force = np.array([0,0,0,0], dtype=np.float64)
            # if np.linalg.norm(particle.force) > 0:
            #     friction_for_current_force = self.myu * np.linalg.norm(down_force) * utils.numpy_get_unit(particle.force)
            
            # if np.linalg.norm(friction_for_current_force) > np.linalg.norm(particle.force):
            #     particle.force -= particle.force
            # else:
            #     particle.force -= friction_for_current_force

            particle.force -= friction_for_velocity

        
    @override
    def check_contact(self, particle: Particle, dt:float) -> bool:
        distance = np.abs(np.dot(self.passpoint - particle.position, self.norm))
        velocity_toward_plane = np.linalg.norm(utils.decompose_by(particle.velocity, self.norm))
        if distance < self.eps:
            if velocity_toward_plane < self.eps / dt:
                return True

        return False

    def overwrite(self, norm, passpoint, k, myu, collision, contact):
        self.norm = norm
        self.passpoint = passpoint
        self.k = k
        self.myu = myu
        self.collision_enabled = collision
        self.contact_enabled = contact


    
# class Triangle_Plane_Collider(Collider):
#     def __init__(self,
#                 vertex1: np.ndarray,
#                 vertex2: np.ndarray,
#                 vertex3: np.ndarray,
#                 k: float = 1.0
#                 ) -> None:
#         super().__init__(k)