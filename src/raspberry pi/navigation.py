class Navigator:

    def __init__(self):

        self.frame_width = 640

        self.center_x = self.frame_width // 2

        self.dead_zone = 80

        self.state = "DRIVE"

    def calculate(self, vision_result):

        red = vision_result["red"]
        green = vision_result["green"]

        # ==================================
        # NO TRAFFIC PILLAR
        # ==================================

        if red is None and green is None:

            self.state = "DRIVE"

            return {
                "drive": "F",
                "steering": "C",
                "state": self.state
            }

        # ==================================
        # BOTH COLORS DETECTED
        # ==================================

        if red is not None and green is not None:

            # use the apparently closer / larger object
            if red["area"] > green["area"]:

                color = "RED"
                target = red

            else:

                color = "GREEN"
                target = green

        elif red is not None:

            color = "RED"
            target = red

        else:

            color = "GREEN"
            target = green

        object_x = target["center_x"]

        # ==================================
        # RED
        # PASS RIGHT
        # ==================================

        if color == "RED":

            self.state = "RED_PILLAR"

            # Move vehicle toward right side
            steering = "R"

        # ==================================
        # GREEN
        # PASS LEFT
        # ==================================

        else:

            self.state = "GREEN_PILLAR"

            # Move vehicle toward left side
            steering = "L"

        return {
            "drive": "F",
            "steering": steering,
            "state": self.state,
            "object_x": object_x,
            "color": color
        }