from matplotlib import pyplot as plt
import numpy as np


def load_file(fname):
    """Load and return output from a psrecord plain text log.


    Return an array of (time, real mem in MB, virtual mem in MB) tuples.
    """
    results = []
    with open(fname) as fp:
        for line in fp:
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split()
            assert len(parts) == 4
            results.append((float(parts[0]), float(parts[2]), float(parts[3])))
    return results


def plot_psrecord(fname, title):
    results = load_file(fname)
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel('time (minutes)')
    ax.set_ylabel('memory (GB)')
    times = [result[0] / 60.0 for result in results]
    real_mem = [result[1] / 1024.0 for result in results]
    virt_mem = [result[2] / 1024.0 for result in results]
    ax.plot(times, real_mem, label='real memory')
    ax.plot(times, virt_mem, '--', label='virtual memory')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    plot_psrecord(fname='FeaTensor/psrecord-output/amazon-reviews-featen-activity.log',
                  title='Memory Usage: FeaTensor with amazon-reviews tensor')
    plot_psrecord(fname='FeaTensor/psrecord-output/patents-featen-activity.log',
                  title='Memory Usage: FeaTensor with patents tensor')
    plot_psrecord(fname='GenTensor/amazon-reviews-genten-activity.log',
                  title='Memory Usage: GenTensor with amazon-reviews based tensor')
