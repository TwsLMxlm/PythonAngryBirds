__author__ = 'marble_xu'
# 工具文件，包含状态类State()，控制类Control()，
# 以及代码段，包含了一个计算两点间距离的函数、一个从精灵图中获取子图像的函数、一个加载目录中所有图像资源的函数，
# 以及 Pygame 的初始化和图像资源的加载。
import os
import json
from abc import abstractmethod
import pygame as pg
from . import constants as c
# from . import allMenu

# 状态类
class State():
    def __init__(self):
        self.start_time = 0.0       # 状态开始的时间
        self.current_time = 0.0     # 当前的时间
        self.done = False           # 状态是否完成
        self.next = None            # 下一个状态的名称
        self.persist = {}           # 用于在状态之间传递信息的数据字典
    
    # 用于设置状态的开始时间，并从 persist 字典中接收共享数据。
    @abstractmethod # 抽象方法，必须在子类中实现
    def startup(self, current_time, persist):
        '''abstract method'''

    # 重置 self.done 标志，表示状态已清理并准备好下一次使用
    def cleanup(self):
        self.done = False
        return self.persist
    
    # 负责在每一帧中更新状态，通常用于处理用户输入、更新游戏逻辑以及在屏幕上绘制内容。
    @abstractmethod # 抽象方法，必须在子类中实现
    def update(self, surface, keys, current_time):
        '''abstract method'''

# Control 类，负责管理游戏的核心循环、事件处理、状态切换和更新。
class Control():
    def __init__(self):
        self.screen = pg.display.get_surface()  # 获取当前的显示窗口的表面，用于之后在屏幕上进行绘制。
        self.done = False   # 游戏是否结束的标志，当设置为 True 时，主循环会退出。
        self.clock = pg.time.Clock()    # 创建一个时钟对象，用来控制帧率。
        self.fps = 60   # 每秒帧数（frames per second），用于限制游戏的帧率为 60 FPS。
        self.keys = pg.key.get_pressed()    # 获取当前按键的状态，键盘输入会存储在 self.keys 中。
        self.mouse_pos = None   # 存储鼠标位置，默认为 None，只有在鼠标点击时才更新。
        self.mouse_pressed = False  # 用来表示鼠标是否按下。
        self.current_time = 0.0 # 当前时间，使用 pygame.time.get_ticks() 更新。
        self.state_dict = {}    # 用来存储不同的游戏状态（state），每个状态都可能是一个关卡、主菜单、暂停画面等。
        self.state_name = None  # 用于存储当前游戏状态的名称。
        self.state = None       # 用于存储当前游戏状态的状态对象
        self.game_info = {c.CURRENT_TIME:0.0,
                          c.LEVEL_NUM:c.START_LEVEL_NUM,
                          c.SCORE:0}    # 记录当前游戏的信息：当前游戏时间、当前关卡号、分数。
 
    # 设置状态参数或初始化游戏场景
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]   # 根据初始状态名称获取并设置当前状态对象。
        self.state.startup(self.current_time, self.game_info)   # 调用当前状态的 startup() 方法，初始化状态。

    # 更新状态
    def update(self):
        self.current_time = pg.time.get_ticks() # 获取当前时间（以毫秒为单位），并更新 self.current_time。
        if self.state.done:
            self.flip_state()   # 状态切换
        self.state.update(self.screen, self.current_time, self.mouse_pos, self.mouse_pressed)   # 更新游戏状态并在屏幕上绘制游戏画面
        self.mouse_pos = None   # 重置 self.mouse_pos，避免在下一帧中错误使用之前的鼠标位置。

    # 状态切换：当一个状态完成后，通过 flip_state() 切换到下一个状态。
    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next    # 获取当前状态名称，并将其更新为下一个状态名称 (self.state.next)
        # 检查当前状态是否为胜利或失败界面，并确认用户输入
        persist = self.state.cleanup()  # 调用当前状态的 cleanup() 方法，执行清理工作并保存需要在状态之间传递的数据。
        self.state = self.state_dict[self.state_name]   # 根据新的状态名称从状态字典中获取对应的状态对象。
        self.state.startup(self.current_time, persist)  # 使用传递的数据（persist）初始化新状态。

    # 事件循环，负责处理所有的用户输入事件
    def event_loop(self):
        for event in pg.event.get():    # 获取所有的用户输入事件
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()    # 返回当前所有按键的状态，返回一个布尔列表，表示每个键是否被按下
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:    # 鼠标按下的事件，button == 1 表示左键
                self.mouse_pos = pg.mouse.get_pos() # 获取鼠标的当前位置 (x, y)，并将其赋值给 self.mouse_pos
                self.mouse_pressed = True   # 标记鼠标左键处于按下状态
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:  # 鼠标按键释放的事件
                self.mouse_pressed = False

    def main(self):
        load_music(c.SONG[2],-1)    # 加载关卡背景音乐
        while not self.done:    # 在 self.done 为 False 的情况下，持续运行游戏主循环
            self.event_loop()   # 处理所有的用户输入事件。
            self.update()   # 更新游戏状态并绘制游戏画面。
            pg.display.update() # 更新显示窗口，呈现最新的游戏画面。
            self.clock.tick(self.fps)   # 限制游戏帧率。
            if c.DEBUG:
                pg.display.set_caption("pos: " + str(pg.mouse.get_pos()))   # 在调试模式下，显示鼠标位置。
        print('game over')  # 当游戏循环结束后，打印 game over。

