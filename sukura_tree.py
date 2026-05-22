import pygame
import random
import sys
import os
import win32gui   # noqa: provided by pywin32
import win32con   # noqa: provided by pywin32
import win32api   # noqa: provided by pywin32


def resource_path(relative_path):
    """兼容开发环境与 PyInstaller 打包后的资源路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

# 初始化 Pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.RESIZABLE)
pygame.display.set_caption("3D Sakura Effect")

# Windows 置顶与透明设置
# noinspection DuplicatedCode
hwnd = pygame.display.get_wm_info()['window']
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
MAGIC_COLOR = (58, 37, 23)
# noinspection PyUnresolvedReferences
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*MAGIC_COLOR), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# --- 加载资源 ---
try:
    petal_image = pygame.image.load(resource_path('resources/petal.png')).convert_alpha()
    trunk_image = pygame.image.load(resource_path('resources/trunk.png')).convert_alpha()
    # 新增：加载三部分树冠
    crown1 = pygame.image.load(resource_path('resources/crown1.png')).convert_alpha()
    crown2 = pygame.image.load(resource_path('resources/crown2.png')).convert_alpha()
    crown3 = pygame.image.load(resource_path('resources/crown3.png')).convert_alpha()
except Exception as e:
    print(f"图片加载失败，请检查文件名: {e}")
    sys.exit()


class Petal:
    def __init__(self):
        self.angle = None
        self.drift = None
        self.size = None
        self.speed = None
        self.x = None
        self.reset()
        self.y = random.randint(0, HEIGHT)  # 初始随机分布

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-150, -30)
        self.speed = random.uniform(0.8, 2.5)
        self.size = random.randint(15, 30)
        self.drift = random.uniform(-0.5, 0.5)
        self.angle = random.uniform(0, 360)

    def update(self):
        self.y += self.speed
        self.x += self.drift
        self.angle += 1
        if self.y > HEIGHT: self.reset()

    def draw(self, surface):
        img = pygame.transform.rotozoom(petal_image, self.angle, self.size / petal_image.get_width())
        surface.blit(img, img.get_rect(center=(self.x, self.y)))


# 初始化
petals = [Petal() for _ in range(40)]
clock = pygame.time.Clock()

# UI 设置
CW_W, CW_H = 200, 80
font = pygame.font.SysFont('SimHei', 18)
running = True

while running:
    # 动态获取当前宽高（适配缩放）
    CUR_W, CUR_H = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 按钮位置检测（右下角）
            btn_rect = pygame.Rect(CUR_W - 150, CUR_H - 50, 100, 30)
            if btn_rect.collidepoint(event.pos): running = False

    screen.fill(MAGIC_COLOR)

    # --- 1. 绘制底层 (树干 + 1、3号树冠) ---
    # 它们会被花瓣遮挡
    t_img = pygame.transform.scale(trunk_image, (CUR_W, CUR_H))
    c1_img = pygame.transform.scale(crown1, (CUR_W, CUR_H))
    c3_img = pygame.transform.scale(crown3, (CUR_W, CUR_H))

    screen.blit(t_img, (0, 0))
    screen.blit(c1_img, (0, -1))
    screen.blit(c3_img, (0, -1))

    # --- 2. 绘制中间层 (花瓣) ---
    for p in petals:
        p.update()
        p.draw(screen)

    # --- 3. 绘制顶层 (2号树冠) ---
    # 花瓣会从 2 号树冠“后面”穿过，营造穿梭感
    c2_img = pygame.transform.scale(crown2, (CUR_W, CUR_H))
    screen.blit(c2_img, (0, 0))

    # --- 4. 绘制控制窗体 (始终最前) ---
    cw_x, cw_y = CUR_W - CW_W - 15, CUR_H - CW_H - 15
    # 窗体背景
    pygame.draw.rect(screen, (30, 30, 30), (cw_x, cw_y, CW_W, CW_H), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (cw_x, cw_y, CW_W, CW_H), 2, border_radius=10)
    # 文字
    txt = font.render("点击这里关闭", True, (255, 255, 255))
    screen.blit(txt, (cw_x + (CW_W - txt.get_width()) // 2, cw_y + 10))
    # 按钮
    btn_r = pygame.Rect(CUR_W - 150, CUR_H - 50, 80, 25)
    pygame.draw.rect(screen, (180, 50, 50), btn_r, border_radius=5)
    btn_txt = font.render("关闭", True, (255, 255, 255))
    screen.blit(btn_txt, (btn_r.centerx - btn_txt.get_width() // 2, btn_r.centery - btn_txt.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()