from gt4py.cartesian.gtscript import BACKWARD, FORWARD, computation, interval

from ndsl.dsl.typing import FloatField

def tridiag_solve(
    a: FloatField,
    b: FloatField,
    c: FloatField,
    d: FloatField,
    x: FloatField,
    delta: FloatField,
):
    """
    This stencil solves a square, k x k tridiagonal matrix system
    with coefficients a, b, and c, and vectors p and d using the Thomas algorithm:
    ! ###                                            ### ###  ###   ###  ###!
    ! #b(0), c(0),  0  ,  0  ,  0  ,   . . .  ,    0   # # x(0) #   # d(0) #!
    ! #a(1), b(1), c(1),  0  ,  0  ,   . . .  ,    0   # # x(1) #   # d(1) #!
    ! # 0  , a(2), b(2), c(2),  0  ,   . . .  ,    0   # # x(2) #   # d(2) #!
    ! # 0  ,  0  , a(3), b(3), c(3),   . . .  ,    0   # # x(3) #   # d(3) #!
    ! # 0  ,  0  ,  0  , a(4), b(4),   . . .  ,    0   # # x(4) #   # d(4) #!
    ! # .                                          .   # #  .   # = #   .  #!
    ! # .                                          .   # #  .   #   #   .  #!
    ! # .                                          .   # #  .   #   #   .  #!
    ! # 0  , . . . , 0 , a(k-2), b(k-2), c(k-2),   0   # #x(k-3)#   #d(k-3)#!
    ! # 0  , . . . , 0 ,   0   , a(k-1), b(k-1), c(k-1)# #x(k-2)#   #d(k-2)#!
    ! # 0  , . . . , 0 ,   0   ,   0   ,  a(k) ,  b(k) # #x(k-1)#   #d(k-1)#!
    ! ###                                            ### ###  ###   ###  ###!

    Inputs:
        a: lower-diagonal matrix coefficients
        b: diagonal matrix coefficients
        c: upper-diagonal matrix coefficients
        d: Result vector
    Outputs:
        x: The vector to solve for
        delta: d post-pivot
    """
    with computation(FORWARD):  # Forward sweep
        with interval(0, 1):
            x = c / b
            delta = d / b
        with interval(1, None):
            x = c / (b - a * x[0, 0, -1])
            delta = (d - a * delta[0, 0, -1]) / (b - a * x[0, 0, -1])
    with computation(BACKWARD):  # Reverse sweep
        with interval(-1, None):
            x = delta
        with interval(0, -1):
            x = delta - x * x[0, 0, 1]