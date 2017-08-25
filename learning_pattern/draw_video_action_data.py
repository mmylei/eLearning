import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
# Random state.
RS = 20150101
# We'll use matplotlib for graphics.
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
# We import seaborn to make nice plots.
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})
# We'll generate an animation with matplotlib and moviepy.
# from moviepy.video.io.bindings import mplfig_to_npimage
# import moviepy.editor as mpy
import json_wrapper


def non_0_row_index(df):
    return (df.T > 0.0001).any()


def drop_long_real_spent_row(df):
    week_df = df[df.real_spent <= 10]
    return week_df


def grades_to_labels(grades):
    # logger.info('grades, mean: ' + str(np.mean(grades)) + ', max: ' + str(np.max(grades)) + ', min: ' + str(np.min(grades)))
    good_normal = np.percentile(grades, 85)
    normal_poor = np.percentile(grades, 35)
    # logger.info('good threshold: ' + str(good_normal))
    # logger.info('poor threshold: ' + str(normal_poor))
    return np.array(map(lambda x: 1 if x >= good_normal else (2 if x < normal_poor else 0), grades), dtype=np.intp)


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


# new feature
df = pd.read_csv('weekly_quantities.csv')
bins = np.array([[0, 1.2, 3.2, 4], [0, 5.2, 10.4, 13], [0, 4.5, 8.1, 9], [0, 4, 8], [0, 4.8, 10.8, 12]], dtype=np.float32)
for week_number in range(1, 6):
    print '-------------- week', week_number, '--------------'
    # indices = np.where(features[:, 0] == week_number)[0]  # only keep week 1 data
    # Y = features[indices, :][:, len(columns)-3]  # grade (last column)
    # X = features[indices, :][:, range(1, len(columns)-3)]  # except module_number (first column) and grade (last column)
    week_df = df[df.module_number == week_number]
    week_df = week_df.groupby('uid') \
        .agg({'real_spent': 'mean', 'coverage': 'mean', 'watched': 'mean', 'pauses': 'mean',
              'pause_length': 'mean', 'avg_speed': 'mean', 'std_speed': 'mean',
              'seek_backward': 'mean', 'seek_forward': 'mean', 'attempts': 'max', 'grade': 'max'}) \
        .reset_index()
    # week_df = drop_all_0_row(week_df)
    week_df = drop_long_real_spent_row(week_df).reset_index()
    X = week_df[
        ['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward',
         'seek_forward', 'attempts']]
    idx = non_0_row_index(X)
    X = X[idx].values
    week_df = week_df[idx].reset_index()
    Y = week_df['grade'].values
    Y = np.digitize(Y, bins[week_number-1])
    data_proj = TSNE(random_state=RS).fit_transform(X)
    scatter(data_proj, Y)
    plt.savefig('tsne-generated_' + str(week_number) + '.png', dpi=120)

# old feature
# f = open('data.json', 'r')
# data = json_wrapper.loads(f.read())
# f.close()
# X = np.array(data['features'], np.float32)
# Y = np.array(data['grades'], np.float32)
# Y = grades_to_labels(Y)
# for i in range(0, X.shape[1]/8):
#     X_video = X[:, np.arange(i*8, i*8+8)[[0,1,2,3,6,7]]]
#     data_proj = TSNE(random_state=RS).fit_transform(X_video)
#     scatter(data_proj, Y)
#     plt.savefig('tsne-generated_' + str(i) + '.png', dpi=120)
