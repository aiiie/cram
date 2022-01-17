Test that consumes stdin. Cram should not fail on this:

  $ echo 123
  123
  $ cat > /dev/null
  $ echo 456
  456
  $ echo 789
  789
