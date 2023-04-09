from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
import time
import _thread as thread
root = Builder.load_string("""
<TopTimeBox>:
	size_hint_y:None
	height:"80dp"
	md_bg_color:220/float(255), 220/float(255), 220/float(255), 1
	MDLabel:
		id:time_label
		text:"10:00"
		text_size:self.size
		halign:"center"
		valign:"middle"
		font_size:"30dp"
""")
class TopTimeBox(MDBoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.minutes = 10
		self.seconds = 60
	def countDown(self):
		while (self.minutes >= 0):
			if self.seconds == 0 and self.minutes > 0:
				self.seconds = 59
				self.minutes = self.minutes - 1
			elif self.seconds > 0:
				self.seconds = self.seconds - 1
			if self.seconds < 10:
				self.ids.time_label.text = str(self.minutes) + ":0"+ str(self.seconds)
			else:
				self.ids.time_label.text = str(self.minutes) + ":"+ str(self.seconds)
			time.sleep(1)