import sys
import argparse
import vtk
# Yo dawg, I heard you like namespaces


def get_image_data():
    """ Reads the image data using the class vtkImageReader2. Returns
    the result of the GetOutput() function call."""
    reader = vtk.vtkImageReader2()
    reader.SetDataScalarTypeToUnsignedShort()
    reader.SetFileDimensionality(2)
    reader.SetFilePrefix("data/slice")
    reader.SetDataExtent(0, 255, 0, 255, 1, 94)
    reader.SetDataSpacing(1, 1, 2)
    #reader.SetDataByteOrderToBigEndian()
    reader.SetNumberOfScalarComponents( 1 )
    reader.UpdateWholeExtent()
    return reader.GetOutput()

if __name__ == '__main__':
    data = get_image_data() # <- this is a vtkImageReader2().GetOutput()
    min_value = data.GetScalarTypeMin()
    max_value = data.GetScalarTypeMax()

    settings = [ ( (200, 250), (0.7, 0, 0), 0.1),        # skin/hair
                 ( (1800, 2500), (0, 0.7, 0), 0.1),      # skeleton
                 ( (3090, 30000), (0, 0, 0.7), 0.1)      # jaw, teeth and coin?
                ]

    actors = []

    for min_max, color, opacity in settings:

        # contour
        data_contour = vtk.vtkMarchingCubes()
        data_contour.SetInput(data)
        data_contour.ComputeNormalsOn()
        data_contour.GenerateValues(5, min_max[0], min_max[1])
        data_contour.Update()

        # geometry
        data_geometry = vtk.vtkPolyDataMapper()
        data_geometry.SetInputConnection(data_contour.GetOutputPort())
        data_geometry.ScalarVisibilityOff()

        # actor
        data_actor = vtk.vtkOpenGLActor()
        data_actor.SetMapper(data_geometry)
        data_actor.GetProperty().SetColor(*color)
        data_actor.GetProperty().SetOpacity(opacity)

        actors.append(data_actor)

    # to plot the outline
    outline = vtk.vtkOutlineFilter()
    outline.SetInput(data)
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    outline_actor = vtk.vtkOpenGLActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(1, 1, 1)


    # below this point we do all rendering (has basically nothing to do with the visualization)
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.33, 0.35, 0.43)

    # TODO: I try to set the camera here. but oh vtk :(
    #renderer.GetActiveCamera().SetPosition(0, 0, 0)
    #print renderer.GetActiveCamera().GetEyeAngle()
    #renderer.GetActiveCamera().Elevation(-0.1)
    #renderer.UpdateCamera()

    # do not forget to add the actors here:
    for actor in actors:
        renderer.AddActor(actor)
    renderer.AddActor(outline_actor)

    window = vtk.vtkRenderWindow()
    window.SetSize(500, 500)
    window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.Initialize()
    window.Render()
    interactor.Start()
