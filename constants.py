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
  "2,3": "2E",
  "2,7": "2S",
  "2,11": "2S",
  "2,15": "2E",
  "3,2": "2E",
  "3,6": "3S",
  "3,12": "3S",
  "3,16": "2E",
  "4,1": "3S",
  "4,5": "2S",
  "4,9": "3S",
  "4,13": "2S",
  "4,17": "3S",
  "5,0": "3S",
  "5,4": "2S",
  "5,8": "3S",
  "5,10": "3S",
  "5,14": "2S",
  "5,18": "3S",
  "6,3": "3S",
  "6,7": "2S",
  "6,11": "2S",
  "6,15": "3S",
  "7,2": "2S",
  "7,6": "2S",
  "7,12": "2S",
  "7,16": "2S",
  "8,1": "2S",
  "8,5": "3S",
  "8,9": "2S",
  "8,11": "2S",
  "8,13": "3S",
  "8,17": "2S",
  "9,0": "2S",
  "9,4": "3S",
  "9,8": "2E",
  "9,14": "3S",
  "9,18": "2S",
  "10,1": "2S",
  "10,5": "3S",
  "10,8": "2S",
  "10,10": "2S",
  "10,13": "3S",
  "10,17": "2S",
  "11,2": "2S",
  "11,6": "2S",
  "11,12": "2S",
  "11,16": "2S",
  "12,3": "3S",
  "12,7": "2S",
  "12,11": "2S",
  "12,15": "3S",
  "13,0": "3S",
  "13,4": "2S",
  "13,8": "3S",
  "13,10": "3S",
  "13,14": "2S",
  "13,18": "3S",
  "14,1": "3S",
  "14,5": "2S",
  "14,9": "3S",
  "14,13": "2S",
  "14,17": "3S",
  "15,2": "2E",
  "15,6": "3S",
  "15,12": "3S",
  "15,16": "2E",
  "16,3": "2E",
  "16,7": "2S",
  "16,11": "2S",
  "16,15": "2E",
  "17,0": "3E",
  "17,4": "3S",
  "17,8": "2S",
  "17,10": "2S",
  "17,14": "3S",
  "17,18": "3E",
  "18,1": "3E",
  "18,5": "3S",
  "18,9": "2S",
  "18,13": "3S",
  "18,17": "3E",  
}