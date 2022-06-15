Set up an empty test which should be detected as test but skipped

  $ touch empty.t

Set up some folders so we can provide an relative path

  $ mkdir -p dir/subdir

Check if . is accepted as relative path

  $ prysk ./empty.t
  s
  # Ran 1 tests, 1 skipped, 0 failed.

Check if .. is accepted as relative path

  $ cd dir/subdir && prysk ../..
  s
  # Ran 1 tests, 1 skipped, 0 failed.

