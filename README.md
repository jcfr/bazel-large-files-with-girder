# bazel-large-files-with-girder

The intent of this project is to demonstrate how to integrate download of large
data file from [Girder](http://girder.readthedocs.io) with a [bazel](https://bazel.build)
based build system.

Note that principle illustrated here are not specific to Bazel, they have already
been successfully implemented in other build system like [CMake](https://cmake.org)
through the use of [ExternalData](https://cmake.org/cmake/help/latest/module/ExternalData.html) module.

### Demo

This source tree is a simple Bazel project organized like this:
 
```
<root>
  |-- WORKSPACE
  |-- data ........ : Collection key files for large data
  |-- test ........ : Test depending on large data files
  |-- tools  ...... : Girder client script to download files
```

TBD


### Integration with Bazel

#### Overview

The basic idea is to update bazel *test* (or *binary*) targets to depend on *data*
target representing the file to download.
 
In the following example, the test `inspect_dragon` depends on a data *target* `//data:dragon.stl`
that will take care of downloading the file from Girder when executing the test.
 
```python
sh_test(
    name = "inspect_dragon",
    srcs = ["inspect_model.sh"],
    args = ["$(location //data:dragon.stl)"],
    data = ["@stlviewerArchive//:stlviewer", "//data:dragon.stl"],
)
```

### Specifying Girder server and credentials

TBD

#### Data targets

TBD

#### Uploading new data files

TBD

### F.A.Q

#### How are data files referenced ?

Data files are not directly stored in the source tree managed by the version
control system (e.g git), instead a *key* file containing the *hashsum* of the
original data is tracked.
 
The use of a [cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function)
allows to uniquely represent the data file of arbitrary size with string of a
fixed size called *hashsum*.

We will be using SHA-512 function, a collision resistant implementation belonging to
the [SHA-2](https://en.wikipedia.org/wiki/SHA-2) family of hash algorithms.


For example, the key file associated with file named `large_data_file.ext`
could be stored as:

```
data/large_data_file.ext.sha512
```

and contain a 128-character string like:

```
01fdd890676e9b2f7f5a8eb25c01dcdb168d23e3f9d95f804df44ff235a1c022c8f516a4fe5871f37ebaa2188c640c7624c738c71c5f3965924b7bd2f9bab11b
```
 
 
#### How are data file retrieved ?

Given the *hashsum* contained in the key file, the actual file can be downloaded
from Girder using this API endpoint:

```
https://${server}/api/v1/file/hashsum/sha512/${hashsum}/download
```

where `${hashsum}` corresponds to a 128-character string.


#### What are the advantages over Git-LFS ? 

[Git-lfs](https://git-lfs.github.com/) (Git Large File System) extension also allows
to store *pointer* to files found on a data server.

While this approach is also [leveraging *hashsum*](https://github.com/git-lfs/git-lfs/blob/master/docs/spec.md)
to retrieve the original file, worth noting that by default [all data files](https://github.com/git-lfs/git-lfs/blob/master/docs/man/git-lfs-clone.1.ronn)
are downloaded when git cloning a repository.

Since in our case, we are interested in:

* only running a subset of tests depending on a subset of the data files
* potentially caching the downloads globally

... the git-lfs approach is suboptimal. Instead, directly integrating with the build
system allows to leverage its dependency resolution mechanism to selectively download
files.