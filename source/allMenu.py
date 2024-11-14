import pygame
import sys
import time
from pygame.locals import QUIT, KEYDOWN, K_KP_ENTER, K_ESCAPE
from . import constants as c
from . import tool
from .state import level

pygame.init()
screen = pygame.display.set_mode(c.SCREEN_SIZE)   # 创建 1200x650 像素的窗口
# 三星
stars = pygame.image.load("resources/images/stars-edited.png").convert_alpha()
rect = pygame.Rect(0, 0, 200, 200)
star1 = stars.subsurface(rect).copy()
rect = pygame.Rect(204, 0, 200, 200)
star2 = stars.subsurface(rect).copy()
rect = pygame.Rect(426, 0, 200, 200)
star3 = stars.subsurface(rect).copy()
# 按钮图片
buttons = pygame.image.load("resources/images/selected-buttons.png").convert_alpha()
# 失败->猪图片
pig_happy = pygame.image.load("resources/images/pig_failed.png").convert_alpha()
# 重玩
rect = pygame.Rect(24, 4, 100, 100)
replay_button = buttons.subsurface(rect).copy()
# 下一关
rect = pygame.Rect(142, 365, 130, 100)
next_button = buttons.subsurface(rect).copy()
# 返回菜单
rect = pygame.Rect(142, 110, 130, 110)
back_button = buttons.subsurface(rect).copy()
# 开始游戏
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()

# 字体设置
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)

def show_text(surface_handle, pos, text, color, font_bold=False, font_size=30, font_italic=False):
    """
    Function:文字处理函数
    Input：surface_handle：surface句柄
           pos：文字显示位置
           color:文字颜色
           font_bold:是否加粗
           font_size:字体大小
           font_italic:是否斜体
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-04-15
    """
    # 获取系统字体，并设置文字大小
    cur_font = pygame.font.SysFont("arial", font_size)

    # 设置是否加粗属性
    cur_font.set_bold(font_bold)

    # 设置是否斜体属性
    cur_font.set_italic(font_italic)

    # 设置文字内容
    text_fmt = cur_font.render(text, 1, color)

    # 绘制文字
    surface_handle.blit(text_fmt, pos)

# 判断一个点是否在给定的矩形区域内
def is_rect(pos, rect): 
    x, y = pos  # 提取点的x和y坐标
    rx, ry, rw, rh = rect
    if (rx <= x <= rw) and (ry <= y <= rh):
    # if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
        return True # 如果点在矩形内，返回True
    return False    # 否则返回False

# 加载（loading）动画
def loading(): 
    screen = pygame.display.set_mode(c.SCREEN_SIZE)    # 设置一个窗口，窗口大小为 955x537 像素
    init_background = pygame.image.load(
        "resources/images/mainPicture.jpg").convert_alpha()   # 加载背景图片，使用 .convert_alpha() 来优化加载的透明度
    init_background = pygame.transform.smoothscale(init_background, c.SCREEN_SIZE)
    pygame.display.set_caption('掌上怒鸟~Angry Birds')    # 设置窗口标题
    temp = 0
    flag = 0
    clock = pygame.time.Clock()  # 用于控制帧率
    
    while True:
        # 处理 Pygame 的事件队列，确保当用户关闭窗口时，程序可以正常退出
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(init_background, (0, 0))    # 绘制背景
        text = u"Loading" + temp * u"."
        show_text(screen, (c.SCREEN_WIDTH-200, c.SCREEN_HEIGHT-100), text, (255, 255, 255), True)  # 动态显示 "Loading" 文字
        # 控制点号数量
        temp += 1
        if temp == 4:
            temp = 0
            flag += 1
            if flag == 3:
                # time.sleep(2) # 控制每帧的间隔时间
                clock.tick(2)   # 延时，设置帧率为 2 FPS
                return
        
        # time.sleep(0.5)
        pygame.display.update() # 更新显示内容
        clock.tick(2)  # 延时，设置每秒两帧更新

# 开始菜单界面
def start_menu():
    screen = pygame.display.set_mode(c.SCREEN_SIZE)
    menu_background = pygame.image.load(
        "resources/images/menu.jpg").convert_alpha()  # 加载菜单背景图片
    menu_background = pygame.transform.smoothscale(menu_background, c.SCREEN_SIZE)
    pygame.display.set_caption('掌上怒鸟~Angry Birds')    # 设置窗口标题

    # 开始按钮的坐标范围
    rect = (c.SCREEN_WIDTH/2-50, c.SCREEN_HEIGHT/2+75, c.SCREEN_WIDTH/2+50, c.SCREEN_HEIGHT/2+125) # 表示按钮的位置和大小，用于检测鼠标点击，矩形的左上角为 (395, 315)，右下角为 (495, 365)

    # 背景音乐
    tool.load_music(c.SONG[1],-1)

    clock = pygame.time.Clock() # 创建一个时钟对象，用于控制帧率
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 回车键开始游戏
            if event.type == KEYDOWN:
                if event.key == K_KP_ENTER:
                    return
                # 按ESC键退出游戏
                if event.key == K_ESCAPE:  
                    pygame.quit()
                    sys.exit()
            
            # 鼠标点击按钮开始游戏
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos, rect):
                    return

        # 调试模式
        if c.DEBUG:
                pygame.display.set_caption("pos: " + str(pygame.mouse.get_pos()))   # 在调试模式下，显示鼠标位置。
                
        # 绘制背景和更新屏幕
        screen.blit(menu_background, (0, 0))
        pygame.display.update()
        
        clock.tick(60)  # 将帧率限制为60帧每秒

