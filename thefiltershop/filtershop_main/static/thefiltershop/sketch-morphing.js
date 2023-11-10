let numbersMatrix = [
  1 + 2 + 4 + 16 + 32 + 64, 4 + 32, 1 + 4 + 8 + 16 + 64, 1 + 4 + 8 + 32 + 64, // 0, 1, 2, 3
  2 + 4 + 8 + 32, 1 + 2 + 8 + 32 + 64, 1 + 2 + 8 + 16 + 32 + 64, // 4, 5, 6
  1 + 4 + 32, 1 + 2 + 4 + 8 + 16 + 32 + 64, 1 + 2 + 4 + 8 + 32 + 64 // 7, 8, 9
];

let posX = []; // Array to store X coordinates of the points
let posY = []; // Array to store Y coordinates of the points
let posZ = []; // Array to store Z coordinates of the points
let colR = []; // Array to store red color values for the points
let colG = []; // Array to store green color values for the points
let colB = []; // Array to store blue color values for the points
let rotX = []; // Rotation on the X axe

let posXBis = []; // Array to store X coordinates of the points
let posYBis = []; // Array to store Y coordinates of the points
let posZBis = []; // Array to store Z coordinates of the points
let colRBis = []; // Array to store red color values for the points
let colGBis = []; // Array to store green color values for the points
let colBBis = []; // Array to store blue color values for the points
let rotXBis = []; // Rotation on the X axe

let typeOfElement = []; // Type of element to draw (or not)
let iPosInPool = 0;

let nb1 = 0;
let nb2 = 0;
let nb3 = 0;

let iFrame = 0

let transparence = 20;

function setup() {
  ourCanva = createCanvas(250, 200);
  ourCanva.center('horizontal');
  setSegments(0, 2, 100, 400, 200, 200);
  setSegments(0, 4, 100, 400, 200, 200);
  setSegments(0, 6, 100, 400, 200, 200);
}

function draw() {
  // Your draw code here
  background(214,245,247,transparence);
  // Call the method to draw points with squares
  drawPointsWithSquares();

  transparence+=0.1;

  if (transparence > 255)
  {
    transparence = 255;
  }

  let changeNeeded = false

  if (!isInTransition) {
    iFrame = 0;
    if (nb1 != 4) {
      nb1 = floor(random(10))
      changeNeeded = true
    }
    if (nb2 != 0) {
      nb2 = floor(random(10))
      changeNeeded = true
    }
    if (nb3 != 4) {
      nb3 = floor(random(10))
      changeNeeded = true
    }
    if (changeNeeded) {
      currentStep = 0;

      // Does a snapshot of the current position, and tell the update loop to transition from these positions 
      // to the normal one (set just after)
      prepareTransition(30);

      iPosInPool = 0; // Start again from 0

      // As we will morph, they will be the target of the update morphing.
      setSegments(nb1, 2, 100, 400, 400, 200)
      setSegments(nb2, 4, 100, 400, 400, 200)
      setSegments(nb3, 6, 100, 400, 400, 200)
    }
  }
}

function drawPointsWithSquares() {
  if (isInTransition) {
    // From bis to normal
    for (let iDraw = 0; iDraw < iPosInPool; ++iDraw) {
      {
        let r = colR[iDraw] * 255; // Scale color values to 0-255

        let x = currentStep * posX[iDraw] + (1 - currentStep) * posXBis[iDraw];
        let y = currentStep * posY[iDraw] + (1 - currentStep) * posYBis[iDraw];
        let z = currentStep * posZ[iDraw] + (1 - currentStep) * posZBis[iDraw];
        let r2 = colR[iDraw] * 255; // Scale color values to 0-255
        let g = colG[iDraw] * 255;
        let b = colB[iDraw] * 255;
        fill(r2, g, b);
        noStroke();
        square(x, y, 5); // Adjust the size of the square as needed
      }
    }

    currentStep += transitionSteps;
    if (currentStep >= 1) {
      // Done
      isInTransition = false;
    }

  }
  else {
    for (let i = 0; i < iPosInPool; i++) {
      let x = posX[i];
      let y = posY[i];
      let z = posZ[i];
      let r = colR[i] * 255; // Scale color values to 0-255
      let g = colG[i] * 255;
      let b = colB[i] * 255;

      fill(r, g, b);
      noStroke();
      square(x, y, 5); // Adjust the size of the square as needed
    }
  }
}

