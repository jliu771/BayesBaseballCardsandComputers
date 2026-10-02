# Bayes, Stats, Cards and Computers

A self-study project in statistics, Bayesian methods and computation, in Python. Lessons are anchored to real problems where possible, including a Pokémon card price project.

The first course here is a set of Jupyter workbooks that follow David Robinson's *Introduction to Empirical Bayes: Examples from Baseball Statistics*, with all the code in Python.

## What's here

| Path | What it is |
|---|---|
| `empirical_bayes/` | 13 lesson notebooks on empirical Bayes, using baseball batting averages. See its [README](empirical_bayes/README.md) for the lesson list. |
| `empirical_bayes/eb_data.py` | Downloads the baseball data and builds the tables each lesson starts from. |
| `LEARNING_STATS_HANDOFF.md` | Working notes for the wider learning plan: resources, environment notes, topics so far and open items. |

## The lessons

The notebooks are **workbooks, not solutions**. Each one starts with a topic, a question, a goal, a contents list and tags, then a setup cell that's ready to run. After that come prompts:

- **Your turn**: a task, with empty code cells for you to fill in;
- **Check**: values to compare your results against;
- **Reflect**: a question to answer in a sentence or two;
- **Card connection**: an optional exercise applying the idea to trading-card data (simulated).

Lessons 01–12 follow Chapters 2–13 of the book: the beta distribution, empirical Bayes estimation, credible intervals, false discovery rates, A/B testing, beta-binomial regression, hierarchical priors, mixture models and EM, the Dirichlet-multinomial, building a small toolkit, and simulation. Lesson 13 goes beyond the book and compares empirical Bayes with a full Bayesian model in PyMC.

## You'll need the book

The book isn't included here. It's a paid ebook, available on Amazon and other stores. The blog series it grew out of is free on David Robinson's blog, [Variance Explained](http://varianceexplained.org/). Its R source is at [dgrtwo/empirical-bayes-book](https://github.com/dgrtwo/empirical-bayes-book).

## Setup

You need Python 3.11 or newer with Jupyter. With Anaconda or Miniconda, create an environment from an Anaconda Prompt (or any terminal):

```
conda create -n pymc -c conda-forge python=3.12 pymc nutpie arviz jupyterlab pandas scipy matplotlib patsy
conda activate pymc
```

Lessons 01–12 need only numpy, pandas, scipy, matplotlib and patsy. PyMC, nutpie and ArviZ are for Lesson 13, which is written for **PyMC 6 and ArviZ 1**. Older tutorials use different function names.

Then start Jupyter from the activated environment:

```
cd path\to\BayesStatsCardsandComputers\empirical_bayes
jupyter lab
```

Open `01_beta_distribution.ipynb` and work through the lessons in order. Later lessons reuse results and functions from earlier ones.

## Data

The baseball data is the [Lahman Baseball Database](https://sabr.org/lahman-database/) (CC BY-SA 3.0). It isn't stored in the repo: Lesson 02's setup cell downloads it into `empirical_bayes/data/lahman/` the first time you run it (about 10 MB). If the download fails, download the CSV version from the SABR page and unzip it into that folder.

The card-project exercises use simulated data only, because the real card price data comes from sources whose terms don't allow republishing it.

## Credits

- David Robinson, *Introduction to Empirical Bayes: Examples from Baseball Statistics* (2017). The lessons follow its structure and examples.
- Sean Lahman's Baseball Database, via SABR and the Chadwick Bureau.
