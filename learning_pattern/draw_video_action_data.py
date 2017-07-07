import numpy as np
from numpy import linalg
from numpy.linalg import norm
from scipy.spatial.distance import squareform, pdist
# We import sklearn.
import sklearn
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
# We'll hack a bit with the t-SNE code in sklearn 0.15.2.
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.manifold.t_sne import (_joint_probabilities,
                                    _kl_divergence)
from sklearn.utils.extmath import _ravel
# Random state.
RS = 20150101
# We'll use matplotlib for graphics.
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
# We import seaborn to make nice plots.
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})
# We'll generate an animation with matplotlib and moviepy.
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
import json_wrapper


def grades_to_labels(grades):
    logger.info('grades, mean: ' + str(np.mean(grades)) + ', max: ' + str(np.max(grades)) + ', min: ' + str(np.min(grades)))
    good_normal = np.percentile(grades, 85)
    normal_poor = np.percentile(grades, 35)
    logger.info('good threshold: ' + str(good_normal))
    logger.info('poor threshold: ' + str(normal_poor))
    return np.array(map(lambda x: 1 if x >= good_normal else (-1 if x < normal_poor else 0), grades), dtype=np.intp)


def scatter(x, colors):
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", 10))
    # We create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40,
                    c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')
    # We add the labels for each digit.
    txts = []
    for i in range(10):
        # Position of each label.
        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)
    return f, ax, sc, txts


f = open('data.json', 'r')
data = json_wrapper.loads(f.read())
f.close()
X = np.array(data['features'], np.float32)
Y = np.array(data['grades'], np.float32)
Y = grades_to_labels(Y)
data_proj = TSNE(random_state=RS).fit_transform(X)
scatter(data_proj, Y)
plt.savefig('tsne-generated.png', dpi=120)
