import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, constraint, speed):
        super().__init__()
        self.sprite = pygame.image.load('../assets/player.png').convert_alpha()
        self.rect = self.sprite.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint

    def get_input(self):
        inputs = pygame.key.get_pressed()

        if inputs[pygame.K_RIGHT]:
            self.rect += self.speed
        elif inputs[pygame.K_LEFT]:
            self.rect -= self.speed
        
        if inputs[pygame.K_SPACE]:
            self.shoot_laser()
        
    def shoot_laser(self):
        print('shoot')

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
    
    def update(self):
        self.get_input()
        self.constraint