# NIST/NRC Corner, Wall, and Cabinet Effects Experiments
The data sets on this page are from large compartment experiments where a natural gas burner was positioned in a corner, against a wall, or inside steel cabinets of various geometries. In the case of the corner and wall, the burner was moved outward in stages until the corner or wall effect became negligible.

The compartment was 11 m long, 7 m wide, and 3.8 m high. The long dimension of the compartment ran east-west. A 1.8 m wide, 2.4 m high door was centered on the east (short) wall. 

## Corner and Wall Effects Experiments
For these experiments, the burner was 60 cm by 60 cm and the burner surface was 54 cm above the floor. The corner fire was located in the southwest corner of the compartment. The wall fire was centered on the south (long) wall. The experiments began with the burner in the corner or against the wall for the first 30 min. At 30 min, the burner was moved so that its edge(s) was 10 cm away from the wall(s). It remained for 15 min, after which it was moved to 20 cm, 30 cm, 50 cm, 100 cm, and 160 cm, each time remaining 15 min for a total experiment time of 2 h.

A three-dimensional array of thermocouples was positioned on a track mounted to the ceiling above the burner. The purpose of this array was to measure maximum plume temperatures at heights of 2.1 m, 2.7 m, and 3.4 m above the floor. As the burner moved, the thermocouple array moved with it. For the corner fire experiments, when the burner was at the 0 cm, 10 cm, and 20 cm positions, the thermocouple array overhead remained at its original location in the corner. As the burner moved beyond 20 cm, the thermocouple array was moved the same amount so that the burner was always below the array in the same position. In other words, for the corner fire experiments, after the center point of the burner reached the point directly below the position 18 on the diagram below, the burner and array moved together, maintaining their relative position.

For each experiment, there are three data files. The first file has a name like `NIST_NRC_Corner_200_kW.csv`, the second has a name like `NIST_NRC_Corner_200_kW_HGL.csv`, and the third `NIST_NRC_Corner_200_kW_Plume.csv`.  

The files of the form, `NIST_NRC_Corner_200_kW.csv`, contain the original thermocouple measurements, time-averaged over 10 s. The key to the column names are as follows:

   * TC-AG-01 through TC-AG-29 are the thermocouples at the top of the cage, 46 cm below the ceiling (see pattern below).

   * TC-BG-01 through TC-BG-29 are the thermocouples at the mid-level of the cage, 107 cm below the ceiling (see pattern below).

   * TC-CG-01 through TC-CG-29 are the thermocouples at the bottom of the cage, 168 cm below the ceiling (see pattern below).

   * TC-WT-01 through TC-WT-13 are the thermocouples of the vertical array called the West Tree. The array was 2.75 m from the west (short) wall and 3.5 m from the south (long) wall. TC-WT-01 was located 2 cm below the ceiling, and the rest were spaced 30 cm apart.

   * TC-ET-01 through TC-ET-13 are the thermocouples of the East Tree. The array was 2.75 m from the east (short) wall and 3.5 m from the south (long) wall. TC-ET-01 was located 2 cm below the ceiling, and the rest were spaced 30 cm apart.

   * TC-C-01 through TC-C-11 are the thermocouples 2 cm from the corner above the corner fire. TC-C-01 was located 2 cm below the ceiling, and the rest were spaced 30 cm apart.

   * TC-W-01 through TC-W-11 are the thermocouples 2 cm from the wall above the wall fire. TC-W-01 was located 2 cm below the ceiling, and the rest were spaced 30 cm apart.

   * HRR (cal) is the heat release rate of the fire as measured using oxygen consumption calorimetry. HRR (NG) is the heat release rate determined from the mass flow rate of natural gas.

