import math
from abc import abstractmethod
from tkinter import Tk, ttk

from PIL import Image, ImageDraw, ImageTk

from vect2d import Vect2D


class RGBAColor():
    def __init__(self, r:int=255, g:int=255, b:int=255, a:int=255):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a
        
        @property
        def r(self):
            return self.__r
        
        @property
        def g(self):
            return self.__g
        
        @property
        def b(self):
            return self.__b
        
        @property
        def a(self):
            return self.__a


class Drawable():
    def __init__(self, size:Vect2D, color:RGBAColor, position:Vect2D):
        self.__size = size
        self.__color = color
        self.__position = position
        
    @property
    def size(self):
        return self.__size
    
    @property
    def color(self):
        return self.__color
    
    @property
    def position(self):
        return self.__position


class App():
    def __init__(self):
        self.__gui = GUI(Vect2D(500,500), RGBAColor(255 ,255, 255), Vect2D(0,0))
        #self.__simulation = Simulation()
    
    
class GUI(Tk, Drawable):
    
    def __init__(self, size:Vect2D, color, position=None):
        Tk.__init__(self)
        Drawable.__init__(self, size, color, position)
        
        self.__control_panel = ControlPanel("Control")
        self.__param_panel = ParamPanel("Param")
        self.__view_window = ViewWindow(size, color)
        self.__width = size.x
        self.__height = size.y
        
        self.__control_panel.pack(side="left", fill="y")
          
        self.title('Boids')
        self.geometry(str(int(self.__width)) + 'x' + str(int(self.__height)))
        self.iconbitmap('boids.ico')
        
        self.mainloop()
               
    # GUI getters #    
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

     
class Entity():
    def __init__(self):
        pass
    
class Updatable():
    def __init__(self):
        pass

    @abstractmethod
    def tick(self):
        pass

 
class Simulation(Updatable):
    def __init__(self, sprites:list[Entity]):
        self.__sprites = sprites

    def tick(self):
        for sprite in self.__sprites:
            sprite.tick()
        


class ControlPanel(ttk.LabelFrame):
    def __init__(self, title):
        ttk.LabelFrame.__init__(self, text=title)
        self.__start_button = ttk.Button(self, text="Start")
        self.__stop_button = ttk.Button(self, text="Stop")
        self.next_button = ttk.Button(self, text="Next Step")

        
        self.__start_button.pack()
        self.__stop_button.pack()
        self.next_button.pack()


class StartStopPanel(ControlPanel):
    def __init__(self):
        self.__start_btn = None
        self.__stop_btn = None
        self.__restart_btn = None


class ViewWindow(Drawable):
    def __init__(self, size, color, position=None):
        Drawable.__init__(self, size, color, position)



class ParamPanel(ttk.LabelFrame):
    def __init__(self, title):
        self.text = title


class VisualParamPanel(ParamPanel):
    def __init__(self):
        pass


class SimParamPanel(ParamPanel):
    def __init__(self):
        pass    

    @abstractmethod
    def draw(self):
        pass
    
    @property
    def sprites(self):
        return self.__sprites


class Gravitational():
    def __init__(self, mass:int, force:int):
        self.__mass = mass
        self.__force = force
       
    @abstractmethod
    def pull(self):
        pass
    
    @property
    def mass(self):
        return self.__mass
    
    @property
    def force(self):
        return self.__force
 
    
class Touchable():
    def __init__(self):
        pass
    
    @abstractmethod
    def check_collision(self):
        pass
    

class Circle(Entity, Touchable, Updatable):
    def __init__(self, radius=random.randrange(5,10), fill_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), border_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), density=random.randrange(0,10), position:Vect2D=Vect2D(random.randrange(0,100),random.randrange(0,100)), speed:Vect2D=Vect2D(random.randrange(-10,10),random.randrange(-10,10)), acceleration:Vect2D=Vect2D(0,0), bounce=0.95, friction=0.95):
        self.__position = position
        self.__color = color
        self.__radius = radius

class Ball(Updatable, Gravitational):
        Gravitational.__init__(self, masse=(density * (math.pi * radius ** 2)))
        self.__radius = radius
        self.__fill_color = fill_color
        self.__border_color = border_color
        self.__density = density
        self.__position = position
        self.__initial_speed = deepcopy(speed)
        self.__speed = deepcopy(speed)
        self.__acceleration = acceleration
        self.__bounce = bounce
        self.__friction = friction
        self.__trail = Trail();

    def move(self, time):
        self.__position.x += self.__speed.x + 0.5 * self.__acceleration.x * time **2
        self.__position.y += self.__speed.y + 0.5 * self.__acceleration.y * time **2
        self.__speed.x += self.__acceleration.x * time
        self.__speed.y += self.__acceleration.y * time
        

    def bounce(self, game_dimension:Vect2D):
        if self.__position.x <= 0 + self.__radius:
            border = 0
            self.__speed.x = -self.__speed.x * self.__bounce
            self.__speed.y *= self.__friction
            self.__position.x = 2.0 * (border + self.__radius) - self.__position.x

        elif self.__position.x >= game_dimension.x - self.__radius :
            border = game_dimension.x
            self.__speed.x = -self.__speed.x * self.__bounce
            self.__speed.y *= self.__friction
            self.__position.x = 2.0 * (border - self.__radius) - self.__position.x

        if self.__position.y <= 0 + self.__radius :
            border = 0
            self.__speed.y = -self.__speed.y * self.__bounce
            self.__speed.x *= self.__friction
            self.__position.y = 2.0 * (border + self.__radius) - self.__position.y

        elif self.__position.y >= game_dimension.y - self.__radius :
            border = game_dimension.y
            self.__speed.y = -self.__speed.y * self.__bounce
            self.__speed.x *= self.__friction
            self.__position.y = 2.0 * (border - self.__radius) - self.__position.y

    def tick(self, time, game_dimensions, acceleration, game):
        
        self.__acceleration = acceleration
        
        if not game.hand_of_god == Vect2D(-1, -1):
            self.pushed_by(game.hand_of_god)
            
        if game.gravity_field_active:
                self.pulled_by(game.balls)
                
        # if acceleration == Vect2D(0, 0):
        #     self.reset_speed()
        #     pass

        self.move(time)
        self.bounce(game_dimensions)

class StaticCircle(Circle):
    def __init__(self):
        pass
 
    
class Movable():
    def __init__(self):
        pass
 
    
class SteeringBehavior():
    def __init__(self):
        self.__force_attraction_repulsion = None
        self.__resulting_direction = None
        
    @abstractmethod    
    def behave(self, this_entity:Entity, target_entity:Entity):
        return target_entity.position - this_entity.position
  
    
class CollisionAvoidance(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class Wander(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class FleeArrival(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class Seek(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
    
class Piloted(Movable):
    def __init__(self, slowing_distance:int, steering_force:Vect2D, desired_speed:Vect2D, steering_behavior:list[SteeringBehavior], acceleration:Vect2D, max_steering_force:Vect2D):
        self.__slowing_distance = slowing_distance
        self.__steering_force = steering_force
        self.__desired_speed = desired_speed
        self.__steering_behavior = steering_behavior
        self.__acceleration = acceleration
        self.__max_steering_force = max_steering_force
    
    @abstractmethod
    def move(self):
        pass

class DynamicCircle(Circle, Piloted):
    def __init__(self, vitesse, vitesse_max):
        self.__vitesse = vitesse
        self.__vitesse_max = vitesse_max
    


def main():
    App()


if __name__ == '__main__':
    main()