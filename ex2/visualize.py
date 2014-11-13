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
    reader.SetDataByteOrderToBigEndian()
    reader.UpdateWholeExtent()
    return reader.GetOutput()


question = 7  # 5 or 6 or 7

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--contour', metavar='contour', type=float,
                        default=[.65], nargs='+')
    parser.add_argument('-r', '--range', metavar='range', type=str)
    args = parser.parse_args()

    # read data
    image_data = get_image_data()

    # 0 -> 65535 (= 2^16 - 1 = max short)
    min = image_data.GetScalarTypeMin()
    max = image_data.GetScalarTypeMax()

    # Filter the contour
    contour_filter = vtk.vtkMarchingCubes()
    contour_filter.SetInput(image_data)

    if question == 5:
        contour_filter.ComputeScalarsOff()

    if not args.contour:
        contour_filter.SetValue(0, (min + max) / 2)
    else:
        for i, val in enumerate(args.contour):
            assert(val > 0)
            assert(val <= 1)
            contour_filter.SetValue(i, int(val * max))

    # PolyMapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(contour_filter.GetOutput())

    if question == 6:
        mapper.ScalarVisibilityOff()
    if args.range:
        vals = args.range.split(',')
        range_min = int(float(vals[0]) * max)
        range_max = int(float(vals[1]) * max)
        mapper.SetScalarRange(range_min, range_max)

    volume_property2 = vtk.vtkVolumeProperty()
    # Actor
    actor = vtk.vtkOpenGLActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 1)  # colors.green_to_white(0, 255))
    actor.GetProperty().SetOpacity(0.3)  # colors.default_opacity(0, 255, 0.5))

    # question 6
    actor.GetProperty().SetColor(.8, .8, .8)

    # Set up renderer, render window and interactor
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.329412, 0.34902, 0.427451)
    renderer.AddActor(actor)
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    interactor.Initialize()
    window.Render()
    interactor.Start()
