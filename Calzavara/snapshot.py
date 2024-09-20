def func(x):
    return x+1

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    pierino = str(func(5))
    snapshot.assert_match(pierino, 'foo_output.txt')
