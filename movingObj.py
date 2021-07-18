# player class
import random
import vector
import pygame
class Player:

    def __init__(self, surf):
        self.radius = 50
        self.pos = vector.Vector2(surf.get_width() / 2 - self.radius / 2, 200)
        self.speed = 200
        self.surf = surf
        self.casting = False

    def handle_input(self, dt):
        global B
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        mpos = pygame.mouse.get_pos()
        mbuttons = pygame.mouse.get_pressed()

        if keys[pygame.K_ESCAPE]:
            done = True
            return done
        if event.type == pygame.QUIT:
            done = True
            return done

        if mbuttons[0]:
            pygame.draw.line(self.surf, "white", (self.pos.x + self.radius / 2, self.pos.y), (mpos[0], mpos[1]), 2)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.casting = True

            init_vel = vector.Vector2(self.pos.x + self.radius / 2, self.pos.y) - vector.Vector2(mpos[0], mpos[1])
            B = Bobber(self.pos.x + self.radius / 2, self.pos.y, init_vel.x, init_vel.y, 10)

        if self.casting and B!=None:
            B.draw_bobber(self.surf, dt, self.pos, self.radius, event)

        # left and right movement
        if keys[pygame.K_d]:
            self.pos.x += self.speed * dt

        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     Fish(self.surf, 3, 300, 300)

        # this code doesn't allow you to go off screen
        if self.pos.x > self.surf.get_width() - self.radius:
            self.pos.x = self.surf.get_width() - self.radius
        if self.pos.x < 0:
            self.pos.x = 0

    def draw_player(self):
        pygame.draw.rect(self.surf, "white", (self.pos.x, self.pos.y, self.radius, self.radius))

class Bobber:
    def __init__(self, x, y, vel_x, vel_y, radius):
        self.velocity = vector.Vector2(vel_x, vel_y)
        self.color = vector.Vector3(255, 0, 0)
        self.radius = radius
        self.position = vector.Vector2(x, y)
        #self.mass = 0.001 * (4 / 3) * math.pi * (self.radius ** 3)
        self.acceleration = vector.Vector2(0, 0)
        #self.max_vel = 300
        self.change_hook = False


    def draw_bobber(self, surf, dt, player_pos, player_rad, event):
        global hook_x, hook_y
        self.position += self.velocity * dt

        self.acceleration = vector.Vector2(0, 0)

        if self.position.x > surf.get_width() - self.radius:
            self.position.x = surf.get_width() - self.radius

        if self.position.x < self.radius:
            self.position.x = self.radius

        if self.velocity.magnitude > 0:
            friction = 150 * dt
            self.velocity.y += friction
            if self.position.y > 250:
                self.velocity = vector.Vector2(0, 0)
                self.change_hook = True
                hook_x = self.position.x
                hook_y = self.position.y
            else:
                self.change_hook = False

        # if we get here, the bobber hit the water
        if self.change_hook:
            pygame.draw.line(surf, "white", (self.position), (hook_x, hook_y), 1)
            pygame.draw.circle(surf, "gold", (hook_x, hook_y), self.radius)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                hook_y += 10
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                hook_y -= 10
            if hook_y <= 250:
                hook_y = 250

        pygame.draw.line(surf, "white", (player_pos.x + player_rad / 2, player_pos.y), (self.position))
        pygame.draw.circle(surf, self.color, self.position, self.radius)
        
class Fish(Player):
    def __init__(self, surf, num_fish, radius):
        super().__init__(surf)
        self.radius = radius
        self.fish_list = []
        for i in range(num_fish):
            self.fish_list.append(random.randint(300, surf.get_height() - self.radius))

    # def update(self, dt):
    #     for i in self.fish_list:
    #         self.pos.x += 30 * dt

    # def draw(self, speed):
    #     for fish in self.fish_list:
    #         pygame.draw.circle(self.surf, "green", (0 + speed, fish), self.radius)

class BoringFish(Fish):
    def __init__(self, surf, num_fish, radius):
        super().__init__(surf, num_fish, radius)
        
    def draw(self, speed):
        for fish in self.fish_list:
            pygame.draw.circle(self.surf, "green", (0 + speed, fish), self.radius)