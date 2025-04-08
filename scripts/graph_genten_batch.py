import json
from matplotlib import pyplot as plt


output_files = [f'output/genten-2025-04-05-flickr-3d/genten-output-{run}.out' for run in range(7)]

def process_genten_batch(output_file):
    opts_line_prefix = '==> opts='
    resource_prefix = 'Rsrc Used:'
    walltime_prefix = 'walltime='
    info = {'failed': False}
    with open(output_file) as fp:
        for line in fp:
            if line.startswith(opts_line_prefix):
                info.update(json.loads(line[len(opts_line_prefix):]))
            if line.startswith(resource_prefix):
                line = line[len(resource_prefix):].strip()
                walltime = [record for record in line.split(',') if record.startswith(walltime_prefix)][0]
                walltime = walltime[len(walltime_prefix):]
                hours, minutes, seconds = [0 if t == '00' else int(t) for t in walltime.split(':')]
                info['walltime'] = hours * 60 + minutes
            if 'CANCELLED' in line or 'Terminated' in line:
                info['failed'] = True
    return info


def plot_gentensor_batch(files, title):
    # Nonzero count in millions
    nnz_count = []
    # Time taken by GenTensor
    times = []
    for output_file in files:
        info = process_genten_batch(output_file)
        tensor_size = 1
        for dim in info['dims']:
            tensor_size *= dim
        requested_nnz_count = info['density'] * tensor_size
        nnz_count.append(f'{int(requested_nnz_count / 10**6)}M')
        times.append(info['walltime'])
        print(nnz_count[-1])
        print(times[-1])
    print(times)
    fig, ax = plt.subplots()
    ax.bar(nnz_count, times)
    ax.set_title(title)
    ax.set_xlabel('number of nonzeros requested')
    ax.set_ylabel('time (minutes)')
    plt.show()


if __name__ == '__main__':
    plot_gentensor_batch(output_files, 'GenTensor tool for flickr-3d-like tensor')
