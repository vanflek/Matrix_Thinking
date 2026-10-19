# Optional patches

Each unified patch transforms a scratch file named `main.py`.

- `patch_21_01_to_02.patch` through `patch_21_10_to_11.patch`: consecutive steps.
- `patch_21_final_to_solution_26.patch` through `patch_21_final_to_solution_30.patch`:
  five independent branches from the unmodified final program.

Use `git apply --check path/to/file.patch` before `git apply path/to/file.patch`.
The full source and target programs are included in the neighboring folders.
No patch is required to run those complete files.

`patch_21_final_to_three_levels.patch` is another independent branch from the
final game and adds the three-wave creative extension in `bonus/`.
