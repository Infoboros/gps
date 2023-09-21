import georinex as gr
from matplotlib import pyplot as plt

OBS_PATH_FIRST = 'dra30350.23o'
OBS_PATH_SECOND = 'dra40350.23o'
SV = 'G15'

C = 299792458
fL_1 = 1575.42 * 10 ** 6
fL_2 = 1227.6 * 10 ** 6

GAMMA = fL_2 ** 2 / fL_1 ** 2
GAMMA_L1 = C / fL_1
GAMMA_L2 = C / fL_2

LAMBDA_L1 = C / fL_1
LAMBDA_L2 = C / fL_2


def ionofree_comb(F_L1, F_L2):
    F_if_star = F_L1 - GAMMA * F_L2
    return F_if_star / (1 - GAMMA)


def widelane_comb(F_L1, F_L2):
    F_wl_star = F_L1 / GAMMA_L1 - F_L2 / GAMMA_L2
    return F_wl_star * GAMMA_L1 * GAMMA_L2 / (GAMMA_L2 - GAMMA_L1)


def get_FL1_and_FL2(L1, L2):
    return LAMBDA_L1 * L1, LAMBDA_L2 * L2


def get_ionfree_and_widelane(path: str):
    obs = gr.load(path).sel(sv=SV)
    ionfree = []
    widelane = []
    for L1, L2 in zip(obs['L1'], obs['L2']):
        F_L1, F_L2 = get_FL1_and_FL2(L1.data, L2.data)
        ionfree.append((ionofree_comb(F_L1, F_L2), L1.time))
        widelane.append((widelane_comb(F_L1, F_L2), L1.time))
    return ionfree, widelane


def get_diffs(second, first, y_range):
    return [
        second[y][0] - first[y][0]
        for y in y_range
        if second[y][1] == first[y][1]
    ]


ionfree_first_file, widelane_first_file = get_ionfree_and_widelane(OBS_PATH_FIRST)
ionfree_second_file, widelane_second_file = get_ionfree_and_widelane(OBS_PATH_SECOND)

ys = range(500, 1500)
plt.plot(
    ys,
    get_diffs(
        ionfree_second_file,
        ionfree_first_file,
        ys
    ),
    label='Разность ionofree-комбинаций измерений'
)
plt.plot(
    ys,
    get_diffs(
        widelane_second_file,
        ionfree_first_file,
        ys
    ),
    label='Разность widelane-комбинаций измерений'
)

plt.legend(loc='best')
plt.show()
