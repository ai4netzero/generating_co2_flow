#!/bin/bash

./_1createMesh.sh
./_2runSnappyHexMesh.sh
./_3initCaseSPFlow.sh
./_4runCaseSPFlow.sh
./_5processSPFlow.sh
./_6initCaseTPFlow.sh
./_7runCaseTPFlow.sh
./_8processTPFlow.sh

reconstructPar > reconstructPar.out
processMeshCellCenters > processMeshCellCenters.out
