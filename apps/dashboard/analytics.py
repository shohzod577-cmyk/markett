"""
Compatibility shim: expose `DashboardAnalytics` from the misspelled module.
This preserves the existing implementation in `analiytics.py` while making
`from .analytics import DashboardAnalytics` work.
"""

from .analiytics import DashboardAnalytics
