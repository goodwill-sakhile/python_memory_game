from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.screenmanager import NoTransition
from kivy.lang import Builder
from touch import TouchBox
import _thread as thread
import time
import random
from runnning_time_header_box import TopTimeBox
root = Builder.load_string("""
<BoardBox>:
	md_bg_color:[190/float(255), 190/float(255), 190/float(255), 1]
<MainGameBox>:
	md_bg_color:[230/float(255), 230/float(255), 230/float(255), 1]
	padding:10
	id:main_game_box
	FloatLayout:
		pos:self.parent.pos
		size:self.parent.size
		MDBoxLayout:
			pos:self.parent.pos
			orientation:"vertical"
			TopTimeBox:
				id:top_time_box
			BlocksLayout:
				root:main_game_box
				pos:self.parent.pos
				size:self.parent.size
				spacing:5
				id:grid_layout
				cols:2
				rows:2
				BoardBox:
				BoardBox:
				BoardBox:
				BoardBox:
		MDBoxLayout:
			ScreenManager:
				id:top_layer_screen_manager
				MDScreen:
					name:"empty_screen"
				MDScreen:
					name:"results_screen"
					BoxLayout:
						orientation:"vertical"
						pos:self.parent.pos
						Widget:
						MDBoxLayout:
							size_hint_y:None
							height:"150dp"
							Widget:
							MDBoxLayout:
							    orientation:"vertical"
								size_hint_x:None
								width:"310dp"
								md_bg_color:[220/float(255), 220/float(255), 220/float(255), 1]
								radius:[20, 20, 20, 20]
								Widget:
								MDBoxLayout:
									MDLabel:
										id:result_message_label
										text:"Congratulations you passed the level!"
										text_size:self.size
										halign:"center"
										valign:"middle"
										color:[0, 0, 0, 1]
								Widget:
								MDBoxLayout:
									padding:10
									size_hint_y:None
									height:"50dp"
									Widget:
									ProceedButtonBox:
									    root:main_game_box
									    radius:[20, 20, 20, 20]
										size_hint_x:None
										width:"100dp"
										md_bg_color:[0, 154/float(255), 255/float(255), 1]
										MDLabel:
									    	text:"Ok"
									    	text_size:self.size
									    	halign:"center"
									    	valign:"middle"
									    	color:[1, 1, 1, 1]
							Widget:
						Widget:
""")
class ProceedButtonBox(TouchBox):
	def respondToTouch(self):
		if self.root.ids.grid_layout.error == 3:
			self.root.ids.grid_layout.repeatStage()
		else:
			self.root.ids.grid_layout.playNextStage()
		self.root.ids.top_layer_screen_manager.transition = NoTransition()
		self.root.ids.top_layer_screen_manager.current = "empty_screen"
class BoardBox(TouchBox):
	def __init__(self, **kwargs):
		super(BoardBox, self).__init__(**kwargs)
		self.chosen = False
	def respondToTouch(self):
		grid_layout = self.parent
		if grid_layout.root.selection_open:
			print("Open")
			box_index = self.parent.children.index(self)
			if ((box_index in grid_layout.root.answers) and (not self.chosen)):
				print(box_index, grid_layout.root.answers)
				self.countCorrect(box_index)
			elif (not self.chosen):
				self.countAsError()
	def countCorrect(self, box_index):
		grid_layout = self.parent
		self.md_bg_color = [0, 154/float(255), 255/float(255), 1]
		self.chosen = True
		grid_layout.root.answers.remove(box_index)
		if grid_layout.root.answers == []:
			print("answer are empty")
			grid_layout.root.selection_open = False
			grid_layout.root.ids.result_message_label.text = "Congratulations you passed the level!"
			self.displayPopUpResultBox()
	def countAsError(self):
		grid_layout = self.parent
		grid_layout.error += 1
		print(grid_layout.error)
		grid_layout.list_of_error_box.append(self)
		if grid_layout.error == 3:
			grid_layout.root.selection_open = False
			self.displayAllErrorBox()
			grid_layout.root.ids.result_message_label.text = "Bummer you failed a level!!"
			self.displayPopUpResultBox()
		elif grid_layout.error < 3:
			thread.start_new_thread(self.markAsError, ())
	def displayPopUpResultBox(self):
		grid_layout = self.parent
		grid_layout.root.ids.top_layer_screen_manager.transition = NoTransition()
		grid_layout.root.ids.top_layer_screen_manager.current = "results_screen"
	def displayAllErrorBox(self):
		grid_layout = self.parent
		for box in grid_layout.list_of_error_box:
			box.md_bg_color = [255/float(255), 0, 0, 1]
	def markAsError(self):
		self.md_bg_color = [255/float(255), 20/float(255), 20/float(255), 1]
		time.sleep(float(0.6))
		self.md_bg_color = [190/float(255), 190/float(255), 190/float(255), 1]
