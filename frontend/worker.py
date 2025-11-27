from PySide6.QtCore import QObject, Signal, QRunnable, Slot
import traceback


class WorkerSignals(QObject):
    """Signals available from a running worker thread."""
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    """QRunnable wrapper to run a function in a thread pool and emit signals."""

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            self.signals.error.emit((e, tb))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
