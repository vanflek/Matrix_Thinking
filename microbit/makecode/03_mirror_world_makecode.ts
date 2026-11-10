// One 5 x 5 brightness matrix, stored row by row.
let world: number[] = []

function drawWorld() {
    for (let row = 0; row <= 4; row++) {
        for (let col = 0; col <= 4; col++) {
            led.plotBrightness(col, row, Math.round(world[row * 5 + col] * 255 / 9))
        }
    }
}

function resetWorld() {
    world = [
        9, 0, 0, 0, 0,
        9, 0, 0, 0, 0,
        9, 0, 0, 0, 0,
        9, 9, 9, 9, 0,
        0, 0, 0, 0, 0
    ]
    drawWorld()
}

function mirrorWorld(leftRight: boolean) {
    let nextWorld: number[] = []
    for (let row = 0; row <= 4; row++) {
        for (let col = 0; col <= 4; col++) {
            if (leftRight) {
                nextWorld.push(world[row * 5 + (4 - col)])
            } else {
                nextWorld.push(world[(4 - row) * 5 + col])
            }
        }
    }
    world = nextWorld
    drawWorld()
}

input.onButtonPressed(Button.A, function () {
    mirrorWorld(true)
})
input.onButtonPressed(Button.B, function () {
    mirrorWorld(false)
})
input.onGesture(Gesture.Shake, function () {
    resetWorld()
})
resetWorld()
