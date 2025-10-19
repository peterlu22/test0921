import pygame
import random
import os
from tetrominoes import TETROMINOES

# 遊戲視窗設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "俄羅斯方塊"

# 遊戲板設定
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# 計算遊戲板在視窗中的位置
GAME_BOARD_X = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GAME_BOARD_Y = (SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 音樂、音效和字型檔案路徑
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
BACKGROUND_MUSIC_PATH = os.path.join(ASSETS_DIR, 'background_music.mp3')
LAND_SOUND_PATH = os.path.join(ASSETS_DIR, 'land_sound.wav')
CLEAR_SOUND_PATH = os.path.join(ASSETS_DIR, 'clear_sound.wav')
FONT_PATH = os.path.join(ASSETS_DIR, 'wqy-zenhei.ttc') # 字型檔案路徑

# 最高分數檔案路徑
HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), 'highscore.txt')

def draw_block(screen, color, x, y):
    pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(screen, WHITE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1) # 邊框

def check_collision(tetromino_shape, x, y, game_board):
    """檢查方塊是否與遊戲板邊界或已固定的方塊發生碰撞"""
    for row_idx, row in enumerate(tetromino_shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board_x = x + col_idx
                board_y = y + row_idx

                # 檢查是否超出左右邊界或底部
                if not (0 <= board_x < GRID_WIDTH and 0 <= board_y < GRID_HEIGHT):
                    return True
                # 檢查是否與已固定的方塊重疊 (只檢查在遊戲板內的方塊)
                if board_y >= 0 and game_board[board_y][board_x] != BLACK:
                    return True
    return False

def rotate_tetromino(tetromino_shape):
    """將方塊順時針旋轉 90 度"""
    # 轉置矩陣 (行變列)
    rotated_shape = [list(row) for row in zip(*tetromino_shape)]
    # 反轉每一行 (實現順時針旋轉)
    rotated_shape = [row[::-1] for row in rotated_shape]
    return rotated_shape

def clear_lines(game_board):
    """檢查並消除遊戲板上的滿行，並將上方的方塊下移"""
    lines_cleared = 0
    for row_idx in range(GRID_HEIGHT - 1, -1, -1): # 從底部往上檢查
        if all(cell != BLACK for cell in game_board[row_idx]): # 如果這一行所有格子都不是黑色 (滿行)
            lines_cleared += 1
            # 移除滿行
            del game_board[row_idx]
            # 在頂部插入一個新的空行
            game_board.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    return lines_cleared

def load_highscore():
    """從檔案載入最高分數"""
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            try:
                return int(f.read())
            except ValueError:
                return 0 # 檔案內容無效則返回 0
    return 0

def save_highscore(score):
    """將最高分數儲存到檔案"""
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))

