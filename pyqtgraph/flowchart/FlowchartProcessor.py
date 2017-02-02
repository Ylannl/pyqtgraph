from PyQt5.QtCore import QObject, Signal
import sys, traceback

class FlowchartProcessor(QObject):

	sigFinished = Signal()

	def setNodeList(self, nodeList):
		self.nodeList = nodeList

	def process(self):
		print(self.nodeList)
		
		for node in self.nodeList:
			try: 
				print("processing", node)
				ins = node.inputValues()
				outs = node.process(**ins)
				if not outs is None:
					node.setOutputNoSignal(propagate=True, **outs)
				print("finished processing", node)
			except Exception as e:
				node.setException(sys.exc_info())
		
		self.sigFinished.emit()
