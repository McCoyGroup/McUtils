from abc import ABCMeta, abstractmethod
__all__ = ['TransformationFunction']

class TransformationFunction(metaclass=ABCMeta):
    """
    The TransformationFunction class is an abstract class
    It provides the scaffolding for representing a single transformation operation
    """

    def __init__(self):
        """Initializes a transformation function based on the transfdata

        :param transfdata:
        :type transfdata:
        """
        ...

    @property
    def inverse(self):
        """
        Returns the inverse of the transformation
        :return:
        :rtype:
        """
        ...

    @abstractmethod
    def merge(self, other):
        """Tries to merge with another TransformationFunction

        :param other: a TransformationFunction to try to merge with
        :type other: TransformationFunction
        :return: tfunc
        :rtype: TransformationFunction
        """
        ...

    @abstractmethod
    def operate(self, coords, shift=True):
        """Operates on the coords. *Must* be able to deal with a list of coordinates, optimally in an efficient manner

        :param coords: the list of coordinates to apply the transformation to
        :type coords: np.ndarry
        """
        ...