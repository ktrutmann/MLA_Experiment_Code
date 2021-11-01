# 3 Matrices Puzzles (ascending difficulty)
(Civelli, A. & Deck, C. (2018). A Flexible and Customizable Method for Assessing Cognitive Abilities. 
Review of Behavioral Economics, Volume 5, Issue 2, 2018, Pages 123-147. 
See online article publication: https://acivelli.hosted.uark.edu/PaperInterface.pdf )

This is a Test for Assessing Cognitive Abilities with 3 Matrices Puzzles (ascending difficulty; 
inspired by Raven’s Progressive Matrices (RPM)).
Each correct answer is incentiviced with 100 Points; calculated as follows:<br>
 3000 points / hour (50 points / minute) <br>
 estimated time for this Task: 6 minutes (= 300 Points)<br>
 points per correct solved matrix: 100 points (300 points / 3 tasks)<br>

After the 3 Puzzles, there are two questions to survey overplacement and overestimation.


The Matrices are generated with a Matlab Interface provided by Civelli & Deck 
(available here: https://acivelli.hosted.uark.edu/ResearchPage.html).

## Settings
The amount of incentivization can be adjustet in models.py, variable `endowment`.

## Exported Data
The main exports are the scores for the three matrices (`cogn_rpm_matrix_1` - `cogn_rpm_matrix_3`) 
and the total score (`cogn_rpm_total_points`).
In addition, the results of the variables overestimation (`pers_rpm_overestimation`) and 
overplacement (`pers_rpm_overplacement`) are in the output file.
