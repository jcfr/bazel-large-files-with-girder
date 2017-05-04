cmake_minimum_required(VERSION 3.8)

project(stlviewer)

find_package(VTK REQUIRED)
vtk_module_config(VTK
  vtkCommonCore
  vtkInteractionStyle
  vtkIOGeometry
  vtkRendering${VTK_RENDERING_BACKEND}
  vtkRenderingLOD
)
include(${VTK_USE_FILE})

add_executable(stlviewer main.cxx)
target_link_libraries(stlviewer ${VTK_LIBRARIES})
