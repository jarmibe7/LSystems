"""
Math and OpenGL rendering for 3D LSystems
"""
import numpy as np
import moderngl
import glfw

# 3D turtle + camera math

def rot_x(theta):
    t = np.deg2rad(theta)
    return np.array([
        [1, 0, 0],
        [0, np.cos(t), -np.sin(t)],
        [0, np.sin(t), np.cos(t)]
    ])

def rot_y(theta):
    t = np.deg2rad(theta)
    return np.array([
        [np.cos(t), 0, np.sin(t)],
        [0, 1, 0],
        [-np.sin(t), 0, np.cos(t)]
    ])

def rot_z(theta):
    t = np.deg2rad(theta)
    return np.array([
        [np.cos(t), -np.sin(t), 0],
        [np.sin(t), np.cos(t), 0],
        [0, 0, 1]
    ])

def perspective(fov, aspect, near, far):
    f = 1.0 / np.tan(np.deg2rad(fov)/2)
    M = np.zeros((4,4), dtype=np.float32)
    M[0,0] = f / aspect
    M[1,1] = f
    M[2,2] = (far + near)/(near - far)
    M[2,3] = (2 * far * near)/(near - far)
    M[3,2] = -1
    return M

def look_at(eye, target, up):
    f = (target - eye)
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)

    mat = np.eye(4, dtype=np.float32)
    mat[0, :3] = s
    mat[1, :3] = u
    mat[2, :3] = -f
    mat[:3, 3] = -mat[:3,:3] @ eye  # correct translation
    return mat


# Renderer and shader

VERT_SHADER = """
#version 330
in vec3 in_pos;
uniform mat4 MVP;
void main() {
    gl_Position = MVP * vec4(in_pos, 1.0);
}
"""

FRAG_SHADER = """
#version 330
out vec4 fragColor;
void main() {
    fragColor = vec4(0.9, 0.9, 0.9, 1.0);
}
"""


class RenderLSystem3D:
    def __init__(self, distance, theta, width=900, height=900):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")

        self.window = glfw.create_window(width, height, "3D L-System", None, None)
        glfw.make_context_current(self.window)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.prog = self.ctx.program(
            vertex_shader=VERT_SHADER,
            fragment_shader=FRAG_SHADER
        )

        self.distance = distance
        self.theta = theta

    def _generate_segments(self, code):
        pos = np.zeros(3)
        R = np.eye(3)

        forward = np.array([0, 1, 0])
        stack = []
        segments = []

        for c in code:
            if c == 'F':
                new_pos = pos + R @ forward * self.distance
                segments.append((pos.copy(), new_pos.copy()))
                pos = new_pos

            elif c == 'f':
                pos = pos + R @ forward * self.distance

            elif c == '[':
                stack.append((pos.copy(), R.copy()))

            elif c == ']':
                pos, R = stack.pop()

            elif c == '+': R = R @ rot_z(self.theta)
            elif c == '-': R = R @ rot_z(-self.theta)
            elif c == '&': R = R @ rot_x(self.theta)
            elif c == '^': R = R @ rot_x(-self.theta)
            elif c == '/': R = R @ rot_y(self.theta)
            elif c == '\\': R = R @ rot_y(-self.theta)

        return np.array(segments, dtype=np.float32)

    def draw(self, code):
        segments = self._generate_segments(code)
        vertices = segments.reshape(-1, 3)
        vbo = self.ctx.buffer(vertices.tobytes())
        vao = self.ctx.simple_vertex_array(self.prog, vbo, "in_pos")

        MVP = np.eye(4, dtype=np.float32)
        MVP[2, 3] = -5.0   # pull camera back

        self.prog["MVP"].write(MVP.tobytes())

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.ctx.clear(0.05, 0.05, 0.05)
            vao.render(moderngl.LINES)
            glfw.swap_buffers(self.window)

# Flying in 3D renderer

