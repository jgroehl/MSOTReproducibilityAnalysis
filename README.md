# Code supplementing the paper: *Teachability Of Multispectral Optoacoustic Tomography* 

Yi Li<sup>1#</sup>, 
Janek Gröhl<sup>2,3#</sup>, 
Briain Haney<sup>1</sup>, 
Milenko Caranovic<sup>1</sup>, 
Eva Lorenz-Meyer<sup>1,7</sup>, 
Julius Kempf<sup>1</sup>, 
Adrian P. Regensburger<sup>4</sup>, 
Emmanuel Nedoschill<sup>4</sup>, 
Adrian Bühler<sup>4</sup>, 
Werner Lang<sup>1</sup>, 
Michael Uder<sup>5</sup>, 
Markus F. Neurath<sup>6,8,9</sup>, 
Maximilian Waldner<sup>6,8,9</sup>, 
Ferdinand Knieling<sup>4*</sup>, 
Ulrich Rother<sup>1*</sup>  

<sup>#</sup> ,<sup>*</sup> Contributed equally

###Affiliations

1 Department of Vascular Surgery, University Hospital Erlangen, 
Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), 
Krankenhausstraße 12, D-91054 Erlangen, Germany

2 Cancer Research UK Cambridge Institute, University of Cambridge, Cambridge, U.K.

3 Department of Physics, University of Cambridge, Cambridge, U.K.

4 Department of Pediatrics and Adolescent Medicine, University Hospital Erlangen, 
Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), Loschgestraße 15, D-91054 
Erlangen, Germany

5 Institute of Radiology, University Hospital Erlangen, Friedrich-Alexander- 
Universität Erlangen-Nürnberg (FAU), Maximiliansplatz 1, D-91054 Erlangen, Germany

6 Department of Medicine 1, University Hospital Erlangen, Friedrich-Alexander- 
Universität Erlangen-Nürnberg (FAU), Ulmenweg 18, D-91054 Erlangen, Germany

7 Faculty of Medicine, Friedrich-Alexander- Universität Erlangen-Nürnberg (FAU), 
Krankenhausstraße 12, D-91054 Erlangen, Germany

8 Deutsches Zentrum für Immuntherapie (DZI), University Hospital Erlangen, 
Friedrich-Alexander- Universität Erlangen-Nürnberg (FAU), Ulmenweg 18, D-91054 
Erlangen, Germany

9 Erlangen Graduate School in Advanced Optical Technologies (SAOT), 
Friedrich-Alexander-Universität Erlangen-Nürnberg, Paul-Gordan-Straße 6, 
D-91052 Erlangen, Germany

## Installing

Download this repository from github and download the corresponding data from zenodo
(https://doi.org/10.5281/zenodo.10957316).

Create a new virtual environment and install the requirements listet in `requirements.txt`, 
for example, using `pip`:

    pip install -r requirements.txt

It is then important to change the `path.py` file and set the `BASE_DATA_PATH` variable
to point to the base directory of the data folder downloaded from zenodo.

Afterwards all scripts, apart from `process_data.py` should be
executable and should reproduce the results as depicted in the paper.

## General data analysis idea

We wanted to find out the repeatability of measurements of the
same muscle using a clinical photoacoustic imaging system with the focus on whether
there are significant differences between expert and novice users, and how a novice 
user that received personal training falls into this category.

Each operator took 7 independent measurements of a muscle on the left and right
extremity of 5 subjects. We treated each of the 10 locations as independent and 
used full-reference image quality measures to quantify the difference between the
measurements. For each location, we analyse all data pair permutations, assuming 
that d(A, B) = d(B, A) by computing the Mean Absolute Error, the Normalised Cross Correlation, the
Bhattacharyya Distance, and the Structural Similarity Index Measure. 

These values are computed using the `compute_distance_values.py` script and
the results are saved in a JSON file.

To assess whether there are significant differences between the measurements,
we then perform a bootstrapped ranking analysis resulting in a podium plot, where
randomly choose a subset of the data with replacement for 100 times and note down
which operator performed the best in the given data sample. Using these results, we can
compute the median rank of each operator for each of the distance measures, which gives
an indication if there are significant trends even with random data permutations.

This can be done with the `visualise_data_and_podium_plot.py` file and the results are
saved as SVG graphics in the base folder.

There are more script that visualise and plot different aspects of the findings: 
`overall_performance_results.py` prints the mean score for each measure over all
operators for the first imaging session compared to the second imaging session.
`showcase_variability_differences.py` creates a graphic that shows an example data
point to qualitatively assess the difference between an expert, novice and trained 
operator.
`visualise_example_data.py` visualises a PA + US data pair.

The operators recorded for 49 frames at each location and by default, 
the analysis is performed on the average reconstruction over those frames.
Additionally, PA imaging was performed over 6 wavelengths:
[700, 730, 760, 800, 850, 900] nanometers but only 800nm was chosen for the analysis. 
However, every third frame and all wavelengths are included in the zenodo data archive
and can also be used for other research purposes at the users discretion.
