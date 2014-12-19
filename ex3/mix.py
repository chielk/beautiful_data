import vtk


def read_data():
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName("data/SMRX.vtk")
    reader.Update()
    return reader

def make_stream_actor(position, color):
    seed = vtk.vtkPointSource()
    seed.SetRadius(15)
    seed.SetNumberOfPoints(100)
    seed.SetCenter(*position)

    stream_tracer = vtk.vtkStreamTracer()
    stream_tracer.SetInputConnection(mixer.GetOutputPort())
    stream_tracer.SetMaximumPropagation(500)
    stream_tracer.SetIntegrator(vtk.vtkRungeKutta45())
    stream_tracer.SetIntegrationDirectionToBoth()
    stream_tracer.SetTerminalSpeed(0.0001)
    stream_tracer.SetSource(seed.GetOutput())

    stream_tube = vtk.vtkTubeFilter()
    stream_tube.SetInputConnection(stream_tracer.GetOutputPort())
    stream_tube.SetRadius(.2)
    stream_tube.SetNumberOfSides(12)

    stream_mapper = vtk.vtkPolyDataMapper()
    stream_mapper.SetInputConnection(stream_tube.GetOutputPort())

    stream_actor = vtk.vtkActor()
    stream_actor.GetProperty().SetColor(*color)
    stream_actor.SetMapper(stream_mapper)
    return stream_actor

if __name__ == '__main__':
    mixer = read_data()

    mixer_contour = vtk.vtkMarchingCubes()
    mixer_contour.SetInputConnection(mixer.GetOutputPort())
    mixer_contour.ComputeNormalsOn()
    mixer_contour.SetValue(0, 7)

    # Yellow
    yellow_stream_actor = make_stream_actor((0, 15, 30), (1, 1, 0))

    # Blue
    blue_stream_actor = make_stream_actor((0, 45, 30), (0, 0, 1))
    blue_stream_actor.GetProperty().SetOpacity(0.15)

    mixer_geometry = vtk.vtkPolyDataMapper()
    mixer_geometry.SetInputConnection(mixer_contour.GetOutputPort())
    mixer_geometry.ScalarVisibilityOff()

    mixer_actor = vtk.vtkOpenGLActor()
    mixer_actor.SetMapper(mixer_geometry)
    mixer_actor.GetProperty().SetColor(0.7, 0.7, 0.7)
    mixer_actor.GetProperty().SetOpacity(0.3)

    # Standard vtk environment stuff
    renderer = vtk.vtkOpenGLRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_interactor = vtk.vtkRenderWindowInteractor()

    renderer.AddActor(mixer_actor)
    renderer.AddActor(yellow_stream_actor)
    renderer.AddActor(blue_stream_actor)
    renderer.SetBackground(0.1, 0.1, 0.1)
    render_window.SetSize(500, 500)

    render_interactor.SetRenderWindow(render_window)

    def exit_check(obj, event):
        if obj.GetEventPending():
            obj.SetAbortRender(1)

    render_window.AddObserver("AbortCheckEvent", exit_check)

    render_interactor.Initialize()
    render_window.Render()
    render_interactor.Start()