class RenderLSystem3DFly:
    def __init__(self, distance, theta, width=900, height=900, fov=60.0):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")

        self.window = glfw.create_window(width, height, "3D L-System Fly Camera", None, None)
        glfw.make_context_current(self.window)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.prog = self.ctx.program(vertex_shader=VERT_SHADER, fragment_shader=FRAG_SHADER)

        self.width = width
        self.height = height
        self.distance = distance
        self.theta = theta
        self.fov = fov

        # Camera parameters
        self.cam_pos = np.array([0.0, -5.0, 5.0], dtype=np.float32)
        self.cam_front = np.array([0.0, 1.0, -1.0], dtype=np.float32)
        self.cam_front /= np.linalg.norm(self.cam_front)
        self.cam_up = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        self.yaw, self.pitch = 90.0, -45.0
        self.lastX, self.lastY = width/2, height/2
        self.first_mouse = True
        self.speed = 0.2
        self.sensitivity = 0.2

        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Fly with mouse
    def mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.lastX = xpos
            self.lastY = ypos
            self.first_mouse = False

        xoffset = (xpos - self.lastX) * self.sensitivity
        yoffset = (self.lastY - ypos) * self.sensitivity
        self.lastX = xpos
        self.lastY = ypos

        self.yaw += xoffset
        self.pitch += yoffset
        self.pitch = max(-89.0, min(89.0, self.pitch))

        front = np.array([
            np.cos(np.deg2rad(self.yaw)) * np.cos(np.deg2rad(self.pitch)),
            np.sin(np.deg2rad(self.pitch)),
            np.sin(np.deg2rad(self.yaw)) * np.cos(np.deg2rad(self.pitch))
        ], dtype=np.float32)
        self.cam_front[:] = front / np.linalg.norm(front)

    # Move with keyboard
    def process_input(self):
        window = self.window
        right = np.cross(self.cam_front, self.cam_up)
        right /= np.linalg.norm(right)

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.cam_pos += self.speed * self.cam_front
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.cam_pos -= self.speed * self.cam_front
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.cam_pos -= self.speed * right
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.cam_pos += self.speed * right
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.cam_pos += self.speed * self.cam_up
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.cam_pos -= self.speed * self.cam_up

    def _generate_segments(self, code):
        pos = np.zeros(3)
        R = np.eye(3)
        forward = np.array([0, 1, 0])
        stack = []
        segments = []

        for c in code:
            if c == 'F':
                new_pos = pos + R @ forward * self.distance
                segments.append((pos.copy(), new_pos.copy()))
                pos = new_pos
            elif c == 'f':
                pos = pos + R @ forward * self.distance
            elif c == '[':
                stack.append((pos.copy(), R.copy()))
            elif c == ']':
                pos, R = stack.pop()
            elif c == '+': R = R @ rot_z(self.theta)
            elif c == '-': R = R @ rot_z(-self.theta)
            elif c == '&': R = R @ rot_x(self.theta)
            elif c == '^': R = R @ rot_x(-self.theta)
            elif c == '/': R = R @ rot_y(self.theta)
            elif c == '\\': R = R @ rot_y(-self.theta)

        return np.array(segments, dtype=np.float32)

    def draw(self, code):
        segments = self._generate_segments(code)
        vertices = segments.reshape(-1, 3)
        vbo = self.ctx.buffer(vertices.tobytes())
        vao = self.ctx.simple_vertex_array(self.prog, vbo, "in_pos")

        projection = perspective(self.fov, self.width/self.height, 0.1, 100.0)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.process_input()

            view = look_at(self.cam_pos, self.cam_pos + self.cam_front, self.cam_up)
            MVP = projection @ view
            self.prog["MVP"].write(MVP.tobytes())

            self.ctx.clear(0.05, 0.05, 0.05)
            vao.render(moderngl.LINES)
            glfw.swap_buffers(self.window)

        glfw.terminate()