"""
Copyright (c) 2009 Ryan Kirkman

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import math


def pre_rating_rd(__rd, vol):
    """ Calculates and updates the player's rating deviation for the
    beginning of a rating period.

    preRatingRD() -> None

    """
    return math.sqrt(math.pow(__rd, 2) + math.pow(vol, 2))


def get_rating(__rating):
    return (__rating * 173.7178) + 1500


def set_rating(rating):
    return (rating - 1500) / 173.7178


def get_rd(__rd):
    return __rd * 173.7178


def set_rd(rd):
    return rd / 173.7178


def g(RD):
    """ The Glicko2 g(RD) function.

    g() -> float

    """
    return 1 / math.sqrt(1 + 3 * math.pow(RD, 2) / math.pow(math.pi, 2))


def E(__rating, p2rating, p2RD):
    """ The Glicko E function.

    E(int) -> float

    """
    return 1 / (1 + math.exp(-1 * g(p2RD) * \
                             (__rating - p2rating)))


def f(__rating, tau, x, delta, v, a):
    ex = math.exp(x)
    num1 = ex * (delta ** 2 - __rating ** 2 - v - ex)
    denom1 = 2 * ((__rating ** 2 + v + ex) ** 2)
    return (num1 / denom1) - ((x - a) / (tau ** 2))


def v(__rating, rating_list, RD_list):
    """ The v function of the Glicko2 system.

    v(list[int], list[int]) -> float

    """
    tempSum = 0
    for i in range(len(rating_list)):
        tempE = E(__rating, rating_list[i], RD_list[i])
        tempSum += math.pow(g(RD_list[i]), 2) * tempE * (1 - tempE)
    return 1 / tempSum



def delta(__rating, rating_list, RD_list, outcome_list, v):
    """ The delta function of the Glicko2 system.

    delta(list, list, list) -> float

    """
    tempSum = 0
    for i in range(len(rating_list)):
        tempSum += g(RD_list[i]) * (outcome_list[i] - E(__rating, rating_list[i], RD_list[i]))
    return v * tempSum


def new_vol(__rating, __rd, rating_list, RD_list, outcome_list, v, vol, tau):
    """ Calculating the new volatility as per the Glicko2 system.

    Updated for Feb 22, 2012 revision. -Leo

    new_vol(list, list, list, float) -> float

    """
    # step 1
    a = math.log(vol ** 2)
    eps = 0.000001
    A = a

    # step 2
    B = None
    _delta = delta(__rating, rating_list, RD_list, outcome_list, v)
    tau = tau
    if (_delta ** 2) > ((__rd ** 2) + v):
        B = math.log(_delta ** 2 - __rd ** 2 - v)
    else:
        k = 1
        while f(__rating, tau, a - k * math.sqrt(tau ** 2), _delta, v, a) < 0:
            k = k + 1
        B = a - k * math.sqrt(tau ** 2)

    # step 3
    fA = f(__rating, tau, A, _delta, v, a)
    fB = f(__rating, tau, B, _delta, v, a)

    # step 4
    while math.fabs(B - A) > eps:
        # a
        C = A + ((A - B) * fA) / (fB - fA)
        fC = f(__rating, tau, C, _delta, v, a)
        # b
        if fC * fB < 0:
            A = B
            fA = fB
        else:
            fA = fA / 2.0
        # c
        B = C
        fB = fC

    # step 5
    return math.exp(A / 2)


class Player:
    def _preRatingRD(self):
        self.__rd = pre_rating_rd(self.__rd, self.vol)

    def getRating(self):
        return get_rating(self.__rating)

    def setRating(self, rating):
        self.__rating = set_rating(rating)

    rating = property(getRating, setRating)

    def getRd(self):
        return get_rd(self.__rd)

    def setRd(self, rd):
        self.__rd = set_rd(rd)

    rd = property(getRd, setRd)

    def __init__(self, rating=1500, rd=350, vol=0.06, tau=0.5):
        # For testing purposes, preload the values
        # assigned to an unrated player.
        self.setRating(rating)
        self.setRd(rd)
        self.vol = vol
        self._tau = tau

    def update_player(self, rating_list, RD_list, outcome_list):
        """ Calculates the new rating and rating deviation of the player.

        update_player(list[int], list[int], list[bool]) -> None

        """
        # Convert the rating and rating deviation values for internal use.
        rating_list = [(x - 1500) / 173.7178 for x in rating_list]
        RD_list = [x / 173.7178 for x in RD_list]

        _v = v(self.__rating, rating_list, RD_list)
        self.vol = new_vol(self.__rating, self.__rd, rating_list, RD_list, outcome_list, _v, self.vol, self._tau)
        self._preRatingRD()

        self.__rd = 1 / math.sqrt((1 / math.pow(self.__rd, 2)) + (1 / _v))

        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += g(RD_list[i]) * \
                       (outcome_list[i] - E(self.__rating, rating_list[i], RD_list[i]))
        self.__rating += math.pow(self.__rd, 2) * tempSum

    def did_not_compete(self):
        """ Applies Step 6 of the algorithm. Use this for
        players who did not compete in the rating period.

        did_not_compete() -> None

        """
        self._preRatingRD()

