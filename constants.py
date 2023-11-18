class Orientation:
  HORIZONTAL = "horizontal"
  VERTICAL = "vertical"

TILES = {
  "+": {
    "frequency": 11,
    "points": 1,
    "type": "operator"
  },
  "-": {
    "frequency": 11,
    "points": 2,
    "type": "negative"
  },
  "×": {
    "frequency": 11,
    "points": 3,
    "type": "operator"
  },
  "÷": {
    "frequency": 11,
    "points": 5,
    "type": "operator"
  },
  "0": {
    "frequency": 3,
    "points": 1,
    "type": "integer"
  },
  "1": {
    "frequency": 3,
    "points": 1,
    "type": "integer"
  },
  "2": {
    "frequency": 9,
    "points": 1,
    "type": "integer"
  },
  "3": {
    "frequency": 9,
    "points": 1,
    "type": "integer"
  },
  "4": {
    "frequency": 9,
    "points": 1,
    "type": "integer"
  },
  "5": {
    "frequency": 9,
    "points": 1,
    "type": "integer"
  },
  "6": {
    "frequency": 9,
    "points": 2,
    "type": "integer"
  },
  "7": {
    "frequency": 9,
    "points": 2,
    "type": "integer"
  },
  "8": {
    "frequency": 9,
    "points": 2,
    "type": "integer"
  },
  "9": {
    "frequency": 9,
    "points": 2,
    "type": "integer"
  },
  "1/2": {
    "frequency": 4,
    "points": 2,
    "type": "fraction"
  },
  "2/2": {
    "frequency": 1,
    "points": 2,
    "type": "fraction"
  },
  "5/2": {
    "frequency": 1,
    "points": 5,
    "type": "fraction"
  },
  "1/3": {
    "frequency": 2,
    "points": 8,
    "type": "fraction"
  },
  "2/3": {
    "frequency": 2,
    "points": 8,
    "type": "fraction"
  },
  "3/3": {
    "frequency": 1,
    "points": 2,
    "type": "fraction"
  },
  "1/4": {
    "frequency": 2,
    "points": 6,
    "type": "fraction"
  },
  "2/4": {
    "frequency": 2,
    "points": 5,
    "type": "fraction"
  },
  "3/4": {
    "frequency": 2,
    "points": 6,
    "type": "fraction"
  },
  "4/4": {
    "frequency": 1,
    "points": 2,
    "type": "fraction"
  },
  "7/4": {
    "frequency": 1,
    "points": 7,
    "type": "fraction"
  },
  "1/6": {
    "frequency": 1,
    "points": 10,
    "type": "fraction"
  },
  "2/6": {
    "frequency": 1,
    "points": 9,
    "type": "fraction"
  },
  "3/6": {
    "frequency": 1,
    "points": 5,
    "type": "fraction"
  },
  "4/6": {
    "frequency": 1,
    "points": 9,
    "type": "fraction"
  },
  "5/6": {
    "frequency": 1,
    "points": 12,
    "type": "fraction"
  },
  "6/6": {
    "frequency": 1,
    "points": 2,
    "type": "fraction"
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