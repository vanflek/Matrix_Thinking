// The five strings are rows of ONE world, not five animation frames.
let world = ["09000", "09900", "00000", "00000", "00000"]

function drawWorld() {
    // This loop only displays the state. It does not move individual lights.
    for (let row = 0; row <= 4; row++) {
        for (let col = 0; col <= 4; col++) {
            if (world[row].charAt(col) == "9") {
                led.plot(col, row)
            } else {
                led.unplot(col, row)
            }
        }
    }
}

input.onButtonPressed(Button.A, function () {
    // Read every source row from the old world, then replace the whole array.
    world = ["00000", world[0], world[1], world[2], world[3]]
    drawWorld()
})

input.onButtonPressed(Button.B, function () {
    world = ["09000", "09900", "00000", "00000", "00000"]
    drawWorld()
})

drawWorld()
