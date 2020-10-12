import pygame
import random


# 全局变量
BACKGROUND_GROUND = (232, 232, 232)  # 窗口背景颜色
SCORE_TEXT_COLOR = (192, 192, 192)  # 分数文字颜色
TIP_TEXT_COLOR = (64, 64, 64)  # 提示文字颜色
SCREEN_RECT = pygame.Rect(0, 0, 640, 480)  # 窗口的大小
CELL_SIZE = 20      # 每一个格子的宽高
FOOD_UPDATE_EVENT = pygame.USEREVENT  # 食物更新事件标志
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1  # 蛇更新事件标志


class Label:
    """标签文本类"""
    def __init__(self, size=48, is_score=True):
        """
        初始化方法
        :param size:字体大小
        :param is_score:是否是显示得分的对象
        """
        self.font = pygame.font.SysFont('simhei', size)  # 黑体字
        self.is_score = is_score

    def draw(self, window, text):
        """绘制当前对象的内容"""
        # 渲染字体
        color = SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR
        text_surface = self.font.render(text, True, color)

        # 获取文本的矩形
        text_rect = text_surface.get_rect()

        # 获取游戏主窗口矩形
        window_rect = window.get_rect()

        if self.is_score:
            # 修改游戏得分位置显示的坐标，使其显示在窗口左下角
            text_rect.bottomleft = window_rect.bottomleft
        else:
            # 提示信息的显示坐标，使其显示在窗口中间
            text_rect.center = window_rect.center

        # 绘制文本内容到窗口
        window.blit(text_surface, text_rect)


class Food:
    def __init__(self):
        """初始化食物"""
        self.color = (255, 0, 0)  # 颜色初始为红色
        self.score = 10  # 默认得分为10分
        self.rect = (0, 0, CELL_SIZE, CELL_SIZE)  # 初始的显示位置

        # 初始化食物时随机分配一个位置
        self.random_rect()

    def draw(self, window):
        """使用当前食物的矩形，绘制实心圆形"""
        if self.rect.width < CELL_SIZE:  # 只要显示的矩形还小于单元格的大小，就继续放大
            self.rect.inflate_ip(2, 2)
        pygame.draw.ellipse(window, self.color, self.rect)

    def random_rect(self):
        """随机确定绘制食物的位置"""
        # 计算可用的行数和列数
        col = SCREEN_RECT.width / CELL_SIZE - 1
        row = SCREEN_RECT.height / CELL_SIZE - 1

        # 随机分配一个行和列，并计算行和列的x，y值
        x = random.randint(0, col) * CELL_SIZE
        y = random.randint(0, row) * CELL_SIZE

        # 重新生成绘制食物的矩形
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.rect.inflate_ip(-CELL_SIZE, -CELL_SIZE)  # 把创建好的矩形大小修改为0

        # 设置定时，时间到了之后要重新设置食物位置
        pygame.time.set_timer(FOOD_UPDATE_EVENT, 30000)


class Snake:
    """蛇类"""
    def __init__(self):
        """初始化蛇的数据"""
        self.dir = pygame.K_RIGHT  # 运动方向
        self.time_interval = 500  # 运动时间间隔500毫秒
        self.score = 0  # 游戏得分
        self.color = (64, 64, 64)  # 身体颜色—深灰色
        self.body_list = []  # 身体列表，列表内容为一个个矩形对象，对应于蛇的每一节

        for i in range(3):  # 初始的蛇有3节
            self.add_node()

    def reset_snake(self):
        """重置蛇的数据"""
        self.dir = pygame.K_RIGHT  # 运动方向
        self.time_interval = 500  # 运动时间间隔500毫秒
        self.score = 0  # 游戏得分
        self.body_list = []  # 身体列表
        self.body_list.clear()  # 清空列表
        for i in range(3):
            self.add_node()

    def add_node(self):
        """添加一节身体"""
        # 生成新的矩形对象
        if self.body_list:
            # 已经有身体了
            # 复制一份在body_list中0号索引的surface对象(列表的copy方法只能拷贝整个列表，这里的copy是pygame的方法)
            head = self.body_list[0].copy()
        else:
            # 还没有身体
            head = pygame.Rect(-CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

        # 根据移动方向，把新生成的头部放到恰当的位置
        if self.dir == pygame.K_RIGHT:  # 向右方向键
            head.x += CELL_SIZE
        elif self.dir == pygame.K_LEFT:  # 向左方向键
            head.x -= CELL_SIZE
        elif self.dir == pygame.K_UP:  # 向上方向键
            head.y -= CELL_SIZE
        elif self.dir == pygame.K_DOWN:  # 向下方向键
            head.y += CELL_SIZE
        # 把新生成的头部放到列表的最前面
        self.body_list.insert(0, head)

        # 定时更新身体
        pygame.time.set_timer(SNAKE_UPDATE_EVENT, self.time_interval)

    def draw(self, window):
        """绘制蛇的每一节身体"""
        for idx, rect in enumerate(self.body_list):
            pygame.draw.rect(
                window,
                self.color,
                rect.inflate(-2, -2),  # 缩小矩形区域，可以让蛇有分节的感觉
                idx == 0  # 蛇头绘制的边框不填充
            )

    def update(self):
        """移动蛇的身体"""
        # 备份移动之前的身体列表（用来蛇死后退回到上一步，这样蛇头就不会消失了，对用户显示更加友好）
        body_list_copy = self.body_list.copy()
        # 移动身体
        self.add_node()
        self.body_list.pop()

        # 判断是否死亡
        if self.is_dead():
            self.body_list = body_list_copy
            return False
        return True

    def change_dir(self, to_dir):
        """改变贪吃蛇的运动方向"""
        # 定义水平和垂直移动方向的元组
        hor_dirs = (pygame.K_RIGHT, pygame.K_LEFT)  # 水平方向
        ver_dirs = (pygame.K_UP, pygame.K_DOWN)  # 垂直方向

        # 判断当前运动方向及要修改的方向
        if self.dir in hor_dirs and to_dir not in hor_dirs or \
                self.dir in ver_dirs and to_dir not in ver_dirs:
            self.dir = to_dir

    def has_eat(self, food):
        """判断是否吃到了食物"""
        if self.body_list[0].contains(food.rect):
            # 蛇头和食物已经重叠
            self.score += food.score  # 修改得分

            # 修改移动间隔
            if self.time_interval > 100:
                self.time_interval -= 50

            # 添加一节身体
            self.add_node()
            return True
        return False

    def is_dead(self):
        """判断是否已经死亡，如果死亡则返回True"""
        head = self.body_list[0]

        # 判断蛇头是否不在窗口里
        if not SCREEN_RECT.contains(head):
            return True

        # 判断蛇头是否与身体重叠
        for body in self.body_list[1:]:
            if head.contains(body):
                return True
        return False