let maxPoints = 0

function setSegments(number, relPosition, nbOfPointsPerSegment, size, relPosY, segPosZ) {

  maxPoints = nbOfPointsPerSegment * 7
  // Segments
  //   _
  //  | |
  //   -
  //  | |
  //   -

  // We always show all segments, but not with the same color and depth

  // 1
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {
    if ((numbersMatrix[number] & 1) !== 0) {
      posX[iPosInPool] = 1 + relPosition * (nbOfPointsPerSegment + 8) + iPoint;
      posY[iPosInPool] = - (nbOfPointsPerSegment + 1) + relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }

  // 2 left up |
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {


    if ((numbersMatrix[number] & 2) !== 0) {
      posX[iPosInPool] = relPosition * (nbOfPointsPerSegment + 8);
      posY[iPosInPool] = -(1 + iPoint) + relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }

  // 4 left up |
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {
    if ((numbersMatrix[number] & 4) !== 0) {
      posX[iPosInPool] = nbOfPointsPerSegment + 1 + relPosition * (nbOfPointsPerSegment + 8);
      posY[iPosInPool] = -(1 + iPoint) + relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }

  // 8, central -
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {

    if ((numbersMatrix[number] & 8) !== 0) {
      posX[iPosInPool] = 1 + relPosition * (nbOfPointsPerSegment + 8) + iPoint;
      posY[iPosInPool] = relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }

  // 16, left bottom |
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {


    if ((numbersMatrix[number] & 16) !== 0) {
      posX[iPosInPool] = relPosition * (nbOfPointsPerSegment + 8);
      posY[iPosInPool] = 1 + iPoint + relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }

  // 32, right bottom |
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {
    if ((numbersMatrix[number] & 32) !== 0) {
      posX[iPosInPool] = nbOfPointsPerSegment + 1 + relPosition * (nbOfPointsPerSegment + 8);
      posY[iPosInPool] = 1 + iPoint + relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }

  // 64, bottom -
  for (let iPoint = 0; iPoint < nbOfPointsPerSegment; iPoint++) {

    if ((numbersMatrix[number] & 64) !== 0) {
      posX[iPosInPool] = 1 + relPosition * (nbOfPointsPerSegment + 8) + iPoint;
      posY[iPosInPool] = nbOfPointsPerSegment + 1 + relPosY;

      posX[iPosInPool] *= 0.25;
      posY[iPosInPool] *= 0.25;

      posZ[iPosInPool] = segPosZ;

      typeOfElement[iPosInPool] = 1;
      colR[iPosInPool] = 0;
      colG[iPosInPool] = 0;
      colB[iPosInPool] = 1;
      rotX[iPosInPool] = 0;

      iPosInPool++;
    }
  }
}

let isInTransition = false;
let transitionSteps = 10;
let currentStep = 0;
let maxTransitionSteps = 10;

function prepareTransition(nbOfSteps) {
  for (let iElements = 0; iElements < iPosInPool; iElements++) {
    posXBis[iElements] = posX[iElements];
    posYBis[iElements] = posY[iElements];
    posZBis[iElements] = posZ[iElements];

    colRBis[iElements] = colR[iElements];
    colGBis[iElements] = colG[iElements];
    colBBis[iElements] = colB[iElements];

    rotXBis[iElements] = rotX[iElements];
  }
  // If we have more origin points that taget points, we still need to save them
  if (iPosInPool < maxPoints) {
    for (let iElements = iPosInPool; iElements < maxPoints; iElements++) {
      posXBis[iElements] = 100;
      posYBis[iElements] = 100;
      posZBis[iElements] = 100;

      colRBis[iElements] = 0;
      colGBis[iElements] = 0;
      colBBis[iElements] = 0;

      rotXBis[iElements] = 0;
    }
  }
  isInTransition = true;

  maxTransitionSteps = nbOfSteps;
  transitionSteps = 1 / maxTransitionSteps;
  currentStep = 0;
}