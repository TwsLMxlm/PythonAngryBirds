# 本游戏是基于2D引擎库pymunk的pygame小项目，基于下面的PythonAngryBirds项目进行了bug修复及改进：
* 修复了游戏通过最后一关后闪退的BUG，现在通过最后一关后会重新跳转到第一关
* 改进了关卡检索逻辑，现在可以根据source/data/map中地图的json文件数量自动调整关卡数量
* 添加了游戏加载界面、开始菜单界面、胜利及失败界面
* 添加了游戏的音乐及音效，包括开始菜单和游戏界面BGM，弹弓音效和小鸟发射音效，胜利和失败界面音效
* 调整了游戏物理引擎参数，使其物理逻辑更符合实际
* 修改绝对路径为相对路径

# requirements
实现环境如下，可参考requirements.txt：
* Python 3.8
* Pygame 1.9.6
* Pymunk 5.5.0

# 以下是原项目介绍：
# PythonAngryBirds
a simple implementation of angrybirds using pygame and pymunk
* support three birds：red bird, blue bird, yellow bird, black bird and white bird
* suport three blocks: glass, wood and stone
* use json file to store level data (e.g. position of block and pig)
* TODO: support different pigs

# Requirement
* Python 3.7
* Python-Pygame 1.9
* Pymunk 5.5.0

# How To Start Game
$ python main.py

# How to Play
* use mouse to drag the bird, modify the direction, then release the mouse to shoot the bird

# Demo
![demo1](https://raw.githubusercontent.com/marblexu/PythonAngryBirds/master/resources/demo/demo1.png)