def main():
    pygame.init() # 初始化 Pygame
    pygame.mixer.init() # 初始化混音器

    # 建立遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)

    # 載入並播放背景音樂
    try:
        pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.play(-1) # -1 表示無限循環播放
    except pygame.error as e:
        print(f"無法載入背景音樂: {e}")
        print(f"請確認檔案是否存在: {BACKGROUND_MUSIC_PATH}")

    # 載入音效
    land_sound = None
    clear_sound = None
    try:
        land_sound = pygame.mixer.Sound(LAND_SOUND_PATH)
    except pygame.error as e:
        print(f"無法載入落地音效: {e}")
        print(f"請確認檔案是否存在: {LAND_SOUND_PATH}")
    try:
        clear_sound = pygame.mixer.Sound(CLEAR_SOUND_PATH)
    except pygame.error as e:
        print(f"無法載入消除音效: {e}")
        print(f"請確認檔案是否存在: {CLEAR_SOUND_PATH}")

    # 遊戲時鐘，用於控制遊戲速度
    clock = pygame.time.Clock()
    FPS = 60

    # 遊戲板 (儲存已固定的方塊)
    game_board = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    current_tetromino = None
    current_tetromino_x = 0
    current_tetromino_y = 0
    current_tetromino_color = BLACK # 初始化顏色

    next_tetromino = None # 新增下一個方塊變數
    next_tetromino_color = BLACK # 新增下一個方塊顏色

    # 方塊自動下落相關變數
    fall_time = 0
    base_fall_speed = 0.5 # 基礎下落速度
    fall_speed = base_fall_speed # 當前下落速度

    # 計分變數
    score = 0
    try:
        font = pygame.font.Font(FONT_PATH, 36) # 使用 wqy-zenhei.ttc 字型
    except pygame.error as e:
        print(f"無法載入字型: {e}")
        print(f"請確認檔案是否存在: {FONT_PATH}")
        font = pygame.font.Font(None, 36) # 如果載入失敗，則使用預設字型

    # 等級變數
    level = 1
    lines_to_next_level = 10 # 每消除 10 行升一級
    total_lines_cleared = 0

    # 最高分數
    highscore = load_highscore()

    # 遊戲狀態
    game_over = False
    paused = False # 新增暫停狀態

    # 遊戲迴圈
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # 按下 P 鍵切換暫停狀態
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause() # 暫停背景音樂
                    else:
                        pygame.mixer.music.unpause() # 恢復背景音樂
                
                if not game_over and not paused: # 只有在遊戲進行中且未暫停時才處理方塊移動
                    if event.key == pygame.K_LEFT:
                        new_x = current_tetromino_x - 1
                        if not check_collision(current_tetromino, new_x, current_tetromino_y, game_board):
                            current_tetromino_x = new_x
                    elif event.key == pygame.K_RIGHT:
                        new_x = current_tetromino_x + 1
                        if not check_collision(current_tetromino, new_x, current_tetromino_y, game_board):
                            current_tetromino_x = new_x
                    elif event.key == pygame.K_DOWN:
                        new_y = current_tetromino_y + 1
                        if not check_collision(current_tetromino, current_tetromino_x, new_y, game_board):
                            current_tetromino_y = new_y
                    elif event.key == pygame.K_UP: # 按下上箭頭鍵旋轉方塊
                        rotated_tetromino = rotate_tetromino(current_tetromino)
                        if not check_collision(rotated_tetromino, current_tetromino_x, current_tetromino_y, game_board):
                            current_tetromino = rotated_tetromino

        if not game_over and not paused:
            fall_time += clock.get_rawtime() # 累計時間
            clock.tick(FPS)

            # 方塊自動下落
            if fall_time / 1000 >= fall_speed: # 將毫秒轉換為秒
                new_y = current_tetromino_y + 1
                if not check_collision(current_tetromino, current_tetromino_x, new_y, game_board):
                    current_tetromino_y = new_y
                else:
                    # 方塊落地，固定方塊到遊戲板
                    for row_idx, row in enumerate(current_tetromino):
                        for col_idx, cell in enumerate(row):
                            if cell:
                                # 確保不會寫入到遊戲板的負索引 (方塊生成在頂部時可能超出)
                                if current_tetromino_y + row_idx >= 0:
                                    game_board[current_tetromino_y + row_idx][current_tetromino_x + col_idx] = current_tetromino_color
                    current_tetromino = None # 生成新方塊

                    if land_sound: # 播放落地音效
                        land_sound.play()

                    lines_cleared = clear_lines(game_board) # 檢查並消除滿行
                    if lines_cleared > 0:
                        if clear_sound: # 如果有消除行，且消除音效存在，則播放
                            clear_sound.play()
                        score += lines_cleared * 100 # 每消除一行加 100 分
                        total_lines_cleared += lines_cleared # 更新總消除行數

                        # 檢查是否升級
                        if total_lines_cleared >= level * lines_to_next_level:
                            level += 1
                            fall_speed = max(0.1, base_fall_speed - (level - 1) * 0.05) # 提升速度，最快 0.1 秒一格

                fall_time = 0 # 重置下落時間

            # 如果沒有當前方塊，則生成一個新的
            if current_tetromino is None:
                # 將下一個方塊變成當前方塊
                if next_tetromino is None:
                    # 第一次生成方塊時，同時生成當前方塊和下一個方塊
                    current_tetromino_name = random.choice(list(TETROMINOES.keys()))
                    current_tetromino = TETROMINOES[current_tetromino_name]['shape']
                    current_tetromino_color = TETROMINOES[current_tetromino_name]['color']
                else:
                    current_tetromino = next_tetromino
                    current_tetromino_color = next_tetromino_color

                current_tetromino_x = GRID_WIDTH // 2 - len(current_tetromino[0]) // 2
                current_tetromino_y = 0

                # 生成新的下一個方塊
                next_tetromino_name = random.choice(list(TETROMINOES.keys()))
                next_tetromino = TETROMINOES[next_tetromino_name]['shape']
                next_tetromino_color = TETROMINOES[next_tetromino_name]['color']

                # 檢查新生成的方塊是否立即碰撞 (遊戲結束條件)
                if check_collision(current_tetromino, current_tetromino_x, current_tetromino_y, game_board):
                    game_over = True
                    pygame.mixer.music.stop() # 遊戲結束時停止背景音樂
                    if score > highscore: # 遊戲結束時更新最高分數
                        highscore = score
                        save_highscore(highscore)

        # 繪製背景
        screen.fill(BLACK)

        # 繪製遊戲板邊框
        pygame.draw.rect(screen, WHITE, (GAME_BOARD_X, GAME_BOARD_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 2)

        # 繪製已固定的方塊
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if game_board[row][col] != BLACK:
                    draw_block(screen, game_board[row][col], GAME_BOARD_X + col * BLOCK_SIZE, GAME_BOARD_Y + row * BLOCK_SIZE)

        # 繪製當前方塊
        if current_tetromino and not paused: # 暫停時不繪製移動中的方塊
            for row_idx, row in enumerate(current_tetromino):
                for col_idx, cell in enumerate(row):
                    if cell:
                        draw_block(screen, current_tetromino_color,
                                   GAME_BOARD_X + (current_tetromino_x + col_idx) * BLOCK_SIZE,
                                   GAME_BOARD_Y + (current_tetromino_y + row_idx) * BLOCK_SIZE)

        # 顯示分數
        score_text = font.render(f"分數: {score}", True, WHITE)
        screen.blit(score_text, (GAME_BOARD_X + GRID_WIDTH * BLOCK_SIZE + 50, GAME_BOARD_Y))

        # 顯示等級
        level_text = font.render(f"等級: {level}", True, WHITE)
        screen.blit(level_text, (GAME_BOARD_X + GRID_WIDTH * BLOCK_SIZE + 50, GAME_BOARD_Y + 50))

        # 顯示下一個方塊
        next_tetromino_label = font.render("下一個:", True, WHITE)
        screen.blit(next_tetromino_label, (GAME_BOARD_X + GRID_WIDTH * BLOCK_SIZE + 50, GAME_BOARD_Y + 120))
        if next_tetromino:
            for row_idx, row in enumerate(next_tetromino):
                for col_idx, cell in enumerate(row):
                    if cell:
                        draw_block(screen, next_tetromino_color,
                                   GAME_BOARD_X + GRID_WIDTH * BLOCK_SIZE + 50 + col_idx * BLOCK_SIZE,
                                   GAME_BOARD_Y + 150 + row_idx * BLOCK_SIZE)

        # 顯示最高分數
        highscore_text = font.render(f"最高分數: {highscore}", True, WHITE)
        screen.blit(highscore_text, (GAME_BOARD_X + GRID_WIDTH * BLOCK_SIZE + 50, GAME_BOARD_Y + 250))

        # 顯示遊戲結束訊息
        if game_over:
            game_over_text = font.render("遊戲結束!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        elif paused: # 顯示暫停訊息
            paused_text = font.render("暫停", True, WHITE)
            text_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(paused_text, text_rect)

        # 更新顯示
        pygame.display.flip()

    pygame.quit() # 結束 Pygame

if __name__ == "__main__":
    main()
