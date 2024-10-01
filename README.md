# Creating-a-3D-Textured-Cube-with-PyQt5-and-OpenGL
This Python script creates a PyQt5 application with OpenGL rendering to display a rotating textured cube. It defines an OpenGLWindow class, inheriting from QOpenGLWidget, to handle the OpenGL context. The cube's faces are textured using images loaded via the PIL library. The script initializes OpenGL settings like enabling textures and loading images as textures. A QTimer is used to rotate the cube continuously by updating the angle every 16ms (approx. 60 FPS). The paintGL() method handles rendering each frame, while the cube's rotation creates an animated 3D effect.

# Required Libraries:
pip install PyQt5 Pillow
pip install numpy==1.21.0 PyOpenGL==3.1.5 PyOpenGL_accelerate==3.1.5

# Image
![image](https://github.com/user-attachments/assets/4dc1037a-6cd1-4ff2-8884-f32fe08a45f0)

