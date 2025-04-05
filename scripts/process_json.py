import argparse
import json
import pprint
import subprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fname')
    args = parser.parse_args()
    with open(args.fname) as fp:
        data = json.load(fp)
    base = data['base']
    assert base['order'] == 3
    dims = [base[key] for key in ['dim_0', 'dim_1', 'dim_2']]
    print('dims:', dims)
    nnz = base['nnz']
    print('nnz:', nnz)
    sparsity = base['sparsity']
    print('sparsity:', sparsity)
    fiber_sparsity = base['fiber_sparsity']
    print('fiber_sparsity:', fiber_sparsity)
    slice_sparsity = base['slice_sparsity']
    print('slice_sparsity:', slice_sparsity)
    #pprint.pprint(data)
    #genten_args = ['./genten', '3']
    #genten_args.extend([dim * args.factor for dim in dims])
    ## Density (sparsity)
    #genten_args.extend(['-d', sparsity])
    ## Fiber sparsity
    #genten_args.extend(['-f', fiber_sparsity])
    ## Fiber sparsity
    #genten_args.extend(['-s', slice_sparsity])
    #genten_args.extend(['-o', args.output])
    #genten_args = [str(arg) for arg in genten_args]
    #print(' '.join(genten_args))
