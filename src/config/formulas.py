import math

import flet as ft


g = 9.81  # m/s^2
R = 287.05  # J/(kg*K)
T0 = 273.15  # K
alpha = -0.0065  # K/m


def qfe(
    qnh: float,  # hPa
    h_stn: float,  # m
    T: float,  # K
) -> float:
    """Computes the QFE for a station given its QNH, height and temperature.
    See the Vaisala website for more details:
    https://docs.vaisala.com/r/M210855EN-E/en-US/GUID-5D3900BF-2FAD-4E11-9A68-B0A3D6F80240

    Args:
        qnh (float): QNH in hectopascals (hPA).
        h_stn (float): height above sea level of station in meters (m).
        T (float): temperature in Kelvin (K).

    Returns:
        float: the QFE computed.
    """
    numerator = h_stn * g
    denominator = R * (T + T0 + (alpha * h_stn) / 2)
    exponent = math.e ** -(numerator / denominator)
    return qnh * exponent
