# Empirical Bayes in Python: lesson notebooks

Workbook notebooks for *Introduction to Empirical Bayes: Examples from Baseball Statistics* by David Robinson (2017). The PDF is in the folder above this one. The book's code is in R; these lessons are in Python, and you write the code.

Each notebook has a topic, a question and goal, a contents list and tags, then a setup cell (already written) followed by prompts:

- **Your turn**: a task, with empty code cells beneath it for your code;
- **Check**: values to compare against (from the book; recent seasons in the data can shift them slightly);
- **Reflect**: a question to answer in a sentence or two;
- **Card connection**: an optional link to the card price project, using simulated data.

## Starting up

In an **Anaconda Prompt**:

```
conda activate pymc
cd "C:\Users\XPS-13\Dropbox\Programming\BayesStatsCardsandComputers\empirical_bayes"
jupyter lab
```

Open a notebook and choose the **Python (pymc)** kernel if asked. Lesson 02's setup cell downloads the baseball data into `data/lahman/` (about 10 MB, once). If the download fails, get the CSV version from https://sabr.org/lahman-database/ and unzip it anywhere inside `data/lahman/`.

Lesson 07 uses `patsy` for splines. If it's missing: `conda install -n pymc -c conda-forge patsy`.

## Lessons

| # | Notebook | Book | Question | Tags |
|---|---|---|---|---|
| 01 | `01_beta_distribution` | Ch. 2 | Why should one hit barely change our belief about a batter? | beta distribution, conjugate prior, simulation |
| 02 | `02_empirical_bayes_estimation` | Ch. 3 | Who were the best and worst hitters, fairly compared? | empirical Bayes, MLE, shrinkage |
| 03 | `03_credible_intervals` | Ch. 4 | How uncertain is each estimate? | credible vs confidence intervals |
| 04 | `04_hypothesis_testing_fdr` | Ch. 5 | Who belongs in a ".300 Hall of Fame"? | PEP, false discovery rate, q-values |
| 05 | `05_bayesian_ab_testing` | Ch. 6 | Is Piazza really better than Aaron? | A/B testing, four computational routes |
| 06 | `06_beta_binomial_regression` | Ch. 7 | Are short-career players overrated by shrinkage? | beta-binomial regression, confounding |
| 07 | `07_hierarchical_modeling` | Ch. 8 | Lefty or righty, and does the era matter? | hierarchical priors, splines, interactions |
| 08 | `08_mixture_models_em` | Ch. 9 | Can batting alone find the pitchers? | mixtures, EM, clustering |
| 09 | `09_dirichlet_multinomial` | Ch. 10 | Who were the best sluggers? | Dirichlet, multinomial |
| 10 | `10_build_your_own_toolkit` | Ch. 11 | Can it all fit in one small module? | writing `my_eb.py`, review |
| 11 | `11_simulation` | Ch. 12 | Does empirical Bayes actually work? | simulation, calibration, parameter recovery |
| 12 | `12_simulating_replications` | Ch. 13 | When does it fail? | replications, sample size |
| 13 | `13_full_bayes_pymc` | beyond the book | What does full Bayes add? | PyMC 6, hierarchical beta-binomial |

The lessons build on each other: Lesson 02 saves your prior to `results/results.json` for later lessons, Lesson 06 writes a fitting function reused in 07 and 10, and Lessons 11–12 import the `my_eb.py` module you write in Lesson 10.

## Files

- `eb_data.py`: data plumbing (download, the per-chapter tables, saving results between lessons). The statistics are left to you.
- `data/lahman/`: the baseball data, created on first run.
- `results/`: values saved by one lesson for the next.
- `my_eb.py`: yours to write in Lesson 10.

## Credits

- David Robinson, *Introduction to Empirical Bayes: Examples from Baseball Statistics* (2017). Book source: https://github.com/dgrtwo/empirical-bayes-book. The lessons follow its structure and examples; the explanations here are short summaries, so read the book alongside.
- Sean Lahman's Baseball Database, CC BY-SA 3.0 (https://sabr.org/lahman-database/), via the Chadwick Bureau's `baseballdatabank`.
