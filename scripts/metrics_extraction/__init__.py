"""
Metrics Extraction Package

Módulos para extração de métricas léxicas e sintáticas.
"""

from .basic_metrics import BasicMetrics
from .syntactic_metrics import SyntacticMetrics
from .windowed_analysis import WindowedAnalysis, validate_text_for_windowed_analysis

__all__ = [
    'BasicMetrics',
    'SyntacticMetrics',
    'WindowedAnalysis',
    'validate_text_for_windowed_analysis'
]

__version__ = '1.0.0'
