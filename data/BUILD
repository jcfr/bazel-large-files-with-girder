
#
# Very small file directly added to the source tree can be
# exported using "exports_files". Exporting a file is required
# so that it can be added as test dependency using this.
#

#exports_files([
#  "very_small_dragon.obj"
#])


#
# Larger file associated with a key file and available
# on Girder file server can be added as a test dependency
# after specifying a rule that will automatically download
# them when needed.
#

genrule(
  name="download_dragon_obj",
  srcs=["dragon.obj.sha512"],
  outs=["dragon.obj"],
  cmd="$(location //tools:download_data) $(location dragon.obj.sha512) $@",
  tools=["//tools:download_data"],
  visibility=["//visibility:public"],
)

