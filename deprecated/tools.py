from math import pi as π
class SoccerBot:
    speed:int
    direction:float
    def move_dir(self, direction:float):
        """TODO
        Changes the robot's move direction to the given ``direction`` in radians
        """
        self.direction = direction % 2*π

    def get_dir_ball(self) -> float:
        """TODO
        Returns the direction in radians of the ball"""