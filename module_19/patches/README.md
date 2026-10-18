# Sequential transitions

Each patch transforms `main.py` from one complete iteration to the next.
Start with a copy of `steps/iteration_19_01_skeleton.py` at the module root.
Apply patches in ascending order using:

```console
git -c core.autocrlf=false apply --check patches/patch_19_01_to_02.patch
git -c core.autocrlf=false apply patches/patch_19_01_to_02.patch
```

Run `python main.py` after every patch. Patch 09_to_10 adds graph tick labels and
final English comments. All nine transitions were applied and byte-checked.
