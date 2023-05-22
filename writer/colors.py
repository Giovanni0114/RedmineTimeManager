COLORS = {
    "purple":	    "#c071f5",
    "pink":	        "#ff00ee",
    "orange":		"#d99011",
    "green":		"#25ba14",
    "red":			"#ff4242",
    "light_blue":	"#6bb0c9",
    "blue":			"#2070b2",
    "white":		"#ffffff"
}

def get_color(color: str) -> str:
    if '_' not in color: 
        return COLORS.get(color)
    return f"bold {color.split('_')[1]}"

