import vtk


def read_data():
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName("data/SMRX.vtk")
    reader.Update()
    return reader


def make_stream_actors(position, color):
    """Create a stream and use two mappers. One to represent velocity with
    the default colour, and the other to change the colour.
    """
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

    # Solid transparent colour
    stream_mapper1 = vtk.vtkPolyDataMapper()
    stream_mapper1.SetInputConnection(stream_tube.GetOutputPort())
    stream_mapper1.ScalarVisibilityOff()

    stream_actor1 = vtk.vtkActor()
    stream_actor1.GetProperty().SetColor(*color)
    stream_actor1.SetMapper(stream_mapper1)
    stream_actor1.GetProperty().SetOpacity(0.4)

    # opaque velocity colour
    stream_mapper2 = vtk.vtkPolyDataMapper()
    stream_mapper2.SetInputConnection(stream_tube.GetOutputPort())

    stream_actor2 = vtk.vtkActor()
    stream_actor2.SetMapper(stream_mapper2)
    stream_actor2.GetProperty().SetOpacity(1.)
    return [stream_actor1, stream_actor2]

if __name__ == '__main__':
    mixer = read_data()

    mixer_contour = vtk.vtkMarchingCubes()
    mixer_contour.SetInputConnection(mixer.GetOutputPort())
    mixer_contour.ComputeNormalsOn()
    mixer_contour.SetValue(0, 1)

    stream_actors = make_stream_actors((0, 15, 30), (0, 1, 0))
    stream_actors += make_stream_actors((0, 45, 30), (0, 0, 1))

    mixer_geometry = vtk.vtkPolyDataMapper()
    mixer_geometry.SetInputConnection(mixer_contour.GetOutputPort())
    mixer_geometry.ScalarVisibilityOff()

    mixer_actor = vtk.vtkOpenGLActor()
    mixer_actor.SetMapper(mixer_geometry)
    mixer_actor.GetProperty().SetColor(.5, .5, .5)
    mixer_actor.GetProperty().SetOpacity(1.)

    # Standard vtk environment stuff
    renderer = vtk.vtkOpenGLRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_interactor = vtk.vtkRenderWindowInteractor()

    renderer.AddActor(mixer_actor)
    for actor in stream_actors:
        renderer.AddActor(actor)
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
