#!/usr/bin/env python

import vtk


def in_box(x0, y0, x1, y1, x2, y2):
    """ returns true if coordinate x0, y0 is in the box specified by coordinate
    x1, y1 and x2, y2 """
    return 

class LeftMouseButton(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, interactor, legend_list):
        self.AddObserver("LeftButtonReleaseEvent",self.leftButtonReleaseEvent)
        self.interactor = interactor
        self.legend_list = legend_list

    def leftButtonReleaseEvent(self,obj,event):
        x, y = self.interactor.GetEventPosition()

        for i, (x1, y1, x2, y2) in enumerate(self.legend_list):
            if x > x1 and x < x2 and y < y1 and y > y2:
                print 'clikced legend item', i
                break

        self.OnLeftButtonUp()


ORGAN_INFO = [
    (2, (0.309804, 0.435294, 1.000000), "Brain"),
    (12, (0.309804, 1.000000, 1.000000), "Nerve"),
    (4, (0.333333, 0.501961, 0.000000), "Eye retina"),
    (5, (0.721569, 0.886275, 0.400000), "Eye white"),
    (1, (1., 0., 0.), "Blood"),
    (6, (0.831373, 0.207843, 0.560784), "Heart"),
    (8, (0.831373, 0.372549, 0.631373), "Kidney"),
    (11, (0.431373, 0.000000, 0.243137), "Lung"),
    #(15, (0.8, 0.6, 0.2), "Stomach"),
    (15, (0.537255, 0.356863, 0.000000), "Stomach"),
    #(15, (0.823529, 0.549020, 0.000000), "Stomach"),
    (3, (0.6, 0.5, 0.2), "Duodenum"),
    #(3, (0.537255, 0.356863, 0.000000), "Duodenum"),
    (7, (0.913725, 0.686275, 0.227451), "Ileum"),
    #(7, (0.619608, 0.462745, 0.152941), "Ileum"),
    (9, (1., 1., 0.5), "Large intestine"),
    #(9, (0.913725, 0.686275, 0.227451), "Large intestine"),
    (10, (0.913725, 0.745098, 0.411765), "Liver"),
    (13, (1., 1., 1.), "Skeleton") ]


LEGEND_WIDTH = 150
LEGEND_HEIGHT = 300

def make_legend(entries):
    """ accept a list of tuples of format: [ ( (r, g, b), name), ... ]
    returns a tuple on the first index the actor that is the legend actor, and
    on the second index a tuple with top left coordinate and bottom right
    coordinate """
    legend = vtk.vtkLegendBoxActor()
    legend.SetNumberOfEntries(len(entries))

    legendBox = vtk.vtkCubeSource()
    legendBox.Update()
    i = 0
    for color, label in entries:
        print i, label
        legend.SetEntry(i, legendBox.GetOutput(), label, color)
        i += 1

    legend.GetPositionCoordinate().SetCoordinateSystemToDisplay()
    legend.GetPositionCoordinate().SetValue(0, 0)

    legend.GetPosition2Coordinate().SetCoordinateSystemToDisplay()
    legend.GetPosition2Coordinate().SetValue(LEGEND_WIDTH, LEGEND_HEIGHT)
    return legend, make_legend_locations(entries)

def make_legend_locations(entries):
    """ accept a list of tuples of format: [ ( (r, g, b), name), ... ] """

    legend_box_height = LEGEND_HEIGHT / float(len(entries))

    legend_boxes = []
    for i in range(len(entries)):
        x1 = 0
        y1 = LEGEND_HEIGHT - (i * legend_box_height)
        x2 = LEGEND_WIDTH
        y2 = y1 - legend_box_height
        legend_boxes.append( (x1, y1, x2, y2))
    return legend_boxes

legend_actor, legend_list = make_legend(map(lambda x: x[1:], ORGAN_INFO))

source = vtk.vtkSphereSource()
source.SetCenter(0, 0, 0)
source.SetRadius(1)
source.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
#renderer.SetBackground(1, 1, 1)
renderer.AddActor(actor)
renderer.AddActor(legend_actor)

renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(LeftMouseButton(interactor, legend_list))
interactor.SetRenderWindow(renwin)

interactor.Initialize()
interactor.Start()
