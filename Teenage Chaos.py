import pygame

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WIDTH,HEIGHT = screen.get_size()
pygame.display.set_caption("Teenage Chaos Demo")

# Clock for controlling FPS
clock = pygame.time.Clock()



#           GAME STATE
class GameState:
    def __init__(self):
        self.state = "explore"
        self.pre_state = None

    def change_state(self,new_state):
        self.pre_state = self.state
        self.state = new_state

    def return_to_previous(self):
        self.state = self.pre_state



#           SCENE CLASS
class Scene:
    def __init__(self):
        self.game = GameState()
        self.player = Player(50,500,500)
        self.obstacle = [Obstacle(50,100,500,2),Obstacle(50,100,700,3),Obstacle(50,100,100,4),Obstacle(50,100,250,1)]
        self.dialouge_tree = {
            "start_dialouge" :{
                "start" : {
                "text" : "Hello! How are you doing?",
                "options" : {
                    "1" : {"text" : "Good!", "next" : "end"},
                    "2" : {"text" : "Bad!", "next" : "end"}
                        }

            },

            "end" : {
                "text" : "Cool..."
            }
                              }}
        self.npc2_tree = {
            "start_dialouge": {
            "start" : {
            "text" : ["Hello! How are you doing?",
                      "I have a job for you! Are you willing to help me?"],
            "options" : {
                "1" : {"text" : "Yes!", "next" : "yes_path"},
                "2" : {"text" : "No!", "next" : "no_path"}
            }

            },

            "yes_path" : {"text" : ["Thanks! That means a lot to me!", "I just need you to pick up the blue cube for me!"],
                          "next" : "end"},

            "no_path" : {"text" : ["Ahhhh, well that's a shame!", "I don't really have anything else to say.....", "............", "You're a dick yk?"],
                         "next" : "end"},

            "end" : {
                "text" : ["Well....", "Bye!"]
            }
                              },

            "DuringQuest_dialouge" : {"start": {"text" : "Have you got the cube yet?", "next" : "end"},
                                      "end" : ""},

            "QuestFinished_dialouge" : {"start" : {"text" : ["Thank you SO MUCH!!!", "You're a legend man!"], "next" : "end"},
                                        "end" : ""}

            }

        self.npclinesquestbluebox = ["OMG!", "Thank you so much!",".","..","...","did you expect a reward...",".","..","...","get lost fool!"]


        self.npc = [NPC(50,800,800,self.dialouge_tree),NPC(50,1000,200,self.npc2_tree)]
        self.item = [Item(20,600,900,"blue cube")]
        self.quest = [Quest("blue cube",self.npc[0])]
        self.current_npc = None

    def collision_check(self):
        for obs in self.obstacle:
            if self.player.player_rect.colliderect(obs.obstacle_rect):
                self.player.player_x = obs.obstacle_x + obs.obstacle_size

    
    def dialouge_check(self,event):
        for npcs in self.npc:
            if self.player.player_rect.colliderect(npcs.npc_rect):
                if self.game.state == "explore":
                    if event.key == pygame.K_e:
                        self.current_npc = npcs
                        self.game.change_state("dialouge")

    
    def dialouge_close(self,event):
        if self.game.state == "dialouge":
            if event.key == pygame.K_o:
                self.current_npc = None
                self.game.change_state("explore")
    

    def item_pick(self,event):
        for itm in self.item:
            if self.game.state == "explore":
                if self.player.player_rect.colliderect(itm.item_rect):
                    if event.key == pygame.K_e:
                        itm.item_picked = True
                        self.player.player_items.append(itm.item_name)
                        self.quest[0].quest_check(self.player,itm,self.npclinesquestbluebox)
                        self.npc[0].dialouge_index = 0

    def update_scene(self,screen):
        # collision checks and functions
        self.player.movement_handling()
        
        for obs in self.obstacle:
            obs.obstacle_movement()

        self.collision_check()


        # draw stuff
    
        screen.fill((30,30,30))
        self.player.update_player()
        for obs in self.obstacle:
            obs.update_obstacle()
        for npcs in self.npc:
            npcs.update_npc()
        for itm in self.item:
            itm.item_update(screen)

    def scene_interactions(self,event):
        self.dialouge_check(event)
        self.dialouge_close(event)
        self.item_pick(event)





#           PLAYER CLASS

class Player(pygame.sprite.Sprite):
    def __init__(self,size,WIDTH,HEIGHT):
        self.player_size = size
        self.player_x = WIDTH
        self.player_y = HEIGHT
        self.player_speed = 5
        self.player_rect = pygame.Rect(self.player_x,self.player_y,self.player_size,self.player_size)
        self.player_items = []

    def movement_handling(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed
        if keys[pygame.K_UP]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
        self.player_rect.topleft = (self.player_x,self.player_y)

            
    def update_player(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.player_x, self.player_y, self.player_size, self.player_size))




#           OBSTACLE CLASS
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,size,WIDTH,HEIGHT,speed):
        self.obstacle_size = size
        self.obstacle_x = WIDTH
        self.obstacle_y = HEIGHT
        self.obstacle_speed = speed
        self.obstacle_rect = pygame.Rect(self.obstacle_x,self.obstacle_y,self.obstacle_size,self.obstacle_size)


    def obstacle_movement(self):
        if self.obstacle_x == 2000 or self.obstacle_x > 2000:
            self.obstacle_x -= 2100
        if self.obstacle_x < 2000:
            self.obstacle_x += self.obstacle_speed
        self.obstacle_rect.topleft = (self.obstacle_x,self.obstacle_y)



    def update_obstacle(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.obstacle_x, self.obstacle_y, self.obstacle_size, self.obstacle_size))




