#!/usr/bin/env python3
import argparse
import os
import json


TENSOR = '~/scratch/tensors/flickr-3d.tns'
PROGRAM_OUTPUT_DIR = 'output/featen-2025-04-05-flickr-3d'


def featen_batch(featen_output, json_output, type_):
    """Return a FeaTensor batch script for the given options."""
    # Header
    body = [
        '#!/bin/sh',
        '#SBATCH -N 1',
        '#SBATCH -n 24',
        '#SBATCH --mem=0',
        f'#SBATCH -o {featen_output}',
    ]
    # Dump type
    body.append(f'printf "==> type={type_}\\n"')
    # Create output directories
    body.append(f'mkdir -p {PROGRAM_OUTPUT_DIR}')
    # Add time commands to get a rough estimate of how much time it took
    body.append('printf "==> start_time=%s\\n" $(date +%s)')
    # Add the command
    body.append(f'srun -N 1 -n 1 ./FeaTensor/featen -i {TENSOR} -c 0 -o {json_output} -m {type_}')
    body.append('printf "==> end_time=%s\\n" $(date +%s)')
    body.append('')
    return '\n'.join(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True, help='output directory')
    args = parser.parse_args()

    for i, type_ in enumerate(['map', 'sort', 'group', 'hybrid']):
        os.makedirs(PROGRAM_OUTPUT_DIR, exist_ok=True)
        featen_output = os.path.join(PROGRAM_OUTPUT_DIR, f'featen-output-{i}.out')
        json_output = os.path.join(PROGRAM_OUTPUT_DIR, f'featen-output-{i}.json')
        with open(os.path.join(args.output, f'batch-{i}.sh'), 'w') as fp:
            fp.write(featen_batch(featen_output, json_output, type_))
