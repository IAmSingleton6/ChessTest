from abc import ABC, abstractmethod

# If a class inherits from more than one of these classes
# The class must include a def delete() func to run the delete 
# of each of the components
# Quite flimsy but did not realise python's gc was so strict

# In future to fix make a wrapper class to automatically include this per object



class Update(ABC):
    objects_to_update = []

    def __new__(cls, *args, **kw):
        instance =  super().__new__(cls)
        Update.objects_to_update.append(instance)
        return instance


    @abstractmethod
    def update(self, dT: float) -> None:
        ...


    def delete(self) -> None:
        self.objects_to_update.remove(self)


    def delete(self) -> None:
        try:
            self.objects_to_update.remove(self)
        except ValueError:
            pass


class Renderer(ABC):
    objects_to_render = []


    def __new__(cls, *args, **kw):
        instance =  super().__new__(cls)
        Renderer.objects_to_render.append(instance)
        instance.set_z_index(0)
        return instance
    

    def set_z_index(self, z) -> None:
        self._z_index =  z
        self.objects_to_render.sort()


    def get_z_index(self) -> None:
        return self._z_index


    @abstractmethod
    def draw(self, window) -> None:
        ...


    def delete(self) -> None:
        try:
            self.objects_to_render.remove(self)
        except ValueError:
            pass


    def __lt__(self, other):
        return self._z_index < other._z_index
    


class Input(ABC):
    objects_receive_input = []

    def __new__(cls, *args, **kw):
        instance =  super().__new__(cls)
        Input.objects_receive_input.append(instance)
        return instance


    @abstractmethod
    def handle_input(self, event, mouse_pos: (int, int)) -> None:
        ...


    def delete(self) -> None:
        try:
            self.objects_receive_input.remove(self)
        except ValueError:
            pass