# 绘制胜利界面
def draw_level_cleared(score,birds_left):
    clock = pygame.time.Clock() # 创建一个时钟对象，用于控制帧率
    level_cleared = bold_font3.render("Level Cleared!", 1, c.WHITE)
    score_level_cleared = bold_font2.render(str(score), 1, c.WHITE)
    tool.load_music(c.SOUND[1],0)
    rect = pygame.Rect(300, 0, 600, 800)
    pygame.draw.rect(screen, c.BLACK, rect)
    screen.blit(level_cleared, (450, 90))
    if (score >= c.STAR_1 and score <= c.STAR_2) or (birds_left > 0 and  birds_left <= 1):
        screen.blit(star1, (310, 190))
    if (score >= c.STAR_2 and score <= c.STAR_3) or (birds_left > 1 and  birds_left <= 2):
        screen.blit(star1, (310, 190))
        screen.blit(star2, (500, 170))
    if score >= c.STAR_3 or birds_left > 2:
        screen.blit(star1, (310, 190))
        screen.blit(star2, (500, 170))
        screen.blit(star3, (700, 200))
    screen.blit(score_level_cleared, (550, 400))
    screen.blit(back_button, (c.SCREEN_WIDTH/2-150, c.SCREEN_HEIGHT/2+125))  # 510, 480
    # screen.blit(replay_button, (c.SCREEN_WIDTH/2-150, c.SCREEN_HEIGHT/2+125))  # 510, 480
    screen.blit(next_button, (c.SCREEN_WIDTH/2+50, c.SCREEN_HEIGHT/2+125))    # 620, 480
    pygame.display.update()
    clock.tick(60)  # 将帧率限制为60帧每秒
    back_rect = (c.SCREEN_WIDTH/2-150, c.SCREEN_HEIGHT/2+125, c.SCREEN_WIDTH/2-50, c.SCREEN_HEIGHT/2+225) # 表示按钮的位置和大小，用于检测鼠标点击
    next_rect = (c.SCREEN_WIDTH/2+50, c.SCREEN_HEIGHT/2+125, c.SCREEN_WIDTH/2+150, c.SCREEN_HEIGHT/2+225)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                # 按ESC键退出游戏
                if event.key == K_ESCAPE:  
                    pygame.quit()
                    sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos,next_rect):    # 下一关
                    tool.load_music(c.SONG[2],-1)
                    return c.LEVEL,c.OVER   # 返回关卡及结束状态
                if is_rect(event.pos,back_rect):  # 返回菜单
                    tool.load_music(c.SONG[1],-1)
                    start_menu()    # 开始菜单
                    game = tool.Control()   # 创建一个 Control 对象
                    state_dict = {c.LEVEL: level.Level()}   # state_dict 是一个字典，用来存储游戏状态。它的键是 c.LEVEL，值是 level.Level()。
                    game.setup_states(state_dict, c.LEVEL)  # 初始化游戏状态，将所有可能的游戏状态传递给 game 对象进行初始化
                    game.main() # 调用Control 类的 main() 方法，启动游戏的主循环
                    return
                
            if c.DEBUG:
                pygame.display.set_caption("pos: " + str(pygame.mouse.get_pos()))   # 在调试模式下，显示鼠标位置。

# 绘制失败界面
def draw_level_failed():
    clock = pygame.time.Clock() # 创建一个时钟对象，用于控制帧率
    failed = bold_font3.render("Level Failed", 1, c.WHITE)
    tool.load_music(c.SOUND[2],0)   # 加载失败音效
    rect = pygame.Rect(300, 0, 600, c.SCREEN_HEIGHT)
    pygame.draw.rect(screen, c.BLACK, rect)
    screen.blit(failed, (c.SCREEN_WIDTH/2-120, 90))  # 450, 90
    screen.blit(pig_happy, (c.SCREEN_WIDTH/2-190, 120))  # (380, 120)
    screen.blit(replay_button, (c.SCREEN_WIDTH/2-50, c.SCREEN_HEIGHT/2+125))  # 520, 460
    pygame.display.update()
    clock.tick(60)  # 将帧率限制为60帧每秒
    replay_rect = (c.SCREEN_WIDTH/2-50, c.SCREEN_HEIGHT/2+125, c.SCREEN_WIDTH/2+50, c.SCREEN_HEIGHT/2+225) # 表示按钮的位置和大小，用于检测鼠标点击
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                # 按ESC键退出游戏
                if event.key == K_ESCAPE:  
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos,replay_rect):
                    tool.load_music(c.SONG[2],-1)
                    return c.LEVEL,c.OVER   # 返回关卡及结束状态
            if c.DEBUG:
                pygame.display.set_caption("pos: " + str(pygame.mouse.get_pos()))   # 在调试模式下，显示鼠标位置。
