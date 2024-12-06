class Settings:
    """Class to store all settings for the Minesweeper application"""
    
    def __init__(self):
        self.screen_width=900
        self.screen_height=1250

        self.bomb_count=98
        self.grid_columns=16
        self.grid_rows=30
        self.grid_count=self.grid_columns*self.grid_rows

        self.color='gray'
        self.grid_bg_color='gray'
        self.grid_height=self.screen_height-150
        self.grid_width=self.screen_width-100

        self.cell_width=(self.grid_width/self.grid_columns)
        self.cell_height=(self.grid_height/self.grid_rows)
        self.cell_gap_offset=2
        self.cell_color = "#C0C0C0"
        self.cell_light_color = "#FFFFFF"
        self.cell_dark_color = "#808080"
        self.cell_font_size = 38

        self.counter_bg_color='black'
        self.counter_font_color='red'
        self.counter_width=100
        self.counter_height=50
        self.counter_font_size=45

        self.dialog_width = 600
        self.dialog_height = 200
        self.dialog_button_width = 200
        self.dialog_button_height = 75
        self.dialog_color = "#989898"
        self.dialog_button_color = "#B0B0B0"
        self.dialog_font_size = 60
        self.dialog_button_font_size = 30