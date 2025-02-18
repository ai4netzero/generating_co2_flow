#!/bin/bash

###### USERS INPUT ############################################################

## Define the total number of iterations of the simulation and how often to output
TotalTime=1.0
WriteTimestep=0.01
runTimestep=1.2e-5 

#### END OF USER INPUT #######################################################

nsatpoints=$(expr $TotalTime/$WriteTimestep | bc)

cp system/fvSolutionTP system/fvSolution
cp system/fvSchemesTP system/fvSchemes
cp system/controlDictTP system/controlDict
cp system/postProcessDictRun system/postProcessDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTimestep/$WriteTimestep/g" system/controlDict
sed -i "s/runTimestep/$runTimestep/g" system/controlDict
sed -i "s/nsatpoints/$nsatpoints/g" system/postProcessDict

if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    echo -e "Run interGCFoam in parallel on $NP processors"
    mpiexec -np $NP interGCFoam  -parallel > interGCFoamTP.out
else
    echo -e "Run interGCFoam"
    interGCFoam > interGCFoamTP.out
fi


