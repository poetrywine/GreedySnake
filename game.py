from game_items import *


class Game:
    def __init__(self):
        self.main_window = pygame.display.set_mode((640, 480))  # 游戏主窗口
        pygame.display.set_caption('贪吃蛇')  # 主窗口标题
        self.score_label = Label()  # 得分的文本标签对象
        self.tip_label = Label(24, False)  # 暂停\游戏结束的文本标签对象
        self.is_game_over = False  # 游戏是否结束的标记，True为结束
        self.is_pause = False  # 游戏是否暂停的标记，True为暂停
        self.food = Food()  # 食物对象
        self.snake = Snake()  # 贪吃蛇对象

    def start(self):
        """启动并控制游戏"""
        clock = pygame.time.Clock()  # 游戏时钟
        while True:
            # 1.事件监听
            for event in pygame.event.get():  # 遍历同一时刻发生的事件列表
                # 与死亡和暂停无关的事件
                if event.type == pygame.QUIT:  # 鼠标按下了窗口的叉叉
                    return
                elif event.type == pygame.KEYDOWN:  # 按下的是键盘
                    if event.key == pygame.K_ESCAPE:  # 按了键盘的ESC键
                        return
                    elif event.key == pygame.K_SPACE:  # 按下了空格键
                        if self.is_game_over:  # 游戏失败，重置游戏参数
                            self.reset_game()
                        else:  # 暂停游戏
                            self.is_pause = not self.is_pause

                # 没死亡，没暂停才执行的事件
                if not self.is_pause and not self.is_game_over:
                    if event.type == FOOD_UPDATE_EVENT:
                        self.food.random_rect()  # 更新食物位置
                    elif event.type == SNAKE_UPDATE_EVENT:
                        self.is_game_over = not self.snake.update()  # 移动蛇的位置
                    elif event.type == pygame.KEYDOWN:  # 有按键按下
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                            self.snake.change_dir(event.key)

            self.main_window.fill(BACKGROUND_GROUND)  # 设置窗口背景颜色

            # 2.绘制得分
            self.score_label.draw(self.main_window, '得分：%d' % self.snake.score)

            # 3.绘制暂停\游戏结束标签
            if self.is_game_over:
                self.tip_label.draw(self.main_window, '游戏结束，按空格键开启新游戏...')
            elif self.is_pause:
                self.tip_label.draw(self.main_window, '游戏暂停，按空格键继续...')
            else:
                if self.snake.has_eat(self.food):
                    self.food.random_rect()

            # 4.绘制食物
            self.food.draw(self.main_window)

            # 5.绘制贪吃蛇
            self.snake.draw(self.main_window)

            # 6.刷新窗口内容
            pygame.display.update()

            # 7.设置刷新率
            clock.tick(60)

    def reset_game(self,):
        """重置游戏参数"""
        self.snake.score = 0
        self.is_game_over = False
        self.is_pause = False
        # 重置蛇的数据
        self.snake.reset_snake()
        # 重置食物位置
        self.food.random_rect()


if __name__ == '__main__':
    pygame.init()  # 游戏开始要初始化pygame模块
    Game().start()  # 游戏逻辑
    pygame.quit()  # 游戏结束要释放pygame占用的资源