# 计算两个点 (xo, yo) 和 (x, y) 之间的欧几里得距离（直线距离）。
def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d

# 从一个大的图片（称为精灵图 sprite sheet）中提取子图像，并进行缩放。
def get_image(sheet, x, y, width, height, colorkey, scale):
        image = pg.Surface([width, height]) # 创建一个新的空白 Surface 对象，用来存放提取出的图像
        rect = image.get_rect()

        image.blit(sheet, (0, 0), (x, y, width, height))    # 使用 blit() 将 sheet 上的指定区域复制到新的 image 表面上
        image.set_colorkey(colorkey)    # 设置图像的透明色，这通常用于去除精灵图的背景
        image = pg.transform.scale(image,
                                   (int(rect.width*scale),
                                    int(rect.height*scale)))    # 将提取出的图像缩放到指定比例。
        return image

# 从指定的目录中加载所有支持的图像文件，并将它们存储在一个字典中，方便后续快速访问。
def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', '.jpg', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(directory):   # 获取目录中的所有文件。
        name, ext = os.path.splitext(pic)   # 获取文件名和扩展名，检查是否是支持的图像格式。
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))   # 加载图像文件
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img    # 将处理后的图像存储在字典 graphics 中，键是文件名，值是图像对象。
    return graphics

# 加载音乐方法
def load_music(song_file,times):
    pg.mixer.music.load(song_file)
    pg.mixer.music.set_volume(c.SONG_VOLUME)
    pg.mixer.music.play(times)

# 加载音效方法
def load_sound(song_file):
    sound = pg.mixer.Sound(song_file)
    sound.set_volume(c.SOUND_VOLUME)
    sound.play()
    
pg.init()   # 初始化 Pygame 模块，必须在使用 Pygame 功能前调用
pg.display.set_caption(c.ORIGINAL_CAPTION)  # 设置窗口标题，c.ORIGINAL_CAPTION 是从常量文件 c 中获取的游戏标题。
SCREEN = pg.display.set_mode(c.SCREEN_SIZE) # 设置游戏窗口的大小，c.SCREEN_SIZE 是从常量文件 c 中获取的屏幕尺寸。

# 初始化 Pygame 的音频模块
pg.mixer.init()
# 设置音频通道数（例如增加到 4 个通道）
pg.mixer.set_num_channels(4)

# 加载图像资源
GFX = load_all_gfx(os.path.join("resources","graphics"))    # 调用前面定义的函数，从 resources/graphics 目录加载所有图像文件