from PyQt5.QtCore import QObject, Signal
import sys, traceback

class FlowchartProcessor(QObject):

	sigFinished = Signal()

	def setNodeList(self, nodeList):
		self.nodeList = nodeList

	def process(self):
		print(self.nodeList)
		try: 
			for node in self.nodeList:
				print("processing", node)
				ins = node.inputValues()
				outs = node.process(**ins)
				if not outs is None:
					node.setOutputNoSignal(propagate=True, **outs)
				print("finished processing", node)
		except Exception as e:
			print(node, e)
			traceback.print_tb(sys.exc_info()[-1])
		finally:
			self.sigFinished.emit()
