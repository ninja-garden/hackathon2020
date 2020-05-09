# TODO implement detector.

from PIL import Image

class Detector:
    def __init__(self: Detector, model_path: str):
        # Init model somehow.
        self.model = None
        pass

    # Don't change signature of methods pls.
    # I don't want to change logic in main program.
    # If you need to use OpenСV or something else,
    # convert image to opencv.image inside of the method.
    def detect(self, image: Image):
        ''' Takes: PIL.Image.
            Returns: List<Tuple<float, float, float, float, float,>>.

            Converts some image to list of tuples of five floats, which
            represent some building on image.
            Floats #1-4 contain x1,y1,x2,y2 in this particular order,
            where x1,y1 - coordinate of left bottom vertice of rectangle,
            x2,y2 - coordinate of right upper vertice of rectangle.
            All coordinates are given in pixel space.
            Point (0,0) is upper left corner of image.
            Float #5 is the angle (in case the rectangle is rotated somehow).
        '''
        return [(0.,0.,float(image.size[0] / 2),float(image.size[1] / 2),0.)]
