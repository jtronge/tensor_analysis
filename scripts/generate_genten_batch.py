#!/usr/bin/env python3
import argparse
import os
import json


TENSOR_DIR = '~/scratch/genten-tests-flickr-3d'
PROGRAM_OUTPUT_DIR = 'output/genten-2025-04-05-flickr-3d'

# Initial dimensions and densities/sparsities are based on FeaTensor output
# for order 1 of the flickr-3d tensor
OPTIONS = [
    {'dims': [int(319686 * scale**(1/3)), int(28153045 * scale**(1/3)),
              int(1607191 * scale**(1/3))],
     'density': 7.80441e-12, 'fiber_density': 2.81914e-06,
     'cv_fiber_per_slice': 5.24218, 'cv_nnz_per_fiber': 1.04003}
    for scale in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
#    {'dims': [int(4821207 * scale**(1/3)), int(1774269 * scale**(1/3)),
#              int(1805187 * scale**(1/3))],
#     'density': 1.12798e-10, 'fiber_density': 6.23487e-05, 'scale': scale}
#    for scale in [1, 2, 3, 4]
]


def genten_batch(opts, output_tensor, genten_output):
    """Return a GenTensor batch script for the given options."""
    dims = opts['dims']
    dim_args = ' '.join(str(dim) for dim in dims)
    density = opts['density']
    fiber_density = opts['fiber_density']
    cv_fiber_per_slice = opts['cv_fiber_per_slice']
    cv_nnz_per_fiber = opts['cv_nnz_per_fiber']
    # Header
    body = [
        '#!/bin/sh',
        '#SBATCH -N 1',
        '#SBATCH -n 24',
        '#SBATCH --mem=0',
        f'#SBATCH -o {genten_output}',
    ]
    # Dump options
    body.append(f"printf '==> opts={json.dumps(opts)}'\"\\n\"")
    # Create output directories
    body.append(f'mkdir -p {PROGRAM_OUTPUT_DIR}')
    body.append(f'mkdir -p {TENSOR_DIR}')
    # Add time commands to get a rough estimate of how much time it took
    body.append('printf "==> start_time=%s\\n" $(date +%s)')
    # Add the command
    body.append(f'srun -N 1 -n 1 ./GenTensor/genten {len(dims)} {dim_args} -d {density} -f {fiber_density} -c {cv_fiber_per_slice} -v {cv_nnz_per_fiber} -s 1 -o {output_tensor}')
    body.append('printf "==> end_time=%s\\n" $(date +%s)')
    body.append('')
    return '\n'.join(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True, help='output directory')
    args = parser.parse_args()

    for i, opts in enumerate(OPTIONS):
        opts = dict(opts)
        # Create the directory for Slurm
        os.makedirs(PROGRAM_OUTPUT_DIR, exist_ok=True)
        output_tensor = os.path.join(TENSOR_DIR, f'sample-{i}.tns')
        genten_output = os.path.join(PROGRAM_OUTPUT_DIR, f'genten-output-{i}.out')
        with open(os.path.join(args.output, f'batch-{i}.sh'), 'w') as fp:
            fp.write(genten_batch(opts, output_tensor, genten_output))
