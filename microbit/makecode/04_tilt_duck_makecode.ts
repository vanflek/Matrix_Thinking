// One unchanged duck matrix. Each tilt chooses how to read its rows and columns.
let initialWorld = [
    0, 0, 0, 9, 0,
    0, 0, 9, 9, 9,
    9, 9, 9, 9, 0,
    0, 9, 9, 9, 0,
    0, 0, 9, 0, 0
]
let world: number[] = []
let leftRight = false
let topBottom = false

function drawWorld() {
    for (let row = 0; row <= 4; row++) {
        for (let col = 0; col <= 4; col++) {
            led.plotBrightness(col, row, Math.round(world[row * 5 + col] * 255 / 9))
        }
    }
}

function reflectWorld() {
    let nextWorld: number[] = []
    for (let row = 0; row <= 4; row++) {
        for (let col = 0; col <= 4; col++) {
            let sourceRow = row
            let sourceCol = col
            if (topBottom) {
                sourceRow = 4 - row
            }
            if (leftRight) {
                sourceCol = 4 - col
            }
            nextWorld.push(initialWorld[sourceRow * 5 + sourceCol])
        }
    }
    world = nextWorld
    drawWorld()
}

function resetWorld() {
    leftRight = false
    topBottom = false
    reflectWorld()
}

function updateTilt() {
    let previousLeft = leftRight
    let previousTop = topBottom
    let x = input.acceleration(Dimension.X)
    let y = input.acceleration(Dimension.Y)
    if (x < -300) {
        leftRight = true
    } else if (x > 300) {
        leftRight = false
    }
    if (y < -300) {
        topBottom = true
    } else if (y > 300) {
        topBottom = false
    }
    if (previousLeft != leftRight || previousTop != topBottom) {
        reflectWorld()
    }
}

input.onGesture(Gesture.Shake, function () {
    resetWorld()
    basic.pause(300)
})
resetWorld()
basic.forever(function () {
    updateTilt()
    basic.pause(40)
})
