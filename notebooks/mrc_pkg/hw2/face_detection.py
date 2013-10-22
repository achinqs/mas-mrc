def eigenfaces(image_filenames):
    """ The eigenfaces function creates a set of eigenfaces from a list of grayscale images. """\
    """ The eigenfaces are returned in a MxN matrix, where M = W*H of each single image, and N is the number of images. """
    raise NotImplementedError()
    
def recognize_face(face, eigenfaces):
    """ Given a query face as numpy.ndarray and a matrix of eigenfaces, returns the index of """\
    """ the eigenface closest to the query face """
    assert numpy.product(face.shape) == eigenfaces.shape[0]
    raise NotImplementedError()