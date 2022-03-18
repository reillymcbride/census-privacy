<h2>Census Reconstruction Baseline: Randomly Generated from Block Distribution Data</h2>


**Code for CMSC 33211 Winter 2022 Final Project**

A baseline for census data reconstruction efforts that utilizes block level distribution data.

Data is for all blocks in Cook County, IL in 2010.


_Python Files:_
  - gen_distributions processes the block-level age-sex and race data, and outputs a csv of:
    - For every block, percent of the population that falls into each category 
      (i.e., percent of block that are males age 20-25, or percent of block that are white)
  - gen_blocks does the following:
    - For every block, with total population size n, use its distribution info from gen_distributions to:
      - Create a "sample" block and a "guessed" block with n records. These blocks are created by assigning categories with probability equal to their distribution in the population. I.e, if block X is 5% women ages 30-35, any given record will have a 5% chance of being a woman age 30-35 (for age, precise number is then randomly generated within this range)
      - Count matches (alignment of age, sex, and race) between the sample and guessed blocks 