![alt text](https://github.com/firemodels/exp/blob/master/NIST_NRC_Corner_Effects/grid.png "TC grid")

The `HGL` files (Hot Gas Layer) contain estimates of the layer height, and upper and lower layer temperatures. These estimates are derived from the West and East TC trees.

The `Plume` files contain time histories of the maximum values of 2 min running averages of the TCs at each of the three levels in the cage above the fire.


## Cabinet Experiments
In these experiments, two different mock steel cabinets were used. Each cabinet was constructed of 12 gauge (2.8 mm or 7/64 in) steel plate with openings as shown below. The large cabinet was nominally 0.9 m by 0.9 m by 2.1 m (3 ft by 3 ft by 7 ft) and the medium size cabinet was 0.6 m by 0.6 m by 2.1 m (2 ft by 2 ft by 7 ft). The primary unit when designing and constructing the cabinets was inches; thus, in the drawings, the dimension given in inches is accurate to 1/16 inches.
![alt text](https://github.com/firemodels/exp/blob/master/NIST_NRC_Corner_Effects/Cabinet_3x3x7.png "Large Cabinet")
![alt text](https://github.com/firemodels/exp/blob/master/NIST_NRC_Corner_Effects/Cabinet_2x2x7.png "Medium Cabinet")

In the first set of experiments (1-6), the large cabinet was positioned with its front opening facing eastward towards the opening of the test compartment. Its left side was 1.8 m (6 ft) from the south wall and its front side was 5.8 m (19 ft 2 in) from the east wall. Two 0.3 m by 0.3 m natural gas burners were placed side by side in the cabinet from the perspective of the cabinet front opening. For the closed door tests, the heat release rate was initially 50 kW for 30 min, then it was increased to 100 kW for 15 min, 200 kW for 15 min, and 400 kW for 15 min. For the open door tests, the heat release rate was initially 200 kW for 15 min, 400 kW for 15 min, 700 kW for 15 min, and 1000 kW for 5 min.

In the second set of experiments (7-10), the medium-sized cabinet was positioned so that its front was the same distance from the east wall as the large cabinet, and its left side was 2.0 m (6.5 ft) from the south wall. A single 30 cm by 30 cm gas burner was centered within. For the closed door tests, the heat release rate was 25 kW, 50 kW, 100 kW, and 200 kW, each for 15 min. For the open door tests, the heat release rate was 40 kW, 80 kW, 200 kW, and 325 kW, each for 15 min.

In the third set of experiments (11-12), the cabinet was removed, and two 30 cm burners were spaced 0.9 m (3 ft) apart, edge to edge, as if separated by the large cabinet. One of the burners was centered under the array of thermocouples. Both burners were 2 m from the south wall. These experiments used the same heat release rate sequence as the open and closed door large cabinet experiments. In these experiments, the plate thermometers were positioned 60 cm from the edge of one of the two burners. Plates 1, 2, 3, 4, 7 and 8 were positioned around the west burner, with similar orientations as they had when the cabinet was present. That is, Plates 1 and 2 faced northward; Plates 3 and 4 faced eastward; Plates 7 and 8 faced southward. Plates 5 and 6 were positioned 60 cm from the edge of the east burner, facing westward.

The data files for these experiments are labelled, `NIST_NRC_Cabinet_Test_n.csv`. These files contain the same measurement positions as the corner and wall experiments, with the following additional measurements: 

   * PT-1 through PT-8 are plate thermometers positioned 0.6 m (2 ft) from each side of the cabinet at heights of 0.8 m (2.5 ft) and 1.4 m (4.5 ft). PT-1 is the upper plate on the left side. PT-2 is lower left. PT-3 is upper back. PT-4 is lower back. PT-5 is upper front. PT-6 is lower front. PT-7 is upper right. PT-8 is lower right. The files labeled `NIST_NRC_Cabinet_Test_n_HF.csv` contain estimates of the heat flux to the plates based on Wickstrom's analysis.

   * STC-1 through STC-6 are sheathed thermocouples within the cabinet, 15 cm (6 in) from the left side, centered. STC-1 is 6 cm (2.5 in) from the top. STC-2 through STC-6 are 30 cm, 60 cm, 90 cm, 120 cm, and 150 cm from the top, respectively.
   
   * TC-Cab is a single 24 gauge Type K thermocouple welded to the center of the back side on the outside of the cabinet.
   
The three dimensional array of thermocouples used in the wall and corner experiments was positioned over the front of the cabinet, such that TC positions 1, 7, 13, 19, and 25 in the diagram shown above were just above the upper front edge of the cabinet.

The hot gas layer (HGL) temperature and height have been calculated from the east and west TC trees, and the results can be found in the files labelled, `NIST_NRC_Cabinet_Test_n_HGL.csv`.

The maximum temperature at each level of the three-tiered thermocouple array can be found in the files labelled, `NIST_NRC_Cabinet_Test_n_Plume.csv`.
   
The test matrix is as follows:

| Test   | Cabinet    | Front Door | Top Vents        | Upper Side Vents                   | HRR (kW)               |
|:------:|:----------:|:----------:|:----------------:|:----------------------------------:|:-----------------------|
|  1     | Large      | Closed     | Closed           | Grill on all four vents            | 50, 100, 200, 400      |
|  2     | Large      | Closed     | All open         | Grill on all four vents            | 50, 100, 200, 400      |
|  3     | Large      | Closed     | Closed           | Front open, all others closed      | 50, 100, 200, 400      |
|  4     | Large      | Closed     | Closed           | Front and back open, others closed | 50, 100, 200, 400      |
|  5     | Large      | Open       | Closed           | Front and back open, others closed | 200, 400, 700, 1000    |
|  6     | Large      | Open       | Open             | All open                           | 200, 400, 700, 1000    |
|  7     | Medium     | Closed     | Closed           | Grill on single front vent         | 25, 50, 100, 200       |
|  8     | Medium     | Closed     | Closed           | Open                               | 25, 50, 100, 200       |
|  9     | Medium     | Open       | Closed           | Open                               | 40, 80, 200, 325       |
|  10    | Medium     | Open       | Closed           | Closed                             | 40, 80, 200, 325       |
|  11    | None       | N/A        | N/A              | N/A                                | 200, 400, 700, 1000    |
|  12    | None       | N/A        | N/A              | N/A                                | 50, 100, 200, 400      |

![alt text](https://github.com/firemodels/exp/blob/master/NIST_NRC_Corner_Effects/grill_drawing.png "Grill Drawing")
