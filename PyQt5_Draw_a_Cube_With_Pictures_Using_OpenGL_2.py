import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


class OpenGLWindow(QOpenGLWidget):
    """
    A custom QOpenGLWidget class for rendering a rotating textured cube using OpenGL.
    """

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Initialize the OpenGLWindow with the parent widget.

        :param parent: The parent widget, typically a QMainWindow.
        """
        super(OpenGLWindow, self).__init__(parent)
        self.angle = 0.0  # Angle for cube rotation
        self.textures = []

        # Timer to update the frame every 16ms (~60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)

    def initializeGL(self) -> None:
        """
        Set up the OpenGL environment. Called once before rendering starts.
        Initializes the background color and enables depth testing.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering
        glEnable(GL_TEXTURE_2D)  # Enable texture mapping
        self.load_textures()

    def resizeGL(self, w: int, h: int) -> None:
        """
        Handle resizing of the OpenGL viewport.

        :param w: The new width of the widget.
        :param h: The new height of the widget.
        """
        glViewport(0, 0, w, h)  # Set the viewport to cover the whole widget
        glMatrixMode(GL_PROJECTION)  # Set up the projection matrix
        glLoadIdentity()
        gluPerspective(45.0, w / h if h != 0 else 1.0, 0.1, 100.0)  # Set perspective projection
        glMatrixMode(GL_MODELVIEW)  # Switch back to the model view matrix

    def paintGL(self) -> None:
        """
        Render the scene. Called every time the widget needs to be repainted.
        Clears the screen and draws a rotating textured cube.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer

        # Reset transformations
        glLoadIdentity()

        # Move camera back to see the cube
        # If you want to see the cube closer, then change camera position.
        # This line controls the camera's position.
        glTranslatef(0.0, 0.0, -4.5)

        # Rotate the cube
        glRotatef(self.angle, 1.0, 1.0, 0.0)

        # Draw the cube with textures
        self.draw_textured_cube()

    def update_frame(self) -> None:
        """
        Update the rotation angle and repaint the widget.
        This is called periodically by the QTimer to animate the cube.
        """
        self.angle += 1.0  # Increment rotation angle
        self.update()  # Request an update (repaint)

    def load_textures(self) -> None:
        """
        Load textures for each face of the cube using the Pillow library.
        """
        images = [
            "space_image_1.png",  # Replace with actual file paths to the images
            "space_image_2.png",
            "space_image_3.jpg",
            "space_image_4.jpg",
            "space_image_5.png",
            "space_image_6.png"
        ]

        self.textures = glGenTextures(6)  # Generate 6 texture IDs

        for i, image_file in enumerate(images):
            glBindTexture(GL_TEXTURE_2D, self.textures[i])
            image = Image.open(image_file)
            # Flip the image vertically for OpenGL
            image = image.transpose(Image.FLIP_TOP_BOTTOM)  
            img_data = image.convert("RGBA").tobytes()
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, 
                         image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

            # Set texture parameters
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def draw_textured_cube(self) -> None:
        """
        Draw a 3D cube with different textures applied to each face.
        """
        # Front face
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
        glEnd()

        # Back face
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, -1.0)
        glEnd()

        # Top face
        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, 1.0, -1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
        glEnd()

        # Bottom face
        glBindTexture(GL_TEXTURE_2D, self.textures[3])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, -1.0, 1.0)
        glEnd()

        # Right face
        glBindTexture(GL_TEXTURE_2D, self.textures[4])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0, -1.0)
        glEnd()

        # Left face
        glBindTexture(GL_TEXTURE_2D, self.textures[5])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, -1.0)
        glEnd()


class MainWindow(QMainWindow):
    """
    Main application window that contains the OpenGL widget.
    """

    def __init__(self) -> None:
        """
        Initialize the main window and set up the OpenGL widget.
        """
        super().__init__()
        self.setWindowTitle('OpenGL with PyQt5: Textured Cube')
        self.setGeometry(100, 100, 800, 600)

        # Add the OpenGL widget to the window
        self.opengl_widget = OpenGLWindow(self)
        self.setCentralWidget(self.opengl_widget)


def main() -> None:
    """
    The main function to initialize and run the PyQt5 application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
