# 이것은 각 상태들을 객체로 구현한 것임.
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0 # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT
import game_world
import game_framework

class Run:

    @staticmethod
    def enter(bird, e):
        pass
    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if bird.action == 2 and bird.frame >= FRAMES_PER_ACTION - 1:
            bird.action, bird.frame = 1, 0
        elif bird.action == 1 and bird.frame >= FRAMES_PER_ACTION - 1:
            bird.action, bird.frame = 0, 0
        elif bird.action == 0 and bird.frame >= FRAMES_PER_ACTION - 2:
            bird.action, bird.frame = 2, 0

        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        bird.x = clamp(25, bird.x, 1500-25)
        if bird.x >= 1500-25:
            bird.facedir = -1
            bird.dir = -1
        elif bird.x <= 100+25:
            bird.facedir = 1
            bird.dir = 1


    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, bird.x, bird.y)
        elif bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, 0, 'h', bird.x, bird.y, 183, 168)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
        self.transitions = {}

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def draw(self):
        self.cur_state.draw(self.bird)

class Bird:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.action = 2
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.font = load_font("ENCR10B.TTF", 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = 'Ball'

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-60, self.y+50, f'{get_time()}', (255, 255, 0))