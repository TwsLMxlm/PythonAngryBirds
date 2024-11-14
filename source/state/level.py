__author__ = 'marble_xu'
# 关卡文件，管理关卡的初始化、游戏元素的加载、物理模拟、状态管理、得分系统、绘制和更新逻辑等。
import os
import json
import math
import pygame as pg
from .. import tool
from .. import constants as c
from ..component import button, physics, bird, pig, block
from .. import allMenu
# import time

bold_font = pg.font.SysFont("arial", 30, bold=True) # 字体设置

def vector(p0, p1):
    """Return the vector of the points
       p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)

def unit_vector(v):
    """Return the unit vector of the points
       v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)

# 关卡初始化与重置
class Level(tool.State):
    def __init__(self): # 继承自 tool.State，这是一个状态类，用于管理游戏的某个关卡
        tool.State.__init__(self)
        self.player = None

    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.reset()    # 加载或重置关卡

    # 加载或重置关卡，重置关卡状态，重新加载地图、背景、鸟、猪、方块等元素。
    def reset(self):
        self.score = 0    #! 设0，各关卡分数不继承
        # self.score = self.game_info[c.SCORE] 
        self.state = c.IDLE
        self.physics = physics.my_phy
        self.physics.reset(self)
        self.load_map()
        self.setup_background()
        self.setup_buttons()
        self.setup_sling()
        self.setup_birds()
        self.setup_pigs()
        self.setup_blocks()
        self.over_timer = 0

    # 地图加载与背景设置，通过读取 .json 文件加载关卡地图数据（包括鸟、猪、方块等的位置和类型）。
    def load_map(self):
        map_file = 'level_' + str(self.game_info[c.LEVEL_NUM]) + '.json'
        file_path = os.path.join('source', 'data', 'map', map_file)
        f = open(file_path)
        self.map_data = json.load(f)
        f.close()

    # 设置关卡背景图像，并根据缩放倍数调整背景的大小。
    def setup_background(self):
        self.background = tool.GFX['background']
        self.bg_rect = self.background.get_rect()
        self.background = pg.transform.smoothscale(self.background, 
                                    (int(self.bg_rect.width*c.BACKGROUND_MULTIPLER),
                                    int(self.bg_rect.height*c.BACKGROUND_MULTIPLER)))
        self.bg_rect = self.background.get_rect()
        self.bg_rect.y = -40

    # 设置 UI 按钮
    def setup_buttons(self):
        self.buttons = []
        self.buttons.append(button.Button(5, c.BUTTON_HEIGHT, c.NEXT_BUTTON))
        self.buttons.append(button.Button(70, c.BUTTON_HEIGHT, c.REPLAY_BUTTON))
    # 设置弹弓图像及其位置，用于发射小鸟。
    def setup_sling(self):
        rect_list = [(50, 0, 70, 200), (0, 0, 60, 200)]

        image = tool.get_image(tool.GFX['sling'], *rect_list[0], c.BLACK, 1)
        self.sling1_image = image
        self.sling1_rect = image.get_rect()
        self.sling1_rect.x = 138
        self.sling1_rect.y = 420

        image = tool.get_image(tool.GFX['sling'], *rect_list[1], c.BLACK, 1)
        self.sling2_image = image
        self.sling2_rect = image.get_rect()
        self.sling2_rect.x = 120
        self.sling2_rect.y = 420
        
        self.sling_click = False
        self.mouse_distance = 0
        self.sling_angle = 0
    # 加载并设置所有鸟的初始位置及其类型。
    def setup_birds(self):
        self.birds = []
        y = c.GROUND_HEIGHT

        for i, data in enumerate(self.map_data[c.BIRDS]):
            x = 120 - (i*35)
            tmp = bird.create_bird(data[c.TYPE], x, y)
            if tmp:
                self.birds.append(tmp)
        self.bird_path = []
        self.bird_old_path = []
        self.active_bird = None
        self.select_bird()
    # 加载猪并将其添加到物理引擎中。
    def setup_pigs(self):
        for data in self.map_data[c.PIGS]:
            tmp = pig.create_pig(data[c.TYPE], data['x'], data['y'])
            if tmp:
                self.physics.add_pig(tmp)
    # 设置方块
    def setup_blocks(self):
        for data in self.map_data[c.BLOCKS]:
            if c.DIRECTION in data:
                direction = data[c.DIRECTION]
            else:
                direction = 0
            tmp = block.create_block(data['x'], data['y'], data[c.MATERIAL],
                              data[c.SHAPE], data[c.TYPE], direction)
            if tmp:
                self.physics.add_block(tmp)

    # 更新关卡的状态，包括处理用户输入、更新物理世界、检查游戏状态，并最终将新的画面绘制到屏幕上
    def update(self, surface, current_time, mouse_pos, mouse_pressed):
        self.game_info[c.CURRENT_TIME] = self.current_time = current_time
        self.handle_states(mouse_pos, mouse_pressed)    # 根据玩家的输入（mouse_pos 和 mouse_pressed）来处理当前游戏状态的变化
        self.check_game_state() # 检查游戏状态
        self.draw(surface)  # 绘制到屏幕
    
    # 检查当前的游戏状态，并根据玩家的操作更新相应的逻辑。
    def handle_states(self, mouse_pos, mouse_pressed):
        if self.state == c.IDLE:
            self.handle_sling(mouse_pos, mouse_pressed)
        elif self.state == c.ATTACK:
            if self.active_bird.state == c.DEAD:
                self.active_bird = None
                self.select_bird()
                self.swith_bird_path()
                self.state = c.IDLE
        elif self.state == c.OVER:
            if self.over_timer == 0:
                self.over_timer = self.current_time

        for bird in self.birds:
            bird.update(self.game_info, self, mouse_pressed)
        self.physics.update(self.game_info, self, mouse_pressed)

        self.check_button_click(mouse_pos, mouse_pressed)

    # 在游戏中选择当前活动的小鸟
    def select_bird(self):
        if len(self.birds) > 0:
            self.active_bird = self.birds[0]
            self.active_bird.update_position(130, 426)

    # 弹弓操作与小鸟发射，当玩家按下鼠标并拖拽时，控制弹弓的拉动和松开以发射小鸟。
    def handle_sling(self, mouse_pos, mouse_pressed):
        if not mouse_pressed:
            if self.sling_click:
                self.sling_click = False
                xo = 154
                yo = 444
                
                # 小鸟发射音效
                sound_channel = pg.mixer.Channel(1)
                sound_channel.stop()
                sound_channel = pg.mixer.Channel(1)
                sound = pg.mixer.Sound(c.SOUND[5])
                sound.set_volume(c.SOUND_VOLUME)
                sound_channel.play(sound)  # 播放新的音效
                tool.load_sound(c.SOUND[5])
                
                # 将小鸟添加到物理世界中，带有初始发射距离和角度
                self.physics.add_bird(self.active_bird, self.mouse_distance,
                                      self.sling_angle, xo, yo)
                self.active_bird.set_attack()   # 设置小鸟的状态为攻击
                self.birds.remove(self.active_bird) # 从待发射小鸟列表中移除当前小鸟
                self.physics.enable_check_collide() # 开启碰撞检测
                self.state = c.ATTACK   # 切换状态到攻击模式
        elif not self.sling_click:
            if mouse_pos:
                mouse_x, mouse_y = mouse_pos
                if (mouse_x > 100 and mouse_x < 250 and 
                    mouse_y > 370 and mouse_y < 550):
                    self.sling_click = True

    # 绘制游戏中的弹弓、当前选中的小鸟，以及根据鼠标的位置控制弹弓的拉动和小鸟的移动
    def draw_sling_and_active_bird(self, surface):
        # 设置弹弓的初始位置与参数
        sling_x, sling_y = 135, 450
        sling2_x, sling2_y = 160, 450   # 弹弓的两个固定端点位置
        rope_length = 90    # 弹弓的绳子最大长度，限制小鸟可以拉动的最大距离
        bigger_rope = 102   # 用于绘制绳子的一个扩展长度，视觉上让绳子看起来更长
        # 检查是否点击了弹弓
        if self.sling_click:
            # 弹弓音效
            tool.load_sound(c.SOUND[3])
            # pg.mixer.Sound(c.SOUND[3]).set_volume(c.SOUND_VOLUME) 
            # pg.mixer.Sound(c.SOUND[3]).play()
            
            mouse_x, mouse_y = pg.mouse.get_pos()
            v = vector((sling_x, sling_y), (mouse_x, mouse_y))
            uv_x, uv_y = unit_vector(v)
            mouse_distance = tool.distance(sling_x, sling_y, mouse_x, mouse_y)
            pu = (uv_x * rope_length + sling_x, uv_y * rope_length + sling_y)
            
            if mouse_distance > rope_length:
                mouse_distance = rope_length
                pux, puy = pu
                pux -= 20
                puy -= 20
                pul = pux, puy
                pu2 = (uv_x * bigger_rope + sling_x, uv_y * bigger_rope + sling_y)
                pg.draw.line(surface, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
                self.active_bird.update_position(pux, puy)
                self.active_bird.draw(surface)
                pg.draw.line(surface, (0, 0, 0), (sling_x, sling_y), pu2, 5)
                
            else:
                mouse_distance += 10
                pu3 = (uv_x * mouse_distance + sling_x, uv_y * mouse_distance + sling_y)
                pg.draw.line(surface, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
                self.active_bird.update_position(mouse_x - 20, mouse_y - 20)
                self.active_bird.draw(surface)
                pg.draw.line(surface, (0, 0, 0), (sling_x, sling_y), pu3, 5)

            # Angle of impulse 计算小鸟发射的角度
            dy = mouse_y - sling_y
            dx = mouse_x - sling_x
            if dx == 0:
                dx = 0.00000000000001
            self.sling_angle = math.atan((float(dy))/dx)
            # 更新发射力度
            if mouse_x < sling_x + 5:
                self.mouse_distance = mouse_distance
            else:
                self.mouse_distance = -mouse_distance
        else:
            pg.draw.line(surface, (0, 0, 0), (sling_x, sling_y-8), (sling2_x, sling2_y-7), 5)
            if self.active_bird.state == c.IDLE:
                self.active_bird.draw(surface)

    # 检查按钮点击事件，并根据玩家的输入执行相应的操作
    def check_button_click(self, mouse_pos, mouse_pressed):
        if mouse_pressed and mouse_pos:
            for button in self.buttons:
                if button.check_mouse_click(mouse_pos):
                    if button.name == c.NEXT_BUTTON:
                        if self.game_info[c.LEVEL_NUM] < c.SUM_LEVEL_NUM:
                            self.game_info[c.LEVEL_NUM] += 1
                            self.reset()
                        elif self.game_info[c.LEVEL_NUM] >= c.SUM_LEVEL_NUM:
                            self.game_info[c.LEVEL_NUM] = c.START_LEVEL_NUM
                            self.reset()
                        # print(self.game_info[c.LEVEL_NUM])
                    elif button.name == c.REPLAY_BUTTON:
                        self.reset()

    # 更新分数
    def update_score(self, score):
        self.score += score
    # 胜利检查
    def check_victory(self):
        if len(self.physics.pigs) > 0:
            return False
        return True
    # 失败检查
    def check_lose(self):
        if len(self.birds) == 0 and len(self.physics.birds) == 0:
            return True
        return False

    # 游戏状态检查，检查当前关卡状态是否结束（胜利或失败），并根据结果切换到下一个关卡或重新加载。
    def check_game_state(self):
        # 检查当前关卡的状态是否为 OVER（结束状态）
        if self.state == c.OVER:   
            # 通过计时器 over_timer 来判断关卡结束后是否已经过了 1 秒（1000 毫秒），为关卡结束增加了一个短暂的延迟
            if (self.current_time - self.over_timer) > 1000:    
                self.done = True
        # 检查是否胜利
        elif self.check_victory() and self.state != c.WAIT_STATE:
            # 进入等待状态，延迟1秒后再显示胜利界面
            self.state = c.WAIT_STATE
            self.over_timer = self.current_time  # 记录当前时间
        # 检查胜利是否经过1秒
        elif self.state == c.WAIT_STATE:
            if (self.current_time - self.over_timer) > 1000:  # 等待2秒
                if self.game_info[c.LEVEL_NUM] < c.SUM_LEVEL_NUM:
                    self.game_info[c.LEVEL_NUM] += 1    # 如果胜利了，关卡号加 1，准备进入下一关卡
                elif self.game_info[c.LEVEL_NUM] >= c.SUM_LEVEL_NUM:
                    self.game_info[c.LEVEL_NUM] = c.START_LEVEL_NUM
                self.update_score(len(self.birds) * 10000)  # 更新分数，每只未使用的小鸟加 10000 分
                self.game_info[c.SCORE] = self.score    #! 将当前分数保存到 self.game_info 中，以便在后续关卡或游戏状态中使用
                # print(self.game_info[c.SCORE])
                if c.GAME_MODE:
                    self.next,self.state = allMenu.draw_level_cleared(self.game_info[c.SCORE],len(self.birds)) # 绘制胜利界面，并设置状态
                else:
                    self.next = c.LEVEL # 设置 self.next 为 c.LEVEL，表示游戏将进入下一个关卡
                    self.state = c.OVER # 将状态设为 OVER，表示当前关卡结束，触发结束的逻辑
        # 检查是否失败
        elif self.check_lose():
            if c.GAME_MODE:
                self.next,self.state = allMenu.draw_level_failed()
            else:
                self.next = c.LEVEL # 如果玩家失败了，设置 self.next = c.LEVEL，表示游戏将重置当前关卡。
                self.state = c.OVER # 将状态设为 OVER，触发结束逻辑

    # 切换小鸟的飞行轨迹：保存当前小鸟的飞行路径，并重置当前路径
    def swith_bird_path(self):
        self.bird_old_path = self.bird_path.copy()
        self.bird_path = []

    # 绘制小鸟的飞行轨迹
    def draw_bird_path(self, surface, path):
        for i, pos in enumerate(path):
            if i % 3 == 0:
                size = 4
            elif i % 3 == 1:
                size = 5
            else:
                size = 6
            pg.draw.circle(surface, c.WHITE, pos, size, 0)

    # 绘制与更新，绘制背景、鸟、猪、弹弓等元素。
    def draw(self, surface):
        surface.fill(c.GRASS_GREEN) # 背景填充，填充空白区域
        surface.blit(self.background, self.bg_rect) # 绘制游戏背景图像，位置由 self.bg_rect 控制
        for button in self.buttons: # 遍历所有按钮，并调用每个按钮的 draw() 方法，将其绘制到 surface 上
            button.draw(surface)

        # 绘制分数
        score_font = bold_font.render("SCORE:", 1, c.RED)   # 创建一个包含文字“SCORE:” 的图像对象
        number_font = bold_font.render(str(self.score), 1, c.RED)   # 显示玩家当前的得分
        surface.blit(score_font, (c.SCREEN_WIDTH - 200, c.BUTTON_HEIGHT))   # 将这两段文本分别绘制到屏幕的右侧对应位置
        surface.blit(number_font, (c.SCREEN_WIDTH - 100, c.BUTTON_HEIGHT))

        # 绘制小鸟的轨迹
        self.draw_bird_path(surface, self.bird_old_path)
        self.draw_bird_path(surface, self.bird_path)

        # 绘制弹弓和当前小鸟
        surface.blit(self.sling1_image, self.sling1_rect)
        self.draw_sling_and_active_bird(surface)
        # 绘制所有小鸟
        for bird in self.birds:
            bird.draw(surface)
        
        # 绘制弹弓的第二部分
        surface.blit(self.sling2_image, self.sling2_rect)

        # 绘制物理世界中的物体
        self.physics.draw(surface)