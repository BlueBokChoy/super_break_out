"""
Author: Roy Chen and Jerry Wang
Date: December 16, 2024
Description: This module contains the sprites for the super break-out game.
"""

# Import and Initalize dependencies.
import pygame
import random
pygame.init()

class Label(pygame.sprite.Sprite):
    """This class defines the sprite for a label."""

    def __init__(self, text, font_size, pos):
        """Initalizes label's image and rect. Takes the text to be displayed, size of font, and position
        on screen as string, integer, and a tuple ordered pair as parameters respectively. Returns
        nothing."""
        
        # Inherits the parent sprite class.
        super().__init__()
        
        # Initalizes the attributes.
        self.__animate = False
        self.__pos = pos
        self.__game_font = pygame.font.Font("fonts/press_start_2.ttf", font_size)
        self.__text = text
        self.__color = (255, 255, 255)
        
        # Initalizes the image attribute.
        self.image = self.__game_font.render(self.__text, True, self.__color)
        
        # Initalizes the rect attributes
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos

    def make_animated(self, up_down_range, speed):
        """This method gives the label up and down animation. Takes the up and down range as a tuple
        ordered pair and the movement speed as an integer parameter. Returns nothing."""

        self.__animate = True
        self.__upper = up_down_range[0]
        self.__lower = up_down_range[1]
        self.__dy = speed

    def set_text(self, text):
        """This method sets the text attribute of the label sprite. Takes the new text as a string parameter.
        Returns nothing."""

        self.__text = text

    def set_text_color(self, color):
        """This method sets the text color attribute of the label sprite. Takes the new color as a tuple
        with rgb values as a parameter."""
        
        self.__color = color

    def highlight(self):
        """This method highlights lets a label highlight itself. Takes no parameters and returns nothing."""

        if ">>" not in self.__text:
            text = ">>" + self.__text + "<<"
            self.set_text(text)

    def dehighlight(self):
        """This method highlights lets a label unhighlight itself. Takes no parameters and returns nothing."""

        if ">>" in self.__text:
            text = self.__text.replace("<<", "").replace(">>", "")
            self.set_text(text)

    def update(self):
        """This method is automatically called to update any changes to the label attributes and to animate
        the label. Takes no parameters and returns nothing."""

        if self.__animate:
            self.rect.y += self.__dy

            if self.rect.top <= self.__upper or self.rect.bottom > self.__lower:
                self.__dy = -self.__dy
        
        self.image = self.__game_font.render(self.__text, True, self.__color)
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos

class Brick(pygame.sprite.Sprite):
    """This class defines the sprite for a brick."""

    # Initalizes the tuple of brick colors as a constant class variable.
    # Order: Purple, Red, Orange, Yellow, Green, Blue
    COLORS = ("p", "r", "o", "y", "g", "b")
    
    # Initalizes the tuple of brick shapes as a constant class variable.
    SHAPES = ("_rect.png", "_circle.png", "_star.png", "_pentagon.png", "_fish.png")
    
    # Initalizes the tuple of brick score values as a constant class variable.
    # Order: Purple, Red, Orange, Yellow, Green, and Blue
    SCORE_VALUES = (6, 5, 4, 3, 2, 1)
    
    def __init__(self, pos, row):
        """Initalizes brick image and rect. Takes in the bricks position as a tuple and which row brick is as an integer.
        Returns nothing"""
        
        # Inherits the parent sprite class.
        super().__init__()
        
        # Initalizes the brick attributes.
        self.__pos = pos
        self.__score_value = Brick.SCORE_VALUES[row]
        self.__downshift_val = 2
        
        # Initalizes the image attribute.
        self.image = pygame.image.load("imgs/" + Brick.COLORS[row] + Brick.SHAPES[random.randrange(4)])
        
        # Initalizes the rect attribute.
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos
        
    def set_downshift_val(self, value):
        """This method sets the downshift value of the brick. Takes the new downshift value as a integer
        parameter. Returns nothing."""
        
        self.__downshift_val = value
    
    def move_down(self):
        """This method moves the brick down by the screen by the downshift value. Takes no parameters and
        returns nothing."""
        
        self.rect.y += self.__downshift_val
        
    def remove_brick(self, hud):
        """This method adds the score value of the brick into the HUD score and removes the brick object.
        Takes no parameters and returns nothing."""
        
        hud.add_score(self.__score_value)
        self.kill()