#           NPC CLASS
class NPC(pygame.sprite.Sprite):
    def __init__(self,size,WIDTH,HEIGHT,dialouge_tree):
        self.npc_size = size
        self.npc_x = WIDTH
        self.npc_y = HEIGHT
        self.npc_rect = pygame.Rect(self.npc_x,self.npc_y,self.npc_size,self.npc_size)
        self.dialouge = dialouge_tree
        self.current_node = "start"
        self.current_dialouge = "start_dialouge"
        self.selection_option = 0
        self.line_index = 0

    def dialouge_display(self,game,screen):
        #font shit
        font = pygame.font.SysFont("ocra",32)
        text_rect = pygame.Rect(0,800,1920,280)
        pygame.draw.rect(screen, (40, 40, 40), text_rect)
        #function shit
        node = self.dialouge[self.current_dialouge][self.current_node]
        if isinstance(node["text"],list):
            current_text = node["text"][self.line_index]
        else:
            current_text = node["text"]
        text = font.render(current_text,True,(255,255,255))
        if "options" in node:
            options_list = list(node["options"].items())
        screen.blit(text,text_rect)

        is_last_line = False

        if isinstance(node["text"], list):
            if self.line_index == len(node["text"]) - 1:
                is_last_line = True
        if isinstance(node["text"], str):
            is_last_line = True

        
        if "options" in node and is_last_line:
            y = 832
            for i, (key, option) in enumerate(options_list):
                if i == self.selection_option:
                    opt_text = f"> {option['text']}"
                    color = (255,255,0)
                else:
                    opt_text = f"  {option['text']}"
                    color = (255,255,255)
                opt_rend = font.render(opt_text,True,color,)
                screen.blit(opt_rend,(50,y))
                y += 32
        #if self.dialouge_index <= len(self.lines)-1:
        #    text = font.render(self.lines[self.dialouge_index],True,(255,0,0),None)
        #    screen.blit(text,text_rect)
        #if self.dialouge_index >= len(self.lines):
        #    game.return_to_previous()
        #    self.dialouge_index = 0
    def dialouge_switch(self,game,event):
        # variables
        node = self.dialouge[self.current_dialouge][self.current_node]
        if "options" in node:
            options_list = list(node["options"].items())
            max_index = len(options_list) - 1

        #functions shit
        if game.state == "dialouge":

            if event.key == pygame.K_SPACE:
                if isinstance(node["text"],list):
                    if self.line_index < len(node["text"])- 1:
                        self.line_index += 1
                    else:
                        if "next" in node:
                            self.current_node = node["next"]
                            self.line_index = 0
                            
                        elif "options" not in node:
                            game.return_to_previous()
                            self.current_node = "start"
                            self.line_index = 0
                            

                if isinstance(node["text"],str):
                    if "next" in node:
                        self.current_node = node["next"]
                        self.line_index = 0
                    elif "options" not in node and node.get("next") is None:
                        game.return_to_previous()
                        self.current_node = "start"
                        self.line_index = 0
                        

            is_last_line = False

            if isinstance(node["text"], list):
                if self.line_index == len(node["text"]) - 1:
                    is_last_line = True
            if isinstance(node["text"], str):
                is_last_line = True
                    

            if "options" in node and is_last_line:

                if event.key == pygame.K_DOWN:
                    self.selection_option = min(self.selection_option + 1, max_index)

                if event.key == pygame.K_UP:
                    self.selection_option = max(self.selection_option - 1, 0)

                elif event.key == pygame.K_RETURN:
                    key, option = options_list[self.selection_option]
                    self.current_node = option["next"]
                    self.selection_option = 0
                    self.line_index = 0

            

                

            
            

            
    def update_npc(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.npc_x, self.npc_y, self.npc_size, self.npc_size))







        


class Item(pygame.sprite.Sprite):
    def __init__(self,size,WIDTH,HEIGHT,itemname):
        self.item_size = size
        self.item_x = WIDTH
        self.item_y = HEIGHT
        self.item_picked = False
        self.item_rect = pygame.Rect(self.item_x,self.item_y,self.item_size,self.item_size)
        self.item_name = itemname

    def item_update(self,screen):
        if not self.item_picked:
            pygame.draw.rect(screen, (0,0,255), self.item_rect)

class Quest(pygame.sprite.Sprite):
    def __init__(self,itemname,npc):
        self.itemname = itemname
        self.quest_completed = False
        self.npc = npc
        self.npc_interacted = True

    def quest_check(self,player,item,newlines):
        if self.npc_interacted:
            npc.current_dialouge = "DuringQuest_dialouge"
            if self.itemname in player.player_items:
                self.quest_completed = True
                npc.current_dialouge = "QuestFinished_dialouge"

#Creating Scene Objects

scene1 = Scene()
current_scene = scene1

#           FUNCTIONS



# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            current_scene.scene_interactions(event)
            if current_scene.current_npc:
                current_scene.current_npc.dialouge_switch(current_scene.game,event)

            #dialouge_check(game,player,npc,event)
            #dialouge_close(game,event)
            #npc.dialouge_switch(game,event)
            #item_pick(game,player,item,event,npc)

    if current_scene.game.state == "explore":
        current_scene.update_scene(screen)

    elif current_scene.game.state == "dialouge":
        screen.fill((20,20,20))
        if current_scene.current_npc:
            current_scene.current_npc.dialouge_display(current_scene.game,screen)

    elif current_scene.game.state == "battle":
        screen.fill((50,50,50))
    
    pygame.display.flip()

pygame.quit()
print("SAFE")
