import pygame
import cv2
import math
import time
import win32gui
import win32con


class LockScreen:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        pygame.display.set_caption("GestureLock")

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont(
            "Arial",
            48,
            bold=True
        )

        self.status_font = pygame.font.SysFont(
            "Arial",
            26,
            bold=True
        )

        self.main_font = pygame.font.SysFont(
            "Arial",
            28
        )

        self.small_font = pygame.font.SysFont(
            "Arial",
            20
        )

        self.locked = True
        self.start_time = time.time()

        self.set_topmost()

    def set_topmost(self):

        hwnd = pygame.display.get_wm_info()["window"]

        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE |
            win32con.SWP_NOSIZE |
            win32con.SWP_SHOWWINDOW
        )

    def draw_background(self):

        self.screen.fill((7, 12, 25))

        pulse = (math.sin(time.time() * 2) + 1) / 2

        for i in range(8):

            alpha = int(8 + pulse * 8)

            surface = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            radius = 250 + i * 100

            pygame.draw.circle(
                surface,
                (40, 80, 150, alpha),
                (
                    self.width // 2,
                    self.height // 2
                ),
                radius
            )

            self.screen.blit(
                surface,
                (0, 0)
            )

    def draw_header(self):

        title = self.title_font.render(
            "GESTURELOCK",
            True,
            (240, 245, 255)
        )

        title_rect = title.get_rect(
            center=(self.width // 2, 55)
        )

        self.screen.blit(
            title,
            title_rect
        )

        status = self.status_font.render(
            "PC LOCKED",
            True,
            (220, 225, 235)
        )

        status_rect = status.get_rect(
            center=(self.width // 2, 105)
        )

        self.screen.blit(
            status,
            status_rect
        )

    def draw_camera(self, frame):

        camera_width = min(760, self.width - 300)
        camera_height = int(camera_width * 9 / 16)

        frame = cv2.resize(
            frame,
            (camera_width, camera_height)
        )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        camera_surface = pygame.surfarray.make_surface(
            frame.swapaxes(0, 1)
        )

        camera_x = self.width // 2 - camera_width // 2
        camera_y = 145

        shadow = pygame.Surface(
            (camera_width + 20, camera_height + 20),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            shadow,
            (0, 0, 0, 100),
            (
                10,
                10,
                camera_width,
                camera_height
            ),
            border_radius=18
        )

        self.screen.blit(
            shadow,
            (camera_x - 10, camera_y - 10)
        )

        self.screen.blit(
            camera_surface,
            (camera_x, camera_y)
        )

        pygame.draw.rect(
            self.screen,
            (100, 130, 180),
            (
                camera_x,
                camera_y,
                camera_width,
                camera_height
            ),
            2,
            border_radius=16
        )

    def draw_instruction(self):

        instruction = self.main_font.render(
            "Perform your gesture password",
            True,
            (210, 218, 235)
        )

        rect = instruction.get_rect(
            center=(self.width // 2, 555)
        )

        self.screen.blit(
            instruction,
            rect
        )

    def draw_progress(self, progress, sequence_length):

        spacing = 70

        total_width = spacing * (sequence_length - 1)

        start_x = self.width // 2 - total_width // 2

        y = 620

        for i in range(sequence_length):

            x = start_x + i * spacing

            if i < progress:

                pygame.draw.circle(
                    self.screen,
                    (235, 240, 250),
                    (x, y),
                    11
                )

            elif i == progress:

                pulse = (math.sin(time.time() * 5) + 1) / 2

                radius = int(11 + pulse * 4)

                pygame.draw.circle(
                    self.screen,
                    (120, 150, 200),
                    (x, y),
                    radius,
                    2
                )

            else:

                pygame.draw.circle(
                    self.screen,
                    (60, 70, 90),
                    (x, y),
                    11,
                    2
                )

    def draw_detected(self, current_gesture):

        if current_gesture:
            text = "Gesture detected"
        else:
            text = "Waiting for hand..."

        detected = self.small_font.render(
            text,
            True,
            (160, 170, 190)
        )

        rect = detected.get_rect(
            center=(self.width // 2, self.height - 35)
        )

        self.screen.blit(
            detected,
            rect
        )

    def draw(
        self,
        frame,
        progress,
        current_gesture,
        next_gesture
    ):

        self.draw_background()

        self.draw_header()

        self.draw_camera(frame)

        self.draw_instruction()

        self.draw_progress(
            progress,
            4
        )

        self.draw_detected(
            current_gesture
        )

        pygame.display.flip()

        self.clock.tick(60)

    def unlock(self):

        self.locked = False

    def is_locked(self):

        return self.locked

    def close(self):

        pygame.quit()