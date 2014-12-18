import numpy as np
import vtk


class LeftMouseButton(vtk.vtkInteractorStyleTrackballCamera):
    """Works with a list of entries to see if the user clicks on a legend item.
    """

    def __init__(self, interactor, legend_list):
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressedEvent)
        self.interactor = interactor
        self.legend_list = legend_list
        self.last_x = -1
        self.last_y = -1
        self.deactivated = []

    def leftButtonPressedEvent(self, obj, event):
        self.last_x, self.last_y = self.interactor.GetEventPosition()
        self.OnLeftButtonDown()

    def leftButtonReleaseEvent(self, obj, event):
        x, y = self.interactor.GetEventPosition()

        if self.last_x != x or self.last_y != y:
            self.OnLeftButtonUp()
            return

        for i, (x1, y1, x2, y2) in enumerate(self.legend_list):
            if x > x1 and x < x2 and y < y1 and y > y2:
                if i in self.deactivated:
                    self.deactivated.remove(i)
                else:
                    self.deactivated.append(i)
                self.property.SetScalarOpacity(alpha_fn(self.deactivated))
                break

        self.OnLeftButtonUp()

    def get_deactivated(self):
        return self.deactivated

    def set_property(self, property):
        self.property = property


def rgb_fn(zipped_data):
    fn = vtk.vtkColorTransferFunction()
    for point, color in zipped_data:
        # Ensure float and not hexidecimal
        if any(type(x) is int or x > 1 for x in color):
            color = [float(i) / float(255) for i in color]
        fn.AddRGBPoint(point, *color)
    return fn


def alpha_fn(deactivated):
    fn = vtk.vtkPiecewiseFunction()
    fn.AddPoint(0, 0)
    for i in range(1, 16):
        fn.AddPoint(i, 0.0 if i - 1 in deactivated else 0.3)
    fn.AddPoint(16, 0)
    return fn


ORGAN_INFO = [(1, (1., 0., 0.), "Blood"),
              (2, (.3, .4, 1.), "Brain"),
              (3, (.6, .5, .2), "Duodenum"),
              (4, (.9, .9, .9), "Eye white"),
              (5, (.2, .7, .3), "Retina"),
              (6, (1., .2, .4), "Heart"),
              (7, (.9, .6, .2), "Ileum"),
              (8, (.8, .4, .6), "Kidney"),
              (9, (1., 1., .5), "Large intestine"),
              (10, (.9, .7, .4), "Liver"),
              (11, (.4, .5, .3), "Lungs"),
              (12, (.3, 1., 1.), "Nerve"),
              (13, (.8, .8, .8), "Skeleton"),
              (14, (0., 1., .3), "Spleen"),
              (15, (.5, .35, 0.), "Stomach")]

ORGAN_FN = rgb_fn(zip(*zip(*ORGAN_INFO)[:-1]))
ORGAN_COLORS = zip(*zip(*ORGAN_INFO)[1:])
LEGEND_WIDTH = 200
LEGEND_HEIGHT = 300


def read_data(filepattern, data_spacing, data_extent):
    dims = data_extent[1] + 1, data_extent[3] + 1
    dtype = np.dtype('B')
    file_range = xrange(1, data_extent[5] + 1)
    dat = np.array([np.reshape(np.fromfile(filepattern % i, dtype=dtype), dims)
                    for i in file_range]).tostring()
    data_reader = vtk.vtkImageImport()
    data_reader.CopyImportVoidPointer(dat, len(dat))
    data_reader.SetDataScalarTypeToUnsignedChar()
    data_reader.SetNumberOfScalarComponents(1)
    data_reader.SetDataSpacing(*data_spacing)
    data_reader.SetDataExtent(*data_extent)
    data_reader.SetWholeExtent(*data_extent)
    return data_reader


def make_legend(entries):
    legend = vtk.vtkLegendBoxActor()
    legend.SetNumberOfEntries(len(entries))

    legendBox = vtk.vtkCubeSource()
    legendBox.Update()
    for i, (color, label) in enumerate(entries):
        legend.SetEntry(i, legendBox.GetOutput(), label, color)

    legend.GetPositionCoordinate().SetCoordinateSystemToDisplay()
    legend.GetPositionCoordinate().SetValue(0, 0)

    legend.GetPosition2Coordinate().SetCoordinateSystemToDisplay()
    legend.GetPosition2Coordinate().SetValue(LEGEND_WIDTH, LEGEND_HEIGHT)
    return legend, make_legend_locations(entries)


def make_legend_locations(entries):
    legend_box_height = LEGEND_HEIGHT / float(len(entries))

    legend_boxes = []
    for i in range(len(entries)):
        x1 = 0
        y1 = LEGEND_HEIGHT - (i * legend_box_height)
        x2 = LEGEND_WIDTH
        y2 = y1 - legend_box_height
        legend_boxes.append((x1, y1, x2, y2))
    return legend_boxes


if __name__ == "__main__":
    SPACING = (1, 1, 1.5)
    EXTENT = (0, 499, 0, 469, 1, 136)
    PATTERN = "data/frog.%03d.raw"
    TISSUE_PATTERN = "data/frogTissue.%03d.raw"

    renderer = vtk.vtkOpenGLRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_interactor = vtk.vtkRenderWindowInteractor()
    legend_actor, legend_list = make_legend(ORGAN_COLORS)
    mouseButton = LeftMouseButton(render_interactor, legend_list)

    frog = read_data(PATTERN, SPACING, EXTENT)
    frog_tissue = read_data(TISSUE_PATTERN, SPACING, EXTENT)

    frog_contour = vtk.vtkMarchingCubes()
    frog_contour.SetInputConnection(frog.GetOutputPort())
    frog_contour.ComputeNormalsOn()
    frog_contour.SetValue(0, 7)

    frog_geometry = vtk.vtkPolyDataMapper()
    frog_geometry.SetInputConnection(frog_contour.GetOutputPort())
    frog_geometry.ScalarVisibilityOff()

    frog_actor = vtk.vtkOpenGLActor()
    frog_actor.SetMapper(frog_geometry)
    frog_actor.GetProperty().SetColor(0.5, 0.5, 0)
    frog_actor.GetProperty().SetOpacity(0.3)

    volume_property2 = vtk.vtkVolumeProperty()
    volume_property2.SetColor(ORGAN_FN)
    volume_property2.SetScalarOpacity(alpha_fn(mouseButton.get_deactivated()))
    mouseButton.set_property(volume_property2)

    render_function = vtk.vtkVolumeRayCastCompositeFunction()
    volume_mapper2 = vtk.vtkVolumeRayCastMapper()
    volume_mapper2.SetVolumeRayCastFunction(render_function)
    volume_mapper2.SetInputConnection(frog_tissue.GetOutputPort())

    volume2 = vtk.vtkVolume()
    volume2.SetMapper(volume_mapper2)
    volume2.SetProperty(volume_property2)

    renderer.AddActor(frog_actor)
    renderer.AddActor(volume2)
    renderer.SetBackground(0.1, 0.1, 0.1)
    render_window.SetSize(500, 500)

    render_interactor.SetInteractorStyle(mouseButton)
    render_interactor.SetRenderWindow(render_window)

    def exit_check(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    render_window.AddObserver("AbortCheckEvent", exit_check)

    renderer.AddActor(legend_actor)

    render_interactor.Initialize()
    render_window.Render()
    render_interactor.Start()
