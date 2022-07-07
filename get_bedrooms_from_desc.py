import re
import numpy as np

def get_bedrooms(description):
    m = re.search('\d* (?=bedroom)', description)

    # it is a normal apartment
    if m is not None:
        return int(m.group(0).strip())

    # It is a studio apartment
    elif re.search('studio', description) is not None:
        return 1

    # it is not an apartment, maybe a parking lot
    else:
        return np.NaN
