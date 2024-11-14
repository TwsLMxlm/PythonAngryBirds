__author__ = 'marble_xu'
# 全局常量文件，提供了游戏的各种配置、颜色定义、游戏状态、角色、物体、分数等信息
from . import file_utils

DEBUG = True   # 调试模式
GAME_MODE = True    # 游戏模式，True 为正常模式，False 为沉浸模式

# 设置游戏初始关卡及关卡数量
directory_path = "source/data/map"
file_extension = ".json"
START_LEVEL_NUM = 1 # 游戏初始关卡为 1
SUM_LEVEL_NUM = file_utils.count_files_in_directory(directory_path, file_extension)   # 游戏关卡数量

# 设置屏幕的宽度为 1200 像素，高度为 650 像素。
ZOOM = 1    # 整体缩放因子(停用)
SCREEN_HEIGHT = int(650*ZOOM)
SCREEN_WIDTH = int(1200*ZOOM)
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)  # 将屏幕宽度和高度作为一个元组，用于 Pygame 窗口设置。

GROUND_HEIGHT = int(550*ZOOM) # 地面的高度为 550 像素。

ORIGINAL_CAPTION = "掌上怒鸟 ~ Angry Birds"    # 游戏窗口的标题。

## COLORS ##
#                R    G    B
GRAY         = (100, 100, 100)
NAVYBLUE     = ( 60,  60, 100)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
FOREST_GREEN = ( 31, 162,  35)
GRASS_GREEN  = (130, 200, 100)
BLUE         = (  0,   0, 255)
SKY_BLUE     = ( 39, 145, 251)
YELLOW       = (255, 255,   0)
ORANGE       = (255, 128,   0)
PURPLE       = (255,   0, 255)
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK   = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)

BGCOLOR = WHITE # 背景颜色设置

# 缩放因子，这些常量定义了不同物体的缩放比例，用于调整背景、鸟和猪的大小比例。
BACKGROUND_MULTIPLER = 1*ZOOM    # 背景图像
BIRD_MULTIPLIER = 0.5*ZOOM   # 鸟类图像
NORMAL_PIG_MULTIPLIER = 0.4*ZOOM # 普通猪图像
BIG_PIG_MULTIPLIER = 0.8*ZOOM    # 大猪图像

# STATES FOR ENTIRE GAME 游戏状态常量
MAIN_MENU = 'main menu' # 主菜单
LOAD_SCREEN = 'load screen' # 加载界面
TIME_OUT = 'time out'   # 超时
GAME_OVER = 'game over' # 游戏结束
LEVEL = 'level' # 关卡进行中
WAIT_STATE = "wait_state"   # 等待状态

# GAME INFO DICTIONARY KEYS 游戏信息字典键
CURRENT_TIME = 'current time'   # 当前时间
LEVEL_NUM = 'level num' # 关卡号
SCORE = 'score' # 分数

# STATE 物体状态常量，表示游戏物体（如鸟或猪）的状态
IDLE = 'idle'   # 空闲
ATTACK = 'attack'   # 攻击 
OVER = 'over'   # 结束
DEAD = 'dead'   # 死亡
INIT_EXPLODE = 'init_explode'   # 初始爆炸
EXPLODE = 'explode' # 爆炸

# LEVEL NAME 关卡元素
MATERIAL = 'material'   # 材料
SHAPE = 'shape' # 形状
TYPE = 'type'   # 类型
DIRECTION = 'direction' # 方向
BIRDS = 'birds' # 鸟
PIGS = 'pigs'   # 猪
BLOCKS = 'blocks'   # 障碍物

# BIRD 鸟类信息，定义了不同鸟类的名称和它们的精灵图资源
BIRD_SHEET = 'angry_birds'  # 精灵图
RED_BIRD = 'red_bird'
BLUE_BIRD = 'blue_bird'
YELLOW_BIRD = 'yellow_bird'
BLACK_BIRD = 'black_bird'
WHITE_BIRD = 'white_bird'
EGG = 'egg'
BIG_RED_BIRD = 'big_red_bird'

# PIG 猪类信息，定义了猪的类型和它们的精灵图资源
PIG_SHEET = 'full-sprite'   # 精灵图
NORMAL_PIG = 'normal_pig'
BIG_PIG = 'big_pig'

# BLOCK INFO 方块信息，定义了游戏中各种方块的材料（玻璃、木材、石头）、形状（梁、圆形）、类型（如不同的梁的类型）以及方向（水平、垂直）
BLOCK_SHEET = 'block'   # 精灵图
# BLOCK MATERIAL 方块的材料
GLASS = 'glass'
WOOD = 'wood'
STONE = 'stone'
# SHAPE TYPE 形状
BEAM = 'beam'
CIRCLE = 'circle'
# BEAM SUBTYPE 梁亚型
BEAM_TYPE_1 = 1
BEAM_TYPE_2 = 2
BEAM_TYPE_3 = 3
BEAM_TYPE_4 = 4
BEAM_TYPE_5 = 5
BEAM_TYPE_6 = 6
# CIRCLE SUBTYPE 圆亚型
CIRCLE_TYPE_1 = 1
CIRCLE_TYPE_2 = 2
# DIRECTION 方向
HORIZONTAL = 0
VERTICAL = 1
# MASS TIMES  质量乘数，用于在游戏中调整每种材料的质量
GLASS_MASS_TIMES = 1
WOOD_MASS_TIMES = 2
STONE_MASS_TIMES = 4

#BUTTON 按钮信息，定义了按钮的高度、按钮的图像资源以及按钮的类型
BUTTON_HEIGHT = 10  # 按钮的高度
BUTTON_IMG = 'selected-buttons' # 按钮的图像资源
NEXT_BUTTON = 'next_button' # 下一关按钮
REPLAY_BUTTON = 'replay_button' # 重玩按钮

# SCORE 分数信息，定义了消灭鸟、猪和破坏形状的分数
BIRD_SCORE = 10000
PIG_SCORE = 5000
SHAPE_SCORE = 1000
STAR_1 = 10000
STAR_2 = 30000
STAR_3 = 50000

# 音乐音效文件目录
SONG = {
    1: 'resources/music/title_theme.wav',  # 开始菜单音乐
    2: 'resources/music/ambient_red_savannah.wav',  # 关卡菜单音乐
}
SOUND = {
    1: 'resources/music/level clear military a1.wav',  # 胜利音效
    2: 'resources/music/level failed piglets a1.wav',  # 失败音效
    3: 'resources/music/slingshot streched.wav',  # 弹弓音效
    4: 'resources/music/bird shot-a1.wav',  # 射击音效
    5: 'resources/music/bird 01 flying.wav' # 飞行音效
}
# 音乐音效音量
SONG_VOLUME = 0.5
SOUND_VOLUME = 1