# stlviewer

This is simple STL model viewer.

## Prerequisites

For building:

* git
* docker

and for uploading the compiled executable:

* python
* virtualenv-wrapper

## Building stlviewer

The following instructions allow to build the `stlviewer` executable by statically linking
it against VTK.

**Note:** Instructions are specific to Linux but could be adapted to MacOSX or Windows.

* Step 1: Pull `dockcross/manylinux-x64` image to build executable and libraries compatible with wide range of linux distributions.

```
docker pull dockcross/manylinux-x64
docker run dockcross/manylinux-x64 > ~/bin/dockcross-manylinux-x64
```

* Step 2: Build VTK and stlviewer

```
# Download VTK source
cd thirdparty
git clone https://gitlab.kitware.com/vtk/vtk.git VTK

# Build VTK
dockcross-manylinux-x64 bash -c "gosu root yum install -y libXt-devel mesa-libGL-devel;cmake -BVTK-build -HVTK -DCMAKE_BUILD_TYPE:STRING=Release -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_TESTING:BOOL=OFF -G Ninja;cd VTK-build;ninja"

# Build stlviewer
dockcross-manylinux-x64 bash -c "gosu root yum install -y libXt-devel mesa-libGL-devel;cmake -Bstlviewer-build -Hstlviewer -DCMAKE_BUILD_TYPE:STRING=Release -G Ninja -DVTK_DIR:PATH=/work/VTK-build;cd stlviewer-build;ninja"
```

## Releasing stlviewer

* Step 3: Archive and upload the viewer as a Github release

```
mkvirtualenv stlviewer_upload
pip install githubrelease

# Remove uneeded symbols
strip ./stlviewer-build/stlviewer

# Create .tar.gz
tar -C ./stlviewer-build -czvf stlviewer-linux-amd64.tar.gz stlviewer

# Set personal GitHub token
export GITHUB_TOKEN=<token>

# Create release
githubrelease release jcfr/bazel-large-files-with-girder create stlviewer --publish

# Delete existing assets (if any)
githubrelease asset jcfr/bazel-large-files-with-girder delete stlviewer "*"

# Upload
githubrelease asset jcfr/bazel-large-files-with-girder upload stlviewer stlviewer-linux-amd64.tar.gz
```

