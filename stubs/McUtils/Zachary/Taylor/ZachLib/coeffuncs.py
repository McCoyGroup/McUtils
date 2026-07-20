"""
coeffuncs defines the functions we use when computing coefficients for FD
"""
import numpy as np, math

def StirlingS1(n):
    """Computes the Stirling numbers

    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def Binomial(n):
    """

    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def GammaBinomial(s, n):
    """Generalized binomial gamma function

    :param s:
    :type s:
    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def Factorial(n):
    """I was hoping to do this in some built in way with numpy...but I guess it's not possible?
    looks like by default things don't vectorize and just call math.factorial

    :param n:
    :type n:
    :return:
    :rtype:
    """
    ...

def EvenFiniteDifferenceWeights(m, s, n):
    """Finds the series coefficients for x^s*ln(x)^m centered at x=1. Uses the method:

             Table[
               Sum[
                ((-1)^(r - k))*Binomial[r, k]*
                    Binomial[s, r - j] StirlingS1[j, m] (m!/j!),
                {r, k, n},
                {j, 0, r}
                ],
               {k, 0, n}
               ]
             ]

        which is shown by J.M. here: https://chat.stackexchange.com/transcript/message/49528234#49528234

    :param m: the order of the derivative requested
    :type m:
    :param s: the offset of the point at which the derivative is requested from the left edge of the stencil
    :type s:
    :param n: the number of points used in the stencil
    :type n:
    :return:
    :rtype:
    """
    ...

def UnevenFiniteDifferenceWeights(m, z, x):
    ...