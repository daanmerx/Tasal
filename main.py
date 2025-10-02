import arduino_runnen as AR
import Camera_controlling as C

# Map waar foto's opgeslagen worden
save_path = r"C:\Users\20223560\Documents\microscopy\MicroscopyVENV\photos_microscope"

# Start sequence met foto na elke move
AR.run_sequence(after_move=lambda: C.take_photo(save_path))

# Sluit Arduino
AR.close()