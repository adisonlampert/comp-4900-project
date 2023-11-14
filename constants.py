class Orientation:
  HORIZONTAL = "horizontal"
  VERTICAL = "vertical"

TILES = {
  "+": {
    "frequency": 11,
    "points": 1
  },
  "-": {
    "frequency": 11,
    "points": 2
  },
  "×": {
    "frequency": 11,
    "points": 3
  },
  "÷": {
    "frequency": 11,
    "points": 5
  },
  "0": {
    "frequency": 3,
    "points": 1
  },
  "1": {
    "frequency": 3,
    "points": 1
  },
  "2": {
    "frequency": 9,
    "points": 1
  },
  "3": {
    "frequency": 9,
    "points": 1
  },
  "4": {
    "frequency": 9,
    "points": 1
  },
  "5": {
    "frequency": 9,
    "points": 1
  },
  "6": {
    "frequency": 9,
    "points": 2
  },
  "7": {
    "frequency": 9,
    "points": 2
  },
  "8": {
    "frequency": 9,
    "points": 2
  },
  "9": {
    "frequency": 9,
    "points": 2
  },
  "1/2": {
    "frequency": 4,
    "points": 2
  },
  "2/2": {
    "frequency": 1,
    "points": 2
  },
  "5/2": {
    "frequency": 1,
    "points": 5
  },
  "1/3": {
    "frequency": 2,
    "points": 8
  },
  "2/3": {
    "frequency": 2,
    "points": 8
  },
  "3/3": {
    "frequency": 1,
    "points": 2
  },
  "1/4": {
    "frequency": 2,
    "points": 6
  },
  "2/4": {
    "frequency": 2,
    "points": 5
  },
  "3/4": {
    "frequency": 2,
    "points": 6
  },
  "4/4": {
    "frequency": 1,
    "points": 2
  },
  "7/4": {
    "frequency": 1,
    "points": 7
  },
  "1/6": {
    "frequency": 1,
    "points": 10
  },
  "2/6": {
    "frequency": 1,
    "points": 9
  },
  "3/6": {
    "frequency": 1,
    "points": 5
  },
  "4/6": {
    "frequency": 1,
    "points": 9
  },
  "5/6": {
    "frequency": 1,
    "points": 12
  },
  "6/6": {
    "frequency": 1,
    "points": 2
  },
}

MULTIPLIERS = {
  "0,1": "3E",
  "0,5": "3S",
  "0,9": "2S",
  "0,13": "3S",
  "0,17": "3E",
  "1,0": "3E",
  "1,4": "3S",
  "1,8": "2S",
  "1,10": "2S",
  "1,14": "3S",
  "1,18": "3E",
  "2,3": ""
}