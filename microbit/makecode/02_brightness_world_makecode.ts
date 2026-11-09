// One logical 5 x 5 brightness matrix, stored row by row.
let world: number[] = []

function drawWorld() {
    for (let row = 0; row <= 4; row++) {
        for (let col = 0; col <= 4; col++) {
            // Data uses 0..9; MakeCode LEDs use 0..255.
            led.plotBrightness(col, row, Math.round(world[row * 5 + col] * 255 / 9))
        }
    }
}

function resetWorld() {
    world = [
        0, 1, 2, 3, 4,
        1, 2, 3, 4, 5,
        2, 3, 4, 5, 6,
        3, 4, 5, 6, 7,
        4, 5, 6, 7, 8
    ]
    drawWorld()
}

function changeBrightness(amount: number) {
    let nextWorld: number[] = []
    for (let brightness of world) {
        nextWorld.push(Math.max(0, Math.min(9, brightness + amount)))
    }
    world = nextWorld
    drawWorld()
}

input.onButtonPressed(Button.A, function () {
    changeBrightness(-1)
})

input.onButtonPressed(Button.B, function () {
    changeBrightness(1)
})

input.onGesture(Gesture.Shake, function () {
    resetWorld()
})

resetWorld()
