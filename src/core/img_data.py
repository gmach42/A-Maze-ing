class ImgData:
    """Structure for image data"""

    def __init__(self):
        self.img: int | None = None  # mlx_new_image
        self.width: int = 0
        self.height: int = 0
        self.data: object = None  # memoryview(int)

    def clear_buffer(self):
        for i in range(len(self.data)):
            self.data[i] = 0
