Exercise cram script with determenistic output that consumes extra stdin if any after each command
Every command has deterministic asserted output:

  $ alias consume="$TESTDIR"/consume-stdin.py
  $ consume ; printf '%s\n' "chunk-0001-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0001-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0002-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0002-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0003-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0003-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0004-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0004-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0005-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0005-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0006-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0006-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0007-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0007-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0008-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0008-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0009-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0009-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0010-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0010-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0011-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0011-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0012-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0012-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0013-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0013-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0014-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0014-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0015-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0015-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0016-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0016-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0017-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0017-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0018-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0018-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0019-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0019-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0020-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0020-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0021-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0021-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0022-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0022-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0023-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0023-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0024-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0024-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0025-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0025-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0026-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0026-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0027-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0027-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0028-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0028-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0029-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0029-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0030-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0030-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0031-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0031-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0032-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0032-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0033-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0033-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0034-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0034-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0035-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0035-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0036-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0036-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0037-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0037-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0038-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0038-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0039-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0039-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0040-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0040-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0041-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0041-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0042-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0042-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0043-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0043-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0044-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0044-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0045-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0045-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0046-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0046-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0047-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0047-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
  $ consume ; printf '%s\n' "chunk-0048-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu"
  chunk-0048-alpha-bravo-charlie-delta-echo-foxtrot-golf-hotel-india-juliet-kilo-lima-mike-november-oscar-papa-quebec-romeo-sierra-tango-uniform-victor-whiskey-xray-yankee-zulu
