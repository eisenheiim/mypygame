import pygame
from sys import exit
from random import randint

def player_animation():
    global player_index,player_surf
    if player_rect.bottom<300:
        player_surf=player_jump
    else:
        player_index+=0.1
        if player_index>=len(player_walk):player_index=0
        player_surf=player_walk[int(player_index)]


def display_score():

    current_time=(pygame.time.get_ticks()//1000)-start
    score_surf=test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x-=5 #we are moving the obstacles
            if obstacle.bottom==300:screen.blit(snail_surface,obstacle) #if it is a snail
            else:     screen.blit(fly_surf,obstacle) #else, fly.
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>0]
        return obstacle_list
    else: return []
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

start=0
score=0
pygame.init() #initializing pygame

screen=pygame.display.set_mode((800,400))

pygame.display.set_caption('runner') #we r titling our display.

clock=pygame.time.Clock()

test_font=pygame.font.Font('font/Pixeltype.ttf',50) #font and font size

sky_surface=pygame.image.load('graphics/Sky.png').convert() #top left corner is 0,0
#any new image that imported is a new surface.

ground_surface=pygame.image.load('graphics/Ground.png').convert()#convert olmazsa blit her seferinde format dönüşümü yapar.

#text_surface=test_font.render("My game", True,(64,64,64)) #turns text into a surface
#text_rect=text_surface.get_rect(bottomright=(450,50))

snail_frame1=pygame.image.load('graphics/snail/snail1.png').convert_alpha()#convert ekran ve görüntünün piksel formatlarını ayarlar. png gibi şeffaflık varsa alpha kullanılır.
snail_frame2=pygame.image.load('graphics/snail/snail2.png').convert_alpha()#convert ekran ve görüntünün piksel formatlarını ayarlar. png gibi şeffaflık varsa alpha kullanılır.
snail_frames=[snail_frame1,snail_frame2]
snail_frame_index=0
snail_surface=snail_frames[snail_frame_index]
fly_surf= pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_surf2= pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames=[fly_surf,fly_surf2]
fly_frame_index=0
fly_surf=fly_frames[fly_frame_index]

obstacle_rect_list=[]

player_walk1=pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2=pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk=[player_walk1,player_walk2]
player_index=0
player_jump=player_walk2=pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf=player_walk[player_index]
player_rect=player_surf.get_rect(midbottom=(80,300)) #everything is much more easier with rect. collision,replacement of surface etc.


player_stand=pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand= pygame.transform.rotozoom(player_stand,0,2)#it can do both turnin or resizing.
player_stand_rect=player_stand.get_rect(center=(400,200))


#we can move surface using rectangle.
gameactive=True
grav=0

game_name=test_font.render("Run Forest Run!", False,(111,196,169))
name_rect=game_name.get_rect(center=(400,80))

game_message=test_font.render('Press space to run',False,(111,196,169))
game_message_rect=game_message.get_rect(center=(400,340))

#TIMER
obstacle_timer=pygame.USEREVENT+1 #outside of built-in events in pygame like keyup,keydown
#you can also create your own custom events. it is mostly used for periodic events.
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)


while True:
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            exit() #so instead of quit method steping in while loop constantly, exit finishes everything.
        if gameactive:
            if event.type==pygame.MOUSEBUTTONDOWN: #when mouse is moved
                if player_rect.collidepoint(event.pos): #if mouse is clicked on the character
                    grav = -10
            if event.type==pygame.KEYDOWN: #if any button is pressed
                if event.key==pygame.K_SPACE and player_rect.bottom==300:
                    grav = -10
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                gameactive= True
                start=pygame.time.get_ticks()//1000


        if gameactive:
            if event.type==obstacle_timer : #we periodically add new obstacles to screen and append to list.
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900,1100),210)))

            if event.type==snail_animation_timer:
                if snail_frame_index==0:snail_frame_index=1
                else: snail_frame_index=0
                snail_surf=snail_frames[snail_frame_index]
            if event.type==fly_animation_timer:
                if fly_frame_index==0:fly_frame_index=1
                else: fly_frame_index=0
                fly_surf=fly_frames[fly_frame_index]
    if gameactive:
        screen.blit(sky_surface,(0,0)) #0,0 top left.
        screen.blit(ground_surface, (0,300))
        #pygame.draw.rect(screen,'#d0e9dc',text_rect,30)#you r using rect object to put your rectangle. now, they ll move together.

        #pygame.draw.line(screen,"Gold",[0,0],pygame.mouse.get_pos(),10)

        #pygame.Rect(left,top,width,height)
        #pygame.draw.ellipse(screen,"Brown",pygame.Rect(50,200,100,200))



        #screen.blit(text_surface,text_rect)

        #screen.blit(snail_surface,snail_rect)
        #snail_rect.x -= 4
        score=display_score()

        #PLAYER PART
        screen.blit(player_surf,player_rect)
        player_animation()
        grav+=0.4

        player_rect.y+=grav

        if player_rect.bottom>=300: player_rect.bottom=300
        #if snail_rect.right <0: snail_rect.left=800 #when snail moves out of screen it appears again from right.

        #if player_rect.colliderect(snail_rect):print("collision") #result it 1 or 0.    #draw all our elements and update everything.


        #OBSTACLE MOVEMENT
        obstacle_rect_list=obstacle_movement(obstacle_rect_list)
        #COLLISION
        gameactive=collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,name_rect)
        obstacle_rect_list.clear()

        player_rect.midbottom=(80,300) #so that whenever game strats again player is on the ground
        grav=0
        score_message=test_font.render(f'Your score is:{score}',False,(111,169,169))
        scoremes_rect=score_message.get_rect(center=(400,330))
        if score==0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,scoremes_rect)

    pygame.display.update()
    clock.tick(60) #while true loop shouldnt run faster than 60 seconds
