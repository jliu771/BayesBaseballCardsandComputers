# Learning statistics: handoff

Written 2026-10-02. This starts a separate, running topic: learning statistics, Bayesian methods, computation and modelling, in Python where possible. It grew out of the card price project (the reading list for notebooks 04 and 07), but it's its own thread. In time it may become something published regularly: a blog series or even a course.

To pick it up in a new conversation, link the folder holding this file and say: *"Read LEARNING_STATS_HANDOFF.md, then let's continue the learning thread."*

## The learner

- Jonathan has experience in data analysis and visualization, and has used PyMC and MCMC before, some time ago.
- Works on Windows with Anaconda and Jupyter. A beginner on the command line, so give exact commands.
- Prefers Python. When a resource is in R (Statistical Rethinking's book code), find or write the Python version.
- Learns best tied to something real. The card price project is the running worked example (see below).

## Environment

- Conda environment `pymc`, Jupyter kernel "Python (pymc)": PyMC 6.3.1, PyTensor 3.3.2, ArviZ 1.3 (split into arviz-base, arviz-stats and arviz-plots), nutpie 0.16.11, pandas 3.0, numpy 2.5.
- **Start Jupyter from the activated environment** (`conda activate pymc`, then `jupyter lab`). Otherwise the first chart can crash the kernel. The details are in `ENVIRONMENT_NOTES.md` in the Cardprice folder, and the PATH-fix block from that file goes at the top of any new notebook's first cell.
- **Version gap:** almost all learning material predates PyMC 6 and ArviZ 1. The statistics carry over; the code names don't. Examples:
  - `pm.sample` now returns an xarray `DataTree` instead of `InferenceData`;
  - ArviZ functions moved: `az.summary` → `arviz_stats.summary`, `az.plot_trace` → `arviz_plots.plot_trace_dist`;
  - the default interval is now an 89% equal-tailed interval instead of a 94% HDI;
  - a dimension can't share a name with a variable.
  
  When adapting old examples, check the current docs.

## Resources so far

From the reading list (`Stats_Reading_List_Notebooks_04_07.pdf` in Downloads, 2026-09-30):

1. **Statistical Rethinking** (McElreath): the main resource. Book plus free lecture videos.
   - Course materials: https://github.com/rmcelreath/stat_rethinking_2026
   - PyMC ports of the book's code: https://github.com/pymc-devs/pymc-resources/tree/main/Rethinking_2
   - Jonathan has cloned **https://github.com/dustinstansbury/statistical-rethinking-2023**, a Python/PyMC version of the 2023 lectures.
2. **Regression and Other Stories** (Gelman, Hill, Vehtari): grounding for regression and notebook 04.
   - Free PDF: https://users.aalto.fi/~ave/ROS.pdf
3. **Bayesian Modeling and Computation in Python** (Martin, Kumar, Lao): optional, hands-on PyMC and ArviZ code. Listed at https://www.pymc.io/projects/docs/en/stable/learn/books.html
4. **Introduction to Empirical Bayes: Examples from Baseball Statistics** (David Robinson, 2017): added 2026-10-02. A short, practical book built from his Variance Explained blog series. It estimates batting averages: a beta prior fitted to all players, shrinkage, credible intervals, hypothesis testing and false discovery rates, A/B testing, beta-binomial regression, hierarchical priors, mixture models and EM, the Dirichlet-multinomial, and simulation.
   - The PDF is in this folder (`IntroductionToEmpiricalBayes-DavidRobinson.pdf`). Book source: https://github.com/dgrtwo/empirical-bayes-book
   - The book's code is in R; the lessons are in Python (see below).
   - Card-project fit: pull rates (hits out of packs opened, with few packs for some sets) and other low-count proportions are exactly the batting-average problem. It also bridges to notebook 07: empirical Bayes fits the prior from the data and plugs it in, while a full multilevel model also carries the uncertainty in that prior.

## The running example: the card price project

Each concept below already appears in a Cardprice notebook, so lessons can point at working code and real results.

| Concept | Where it shows up | Statistical Rethinking chapter |
| --- | --- | --- |
| Log transform: effects as multipliers, the median vs the mean | 04 (OLS on log price) | 4; ROS ch. 12 |
| Linear regression, polynomial terms, partial residuals | 04 (age + age², section 5b) | 4 |
| Cluster-robust standard errors | 04 | (ROS, lightly) |
| Splines (B-spline basis, random-walk prior) | 07 (`D_both_spline`) | 4 |
| Robust likelihood (Student-t) | 07, 07b | 7 |
| Monotonic ordered predictors | 07 (rarity ladder), 07b (condition ladder) | 12 |
| Multilevel models: varying intercepts, partial pooling, non-centered parameterization | 07 (card, set, illustrator, Pokémon) | 13–14 |
| MCMC diagnostics: R-hat, ESS, divergences, rank plots | 07 | 9 |
| Prior and posterior predictive checks | 07, 07b | throughout |
| PSIS-LOO, Pareto k, model comparison | 07 | 7 |
| Grouped cross-validation, interval coverage, calibration | 07 (by card), 08 | 7 |
| A one-time holdout, and why you look only once | 08 | — |
| Simulation and parameter recovery | 07b (`USE_SIMULATED`) | throughout (simulate first) |
| Nonlinear models beyond GLMs | 07b (price-level scaling) | — |
| Missing data and missing-at-random | 07b (missing played-condition prices) | 15 |

Results worth reusing as teaching material:
- **Notebook 07's final model C_both** is typically off by a factor of 1.72 in cross-validation, against 1.97 for the OLS. Its 90% intervals cover 90.6%.
- **`Card_Price_Trait_Effects.pdf`** ranks traits by catalog-wide spread: age 4.6×, rarity 3.9×, then the varying effects. That's a variance-decomposition example.

## Topics already discussed (seeds for lessons)

- **Generalized linear models and the project (2026-10-01).** A GLM has three parts: a linear predictor, a link function and an outcome distribution.
  - **04** is the identity-link Normal case on log price.
  - **07** is a GLM-shaped multilevel model (a GLMM). Its Student-t likelihood isn't a classic exponential-family distribution, and MCMC doesn't need one.
  - **Splines, the quadratic age term and the monotonic ladder** are still linear in the parameters.
  - **07b** is genuinely nonlinear.
  - **Log the outcome or use a log link?** Logging the outcome models the median price; a log-link GLM (such as a Gamma GLM) models the mean. For fair value the median is right.
  - **Real GLM uses in the project:** logistic regression for missing prices, Binomial for pull rates, negative binomial for sales counts.
- **Two layers of unexplained variance in a multilevel model (2026-10-01).** Residuals relative to the traits include the card's own premium (a card being Charizard), while residuals relative to everything are only the noise σ. A residual section for notebook 07 was proposed: a histogram with the fitted Student-t curve, residuals against fitted values, residuals by era, and a bar chart splitting the variance. Not built yet.
- **Harmless RuntimeWarnings in notebook 07's cross-validation.** Some reported quantities are fixed at zero by construction, such as the reference rung of a ladder, so dividing by their spread warns. A lesson on reference categories and identifiability.
- **Partial pooling in practice.** Set effects let the model price a card from a set it has never seen, which set dummies can't. That was Jonathan's reason for choosing a multilevel model.

## Suggested shape of the thread (not agreed)

A rough sequence, each step anchored to the card project where possible:

1. Probability and simulation: thinking generatively and simulating data before modelling.
2. Regression as a model, not a recipe: log scales, interpretation, checking fit (04).
3. Bayesian basics: priors, likelihood, posterior; grid approximation, then MCMC.
4. MCMC in practice: what NUTS does, diagnostics, what divergences mean (07).
5. Model checking and comparison: predictive checks, LOO, cross-validation, calibration (07, 08).
6. Multilevel models: pooling, shrinkage, non-centered parameterization (07).
7. GLMs: logistic, Poisson and negative binomial, ordered outcomes.
8. Special structures: monotonic effects, splines, nonlinear models, missing data (07, 07b).
9. Causal thinking: DAGs and confounding (Statistical Rethinking's other half; the card project is mostly prediction, so new examples are needed).
10. Computation: PyTensor graphs, samplers (nutpie), performance, reparameterization.

## Working toward a blog or course

To keep the option open without extra work later, give each session's main idea a consistent shape:
- **the question** (ideally from the card project);
- **the intuition**, in plain words;
- **the maths**, kept minimal;
- **the code**, as runnable Python using current PyMC 6 and ArviZ 1;
- **a figure**;
- **a short exercise**;
- **references**.

A running log, one entry per session, can then be edited into posts or course units.

Decisions for later:
- **Format and platform:** for example, Jupyter notebooks published as a Quarto or Jupyter Book site, or a newsletter or blog with linked notebooks.
- **Audience:** the level of maths assumed, and whether readers need Python already.
- **Data rights before publishing anything:**
  - **TCGdex:** check its terms on reuse.
  - **Scrydex:** a paid plan's terms forbid bulk redistribution, so its data can't be published as a dataset.
  - **Pull rates scraped from thepricedex.com:** shouldn't be republished.
  
  Course material may need simulated data, or small extracts within those terms.
- **Credit:** how lessons acknowledge the books and courses they follow.

## Empirical Bayes lesson notebooks (2026-10-02)

Folder `empirical_bayes/` in this folder: 13 Jupyter workbooks following Robinson's book. Lessons 01–12 follow Chapters 2–13, and Lesson 13 bridges to full Bayes in PyMC.
- Each notebook has a topic, a question and goal, a contents list and tags, then a filled-in setup cell. After that come **Your turn** prompts with empty code cells for Jonathan to write, plus **Check** values, **Reflect** questions and optional **Card connection** exercises on simulated data.
- `eb_data.py` handles the data: it downloads the Lahman CSVs into `data/lahman/`, builds each chapter's tables, and saves results between lessons in `results/results.json`. The statistics are left to the learner.
- Lessons depend on earlier ones. Lesson 02 saves the prior, Lesson 06 writes a beta-binomial regression function reused in 07 and 10, and Lesson 10 builds `my_eb.py`, which 11–12 import.
- The lesson metadata, including tags, is stored in each notebook's metadata under `lesson`, for a possible course site later.
- `README.md` in that folder lists the lessons and the startup commands.

## Open items

- [x] Where this thread's files live: `Dropbox\Programming\BayesStatsCardsandComputers`.
- [ ] Start a running log (`LEARNING_LOG.md`), one entry per session.
- [ ] Pick the first topic. Natural candidates:
  - the residual section for notebook 07;
  - working through the cloned Statistical Rethinking 2023 notebooks under PyMC 6, noting each API change as it comes up;
  - a lesson on simulation and parameter recovery using 07b.
  - working through the Empirical Bayes lessons (`empirical_bayes/`, start with Lesson 01).
