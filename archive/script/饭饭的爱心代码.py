import pygame
import random
import math
import os

# 初始化pygame
pygame.init()

# 窗口设置
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))


# 改进的字体设置函数
def get_font(size):
    # 尝试加载系统中文字体
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # Windows 黑体
        "C:/Windows/Fonts/msyh.ttc",  # Windows 微软雅黑
        "C:/Windows/Fonts/simsun.ttc",  # Windows 宋体
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/System/Library/Fonts/Arial.ttf",  # macOS
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # Linux
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue

    # 如果找不到中文字体，使用默认字体
    try:
        return pygame.font.SysFont("Arial", size)
    except:
        return pygame.font.Font(None, size)


# 创建字体对象
font = get_font(20)  # 稍微减小字体大小
title_font = get_font(36)

# 从图片中提取的文字内容（清理后的版本）
love_texts = [
    "Mola le offi la tee",
    "mihai amestiah sind",
    "milvini un ne seibesc",
    "Le sakam",
    "Mlohuujam",
    "Te sakam",
    "chami dài e n ki n M",
    "Te dua",
    "Té okabescu",
    "Tá grá agam duit",
    "Kocham Ci",
    "Saya cintakan kamu",
    "我爱你",
    "Te ambesc",
    "Mahal kita",
    "Jeg elsker deg",
    "Mihaji té",
    "Meng sona",
    "Szerethékda",
    "Jag Tjukin",
    "Teja amerhi",
    "L kertesi skarji",
    "joga nem lesen",
    "nyolyomni",
    "I love you",  # 英语
    "Je t'aime",  # 法语
    "Ich liebe dich",  # 德语
    "Ti amo",  # 意大利语
    "Te amo",  # 西班牙语
    "あいしてる",  # 日语
    # "사랑해",  # 韩语
    "我爱你",  # 中文（方言：粤语）
    "我中意你",  # 中文（方言：粤语）
    "我爱侬",  # 中文（方言：吴语）
    "我欢喜你",  # 中文（方言：闽南语）
    "我爱你",  # 中文（繁体）
    "我愛你",  # 中文（繁体）
    "勾买蒙",  # 中文（壮话）
    "额爱你",  # 陕西话
    "恩欢喜你",
    "我爱列",
    "Ik hou van je",
    "Saya cintakan mu",
    "Ti amo",
    "Jeg elsker dig",
    "Aku cinta padamu",
    "Saya cinta kamu",
    "Ljubim te",
    "俺喜欢",
    "我稀罕你",
    "俺稀罕你"

]
# 爱心坐标生成
love_points = []
for t in range(1000):
    theta = t / 1000 * 2 * math.pi
    x = 15 * (pow(math.sin(theta), 3))
    y = 10 * math.cos(theta) - 5 * math.cos(2 * theta) - 2 * math.cos(3 * theta) - math.cos(4 * theta)
    # 缩放并偏移到窗口中心
    x = x * 18 + width // 2
    y = -y * 18 + height // 2
    love_points.append((int(x), int(y)))

# 文字对象列表
text_objects = []
colors = [
    (255, 182, 193),  # 浅粉红
    (255, 105, 180),  # 热粉红
    (255, 20, 147),  # 深粉红

]

# 测试字体渲染
print("测试字体渲染...")
for text in love_texts:
    try:
        test_surface = font.render(text, True, (255, 255, 255))
        print(f"成功渲染: {text}")
    except Exception as e:
        print(f"渲染失败: {text} - 错误: {e}")

for i, text in enumerate(love_texts):
    # 为每种文字分配颜色
    color = colors[i % len(colors)]

    # 渲染文字表面（添加错误处理）
    try:
        # 确保文本是字符串类型
        if not isinstance(text, str):
            text = str(text)
        text_surface = font.render(text, True, color)
    except Exception as e:
        print(f"渲染失败 '{text}': {e}")
        # 使用简单回退文本
        text_surface = font.render("Love", True, color)

    # 随机初始位置
    idx = random.randint(0, len(love_points) - 1)
    x, y = love_points[idx]

    # 随机速度
    speed_x = random.uniform(-0.15, 0.15)
    speed_y = random.uniform(-0.15, 0.15)

    text_objects.append({
        "surface": text_surface,
        "text": text,  # 保存原始文本用于调试
        "x": x,
        "y": y,
        "speed_x": speed_x,
        "speed_y": speed_y,
        "target_idx": idx,
        "color": color
    })

# 添加标题
try:
    title_text = title_font.render("", True, (255, 255, 255))
except:
    title_text = title_font.render("I Love You in Multiple Languages", True, (255, 255, 255))

# 添加说明文字
instruction_font = get_font(16)
instruction_text = instruction_font.render("按ESC键退出", True, (150, 150, 150))

# 主循环
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 黑色背景
    screen.fill((0, 0, 0))

    # 绘制标题
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 20))

    # 绘制说明文字
    screen.blit(instruction_text, (width - instruction_text.get_width() - 10, height - 30))

    # 绘制和移动文字
    for obj in text_objects:
        # 绘制文字
        text_rect = obj["surface"].get_rect(center=(obj["x"], obj["y"]))
        screen.blit(obj["surface"], text_rect)

        # 移动文字
        target_x, target_y = love_points[obj["target_idx"]]
        obj["x"] += (target_x - obj["x"]) * 0.02 + obj["speed_x"]
        obj["y"] += (target_y - obj["y"]) * 0.02 + obj["speed_y"]

        # 更新目标点
        obj["target_idx"] = (obj["target_idx"] + 1) % len(love_points)

        # 边界检查
        if obj["x"] < 0 or obj["x"] > width:
            obj["speed_x"] *= -1
        if obj["y"] < 50 or obj["y"] > height - 50:
            obj["speed_y"] *= -1

    # 显示帧率
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (100, 100, 100))
    screen.blit(fps_text, (10, height - 30))

    pygame.display.flip()
    clock.tick(60)