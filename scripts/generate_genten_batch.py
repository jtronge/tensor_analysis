#!/usr/bin/env python3
import argparse
import os


TENSOR_DIR = '~/scratch/genten-tests'
PROGRAM_OUTPUT_DIR = 'output/genten-2025-04-02'
OPTIONS = [
    {'dims': [dim, dim, dim], 'density': density, 'fiber_density': density * 4}
    for density in [0.1, 0.1e-6, 0.1e-10]
    for dim in [8**i * 100 for i in range(8)]
]


def genten_batch(opts, output_tensor, genten_output):
    """Return a GenTensor batch script for the given options."""
    dims = opts['dims']
    dim_args = ' '.join(str(dim) for dim in dims)
    density = opts['density']
    fiber_density = opts['fiber_density']
    body = [
        '#!/bin/sh',
        '#SBATCH -N 1',
        '#SBATCH -n 24',
        '#SBATCH --mem=0',
        f'#SBATCH -o {genten_output}',
    ]
    body.append('printf "## options:\\n"')
    for opt, value in opts.items():
        body.append(f'printf "{opt}={value}\\n"')
    body.append('printf "## end options\\n"')
    body.append(f'mkdir -p {PROGRAM_OUTPUT_DIR}')
    body.append(f'mkdir -p {TENSOR_DIR}')
    body.append(f'srun -N 1 -n 1 time ./GenTensor/genten {len(dims)} {dim_args} -d {density} -f {fiber_density} -s 1 -o {output_tensor}')
    body.append('')
    return '\n'.join(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True, help='output directory')
    args = parser.parse_args()

    for i, opts in enumerate(OPTIONS):
        opts = dict(opts)
        output_tensor = os.path.join(TENSOR_DIR, f'sample-{i}.tns')
        genten_output = os.path.join(PROGRAM_OUTPUT_DIR, f'genten-output-{i}.out')
        with open(os.path.join(args.output, f'batch-{i}.sh'), 'w') as fp:
            fp.write(genten_batch(opts, output_tensor, genten_output))
