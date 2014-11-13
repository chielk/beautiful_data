import sys
import argparse
from vtk import (vtkImageReader2, vtkRenderer, vtkRenderWindowInteractor,
        vtkRenderWindow, vtkRenderWindowInteractor, vtkContourFilter,
        vtkPolyDataMapper, vtkLODActor, vtkSmoothPolyDataFilter)


def get_image_data():
    reader = vtkImageReader2()
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
    parser.add_argument('--contour', metavar='contour', type=float, nargs='+')
    parser.add_argument('-r', '--range', metavar='range', type=str)
    args = parser.parse_args()

    # read data
    image_data = get_image_data()

    # 0 -> 65535 (= 2^16 - 1 = max short)
    min = image_data.GetScalarTypeMin()
    max = image_data.GetScalarTypeMax()

    # Filter the contour
    contour_filter = vtkContourFilter()
    contour_filter.SetInput(image_data)

    if question == 5:
        contour_filter.ComputeScalarsOff()

    if not args.contour:
        contour_filter.SetValue(min, (min + max) / 2)
    else:
        for i, val in enumerate(args.contour):
            assert(val > 0)
            assert(val <= 1)
            contour_filter.SetValue(i, int(val * max))

    # PolyMapper
    mapper = vtkPolyDataMapper()
    mapper.SetInput(contour_filter.GetOutput())

    if question == 6:
        mapper.ScalarVisibilityOff()
    if args.range:
        vals = args.range.split(',')
        range_min = int(float(vals[0]) * max)
        range_max = int(float(vals[1]) * max)
        mapper.SetScalarRange(range_min, range_max)

    # Actor
    actor = vtkLODActor()
    actor.SetMapper(mapper)
    actor.SetNumberOfCloudPoints(100000)

    # question 6
    actor.GetProperty().SetColor(.8, .8, .8)

    # Set up renderer, render window and interactor
    renderer = vtkRenderer()
    renderer.SetBackground(0.329412, 0.34902, 0.427451)
    renderer.AddActor(actor)
    window = vtkRenderWindow()
    window.AddRenderer(renderer)
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    interactor.Initialize()
    window.Render()
    interactor.Start()