class Platform(pygame.sprite.Sprite):
    """This class defines the sprite for a player controlled platform."""
    
    # Initalizes the tuple of platform sizez as a constant class variable.
    # Order: Super Easy, Easy, Medium, Hard
    SIZES = {2: (160, 10), 3: (120, 10), 4: (80, 15), 5: (40, 10)}
    
    
    def __init__(self, pos):
        """Initalizes the platform image and rect. Takes the position parameter as a tuple ordered pair.
        Returns nothing."""
        
        # Inherits the parent sprite class.
        super().__init__()
        
        # Initalizes the platform attributes.
        self.__size = Platform.SIZES[2]
        self.__color = (255, 255, 255)
        self.__dx = 10
        self.__pos = pos
        
        # Initalizes the image attribute.
        self.image = pygame.Surface(self.__size)
        self.image.fill((255, 255, 255))
        
        # Initalizes the rect attribute.
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos
    
    def move(self, direction):
        """This method moves the platform left or right by the preset dx speed. Takes the direction of
        movement as a string parameter. Returns nothing."""
        
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.__dx
        elif direction == "right" and self.rect.right < 800:
            self.rect.x += self.__dx
            
    def third_phase(self):
        """This method changes the platform for third phase difficulty by halfing the platform size and
        changing the platform color to red. Takes no parameters and returns nothing."""
        
        self.__pos = self.rect.center
        self.__color = (255, 0, 0)
        self.__size = (self.__size[0] // 2, self.__size[1])
        self.update_platform()
    
    def change_platform_size(self, difficulty):
        """This method changes the platform size to match the difficulty level. Takes the difficulty level
        as an integer parameter from 2 to 5 representing super easy to hard. Returns nothing."""
        
        self.__size = Platform.SIZES[difficulty]
        self.update_platform()
        
    def remove_platform(self):
        """This method removes the platform. Takes no parameters and returns nothing."""
        
        self.kill()
        
    def set_platform_pos(self, pos):
        """This method sets the position of the platform. Takes the new position parameter as a tuple
        ordered pair. Returns nothing."""
        
        self.__pos = pos
        self.update_platform()
        
    def update_platform(self):
        """Updates the platform image and rect attributes. Takes no parameters and returns nothing."""
        
        self.image = pygame.Surface(self.__size)
        self.image.fill(self.__color)
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos
        
class Ball(pygame.sprite.Sprite):
    """This class defines the sprite for a moving ball."""
    
    def __init__(self):
        """Initalizes the ball image and rect. Takes no parameters and returns nothing."""
        
        # Inherits the parent sprite class.
        super().__init__()
        
        # Initalizes the ball attributes.
        self.__dx = 4
        self.__dy = 6
        
        # Initalizes the image attributes.
        self.image = pygame.image.load("imgs/ball.png")
        self.image.set_colorkey((0,0,0))
        
        # Initalizes the rect attributes.
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)
    
    def change_direction(self, collided_item):
        """This method changes the movement direction of the ball based on the point of collision
        from another sprite. Takes the other sprite as an object parameter. Returns nothing."""
        
        # Reverse dy for a bounce.
        self.__dy = -self.__dy

        # Calculate the position where the ball hits the platform.
        collision_spot = (self.rect.centerx - collided_item.rect.left) / collided_item.rect.width

        # Normalize the hit position to a range of -1 to 1 (left to right).
        collision_spot = (collision_spot * 2) - 1 

        # Adjust the horizontal velocity based on the collision point.
        self.__dx = collision_spot * 4
        
    def increase_speed(self, amount):
        """This method increases the speed of the movement direction of the ball. Takes the amount
        to increase by as an integer parameter and returns nothing."""
        
        # Checks which direction the ball is currently travelling.
        if self.__dy > 0:
            self.__dy += amount
        else:
            self.__dy -= amount
    
    def reset(self):
        """This method resets the ball to the centre of the screen. Takes no parameters and returns
        nothing."""
        
        self.rect.center = (400, 400)
                
    def update(self):
        """This method will be called automatically to reposition the ball sprite on the screen.
        Takes no parameters and returns nothing."""
        
        # Check for collisions with the left and right screen edges
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.__dx = -self.__dx
            
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= 800: 
                self.rect.right = 800
        
        # Move the ball horizontally
        self.rect.x += self.__dx
        
        # Check for collisions with the top and bottom screen edges
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.__dy = -self.__dy
            
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= 600:
                self.rect.bottom = 600
        
        # Move the ball vertically
        self.rect.y += self.__dy
        
