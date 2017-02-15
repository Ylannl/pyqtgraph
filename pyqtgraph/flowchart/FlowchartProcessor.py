import sys, traceback
from ..Qt import QtCore

class FlowchartProcessor(QtCore.QObject):
	sigFinished = QtCore.Signal()

	def loadNodes(self, nodes):
		self.nodeList = nodes.copy()
		# print("added node to queue", nodes)

	def process(self):
		# print('starting process()', self.nodeList)

		for node in self.nodeList:
			try: 
				node.sigReColor.emit('processing')
				print("processing", node)
				ins = node.inputValues()
				outs = node.process(**ins)
				if not outs is None:
					node.setOutputNoSignal(propagate=True, **outs)
				print("finished processing", node)
				node.clearException()
				node.sigReColor.emit('processed')
			except Exception as e:
				node.setException(sys.exc_info())
				node.sigReColor.emit('exception')
				traceback.print_exc()
		
		self.sigFinished.emit()
		# print (self.nodeQueue)

class FlowchartProcessorController(object):
	def __init__(self):
		self.queue = []
		self.isProcessing = False
		
	def finishUpdate(self):
		# if self.queue:
		# 	self.run()
		# else:
		self.isProcessing = False

	def addNodes(self, nodes):
		if self.isProcessing:
			return
		else:
			self.queue.append(nodes)
			self.run()

	def run(self):
		self.updateThread = QtCore.QThread()
		self.fp = FlowchartProcessor()
		self.fp.moveToThread(self.updateThread)
		self.updateThread.started.connect(self.fp.process)
		self.fp.sigFinished.connect(self.finishUpdate)
		self.fp.sigFinished.connect(self.updateThread.quit)
		self.fp.sigFinished.connect(self.fp.deleteLater)
		self.updateThread.finished.connect(self.updateThread.deleteLater)

		self.fp.loadNodes(self.queue.pop(0))
		self.updateThread.start()
		self.isProcessing = True

        