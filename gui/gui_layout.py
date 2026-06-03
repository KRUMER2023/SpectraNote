
class Layout:

    def __init__(self):

        self.measurements = self.compute_layout()

        s = self.measurements["scale"]

        self.positions = {
            
            "Toogler":
            {   
                "button":
                {
                    # toggle buttons
                    "toggle_left":  (393*s, 20*s),
                    "toggle_right": (476*s, 20*s)
                },
                
                "bg":
                {
                    "main_bg" : (1,1),
                    "icon":     (1,1) 
                }
            },

            "Right_panel":
            { 
                "button":
                {
                    # right panel
                    "exit":     (835*s, 12*s),
                    "bullet":   (781*s, 12*s),
                    "h2":       (727*s, 12*s),
                    "h1":       (673*s, 12*s),
                    "bold":     (619*s, 12*s),
                    "italic":   (565*s, 12*s),
                    "normal":   (511*s, 12*s)
                },
                
                "bg":
                {
                    # right panel bg
                    "right_bg_bg" : (667, 1),
                    "right_line_bg" : (694, 1)
                }
            },

            "Left_panel":
            { 
                
                "button":
                {
                    # left panel
                    "folder":     ( 15*s, 12*s),
                    "file":       ( 69*s, 12*s),
                    "chatbot":    (123*s, 12*s),
                    "summary":    (177*s, 12*s),
                    "translator": (231*s, 12*s),
                    "snapshot":     (285*s, 12*s),
                    "youtube":    (339*s, 12*s)
                },
                
                "bg":
                {
                    # left panel bg
                    "left_bg_bg" : (224, 1),
                    "left_line_bg" : (198, 1)
                }
            }

            
        }

    def compute_layout(self):
        from screeninfo import get_monitors
        
        m = get_monitors()
        SW = m[0].width
        SH =m[0].height
        # print(SW,SH)

        BASE_W = 892
        BASE_H = 70

        scale = 1.0
        if SW < BASE_W:
            scale = SW / BASE_W
            self.width = int(BASE_W * scale)
            self.height = int(BASE_H * scale)
            print(f"[INFO] Screen width {SW} < {BASE_W}; scaling UI by {scale:.2f}")
        else:
            self.width = BASE_W
            self.height = BASE_H

        return {
            "screen_w": SW,
            "screen_h": SH,
            "width": self.width,
            "height": self.height,
            "base_width" : BASE_W,
            "base_height" : BASE_H,
            "scale": scale
        }

    