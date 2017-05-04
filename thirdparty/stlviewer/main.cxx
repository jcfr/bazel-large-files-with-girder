
// VTK includes
#include <vtkActor.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkNew.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSmartPointer.h>
#include <vtkSTLReader.h>

// STD includes
#include <string>
#include <vector>

int main(int argc, char* argv[])
{
  if (argc != 2)
    {
    std::cout << "usage: " << argv[0] << " /path/to/file.stl" << std::endl;
    return EXIT_FAILURE;
    }
  
  vtkNew<vtkSTLReader> part;
  part->SetFileName(argv[1]);
  
  vtkNew<vtkPolyDataMapper> partMapper;
  partMapper->SetInputConnection(part->GetOutputPort());

  vtkNew<vtkActor> partActor;
  partActor->SetMapper(partMapper.GetPointer());

  vtkNew<vtkRenderer> ren;
  ren->SetBackground( 0.1, 0.2, 0.4 );

  vtkNew<vtkRenderWindow> renWin;
  renWin->AddRenderer(ren.GetPointer());
  renWin->SetSize( 600, 600 );

  vtkNew<vtkRenderWindowInteractor> iren;
  iren->SetRenderWindow(renWin.GetPointer());

  iren->SetInteractorStyle(
    vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New());

  ren->AddActor(partActor.GetPointer());

  iren->Initialize();
  iren->Start();
}

