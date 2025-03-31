import json
from matplotlib import pyplot as plt
import numpy as np


def load_tensor_features(fname):
    with open(fname) as fp:
        data = json.load(fp)
    return data


def get_dimensions(tensor_info):
    return [tensor_info['base'][dim] for dim in ['dim_0', 'dim_1', 'dim_2']]


def permute_tensor_dims(dims):
    """Return a permutation of the tensor dimensions such that the dimensions are ordered from smallest to largest."""
    ordered = sorted((dim, i) for i, dim in enumerate(dims))
    return [i for _, i in ordered]


if __name__ == '__main__':
    amazon_reviews = load_tensor_features('tensor_features/amazon-reviews.json')
    aminer = load_tensor_features('tensor_features/aminer.json')
    fig, ax = plt.subplots(1, 3)
    fig.suptitle('Coefficient of variation for AMiner and amazon-reviews tensors')
    key2name = {
        'slices': 'nonzeros per slice',
        'fibers': 'nonzeros per fiber',
        'fibperslice': 'fibers per slice',
    }
    dims_aminer = get_dimensions(aminer)
    dims_amazon_reviews = get_dimensions(amazon_reviews)
    # Get a permutation for the tensor dimensions from smallest to largest
    perm_aminer = permute_tensor_dims(dims_aminer)
    perm_amazon_reviews = permute_tensor_dims(dims_amazon_reviews)
    for i, key in enumerate(['slices', 'fibers', 'fibperslice']):
        aminer_cv = [aminer[key][i]['cv'] for i in perm_aminer]
        amazon_reviews_cv = [amazon_reviews[key][i]['cv'] for i in perm_amazon_reviews]
        assert len(aminer_cv) == len(amazon_reviews_cv)
        width = 0.2
        x = np.arange(len(aminer_cv))
        ax[i].set_title(key2name[key])
        ax[i].bar(x, aminer_cv, label='aminer', width=width)
        ax[i].bar(x + width, amazon_reviews_cv, label='amazon-reviews', width=width)
        ax[i].set_xticks(x + 0.5 * width, x)
        if i == 2:
            ax[i].legend()
    plt.show()
