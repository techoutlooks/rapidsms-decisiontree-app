from django.dispatch import Signal


session_end_signal = Signal(providing_args=["session", "cancelled"])
