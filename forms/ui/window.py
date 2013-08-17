
class SurfaceDetailWindow:

	def __init__(self):
		
		self.window  = 'forms_optionsWindow'
		self.title   = 'FORMS :: Options Window'
		self.helpURL = 'https://github.com/davidpaulrosser/Forms'
		self.size    = (500, 400)
		self.supportsToolAction = False
		self.actionName = 'Apply and Close'

	def create(self):
		
		if pm.window(self.window, exists = True):
			pm.deleteUI(self.window, window = True)
		
		self.window = pm.window(
			self.window,
			title = self.title,
			widthHeight = self.size,
			menuBar = True
		)
		self.mainForm = pm.formLayout(numberOfDivisions = 100)
		self.commonMenu()
		self.commonButtons()
		self.optionsBorder = pm.tabLayout(
			scrollable = True, 
			tabsVisible = False, 
			height = 1
		)
		pm.formLayout(
			self.mainForm,
			edit = True,
			attachForm = (
				[self.optionsBorder, 'top', 0],
				[self.optionsBorder, 'left', 2],
				[self.optionsBorder, 'right', 2]
			),
			attachControl = (
				[self.optionsBorder, 'bottom', 5, self.applyButton]
			)
		)
		self.optionsForm = pm.formLayout(numberOfDivisions = 100)
		self.displayOptions()
		pm.showWindow()

	def commonMenu(self):
		self.editMenu = pm.menu(label = 'Edit')
		self.editMenuSave = pm.menuItem(
			label = 'Save Settings',
			command = self.editMenuSaveCommand
		)
		self.editMenuReset = pm.menuItem(
			label = 'Reset Settings',
			command = self.editMenuResetCommand
		)
		self.editMenuDiv = pm.menuItem(d = True)
		self.editMenuRadio = pm.radioMenuItemCollection()
		self.editMenuTool = pm.menuItem(
			label = 'Tool',
			radioButton = True,
			enable = self.supportsToolAction,
			command = self.editMenuToolCommand
		)
		self.editMenuAction = pm.menuItem(
			label = 'Tool Action',
			radioButton = True,
			enable = self.supportsToolAction,
			command = self.editMenuActionCommand
		)
		self.helpMenu = pm.menu(label = 'Help')
		self.helpMenuItem = pm.menuItem(
			label = 'Help on %s' % self.title,
			command = self.helpMenuCommand
		)

	def helpMenuCommand(self, *args):
		pm.launch(web = self.helpURL)

	def editMenuSaveCommand(self, *args): pass
	def editMenuResetCommand(self, *args): pass
	def editMenuToolCommand(self, *args): pass
	def editMenuActionCommand(self, *args): pass

	def commonButtons(self):
		self.commonButtonSize = ((self.size[0]-18)/3, 26)
		self.actionButton = pm.button(
			label = self.actionName,
			height = self.commonButtonSize[1],
			command = self.actionButtonCommand
		)
		self.applyButton = pm.button(
			label = 'Apply',
			height = self.commonButtonSize[1],
			command = self.actionButtonCommand
		)
		self.closeButton = pm.button(
			label = 'Close',
			height = self.commonButtonSize[1],
			command = self.closeButtonCommand
		)
		pm.formLayout(
			self.mainForm,
			edit = True,
			attachForm = (
				[self.actionButton, 'left', 5],
				[self.actionButton, 'bottom', 5],
				[self.applyButton, 'bottom', 5],
				[self.closeButton, 'bottom', 5],
				[self.closeButton, 'right', 5]
			),
			attachPosition = (
				[self.actionButton, 'right', 1, 33],
				[self.closeButton, 'left', 0, 67]
			),
			attachControl = (
				[self.applyButton, 'left', 4, self.actionButton],
				[self.applyButton, 'right', 4, self.closeButton]
			),
			attachNone = (
				[self.actionButton, 'top'],
				[self.applyButton, 'top'],
				[self.closeButton, 'top']
			)
		)

	
	def actionButtonCommand(self, *args):
		self.createButtonCommand()
		self.closeButtonCommand()

	def createButtonCommand(self, *args): pass
	def closeButtonCommand(self, *args):
		pm.deleteUI(self.window, window = True)

	def displayOptions(self): pass
