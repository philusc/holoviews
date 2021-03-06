import json
import param

from ..widgets import NdWidget, SelectionWidget, ScrubberWidget

class PlotlyWidget(NdWidget):

    extensionjs = param.String(default='plotlywidgets.js', doc="""
        Optional javascript extension file for a particular backend.""")

    def _get_data(self):
        msg, metadata = self.renderer.components(self.plot, divuuid=self.id, comm=False)
        data = super(PlotlyWidget, self)._get_data()
        return dict(data, init_html=msg['text/html'],
                    init_js=msg['application/javascript'])

    def encode_frames(self, frames):
        frames = json.dumps(frames).replace('</', r'<\/')
        return frames

    def _plot_figure(self, idx, fig_format='json'):
        """
        Returns the figure in html format on the
        first call and
        """
        self.plot.update(idx)
        if self.embed:
            return self.renderer.diff(self.plot)


class PlotlySelectionWidget(PlotlyWidget, SelectionWidget):

    def _get_data(self):
        if not self.plot.dynamic:
            widgets, _, _ = self.get_widgets()
            key = tuple(w['value'] for w in widgets)
            self.plot.update(tuple(key))
        return super(PlotlySelectionWidget, self)._get_data()

class PlotlyScrubberWidget(PlotlyWidget, ScrubberWidget):
    pass
