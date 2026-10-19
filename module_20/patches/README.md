# Sequential patches

Copy `steps/iteration_20_01_skeleton.py` to `main.py` in this module folder.
Apply patches one at a time, in numerical order, from the module folder:

```console
git apply --check patches/patch_20_01_to_02.patch
git apply patches/patch_20_01_to_02.patch
python main.py
```

Each patch transforms the unchanged preceding iteration into the next complete
iteration. If you have made your own experiments, keep a separate copy and
restore the expected preceding iteration before applying a patch.

Patch 08-to-09 switches to the temporary translate-before-rotate experiment and
sets the angle to 90 degrees. Patch 09-to-10 restores the standard TRS order,
the 30-degree starting angle, and adds keyboard controls.

Git is needed only to apply these optional patches. You can instead open any
complete file from `steps/` directly. Solutions are independent copies, not
additional steps in this patch chain.
