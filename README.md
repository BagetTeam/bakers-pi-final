# RoboDelivery
A robot that delivers packages to rooms automatically! It traverses the map, looks through rooms without meetings (red pads) and finds the package landing pad (green pad) where the package is going to be delivered at. After a succesful delivery, it returns back to the mail room (blue room), and celebrates.

Cool sound effects added to the robot to give a nice ambiance when the robot is traveling and delivering packages, including a superb audio for when it finishes its job.

## How it works
The robot is built using LEGOs and is embedded with a BrickPi (Raspberry Pi add-on board for LEGO) to perform commands.
It contains multiple subsystems, including the Navigation, Room Search, Delivery and Sound systems.

### Navigation
Uses a Line tracking algorithm to closely follow the line without diverging outside the track using a colour sensor. Contains some waypoint logic to skip over unwanted intersections.

### Room Search
Utilizes both the colour sensor and a gyro sensor for sweeping the room, looking for the package landing pad, while making sure to stay properly aligned.

### Delivery
Uses a piston like component, powered with a motor, to push out the package. Packages and stacked one on top of each other, making sure that we push one at a time while having the next package ready simply by retrieving the arm of the piston.

### Sound
Cool sounds with an integrated speaker.

# Demo
[![Demo](https://img.youtube.com/vi/plpx3dQ-prg/0.jpg)](https://youtu.be/plpx3dQ-prg)


# Built by the Bakers' PI team
