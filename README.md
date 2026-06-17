final project
for i in {1..15}; do ssh -o ConnectTimeout=2 -o NumberOfPasswordPrompts=1 fakeuser@127.0.0.1; done