class Loss_zone(pygame.sprite.Sprite):
    """This class defines the sprite for a loss zone."""
    
    def __init__(self):
        """Initalizes the loss zone image and rect. Takes no parameters and returns nothing"""
        
        # Inherits the parent sprite class.
        super().__init__()
        
        # Initalizes the image attributes.
        self.image = pygame.Surface((800, 20))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        
        # Initalizes the rect attributes.
        self.rect = self.image.get_rect()
        self.rect.center = (400, 595)
        

class Hud(pygame.sprite.Sprite):
    """This class defines the sprite for the HUD."""
    
    def __init__(self):
        """Initalizes the HUD image and rect. Takes no parameters and returns nothing."""
        
        super().__init__()
        
        # Initializes the HUD attributes.
        self.__score = 0
        self.__lives = 3
        self.__win = False
        
        # Initalizes the image attributes.
        self.image = pygame.Surface((180, 100))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        
        # Initalizes the HUD Text font.
        self.__game_font = pygame.font.Font("fonts/press_start_2.ttf", 20)
        
        # Initalizes the HUD elements.
        self.score_text = self.__game_font.render(str(self.__score), True, (255, 255, 255))
        self.lives_text = self.__game_font.render(str(self.__lives), True, (255, 255, 255))
        self.score_label = self.__game_font.render("Score", True, (255, 255, 255))
        self.heart_img = pygame.transform.scale(pygame.image.load("imgs/heart.png"), (25, 25))
        self.x_text = self.__game_font.render("x", True, (255, 255, 255))
        
        # # Initalizes the rect attributes..
        self.rect = self.image.get_rect()
        self.rect.center = (120, 530)
    
    def add_score(self, new_values):
        """Increases the score by the specified amount. Takes the amount as a parameter and
        returns nothing."""

        # Adds the new values to the current score.
        self.__score += new_values

    def remove_life(self, amount):
        """This method removes a specified number of lives. Takes the amount as a parameter
        and returns nothing."""

        # Decreases the number of lives by the specified amount.
        self.__lives -= amount

    def get_score(self):
        """This method returns the current score. Takes no parameters and returns the value
        stored in the score attribute."""

        # Returns the current score.
        return self.__score

    def get_lives(self):
        """This method gets the current number of lives. Takes no parameters and returns the
        value stored in the lives attribute."""

        # Returns the current number of lives.
        return self.__lives

    def get_win(self):
        """This method gets whether the player has won the game. Takes no parameters and
        returns the value stored in the win attribute."""

        # Returns the win status (True if the player has won, False otherwise).
        return self.__win

    def check_game_over(self):
        """This method checks if the game is over based on the score or remaining lives. Takes
        no parameters and returns nothing."""

        # Checks if the player has won.
        if self.__score == 378:
            self.__win = True 
            return True  

        # Checks if the player has lost all lives.
        elif self.__lives < 1:
            self.__win = False  
            return True 

    def update(self):
        """This method updates the HUD elements on the screen, rendering the score and lives.
        Takes no parameters and returns nothing."""
        
        # Clears HUD.
        self.image.fill((0, 0, 0, 0))
        
        # Blits HUD elements onto HUD.
        self.image.blit(self.__game_font.render(str(self.__score), True, (255, 255, 255)), (0, 20))
        self.image.blit(self.__game_font.render("Score", True, (255, 255, 255)), (80, 20))
        self.image.blit(self.heart_img, (5, 65))
        self.image.blit(self.__game_font.render("x", True, (255, 255, 255)), (45, 70))
        self.image.blit(self.__game_font.render(str(self.__lives), True, (255, 255, 255)), (80, 70))