class BlocksLayout(MDGridLayout):
	def __init__(self, **kwargs):
		super(BlocksLayout, self).__init__(**kwargs)
		self.error = 0
		self.list_of_error_box = []
	def addBoxes(self): 
		for i in range((self.cols)**2):
			box = BoardBox()
			self.add_widget(box)
	def moveToNextStage(self):
		main_game_box  = self.root
		self.clear_widgets()
		main_game_box.stage += 1
		self.cols = main_game_box.stage + 1
		self.rows = main_game_box.stage + 1
		self.addBoxes()
	def getBoxesNumbersRandomly(self):
		chosen_boxes_numbers = []
		main_game_box  = self.root
		number_of_boxes = ((main_game_box.stage + 1)**2)
		options  = list(range(1, number_of_boxes + 1))
		for i in range((main_game_box.stage + 1)):	
			random.shuffle(options)
			box_number = random.choice(options)
			options.remove(box_number)
			if (box_number - 1) not in chosen_boxes_numbers:
				chosen_boxes_numbers.append(box_number - 1)
		return chosen_boxes_numbers
	def pickBoxes(self, boxes_numbers_list):
		layout_boxes_number = len(self.children)
		for number in boxes_numbers_list:
			box = self.children[number]
			time.sleep(float(0.6))
			box.md_bg_color = [0, 154/float(255), 255/float(255), 1]
			time.sleep(float(0.6))
			box.md_bg_color = [190/float(255), 190/float(255), 190/float(255), 1]
		self.root.selection_open = True
	def playNextStage(self):
		self.error = 0
		self.moveToNextStage()
		boxes_numbers = self.getBoxesNumbersRandomly()
		self.root.answers  = boxes_numbers
		thread.start_new_thread(self.pickBoxes, (boxes_numbers, ))
	def repeatStage(self):
		self.error = 0
		self.clear_widgets()
		self.addBoxes()
		boxes_numbers = self.getBoxesNumbersRandomly()
		self.root.answers  = boxes_numbers
		thread.start_new_thread(self.pickBoxes, (boxes_numbers, ))
class MainGameBox(MDBoxLayout):
	def __init__(self, **kwargs):
		super(MainGameBox, self).__init__(**kwargs)
		self.stage = 1
		self.answers = []
		self.selection_open = False
		self.run_timer = True
	def checkTimer(self):
		while self.run_timer:
			if ((self.ids.top_time_box.minutes == 0) and (self.ids.top_time_box.seconds == 0)):
				print("Time is Up")
				self.run_timer = False
			else:
				pass
class MainApp(MDApp):	
	#memory game app loop object	
	def build(self):
		root = MainGameBox()
		boxes_numbers = root.ids.grid_layout.getBoxesNumbersRandomly()
		print("Boxes: ", boxes_numbers)
		root.answers = boxes_numbers
		thread.start_new_thread(root.ids.grid_layout.pickBoxes, (boxes_numbers, ))
		thread.start_new_thread(root.ids.top_time_box.countDown, ())
		thread.start_new_thread(root.checkTimer, ())
		return root
if __name__  == "__main__":
	MainApp().run()