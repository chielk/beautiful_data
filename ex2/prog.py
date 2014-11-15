import sys
import argparse
import vtk
# Yo dawg, I heard you like namespaces


def get_image_data():
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

    settings = [ ( (190.0, 200.0), (0.7, 0, 0), 0.1),
                 ( (200, 250), (0, 0.7, 0.7), 0.1),
                 ( (1900, 2100), (0, 0.7, 0), 0.1),
                 ( (2900, 3100), (0, 0, 0.7), 0.1)]
                 #( (max_value * 0.9, max_value), (0, 0.7, 0), 0.4)]
                 #( (max_value * 0.83, max_value * 0.9), (0, 0, 0.7), 0.4)]

    settings2 = [ ( 700, (0.7, 0, 0), 0.2),
                 ( 2000, (0, 0.7, 0), 0.4)]
                 #( (max_value * 0.9, max_value), (0, 0.7, 0), 0.4)]
                 #( (max_value * 0.83, max_value * 0.9), (0, 0, 0.7), 0.4)]

    actors = []

    i = 0
    for min_max, color, opacity in settings:


        print 'min max', min_max
        print 'color', color
        print 'opacity', opacity

        # contour
        data_contour = vtk.vtkMarchingCubes()
        #data_contour.SetInputConnection(data.GetOutputPort())
        data_contour.SetInput(data)
        data_contour.ComputeNormalsOn()
        data_contour.GenerateValues(5, min_max[0], min_max[1])
        #data_contour.SetValue(i, min_max)
        i += 1
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


    ## color (for the volume property)
    #volume_color = vtk.vtkColorTransferFunction()
    #volume_color.AddRGBPoint(1, 0.7, 0, 0)
    #volume_color.AddRGBPoint(2, 0, 0.7, 0)

    ## for the opacity (for the volume property)
    #volume_opacity = vtk.vtkPiecewiseFunction()
    #volume_opacity.AddPoint(1, 0.1)
    #volume_opacity.AddPoint(2, 0.2)

    ## create the volume property (for the volume)
    #volume_property = vtk.vtkVolumeProperty()
    #volume_property.SetColor(volume_color)
    #volume_property.SetScalarOpacity(volume_opacity)

    ## render function (for the mapper)
    #render_function = vtk.vtkVolumeRayCastCompositeFunction()

    ## mapper (volume)
    #volume_mapper = vtk.vtkVolumeRayCastMapper()
    #volume_mapper.SetVolumeRayCastFunction(render_function)
    #volume_mapper.SetInput(data)

    ## actual volume (this is an actor)
    #volume = vtk.vtkVolume()
    #volume.SetMapper(volume_mapper)
    #volume.SetProperty(volume_property)


    # here we do all rendering (has basically nothing to do with the visualization)
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.329412, 0.34902, 0.427451)

    # do not forget to add the actors here:
    for actor in actors:
        renderer.AddActor(actor)
    #renderer.AddActor(volume)

    window = vtk.vtkRenderWindow()
    window.SetSize(500, 500)
    window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.Initialize()
    window.Render()
    interactor.Start()
