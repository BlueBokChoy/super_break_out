"""
Author: Jerry Wang and Roy Chen
Date: December 16, 2024
Description: This program is a recreation of 1978 video game by Atari, Super Break-Out.
This recreation features a multiplayer mode, 4 difficulties, progressively increasing difficulty, music, and unique shapes.
"""

# Initalizes and imports dependencies.
import pygame
import game_sprites
import time
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((960, 720))


class main():
    """This is the mainline logic."""

    def __init__(self):
        """Initalizes the IDEA/ALTER logic."""

        # Initializes the display background
        pygame.display.set_caption("Super Break Out")

        # Initializes the entities.
        self.entities()

        # Displays the menu.
        self.alter()

    def entities(self):
        """This method initializes the entities. Takes no parameters and returns nothing."""
        
        # Initializes the background.
        self.__background = pygame.Surface(screen.get_size())
        self.__background = self.__background.convert()
        self.__background.fill((73, 13, 97))
        screen.blit(self.__background, (0, 0))
        
        # Initalizes the background music.
        pygame.mixer.music.load("music/menu_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        # Initalizes the sfxs.
        self.sfx_entities()
        
        # Initalizes the entities for each display state.
        self.menu_entities()
        self.game_opt_entities()
        self.game_instr_entities()
        self.game_entities()
        self.game_over_entities()
        
        # Initalizes a tuple with all the game sprite groups.
        self.all_sprite_groups = (self.__menu_sprites,\
                                  self.__game_opt_sprites,\
                                  self.__game_instr_sprites,\
                                  self.__game_sprites,\
                                  self.game_over_sprites)

    def alter(self):
        """This method is the game loop in ALTER logic. Takes no parameters and returns
        nothing."""

        # Assign the variables.
        self.assign()
        
        # The game loop.
        while self.__keep_going:

            # Initializes the FPS.
            self.__clock.tick(30)

            # Checks and handles events.
            self.events()

            # Updates and refresh the display.
            self.refresh()

        # Quits the game.
        pygame.quit()
        
    def assign(self):
        """This method assigns the instance variables used in the game loop. Takes no
        parameters and returns nothing."""
        
        # Initializes the game loop variables.
        self.__keep_going = True
        self.__clock = pygame.time.Clock()
        self.__display_state = 0
        self.__last_display_state = 0
        
        # Initializes the variables for event handlers.
        self.__events_dict = (self.menu_events_handler,\
                              self.game_opt_events_handler,\
                              self.game_instr_events_handler,\
                              self.game_events_handler,\
                              self.game_over_events_handler)
        
        # Initializes the option display variables.
        self.__highlighted_option = 0
        self.__selected_difficulty = None
        self.__selected_players = None
        
        # Initializes the game display variables.
        self.__phase = 1
        
        # Hides cursor.
        pygame.mouse.set_visible(not self.__keep_going)
    
    def events(self):
        """This method handles the events. Takes no parameters and returns nothing."""
        
        # Single press event handling.
        for event in pygame.event.get():
            
            # Checks for quit events.
            if event.type == pygame.QUIT:
                self.__keep_going = False
            
            # Checks for key press events.
            if event.type == pygame.KEYDOWN:
                if self.__display_state in (0, 1, 2, 4):
                    self.__events_dict[self.__display_state](event)
        
        # Continuous state event handling.
        if self.__display_state == 3:
            self.__events_dict[3]()
        
    def refresh(self):
        """This method refreshes the display with the correct page. Takes no parameters and
        returns nothing."""
        
        # Clear previous screens if needed.
        if self.__last_display_state != self.__display_state:
            self.all_sprite_groups[self.__display_state - 1].clear(screen, self.__background)
            self.__last_display_state = self.__display_state           
        
        # Clear, update, and draw sprites.
        self.all_sprite_groups[self.__display_state].clear(screen, self.__background)
        self.all_sprite_groups[self.__display_state].update()
        self.all_sprite_groups[self.__display_state].draw(screen)
        
        # Updates the text features on game options
        if self.__display_state == 1:
            self.update_option_text()

        # Flips the display.
        pygame.display.flip()
        
        # Sets the mouse to be visible when program ends.
        pygame.mouse.set_visible(not self.__keep_going)
        
    def sfx_entities(self):
        """This helper method initializes the sound effect entites and assigns each an
        instance variable.Takes no parameters and returns nothing."""
        
        self.__select_opt_sfx = pygame.mixer.Sound("sounds/select.mp3")
        self.__intro_sfx = pygame.mixer.Sound("sounds/intro.mp3")
        self.__bounce_sfx = pygame.mixer.Sound("sounds/bounce.mp3")
        self.__brick_break_sfx = pygame.mixer.Sound("sounds/brick_break.mp3")
        self.__transition_sfx = pygame.mixer.Sound("sounds/transition.mp3")
        self.__damage_sfx = pygame.mixer.Sound("sounds/damage.mp3")
        self.__lose_sfx = pygame.mixer.Sound("sounds/lose.mp3")
        self.__win_sfx = pygame.mixer.Sound("sounds/win.mp3")

    def menu_entities(self):
        """This helper method initializes the menu sprites into a group. Takes no parameters
        and returns nothing."""
        
        self.__menu_sprites = pygame.sprite.Group()
        
        # Initalizes the title label.
        self.__menu_sprites.add(game_sprites.Label("SUPER BREAK OUT", 50, (400, 250)))
        
        # Initalizes the subtitle label.
        self.__menu_subtitle = game_sprites.Label("Press [SPACE] to start", 25,(400, 400))
        self.__menu_subtitle.make_animated((380, 420), 1)
        
        # Adds menu sprites into one group
        self.__menu_sprites.add(self.__menu_subtitle)

    def game_opt_entities(self):
        """This helper method initializes the game option sprites into a group. Takes no
        parameters and returns nothing."""
        
        self.__game_opt_sprites = pygame.sprite.Group()
        
        # Initalize the title label.
        self.__opt_title = game_sprites.Label("Game Options", 40, (400, 75))
        
        # Initalize the subtitle label.
        self.__opt_subtitle = (game_sprites.Label("Players", 30, (400, 150)),\
                             game_sprites.Label("Difficulty", 30, (400, 300)))
        
        # Initalize the selectable option labels
        self.__opt_selectables = (game_sprites.Label("1P", 25, (200, 225)),\
                                game_sprites.Label("2P", 25, (600, 225)),\
                                game_sprites.Label("Very Easy", 25, (200, 375)),\
                                game_sprites.Label("Easy", 25, (600, 375)),\
                                game_sprites.Label("Medium", 25, (200, 450)),\
                                game_sprites.Label("Hard", 25, (600, 450)))
        
        # Initalizes the instructions label for the options.
        self.__opt_instructions = (game_sprites.Label("[←/→] to switch options", 15, (400, 515)),\
                                 game_sprites.Label("[S] to select an option", 15, (400, 535)),\
                                 game_sprites.Label("[SPACE] to start game", 15, (400, 555 )))
        
        # Add game option sprites into one group.
        self.__game_opt_sprites.add(self.__opt_selectables,\
                                    self.__opt_title,\
                                    self.__opt_instructions,\
                                    self.__opt_subtitle)
        
    def game_instr_entities(self):
        """This helper method initializes the game instructions sprites into a group. Takes no
        parameters and returns nothing."""
        
        self.__game_instr_sprites = pygame.sprite.Group()
        
        self.__game_instr_sprites.add(game_sprites.Label("Welcome to Super Break Out!", 20, (400, 100)),
                                    game_sprites.Label("Your goal is to destroy all of the bricks", 15, (400, 175)),
                                    game_sprites.Label("above you with the bouncing ball.", 15, (400, 200)),
                                    game_sprites.Label("After 80 points, the ball moves faster.", 15, (400, 225)),
                                    game_sprites.Label("At the halfway mark, your paddle halves in size!", 15, (400, 250)),
                                    game_sprites.Label("Be careful not to let the ball touch the ground!", 15, (400, 275)),
                                    game_sprites.Label("For player 1, use [←/→] to move.", 15, (400, 325)),
                                    game_sprites.Label("For player 2, use [LMB/RMB] to move.", 15, (400, 350)),
                                    game_sprites.Label("Good luck and have fun!", 20, (400, 400)),
                                    game_sprites.Label("Press [space] to continue.", 10, (400, 425)))
        
    def game_entities(self):
        """This helper method initializes the game sprites into a group. Takes no parameters and
        returns nothing."""
        
        # Initalize game entity sprite groups.
        self.__game_sprites = pygame.sprite.Group()
        self.__game_bricks = pygame.sprite.Group()
        self.__game_players = pygame.sprite.Group()
        self.__game_loss_zone = game_sprites.Loss_zone()
        
        # Initalizes the game HUD.
        self.__hud = game_sprites.Hud()
        
        # Initalizes the game bricks.
        for row in range(6):
            for col in range(18):
                pos_x = (col * (40 + 5)) + 40 // 2
                pos_y = (row * (24 + 5)) + 34 // 2
                
                brick = game_sprites.Brick((pos_x, pos_y), row)
                
                self.__game_bricks.add(brick)
                      
        # Initalizes the players
        self.__game_player1 = game_sprites.Platform((200, 580))
        self.__game_player2 = game_sprites.Platform((600, 560))
        self.__game_players.add(self.__game_player1, self.__game_player2)
        
        # Initalizes the ball.
        self.__game_ball = game_sprites.Ball()
        
        # Adds game sprites everything into the game sprites group.
        self.__game_sprites.add(self.__game_bricks,\
                                self.__game_players,\
                                self.__game_ball,\
                                self.__game_loss_zone,\
                                self.__hud)
        
    def game_over_entities(self):
        """This helper method initalizes the game over sprites. Takes no parameters and returns
        nothing."""
        
        self.game_over_sprites = pygame.sprite.Group()
        
        self.__result_text = game_sprites.Label("", 80, (400, 175))
        self.__score_text = game_sprites.Label("", 40, (400, 300))
        
        
        self.__game_over_subtitle = game_sprites.Label("Press [SPACE] to play again", 25, (400, 400))
        self.__game_over_subtitle.make_animated((380, 420), 1)
        self.game_over_sprites.add()
    
        self.game_over_sprites.add(self.__result_text,\
                                   self.__score_text,\
                                   self.__game_over_subtitle)
    
    def menu_events_handler(self, event):
        """This helper method handles the events for menu. Takes the event as a list parameter
        and returns nothing."""
            
        # Switch to game options screen on SPACE key press.
        if event.key == pygame.K_SPACE:
            self.__display_state = 1
    
    def game_opt_events_handler(self, event):
        """This helper method handles the events for game options. Takes the event as a list
        parameter and returns nothing."""
            
        # Left/Right option navigation.
        if event.key == pygame.K_RIGHT:
            if self.__highlighted_option < 5:
                self.__highlighted_option += 1
            else:
                self.__highlighted_option = 0
        if event.key == pygame.K_LEFT:
            if self.__highlighted_option > 0:
                self.__highlighted_option -= 1
            else:
                self.__highlighted_option = 5
                
        # Select an option using the s key.
        if event.key == pygame.K_s:
            if self.__highlighted_option == 0 or self.__highlighted_option == 1:
                self.__selected_players = self.__highlighted_option
                self.__select_opt_sfx.play()
            elif self.__highlighted_option > 1 or self.__highlighted_option < 6:
                self.__selected_difficulty = self.__highlighted_option
                self.__select_opt_sfx.play()

        # Switch to game instructions screen on SPACE key press.
        # Validates if the user has selected options.
        if event.key == pygame.K_SPACE:
            if (self.__selected_players is not None) and (self.__selected_difficulty is not None):
                self.__display_state = 2
                pygame.mixer.music.stop()
                self.__intro_sfx.play()
        
    def game_instr_events_handler(self, event):
        """This helper method handles the events for game instructions. Takes the event as a list
        and returns nothing."""
        
        # Switch to game screen on SPACE key press.
        if event.key == pygame.K_SPACE:
            self.__display_state = 3
            # Changes menu bg music to game bg music.
            self.change_background_music("music/phase_one_music.mp3")
            # Update game to user preferences.
            self.update_game()
    
    def game_events_handler(self):
        """This helper method handles the events for the game. Takes no parameters and returns
        nothing."""
 
         # Left/Right movement for player 1.
        keyboard_keys = pygame.key.get_pressed()
        if keyboard_keys[pygame.K_LEFT]:
            self.__game_player1.move("left")
        if keyboard_keys[pygame.K_RIGHT]:
            self.__game_player1.move("right")
        
        # Checks if player 2 exists.
        if self.__selected_players == 1:
            # Left/Right movement for player 2.
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[0]:
                self.__game_player2.move("left")
            if mouse_keys[2]:
                self.__game_player2.move("right")
            
        # Increase difficulty after player reaches halfway score.
        if (self.__hud.get_score() >= 189) and (self.__phase == 2):
            
            # Increases to next phase.
            self.__phase = 3
            
            # Play transition sounds and swap background music.
            self.freeze_and_sfx(self.__transition_sfx, self.__transition_sfx.get_length(), False)
            self.change_background_music("music/phase_three_music.mp3")
            
            # Adjustments to game entities.
            self.__game_player1.third_phase()
            if self.__selected_players == 1:
                self.__game_player2.third_phase()
            self.__game_ball.increase_speed(2)
            for brick in self.__game_bricks:
                brick.set_downshift_val(8)
        
        # Increases difficulty after player reaches phase 1.
        if (self.__hud.get_score() >= 80) and (self.__phase == 1):
            
            # Increases to next phase.
            self.__phase += 1
            
            # Phase transition sounds.
            self.freeze_and_sfx(self.__transition_sfx, self.__transition_sfx.get_length(), False)
            self.change_background_music("music/phase_two_music.mp3")
            
            # Adjustments to game entities.
            self.__game_ball.increase_speed(1)
            for brick in self.__game_bricks:
                brick.set_downshift_val(4)

        # Checks if end condition is present.
        if self.__hud.check_game_over():
            pygame.mixer.music.stop()
            self.update_game_over()
            self.__display_state = 4

        # Checks for collisions with other game sprites.

        # Player-ball collisions.
        collided_platform = pygame.sprite.spritecollide(self.__game_ball, self.__game_players, False)
        if collided_platform:

            # Plays sfx.
            self.__bounce_sfx.play()
            
            # Changes ball direction.
            self.__game_ball.change_direction(collided_platform[0])

            # Shifts all bricks down.
            for bricks in self.__game_bricks:
                bricks.move_down()
                
        # Ball-brick collisions.
        broken_bricks = pygame.sprite.spritecollide(self.__game_ball, self.__game_bricks, False)
        if broken_bricks:
            
            # Plays sfx.
            self.__bounce_sfx.play()
            self.__brick_break_sfx.play()
            
            # Removes brick and adds to score.
            for brick in broken_bricks: 
                brick.remove_brick(self.__hud)
            
            # Reverse ball direction.
            self.__game_ball.change_direction(broken_bricks[0])

        # Loss zone-brick collisions.
        if pygame.sprite.spritecollide(self.__game_loss_zone, self.__game_bricks, False):
            
            # Removes all lifes.
            self.__hud.remove_life(3)

        # Ball-loss zone collisions.
        if self.__game_ball.rect.colliderect(self.__game_loss_zone):
            
            # Checks if player has enough lives to keep playing.
            if self.__hud.get_lives() > 1:
                
                # Plays sfx.
                self.freeze_and_sfx(self.__damage_sfx, 2, True)
                
                # Resets ball to center of display.
                self.__game_ball.reset()
                
            # Removes a life.
            self.__hud.remove_life(1)
             
    def game_over_events_handler(self, event):
        """This helper method handles the events for game over. Takes the event as a list parameter
        and returns nothing."""

        # Switch to game screen on SPACE key press.
        if event.key == pygame.K_SPACE:
            self.__display_state = 0
            self.reset()        
        
    def update_option_text(self):
        """This method updates the displayed text for highlight options and categories. Takes no
        parameters and returns nothing."""

        # Reset all option.
        for option in self.__opt_selectables:
            option.dehighlight()
            option.set_text_color((255, 255, 255))

        # Highlight the player option.
        self.__opt_selectables[self.__highlighted_option].highlight()
                
        # Changes the color of the selected option to yellow.
        if self.__selected_players is not None: 
            self.__opt_selectables[self.__selected_players].set_text_color((235, 207, 52))
        if self.__selected_difficulty is not None: 
            self.__opt_selectables[self.__selected_difficulty].set_text_color((235, 207, 52))
    
    def reset(self):
        """This method resets the program entities and variables. Takes no parameters and returns
        nothing."""
        
        # Calls entities and assign again to reset them.
        self.entities()
        self.assign()
    
    def change_background_music(self, music_file):
        """This methed chages the background music and play new background music. Takes the new
        background music as an object parameter and returns nothing."""
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
            
    def freeze_and_sfx(self, sound, length, continue_playing):
        """This method freezes the game and plays a sound effect. Takes the sound effect to play,
        duration of freeze, and whether to continue playing backgroun music afterwards as a
        object, integer, and boolean parameter respective. Returns nothing."""
        
        # Checks if background music will stop permanently.
        if continue_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.stop()
        
        # Plays sfx and freezes program.
        sound.play()
        time.sleep(length)
        
        # Unpauses background music if necessary.
        if continue_playing:
            pygame.mixer.music.unpause()
        
    def update_game(self):
        """This method updates the game entities with the player's selected option. Takes no
        parameters and returns nothing."""
        
        # Checks how many players and sets difficulty of game.
        if self.__selected_players == 0:
            self.__game_player1.change_platform_size(self.__selected_difficulty)
            self.__game_player1.set_platform_pos((400, 580))
            self.__game_player2.remove_platform()
        elif self.__selected_players == 1:
            self.__game_player1.change_platform_size(self.__selected_difficulty)
            self.__game_player2.change_platform_size(self.__selected_difficulty)
        
    def update_game_over(self):
        """This method updates the game over entities with the result of the user's last game.
        Takes no parameters and returns nothing."""
        
        # Checks and updates result label for win or loss.
        if self.__hud.get_win():
            self.__win_sfx.play()
            self.__result_text.set_text("YOU WIN!")
        else:
            self.__lose_sfx.play()
            self.__result_text.set_text("YOU LOST!")
        
        # Update score label with final score.
        self.__score_text.set_text("Final Score: " + str(self.__hud.get_score()))

# Creates a game object.
game = main()
