__author__ = 'marble_xu'
# 主函数执行文件
import pygame as pg
from . import tool  # 从当前包中导入 tool 模块，tool 包含了一些工具类或控制游戏流程的逻辑
from . import constants as c    # 从当前包中导入 constants 模块，constants 模块用于定义一些常量，比如游戏中的关卡名称、窗口大小、颜色等
from .state import level    # 从 state 包中导入 level 模块，state 可能是一个用于管理游戏状态的包，level 模块可能负责某个特定的游戏关卡
from . import allMenu # 从当前包中导入menu模块，menu 包含了游戏的菜单界面

def main():
    game = tool.Control()   # 创建一个 Control 对象
    state_dict = {c.LEVEL: level.Level()}   # state_dict 是一个字典，用来存储游戏状态。它的键是 c.LEVEL，值是 level.Level()。
    game.setup_states(state_dict, c.LEVEL)  # 初始化游戏状态，将所有可能的游戏状态传递给 game 对象进行初始化
    pg.init()   # pygame 初始化
    allMenu.loading()  # 调用 allMenu 类的 loading()方法，启动加载界面
    allMenu.start_menu()  # 调用 allMenu 类的 start_menu()方法，启动开始界面
    game.main() # 调用Control 类的 main() 方法，启动游戏的主循环
