from warnings import warn

import pandas as pd

from ..utils import make_iterable, order_as_data_mapping
from ..exceptions import PlotnineWarning
from ..doctools import document
from ..mapping import aes
from .geom import geom
from .geom_segment import geom_segment


@document
class geom_hline(geom):
    """
    Horizontal line

    {usage}

    Parameters
    ----------
    {common_parameters}
    """
    DEFAULT_AES = {'color': 'black', 'linetype': 'solid',
                   'size': 0.5, 'alpha': 1}
    REQUIRED_AES = {'yintercept'}
    DEFAULT_PARAMS = {'stat': 'identity', 'position': 'identity',
                      'na_rm': False, 'inherit_aes': False}
    legend_geom = 'path'

    def __init__(self, data=None, mapping=None, **kwargs):
        data, mapping = order_as_data_mapping(data, mapping)
        yintercept = kwargs.pop('yintercept', None)
        if yintercept is not None:
            if mapping:
                warn("The 'yintercept' parameter has overridden "
                     "the aes() mapping.", PlotnineWarning)
            data = pd.DataFrame({'yintercept': make_iterable(yintercept)})
            mapping = aes(yintercept='yintercept')
            kwargs['show_legend'] = False

        geom.__init__(self, data, mapping, **kwargs)

    def draw_panel(self, data, panel_params, coord, ax, **params):
        """
        Plot all groups
        """
        ranges = coord.backtransform_range(panel_params)
        data['y'] = data['yintercept']
        data['yend'] = data['yintercept']
        data['x'] = ranges.x[0]
        data['xend'] = ranges.x[1]
        data = data.drop_duplicates()

        for _, gdata in data.groupby('group'):
            gdata.reset_index(inplace=True)
            geom_segment.draw_group(gdata, panel_params,
                                    coord, ax, **params)
