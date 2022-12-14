import pygame, sys
from random import choice
from player import Player
from alien import Alien
from laser import Laser
 
class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 3
        self.live_surf = pygame.image.load('./assets/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.font = pygame.font.Font('./assets/space_invaders.ttf',20)
        
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        
    def alien_setup(self, rows, cols, x_distance = 60, y_distance=48, x_offset= 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                if row_index == 0: alien_sprite = Alien('green',x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('yellow',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien =  choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,8,screen_height)
            self.alien_lasers.add(laser_sprite)

    def collision_checks(self):
            if self.player.sprite.lasers:
                for laser in self.player.sprite.lasers:
                    if pygame.sprite.spritecollide(laser,self.aliens,True):
                        laser.kill()
            
            if self.alien_lasers:
                for laser in self.alien_lasers:
                    if pygame.sprite.spritecollide(laser,self.player,False):
                        laser.kill()
                        self.lives -= 1
                        

            if self.aliens:
                for alien in self.aliens:
                    if pygame.sprite.spritecollide(alien,self.player,False):
                        self.lives = 0

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,10))

    def victory_message(self):
        if not self.aliens.sprites() and self.lives >= 1:
            victory_surf = self.font.render('You won',False,'Green')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def lost_message(self):
        if self.lives == 0:
            self.aliens.empty()
            self.alien_lasers.empty()
            self.player.sprite.lasers.empty()
            lost_surf = self.font.render('You lost',False,'Red')
            lost_rect = lost_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(lost_surf, lost_rect)

    def run(self):
        self.player.update()	
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        self.display_lives()

        self.alien_position_checker()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.victory_message()
        self.lost_message()
    

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    alienlaser = pygame.USEREVENT + 1
    pygame.time.set_timer(alienlaser,600)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alienlaser:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()
        #crt.draw()
            
        pygame.display.flip()
        clock.tick(60)